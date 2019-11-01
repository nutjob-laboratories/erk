#
#  Erk IRC Client
#  Copyright (C) 2019  Daniel Hetrick
#               _   _       _                         
#              | | (_)     | |                        
#   _ __  _   _| |_ _  ___ | |__                      
#  | '_ \| | | | __| |/ _ \| '_ \                     
#  | | | | |_| | |_| | (_) | |_) |                    
#  |_| |_|\__,_|\__| |\___/|_.__/ _                   
#  | |     | |    _/ |           | |                  
#  | | __ _| |__ |__/_  _ __ __ _| |_ ___  _ __ _   _ 
#  | |/ _` | '_ \ / _ \| '__/ _` | __/ _ \| '__| | | |
#  | | (_| | |_) | (_) | | | (_| | || (_) | |  | |_| |
#  |_|\__,_|_.__/ \___/|_|  \__,_|\__\___/|_|   \__, |
#                                                __/ |
#                                               |___/ 
#  https://github.com/nutjob-laboratories
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
from collections import defaultdict
import fnmatch
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_IS_AVAILABLE = False
except Exception as exception:
	SSL_IS_AVAILABLE = False

from erk.common import *
from erk.irc import connect,connectSSL,reconnect,reconnectSSL

import erk.dialogs.edit_user as EditUserDialog
import erk.dialogs.about as AboutDialog
import erk.dialogs.ignore as IgnoreDialog
import erk.dialogs.window_size as WindowSizeDialog

class Connection:
	def __init__(self,obj,ident):
		self.id = ident
		self.connection = obj
		self.windows = {}
		self.console = None
		self.network = 'Unknown'
		self.hostname = 'Unknown'
		self.modes = ''
		self.channel_list = None
		self.motd = None
		self.motd_window = None

