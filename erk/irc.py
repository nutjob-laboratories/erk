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

from erk.common import *

from twisted.internet import reactor, protocol

try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

from twisted.words.protocols import irc


def connect(host,port,nick,username=None,ircname=None,gui=None,password=None):
	bot = IRC_Connection_Factory(nick,username,ircname,gui,password,host,port)
	reactor.connectTCP(host,port,bot)

def connectSSL(host,port,nick,username=None,ircname=None,gui=None,password=None):
	bot = IRC_Connection_Factory(nick,username,ircname,gui,password,host,port)
	reactor.connectSSL(host,port,bot,ssl.ClientContextFactory())

def reconnect(host,port,nick,username=None,ircname=None,gui=None,password=None):
	bot = IRC_ReConnection_Factory(nick,username,ircname,gui,password,host,port)
	reactor.connectTCP(host,port,bot)

def reconnectSSL(host,port,nick,username=None,ircname=None,gui=None,password=None):
	bot = IRC_ReConnection_Factory(nick,username,ircname,gui,password,host,port)
	reactor.connectSSL(host,port,bot,ssl.ClientContextFactory())

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

	def irc_RPL_BANLIST(self,prefix,params):
		channel = params[1]
		ban = params[2]
		banner = params[3]

		if channel in self.banlist:
			entry = [ban,banner]
			self.banlist[channel].append(entry)
		else:
			self.banlist[channel] = []
			entry = [ban,banner]
			self.banlist[channel].append(entry)

	def irc_RPL_ENDOFBANLIST(self,prefix,params):
		channel = params[1]

		if not channel in self.banlist:
			self.gui.gotBanlist(self.id,channel,[])
			return

		banlist = self.banlist[channel]
		del self.banlist[channel]

		self.gui.gotBanlist(self.id,channel,banlist)

	def isupport(self,options):
		self.options = options

		self.gui.serveroptions(self.id,self.options)

	def __init__(self,nickname,username,realname,gui,password,host,port):
		self.nickname = nickname
		self.username = username
		self.realname = realname
		if password != None:
			self.password = password
		self.gui = gui
		self.host = host
		self.port = port
		self.ircnetwork = ""

		self.oldnick = nickname

		#self.id = generateID()

		nid = generateID()
		while nid in self.gui.connections:
			nid = generateID()

		self.id = nid

		self.users = {}

		self.whois_data = {}

		self.whowas = {}

		self.channelList = []

		self.options = []

		self.banlist = {}

		self.alive = True

		self.maxnicklen = 0
		self.maxchannels = 0
		self.channellen = 0
		self.topiclen = 0
		self.kicklen = 0
		self.awaylen = 0
		self.maxtargets = 0
		self.network = ""
		self.casemapping = ""
		self.cmds = []
		self.prefix = []
		self.chanmodes = []
		self.supports = []
		self.modes = 0
		self.maxmodes = []

		self.serverChannelList = {}

	def connectionMade(self):

		# PROTOCTL UHNAMES
		self.sendLine("PROTOCTL UHNAMES")

		self.gui.connect(self.id,self)

		irc.IRCClient.connectionMade(self)

	def connectionLost(self, reason):

		self.gui.disconnect(self.id,reason)

		irc.IRCClient.connectionLost(self, reason)

	def signedOn(self):
		
		self.gui.registered(self.id)

	def joined(self, channel):
		self.sendLine(f"MODE {channel}")
		self.sendLine(f"MODE {channel} +b")

		self.gui.joined(self.id,channel)

	def privmsg(self, user, target, msg):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]

		tokens = msg.split(' ')

		if target==self.nickname:
			self.gui.privateMessage(self.id,user,msg)
		else:
			self.gui.publicMessage(self.id,target,user,msg)


	def noticed(self, user, channel, message):
		tok = user.split('!')
		if len(tok) >= 2:
			pnick = tok[0]
			phostmask = tok[1]
		else:
			pnick = user
			phostmask = user

		self.gui.noticeMessage(self.id,channel,user,message)
		

	def receivedMOTD(self, motd):
		self.gui.motd(self.id,motd)

	def modeChanged(self, user, channel, mset, modes, args):
		if "b" in modes: self.sendLine(f"MODE {channel} +b")
		self.gui.mode(self.id,user,channel,mset,modes,args)
		
	def nickChanged(self,nick):
		self.gui.renamed(self.id,nick,self.oldnick,"You are")
		self.oldnick = nick
		self.nickname = nick

	def userJoined(self, user, channel):
		if user.split('!')[0] == self.nickname:
			return

		self.gui.userJoined(self.id,user,channel)

	def userLeft(self, user, channel):

		self.gui.userParted(self.id,user,channel)

	def irc_ERR_NICKNAMEINUSE(self, prefix, params):
		oldnick = self.nickname
		if oldnick != self.gui.alternate:
			newnick = self.gui.alternate
		else:
			newnick = self.nickname + "_"
		d = systemTextDisplay(f"Nickname \"{oldnick}\" in use, changing nick to \"{newnick}\"",self.gui.maxnicklen,SYSTEM_COLOR)
		self.setNick(newnick)
		self.gui.writeToLog(d)
		self.gui.nickname = newnick

		self.oldnick = oldnick

	def userRenamed(self, oldname, newname):

		self.gui.renamed(self.id,newname,oldname,f"{oldname} is")
					
	def topicUpdated(self, user, channel, newTopic):
		
		self.gui.topic(self.id,user,channel,newTopic)

	def action(self, user, channel, data):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]
		
		self.gui.actionMessage(self.id,channel,user,data)

	def userKicked(self, kickee, channel, kicker, message):

		self.gui.userKicked(self.id,kickee,channel,kicker,message)

	def kickedFrom(self, channel, kicker, message):
		self.gui.gotKicked(self.id,channel,kicker,message)

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

		self.gui.ircQuit(self.id,prefix,msg)

	def irc_RPL_NAMREPLY(self, prefix, params):
		channel = params[2].lower()
		nicklist = params[3].split(' ')

		if channel in self.users:
			for n in nicklist:
				if len(n)==0: continue
				if n.isspace(): continue
				self.users[channel].append(n)
		else:
			self.users[channel] = []
			for n in nicklist:
				if len(n)==0: continue
				if n.isspace(): continue
				self.users[channel].append(n)

	def irc_RPL_ENDOFNAMES(self, prefix, params):

		channel = params[1].lower()

		users = self.users[channel]
		del self.users[channel]

		ops = []
		voiced = []
		norm = []

		for u in users:
			if u[0]=='@':
				ops.append(u)
				continue
			if u[0]=='+':
				voiced.append(u)
				continue
			norm.append(u)

		users = ops + voiced + norm

		# user contains a channel user list
		self.gui.channelNames(self.id,channel,users)


	def irc_RPL_TOPIC(self, prefix, params):
		# global TOPIC
		if not params[2].isspace():
			TOPIC = params[2]
		else:
			TOPIC = ""

		channel = params[1]

		self.gui.topic(self.id,self.hostname,channel,TOPIC)

	def irc_RPL_WHOISCHANNELS(self, prefix, params):
		params.pop(0)
		nick = params.pop(0)
		channels = ", ".join(params)

		if nick in self.whois_data:
			self.whois_data[nick].name = nick
			self.whois_data[nick].channels = params
		else:
			self.whois_data[nick] = Whois()
			self.whois_data[nick].name = nick
			self.whois_data[nick].channels = params

	def irc_RPL_WHOISUSER(self, prefix, params):
		nick = params[1]
		username = params[2]
		host = params[3]
		realname = params[5]

		if nick in self.whois_data:
			self.whois_data[nick].name = nick
			self.whois_data[nick].username = username
			self.whois_data[nick].host = host
			self.whois_data[nick].realname = realname
		else:
			self.whois_data[nick] = Whois()
			self.whois_data[nick].name = nick
			self.whois_data[nick].username = username
			self.whois_data[nick].host = host
			self.whois_data[nick].realname = realname

	def irc_RPL_WHOISIDLE(self, prefix, params):
		params.pop(0)
		nick = params.pop(0)
		idle_time = params.pop(0)
		signed_on = params.pop(0)

		if nick in self.whois_data:
			self.whois_data[nick].name = nick
			self.whois_data[nick].idle = idle_time
			self.whois_data[nick].signedon = signed_on
		else:
			self.whois_data[nick] = Whois()
			self.whois_data[nick].name = nick
			self.whois_data[nick].idle = idle_time
			self.whois_data[nick].signedon = signed_on

	def irc_RPL_WHOISSERVER(self, prefix, params):
		nick = params[1]
		server = params[2]

		if nick in self.whois_data:
			self.whois_data[nick].name = nick
			self.whois_data[nick].server = server
		else:
			self.whois_data[nick] = Whois()
			self.whois_data[nick].name = nick
			self.whois_data[nick].server = server

	def irc_RPL_ENDOFWHOIS(self, prefix, params):
		nick = params[1]

		if nick in self.whois_data:
			# self.whois_data[nick] contains whois data
			self.gui.whois(self.id,self.whois_data[nick])
			del self.whois_data[nick]

	def irc_RPL_WHOWASUSER(self, prefix, params):
		nick = params[1]
		username = params[2]
		host = params[3]
		realname = params[5]

		w = Whowas()
		w.name = nick
		w.username = username
		w.host = host
		w.realname = realname

		self.whowas[nick] = w


	def irc_RPL_ENDOFWHOWAS(self, prefix, params):
		nick = params[1]

		if nick in self.whowas:
			self.gui.whowas(self.id,self.whowas[nick])
			del self.whowas[nick]

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
					self.gui.mode(self.id,self.hostname,channel,True,m,())
				else:
					m = m[1:]
					# mode removed
					self.gui.mode(self.id,self.hostname,channel,False,m,())

	def irc_RPL_YOUREOPER(self, prefix, params):
		self.gui.serverAllMessage(self.id,f"You have been granted operator status on {self.hostname}.")

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

		self.gui.invite(self.id,prefix,channel)


	def irc_RPL_INVITING(self,prefix,params):
		user = params[1]
		channel = params[2]

		self.gui.serverMessage(self.id,channel,f"Channel invitation to {user} sent.")

	def irc_RPL_LIST(self,prefix,params):

		server = prefix
		channel = params[1]
		usercount = params[2]
		topic = params[3]

		self.gui.channelListEntry(self.id,channel,usercount,topic)

	def irc_RPL_LISTSTART(self,prefix,params):
		server = prefix

		self.gui.channelListStart(self.id)

	def irc_RPL_LISTEND(self,prefix,params):
		server = prefix

		self.gui.channelListEnd(self.id)

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

		self.gui.irc_raw(self.id,line2)

		d = line2.split(" ")
		if len(d) >= 2:
			if d[1].isalpha(): return irc.IRCClient.lineReceived(self, line)

		if "Cannot join channel (+k)" in line2:
			self.gui.ircerror(self.id,f"Cannot join channel (wrong or missing password)")
			pass
		if "Cannot join channel (+l)" in line2:
			self.gui.ircerror(self.id,f"Cannot join channel (channel is full)")
			pass
		if "Cannot join channel (+b)" in line2:
			self.gui.ircerror(self.id,f"Cannot join channel (banned)")
			pass
		if "Cannot join channel (+i)" in line2:
			self.gui.ircerror(self.id,f"Cannot join channel (channel is invite only)")
			pass
		if "not an IRC operator" in line2:
			self.gui.ircerror(self.id,"Permission denied (you're not an IRC operator")
			pass
		if "not channel operator" in line2:
			self.gui.ircerror(self.id,"Permission denied (you're not channel operator)")
			pass
		if "is already on channel" in line2:
			self.gui.ircerror(self.id,"Invite failed (user is already in channel)")
			pass
		if "not on that channel" in line2:
			self.gui.ircerror(self.id,"Permission denied (you're not in channel)")
			pass
		if "aren't on that channel" in line2:
			self.gui.ircerror(self.id,"Permission denied (target user is not in channel)")
			pass
		if "have not registered" in line2:
			self.gui.ircerror(self.id,"You're not registered")
			pass
		if "may not reregister" in line2:
			self.gui.ircerror(self.id,"You can't reregister")
			pass
		if "enough parameters" in line2:
			self.gui.ircerror(self.id,"Error: not enough parameters supplied to command")
			pass
		if "isn't among the privileged" in line2:
			self.gui.ircerror(self.id,"Registration refused (server isn't setup to allow connections from your host)")
			pass
		if "Password incorrect" in line2:
			self.gui.ircerror(self.id,"Permission denied (incorrect password)")
			pass
		if "banned from this server" in line2:
			self.gui.ircerror(self.id,"You are banned from this server")
			pass
		if "kill a server" in line2:
			self.gui.ircerror(self.id,"Permission denied (you can't kill a server)")
			pass
		if "O-lines for your host" in line2:
			self.gui.ircerror(self.id,"Error: no O-lines for your host")
			pass
		if "Unknown MODE flag" in line2:
			self.gui.ircerror(self.id,"Error: unknown MODE flag")
			pass
		if "change mode for other users" in line2:
			self.gui.ircerror(self.id,"Permission denied (can't change mode for other users)")
			pass
		return irc.IRCClient.lineReceived(self, line)

class IRC_Connection_Factory(protocol.ClientFactory):
	def __init__(self,nickname,username,realname,gui,password,host,port):
		self.nickname = nickname
		self.username = username
		self.realname = realname
		self.gui = gui
		self.password = password
		self.host = host
		self.port = port

	def buildProtocol(self, addr):
		bot = IRC_Connection(self.nickname,self.username,self.realname,self.gui,self.password,self.host,self.port)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):
		pass

	def clientConnectionFailed(self, connector, reason):
		pass

class IRC_ReConnection_Factory(protocol.ReconnectingClientFactory):
	def __init__(self,nickname,username,realname,gui,password,host,port):
		self.nickname = nickname
		self.username = username
		self.realname = realname
		self.gui = gui
		self.password = password
		self.host = host
		self.port = port

	def buildProtocol(self, addr):
		bot = IRC_Connection(self.nickname,self.username,self.realname,self.gui,self.password,self.host,self.port)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):
		if self.gui.disconnected_on_purpose:
			self.gui.disconnected_on_purpose = False
			return
		protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		# if self.gui.disconnected_on_purpose:
		# 	self.gui.disconnected_on_purpose = False
		# 	return
		protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
