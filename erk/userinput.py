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
import fnmatch

from PyQt5.QtGui import *

from .objects import *
from .files import *
from . import config
from . import macros

COMMON_COMMANDS = {
	config.INPUT_COMMAND_SYMBOL+"msg": config.INPUT_COMMAND_SYMBOL+"msg ",
	config.INPUT_COMMAND_SYMBOL+"part": config.INPUT_COMMAND_SYMBOL+"part ",
	config.INPUT_COMMAND_SYMBOL+"join": config.INPUT_COMMAND_SYMBOL+"join ",
	config.INPUT_COMMAND_SYMBOL+"notice": config.INPUT_COMMAND_SYMBOL+"notice ",
	config.INPUT_COMMAND_SYMBOL+"nick": config.INPUT_COMMAND_SYMBOL+"nick ",
	config.INPUT_COMMAND_SYMBOL+"mode": config.INPUT_COMMAND_SYMBOL+"mode ",
	config.INPUT_COMMAND_SYMBOL+"away": config.INPUT_COMMAND_SYMBOL+"away ",
	config.INPUT_COMMAND_SYMBOL+"back": config.INPUT_COMMAND_SYMBOL+"back",
	config.INPUT_COMMAND_SYMBOL+"oper": config.INPUT_COMMAND_SYMBOL+"oper ",
	config.INPUT_COMMAND_SYMBOL+"switch": config.INPUT_COMMAND_SYMBOL+"switch ",
	config.INPUT_COMMAND_SYMBOL+"connect": config.INPUT_COMMAND_SYMBOL+"connect ",
	config.INPUT_COMMAND_SYMBOL+"reconnect": config.INPUT_COMMAND_SYMBOL+"reconnect ",
	config.INPUT_COMMAND_SYMBOL+"ssl": config.INPUT_COMMAND_SYMBOL+"ssl ",
	config.INPUT_COMMAND_SYMBOL+"ressl": config.INPUT_COMMAND_SYMBOL+"ressl ",
	config.INPUT_COMMAND_SYMBOL+"send": config.INPUT_COMMAND_SYMBOL+"send ",
	config.INPUT_COMMAND_SYMBOL+"invite": config.INPUT_COMMAND_SYMBOL+"invite ",
	config.INPUT_COMMAND_SYMBOL+"list": config.INPUT_COMMAND_SYMBOL+"list",
	config.INPUT_COMMAND_SYMBOL+"refresh": config.INPUT_COMMAND_SYMBOL+"refresh",
	config.INPUT_COMMAND_SYMBOL+"help": config.INPUT_COMMAND_SYMBOL+"help",
	config.INPUT_COMMAND_SYMBOL+"topic": config.INPUT_COMMAND_SYMBOL+"topic ",
	config.INPUT_COMMAND_SYMBOL+"time": config.INPUT_COMMAND_SYMBOL+"time",
	config.INPUT_COMMAND_SYMBOL+"whois": config.INPUT_COMMAND_SYMBOL+"whois ",
	config.INPUT_COMMAND_SYMBOL+"whowas": config.INPUT_COMMAND_SYMBOL+"whowas ",
	config.INPUT_COMMAND_SYMBOL+"version": config.INPUT_COMMAND_SYMBOL+"version",
	config.INPUT_COMMAND_SYMBOL+"who": config.INPUT_COMMAND_SYMBOL+"who ",
}

CHANNEL_COMMANDS = {
	config.INPUT_COMMAND_SYMBOL+"me": config.INPUT_COMMAND_SYMBOL+"me ",	
	config.INPUT_COMMAND_SYMBOL+"part": config.INPUT_COMMAND_SYMBOL+"part",
}

PRIVATE_COMMANDS = {
	config.INPUT_COMMAND_SYMBOL+"me": config.INPUT_COMMAND_SYMBOL+"me ",	
}