class Erk(QMainWindow):

	# |==================|
	# | IRC EVENTS BEGIN |
	# |==================|

	def irc_output(self,obj,line):

		for c in self.connections:
			if c.id==obj.id:
				if c.console:
					c.console.writeLine(line,False)

		if self.view_all_traffic:
			if obj.hostname:
				sid = obj.hostname
			else:
				sid = obj.server+":"+str(obj.port)

			print("->"+sid+"\t"+line)

	def irc_input(self,obj,line):

		for c in self.connections:
			if c.id==obj.id:
				if c.console:
					c.console.writeLine(line,True)

		if self.view_all_traffic:
			if obj.hostname:
				sid = obj.hostname
			else:
				sid = obj.server+":"+str(obj.port)

			print("<-"+sid+"\t"+line)

	def irc_list(self,obj,server,channel,usercount,topic):
		# def add_channel(self,channel):
		topic = topic.strip()

		for c in self.connections:
			if c.id==obj.id:
				if c.channel_list:
					c.channel_list.add_channel(channel,usercount,topic)

	def irc_start_list(self,obj,server):
		# self.x = ListWindow("SERVER",self.MDI,None,self)
		for c in self.connections:
			if c.id==obj.id:
				if c.channel_list==None:
					c.channel_list = ListWindow(server,self.MDI,obj,self)
				else:
					c.channel_list.clear()
					self.restoreWindow(c.channel_list,c.channel_list.subwindow)
				#c.channel_list.disable_refresh()

	def irc_end_list(self,obj,server):
		for c in self.connections:
			if c.id==obj.id:
				#c.channel_list.enable_refresh()
				pass

	def irc_uptime(self,obj,uptime):

		t = convertSeconds(uptime)
		hours = t[0]
		if len(str(hours))==1: hours = f"0{hours}"
		minutes = t[1]
		if len(str(minutes))==1: minutes = f"0{minutes}"
		seconds = t[2]
		if len(str(seconds))==1: seconds = f"0{seconds}"
		if self.display_uptime_seconds:
			display = f"{hours}:{minutes}:{seconds}"
		else:
			display = f"{hours}:{minutes}"

		for c in self.connections:
			if c.id==obj.id:
				c.console.uptime_display(display)
				for channel in c.windows:
					c.windows[channel].uptime_display(display)

	def irc_is_away(self,obj,message):
		dmsg = "You have been marked as being away"
		self.serverLog(obj,dmsg)

		for c in self.connections:
			if c.id==obj.id:
				for channel in c.windows:
					c.windows[channel].is_away = True
					c.windows[channel].update_nick(obj.nickname)

		rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],dmsg )
		try:
			w = self.MDI.activeSubWindow()
			win = w.window
			if win.is_console: return
			win.writeText(rmsg)
		except:
			pass

	def irc_not_away(self,obj,message):
		dmsg = "You are no longer marked as being away"
		self.serverLog(obj,dmsg)

		for c in self.connections:
			if c.id==obj.id:
				for channel in c.windows:
					c.windows[channel].is_away = False
					c.windows[channel].update_nick(obj.nickname)

		rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],dmsg )
		try:
			w = self.MDI.activeSubWindow()
			win = w.window
			if win.is_console: return
			win.writeText(rmsg)
		except:
			pass

	def irc_user_away(self,obj,user,message):
		dmsg = user+" is away: "+message
		self.serverLog(obj,dmsg)

		rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],dmsg )
		try:
			w = self.MDI.activeSubWindow()
			win = w.window
			if win.is_console: return
			if win.is_channel: return
			win.writeText(rmsg)
		except:
			pass

	def irc_invited(self,obj,user,target,channel):
		if self.is_ignored(obj,user): return

		if target==obj.nickname:
			# the client was invited
			dmsg = user+" invited you to "+channel
			self.serverLog(obj,dmsg)

			rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],dmsg )
			try:
				w = self.MDI.activeSubWindow()
				win = w.window
				if win.is_console: return
				win.writeText(rmsg)
			except:
				pass
		else:
			p = user.split('!')
			if len(p)==2:
				user = p[0]
				self.update_user_hostmask(obj,p[0],p[1])

			dmsg = user+" invited "+target+" to the channel"
			rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],dmsg )
			self.writeToChannel(obj,channel,rmsg)
			self.writeToChannelLog(obj,channel,'',dmsg)

	def irc_inviting(self,obj,target,channel):

		dmsg = "Invitation to "+channel+" sent to "+target
		self.serverLog(obj,dmsg)

		rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],dmsg )
		try:
			w = self.MDI.activeSubWindow()
			win = w.window
			if win.is_console: return
			win.writeText(rmsg)
		except:
			pass

	def irc_you_are_oper(self,obj):
		rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],"You are an IRC operator" )
		self.serverLog(obj,"You are an IRC operator")

		try:
			w = self.MDI.activeSubWindow()
			win = w.window
			if win.is_console: return
			win.writeText(rmsg)
		except:
			pass

	def irc_options(self,obj,optiondata):
		for c in self.connections:
			if c.id==obj.id:
				c.console.server_options(optiondata)

		self.buildConnectionsMenu()

	def irc_whois(self,obj,whoisdata):

		self.update_user_hostmask(obj,whoisdata.nickname,whoisdata.username+"@"+whoisdata.host)

		pretty = datetime.fromtimestamp(int(whoisdata.signon)).strftime('%B %d, %Y at %H:%M:%S')

		if int(whoisdata.idle)>1:
			suffix = "s"
		else:
			suffix = ""

		wd = [
			render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[WHOIS_STYLE_NAME],whoisdata.nickname,self.styles[WHOIS_TEXT_STYLE_NAME],"("+whoisdata.username+"@"+whoisdata.host+"): "+whoisdata.realname ),
			render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[WHOIS_STYLE_NAME],whoisdata.nickname,self.styles[WHOIS_TEXT_STYLE_NAME],whoisdata.channels ),
			render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[WHOIS_STYLE_NAME],whoisdata.nickname,self.styles[WHOIS_TEXT_STYLE_NAME],"Connected to "+whoisdata.server ),
			render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[WHOIS_STYLE_NAME],whoisdata.nickname,self.styles[WHOIS_TEXT_STYLE_NAME],whoisdata.privs ),
			render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[WHOIS_STYLE_NAME],whoisdata.nickname,self.styles[WHOIS_TEXT_STYLE_NAME],"Idle "+whoisdata.idle+" second"+suffix),
			render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[WHOIS_STYLE_NAME],whoisdata.nickname,self.styles[WHOIS_TEXT_STYLE_NAME],"Signed on "+pretty ),
		]

		try:
			w = self.MDI.activeSubWindow()
			win = w.window
			for line in wd:
				win.writeText(line)
		except:
			pass


	def irc_kick(self,obj,target,channel,kicker,message):
		p = kicker.split("!")
		if len(p)==2:
			kicker=p[0]
			self.update_user_hostmask(obj,p[0],p[1])

		if len(message)>0:
			dmsg = kicker+" kicked "+target+" from "+channel+" ("+message+")"
		else:
			dmsg = kicker+" kicked "+target+" from "+channel

		self.serverLog(obj,dmsg)

		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					clean = []
					dont_display_kick = c.windows[channel].ignore_kick_messages
					for u in c.windows[channel].users:
						p = u.split('!')
						if len(p)==2:
							tnick = p[0]
						else:
							tnick = u
						tnick = tnick.replace('@','')
						tnick = tnick.replace('!','')
						if tnick==target: continue
						clean.append(u)
					c.windows[channel].users = clean
					c.windows[channel].refreshUserlist()

		if not dont_display_kick:
			rmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],dmsg )
			self.writeToChannel(obj,channel,rmsg)
			self.writeToChannelLog(obj,channel,'',dmsg)

	def irc_parting(self,obj,channel):
		self.is_parting.append(channel)

		for c in self.connections:
			if c.id==obj.id:
				for chan in c.windows:
					if c.windows[chan].name==channel:
						c.windows[chan].close()
						del c.windows[chan]
						break

		self.serverLog(obj,"You have left "+channel)
		self.buildWindowMenu()

	def irc_close_user_chat(self,obj,channel):

		for c in self.connections:
			if c.id==obj.id:
				for chan in c.windows:
					if c.windows[chan].name==channel:
						c.windows[chan].close()
						del c.windows[chan]
						break

		self.buildWindowMenu()

	def irc_kicked(self,obj,channel,kicker,message):
		self.is_parting.append(channel)
		p = kicker.split('!')
		if len(p)==2:
			kicker = p[0]
			self.update_user_hostmask(obj,p[0],p[1])

		for c in self.connections:
			if c.id==obj.id:
				for chan in c.windows:
					if c.windows[chan].name==channel:
						c.windows[chan].close()
						del c.windows[chan]
						break

		if len(message)>0:
			self.serverLog(obj,kicker+" kicked you from "+channel+" ("+message+")")
		else:
			self.serverLog(obj,kicker+" kicked you from "+channel)

		self.buildWindowMenu()

	def irc_quit(self,obj,user,qmsg):
		p = user.split('!')
		if len(p)==2:
			user = p[0]
			self.update_user_hostmask(obj,p[0],'')

		if qmsg!='':
			self.serverLog(obj,user+" has quit IRC ("+qmsg+")")
		else:
			self.serverLog(obj,user+" has quit IRC")

		for c in self.connections:
			if c.id==obj.id:
				for channel in c.windows:
					if not c.windows[channel].is_channel: continue
					dont_display_quit = c.windows[channel].ignore_quit_messages
					clean = []
					found = False
					for u in c.windows[channel].users:
						p = u.split('!')
						if len(p)==2:
							tnick = p[0]
						else:
							tnick = u
						tnick = tnick.replace('@','')
						tnick = tnick.replace('!','')
						if tnick==user:
							found = True
							continue
						clean.append(u)

					if found:
						c.windows[channel].users = clean
						c.windows[channel].refreshUserlist()

						if not dont_display_quit:
							if qmsg!='':
								msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],user+" has quit IRC ("+qmsg+")" )
								self.writeToChannel(obj,channel, msg )
								self.writeToChannelLog(obj,channel,'',user+" has quit IRC ("+qmsg+")")
							else:
								msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],user+" has quit IRC" )
								self.writeToChannel(obj,channel, msg )
								self.writeToChannelLog(obj,channel,'',user+" has quit IRC")


	def irc_error(self,obj,msg):

		emsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[ERROR_STYLE_NAME],msg )
		self.writeToConsole(obj,emsg)

		try:
			w = self.MDI.activeSubWindow()
			win = w.window
			if win.is_console: return
			win.writeText(emsg)
		except:
			pass

	def irc_mode(self,obj,user,channel,mset,modes,args):

		if len(modes)<1: return

		args = list(args)

		if channel==obj.nickname:
			for c in self.connections:
				if c.id==obj.id:
					if mset:
						for m in modes:
							c.modes = c.modes + m
						msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],"Mode +"+modes+" set on "+channel )
					else:
						for m in modes:
							c.modes = c.modes.replace(m,'')
						msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],"Mode -"+modes+" set on "+channel )
			self.writeToConsole(obj,msg)
			self.writeToConsoleLog(obj,'',msg)
			self.buildConnectionsMenu()
			return

		cleaned = []
		for a in args:
			if a == None: continue
			cleaned.append(a)
		args = cleaned

		p = user.split('!')
		if len(p)==2:
			user = p[0]
			self.update_user_hostmask(obj,p[0],p[1])

		reportadd = []
		reportremove = []

		get_names = False

		for m in modes:

			if m=="k":
				if len(args)>0:
					n = args.pop(0)
				else:
					n = None
				if mset:
					if n:
						msg = f"{user} set {channel}'s channel key to \"{n}\""
						self.setChannelKey(obj,channel,n)
						self.setChannelMode(obj,channel,"k")
					else:
						msg = ''
				else:
					msg = f"{user} unset {channel}'s channel key"
					self.setChannelKey(obj,channel,'')
					self.unsetChannelMode(obj,channel,"k")
				if len(msg)>0:
					dmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],msg )
					self.writeToChannel(obj,channel,dmsg)
					self.writeToChannelLog(obj,channel,'',msg)
				continue

			if m=="o":
				if len(args)>0:
					n = args.pop(0)
				else:
					n = None
				if mset:
					if n:
						msg = f"{user} granted {channel} operator status to {n}"
					else:
						msg = ''
				else:
					if n:
						msg = f"{user} took {channel} operator status from {n}"
					else:
						msg = ''
				if len(msg)>0:
					dmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],msg )
					self.writeToChannel(obj,channel,dmsg)
					self.writeToChannelLog(obj,channel,'',msg)
					get_names = True
				continue

			if m=="v":
				if len(args)>0:
					n = args.pop(0)
				else:
					n = None
				if mset:
					if n:
						msg = f"{user} granted {channel} voiced status to {n}"
					else:
						msg = ''
				else:
					if n:
						msg = f"{user} took {channel} voiced status from {n}"
					else:
						msg = ''
				if len(msg)>0:
					dmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],msg )
					self.writeToChannel(obj,channel,dmsg)
					self.writeToChannelLog(obj,channel,'',msg)
					get_names = True
				continue

			if m=="b":
				if mset:
					for u in args:
						msg = f"{user} banned {u} from {channel}"
						dmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],msg )
						self.writeToChannel(obj,channel,dmsg)
						self.writeToChannelLog(obj,channel,'',msg)
				else:
					for u in args:
						msg = f"{user} unbanned {u} from {channel}"
						dmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],msg )
						self.writeToChannel(obj,channel,dmsg)
						self.writeToChannelLog(obj,channel,'',msg)
				continue

			if m=="c":
				if mset:
					self.setChannelMode(obj,channel,"c")
					reportadd.append("c")
				else:
					self.unsetChannelMode(obj,channel,"c")
					reportremove.append("c")
				continue

			if m=="C":
				if mset:
					self.setChannelMode(obj,channel,"C")
					reportadd.append("C")
				else:
					self.unsetChannelMode(obj,channel,"C")
					reportremove.append("C")
				continue

			if m=="m":
				if mset:
					self.setChannelMode(obj,channel,"m")
					reportadd.append("m")
				else:
					self.unsetChannelMode(obj,channel,"m")
					reportremove.append("m")
				continue

			if m=="n":
				if mset:
					self.setChannelMode(obj,channel,"n")
					reportadd.append("n")
				else:
					self.unsetChannelMode(obj,channel,"n")
					reportremove.append("n")
				continue

			if m=="p":
				if mset:
					self.setChannelMode(obj,channel,"p")
					reportadd.append("p")
				else:
					self.unsetChannelMode(obj,channel,"p")
					reportremove.append("p")
				continue

			if m=="s":
				if mset:
					self.setChannelMode(obj,channel,"s")
					reportadd.append("s")
				else:
					self.unsetChannelMode(obj,channel,"s")
					reportremove.append("s")
				continue

			if m=="t":
				if mset:
					self.setChannelMode(obj,channel,"t")
					reportadd.append("t")
				else:
					self.unsetChannelMode(obj,channel,"t")
					reportremove.append("t")
				continue

			if mset:
				reportadd.append(m)
			else:
				reportremove.append(m)

		if len(reportadd)>0 or len(reportremove)>0:
			if mset:
				msg = f"{user} set +{''.join(reportadd)} in {channel}"
				dmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],msg )
				self.writeToChannel(obj,channel,dmsg)
				self.writeToChannelLog(obj,channel,'',msg)
			else:
				msg = f"{user} set -{''.join(reportremove)} in {channel}"
				dmsg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],msg )
				self.writeToChannel(obj,channel,dmsg)
				self.writeToChannelLog(obj,channel,'',msg)

		if get_names: obj.sendLine(f"NAMES {channel}")

	def irc_topic(self,obj,user,channel,topic):
		p = user.split('!')
		if len(p)==2:
			user = p[0]
			self.update_user_hostmask(obj,p[0],p[1])
		for c in self.connections:
			if c.id==obj.id:
				for chan in c.windows:
					if c.windows[chan].is_channel:
						if chan==channel:
							c.windows[chan].updateTopic(topic)
							if topic!='':
								if not c.windows[chan].ignore_topic_messages:
									msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],user+" set the topic to \""+topic+"\"" )
									self.writeToChannel(obj,chan,msg)
									self.writeToChannelLog(obj,chan,'',user+" set the topic to \""+topic+"\"")
								# Make sure the app title is updated if necessary
								self.updateActiveChild(self.MDI.activeSubWindow())
							else:
								if user!=obj.hostname:
									if not c.windows[chan].ignore_topic_messages:
										msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],user+" set the topic to nothing" )
										self.writeToChannel(obj,chan,msg)
										self.writeToChannelLog(obj,chan,'',user+" set the topic to nothing")
									# Make sure the app title is updated if necessary
									self.updateActiveChild(self.MDI.activeSubWindow())

	def irc_banlist(self,obj,channel,banlist):
		for c in self.connections:
			if c.id==obj.id:
				for chan in c.windows:
					if c.windows[chan].is_channel:
						if chan==channel:
							c.windows[chan].banlist = banlist
							c.windows[chan].rebuildBanMenu()
							return

	def irc_registered(self,obj):
		c = self.fetchConnection(obj)
		msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],"Registered with "+obj.server+":"+str(obj.port) )
		self.writeToConsole(obj,msg)
		self.writeToConsoleLog(obj,'',msg)

		#obj.join("#quirc")
		#self.autojoins[info.server]

		for serv in self.autojoins:
			if serv == obj.server:
				for channel in self.autojoins[serv]:
					if channel[1]!='':
						obj.join(channel[0],channel[1])
					else:
						obj.join(channel[0])

		if obj.server in self.autojoins: del self.autojoins[obj.server]

		self.buildConnectionsMenu()

	def irc_motd(self,obj,motd):
		c = self.fetchConnection(obj)
		msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],"<br>".join(motd) )
		self.writeToConsole(obj,msg)
		self.writeToConsoleLog(obj,'',"<br>".join(motd))

		c.motd = motd

	def irc_network_and_hostname(self,obj,network,hostname):
		c = self.fetchConnection(obj)
		c.network = network
		c.hostname = hostname
		c.console.hostname = hostname

		self.serverLog(obj,"Server is a part of the  "+network+" network")
		self.serverLog(obj,"Server's hostname is  "+hostname)

		c.console.setWindowTitle(" "+hostname+" ("+network+")")

		c.console.network = network
		nurl = get_network_url(network)
		if nurl:
			c.console.network_url = nurl

		self.buildWindowMenu()

		self.buildConnectionsMenu()

		if self.save_server_history:
			update_history_network(obj.server,obj.port,network)

	def irc_notice(self,obj,user,target,text):
		if not self.window_is_active: self.IS_FLASHING = True
		p = user.split('!')
		if len(p)==2:
			user = p[0]
			self.update_user_hostmask(obj,p[0],p[1])
			if self.is_ignored(obj,p[1]): return

		if self.is_ignored(obj,user): return

		if target.lower()=='auth':
			msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],text )
			self.writeToConsole(obj,msg)
			self.writeToConsoleLog(obj,'',text)
			return

		if obj.hostname==None:
			msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[NOTICE_STYLE_NAME],user,self.styles[NOTICE_TEXT_STYLE_NAME],text )
			self.writeToConsole(obj,msg)
			self.writeToConsoleLog(obj,'&'+user,text)
			return

		# Catch ctcp-action message
		if target==obj.nickname:

			# Check to see if user window exists
			if self.userWindowExists(obj,user):
				msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[NOTICE_STYLE_NAME],user,self.styles[NOTICE_TEXT_STYLE_NAME],text )
				self.writeToChannel(obj,user,msg)
				self.writeToChannelLog(obj,user,'&'+user,text)
				return
			else:
				msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[NOTICE_STYLE_NAME],user,self.styles[NOTICE_TEXT_STYLE_NAME],text )
				try:
					w = self.MDI.activeSubWindow()
					win = w.window
					if not win.is_console:
						win.writeText(rmsg)
				except:
					pass

				self.writeToConsole(obj,msg)
				self.writeToConsoleLog(obj,'&'+user,text)
				return

		msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[NOTICE_STYLE_NAME],user+"/"+target,self.styles[NOTICE_TEXT_STYLE_NAME],text )
		self.writeToChannel(obj,target,msg)
		self.writeToChannelLog(obj,target,'&'+user+"/"+target,text)

	def irc_action(self,obj,user,target,text):
		if not self.window_is_active: self.IS_FLASHING = True
		p = user.split('!')
		if len(p)==2:
			user = p[0]
			self.update_user_hostmask(obj,p[0],p[1])
			if self.is_ignored(obj,p[1]): return

		if self.is_ignored(obj,user): return

		# Catch ctcp-action message
		if target==obj.nickname:
			if self.open_private_chat_windows:
				# Check to see if user window exists
				if not self.userWindowExists(obj,user):
					c = self.fetchConnection(obj)
					win = UserWindow(user,self.MDI,obj,self)
					c.windows[user] = win
					self.buildWindowMenu()
				msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[ACTION_STYLE_NAME],user+" "+text )
				self.writeToChannel(obj,user,msg)
				self.writeToChannelLog(obj,user,'+'+user,text)
				return
			else:
				msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[ACTION_STYLE_NAME],user+" "+text )
				self.writeToConsole(obj,msg)
				self.writeToConsoleLog(obj,'+'+user,text)
				return

		msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[ACTION_STYLE_NAME],user+" "+text )
		self.writeToChannel(obj,target,msg)
		self.writeToChannelLog(obj,target,'+'+user,text)

	def irc_privmsg(self,obj,user,target,text):
		if not self.window_is_active: self.IS_FLASHING = True
		p = user.split('!')
		if len(p)==2:
			user = p[0]
			self.update_user_hostmask(obj,p[0],p[1])
			if self.is_ignored(obj,p[1]): return

		if self.is_ignored(obj,user): return

		# Catch private message
		if target==obj.nickname:
			if self.open_private_chat_windows:
				# Check to see if user window exists
				if not self.userWindowExists(obj,user):
					c = self.fetchConnection(obj)
					win = UserWindow(user,self.MDI,obj,self)
					c.windows[user] = win
					self.buildWindowMenu()
				# Display the message and return
				msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[USERNAME_STYLE_NAME],user,self.styles[MESSAGE_STYLE_NAME],text )
				self.writeToChannel(obj,user,msg)
				self.writeToChannelLog(obj,user,user,text)
				# self.writeToChannel(obj,user,user+": "+text)
				return
			else:
				msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[USERNAME_STYLE_NAME],user,self.styles[MESSAGE_STYLE_NAME],text )
				self.writeToConsole(obj,msg)
				self.writeToConsoleLog(obj,user,text)
				#self.writeToConsole(obj,user+": "+text)
				return

		msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[USERNAME_STYLE_NAME],user,self.styles[MESSAGE_STYLE_NAME],text )
		self.writeToChannel(obj,target,msg)
		self.writeToChannelLog(obj,target,user,text)
		#self.writeToChannel(obj,target,user+": "+text)

	def irc_disconnect(self,obj,reason):
		if not self.disconnecting:
			if not self.quitting:
				try:
					self.lostIRCConnection(obj)
				except:
					pass	

	def irc_connect(self,obj):
		
		# Create console window for connection, and store it and the connection
		c = Connection(obj,obj.id)
		ccon = ConsoleWindow(obj.server+":"+str(obj.port),self.MDI,obj,self)
		c.console = ccon
		self.connections.append(c)

		msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],"Connected to "+obj.server+":"+str(obj.port) )
		ccon.writeText(msg)
		ccon.add_to_log('',"Connected to "+obj.server+":"+str(obj.port))
		# ccon.writeText("Connected!")

		self.buildWindowMenu()

		self.buildConnectionsMenu()

		if self.keep_alive:
			obj.heartbeatInterval = self.keep_alive_interval
			obj.startHeartbeat()

	def irc_client_joined(self,obj,channel):

		self.serverLog(obj,"Joined "+channel)

		c = self.fetchConnection(obj)
		if c:
			chan = ChannelWindow(channel,self.MDI,obj,self)
			c.windows[channel] = chan
			# chan.writeText("Joined "+channel)
			msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],"Joined "+channel )
			chan.writeText(msg)
			chan.add_to_log('',"Joined "+channel)
			self.buildWindowMenu()
	
	def irc_userlist(self,obj,channel,users):
		self.writeChannelUserlist(obj,channel,users)

	def irc_join(self,obj,user,channel):
		p = user.split('!')
		if len(p)==2:
			nick = p[0]
			self.update_user_hostmask(obj,p[0],p[1])
		else:
			nick = user

		self.serverLog(obj,nick+" has joined "+channel)

		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					c.windows[channel].users.append(user)
					c.windows[channel].refreshUserlist()
					# self.writeToChannel(obj,channel, nick+" has joined "+channel )

					if not c.windows[channel].ignore_join_messages:
						msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],nick+" has joined "+channel )
						self.writeToChannel(obj,channel, msg )
						self.writeToChannelLog(obj,channel,'',nick+" has joined "+channel)

	def irc_part(self,obj,user,channel):
		p = user.split('!')
		if len(p)==2:
			nick = p[0]
			self.update_user_hostmask(obj,p[0],'')
		else:
			nick = user

		self.serverLog(obj,nick+" has left "+channel)

		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					clean = []
					for u in c.windows[channel].users:
						p = u.split('!')
						if len(p)==2:
							tnick = p[0]
						else:
							tnick = u
						tnick = tnick.replace('@','')
						tnick = tnick.replace('!','')
						if tnick==user: continue
						clean.append(u)
					c.windows[channel].users = clean
					c.windows[channel].refreshUserlist()
					#self.writeToChannel(obj,channel, nick+" has left "+channel )

					if not c.windows[channel].ignore_part_messages:
						msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],nick+" has left "+channel )
						self.writeToChannel(obj,channel, msg )
						self.writeToChannelLog(obj,channel,'',nick+" has left "+channel)


	def irc_nick_changed(self,obj,oldnick,newnick):
		if obj.nickname==oldnick:
			self.serverLog(obj,"You are now known as "+newnick)
		else:
			self.serverLog(obj,oldnick+" is now known as "+newnick)
		renamed_user_window = False
		newwin = None
		for c in self.connections:
			if c.id==obj.id:
				for channel in c.windows:
					if obj.nickname==oldnick:
						c.windows[channel].update_nick(newnick)
					if not c.windows[channel].is_channel:
						if channel==oldnick:
							newwin = c.windows[channel]
							# newwin.name = newnick
							# newwin.setWindowTitle(" "+newnick)
							newwin.rename(newnick)
							renamed_user_window = True
							continue
						continue
					clean = []
					found = False
					for u in c.windows[channel].users:
						p = u.split('!')
						if len(p)==2:
							nick = p[0]
						else:
							nick = u

						if '@' in nick:
							nick = nick.replace('@','')
						if '+' in nick:
							nick = nick.replace('+','')

						if nick==oldnick:
							found = True
							u = u.replace(oldnick,newnick)

						clean.append(u)

					if found:
						c.windows[channel].users = clean
						c.windows[channel].refreshUserlist()

						if not c.windows[channel].ignore_nick_messages:
							if obj.nickname==oldnick:
								msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME], "You are now known as "+newnick )
								self.writeToChannel(obj,channel, msg )
								self.writeToChannelLog(obj,channel,'',"You are now known as "+newnick)
							else:
								msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME], oldnick+" is now known as "+newnick )
								self.writeToChannel(obj,channel, msg )
								self.writeToChannelLog(obj,channel,'',oldnick+" is now known as "+newnick)

		if renamed_user_window:
			if newwin:
				for c in self.connections:
					if c.id==obj.id:
						c.windows[newnick] = newwin
						del c.windows[oldnick]
				self.buildWindowMenu()

				msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME], oldnick+" is now known as "+newnick )
				self.writeToChannel(obj,newnick, msg )
				self.writeToChannelLog(obj,newnick,'',oldnick+" is now known as "+newnick)

	# |================|
	# | IRC EVENTS END |
	# |================|

	# |============================|
	# | GUI HELPER FUNCTIONS BEGIN |
	# |============================|

	def get_user_hostmask(self,obj,tnick):
		for c in self.connections:
			if c.id==obj.id:
				for channel in c.windows:
					if c.windows[channel].is_channel:
						for u in c.windows[channel].users:
							p = u.split('!')
							if len(p)==2:
								nick = p[0]
								hostmask = p[1]
							else:
								nick = u
								hostmask = None

							nick = nick.replace('@','')
							nick = nick.replace('+','')

							if nick==tnick:
								return hostmask
		return None

	def update_user_hostmask(self,obj,tnick,hostmask):
		for c in self.connections:
			if c.id==obj.id:
				for channel in c.windows:
					if c.windows[channel].is_channel:
						for u in c.windows[channel].users:
							p = u.split('!')
							if len(p)==2:
								nick = p[0]
							else:
								nick = u

							nick = nick.replace('@','')
							nick = nick.replace('+','')

							if nick==tnick:
								c.windows[channel].update_hostmask(tnick,hostmask)
								break

	def serverLog(self,obj,text):
		msg = render_system(self, self.styles[TIMESTAMP_STYLE_NAME],self.styles[SYSTEM_STYLE_NAME],text )
		self.writeToConsole(obj,msg)
		self.writeToConsoleLog(obj,'',msg)

	def getChannelList(self,obj):
		channels = []
		c = self.fetchConnection(obj)
		for w in c.windows:
			if c.windows[w].is_channel:
				channels.append(c.windows[w].name)
		return channels

	def getChannelListExcept(self,obj,name):
		channels = []
		c = self.fetchConnection(obj)
		for w in c.windows:
			if c.windows[w].is_channel:
				if c.windows[w].name==name: continue
				channels.append(c.windows[w].name)
		return channels

	def writePrivateMessage(self,obj,target,text,notice=False):
		if self.open_private_chat_windows:
			# Check to see if user window exists
			if not self.userWindowExists(obj,target):
				c = self.fetchConnection(obj)
				win = UserWindow(target,self.MDI,obj,self)
				c.windows[target] = win
			# Display the message and return
			if notice:
				ustyle = self.styles[NOTICE_STYLE_NAME]
				mstyle = self.styles[SYSTEM_STYLE_NAME]
				glyph = GLYPH_NOTICE
			else:
				ustyle = self.styles[SELF_STYLE_NAME]
				mstyle = self.styles[MESSAGE_STYLE_NAME]
				glyph = GLYPH_SELF
			msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],ustyle,obj.nickname,mstyle,text )
			self.writeToChannel(obj,target,msg)
			self.writeToChannelLog(obj,target,glyph+obj.nickname,text)
			return
		self.writeChannelMessage(obj,target,text)

	def writeChannelMessage(self,obj,target,text,notice=False):
		if self.userWindowExists(obj,target):
			if notice:
				ustyle = self.styles[NOTICE_STYLE_NAME]
				mstyle = self.styles[SYSTEM_STYLE_NAME]
				glyph = GLYPH_NOTICE
			else:
				ustyle = self.styles[SELF_STYLE_NAME]
				mstyle = self.styles[MESSAGE_STYLE_NAME]
				glyph = GLYPH_SELF
			msg = render_message(self, self.styles[TIMESTAMP_STYLE_NAME],ustyle,obj.nickname,mstyle,text )
			self.writeToChannel(obj,target,msg)
			self.writeToChannelLog(obj,target,glyph+obj.nickname,text)

	def double_click_user(self,obj,nick):
		if nick==obj.nickname: return
		if not self.userWindowExists(obj,nick):
			c = self.fetchConnection(obj)
			win = UserWindow(nick,self.MDI,obj,self)
			c.windows[nick] = win
			self.buildWindowMenu()
		else:
			for c in self.connections:
				for win in c.windows:
					if win==nick:
						self.restoreWindow(c.windows[win],c.windows[win].subwindow)
						return

	def userWindowExists(self,obj,user):
		for c in self.connections:
			if c.id==obj.id:
				if user in c.windows: return True
		return False

	def writeToConsole(self,obj,text):
		for c in self.connections:
			if c.id==obj.id:
				c.console.writeText(text)
				return

	def writeToConsoleLog(self,obj,user,text):
		for c in self.connections:
			if c.id==obj.id:
				c.console.add_to_log(user,text)
				return

	def writeToChannel(self,obj,channel,text):
		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					c.windows[channel].writeText(text)

	def writeToChannelLog(self,obj,channel,user,text):
		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					c.windows[channel].add_to_log(user,text)

	def fetchConnection(self,obj):
		for c in self.connections:
			if c.id==obj.id: return c
		return None

	def writeChannelUserlist(self,obj,channel,users):
		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					c.windows[channel].writeUserlist(users)

	def setChannelMode(self,obj,channel,text):
		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					c.windows[channel].addModes(text)

	def unsetChannelMode(self,obj,channel,text):
		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					c.windows[channel].removeModes(text)

	def setChannelKey(self,obj,channel,text):
		for c in self.connections:
			if c.id==obj.id:
				if channel in c.windows:
					c.windows[channel].setKey(text)

	def restoreConsole(self,obj):
		# win.triggered.connect(lambda state,f=c.console,y=c.console.subwindow: self.restoreWindow(f,y))
		for c in self.connections:
			if c.id==obj.id:
				self.restoreWindow(c.console,c.console.subwindow)

	def closeConsole(self,obj):
		for c in self.connections:
			if c.id==obj.id:
				c.console.close()

	def remove_connection(self,cid):
		clean = []
		for c in self.connections:
			ccid = c.connection.server + ":" + str(c.connection.port)
			if ccid == cid: continue
			clean.append(c)
		self.connections = clean

	def restoreWindow(self,win,subwin):
		# Unminimize window if the window is minimized
		win.setWindowState(win.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
		win.activateWindow()
		win.showNormal()

		subwin.show()

		# Bring the window to the front
		self.MDI.setActiveSubWindow(subwin)

	def connectToIRCServer(self,info):
		if info.ssl:
			if info.reconnect:
				reconnectSSL(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=True
				)
			else:
				connectSSL(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=False
				)
		else:
			if info.reconnect:
				reconnect(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=True
				)
			else:
				connect(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=False
				)

	# |==========================|
	# | GUI HELPER FUNCTIONS END |
	# |==========================|

	# |===============|
	# | QT CODE BEGIN |
	# |===============|

	def closeEvent(self, event):

		self.clock.stop()
		self.tray.hide()

		self.quitting = True

		# Close all windows (so that logs are saved)
		for c in self.connections:

			# Save log
			if self.save_logs_on_quit:
				if len(c.console.newlog)>0:
					cid = c.console.client.server+":"+str(c.console.client.port)
					saveLog(cid,None,c.console.newlog)

			c.connection.quit()
			c.console.close()
			try:
				c.channel_list.close()
				del c.channel_list
			except:
				pass
			del c.console
			for w in c.windows:
				c.windows[w].close()

		self.app.quit()

	def updateActiveChild(self,subWindow):
		if not self.set_window_title_to_active: return
		try:
			w = subWindow.windowTitle()
			self.setWindowTitle(w)
		except:
			self.setWindowTitle(DEFAULT_WINDOW_TITLE)

	def lostIRCConnection(self,obj):

		c = self.fetchConnection(obj)
		# Save log
		if self.save_logs_on_quit:
			if len(c.console.newlog)>0:
				cid = c.console.client.server+":"+str(c.console.client.port)
				saveLog(cid,None,c.console.newlog)
		c.console.close()
		try:
			c.channel_list.close()
		except:
			pass

		# Autojoins
		aj = []
		for c in self.connections:
			if c.id==obj.id:
				for w in c.windows:
					if c.windows[w].is_channel:
						if c.windows[w].key!='':
							e = [c.windows[w].name,c.windows[w].key]
						else:
							e = [c.windows[w].name,'']
						aj.append(e)
		if self.rejoin_channels: self.autojoins[obj.server] = aj
		
		clean = []
		wins = []
		for c in self.connections:
			if c.id==obj.id:
				try:
					c.motd_window.close()
				except:
					pass
				for w in c.windows:
					wins.append(c.windows[w])
				continue
			clean.append(c)

		for w in wins:
			w.close()

		del wins

		self.connections = clean

		self.setWindowTitle(DEFAULT_WINDOW_TITLE)
		self.buildWindowMenu()
		self.buildConnectionsMenu()

	def disconnectFromIRC(self,obj,msg=None):
		self.disconnecting = True
		if obj.reconnect:
			cid = obj.server+":"+str(obj.port)
			self.disconnected.append(cid)
		if msg:
			obj.qui(msg)
		else:
			obj.quit()

		c = self.fetchConnection(obj)
		# Save log
		if self.save_logs_on_quit:
			if len(c.console.newlog)>0:
				cid = c.console.client.server+":"+str(c.console.client.port)
				saveLog(cid,None,c.console.newlog)
		c.console.close()
		try:
			c.channel_list.close()
		except:
			pass
		
		clean = []
		wins = []
		for c in self.connections:
			if c.id==obj.id:
				try:
					c.motd_window.close()
				except:
					pass
				for w in c.windows:
					wins.append(c.windows[w])
				continue
			clean.append(c)
		self.connections = clean

		for w in wins:
			w.close()

		self.setWindowTitle(DEFAULT_WINDOW_TITLE)
		self.buildWindowMenu()
		self.buildConnectionsMenu()

	def ignore_user(self,obj,user):
		if not self.allow_ignore: return
		self.ignore.append(user)
		save_ignore(self.ignore)

	def unignore_user(self,obj,user):
		if not self.allow_ignore: return
		clean = []
		for e in self.ignore:
			if fnmatch.fnmatch(user,e): continue
			if e.lower()==user.lower(): continue
			clean.append(e)
		self.ignore = clean
		save_ignore(self.ignore)

	def is_ignored(self,obj,user):
		if not self.allow_ignore: return False
		for e in self.ignore:
			if fnmatch.fnmatch(user,e): return True
			if e.lower()==user.lower(): return True
		return False

	def eventFilter(self, obj, event):
		if event.type() == QEvent.WindowActivate:
			self.window_is_active = True
			self.IS_FLASHING = False
		elif event.type()== QEvent.WindowDeactivate:
			self.window_is_active = False
		elif event.type()== QEvent.FocusIn:
			self.window_is_active = True
			self.IS_FLASHING = False
		elif event.type()== QEvent.FocusOut:
			self.window_is_active = False

		return QMainWindow.eventFilter(self,obj,event)

	def clock_tick(self):
		if self.systray_notification:
			if self.IS_FLASHING:
				if self.FLASH_STATE==0:
					self.FLASH_STATE = 1
					self.tray.setIcon(self.flash_icon)
				else:
					self.FLASH_STATE = 0
					self.tray.setIcon(self.tray_icon)
			else:
				self.FLASH_STATE = 0
				self.tray.setIcon(self.tray_icon)

	def __init__(self,app,settings_file=SETTINGS_FILE,text_settings_file=TEXT_SETTINGS_FILE,parent=None):
		super(Erk, self).__init__(parent)

		self.app = app
		self.parent = parent
		self.settings_file = settings_file
		self.text_settings_file = text_settings_file

		self.installEventFilter(self)

		self.window_is_active = True

		self.quitting = False
		self.disconnecting = False

		self.is_parting = []

		self.connections = []

		self.disconnected = []

		self.keep_alive_interval = DEFAULT_KEEPALIVE_INTERVAL

		self.view_all_traffic = False

		self.ignore = get_ignore()

		self.autojoins = defaultdict(list)

		self.styles = get_text_settings(self.text_settings_file)

		self.settings = get_settings(self.settings_file)

		self.tray_icon = QIcon(ERK_ICON)
		self.flash_icon = QIcon(FLASH_ICON)

		self.clock = Clock()
		self.clock.beat.connect(self.clock_tick)
		self.clock.start()

		# Settings changable via the gui
		self.open_private_chat_windows				= self.settings[SETTING_OPEN_PRIVATE_WINDOWS]
		self.display_status_bar_on_chat_windows		= self.settings[SETTING_CHAT_STATUS_BARS]
		self.plain_user_lists						= self.settings[SETTING_PLAIN_USER_LISTS]
		self.font_string							= self.settings[SETTING_APPLICATION_FONT]
		self.display_timestamp						= self.settings[SETTING_DISPLAY_TIMESTAMPS]
		self.use_24_hour_timestamp					= self.settings[SETTING_24HOUR_TIMESTAMPS]
		self.use_seconds_in_timestamp				= self.settings[SETTING_DISPLAY_TIMESTAMP_SECONDS]
		self.load_logs_on_start						= self.settings[SETTING_LOAD_LOGS_ON_START]
		self.save_logs_on_quit						= self.settings[SETTING_SAVE_LOGS_ON_EXIT]
		self.spellCheck								= self.settings[SETTING_SPELL_CHECK]
		self.spellCheckLanguage						= self.settings[SETTING_SPELL_CHECK_LANGUAGE]
		self.use_asciimojis							= self.settings[SETTING_ASCIIMOJI]
		self.use_emojis								= self.settings[SETTING_EMOJI]
		self.set_window_title_to_active				= self.settings[SETTING_SET_WINDOW_TITLE_TO_ACTIVE]
		self.autocomplete_commands					= self.settings[SETTING_AUTOCOMPLETE_CMDS]
		self.autocomplete_nicks						= self.settings[SETTING_AUTOCOMPLETE_NICKS]
		self.convert_links_in_chat					= self.settings[SETTING_HYPERLINKS]
		self.strip_html_from_chat					= self.settings[SETTING_STRIP_HTML]
		self.window_on_top							= False
		self.window_fullscreen						= False
		self.log_private_chat						= self.settings[SETTING_LOG_PRIVATE_CHAT]
		self.hide_private_chat						= self.settings[SETTING_HIDE_PRIVATE_CHAT]
		self.save_server_history					= self.settings[SETTING_SAVE_HISTORY]
		self.filter_profanity						= self.settings[SETTING_PROFANITY_FILTER]
		self.display_uptime_console					= self.settings[SETTING_DISPLAY_UPTIME_CONSOLE]
		self.display_uptime_chat					= self.settings[SETTING_DISPLAY_UPTIME_CHAT]
		self.display_uptime_seconds					= self.settings[SETTING_UPTIME_SECONDS]
		self.keep_alive								= self.settings[SETTING_KEEP_ALIVE]
		self.default_window_width					= self.settings[SETTING_WINDOW_WIDTH]
		self.default_window_height					= self.settings[SETTING_WINDOW_HEIGHT]
		self.display_irc_colors						= self.settings[SETTING_DISPLAY_IRC_COLOR]
		self.rejoin_channels						= self.settings[SETTING_REJOIN_CHANNELS]
		self.systray_notification					= self.settings[SETTING_SYSTRAY_NOTIFICATION]

		self.allow_ignore							= self.settings[SETTING_ENABLE_IGNORE]
		if not self.allow_ignore: self.actIgnore.setVisible(False)

		self.autocomplete_asciimoji = self.settings[SETTING_ASCIIMOJI_AUTOCOMPLETE]
		self.ASCIIMOJI_AUTOCOMPLETE = []

		if self.autocomplete_asciimoji:
			self.ASCIIMOJI_AUTOCOMPLETE = load_asciimoji_autocomplete()

		self.autocomplete_emoji = self.settings[SETTING_EMOJI_AUTOCOMPLETE]
		self.EMOJI_AUTOCOMPLETE = []

		if self.autocomplete_emoji:
			self.EMOJI_AUTOCOMPLETE = load_emoji_autocomplete()

		# Settings not changeable via gui
		self.max_username_length					= self.settings[SETTING_MAX_NICK_LENGTH]
		self.max_displayed_log						= self.settings[SETTING_LOADED_LOG_LENGTH]

		self.tray = QSystemTrayIcon(self)
		self.tray.setIcon(self.tray_icon)

		if self.systray_notification:
			self.tray.show()

		self.IS_FLASHING = False
		self.FLASH_STATE = 0

		# Custom style for various menus
		self.menu_style = ErkSmallStyle('Windows')

		f = QFont()
		f.fromString(self.font_string)
		self.font = f

		app.setFont(self.font)

		self.setWindowTitle(DEFAULT_WINDOW_TITLE)

		self.setWindowIcon(QIcon(ERK_ICON))

		self.MDI = QMdiArea()
		self.setCentralWidget(self.MDI)

		self.MDI.subWindowActivated.connect(self.updateActiveChild)

		pix = QPixmap(MDI_BACKGROUND)
		backgroundBrush = QBrush(pix)
		self.MDI.setBackground(backgroundBrush)

		self.menubar = self.menuBar()
		menuBoldText = self.menubar.font()
		menuBoldText.setBold(True)

		# IRC Menu

		self.ircMenu = self.menubar.addMenu(APPLICATION_NAME)

		self.ircMenu.setFont(menuBoldText)

		self.actConnect = fancyMenuAction(self,FANCY_CONNECT_ICON,"Connect","Connect to an IRC server",self.menuConnect)
		self.ircMenu.addAction(self.actConnect)

		self.actNetwork = fancyMenuAction(self,FANCY_NETWORK_ICON,"Servers","Select server from a list",self.menuNetwork)
		self.ircMenu.addAction(self.actNetwork)

		self.actEditUserInfo = fancyMenuAction(self,FANCY_USER_ICON,"User","Edit default user information",self.menuEditUser)
		self.ircMenu.addAction(self.actEditUserInfo)

		self.ircMenu.addSeparator()

		self.actRestart = QAction(QIcon(RESTART_ICON),"Restart",self)
		self.actRestart.triggered.connect(self.menuRestart)
		self.ircMenu.addAction(self.actRestart)

		self.actExit = QAction(QIcon(EXIT_ICON),"Exit",self)
		self.actExit.triggered.connect(self.close)
		if EXIT_SHORTCUT!=None:
			self.actExit.setShortcut(EXIT_SHORTCUT)
		self.ircMenu.addAction(self.actExit)

		# CONNECTIONS MENU

		self.connectionsMenu = self.menubar.addMenu("Connections")

		self.buildConnectionsMenu()

		# Settings Menu

		settingsMenu = self.menubar.addMenu("Settings")

		settingsMenu.setFont(menuBoldText)

		sep = textSeparator(self,"<i>Configuration</i>")
		settingsMenu.addAction(sep)

		self.actIgnore = QAction(QIcon(IGNORE_ICON),"Ignored Users",self)
		self.actIgnore.triggered.connect(self.menuIgnore)
		settingsMenu.addAction(self.actIgnore)

		#settingsMenu.addSeparator()

		displaySubMenu = settingsMenu.addMenu(QIcon(DISPLAY_ICON),"Display")

		self.actFont = QAction(QIcon(FONT_ICON),"Font",self)
		self.actFont.triggered.connect(self.menuFont)
		displaySubMenu.addAction(self.actFont)

		pf = self.font_string.split(',')
		mf = pf[0]
		ms = pf[1]
		self.actFont.setText(f"Font ({mf}, {ms}pt)")

		self.actSetSize = QAction(QIcon(RESIZE_ICON),"Set initial window size",self)
		self.actSetSize.triggered.connect(self.menuWindowSize)
		displaySubMenu.addAction(self.actSetSize)

		displaySubMenu.addSeparator()

		self.actTray = QAction("System tray message notification",self,checkable=True)
		self.actTray.setChecked(self.systray_notification)
		self.actTray.triggered.connect(self.menuTray)
		displaySubMenu.addAction(self.actTray)

		self.actStatusBars = QAction("Status bars on chat windows",self,checkable=True)
		self.actStatusBars.setChecked(self.display_status_bar_on_chat_windows)
		self.actStatusBars.triggered.connect(self.menuChatStatusBars)
		displaySubMenu.addAction(self.actStatusBars)

		self.actPlainUserLists = QAction("Plain user lists",self,checkable=True)
		self.actPlainUserLists.setChecked(self.plain_user_lists)
		self.actPlainUserLists.triggered.connect(self.menuPlainUserLists)
		displaySubMenu.addAction(self.actPlainUserLists)

		self.actHidePrivate = QAction("Hide user chat windows on close",self,checkable=True)
		self.actHidePrivate.setChecked(self.hide_private_chat)
		self.actHidePrivate.triggered.connect(self.menuToggleHideChat)
		displaySubMenu.addAction(self.actHidePrivate)

		self.actWindowTitle = QAction("Use application title of the active window",self,checkable=True)
		self.actWindowTitle.setChecked(self.set_window_title_to_active)
		self.actWindowTitle.triggered.connect(self.menuWindowTitle)
		displaySubMenu.addAction(self.actWindowTitle)

		displaySubMenu.addSeparator()

		self.actOnTop = QAction("Always on top",self,checkable=True)
		self.actOnTop.setChecked(self.window_on_top)
		self.actOnTop.triggered.connect(self.menuToggleWindowOnTop)
		displaySubMenu.addAction(self.actOnTop)

		self.actFullscreen = QAction("Full screen",self,checkable=True)
		self.actFullscreen.setChecked(self.window_fullscreen)
		self.actFullscreen.triggered.connect(self.menuToggleFullscreen)
		displaySubMenu.addAction(self.actFullscreen)

		sep = textSeparator(self,"<i>Preferences</i>")
		settingsMenu.addAction(sep)

		uptimeSubMenu = settingsMenu.addMenu(QIcon(UPTIME_ICON),"Uptime")

		self.actConsoleUptime = QAction("Display uptime on console windows",self,checkable=True)
		self.actConsoleUptime.setChecked(self.display_uptime_console)
		self.actConsoleUptime.triggered.connect(self.menuConsoleUptime)
		uptimeSubMenu.addAction(self.actConsoleUptime)

		self.actChatUptime = QAction("Display uptime on chat windows",self,checkable=True)
		self.actChatUptime.setChecked(self.display_uptime_chat)
		self.actChatUptime.triggered.connect(self.menuChatUptime)
		uptimeSubMenu.addAction(self.actChatUptime)

		self.actSecondsUptime = QAction("Display seconds in uptime",self,checkable=True)
		self.actSecondsUptime.setChecked(self.display_uptime_seconds)
		self.actSecondsUptime.triggered.connect(self.menuSecondsUptime)
		uptimeSubMenu.addAction(self.actSecondsUptime)

		timestampSubMenu = settingsMenu.addMenu(QIcon(TIMESTAMP_ICON),"Timestamps")

		self.actToggleTimestamp = QAction("Display timestamps",self,checkable=True)
		self.actToggleTimestamp.setChecked(self.display_timestamp)
		self.actToggleTimestamp.triggered.connect(self.menuToggleTimestamp)
		timestampSubMenu.addAction(self.actToggleTimestamp)

		self.actToggle24Clock = QAction("Use 24 hour clock for timestamps",self,checkable=True)
		self.actToggle24Clock.setChecked(self.use_24_hour_timestamp)
		self.actToggle24Clock.triggered.connect(self.menuToggle24HourClock)
		timestampSubMenu.addAction(self.actToggle24Clock)

		self.actToggleSecondsTimestamp = QAction("Display seconds in timestamps",self,checkable=True)
		self.actToggleSecondsTimestamp.setChecked(self.use_seconds_in_timestamp)
		self.actToggleSecondsTimestamp.triggered.connect(self.menuToggleSecondsTimestamp)
		timestampSubMenu.addAction(self.actToggleSecondsTimestamp)

		chatSubMenu = settingsMenu.addMenu(QIcon(CHAT_ICON),"Chat")

		self.actEmoji = QAction("Enable emoji shortcodes",self,checkable=True)
		self.actEmoji.setChecked(self.use_emojis)
		self.actEmoji.triggered.connect(self.menuEmoji)
		chatSubMenu.addAction(self.actEmoji)

		self.actAsciimoji = QAction("Enable ASCIImoji shortcodes",self,checkable=True)
		self.actAsciimoji.setChecked(self.use_asciimojis)
		self.actAsciimoji.triggered.connect(self.menuAsciimoji)
		chatSubMenu.addAction(self.actAsciimoji)

		self.actChatUrls = QAction("Link URLs in chat",self,checkable=True)
		self.actChatUrls.setChecked(self.convert_links_in_chat)
		self.actChatUrls.triggered.connect(self.menuConvertUrl)
		chatSubMenu.addAction(self.actChatUrls)

		self.actStripHtml = QAction("Strip HTML from messages",self,checkable=True)
		self.actStripHtml.setChecked(self.strip_html_from_chat)
		self.actStripHtml.triggered.connect(self.menuStripHtml)
		chatSubMenu.addAction(self.actStripHtml)

		self.actProfanity = QAction("Censor profanity",self,checkable=True)
		self.actProfanity.setChecked(self.filter_profanity)
		self.actProfanity.triggered.connect(self.menuProfanity)
		chatSubMenu.addAction(self.actProfanity)

		self.actColor = QAction("Display IRC colors",self,checkable=True)
		self.actColor.setChecked(self.display_irc_colors)
		self.actColor.triggered.connect(self.menuColor)
		chatSubMenu.addAction(self.actColor)

		self.actToggleIgnore = QAction("Ignore selected users",self,checkable=True)
		self.actToggleIgnore.setChecked(self.allow_ignore)
		self.actToggleIgnore.triggered.connect(self.menuToggleIgnore)
		chatSubMenu.addAction(self.actToggleIgnore)

		self.actOpenPrivateWindows = QAction("Open windows for private messages",self,checkable=True)
		self.actOpenPrivateWindows.setChecked(self.open_private_chat_windows)
		self.actOpenPrivateWindows.triggered.connect(self.menuPrivateWindows)
		chatSubMenu.addAction(self.actOpenPrivateWindows)

		autoSubMenu = settingsMenu.addMenu(QIcon(AUTOCOMPLETE_ICON),"Autocomplete")

		self.actAutoCmds = QAction("Autocomplete commands",self,checkable=True)
		self.actAutoCmds.setChecked(self.autocomplete_commands)
		self.actAutoCmds.triggered.connect(self.menuAutoCmds)
		autoSubMenu.addAction(self.actAutoCmds)

		self.actAutoNicks = QAction("Autocomplete nicks/channels",self,checkable=True)
		self.actAutoNicks.setChecked(self.autocomplete_nicks)
		self.actAutoNicks.triggered.connect(self.menuAutoNicks)
		autoSubMenu.addAction(self.actAutoNicks)

		self.actAutoAsciimoji = QAction("Autocomplete ASCIImojis",self,checkable=True)
		self.actAutoAsciimoji.setChecked(self.autocomplete_asciimoji)
		self.actAutoAsciimoji.triggered.connect(self.menuAutoAsciimoji)
		autoSubMenu.addAction(self.actAutoAsciimoji)

		self.actAutoEmoji = QAction("Autocomplete Emojis",self,checkable=True)
		self.actAutoEmoji.setChecked(self.autocomplete_emoji)
		self.actAutoEmoji.triggered.connect(self.menuAutoEmoji)
		autoSubMenu.addAction(self.actAutoEmoji)

		self.spellMenu = settingsMenu.addMenu(QIcon(SPELL_ICON),"Spell check")

		self.optSpellCheck = QAction("Enabled",self,checkable=True)
		self.optSpellCheck.setChecked(self.spellCheck)
		self.optSpellCheck.triggered.connect(self.menuToggleSpellCheck)
		self.spellMenu.addAction(self.optSpellCheck)

		self.spellMenu.addSeparator()

		self.scEnglish = QAction("English",self,checkable=True)
		self.scEnglish.setChecked(False)
		self.scEnglish.triggered.connect(lambda state,l="en": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scEnglish)

		self.scFrench = QAction("French",self,checkable=True)
		self.scFrench.setChecked(False)
		self.scFrench.triggered.connect(lambda state,l="fr": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scFrench)

		self.scSpanish = QAction("Spanish",self,checkable=True)
		self.scSpanish.setChecked(False)
		self.scSpanish.triggered.connect(lambda state,l="es": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scSpanish)

		self.scGerman = QAction("German",self,checkable=True)
		self.scGerman.setChecked(False)
		self.scGerman.triggered.connect(lambda state,l="de": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scGerman)

		if self.spellCheckLanguage=="en": self.scEnglish.setChecked(True)
		if self.spellCheckLanguage=="fr": self.scFrench.setChecked(True)
		if self.spellCheckLanguage=="es": self.scSpanish.setChecked(True)
		if self.spellCheckLanguage=="de": self.scGerman.setChecked(True)

		if not self.spellCheck:
			self.scEnglish.setEnabled(False)
			self.scFrench.setEnabled(False)
			self.scSpanish.setEnabled(False)
			self.scGerman.setEnabled(False)

		logSubMenu = settingsMenu.addMenu(QIcon(LOG_ICON),"Logs")

		self.actSaveLogs = QAction("Automatically save logs",self,checkable=True)
		self.actSaveLogs.setChecked(self.save_logs_on_quit)
		self.actSaveLogs.triggered.connect(self.menuToggleSaveLogs)
		logSubMenu.addAction(self.actSaveLogs)

		self.actLoadLogs = QAction("Automatically load logs",self,checkable=True)
		self.actLoadLogs.setChecked(self.load_logs_on_start)
		self.actLoadLogs.triggered.connect(self.menuToggleLoadLogs)
		logSubMenu.addAction(self.actLoadLogs)

		self.actPrivateLogs = QAction("Save private chat logs",self,checkable=True)
		self.actPrivateLogs.setChecked(self.log_private_chat)
		self.actPrivateLogs.triggered.connect(self.menuTogglePrivateLogs)
		logSubMenu.addAction(self.actPrivateLogs)

		if not self.save_logs_on_quit: self.actPrivateLogs.setEnabled(False)

		# Windows Menu

		self.windowMenu = self.menubar.addMenu("Windows")
		self.windowMenu.setFont(menuBoldText)

		self.buildWindowMenu()

		self.helpMenu = self.menubar.addMenu("Help")
		self.helpMenu.setFont(menuBoldText)

		self.actAbout = QAction(QIcon(ABOUT_ICON),"About "+APPLICATION_NAME,self)
		self.actAbout.triggered.connect(self.menuAbout)
		self.helpMenu.addAction(self.actAbout)

		helpLink = QAction(QIcon(ERK_ICON),"Source code repository",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/nutjob-laboratories/erk": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(OPEN_SOURCE_ICON),"GNU Public License 3",self)
		helpLink.triggered.connect(lambda state,u="https://www.gnu.org/licenses/gpl-3.0.en.html": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(LINK_ICON),"Emoji shortcode list",self)
		helpLink.triggered.connect(lambda state,u="https://www.webfx.com/tools/emoji-cheat-sheet/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"ASCIImoji shortcode list",self)
		helpLink.triggered.connect(lambda state,u="http://asciimoji.com/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(LINK_ICON),"RFC 1459",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc1459": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"RFC 2812",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc2812": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(PYTHON_SMALL_ICON),"Python",self)
		helpLink.triggered.connect(lambda state,u="https://www.python.org/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(QT_SMALL_ICON),"Qt",self)
		helpLink.triggered.connect(lambda state,u="https://www.qt.io/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(PYQT_ICON),"PyQt5",self)
		helpLink.triggered.connect(lambda state,u="https://www.riverbankcomputing.com/software/pyqt/intro": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(TWISTED_ICON),"Twisted",self)
		helpLink.triggered.connect(lambda state,u="https://twistedmatrix.com/trac/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(ICONS8_ICON),"Icons8",self)
		helpLink.triggered.connect(lambda state,u="https://icons8.com/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(PYTHON_SMALL_ICON),"pyspellchecker",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/barrust/pyspellchecker": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

	def menuIgnore(self):
		y = IgnoreDialog.Dialog(self)
		y.show()

	def open_link_in_browser(self,url):
		u = QUrl()
		u.setUrl(url)
		QDesktopServices.openUrl(u)

	def menuAbout(self):
		x = AboutDialog.Dialog(self)
		x.show()

	def menuTray(self):
		if self.systray_notification:
			self.systray_notification = False
			self.tray.hide()
		else:
			self.systray_notification = True
			self.tray.show()
		self.settings[SETTING_SYSTRAY_NOTIFICATION] = self.systray_notification
		save_settings(self.settings,self.settings_file)

	def menuRejoin(self):
		if self.rejoin_channels:
			self.rejoin_channels = False
		else:
			self.rejoin_channels = True
		self.settings[SETTING_REJOIN_CHANNELS] = self.rejoin_channels
		save_settings(self.settings,self.settings_file)

	def menuWindowSize(self):
		x = WindowSizeDialog.Dialog(self)
		e = x.get_window_information(self)

		if not e: return 

		self.default_window_width = e[0]
		self.default_window_height = e[1]

		self.settings[SETTING_WINDOW_WIDTH] = self.default_window_width
		save_settings(self.settings,self.settings_file)
		self.settings[SETTING_WINDOW_HEIGHT] = self.default_window_height
		save_settings(self.settings,self.settings_file)

	def menuEditUser(self):
		x = EditUserDialog.Dialog()
		e = x.get_user_information()
		del x

	def menuSecondsUptime(self):
		if self.display_uptime_seconds:			
			self.display_uptime_seconds = False
			for c in self.connections:
				t = convertSeconds(c.connection.uptime)
				hours = t[0]
				if len(str(hours))==1: hours = f"0{hours}"
				minutes = t[1]
				if len(str(minutes))==1: minutes = f"0{minutes}"
				seconds = t[2]
				if len(str(seconds))==1: seconds = f"0{seconds}"
				display = f"{hours}:{minutes}"

				try:
					if self.display_uptime_console:
						c.console.uptime_display(display)
						c.console.hide_uptime()
						c.console.show_uptime()
				except:
					pass
				for channel in c.windows:
					try:
						if self.display_uptime_chat:
							c.windows[channel].uptime_display(display)
							c.windows[channel].hide_uptime()
							c.windows[channel].show_uptime()
					except:
						pass
		else:
			self.display_uptime_seconds = True
			for c in self.connections:
				t = convertSeconds(c.connection.uptime)
				hours = t[0]
				if len(str(hours))==1: hours = f"0{hours}"
				minutes = t[1]
				if len(str(minutes))==1: minutes = f"0{minutes}"
				seconds = t[2]
				if len(str(seconds))==1: seconds = f"0{seconds}"
				display = f"{hours}:{minutes}:{seconds}"

				try:
					if self.display_uptime_console:
						c.console.uptime_display(display)
						c.console.hide_uptime()
						c.console.show_uptime()
				except:
					pass
				for channel in c.windows:
					try:
						if self.display_uptime_chat:
							c.windows[channel].uptime_display(display)
							c.windows[channel].hide_uptime()
							c.windows[channel].show_uptime()
					except:
						pass
		self.settings[SETTING_UPTIME_SECONDS] = self.display_uptime_seconds
		save_settings(self.settings,self.settings_file)

	def menuChatUptime(self):
		if self.display_uptime_chat:
			self.display_uptime_chat = False
			for c in self.connections:
				for channel in c.windows:
					try:
						c.windows[channel].hide_uptime()
					except:
						pass
		else:
			self.display_uptime_chat = True
			for c in self.connections:
				for channel in c.windows:
					try:
						c.windows[channel].show_uptime()
					except:
						pass
		self.settings[SETTING_DISPLAY_UPTIME_CHAT] = self.display_uptime_chat
		save_settings(self.settings,self.settings_file)

	def menuConsoleUptime(self):
		if self.display_uptime_console:
			self.display_uptime_console = False
			for c in self.connections:
				try:
					c.console.hide_uptime()
				except:
					pass
		else:
			self.display_uptime_console = True
			for c in self.connections:
				try:
					c.console.show_uptime()
				except:
					pass
		self.settings[SETTING_DISPLAY_UPTIME_CONSOLE] = self.display_uptime_console
		save_settings(self.settings,self.settings_file)

	def menuToggleIgnore(self):
		if self.allow_ignore:
			self.allow_ignore = False
			self.actIgnore.setVisible(False)
		else:
			self.allow_ignore = True
			self.actIgnore.setVisible(True)

		self.settings[SETTING_ENABLE_IGNORE] = self.allow_ignore
		save_settings(self.settings,self.settings_file)

	def menuAutoEmoji(self):
		if self.autocomplete_emoji:
			self.autocomplete_emoji = False
			self.EMOJI_AUTOCOMPLETE = []
		else:
			self.autocomplete_emoji = True
			if len(self.EMOJI_AUTOCOMPLETE)==0:
				self.EMOJI_AUTOCOMPLETE = load_emoji_autocomplete()
		self.settings[SETTING_EMOJI_AUTOCOMPLETE] = self.autocomplete_emoji
		save_settings(self.settings,self.settings_file)

	def menuAutoAsciimoji(self):
		if self.autocomplete_asciimoji:
			self.autocomplete_asciimoji = False
			self.ASCIIMOJI_AUTOCOMPLETE = []
		else:
			self.autocomplete_asciimoji = True
			if len(self.ASCIIMOJI_AUTOCOMPLETE)==0:
				self.ASCIIMOJI_AUTOCOMPLETE = load_asciimoji_autocomplete()
		self.settings[SETTING_ASCIIMOJI_AUTOCOMPLETE] = self.autocomplete_asciimoji
		save_settings(self.settings,self.settings_file)

	def menuStripHtml(self):
		if self.strip_html_from_chat:
			self.strip_html_from_chat = False
		else:
			self.strip_html_from_chat = True
		self.settings[SETTING_STRIP_HTML] = self.strip_html_from_chat
		save_settings(self.settings,self.settings_file)

	def menuColor(self):
		if self.display_irc_colors:
			self.display_irc_colors = False
		else:
			self.display_irc_colors = True

		for c in self.connections:
			c.console.rerenderText()
			for channel in c.windows:
				c.windows[channel].rerenderText()

		self.settings[SETTING_DISPLAY_IRC_COLOR] = self.display_irc_colors
		save_settings(self.settings,self.settings_file)

	def menuConvertUrl(self):
		if self.convert_links_in_chat:
			self.convert_links_in_chat = False
		else:
			self.convert_links_in_chat = True
		self.settings[SETTING_HYPERLINKS] = self.convert_links_in_chat
		save_settings(self.settings,self.settings_file)

	def menuToggleHistory(self):
		if self.save_server_history:
			self.save_server_history = False
		else:
			self.save_server_history = True
		self.settings[SETTING_SAVE_HISTORY] = self.save_server_history
		save_settings(self.settings,self.settings_file)

	def menuToggleHideChat(self):
		if self.hide_private_chat:
			self.hide_private_chat = False
		else:
			self.hide_private_chat = True
		self.settings[SETTING_HIDE_PRIVATE_CHAT] = self.hide_private_chat
		save_settings(self.settings,self.settings_file)

	def menuTogglePrivateLogs(self):
		if self.log_private_chat:
			self.log_private_chat = False
		else:
			self.log_private_chat = True
		self.settings[SETTING_LOG_PRIVATE_CHAT] = self.log_private_chat
		save_settings(self.settings,self.settings_file)

	def menuToggleFullscreen(self):
		if self.window_fullscreen:
			self.window_fullscreen = False
			self.showNormal()
			self.update()
		else:
			self.window_fullscreen = True
			self.showFullScreen()

	def menuToggleWindowOnTop(self):
		if self.window_on_top:
			self.window_on_top = False
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
			self.show()
		else:
			self.window_on_top = True
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
			self.show()
		
	def buildWindowMenu(self):

		self.windowMenu.clear()

		actCascade = QAction(QIcon(CASCADE_ICON),"Cascade Windows",self)
		actCascade.triggered.connect(lambda state: self.MDI.cascadeSubWindows())
		self.windowMenu.addAction(actCascade)

		actTile = QAction(QIcon(TILE_ICON),"Tile Windows",self)
		actTile.triggered.connect(lambda state: self.MDI.tileSubWindows())
		self.windowMenu.addAction(actTile)

		if len(self.connections)<1: return

		self.windowMenu.addSeparator()

		for c in self.connections:
			# c.console
			if c.connection.hostname:
				ctitle = c.connection.hostname
			else:
				ctitle = c.connection.server+":"+str(c.connection.port)

			sep = textSeparator(self,"<i>"+ctitle+"</i>")
			self.windowMenu.addAction(sep)

			for win in c.windows:
				if c.windows[win].is_channel:
					if c.windows[win].key=='':
						cwin = QAction(QIcon(CHANNEL_WINDOW),c.windows[win].name,self)
					else:
						cwin = QAction(QIcon(LOCKED_CHANNEL),c.windows[win].name,self)
				else:
					cwin = QAction(QIcon(USER_WINDOW),c.windows[win].name,self)
				cwin.triggered.connect(lambda state,f=c.windows[win],y=c.windows[win].subwindow: self.restoreWindow(f,y))
				self.windowMenu.addAction(cwin)

			#self.windowMenu.addSeparator()

	def menuAutoNicks(self):
		if self.autocomplete_nicks:
			self.autocomplete_nicks = False
		else:
			self.autocomplete_nicks = True
		self.settings[SETTING_AUTOCOMPLETE_NICKS] = self.autocomplete_commands
		save_settings(self.settings,self.settings_file)

	def menuAutoCmds(self):
		if self.autocomplete_commands:
			self.autocomplete_commands = False
		else:
			self.autocomplete_commands = True
		self.settings[SETTING_AUTOCOMPLETE_CMDS] = self.autocomplete_commands
		save_settings(self.settings,self.settings_file)

	def menuWindowTitle(self):
		if self.set_window_title_to_active:
			self.set_window_title_to_active = False
			self.setWindowTitle(DEFAULT_WINDOW_TITLE)
		else:
			self.set_window_title_to_active = True
			self.updateActiveChild(self.MDI.activeSubWindow())
		self.settings[SETTING_SET_WINDOW_TITLE_TO_ACTIVE] = self.set_window_title_to_active
		save_settings(self.settings,self.settings_file)

	def menuEmoji(self):
		if self.use_emojis:
			self.use_emojis = False
			self.actAutoEmoji.setEnabled(False)
		else:
			self.use_emojis = True
			self.actAutoEmoji.setEnabled(True)
		self.settings[SETTING_EMOJI] = self.use_emojis
		save_settings(self.settings,self.settings_file)

	def menuAsciimoji(self):
		if self.use_asciimojis:
			self.use_asciimojis = False
			self.actAutoAsciimoji.setEnabled(False)
		else:
			self.use_asciimojis = True
			self.actAutoAsciimoji.setEnabled(True)
		self.settings[SETTING_ASCIIMOJI] = self.use_asciimojis
		save_settings(self.settings,self.settings_file)

	def menuToggleSpellCheck(self):
		if self.spellCheck:
			self.spellCheck = False
			self.scEnglish.setEnabled(False)
			self.scFrench.setEnabled(False)
			self.scSpanish.setEnabled(False)
			self.scGerman.setEnabled(False)
		else:
			self.spellCheck = True
			self.scEnglish.setEnabled(True)
			self.scFrench.setEnabled(True)
			self.scSpanish.setEnabled(True)
			self.scGerman.setEnabled(True)

		self.settings[SETTING_SPELL_CHECK] = self.spellCheck
		save_settings(self.settings,self.settings_file)

		for c in self.connections:
			t = c.console.userTextInput.toPlainText()
			c.console.userTextInput.setPlainText(t)
			c.console.userTextInput.moveCursor(QTextCursor.End)
			for channel in c.windows:
				t = c.windows[channel].userTextInput.toPlainText()
				c.windows[channel].userTextInput.setPlainText(t)
				c.windows[channel].userTextInput.moveCursor(QTextCursor.End)

	def setSpellCheckLanguage(self,lang):
		self.spellCheckLanguage = lang

		for c in self.connections:
			c.console.userTextInput.changeLanguage(lang)
			for channel in c.windows:
				c.windows[channel].userTextInput.changeLanguage(lang)

		self.settings[SETTING_SPELL_CHECK_LANGUAGE] = self.spellCheckLanguage
		save_settings(self.settings,self.settings_file)

		if lang=="en":
			self.scEnglish.setChecked(True)
			self.scFrench.setChecked(False)
			self.scSpanish.setChecked(False)
			self.scGerman.setChecked(False)
			return

		if lang=="fr":
			self.scEnglish.setChecked(False)
			self.scFrench.setChecked(True)
			self.scSpanish.setChecked(False)
			self.scGerman.setChecked(False)
			return

		if lang=="es":
			self.scEnglish.setChecked(False)
			self.scFrench.setChecked(False)
			self.scSpanish.setChecked(True)
			self.scGerman.setChecked(False)
			return

		if lang=="de":
			self.scEnglish.setChecked(False)
			self.scFrench.setChecked(False)
			self.scSpanish.setChecked(False)
			self.scGerman.setChecked(True)
			return

	def menuToggleLoadLogs(self):
		if self.load_logs_on_start:
			self.load_logs_on_start = False
		else:
			self.load_logs_on_start = True

		self.settings[SETTING_LOAD_LOGS_ON_START] = self.load_logs_on_start
		save_settings(self.settings,self.settings_file)

	def menuToggleSaveLogs(self):
		if self.save_logs_on_quit:
			self.save_logs_on_quit = False
			self.actPrivateLogs.setEnabled(False)
		else:
			self.save_logs_on_quit = True
			self.actPrivateLogs.setEnabled(True)

		self.settings[SETTING_SAVE_LOGS_ON_EXIT] = self.save_logs_on_quit
		save_settings(self.settings,self.settings_file)

	def menuProfanity(self):
		if self.filter_profanity:
			self.filter_profanity = False
		else:
			self.filter_profanity = True

		for c in self.connections:
			c.console.rerenderText()
			for channel in c.windows:
				c.windows[channel].rerenderText()

		self.settings[SETTING_PROFANITY_FILTER] = self.filter_profanity
		save_settings(self.settings,self.settings_file)

	def menuToggleSecondsTimestamp(self):
		if self.use_seconds_in_timestamp:
			self.use_seconds_in_timestamp = False
		else:
			self.use_seconds_in_timestamp = True

		for c in self.connections:
			c.console.rerenderText()
			for channel in c.windows:
				c.windows[channel].rerenderText()
		self.settings[SETTING_DISPLAY_TIMESTAMP_SECONDS] = self.use_seconds_in_timestamp
		save_settings(self.settings,self.settings_file)

	def menuToggle24HourClock(self):
		if self.use_24_hour_timestamp:
			self.use_24_hour_timestamp = False
		else:
			self.use_24_hour_timestamp = True

		for c in self.connections:
			c.console.rerenderText()
			for channel in c.windows:
				c.windows[channel].rerenderText()
		self.settings[SETTING_24HOUR_TIMESTAMPS] = self.use_24_hour_timestamp
		save_settings(self.settings,self.settings_file)

	def menuToggleTimestamp(self):
		if self.display_timestamp:
			self.display_timestamp = False
		else:
			self.display_timestamp = True

		for c in self.connections:
			c.console.rerenderText()
			for channel in c.windows:
				c.windows[channel].rerenderText()
		self.settings[SETTING_DISPLAY_TIMESTAMPS] = self.display_timestamp
		save_settings(self.settings,self.settings_file)

	def menuPlainUserLists(self):
		if self.plain_user_lists:
			self.plain_user_lists = False
		else:
			self.plain_user_lists = True
		self.settings[SETTING_PLAIN_USER_LISTS] = self.plain_user_lists
		save_settings(self.settings,self.settings_file)

		for c in self.connections:
			for channel in c.windows:
				if c.windows[channel].is_channel:
					c.windows[channel].refreshUserlist()

	def menuChatStatusBars(self):
		if self.display_status_bar_on_chat_windows:
			self.display_status_bar_on_chat_windows = False
			for c in self.connections:
				for channel in c.windows:
					c.windows[channel].status.hide()
		else:
			self.display_status_bar_on_chat_windows = True
			for c in self.connections:
				for channel in c.windows:
					c.windows[channel].status.show()
		self.settings[SETTING_CHAT_STATUS_BARS] = self.display_status_bar_on_chat_windows
		save_settings(self.settings,self.settings_file)

	def menuPrivateWindows(self):
		if self.open_private_chat_windows:
			self.open_private_chat_windows = False
		else:
			self.open_private_chat_windows = True
		self.settings[SETTING_OPEN_PRIVATE_WINDOWS] = self.open_private_chat_windows
		save_settings(self.settings,self.settings_file)

	def menuKeepAlive(self):
		if self.keep_alive:
			self.keep_alive = False
			for c in self.connections:
				try:
					c.connection.stopHeartbeat()
				except:
					pass
		else:
			self.keep_alive = True
			for c in self.connections:
				try:
					c.connection.startHeartbeat()
				except:
					pass
		self.settings[SETTING_KEEP_ALIVE] = self.keep_alive
		save_settings(self.settings,self.settings_file)

	def menuFont(self):
		font, ok = QFontDialog.getFont()
		if ok:
			# Save settings
			self.settings[SETTING_APPLICATION_FONT] = font.toString()
			save_settings(self.settings,self.settings_file)

			self.font_string = self.settings[SETTING_APPLICATION_FONT]
			self.font = font

			pf = self.font_string.split(',')
			mf = pf[0]
			ms = pf[1]
			self.actFont.setText(f"Font ({mf}, {ms}pt)")

			# Set font to all windows & widgets
			self.app.setFont(font)
			self.setFont(font)
			self.MDI.setFont(font)
			self.menubar.setFont(font)
			for c in self.connections:
				c.console.setFont(font)
				for channel in c.windows:
					c.windows[channel].setFont(font)
					if not c.windows[channel].is_console:
						if self.display_status_bar_on_chat_windows:
							c.windows[channel].status_text.setFont(font)

	def menuRestart(self):
		restart_program()

	def menuNetwork(self):
		info = NetworkDialog()
		if info!=None:
			if len(info.autojoin)>0:
				self.autojoins[info.server] = info.autojoin
			self.connectToIRCServer(info)

	def menuConnect(self):
		info = ConnectDialog(self)
		if info!=None:
			if len(info.autojoin)>0:
				self.autojoins[info.server] = info.autojoin
			self.connectToIRCServer(info)

	def triggerRebuildConnections(self):
		self.buildConnectionsMenu()

	def view_motd(self,obj):

		for c in self.connections:
			if c.id==obj.id:
				if c.motd:
					c.motd_window = TextWindow("MOTD ("+obj.server+":"+str(obj.port)+")",self.MDI,obj,self)
					for l in c.motd:
						c.motd_window.write(l)

	def buildConnectionsMenu(self):
		# self.connectionsMenu
		self.connectionsMenu.clear()
		scount = 0
		for c in self.connections:
			# c.console.buildConnectionMenu(self.connectionsMenu,c)
			# scount = scount + 1
			try:
				c.console.buildConnectionMenu(self.connectionsMenu,c)
				scount = scount + 1
			except:
				pass

			#self.connectionsMenu.addSeparator()

		if scount==0:
			noConnectionsLabel = QLabel(f"<center><i>Not connected to any servers.</i></center>")
			noConnectionsAction = QWidgetAction(self)
			noConnectionsAction.setDefaultWidget(noConnectionsLabel)
			self.connectionsMenu.addAction(noConnectionsAction)

			self.connectionsMenu.addSeparator()

		self.connectionsMenu.addSeparator()

		self.actSaveHistory = QAction("Save server history",self,checkable=True)
		self.actSaveHistory.setChecked(self.save_server_history)
		self.actSaveHistory.triggered.connect(self.menuToggleHistory)
		self.connectionsMenu.addAction(self.actSaveHistory)

		self.actKeepAlive = QAction("Keep connections alive",self,checkable=True)
		self.actKeepAlive.setChecked(self.keep_alive)
		self.actKeepAlive.triggered.connect(self.menuKeepAlive)
		self.connectionsMenu.addAction(self.actKeepAlive)

		self.actRejoin = QAction("Rejoin channels on disconnection",self,checkable=True)
		self.actRejoin.setChecked(self.rejoin_channels)
		self.actRejoin.triggered.connect(self.menuRejoin)
		self.connectionsMenu.addAction(self.actRejoin)

	# |=============|
	# | QT CODE END |
	# |=============|

	def oldschoolMode(self):

		self.display_status_bar_on_chat_windows = False
		self.plain_user_lists = True
		self.display_timestamp = True
		self.use_24_hour_timestamp = True
		self.load_logs_on_start = False
		self.save_logs_on_quit = False
		self.spellCheck = False
		self.use_asciimojis	= False
		self.use_emojis = False
		self.autocomplete_commands = False
		self.autocomplete_nicks = False
		self.convert_links_in_chat = False
		self.strip_html_from_chat = True
		self.log_private_chat = False
		self.hide_private_chat = False
		self.save_server_history = False
		self.filter_profanity = False
		self.display_uptime_console	= False
		self.display_uptime_chat = False
		self.display_uptime_seconds = False
		self.display_irc_colors	= False
		self.autocomplete_asciimoji = False
		self.autocomplete_emoji = False
		self.set_window_title_to_active = False


		self.actHidePrivate.setEnabled(False)
		self.actHidePrivate.setChecked(False)

		self.actStatusBars.setEnabled(False)
		self.actStatusBars.setChecked(False)

		self.actWindowTitle.setEnabled(False)
		self.actWindowTitle.setChecked(False)

		self.actPlainUserLists.setEnabled(False)
		self.actPlainUserLists.setChecked(True)

		self.actConsoleUptime.setEnabled(False)
		self.actConsoleUptime.setChecked(False)

		self.actChatUptime.setEnabled(False)
		self.actChatUptime.setChecked(False)

		self.actSecondsUptime.setEnabled(False)
		self.actSecondsUptime.setChecked(False)

		self.actToggleTimestamp.setEnabled(False)
		self.actToggleTimestamp.setChecked(True)

		self.actToggle24Clock.setEnabled(False)
		self.actToggle24Clock.setChecked(True)

		self.actToggleSecondsTimestamp.setEnabled(False)
		self.actToggleSecondsTimestamp.setChecked(False)

		self.actSaveLogs.setEnabled(False)
		self.actSaveLogs.setChecked(False)

		self.actLoadLogs.setEnabled(False)
		self.actLoadLogs.setChecked(False)

		self.actPrivateLogs.setEnabled(False)
		self.actPrivateLogs.setChecked(False)

		self.actEmoji.setEnabled(False)
		self.actEmoji.setChecked(False)

		self.actAsciimoji.setEnabled(False)
		self.actAsciimoji.setChecked(False)

		self.actChatUrls.setEnabled(False)
		self.actChatUrls.setChecked(False)

		self.actStripHtml.setEnabled(False)
		self.actStripHtml.setChecked(True)

		self.actProfanity.setEnabled(False)
		self.actProfanity.setChecked(False)

		self.actColor.setEnabled(False)
		self.actColor.setChecked(False)

		self.actAutoCmds.setEnabled(False)
		self.actAutoCmds.setChecked(False)

		self.actAutoNicks.setEnabled(False)
		self.actAutoNicks.setChecked(False)

		self.actAutoAsciimoji.setEnabled(False)
		self.actAutoAsciimoji.setChecked(False)

		self.actAutoEmoji.setEnabled(False)
		self.actAutoEmoji.setChecked(False)

		self.optSpellCheck.setEnabled(False)
		self.optSpellCheck.setChecked(False)

		self.scEnglish.setEnabled(False)
		self.scFrench.setEnabled(False)
		self.scSpanish.setEnabled(False)
		self.scGerman.setEnabled(False)

	def noIgnore(self):
		self.allow_ignore = False
		self.actIgnore.setVisible(False)
		self.actToggleIgnore.setEnabled(False)

class Clock(QThread):

	beat = pyqtSignal()

	def __init__(self,parent=None):
		super(Clock, self).__init__(parent)
		self.threadactive = True

	def run(self):
		while self.threadactive:
			time.sleep(0.5)
			self.beat.emit()

	def stop(self):
		self.threadactive = False
		self.wait()