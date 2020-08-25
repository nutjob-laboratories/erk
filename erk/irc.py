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

SSL_AVAILABLE = True

import sys
import random
import string
from collections import defaultdict
import time
import fnmatch

from .resources import *
from .files import *
from .strings import *
from .objects import *
from . import config
from . import events

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from .dialogs import(
	NeterrorDialog
	)

from twisted.internet import reactor, protocol

try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

from twisted.words.protocols import irc
from twisted.words.protocols.irc import ctcpStringify


def connect(**kwargs):
	bot = IRC_Connection_Factory(**kwargs)
	reactor.connectTCP(kwargs["server"],kwargs["port"],bot)

def connectSSL(**kwargs):
	bot = IRC_Connection_Factory(**kwargs)
	reactor.connectSSL(kwargs["server"],kwargs["port"],bot,ssl.ClientContextFactory())

def reconnect(**kwargs):
	bot = IRC_ReConnection_Factory(**kwargs)
	reactor.connectTCP(kwargs["server"],kwargs["port"],bot)

def reconnectSSL(**kwargs):
	bot = IRC_ReConnection_Factory(**kwargs)
	reactor.connectSSL(kwargs["server"],kwargs["port"],bot,ssl.ClientContextFactory())

client = None

def generateID(tlength=16):
	letters = string.ascii_letters
	return ''.join(random.choice(letters) for i in range(tlength))

# =====================================
# | TWISTED IRC CONNECTION MANAGEMENT |
# =====================================