COMMAND_HELP = [
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"msg</b> TARGET MESSAGE", "Sends a private message" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"notice</b> TARGET MESSAGE", "Sends a notice" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"join</b> CHANNEL [KEY]", "Joins a channel" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"part</b> CHANNEL [MESSAGE]", "Leaves a channel" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"invite</b> USER CHANNEL", "Sends a channel invite to a user" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"nick</b> NEW_NICKNAME", "Changes your nickname" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"away</b> [MESSAGE]", "Sets your status to \"away\"" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"back</b>", "Sets your status to \"back\"" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"mode</b> TARGET MODE [ARGUMENTS]", "Sets a channel or user mode" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"oper</b> USERNAME PASSWORD", "Logs into an operator account" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"topic</b> CHANNEL NEW_TOPIC", "Sets a channel topic" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"send</b> MESSAGE", "Sends a raw, unaltered command to the server" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"list</b> [TERMS]", "Fetches a channel list from the server" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"refresh</b>", "Requests a new channel list from the server" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"time</b> [SERVER]", "Requests server time" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"version</b> [SERVER]", "Requests server version" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whowas</b> [NICKNAME] [COUNT] [SERVER]", "Requests past user data" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whois</b> NICKNAME [NICKNAME ...]", "Requests user data" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"who</b> USER", "Requests user data" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"script</b> FILENAME", "Loads a text file and executes its contents as commands" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"switch</b> CHANNEL|USER", "Switches to a different, open chat" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"connect</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"reconnect</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server, reconnecting on disconnect" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"ssl</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server via SSL" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"ressl</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server via SSL, reconnecting on disconnect" ],
]

CHAT_HELP = [
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"msg</b> TARGET MESSAGE", "Sends a private message" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"me</b> MESSAGE", "Sends CTCP action message" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"notice</b> TARGET MESSAGE", "Sends a notice" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"join</b> CHANNEL [KEY]", "Joins a channel" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"part</b> [CHANNEL] [MESSAGE]", "Leaves a channel" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"invite</b> USER [CHANNEL]", "Sends a channel invite to a user" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"nick</b> NEW_NICKNAME", "Changes your nickname" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"away</b> [MESSAGE]", "Sets your status to \"away\"" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"back</b>", "Sets your status to \"back\"" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"mode</b> TARGET MODE [ARGUMENTS]", "Sets a channel or user mode" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"oper</b> USERNAME PASSWORD", "Logs into an operator account" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"send</b> MESSAGE", "Sends a raw, unaltered command to the server" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"list</b> [TERMS]", "Fetches a channel list from the server" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"refresh</b>", "Requests a new channel list from the server" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"topic</b> [CHANNEL] NEW_TOPIC", "Sets a channel topic" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"time</b> [SERVER]", "Requests server time" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"version</b> [SERVER]", "Requests server version" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whowas</b> [NICKNAME] [COUNT] [SERVER]", "Requests past user data" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whois</b> NICKNAME [NICKNAME ...]", "Requests user data" ],
	[ "<b>"+config.INPUT_COMMAND_SYMBOL+"who</b> USER", "Requests user data" ],
]

hentries = []
for e in COMMAND_HELP:
	t = HELP_ENTRY
	t = t.replace("%_USAGE_%",e[0])
	t = t.replace("%_DESCRIPTION_%",e[1])
	hentries.append(t)

HELP_DISPLAY = HELP_HTML_TEMPLATE.replace("%_LIST_%","\n".join(hentries))

hentries = []
for e in CHAT_HELP:
	t = HELP_ENTRY
	t = t.replace("%_USAGE_%",e[0])
	t = t.replace("%_DESCRIPTION_%",e[1])
	hentries.append(t)

CHAT_HELP_DISPLAY = CHAT_HELP_HTML_TEMPLATE.replace("%_LIST_%","\n".join(hentries))

def handle_input(window,client,text):
	if len(text.strip())==0: return

	if handle_ui_input(window,client,text):
		window.input.setFocus()
		return
	
	if window.type==config.CHANNEL_WINDOW:
		handle_channel_input(window,client,text)
		window.input.setFocus()
	elif window.type==config.PRIVATE_WINDOW:
		handle_private_input(window,client,text)
		window.input.setFocus()
	elif window.type==config.SERVER_WINDOW:
		handle_console_input(window,client,text)
		window.input.setFocus()

	window.input.setFocus()

