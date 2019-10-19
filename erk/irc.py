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

from erk.common import *

from twisted.internet import reactor, protocol

try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

from twisted.words.protocols import irc


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

class WhoisData:
	def __init__(self):
		self.nickname = 'Unknown'
		self.username = 'Unknown'
		self.realname = 'Unknown'
		self.host = 'Unknown'
		self.signon = '0'
		self.idle = '0'
		self.server = 'Unknown'
		self.channels = 'Unknown'
		self.privs = 'is a normal user'

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

		self.gui.irc_banlist(self,channel,banlist)


	def isupport(self,options):
		self.options = options

		for o in options:
			p = o.split('=')
			if len(p)==2:
				if p[0].lower()=='network':
					self.network = p[1]
					self.gui.irc_network_and_hostname(self,p[1],self.hostname)

		self.gui.irc_options(self,options)

	def __init__(self,**kwargs):

		config(self,**kwargs)

		self.oldnick = self.nickname

		self.id = generateID()
		self.network = 'Unknown'

		self.userlists = defaultdict(list)
		self.banlists = defaultdict(list)

		self.whois = {}


	def connectionMade(self):

		# PROTOCTL UHNAMES
		self.sendLine("PROTOCTL UHNAMES")

		self.gui.irc_connect(self)

		irc.IRCClient.connectionMade(self)

	def connectionLost(self, reason):

		self.gui.irc_disconnect(self,reason)

		irc.IRCClient.connectionLost(self, reason)

	def signedOn(self):

		self.gui.irc_registered(self)

	def joined(self, channel):
		self.sendLine(f"MODE {channel}")
		self.sendLine(f"MODE {channel} +b")

		self.gui.irc_client_joined(self,channel)


	def privmsg(self, user, target, msg):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]

		self.gui.irc_privmsg(self,user,target,msg)

	def noticed(self, user, channel, msg):
		tok = user.split('!')
		if len(tok) >= 2:
			pnick = tok[0]
			phostmask = tok[1]
		else:
			pnick = user
			phostmask = user

		self.gui.irc_notice(self,user,channel,msg)

		

	def receivedMOTD(self, motd):
		self.gui.irc_motd(self,motd)

	def modeChanged(self, user, channel, mset, modes, args):
		if "b" in modes: self.sendLine(f"MODE {channel} +b")

		self.gui.irc_mode(self,user,channel,mset,modes,args)
		
		
	def nickChanged(self,nick):
		self.gui.irc_nick_changed(self,self.nickname,nick)
		self.nickname = nick
		#self.gui.irc_nick(self,nick)
		self.gui.buildConnectionsMenu()

	def userJoined(self, user, channel):
		if user.split('!')[0] == self.nickname:
			return

		self.gui.irc_join(self,user,channel)


	def userLeft(self, user, channel):

		self.gui.irc_part(self,user,channel)

	def irc_ERR_NICKNAMEINUSE(self, prefix, params):
		oldnick = self.nickname
		if oldnick != self.alternate:
			newnick = self.alternate
		else:
			newnick = self.nickname + "_"
		#d = systemTextDisplay(f"Nickname \"{oldnick}\" in use, changing nick to \"{newnick}\"",self.gui.maxnicklen,SYSTEM_COLOR)
		self.setNick(newnick)

		self.oldnick = oldnick

	def userRenamed(self, oldname, newname):

		self.gui.irc_nick_changed(self,oldname,newname)
					
	def topicUpdated(self, user, channel, newTopic):
		
		self.gui.irc_topic(self,user,channel,newTopic)

	def action(self, user, channel, data):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]
		
		self.gui.irc_action(self,user,channel,data)
		

	def userKicked(self, kickee, channel, kicker, message):
		self.gui.irc_kick(self,kickee,channel,kicker,message)

	def kickedFrom(self, channel, kicker, message):
		self.gui.irc_kicked(self,channel,kicker,message)

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

		self.gui.irc_quit(self,prefix,msg)


	def irc_RPL_NAMREPLY(self, prefix, params):
		channel = params[2].lower()
		nicklist = params[3].split(' ')

		if channel in self.userlists:
			# Add to user list
			self.userlists[channel] = self.userlists[channel] + nicklist
			# Remove duplicates
			self.userlists[channel] = list(dict.fromkeys(self.userlists[channel]))
		else:
			self.userlists[channel] = nicklist

		

	def irc_RPL_ENDOFNAMES(self, prefix, params):

		channel = params[1].lower()

		if channel in self.userlists:
			self.gui.irc_userlist(self,channel,self.userlists[channel])
			del self.userlists[channel]

	def irc_RPL_TOPIC(self, prefix, params):
		# global TOPIC
		if not params[2].isspace():
			TOPIC = params[2]
		else:
			TOPIC = ""

		channel = params[1]

		self.gui.irc_topic(self,self.hostname,channel,TOPIC)

		

	def irc_RPL_WHOISCHANNELS(self, prefix, params):
		params.pop(0)
		nick = params.pop(0)
		channels = ", ".join(params)

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

		if nick in self.whois:
			self.whois[nick].server = server
		else:
			self.whois[nick] = WhoisData()
			self.whois[nick].nickname = nick
			self.whois[nick].server = server

	def irc_RPL_WHOISOPERATOR(self,prefix,params):
		nick = params[1]
		privs = params[2]

		if nick in self.whois:
			self.whois[nick].privs = privs
		else:
			self.whois[nick] = WhoisData()
			self.whois[nick].nickname = nick
			self.whois[nick].privs = privs

	def irc_RPL_ENDOFWHOIS(self, prefix, params):
		nick = params[1]

		if nick in self.whois:
			self.gui.irc_whois(self,self.whois[nick])
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
					# mode added
					self.gui.irc_mode(self,self.hostname,channel,True,m,[])
				else:
					m = m[1:]
					# mode removed
					self.gui.irc_mode(self,self.hostname,channel,False,m,[])
		
		

	def irc_RPL_YOUREOPER(self, prefix, params):
		pass

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

		


	def irc_RPL_INVITING(self,prefix,params):
		user = params[1]
		channel = params[2]

		

	def irc_RPL_LIST(self,prefix,params):

		server = prefix
		channel = params[1]
		usercount = params[2]
		topic = params[3]

		

	def irc_RPL_LISTSTART(self,prefix,params):
		server = prefix

		

	def irc_RPL_LISTEND(self,prefix,params):
		server = prefix

		

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

		d = line2.split(" ")
		if len(d) >= 2:
			if d[1].isalpha(): return irc.IRCClient.lineReceived(self, line)

		if "Cannot join channel (+k)" in line2:
			self.gui.irc_error(self,f"Cannot join channel (wrong or missing password)")
			pass
		if "Cannot join channel (+l)" in line2:
			self.gui.irc_error(self,f"Cannot join channel (channel is full)")
			pass
		if "Cannot join channel (+b)" in line2:
			self.gui.irc_error(self,f"Cannot join channel (banned)")
			pass
		if "Cannot join channel (+i)" in line2:
			self.gui.irc_error(self,f"Cannot join channel (channel is invite only)")
			pass
		if "not an IRC operator" in line2:
			self.gui.irc_error(self,"Permission denied (you're not an IRC operator")
			pass
		if "not channel operator" in line2:
			self.gui.irc_error(self,"Permission denied (you're not channel operator)")
			pass
		if "is already on channel" in line2:
			self.gui.irc_error(self,"Invite failed (user is already in channel)")
			pass
		if "not on that channel" in line2:
			self.gui.irc_error(self,"Permission denied (you're not in channel)")
			pass
		if "aren't on that channel" in line2:
			self.gui.irc_error(self,"Permission denied (target user is not in channel)")
			pass
		if "have not registered" in line2:
			self.gui.irc_error(self,"You're not registered")
			pass
		if "may not reregister" in line2:
			self.gui.irc_error(self,"You can't reregister")
			pass
		if "enough parameters" in line2:
			self.gui.irc_error(self,"Error: not enough parameters supplied to command")
			pass
		if "isn't among the privileged" in line2:
			self.gui.irc_error(self,"Registration refused (server isn't setup to allow connections from your host)")
			pass
		if "Password incorrect" in line2:
			self.gui.irc_error(self,"Permission denied (incorrect password)")
			pass
		if "banned from this server" in line2:
			self.gui.irc_error(self,"You are banned from this server")
			pass
		if "kill a server" in line2:
			self.gui.irc_error(self,"Permission denied (you can't kill a server)")
			pass
		if "O-lines for your host" in line2:
			self.gui.irc_error(self,"Error: no O-lines for your host")
			pass
		if "Unknown MODE flag" in line2:
			self.gui.irc_error(self,"Error: unknown MODE flag")
			pass
		if "change mode for other users" in line2:
			self.gui.irc_error(self,"Permission denied (can't change mode for other users)")
			pass
		return irc.IRCClient.lineReceived(self, line)

def config(obj,**kwargs):

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

class IRC_Connection_Factory(protocol.ClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):
		pass

	def clientConnectionFailed(self, connector, reason):
		pass

class IRC_ReConnection_Factory(protocol.ReconnectingClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):
		if self.kwargs["gui"].quitting:
			return

		cid = self.kwargs["server"]+":"+str(self.kwargs["port"])
		if cid in self.kwargs["gui"].disconnected:
			try:
				self.kwargs["gui"].disconnected.remove(cid)
			except:
				pass
			return

		protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		if self.kwargs["gui"].quitting:
			return

		cid = self.kwargs["server"]+":"+str(self.kwargs["port"])
		if cid in self.kwargs["gui"].disconnected:
			try:
				self.kwargs["gui"].disconnected.remove(cid)
			except:
				pass
			return

		protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