class IRC_Connection(irc.IRCClient):
	nickname = 'bot'
	realname = 'bot'
	username = 'bot'

	versionName = APPLICATION_NAME
	versionNum = APPLICATION_VERSION
	sourceURL = OFFICIAL_REPOSITORY

	heartbeatInterval = 120

	def irc_RPL_AWAY(self,prefix,params):
		user = params[1]
		msg = params[2]

		# Make sure to not display the away message
		# if the reason why we're receiving it is
		# because of an automatic "whois" request
		for nick in self.request_whois:
			if nick==user: return

		
		events.user_away(self.gui,self,user,msg)

		# self.gui.irc_user_away(self,user,msg)

	def irc_RPL_UNAWAY(self,prefix,params):
		msg = params[1]

		self.is_away = False
		events.build_connection_display(self.gui)

		# self.gui.irc_not_away(self,msg)
		#events.client_unaway(self.gui,self)

	def irc_RPL_NOWAWAY(self,prefix,params):

		msg = params[1]

		self.is_away = True
		events.build_connection_display(self.gui)

		# self.gui.irc_is_away(self,msg)

		#events.client_away(self.gui,self)


	def irc_RPL_BANLIST(self,prefix,params):
		channel = params[1]
		ban = params[2]
		banner = params[3]

		e = [ban,banner]
		self.banlists[channel].append(e)
			


	def irc_RPL_ENDOFBANLIST(self,prefix,params):
		channel = params[1]

		banlist = []
		if channel in self.banlists:
			banlist = self.banlists[channel]
			self.banlists[channel] = []

		# self.gui.irc_banlist(self,channel,banlist)

		# events.received_network_and_hostname(self.gui,self,p[1],self.hostname)

		# banlist(gui,client,channel,banlist):

		events.banlist(self.gui,self,channel,banlist)


	def isupport(self,options):
		self.options = options

		for o in options:
			p = o.split('=')
			if len(p)==2:
				if p[0].lower()=='network':
					self.network = p[1]


					# self.gui.irc_network_and_hostname(self,p[1],self.hostname)
					#events.received_network_and_hostname(self.gui,self,p[1],self.hostname)

					# update_user_history_network(host,port,network,filename=USER_FILE):
					# if self.gui.save_history:
					# 	update_user_history_network(self.server,self.port,p[1])


		self.server_options(options)

		# self.gui.irc_options(self,options)
		events.server_options(self.gui,self,options)

		

	def __init__(self,**kwargs):

		self.kwargs = kwargs

		objectconfig(self,**kwargs)

		self.oldnick = self.nickname

		self.id = generateID()
		self.network = 'Unknown'

		self.userlists = defaultdict(list)
		self.banlists = defaultdict(list)

		self.whois = {}

		self.is_away = False

		self.uptime = 0

		self.joined_channels = []
		self.do_whois = []
		self.request_whois = []

		self.registered = False

		self.flat_motd = ''

		self.last_tried_nickname = ''

		# BEGIN SERVER INFO

		self.maxnicklen = 0
		self.maxchannels = 0
		self.channellen = 0
		self.topiclen = 0
		self.kicklen = 0
		self.awaylen = 0
		self.maxtargets = 0
		self.casemapping = ""
		self.cmds = []
		self.prefix = []
		self.chanmodes = []
		self.supports = []
		self.modes = 0
		self.maxmodes = []

		self.safelist = False

		self.channels = []
		self.channellist = []

		self.last_fetch = 0

		self.list_requested = False
		self.list_window = None
		self.list_search = None

		# END SERVER INFO

		entry = [self.server,self.port]
		self.gui.connecting.append(entry)
		self.gui.start_spinner()

		events.startup(self.gui,self)

	def uptime_beat(self):

		self.uptime = self.uptime + 1

		#self.gui.uptime(self,self.uptime)
		events.uptime(self.gui,self,self.uptime)
		
		# self.gui.irc_uptime(self,self.uptime)

		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
			if len(self.do_whois)>0:
				nick = self.do_whois.pop(0)
				if len(nick.strip())>0:
					self.request_whois.append(nick)
					self.sendLine("WHOIS "+nick)

		# Refresh internal userlist
		if config.AUTOMATICALLY_FETCH_CHANNEL_LIST:
			if self.uptime % config.CHANNEL_LIST_REFRESH_FREQUENCY==0:
				self.sendLine("LIST")
				self.last_fetch = self.uptime


	def connectionMade(self):

		# PROTOCTL UHNAMES
		self.sendLine("PROTOCTL UHNAMES")

		# self.gui.irc_connect(self)

		# self.uptimeTimer = UptimeHeartbeat()
		# self.uptimeTimer.beat.connect(self.uptime_beat)
		# self.uptimeTimer.start()

		try:
			self._erk_net_connection_lost.close()
		except:
			pass

		events.connection(self.gui,self)

		irc.IRCClient.connectionMade(self)

	def connectionLost(self, reason):

		# self.gui.irc_disconnect(self,reason)

		# MUST BE ABLE TO TRACK AND SAVE KEY FOR THIS TO ACTUALLY WORK
		# if config.SAVE_JOINED_CHANNELS:
		# 	u = get_user()
		# 	u["channels"] = self.kwargs["autojoin"]
		# 	save_user(u)

		if hasattr(self,"uptimeTimer"):
			self.uptimeTimer.stop()
			self.uptime = 0
		else:
			print("Error connecting to server")

		self.last_tried_nickname = ''

		self.registered = False

		try:
			self._erk_net_connection_lost.close()
		except:
			pass

		events.disconnection(self.gui,self)

		irc.IRCClient.connectionLost(self, reason)

	def signedOn(self):

		events.registered(self.gui,self)

		self.uptimeTimer = UptimeHeartbeat()
		self.uptimeTimer.beat.connect(self.uptime_beat)
		self.uptimeTimer.start()

		self.registered = True

		# self.gui.irc_registered(self)
		if len(self.autojoin)>0:
			for channel in self.autojoin:
				chan = channel[0]
				key = channel[1]
				if len(key)>0:
					self.sendLine(f"JOIN {chan} {key}")
				else:
					self.sendLine(f"JOIN {chan}")

	def joined(self, channel):
		self.sendLine(f"MODE {channel}")
		self.sendLine(f"MODE {channel} +b")

		self.joined_channels.append(channel)

		events.erk_joined_channel(self.gui,self,channel)

		# self.gui.irc_client_joined(self,channel)
		self.autojoin.append( [channel,''] )

	def left(self, channel):

		events.erk_left_channel(self.gui,self,channel)

		clean = []
		for c in self.autojoin:
			if c[0]==channel: continue
			clean.append(c)
		self.autojoin = clean

	def privmsg(self, user, target, msg):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]

		# self.gui.irc_privmsg(self,user,target,msg)

		if target==self.nickname:
			events.private_message(self.gui,self,user,msg)
		else:
			events.public_message(self.gui,self,target,user,msg)

	def noticed(self, user, channel, msg):
		tok = user.split('!')
		if len(tok) >= 2:
			pnick = tok[0]
			phostmask = tok[1]
		else:
			pnick = user
			phostmask = user

		# self.gui.irc_notice(self,user,channel,msg)
		events.notice_message(self.gui,self,channel,user,msg)

	def receivedMOTD(self, motd):
		# self.gui.irc_motd(self,motd)
		events.motd(self.gui,self,motd)

		#self.flat_motd = "\n".join(motd)
		#self.flat_motd = convert_irc_color_to_html(self.flat_motd)

	def modeChanged(self, user, channel, mset, modes, args):
		if "b" in modes: self.sendLine(f"MODE {channel} +b")
		if "o" in modes: self.sendLine("NAMES "+channel)
		if "v" in modes: self.sendLine("NAMES "+channel)

		# self.gui.irc_mode(self,user,channel,mset,modes,args)
		events.mode(self.gui,self,channel,user,mset,modes,args)

		for m in modes:
			if m=='k':
				if mset:
					# Update autojoins
					if len(self.autojoin)>0:
						chans = []
						changed = False
						key=args[0]
						for c in self.autojoin:
							chan = c[0]
							ckey = c[1]
							if chan==channel:
								changed = True
								e = [channel,key]
								chans.append(e)
								continue
							chans.append(c)
						if changed: self.autojoin = chans
				else:
					if len(self.autojoin)>0:
						chans = []
						changed = False
						for c in self.autojoin:
							chan = c[0]
							ckey = c[1]
							if chan==channel:
								changed = True
								e = [channel,'']
								chans.append(e)
								continue
							chans.append(c)
						if changed: self.autojoin = chans

		
		
	def nickChanged(self,nick):
		# self.gui.irc_nick_changed(self,self.nickname,nick)
		self.nickname = nick
		## self.gui.irc_nick(self,nick)
		# self.gui.buildConnectionsMenu()
		events.erk_changed_nick(self.gui,self,nick)

		for c in events.fetch_channel_list(self):
			self.sendLine("NAMES "+c)

	def userJoined(self, user, channel):
		if user.split('!')[0] == self.nickname:
			return

		p = user.split('!')
		if len(p)==2:
			if p[0] == self.nickname: return
		else:
			if config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
				self.do_whois.append(user)

		# self.gui.irc_join(self,user,channel)
		events.join(self.gui,self,user,channel)

		self.sendLine("NAMES "+channel)


	def userLeft(self, user, channel):

		# self.gui.irc_part(self,user,channel)
		events.part(self.gui,self,user,channel)

		self.sendLine("NAMES "+channel)

	def irc_ERR_NICKNAMEINUSE(self, prefix, params):

		if self.registered:
			# Since we're already registered, just
			# let the user know that the desired nickname
			# is already in use
			events.erk_nickname_in_use(self.gui,self,params[1])
			return

		oldnick = params[1]

		if self.last_tried_nickname=='':
			self.last_tried_nickname = self.alternate
			self.setNick(self.alternate)
			events.erk_changed_nick(self.gui,self,self.alternate)
			return

		self.last_tried_nickname = self.last_tried_nickname + "_"
		self.setNick(self.last_tried_nickname)
		events.erk_changed_nick(self.gui,self,self.last_tried_nickname)

	def userRenamed(self, oldname, newname):

		for c in events.where_is_user(self,oldname):
			self.sendLine("NAMES "+c)

		# self.gui.irc_nick_changed(self,oldname,newname)
		events.nick(self.gui,self,oldname,newname)
					
	def topicUpdated(self, user, channel, newTopic):
		
		# self.gui.irc_topic(self,user,channel,newTopic)
		events.topic(self.gui,self,user,channel,newTopic)

	def action(self, user, channel, data):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]
		
		# self.gui.irc_action(self,user,channel,data)
		events.action_message(self.gui,self,channel,user,data)
		

	def userKicked(self, kickee, channel, kicker, message):
		self.sendLine("NAMES "+channel)

		msg = Message(SYSTEM_MESSAGE,'',kickee+" was kicked from "+channel+" by "+kicker+" ("+message+")")

		win = events.fetch_console_window(self)
		if win:
			win.writeText( msg )

		win = events.fetch_channel_window(self,channel)
		if win:
			win.writeText( msg )


	def kickedFrom(self, channel, kicker, message):

		events.kicked_channel_window(self,channel)

		win = events.fetch_console_window(self)
		if win:
			win.writeText( Message(SYSTEM_MESSAGE,'',"You were kicked from "+channel+" by "+kicker+" ("+message+")") )

	def irc_QUIT(self,prefix,params):
		x = prefix.split('!')
		if len(x) >= 2:
			nick = x[0]
		else:
			nick = prefix
		if len(params) >=1:
			m = params[0].split(':')
			if len(m)>=2:
				msg = m[1].strip()
			else:
				msg = ""
		else:
			msg = ""

		for c in events.where_is_user(self,nick):
			self.sendLine("NAMES "+c)

		# self.gui.irc_quit(self,prefix,msg)
		events.quit(self.gui,self,nick,msg)


	def irc_RPL_NAMREPLY(self, prefix, params):
		channel = params[2].lower()
		nicklist = params[3].split(' ')

		if channel in self.joined_channels:
			if config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
				for u in nicklist:
					p = u.split('!')
					if len(p)!=2:
						u = u.replace('@','')
						u = u.replace('+','')
						if not events.channel_has_hostmask(self.gui,self,channel,u):
							self.do_whois.append(u)

		if channel in self.userlists:
			# Add to user list
			self.userlists[channel] = self.userlists[channel] + nicklist
			# Remove duplicates
			self.userlists[channel] = list(dict.fromkeys(self.userlists[channel]))
		else:
			self.userlists[channel] = nicklist

		

	def irc_RPL_ENDOFNAMES(self, prefix, params):

		channel = params[1].lower()

		try:
			self.joined_channels.remove(channel)
		except:
			pass

		if channel in self.userlists:
			#self.gui.irc_userlist(self,channel,self.userlists[channel])
			events.userlist(self.gui,self,channel,self.userlists[channel])
			del self.userlists[channel]

	def irc_RPL_TOPIC(self, prefix, params):
		# global TOPIC
		if not params[2].isspace():
			TOPIC = params[2]
		else:
			TOPIC = ""

		channel = params[1]

		# self.gui.irc_topic(self,self.hostname,channel,TOPIC)
		events.topic(self.gui,self,'',channel,TOPIC)

		

	def irc_RPL_WHOISCHANNELS(self, prefix, params):
		params.pop(0)
		nick = params.pop(0)
		channels = ", ".join(params)

		if nick in self.request_whois: return

		if nick in self.whois:
			self.whois[nick].channels = channels
		else:
			self.whois[nick] = WhoisData()
			self.whois[nick].nickname = nick
			self.whois[nick].channels = channels

		

	def irc_RPL_WHOISUSER(self, prefix, params):
		nick = params[1]
		username = params[2]
		host = params[3]
		realname = params[5]

		if nick in self.request_whois:
			#self.gui.update_user_hostmask(self,nick,username+"@"+host)
			events.received_hostmask_for_channel_user(self.gui,self,nick,username+"@"+host)
			return

		if nick in self.whois:
			self.whois[nick].username = username
			self.whois[nick].host = host
			self.whois[nick].realname = realname
		else:
			self.whois[nick] = WhoisData()
			self.whois[nick].nickname = nick
			self.whois[nick].username = username
			self.whois[nick].host = host
			self.whois[nick].realname = realname

		

	def irc_RPL_WHOISIDLE(self, prefix, params):
		params.pop(0)
		nick = params.pop(0)
		idle_time = params.pop(0)
		signed_on = params.pop(0)

		if nick in self.request_whois: return

		if nick in self.whois:
			self.whois[nick].idle = idle_time
			self.whois[nick].signon = signed_on
		else:
			self.whois[nick] = WhoisData()
			self.whois[nick].nickname = nick
			self.whois[nick].idle = idle_time
			self.whois[nick].signon = signed_on

		

	def irc_RPL_WHOISSERVER(self, prefix, params):
		nick = params[1]
		server = params[2]

		if nick in self.request_whois: return

		if nick in self.whois:
			self.whois[nick].server = server
		else:
			self.whois[nick] = WhoisData()
			self.whois[nick].nickname = nick
			self.whois[nick].server = server

	def irc_RPL_WHOISOPERATOR(self,prefix,params):
		nick = params[1]
		privs = params[2]

		if nick in self.request_whois: return

		if nick in self.whois:
			self.whois[nick].privs = privs
		else:
			self.whois[nick] = WhoisData()
			self.whois[nick].nickname = nick
			self.whois[nick].privs = privs

	def irc_RPL_ENDOFWHOIS(self, prefix, params):
		nick = params[1]

		if nick in self.request_whois:
			try:
				self.request_whois.remove(nick)
			except:
				pass
			return

		if nick in self.whois:
			#self.gui.irc_whois(self,self.whois[nick])
			events.received_whois(self.gui,self,self.whois[nick])
			del self.whois[nick]

		

	def irc_RPL_WHOWASUSER(self, prefix, params):
		nick = params[1]
		username = params[2]
		host = params[3]
		realname = params[5]

		


	def irc_RPL_ENDOFWHOWAS(self, prefix, params):
		nick = params[1]

		

	def irc_RPL_WHOREPLY(self, prefix, params):
		channel = params[1]
		username = params[2]
		host = params[3]
		server = params[4]
		nick = params[5]
		hr = params[7].split(' ')

	def irc_RPL_ENDOFWHO(self, prefix, params):
		nick = params[1]
		#server_info_msg_display(ircform,"WHO",f"End of who data for {nick}")

	def irc_RPL_VERSION(self, prefix, params):
		sversion = params[1]
		server = params[2]

	def irc_RPL_CHANNELMODEIS(self, prefix, params):
		params.pop(0)
		channel = params.pop(0)

		for m in params:
			if len(m)>0:
				if m[0] == "+":
					m = m[1:]

					if m=="k":
						params.pop(0)
						chankey = params.pop(0)
						# self.gui.irc_mode(self,self.hostname,channel,True,m,[chankey])
						events.mode(self.gui,self,channel,self.hostname,True,m,[chankey])

						# Update autojoins
						if len(self.autojoin)>0:
							chans = []
							changed = False
							for c in self.autojoin:
								chan = c[0]
								key = c[1]
								if chan==channel:
									changed = True
									e = [channel,chankey]
									chans.append(e)
									continue
								chans.append(c)
							if changed: self.autojoin = chans
						continue
					# mode added
					# self.gui.irc_mode(self,self.hostname,channel,True,m,[])
					events.mode(self.gui,self,channel,self.hostname,True,m,[])
				else:
					m = m[1:]
					# mode removed
					# self.gui.irc_mode(self,self.hostname,channel,False,m,[])
					events.mode(self.gui,self,channel,self.hostname,False,m,[])

					# Update autojoins
					if m=="k":
						if len(self.autojoin)>0:
							chans = []
							changed = False
							for c in self.autojoin:
								chan = c[0]
								key = c[1]
								if chan==channel:
									changed = True
									e = [channel,'']
									chans.append(e)
									continue
								chans.append(c)
							if changed: self.autojoin = chans
		
		

	def irc_RPL_YOUREOPER(self, prefix, params):
		
		events.erk_youre_oper(self.gui,self)

	def irc_RPL_TIME(self, prefix, params):
		t = params[2]


	def irc_INVITE(self,prefix,params):
		#print("INVITE",prefix,params)
		p = prefix.split("!")
		if len(p)==2:
			nick = p[0]
			hostmask = p[1]
		else:
			nick = prefix
			hostmask = None

		target = params[0]
		channel = params[1]

		# self.gui.irc_invited(self,prefix,target,channel)
		#events.writeInviteActiveWindow(self.gui,self,prefix,channel)

		events.erk_invited(self.gui,self,prefix,channel)
		


	def irc_RPL_INVITING(self,prefix,params):
		user = params[1]
		channel = params[2]

		# self.gui.irc_inviting(self,user,channel)
		#events.writeInvitingActiveWindow(self.gui,self,user,channel)

		events.erk_inviting(self.gui,self,user,channel)

		

	def irc_RPL_LIST(self,prefix,params):

		server = prefix
		channel = params[1]
		usercount = params[2]
		topic = params[3]

		# self.gui.irc_list(self,server,channel,usercount,topic)
		#print(channel,usercount,topic)

		self.channels.append(channel)
		e = ChannelInfo(channel,usercount,topic)
		self.channellist.append(e)

		# self.list_requested = False
		# self.list_window = None

		if self.list_requested:
			
			found = False
			if self.list_search!=None:
				if fnmatch.fnmatch(e.name,self.list_search): found = True
				if fnmatch.fnmatch(e.topic,self.list_search): found = True

			if self.list_search!=None:
				if not found: return

			if len(e.topic.strip())>0:
				msg = Message(PLUGIN_MESSAGE,'',"<a href=\""+e.name+"\">"+e.name+"</a> ("+str(e.count)+" users) - "+e.topic)
			else:
				msg = Message(PLUGIN_MESSAGE,'',"<a href=\""+e.name+"\">"+e.name+"</a> ("+str(e.count)+" users)")
			self.list_window.writeText(msg,True)


	def irc_RPL_LISTSTART(self,prefix,params):
		server = prefix

		# self.gui.irc_start_list(self,server)

		self.channels = []
		self.channellist= []

		self.last_fetch = self.uptime

		if self.list_requested:
			#msg = Message(PLUGIN_MESSAGE,'',"<b>BEGIN CHANNEL LIST</b>")
			#self.list_window.writeText(msg,True)

			msg = Message(HORIZONTAL_RULE_MESSAGE,'','')
			self.list_window.writeText(msg,True)

			if self.list_search!=None:
				msg = Message(PLUGIN_MESSAGE,'',"Channels with <b><i>"+self.list_search+"</i></b> in the name or topic")
				self.list_window.writeText(msg,True)

		

	def irc_RPL_LISTEND(self,prefix,params):
		server = prefix

		# self.gui.irc_end_list(self,server)

		# if self.list_requested:
		# 	msg = Message(HORIZONTAL_RULE_MESSAGE,'','')
		# 	self.list_window.writeText(msg,True)

		self.list_requested = False
		self.list_window = None
		self.list_search = None

	def irc_RPL_TIME(self,prefix,params):

		server = params[1]
		time = params[2]

		#events.writeTimeActiveWindow(self.gui,self,server,time)

	def irc_RPL_USERHOST(self,prefix,params):
		data = params[1]

		#events.writeUserhostActiveWindow(self.gui,self,data)

	def sendLine(self,line):
		
		# self.gui.irc_output(self,line)
		#print(line)

		events.line_output(self.gui,self,line)

		return irc.IRCClient.sendLine(self, line)

	def irc_ERR_NOSUCHNICK(self,prefix,params):
		events.received_error(self.gui,self,params[1]+": "+params[2])

	def irc_ERR_NOSUCHSERVER(self,prefix,params):
		events.received_error(self.gui,self,params[1]+": "+params[2])

	def irc_ERR_NOSUCHCHANNEL(self,prefix,params):
		events.received_error(self.gui,self,params[1]+": "+params[2])

	def irc_ERR_CANNOTSENDTOCHAN(self,prefix,params):
		events.received_error(self.gui,self,params[1]+": "+params[2])


	def msg(self,target,msg,write=True):

		if write:
			found = False
			for window in events.fetch_window_list(self):
				if window.name==target:
					out = Message(SELF_MESSAGE,self.nickname,msg)
					window.writeText(out)
					found = True

			if not found:
				if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
					# target is not a channel
					if config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
						w = events.open_private_window(self,target)
						if w:
							out = Message(SELF_MESSAGE,self.nickname,msg)
							w.writeText(out)

		return irc.IRCClient.msg(self, target, msg)

	def describe(self,target,msg,write=True):

		if write:
			found = False
			for window in events.fetch_window_list(self):
				if window.name==target:
					out = Message(ACTION_MESSAGE,self.nickname,msg)
					window.writeText(out)
					found = True

			if not found:
				if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
					# target is not a channel
					if config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
						w = events.open_private_window(self,target)
						if w:
							out = Message(ACTION_MESSAGE,self.nickname,msg)
							w.writeText(out)

		return irc.IRCClient.describe(self, target, msg)

	def notice(self,target,msg,write=True):

		if write:
			found = False
			for window in events.fetch_window_list(self):
				if window.name==target:
					out = Message(NOTICE_MESSAGE,self.nickname,msg)
					window.writeText(out)
					found = True

			if not found:
				if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
					# target is not a channel
					if config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
						w = events.open_private_window(self,target)
						if w:
							out = Message(NOTICE_MESSAGE,self.nickname,msg)
							w.writeText(out)

		return irc.IRCClient.notice(self, target, msg)

	def ctcpMakeReply(self, user, messages):
		"""
		Send one or more C{extended messages} as a CTCP reply.
		@type messages: a list of extended messages.  An extended
		message is a (tag, data) tuple, where 'data' may be C{None}.
		"""
		self.notice(user, ctcpStringify(messages),False)

	def ctcpMakeQuery(self, user, messages):
		"""
		Send one or more C{extended messages} as a CTCP query.
		@type messages: a list of extended messages.  An extended
		message is a (tag, data) tuple, where 'data' may be C{None}.
		"""
		self.msg(user, ctcpStringify(messages), False)

	def lineReceived(self, line):

		# Decode the incoming text line
		try:
			line2 = line.decode('utf-8')
		except UnicodeDecodeError:
			try:
				line2 = line.decode('iso-8859-1')
			except UnicodeDecodeError:
				line2 = line.decode("CP1252", 'replace')

		# Re-encode the text line to utf-8 for all other
		# IRC events (this fixes an error raised when attempting
		# to get a channel list from a server)
		line = line2.encode('utf-8')

		#print(line)
		# self.gui.irc_input(self,line2)

		events.line_input(self.gui,self,line2)

		d = line2.split(" ")
		if len(d) >= 2:
			if d[1].isalpha(): return irc.IRCClient.lineReceived(self, line)

		if "Cannot join channel (+k)" in line2:
			events.received_error(self.gui,self,f"Cannot join channel (wrong or missing password)")
			pass
		if "Cannot join channel (+l)" in line2:
			events.received_error(self.gui,self,f"Cannot join channel (channel is full)")
			pass
		if "Cannot join channel (+b)" in line2:
			events.received_error(self.gui,self,f"Cannot join channel (banned)")
			pass
		if "Cannot join channel (+i)" in line2:
			events.received_error(self.gui,self,f"Cannot join channel (channel is invite only)")
			pass
		if "not an IRC operator" in line2:
			events.received_error(self.gui,self,"Permission denied (you're not an IRC operator")
			pass
		if "not channel operator" in line2:
			events.received_error(self.gui,self,"Permission denied (you're not channel operator)")
			pass
		if "is already on channel" in line2:
			events.received_error(self.gui,self,"Invite failed (user is already in channel)")
			pass
		if "not on that channel" in line2:
			events.received_error(self.gui,self,"Permission denied (you're not in channel)")
			pass
		if "aren't on that channel" in line2:
			events.received_error(self.gui,self,"Permission denied (target user is not in channel)")
			pass
		if "have not registered" in line2:
			events.received_error(self.gui,self,"You're not registered")
			pass
		if "may not reregister" in line2:
			events.received_error(self.gui,self,"You can't reregister")
			pass
		if "enough parameters" in line2:
			events.received_error(self.gui,self,"Error: not enough parameters supplied to command")
			pass
		if "isn't among the privileged" in line2:
			events.received_error(self.gui,self,"Registration refused (server isn't setup to allow connections from your host)")
			pass
		if "Password incorrect" in line2:
			events.received_error(self.gui,self,"Permission denied (incorrect password)")
			pass
		if "banned from this server" in line2:
			events.received_error(self.gui,self,"You are banned from this server")
			pass
		if "kill a server" in line2:
			events.received_error(self.gui,self,"Permission denied (you can't kill a server)")
			pass
		if "O-lines for your host" in line2:
			events.received_error(self.gui,self,"Error: no O-lines for your host")
			pass
		if "Unknown MODE flag" in line2:
			events.received_error(self.gui,self,"Error: unknown MODE flag")
			pass
		if "change mode for other users" in line2:
			events.received_error(self.gui,self,"Permission denied (can't change mode for other users)")
			pass

		return irc.IRCClient.lineReceived(self, line)

	# BEGIN SERVER OPTIONS

	def server_options(self,options):

		# Options are sent in chunks: not every option
		# will be set in each chunk

		supports = []
		maxchannels = 0
		maxnicklen = 0
		nicklen = 0
		channellen = 0
		topiclen = 0
		kicklen = 0
		awaylen = 0
		maxtargets = 0
		modes = 0
		maxmodes = []
		chanmodes = []
		prefix = []
		cmds = []
		casemapping = "none"

		for o in options:
			if "=" in o:
				p = o.split("=")
				if len(p)>1:
					if p[0].lower() == "maxchannels": maxchannels = int(p[1])
					if p[0].lower() == "maxnicklen": maxnicklen = int(p[1])
					if p[0].lower() == "nicklen": nicklen = int(p[1])
					if p[0].lower() == "channellen": channellen = int(p[1])
					if p[0].lower() == "topiclen": topiclen = int(p[1])
					if p[0].lower() == "kicklen": kicklen = int(p[1])
					if p[0].lower() == "awaylen": awaylen = int(p[1])
					if p[0].lower() == "maxtargets": maxtargets = int(p[1])
					if p[0].lower() == "modes": modes = int(p[1])
					if p[0].lower() == "casemapping": casemapping = p[1]

					if p[0].lower() == "cmds":
						for c in p[1].split(","):
							cmds.append(c)

					if p[0].lower() == "prefix":
						pl = p[1].split(")")
						if len(pl)>=2:
							pl[0] = pl[0][1:]	# get rid of prefixed (

							for i in range(len(pl[0])):
								entry = [ pl[0][i], pl[1][i] ]
								prefix.append(entry)

					if p[0].lower() == "chanmodes":
						for e in p[1].split(","):
							chanmodes.append(e)

					if p[0].lower() == "maxlist":
						for e in p[1].split(","):
							ml = e.split(':')
							if len(ml)==2:
								entry = [ml[0],int(ml[1])]
								maxmodes.append(entry)
			else:
				supports.append(o)

		if len(maxmodes)>0: self.maxmodes = maxmodes
		if maxnicklen>0: self.maxnicklen = maxnicklen
		if maxchannels > 0: self.maxchannels = maxchannels
		if channellen > 0: self.channellen = channellen
		if topiclen > 0: self.topiclen = topiclen
		if kicklen > 0: self.kicklen = kicklen
		if awaylen > 0: self.awaylen = awaylen
		if maxtargets > 0: self.maxtargets = maxtargets
		if modes > 0: self.modes = modes
		if casemapping != "": self.casemapping = casemapping

		if len(cmds)>0:
			for c in cmds:
				self.cmds.append(c)

		if len(prefix)>0: self.prefix = prefix
		if len(chanmodes)>0: self.chanmodes = chanmodes
		if len(supports)>0:
			for s in supports:
				self.supports.append(s)

		if config.AUTOMATICALLY_FETCH_CHANNEL_LIST:
			if 'SAFELIST' in self.supports:
				if not self.safelist:
					self.safelist = True
					self.sendLine("LIST")

	# BEGIN SERVER OPTIONS