def handle_macro_input(window,client,text):

	if client.gui.block_macros: return False

	if not config.MACROS_ENABLED: return False

	tokens = text.split()

	# Macros
	for m in macros.MACROS:
		argc = m["arguments"]
		output = m["output"]
		trigger = m["trigger"]
		mtype = m["type"]
		execute = m["execute"]

		if len(tokens)>0:
			if tokens[0].lower()==trigger and (len(tokens)-1)==argc:
				tokens.pop(0)

				output = output.replace('$$',"_ESCAPED_DOLLAR_SIGN_")

				output = macros.macro_variables(window,client,output)

				for a in tokens:
					output = output.replace('$',a,1)

				output = output.replace('_ESCAPED_DOLLAR_SIGN_',"$")

				if mtype=="privmsg":

					if window.type==config.CHANNEL_WINDOW or window.type==config.PRIVATE_WINDOW:

						if execute:
							if config.USE_EMOJIS: output = emoji.emojize(output,use_aliases=True)

							client.msg(window.name,output)

						else:
							window.input.setText(config.INPUT_COMMAND_SYMBOL+"msg "+output)
							window.input.moveCursor(QTextCursor.End)
						return True
					else:
						msg = Message(ERROR_MESSAGE,'',"Can't send messages from the console")
						window.writeText(msg,True)
						return True

				elif mtype=="action":

					if window.type==config.CHANNEL_WINDOW or window.type==config.PRIVATE_WINDOW:

						if execute:
							if config.USE_EMOJIS: output = emoji.emojize(output,use_aliases=True)

							client.describe(window.name,output)

						else:
							window.input.setText(config.INPUT_COMMAND_SYMBOL+"me "+output)
							window.input.moveCursor(QTextCursor.End)
						return True
					else:
						msg = Message(ERROR_MESSAGE,'',"Can't send messages from the console")
						window.writeText(msg,True)
						return True
				elif mtype=="notice":

					if window.type==config.CHANNEL_WINDOW or window.type==config.PRIVATE_WINDOW:

						if execute:
							if config.USE_EMOJIS: output = emoji.emojize(output,use_aliases=True)

							client.notice(window.name,output)

						else:
							window.input.setText(config.INPUT_COMMAND_SYMBOL+"notice "+output)
							window.input.moveCursor(QTextCursor.End)
						return True
					else:
						msg = Message(ERROR_MESSAGE,'',"Can't send messages from the console")
						window.writeText(msg,True)
						return True
				elif mtype=="command":
					if execute:
						if window.type==config.CHANNEL_WINDOW:
							handle_channel_input(window,client,output)
							return True

						if window.type==config.PRIVATE_WINDOW:
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
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'topic' and len(tokens)>=2:
			if tokens[1][:1]=='#' or tokens[1][:1]=='&' or tokens[1][:1]=='!' or tokens[1][:1]=='+':
				# channel has been passed as an argument
				# Do not handle the command here, let the command get
				# handled in handle_common_input()
				pass
			else:
				tokens.pop(0)
				data = ' '.join(tokens)
				client.topic(window.name,data)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'help':
			msg = Message(PLUGIN_MESSAGE,'',CHAT_HELP_DISPLAY)
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'invite' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			client.sendLine("INVITE "+target+" "+window.name)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'invite' and len(tokens)==1:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"invite USER [CHANNEL]")
			window.writeText(msg,True)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'invite' and len(tokens)>3:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"invite USER [CHANNEL]")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'mode' and len(tokens)>=2:
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
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'me' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.describe(window.name,msg)

			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'me':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"me [MESSAGE]")
			window.writeText(msg,True)
			return True

	# Handle channel-specific cases of the /part command
	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'part' and len(tokens)==1:
			window.leaveChannel(window.name)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'part' and len(tokens)>=2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# channel has not been passed as an argument
				tokens.pop(0)
				partmsg = ' '.join(tokens)
				window.leaveChannel(window.name,partmsg)
				return True

	if handle_common_input(window,client,text): return

	if config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)

	client.msg(window.name,text)

