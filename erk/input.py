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

#import erk.events
import emoji
import os

from PyQt5.QtGui import *

from erk.objects import *
from erk.files import *
import erk.config
import erk.macros

COMMON_COMMANDS = {
	"/msg": "/msg ",
	"/part": "/part ",
	"/join": "/join ",
	"/notice": "/notice ",
	"/nick": "/nick ",
	"/mode": "/mode ",
	"/away": "/away ",
	"/back": "/back",
	"/oper": "/oper ",
	"/switch": "/switch ",
	"/connect": "/connect ",
	"/reconnect": "/reconnect ",
	"/ssl": "/ssl ",
	"/ressl": "/ressl ",
	"/send": "/send ",
	"/invite": "/invite ",
}

CHANNEL_COMMANDS = {
	"/me": "/me ",	
	"/part": "/part",
}

PRIVATE_COMMANDS = {
	"/me": "/me ",	
}

def handle_input(window,client,text):
	if len(text.strip())==0: return

	if handle_ui_input(window,client,text): return
	
	if window.type==erk.config.CHANNEL_WINDOW:
		handle_channel_input(window,client,text)
	elif window.type==erk.config.PRIVATE_WINDOW:
		handle_private_input(window,client,text)
	elif window.type==erk.config.SERVER_WINDOW:
		handle_console_input(window,client,text)

def handle_macro_input(window,client,text):

	if client.gui.block_macros: return False

	if not erk.config.MACROS_ENABLED: return False

	tokens = text.split()

	# Macros
	for m in erk.macros.MACROS:
		argc = m["arguments"]
		output = m["output"]
		trigger = m["trigger"]
		mtype = m["type"]
		execute = m["execute"]

		if len(tokens)>0:
			if tokens[0].lower()==trigger and (len(tokens)-1)==argc:
				tokens.pop(0)

				output = output.replace('$$',"_ESCAPED_DOLLAR_SIGN_")

				output = erk.macros.macro_variables(window,client,output)

				for a in tokens:
					output = output.replace('$',a,1)

				output = output.replace('_ESCAPED_DOLLAR_SIGN_',"$")

				if mtype=="privmsg":

					if window.type==erk.config.CHANNEL_WINDOW or window.type==erk.config.PRIVATE_WINDOW:

						if execute:
							if erk.config.USE_EMOJIS: output = emoji.emojize(output,use_aliases=True)

							client.msg(window.name,output)

						else:
							window.input.setText("/msg "+output)
							window.input.moveCursor(QTextCursor.End)
						return True
					else:
						msg = Message(ERROR_MESSAGE,'',"Can't send messages from the console")
						window.writeText(msg,True)
						return True

				elif mtype=="action":

					if window.type==erk.config.CHANNEL_WINDOW or window.type==erk.config.PRIVATE_WINDOW:

						if execute:
							if erk.config.USE_EMOJIS: output = emoji.emojize(output,use_aliases=True)

							client.describe(window.name,output)

						else:
							window.input.setText("/me "+output)
							window.input.moveCursor(QTextCursor.End)
						return True
					else:
						msg = Message(ERROR_MESSAGE,'',"Can't send messages from the console")
						window.writeText(msg,True)
						return True
				elif mtype=="notice":

					if window.type==erk.config.CHANNEL_WINDOW or window.type==erk.config.PRIVATE_WINDOW:

						if execute:
							if erk.config.USE_EMOJIS: output = emoji.emojize(output,use_aliases=True)

							client.notice(window.name,output)

						else:
							window.input.setText("/notice "+output)
							window.input.moveCursor(QTextCursor.End)
						return True
					else:
						msg = Message(ERROR_MESSAGE,'',"Can't send messages from the console")
						window.writeText(msg,True)
						return True
				elif mtype=="command":
					if execute:
						if window.type==erk.config.CHANNEL_WINDOW:
							handle_channel_input(window,client,output)
							return True

						if window.type==erk.config.PRIVATE_WINDOW:
							handle_private_input(window,client,output)
							return True

						handle_console_input(window,client,output)
						return True
					else:
						window.input.setText(output)
						window.input.moveCursor(QTextCursor.End)
						return True

				#return True
			if tokens[0].lower()==trigger:

				passed = (len(tokens)-1)

				if argc==0 or argc==1:
					sarg = "argument"
				else:
					sarg = "arguments"

				if passed>argc:
					# too many arguments
					msg = Message(ERROR_MESSAGE,'',"Too many arguments: \""+trigger+"\" takes "+str(argc)+" "+sarg)
				elif passed<argc:
					# too few argument
					msg = Message(ERROR_MESSAGE,'',"Not enough arguments: \""+trigger+"\" takes "+str(argc)+" "+sarg)

				window.writeText(msg,True)
				return True