def objectconfig(obj,**kwargs):

	for key, value in kwargs.items():

		if key=="nickname":
			obj.nickname = value
		
		if key=="alternate":
			obj.alternate = value

		if key=="username":
			obj.username = value

		if key=="realname":
			obj.realname = value

		if key=="server":
			obj.server = value

		if key=="port":
			obj.port = value

		if key=="ssl":
			obj.usessl = value

		if key=="password":
			obj.password = value

		if key=="gui":
			obj.gui = value

		if key=="reconnect":
			obj.reconnect = value

		if key=="autojoin":
			obj.autojoin = value

		if key=="failreconnect":
			obj.failreconnect = value

class IRC_Connection_Factory(protocol.ClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):

		cid = self.kwargs["server"]+str(self.kwargs["port"])
		if cid in self.kwargs["gui"].quitting:
			try:
				self.kwargs["gui"].quitting.remove(cid)
			except:
				pass
			return

		# TODO: Dialog that notifies the user that the connection
		# to the server was lost

		if config.SHOW_CONNECTION_LOST_ERROR:
			self._erk_net_connection_lost = NeterrorDialog("Connection lost",f'Connection to {self.kwargs["server"]}:{str(self.kwargs["port"])} was lost.')
			self._erk_net_connection_lost.server = self.kwargs["server"]
			self._erk_net_connection_lost.port = self.kwargs["port"]

	def clientConnectionFailed(self, connector, reason):

		cid = self.kwargs["server"]+str(self.kwargs["port"])
		if cid in self.kwargs["gui"].quitting:
			try:
				self.kwargs["gui"].quitting.remove(cid)
			except:
				pass
			return

		# TODO: Dialog that notifies the user that the connection
		# to the server failed to establish

		if config.SHOW_CONNECTION_FAIL_ERROR:
			self._erk_net_connection_lost = NeterrorDialog("Connection lost",f'Connection to {self.kwargs["server"]}:{str(self.kwargs["port"])} could not be established.')
			self._erk_net_connection_lost.server = self.kwargs["server"]
			self._erk_net_connection_lost.port = self.kwargs["port"]