def handle_private_input(window,client,text):

	if not client.gui.block_plugins:
		if client.gui.plugins.input(client,window.name,text): return True

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'help':
			msg = Message(PLUGIN_MESSAGE,'',CHAT_HELP_DISPLAY)
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'me' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.describe(window.name,msg)

			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'me':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"me MESSAGE")
			window.writeText(msg,True)
			return True

	if handle_common_input(window,client,text): return True

	if config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)

	client.msg(window.name,text)

def handle_console_input(window,client,text):

	if not client.gui.block_plugins:
		if client.gui.plugins.input(client,window.name,text): return
	
	if handle_common_input(window,client,text): return

def handle_common_input(window,client,text):

	tokens = text.split()

	if handle_macro_input(window,client,text): return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'who' and len(tokens)==2:
			tokens.pop(0)
			nick = tokens.pop(0)
			client.sendLine("WHO "+nick)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'who':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"who USER")
			window.writeText(msg,True)
			return True


	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'version' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			client.sendLine("VERSION "+server)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'version' and len(tokens)==1:
			client.sendLine("VERSION")
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'version' and len(tokens)>2:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"version [SERVER]")
			window.writeText(msg,True)
			return True



	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'whowas' and len(tokens)==4:
			tokens.pop(0)
			nick = tokens.pop(0)
			count = tokens.pop(0)
			server = tokens.pop(0)
			client.sendLine("WHOWAS "+nick+" "+count+" "+server)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'whowas' and len(tokens)==3:
			tokens.pop(0)
			nick = tokens.pop(0)
			count = tokens.pop(0)
			client.sendLine("WHOWAS "+nick+" "+count)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'whowas' and len(tokens)==2:
			tokens.pop(0)
			nick = tokens.pop(0)
			client.sendLine("WHOWAS "+nick)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'whowas':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"whowas [NICKNAME] [COUNT] [SERVER]")
			window.writeText(msg,True)
			return True


	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'time' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			client.sendLine("TIME "+server)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'time' and len(tokens)==1:
			client.sendLine("TIME")
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'time' and len(tokens)>2:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"time [SERVER]")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'topic' and len(tokens)>=2:
			if tokens[1][:1]=='#' or tokens[1][:1]=='&' or tokens[1][:1]=='!' or tokens[1][:1]=='+':
				tokens.pop(0)
				target = tokens.pop(0)
				data = ' '.join(tokens)
				client.topic(target,data)
				return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'topic':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if len(tokens)==1 and tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'refresh':
			client.sendLine("LIST")
			msg = Message(SYSTEM_MESSAGE,'',"Sent channel list request to the server")
			window.writeText(msg,True)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'refresh':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"refresh")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if len(tokens)==1 and tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'list':
			if len(client.channels)==0:
				client.list_requested = True
				client.list_window = window
				client.sendLine("LIST")
				return True
			else:
				msg = Message(HORIZONTAL_RULE_MESSAGE,'','')
				window.writeText(msg,True)
				for e in client.channellist:
					if len(e.topic.strip())>0:
						msg = Message(PLUGIN_MESSAGE,'',"<a href=\""+e.name+"\">"+e.name+"</a> ("+str(e.count)+" users) - "+e.topic)
					else:
						msg = Message(PLUGIN_MESSAGE,'',"<a href=\""+e.name+"\">"+e.name+"</a> ("+str(e.count)+" users)")
					window.writeText(msg,True)
				# msg = Message(HORIZONTAL_RULE_MESSAGE,'','')
				# window.writeText(msg,True)
				return True

		if len(tokens)>=2 and tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'list':
			tokens.pop(0)	# remove command
			terms = ' '.join(tokens)
			if len(client.channels)==0:
				client.list_requested = True
				client.list_window = window
				client.list_search = terms
				client.sendLine("LIST")
				return True
			else:
				msg = Message(HORIZONTAL_RULE_MESSAGE,'','')
				window.writeText(msg,True)
				msg = Message(PLUGIN_MESSAGE,'',"Channels with <b><i>"+terms+"</i></b> in the name or topic")
				window.writeText(msg,True)
				for e in client.channellist:

					found = False
					if fnmatch.fnmatch(e.name,terms): found = True
					if fnmatch.fnmatch(e.topic,terms): found = True
					if not found: continue


					if len(e.topic.strip())>0:
						msg = Message(PLUGIN_MESSAGE,'',"<a href=\""+e.name+"\">"+e.name+"</a> ("+str(e.count)+" users) - "+e.topic)
					else:
						msg = Message(PLUGIN_MESSAGE,'',"<a href=\""+e.name+"\">"+e.name+"</a> ("+str(e.count)+" users)")
					window.writeText(msg,True)
				# msg = Message(HORIZONTAL_RULE_MESSAGE,'','')
				# window.writeText(msg,True)
				return True



	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'help':
			msg = Message(PLUGIN_MESSAGE,'',HELP_DISPLAY)
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'invite' and len(tokens)==3:
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

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'invite':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"invite USER CHANNEL")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'notice' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)

			if config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.notice(target,msg)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'notice':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"notice TARGET MESSAGE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'oper' and len(tokens)==3:
			tokens.pop(0)
			username = tokens.pop(0)
			password = tokens.pop(0)
			client.sendLine("OPER "+username+" "+password)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'oper':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"oper USERNAME PASSWORD")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'back' and len(tokens)==1:
			client.back()
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'back' and len(tokens)==1:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"back")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'away' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			client.away(msg)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'away' and len(tokens)==1:
			client.away('busy')
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'mode' and len(tokens)>=3:
			tokens.pop(0)
			data = ' '.join(tokens)
			client.sendLine("MODE "+data)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'mode':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"mode TARGET MODE [ARGUMENTS]")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'send' and len(tokens)>=2:
			tokens.pop(0)
			data = ' '.join(tokens)
			client.sendLine(data)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'send':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"send MESSAGE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'whois' and len(tokens)>=2:
			tokens.pop(0)
			target = " ".join(tokens)
			client.sendLine("WHOIS "+target)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'whois':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"whois NICKNAME [NICKNAME] ...")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'quit' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			window.parent.disconnect_current(msg)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'quit' and len(tokens)==1:
			window.parent.disconnect_current()
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'msg' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)

			if config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)

			client.msg(target,msg)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'msg':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"msg TARGET MESSAGE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'part' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			if not channel in window.channelList():
				msg = Message(ERROR_MESSAGE,'',"You are not in "+channel)
				window.writeText(msg,True)
				return True
			window.leaveChannel(channel)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'part' and len(tokens)>=2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# channel has not been passed as an argument
				msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]")
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
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'part':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'join' and len(tokens)==3:
			tokens.pop(0)
			channel = tokens.pop(0)
			key = tokens.pop(0)
			client.join(channel,key)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'join' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			client.join(channel)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'join':
			window.doJoin(client)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'nick' and len(tokens)==2:
			tokens.pop(0)
			newnick = tokens.pop(0)
			client.setNick(newnick)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'nick':
			window.doNick(client)
			return True

	return False

def handle_ui_input(window,client,text):

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'script' and len(tokens)==2:
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
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'script':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"script FILE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'switch' and len(tokens)==2:
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
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'switch':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"switch CHAT_NAME")
			window.writeText(msg,True)
			return True

	if config.DISABLE_CONNECT_COMMANDS: return False

	# /connect SERVER [PORT] [PASSWORD]
	# /reconnect SERVER [PORT] [PASSWORD]
	# /ssl ...
	# /ressl ...
	if len(tokens)>0:

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connect' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connect' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connect' and len(tokens)==4:
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

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False)
			window.doConnect(info)
			return True

			# RECONNECT

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'reconnect' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'reconnect' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'reconnect' and len(tokens)==4:
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

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

			#ssl

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ssl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ssl' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ssl' and len(tokens)==4:
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

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False)
			window.doConnect(info)
			return True

			#ressl

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ressl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ressl' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg,True)
				return True

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ressl' and len(tokens)==4:
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

			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connect' or tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'reconnect' or tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ssl' or tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ressl':
			window.connectDialog()
			return True

	return False