def handle_channel_input(window,client,text):

	if not client.gui.block_plugins:
		if client.gui.plugins.input(client,window.name,text): return True

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()=='/invite' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			client.sendLine("INVITE "+target+" "+window.name)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/mode' and len(tokens)>=2:
			if tokens[1][:1]=='#' or tokens[1][:1]=='&' or tokens[1][:1]=='!' or tokens[1][:1]=='+':
				# channel has been passed as an argument
				# Do not handle the command here, let the command get
				# handled in handle_common_input()
				pass
			else:
				tokens.pop(0)
				data = ' '.join(tokens)
				client.sendLine("MODE "+window.name+" "+data)
				return True

	if len(tokens)>0:
		if tokens[0].lower()=='/me' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if erk.config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.describe(window.name,msg)

			return True
		if tokens[0].lower()=='/me':
			msg = Message(ERROR_MESSAGE,'',"Usage: /me [MESSAGE]")
			window.writeText(msg,True)
			return True

	# Handle channel-specific cases of the /part command
	if len(tokens)>0:
		if tokens[0].lower()=='/part' and len(tokens)==1:
			window.leaveChannel(window.name)
			return True
		if tokens[0].lower()=='/part' and len(tokens)>=2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# channel has not been passed as an argument
				tokens.pop(0)
				partmsg = ' '.join(tokens)
				window.leaveChannel(window.name,partmsg)
				return True

	if handle_common_input(window,client,text): return

	if erk.config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)

	client.msg(window.name,text)

def handle_private_input(window,client,text):

	if not client.gui.block_plugins:
		if client.gui.plugins.input(client,window.name,text): return True

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()=='/me' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if erk.config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.describe(window.name,msg)

			return True
		if tokens[0].lower()=='/me':
			msg = Message(ERROR_MESSAGE,'',"Usage: /me [MESSAGE]")
			window.writeText(msg,True)
			return True

	if handle_common_input(window,client,text): return True

	if erk.config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)

	client.msg(window.name,text)

def handle_console_input(window,client,text):

	if not client.gui.block_plugins:
		if client.gui.plugins.input(client,window.name,text): return
	
	if handle_common_input(window,client,text): return