class IRC_ReConnection_Factory(protocol.ReconnectingClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):

		cid = self.kwargs["server"]+str(self.kwargs["port"])
		if cid in self.kwargs["gui"].quitting:
			try:
				self.kwargs["gui"].quitting.remove(cid)
			except:
				pass
			return

		if config.SHOW_CONNECTION_LOST_ERROR:
			self._erk_net_connection_lost = NeterrorDialog("Connection lost",f'Connection to {self.kwargs["server"]}:{str(self.kwargs["port"])} was lost.')
			self._erk_net_connection_lost.server = self.kwargs["server"]
			self._erk_net_connection_lost.port = self.kwargs["port"]

		protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):

		cid = self.kwargs["server"]+str(self.kwargs["port"])
		if cid in self.kwargs["gui"].quitting:
			try:
				self.kwargs["gui"].quitting.remove(cid)
			except:
				pass
			return

		# TODO: Dialog that notifies the user that the connection
		# to the server failed to establish

		if config.SHOW_CONNECTION_FAIL_ERROR:
			self._erk_net_connection_lost = NeterrorDialog("Connection lost",f'Connection to {self.kwargs["server"]}:{str(self.kwargs["port"])} could not be established.')
			self._erk_net_connection_lost.server = self.kwargs["server"]
			self._erk_net_connection_lost.port = self.kwargs["port"]

		if self.kwargs["failreconnect"]:
			protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class UptimeHeartbeat(QThread):

	beat = pyqtSignal()

	def __init__(self,parent=None):
		super(UptimeHeartbeat, self).__init__(parent)
		self.threadactive = True

	def run(self):
		while self.threadactive:
			time.sleep(1)
			self.beat.emit()

	def stop(self):
		self.threadactive = False
		self.wait()