def handle_common_input(window,client,text):

	tokens = text.split()

	if handle_macro_input(window,client,text): return True

	if len(tokens)>0:
		if tokens[0].lower()=='/invite' and len(tokens)==3:
			if tokens[2][:1]=='#' or tokens[2][:1]=='&' or tokens[2][:1]=='!' or tokens[2][:1]=='+':
				# invite channel is a valid name
				tokens.pop(0)
				user = tokens.pop(0)
				channel = tokens.pop(0)
				client.sendLine("INVITE "+user+" "+channel)
				return True
			else:
				msg = Message(ERROR_MESSAGE,'',tokens[2]+" is not a valid channel name")
				window.writeText(msg,True)
				return True

		if tokens[0].lower()=='/invite':
			msg = Message(ERROR_MESSAGE,'',"Usage: /invite USER CHANNEL")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/notice' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)

			if erk.config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.notice(target,msg)
			return True

		if tokens[0].lower()=='/notice':
			msg = Message(ERROR_MESSAGE,'',"Usage: /notice TARGET MESSAGE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/oper' and len(tokens)==3:
			tokens.pop(0)
			username = tokens.pop(0)
			password = tokens.pop(0)
			client.sendLine("OPER "+username+" "+password)
			return True
		if tokens[0].lower()=='/oper':
			msg = Message(ERROR_MESSAGE,'',"Usage: /oper USERNAME PASSWORD")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/back' and len(tokens)==1:
			client.back()
			return True
		if tokens[0].lower()=='/back' and len(tokens)==1:
			msg = Message(ERROR_MESSAGE,'',"Usage: /back")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/away' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			client.away(msg)
			return True
		if tokens[0].lower()=='/away' and len(tokens)==1:
			client.away('busy')
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/mode' and len(tokens)>=3:
			tokens.pop(0)
			data = ' '.join(tokens)
			client.sendLine("MODE "+data)
			return True
		if tokens[0].lower()=='/mode':
			msg = Message(ERROR_MESSAGE,'',"Usage: /mode TARGET MODE [ARGUMENTS]")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/send' and len(tokens)>=2:
			tokens.pop(0)
			data = ' '.join(tokens)
			client.sendLine(data)
			return True
		if tokens[0].lower()=='/send':
			msg = Message(ERROR_MESSAGE,'',"Usage: /send MESSAGE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/whois' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			client.sendLine("WHOIS "+target)
			return True
		if tokens[0].lower()=='/whois':
			msg = Message(ERROR_MESSAGE,'',"Usage: /whois NICKNAME [NICKNAME] ...")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/quit' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			window.parent.disconnect_current(msg)
			return True
		if tokens[0].lower()=='/quit' and len(tokens)==1:
			window.parent.disconnect_current()
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/msg' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)

			if erk.config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.msg(target,msg)
			return True

		if tokens[0].lower()=='/msg':
			msg = Message(ERROR_MESSAGE,'',"Usage: /msg TARGET MESSAGE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/part' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			if not channel in window.channelList():
				msg = Message(ERROR_MESSAGE,'',"You are not in "+channel)
				window.writeText(msg,True)
				return True
			window.leaveChannel(channel)
			return True
		if tokens[0].lower()=='/part' and len(tokens)>=2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# channel has not been passed as an argument
				msg = Message(ERROR_MESSAGE,'',"Usage: /part CHANNEL [MESSAGE]")
				window.writeText(msg,True)
				return True
			tokens.pop(0)
			channel = tokens.pop(0)
			if not channel in window.channelList():
				msg = Message(ERROR_MESSAGE,'',"You are not in "+channel)
				window.writeText(msg,True)
				return True
			partmsg = ' '.join(tokens)
			window.leaveChannel(channel,partmsg)
			return True
		if tokens[0].lower()=='/part':
			msg = Message(ERROR_MESSAGE,'',"Usage: /part CHANNEL [MESSAGE]")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/join' and len(tokens)==3:
			tokens.pop(0)
			channel = tokens.pop(0)
			key = tokens.pop(0)
			client.join(channel,key)
			return True
		if tokens[0].lower()=='/join' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			client.join(channel)
			return True
		if tokens[0].lower()=='/join':
			window.doJoin(client)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/nick' and len(tokens)==2:
			tokens.pop(0)
			newnick = tokens.pop(0)
			client.setNick(newnick)
			return True
		if tokens[0].lower()=='/nick':
			window.doNick(client)
			return True

	return False

def handle_ui_input(window,client,text):

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()=='/script' and len(tokens)==2:
			tokens.pop(0)
			file = tokens.pop(0)
			if os.path.isfile(file):
				s = open(file,"r")
				script = s.read()
				s.close()
				for line in script.split("\n"):
					handle_input(window,client,line)
				return True
			else:
				msg = Message(ERROR_MESSAGE,'',"File \""+file+"\" not found")
				window.writeText(msg,True)
				return True
		if tokens[0].lower()=='/script':
			msg = Message(ERROR_MESSAGE,'',"Usage: /script FILE")
			window.writeText(msg,True)
			return True



	if len(tokens)>0:
		if tokens[0].lower()=='/switch' and len(tokens)==2:
			tokens.pop(0)
			winname = tokens.pop(0)
			channels = window.channelList()
			privates = window.privateList()

			if winname.lower()=="list":
				dl = channels + privates
				msg = Message(SYSTEM_MESSAGE,'',"Available chats: "+', '.join(dl))
				window.writeText(msg,True)
				return True

			if not winname in channels:
				if not winname in privates:
					msg = Message(ERROR_MESSAGE,'',"No chat named \""+winname+"\" found")
					window.writeText(msg,True)
					return True
			if winname in channels:
				swin = window.nameToChannel(winname)
			elif winname in privates:
				swin = window.nameToPrivate(winname)
			else:
				msg = Message(ERROR_MESSAGE,'',"No chat named \""+winname+"\" found")
				window.writeText(msg,True)
				return True
			window.parent.stack.setCurrentWidget(swin)
			return True
		if tokens[0].lower()=='/switch':
			msg = Message(ERROR_MESSAGE,'',"Usage: /switch CHAT_NAME")
			window.writeText(msg,True)
			return True

	if erk.config.DISABLE_CONNECT_COMMANDS: return False

	# /connect SERVER [PORT] [PASSWORD]
	# /reconnect SERVER [PORT] [PASSWORD]
	# /ssl ...
	# /ressl ...
	if len(tokens)>0:

		if tokens[0].lower()=='/connect' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/connect' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/connect' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

			# RECONNECT

		if tokens[0].lower()=='/reconnect' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/reconnect' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/reconnect' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

			#ssl

		if tokens[0].lower()=='/ssl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ssl' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ssl' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

			#ressl

		if tokens[0].lower()=='/ressl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ressl' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ressl' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/connect' or tokens[0].lower()=='/reconnect' or tokens[0].lower()=='/ssl' or tokens[0].lower()=='/ressl':
			window.connectDialog()
			return True

	return False