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

import emoji
import os
import fnmatch
import string
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from .objects import *
from .files import *
from . import config
from .irc import ScriptThreadWindow,SearchListThread,found_in_list,begin_list,end_list
from . import events
from . import plugins

from .dialogs import ScriptEditor

COMMON_COMMANDS = {}
CHANNEL_COMMANDS = {}
PRIVATE_COMMANDS = {}
COMMAND_HELP = []
CHAT_HELP = []
COMMAND_HELP_ENTRIES = []
CHAT_HELP_ENTRIES = []

CMDLINE_BLOCK_SCRIPTS = False
CMDLINE_BLOCK_EDITOR = False
CMDLINE_BLOCK_STYLES = False

LIST_THREAD = None

def buildHelp():

	global COMMON_COMMANDS
	global CHANNEL_COMMANDS
	global PRIVATE_COMMANDS
	global COMMAND_HELP
	global CHAT_HELP
	global COMMAND_HELP_ENTRIES
	global CHAT_HELP_ENTRIES

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
		config.INPUT_COMMAND_SYMBOL+"ignore": config.INPUT_COMMAND_SYMBOL+"ignore ",
		config.INPUT_COMMAND_SYMBOL+"unignore": config.INPUT_COMMAND_SYMBOL+"unignore ",
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
		config.INPUT_COMMAND_SYMBOL+"exit": config.INPUT_COMMAND_SYMBOL+"exit",
		config.INPUT_COMMAND_SYMBOL+"quit": config.INPUT_COMMAND_SYMBOL+"quit",
		config.INPUT_COMMAND_SYMBOL+"settings": config.INPUT_COMMAND_SYMBOL+"settings",
		config.INPUT_COMMAND_SYMBOL+"preferences": config.INPUT_COMMAND_SYMBOL+"preferences",
		config.INPUT_COMMAND_SYMBOL+"print": config.INPUT_COMMAND_SYMBOL+"print ",
		config.INPUT_COMMAND_SYMBOL+"echo": config.INPUT_COMMAND_SYMBOL+"echo ",

		config.INPUT_COMMAND_SYMBOL+"script": config.INPUT_COMMAND_SYMBOL+"script ",

		config.INPUT_COMMAND_SYMBOL+"style": config.INPUT_COMMAND_SYMBOL+"style ",

		config.INPUT_COMMAND_SYMBOL+"connectscript": config.INPUT_COMMAND_SYMBOL+"connectscript ",

		config.INPUT_COMMAND_SYMBOL+"edit": config.INPUT_COMMAND_SYMBOL+"edit ",

		config.INPUT_COMMAND_SYMBOL+"macro": config.INPUT_COMMAND_SYMBOL+"macro ",
		config.INPUT_COMMAND_SYMBOL+"macrohelp": config.INPUT_COMMAND_SYMBOL+"macrohelp ",
		config.INPUT_COMMAND_SYMBOL+"macrousage": config.INPUT_COMMAND_SYMBOL+"macrousage ",
		config.INPUT_COMMAND_SYMBOL+"unmacro": config.INPUT_COMMAND_SYMBOL+"unmacro ",

		config.INPUT_COMMAND_SYMBOL+"dictionary": config.INPUT_COMMAND_SYMBOL+"dictionary ",
		config.INPUT_COMMAND_SYMBOL+"undictionary": config.INPUT_COMMAND_SYMBOL+"undictionary ",
		config.INPUT_COMMAND_SYMBOL+"write": config.INPUT_COMMAND_SYMBOL+"write ",
		config.INPUT_COMMAND_SYMBOL+"cat": config.INPUT_COMMAND_SYMBOL+"cat ",
	}

	display_edit = True
	if not config.ENABLE_SCRIPTS: display_edit = False
	if not config.ENABLE_SCRIPT_EDITOR: display_edit = False
	if CMDLINE_BLOCK_EDITOR: display_edit = False
	if CMDLINE_BLOCK_SCRIPTS: display_edit = False

	if not display_edit:
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"edit"]

	display_script = True
	if not config.ENABLE_SCRIPTS: display_script = False
	if CMDLINE_BLOCK_SCRIPTS: display_script = False

	if not display_script:
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"script"]
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"connectscript"]

	display_macro = True
	if not config.ENABLE_SCRIPTS: display_macro = False
	if CMDLINE_BLOCK_SCRIPTS: display_macro = False
	if not config.ENABLE_MACROS: display_macro = False

	if not display_macro:
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"macro"]
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"macrohelp"]
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"macrousage"]
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"unmacro"]

	display_style = True
	if CMDLINE_BLOCK_STYLES: display_style = False

	if not display_style:
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"style"]

	display_ignore = True
	if not config.ENABLE_IGNORE: display_ignore = False

	if not display_ignore:
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"ignore"]
		del COMMON_COMMANDS[config.INPUT_COMMAND_SYMBOL+"unignore"]

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
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"ignore</b> TARGET", "Ignore messages from certain users" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"unignore</b> TARGET", "Remove users from the ignore list" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"list</b> [TERMS]", "Fetches a channel list from the server" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"refresh</b>", "Requests a new channel list from the server" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"time</b> [SERVER]", "Requests server time" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"version</b> [SERVER]", "Requests server version" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whowas</b> [NICKNAME] [COUNT] [SERVER]", "Requests past user data" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whois</b> NICKNAME [NICKNAME ...]", "Requests user data" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"who</b> USER", "Requests user data" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"script</b> FILENAME", "Loads a script and executes its contents as commands" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"edit</b> [FILENAME]", "Loads the script editor or uses it to edit a script" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"connectscript</b> SERVER [PORT]", "Loads and executes SERVER:PORT's connection script" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"macro</b> COMMAND ARG_COUNT MESSAGE...", "Creates a macro" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"macrohelp</b> NAME MESSAGE...", "Sets the \"help\" text for a macro" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"macrousage</b> NAME MESSAGE...", "Sets the \"usage\" text for a macro" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"unmacro</b> NAME", "Deletes a macro" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"switch</b> [CHANNEL|USER]", "Switches to a different, open chat (use without argument to list all chats)" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"style</b> FILENAME", "Loads a style file into the current chat" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"print</b> MESSAGE", "Prints a message to the current window" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"write</b> MESSAGE", "Prints a message to the current window, and saves it in the log" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"cat</b> [TARGET] FILENAME", "Opens a file and sends its contents as messages" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"dictionary</b> [WORD] ...", "View or add a word to the spellcheck dictionary" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"undictionary</b> WORD [WORD...]", "Remove a word from the spellcheck dictionary" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"connect</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"reconnect</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server, reconnecting on disconnect" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"ssl</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server via SSL" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"preferences</b>", "Opens the preferences dialog" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"ressl</b> [SERVER] [PORT] [PASSWORD]", "Connects to an IRC server via SSL, reconnecting on disconnect" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"quit</b> [MESSAGE]", "Disconnects from the current IRC server" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"exit</b>", "Closes the application" ],
	]

	if not display_edit:
		clean = []
		for h in COMMAND_HELP:
			if config.INPUT_COMMAND_SYMBOL+"edit" in h[0]: continue
			clean.append(h)
		COMMAND_HELP = clean

	if not display_script:
		clean = []
		for h in COMMAND_HELP:
			if config.INPUT_COMMAND_SYMBOL+"script" in h[0]: continue
			if config.INPUT_COMMAND_SYMBOL+"connectscript" in h[0]: continue
			clean.append(h)
		COMMAND_HELP = clean

	if not display_macro:
		clean = []
		for h in COMMAND_HELP:
			if config.INPUT_COMMAND_SYMBOL+"macro" in h[0]: continue
			if config.INPUT_COMMAND_SYMBOL+"macrohelp" in h[0]: continue
			if config.INPUT_COMMAND_SYMBOL+"macrousage" in h[0]: continue
			if config.INPUT_COMMAND_SYMBOL+"unmacro" in h[0]: continue
			clean.append(h)
		COMMAND_HELP = clean

	if not display_style:
		clean = []
		for h in COMMAND_HELP:
			if config.INPUT_COMMAND_SYMBOL+"style" in h[0]: continue
			clean.append(h)
		COMMAND_HELP = clean

	if not display_ignore:
		clean = []
		for h in COMMAND_HELP:
			if config.INPUT_COMMAND_SYMBOL+"ignore" in h[0]: continue
			if config.INPUT_COMMAND_SYMBOL+"unignore" in h[0]: continue
			clean.append(h)
		COMMAND_HELP = clean

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
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"ignore</b> TARGET", "Ignore messages from certain users" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"unignore</b> TARGET", "Remove users from the ignore list" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"list</b> [TERMS]", "Fetches a channel list from the server" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"refresh</b>", "Requests a new channel list from the server" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"topic</b> [CHANNEL] NEW_TOPIC", "Sets a channel topic" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"time</b> [SERVER]", "Requests server time" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"version</b> [SERVER]", "Requests server version" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whowas</b> [NICKNAME] [COUNT] [SERVER]", "Requests past user data" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"whois</b> NICKNAME [NICKNAME ...]", "Requests user data" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"who</b> USER", "Requests user data" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"script</b> FILENAME", "Loads a script and executes its contents as commands" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"edit</b> [FILENAME]", "Loads the script editor or uses it to edit a script" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"switch</b> [CHANNEL|USER]", "Switches to a different, open chat (use without argument to list all chats)" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"style</b> FILENAME", "Loads a style file into the current chat" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"preferences</b>", "Opens the preferences dialog" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"quit</b> [MESSAGE]", "Disconnects from the current IRC server" ],
		[ "<b>"+config.INPUT_COMMAND_SYMBOL+"exit</b>", "Closes the application" ],
	]

	if not display_edit:
		 clean = []
		 for h in CHAT_HELP:
		 	if config.INPUT_COMMAND_SYMBOL+"edit" in h[0]: continue
		 	clean.append(h)
		 CHAT_HELP = clean

	if not display_script:
		clean = []
		for h in CHAT_HELP:
			if config.INPUT_COMMAND_SYMBOL+"script" in h[0]: continue
			if config.INPUT_COMMAND_SYMBOL+"connectscript" in h[0]: continue
			clean.append(h)
		CHAT_HELP = clean

	if not display_style:
		clean = []
		for h in CHAT_HELP:
			if config.INPUT_COMMAND_SYMBOL+"style" in h[0]: continue
			clean.append(h)
		CHAT_HELP = clean

	if not display_ignore:
		clean = []
		for h in CHAT_HELP:
			if config.INPUT_COMMAND_SYMBOL+"ignore" in h[0]: continue
			if config.INPUT_COMMAND_SYMBOL+"unignore" in h[0]: continue
			clean.append(h)
		CHAT_HELP = clean

	COMMAND_HELP_ENTRIES = []
	for e in COMMAND_HELP:
		t = HELP_ENTRY
		t = t.replace("%_USAGE_%",e[0])
		t = t.replace("%_DESCRIPTION_%",e[1])
		COMMAND_HELP_ENTRIES.append(t)

	CHAT_HELP_ENTRIES = []
	for e in CHAT_HELP:
		t = HELP_ENTRY
		t = t.replace("%_USAGE_%",e[0])
		t = t.replace("%_DESCRIPTION_%",e[1])
		CHAT_HELP_ENTRIES.append(t)

buildHelp()

SCRIPT_THREADS = []

VARIABLE_TABLE = {}

MACROS = []

PROTECTED_NAMES = [
		'away',
		'back',
		'invite',
		'join',
		'list',
		'me',
		'msg',
		'nick',
		'notice',
		'oper',
		'part',
		'quit',
		'send',
		'time',
		'topic',
		'version',
		'who',
		'whois',
		'whowas',
		'alias',
		'argcount',
		'connect',
		'connectscript',
		'exit',
		'help',
		'print',
		'reconnect',
		'refresh',
		'ressl',
		'script',
		'settings',
		'ssl',
		'style',
		'switch',
		'wait',
		'_alias',
		'macro',
		'macrohelp',
		'unmacro',
		'edit',
		'msgbox',
		'macrousage',
		'unalias',
		'cat',
		'write',
		'dictionary',
		'undictionary',
		'ignore',
		'unignore'
	]

FORBIDDEN_CHARACTERS = [
	config.INPUT_COMMAND_SYMBOL,
	config.SCRIPT_INTERPOLATE_SYMBOL,
	config.MACRO_INTERPOLATE_SYMBOL,
]

def handle_macros(window,client,text):

	tokens = text.split()

	for m in MACROS:
		macro_name = m.name
		macro_argcount = m.argcount
		macro_data = m.command
		macro_args = m.args

		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+macro_name:
				tokens.pop(0)

				if macro_argcount<0:
					counter = 0
					for a in tokens:
						counter = counter + 1
						macro_data = macro_data.replace(config.MACRO_INTERPOLATE_SYMBOL+str(counter),a)
					macro_data = macro_data.replace(config.MACRO_INTERPOLATE_SYMBOL+"+",' '.join(tokens))
					if len(tokens)>1:
						rest = tokens[1:]
						macro_data = macro_data.replace(config.MACRO_INTERPOLATE_SYMBOL+"-",' '.join(rest))

					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"NICK",client.nickname)
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"USERNAME",client.username)
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"REALNAME",client.realname)
					if client.hostname:
						macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"HOSTNAME",client.hostname)
					else:
						macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"HOSTNAME",client.server+":"+str(client.port))
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"SERVER",client.server)
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"PORT",str(client.port))

					if window.name==SERVER_CONSOLE_NAME:
						if client.hostname:
							macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"WHERE",client.hostname)
						else:
							macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"WHERE",client.server+":"+str(client.port))
					else:
						macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"WHERE",window.name)

					return macro_data
				elif len(tokens)!=macro_argcount:
					if macro_args==None:
						msg = Message(ERROR_MESSAGE,'',"Macro \""+config.INPUT_COMMAND_SYMBOL+macro_name+"\" requires "+str(macro_argcount)+" arguments")
						window.writeText(msg,True)
					else:
						msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+macro_name+" "+macro_args)
						window.writeText(msg,True)
					return None
				else:
					counter = 0
					for a in tokens:
						counter = counter + 1
						macro_data = macro_data.replace(config.MACRO_INTERPOLATE_SYMBOL+str(counter),a)
					macro_data = macro_data.replace(config.MACRO_INTERPOLATE_SYMBOL+"0",' '.join(tokens))
					if len(tokens)>1:
						rest = tokens[1:]
						macro_data = macro_data.replace(config.MACRO_INTERPOLATE_SYMBOL+"+",' '.join(rest))

					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"NICK",client.nickname)
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"USERNAME",client.username)
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"REALNAME",client.realname)
					if client.hostname:
						macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"HOSTNAME",client.hostname)
					else:
						macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"HOSTNAME",client.server+":"+str(client.port))
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"SERVER",client.server)
					macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"PORT",str(client.port))

					if window.name==SERVER_CONSOLE_NAME:
						if client.hostname:
							macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"WHERE",client.hostname)
						else:
							macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"WHERE",client.server+":"+str(client.port))
					else:
						macro_data = macro_data.replace(config.SCRIPT_INTERPOLATE_SYMBOL+"WHERE",window.name)

					return macro_data

	return text

def handle_input(window,client,text,force=True,is_script=False):
	if len(text.strip())==0: return

	# Strip leading and trailing whitespace
	text = text.strip()

	# Allow use of the CTCP action command if commands are blocked
	if config.ALWAYS_ALLOW_ME:
		if not force:
			tokens = text.split()
			if len(tokens)>0:
				if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'me' and len(tokens)>=2:
					force = True

	if not force:
		if window.type!=config.SERVER_WINDOW:
			if config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)
			client.msg(window.name,text)
		return

	if not client.gui.block_scripts:
		for key in VARIABLE_TABLE:
			text = text.replace(config.SCRIPT_INTERPOLATE_SYMBOL+key,VARIABLE_TABLE[key])

	if not client.gui.block_scripts:
		if config.ENABLE_MACROS:
			text = handle_macros(window,client,text)
			if text == None: return

	if handle_ui_input(window,client,text):
		window.input.setFocus()
		return

	if not is_script:
		if plugins.input(client,window,text):
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

def handle_channel_input(window,client,text):

	# if not client.gui.block_plugins:
	# 	if client.gui.plugins.input(client,window.name,text): return True

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
			
			hdisplay = list(CHAT_HELP_ENTRIES)

			if not client.gui.block_scripts:
				if config.ENABLE_MACROS:
					if len(MACROS)>0:
						for m in MACROS:
							macro_name = m.name
							macro_argcount = m.argcount
							if m.args==None:
								if macro_argcount<0:
									margs = "[ARG...]"
								else:
									margs = "ARG "*macro_argcount
									margs = margs.strip()
							else:
								margs = m.args
							t = HELP_ENTRY
							t = t.replace("%_USAGE_%","<b>"+config.INPUT_COMMAND_SYMBOL+macro_name+" "+margs+"</b>")
							if m.help==None:
								t = t.replace("%_DESCRIPTION_%","Macro")
							else:
								t = t.replace("%_DESCRIPTION_%",m.help)
							hdisplay.append(t)

			if not client.gui.block_plugins:
				if config.PLUGIN_HELP:
					if len(plugins.HELP)>0:
						for entry in plugins.HELP:
							t = HELP_ENTRY
							t = t.replace("%_USAGE_%","<b>"+entry[0]+"</b>")
							t = t.replace("%_DESCRIPTION_%",entry[1])
							hdisplay.append(t)

			CHAT_HELP_DISPLAY = CHAT_HELP_HTML_TEMPLATE.replace("%_LIST_%","\n".join(hdisplay))
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
			client.part(window.name,config.DEFAULT_QUIT_PART_MESSAGE)
			return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'part' and len(tokens)>=2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# channel has not been passed as an argument
				tokens.pop(0)
				partmsg = ' '.join(tokens)
				client.part(window.name,partmsg)
				return True

	if handle_common_input(window,client,text): return

	if config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)

	client.msg(window.name,text)

def handle_private_input(window,client,text):

	# if not client.gui.block_plugins:
	# 	if client.gui.plugins.input(client,window.name,text): return True

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'help':
			hdisplay = list(CHAT_HELP_ENTRIES)

			if not client.gui.block_scripts:
				if config.ENABLE_MACROS:
					if len(MACROS)>0:
						for m in MACROS:
							macro_name = m.name
							macro_argcount = m.argcount
							if m.args==None:
								if macro_argcount<0:
									margs = "[ARG...]"
								else:
									margs = "ARG "*macro_argcount
									margs = margs.strip()
							else:
								margs = m.args
							t = HELP_ENTRY
							t = t.replace("%_USAGE_%","<b>"+config.INPUT_COMMAND_SYMBOL+macro_name+" "+margs+"</b>")
							if m.help==None:
								t = t.replace("%_DESCRIPTION_%","Macro")
							else:
								t = t.replace("%_DESCRIPTION_%",m.help)
							hdisplay.append(t)

			if not client.gui.block_plugins:
				if config.PLUGIN_HELP:
					if len(plugins.HELP)>0:
						for entry in plugins.HELP:
							t = HELP_ENTRY
							t = t.replace("%_USAGE_%","<b>"+entry[0]+"</b>")
							t = t.replace("%_DESCRIPTION_%",entry[1])
							hdisplay.append(t)

			CHAT_HELP_DISPLAY = CHAT_HELP_HTML_TEMPLATE.replace("%_LIST_%","\n".join(hdisplay))
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

	# if not client.gui.block_plugins:
	# 	if client.gui.plugins.input(client,window.name,text): return
	
	if handle_common_input(window,client,text): return

def handle_common_input(window,client,text):
	global LIST_THREAD

	tokens = text.split()

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
				client.list_search = "*"
				client.sendLine("LIST")
				msg = Message(LIST_MESSAGE,'',"Fetching server channel list, please wait a moment...")
				window.writeText(msg,True)
				return True
			else:
				LIST_THREAD = SearchListThread(client.channellist,'*',window)
				LIST_THREAD.found.connect(found_in_list)
				LIST_THREAD.begin.connect(begin_list)
				LIST_THREAD.end.connect(end_list)
				LIST_THREAD.start()
				return True

		if len(tokens)>=2 and tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'list':
			tokens.pop(0)	# remove command
			terms = ' '.join(tokens)
			if len(client.channels)==0:
				client.list_requested = True
				client.list_window = window
				client.list_search = terms
				client.sendLine("LIST")
				msg = Message(LIST_MESSAGE,'',"Fetching server channel list, please wait a moment...")
				window.writeText(msg,True)
				return True
			else:
				LIST_THREAD = SearchListThread(client.channellist,terms,window)
				LIST_THREAD.found.connect(found_in_list)
				LIST_THREAD.begin.connect(begin_list)
				LIST_THREAD.end.connect(end_list)
				LIST_THREAD.start()
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'help':
			hdisplay = list(COMMAND_HELP_ENTRIES)

			if not client.gui.block_scripts:
				if config.ENABLE_MACROS:
					if len(MACROS)>0:
						for m in MACROS:
							macro_name = m.name
							macro_argcount = m.argcount
							if m.args==None:
								if macro_argcount<0:
									margs = "[ARG...]"
								else:
									margs = "ARG "*macro_argcount
									margs = margs.strip()
							else:
								margs = m.args
							t = HELP_ENTRY
							t = t.replace("%_USAGE_%","<b>"+config.INPUT_COMMAND_SYMBOL+macro_name+" "+margs+"</b>")
							if m.help==None:
								t = t.replace("%_DESCRIPTION_%","Macro")
							else:
								t = t.replace("%_DESCRIPTION_%",m.help)
							hdisplay.append(t)

			if not client.gui.block_plugins:
				if config.PLUGIN_HELP:
					if len(plugins.HELP)>0:
						for entry in plugins.HELP:
							t = HELP_ENTRY
							t = t.replace("%_USAGE_%","<b>"+entry[0]+"</b>")
							t = t.replace("%_DESCRIPTION_%",entry[1])
							hdisplay.append(t)

			CHAT_HELP_DISPLAY = CHAT_HELP_HTML_TEMPLATE.replace("%_LIST_%","\n".join(hdisplay))
			msg = Message(PLUGIN_MESSAGE,'',CHAT_HELP_DISPLAY)
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
			window.parent.disconnect_current(config.DEFAULT_QUIT_PART_MESSAGE)
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
			client.part(channel,config.DEFAULT_QUIT_PART_MESSAGE)
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
			client.part(channel,partmsg)
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

	global MACROS

	tokens = text.split()

	# IGNORE BEGIN

	if len(tokens)>0:
		if not config.ENABLE_IGNORE and tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ignore':
			msg = Message(ERROR_MESSAGE,'',f"Ignore is disabled.")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if not config.ENABLE_IGNORE and tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'unignore':
			msg = Message(ERROR_MESSAGE,'',f"Unignore is disabled.")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ignore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)

			ilist = client.gui.ignore
			for t in ilist:
				if t==target:
					msg = Message(ERROR_MESSAGE,'',f"\"{target}\" is already ignored.")
					window.writeText(msg,True)
					return True

			if target=='*':
				msg = Message(ERROR_MESSAGE,'',f"Warning! You are now ignoring all messages sent to you, public or private")
				window.writeText(msg,True)
				msg = Message(ERROR_MESSAGE,'',f"Type \"{config.INPUT_COMMAND_SYMBOL}unignore *\" to stop ignoring all messages")
				window.writeText(msg,True)

			client.gui.ignore.append(target)
			u = get_user(client.gui.userfile)
			u["ignore"] = client.gui.ignore
			save_user(u,client.gui.userfile)

			events.recheck_userlists()

			msg = Message(SYSTEM_MESSAGE,'',f"\"{target}\" is now ignored.")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ignore' and len(tokens)==1:

			ilist = []
			for t in client.gui.ignore:
				ilist.append(t)

			if len(ilist)==0:
				msg = Message(SYSTEM_MESSAGE,'',"No ignored targets.")
				window.writeText(msg,True)
				return True

			msg = Message(SYSTEM_MESSAGE,'',"Ignored targets: "+", ".join(ilist))
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ignore':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"ignore TARGET")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'unignore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)

			ilist = client.gui.ignore
			clean = []
			for t in ilist:
				if t==target: continue
				clean.append(t)

			if len(ilist)==len(clean) and target!='*':
				msg = Message(ERROR_MESSAGE,'',f"\"{target}\" is not being ignored.")
				window.writeText(msg,True)
				return True

			client.gui.ignore = clean
			u = get_user(client.gui.userfile)
			u["ignore"] = client.gui.ignore
			save_user(u,client.gui.userfile)

			events.recheck_userlists()

			msg = Message(SYSTEM_MESSAGE,'',f"\"{target}\" is unignored.")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'unignore':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"unignore TARGET")
			window.writeText(msg,True)
			return True

	# IGNORE END



	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'cat' and len(tokens)==3:
			tokens.pop(0)
			target = tokens.pop(0)
			filename = tokens.pop(0)

			f = find_cat_file(filename,client.gui.scriptsdir)
			if f!=None:
				with open(f) as fp:
					lines = fp.readlines()
					for line in lines:
						client.msg(target,line)
				return True
			else:
				msg = Message(ERROR_MESSAGE,'',"File \'"+filename+"\" not found")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'cat' and len(tokens)==2:
			tokens.pop(0)
			filename = tokens.pop(0)

			if window.name==SERVER_CONSOLE_NAME:
				msg = Message(ERROR_MESSAGE,'',"Messages can't be sent to server.")
				window.writeText(msg,True)
				return True

			f = find_cat_file(filename,client.gui.scriptsdir)
			if f!=None:
				with open(f) as fp:
					lines = fp.readlines()
					for line in lines:
						client.msg(window.name,line)
				return True
			else:
				msg = Message(ERROR_MESSAGE,'',"File \'"+filename+"\" not found")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'cat':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"cat [TARGET] FILENAME")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'write' and len(tokens)>=2:
			tokens.pop(0)

			msg = Message(SYSTEM_MESSAGE,'',' '.join(tokens))
			window.writeText(msg,False)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'write':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"write MESSAGE...")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'dictionary' and len(tokens)>=2:
			tokens.pop(0)

			for t in tokens:
				config.DICTIONARY.append(t)

			config.save_settings(client.gui.configfile)

			if len(tokens)>1:
				last_word = tokens.pop()
				rep = "Added "+", ".join(tokens)+", and "+last_word+" to dictionary"
				msg = Message(SYSTEM_MESSAGE,'',rep)
				window.writeText(msg,True)
			else:
				word = tokens.pop(0)
				rep = "Added "+word+" to dictionary"
				msg = Message(SYSTEM_MESSAGE,'',rep)
				window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'dictionary':

			if len(config.DICTIONARY)==0:
				rep = "There are no dictionary entries"
			elif len(config.DICTIONARY)==1:
				rep = config.DICTIONARY[0]
			else:
				rep = ", ".join(config.DICTIONARY)


			msg = Message(SYSTEM_MESSAGE,'',rep)
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'undictionary' and len(tokens)>=2:
			tokens.pop(0)

			clean = []
			for e in config.DICTIONARY:
				if e in tokens: continue
				clean.append(e)
			config.DICTIONARY = list(clean)

			config.save_settings(client.gui.configfile)

			if len(tokens)>1:
				last_word = tokens.pop()
				rep = "Removed "+", ".join(tokens)+", and "+last_word+" from dictionary"
				msg = Message(SYSTEM_MESSAGE,'',rep)
				window.writeText(msg,True)
			else:
				word = tokens.pop(0)
				rep = "Removed "+word+" from dictionary"
				msg = Message(SYSTEM_MESSAGE,'',rep)
				window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'undictionary':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"undictionary WORD [WORD...]")
			window.writeText(msg,True)
			return True

	if client.gui.block_scripts:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macrousage':
				msg = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macrousage' and len(tokens)>=3:
			tokens.pop(0)
			name = tokens.pop(0)
			macrohelp = ' '.join(tokens)

			for m in MACROS:
				if m.name==name:
					m.args = macrohelp
					msg = Message(SYSTEM_MESSAGE,'',"Usage for macro \""+name+"\" updated")
					window.writeText(msg,True)
					return True

			msg = Message(ERROR_MESSAGE,'',"Macro \""+name+"\" not found")
			window.writeText(msg,True)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macrousage':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"macrousage NAME MESSAGE...")
			window.writeText(msg,True)
			return True

	if client.gui.block_scripts:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'unmacro':
				msg = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'unmacro' and len(tokens)==2:
			tokens.pop(0)
			name = tokens.pop(0)

			clean = []
			found = False
			for m in MACROS:
				if m.name==name:
					found = True
					continue
				clean.append(m)

			if found:
				MACROS = clean

				if config.SAVE_MACROS:
					save_macros(MACROS,client.gui.macrofile)

				msg = Message(SYSTEM_MESSAGE,'',"Macro \""+name+"\" removed")
				window.writeText(msg,True)
				return True
			else:
				msg = Message(ERROR_MESSAGE,'',"Macro \""+name+"\" not found")
				window.writeText(msg,True)
				return True

			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'unmacro':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"unmacro NAME")
			window.writeText(msg,True)
			return True

	if client.gui.block_scripts:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macrohelp':
				msg = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macrohelp' and len(tokens)>=3:
			tokens.pop(0)
			name = tokens.pop(0)
			macrohelp = ' '.join(tokens)

			for m in MACROS:
				if m.name==name:
					m.help = macrohelp
					msg = Message(SYSTEM_MESSAGE,'',"Help for macro \""+name+"\" updated")
					window.writeText(msg,True)
					return True

			msg = Message(ERROR_MESSAGE,'',"Macro \""+name+"\" not found")
			window.writeText(msg,True)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macrohelp':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"macrohelp NAME MESSAGE...")
			window.writeText(msg,True)
			return True

	if client.gui.block_scripts:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macro':
				msg = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macro' and len(tokens)>=4:
			tokens.pop(0)
			name = tokens.pop(0)
			args = tokens.pop(0)
			data = ' '.join(tokens)

			if name in PROTECTED_NAMES:
				msg = Message(ERROR_MESSAGE,'',"\""+name+"\" already exists as a command, and can't be used as a macro name")
				window.writeText(msg,True)
				return True

			for c in FORBIDDEN_CHARACTERS:
				if c in name:
					msg = Message(ERROR_MESSAGE,'',"Macro names can't contains the following: \""+c+"\"")
					window.writeText(msg,True)
					return True

			if args=='*': args = -1

			try:
				args = int(args)
			except:
				msg = Message(ERROR_MESSAGE,'',"Error calling "+config.INPUT_COMMAND_SYMBOL+"macro: \""+args+"\" is not a number")
				window.writeText(msg,True)
				return True
			else:
				m = Macro(name,args,data)

				NEW_MACROS = []
				replaced = False
				for c in MACROS:
					if c.name == name:
						NEW_MACROS.append(m)
						replaced = True
					else:
						NEW_MACROS.append(c)

				if replaced:
					msg = Message(SYSTEM_MESSAGE,'',"Replaced \""+name+"\" macro")
					window.writeText(msg,True)
				else:
					msg = Message(SYSTEM_MESSAGE,'',"Added \""+name+"\" macro")
					window.writeText(msg,True)
					NEW_MACROS.append(m)

				MACROS = list(NEW_MACROS)
				return True

			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'macro':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"macro NAME ARG_COUNT TEXT...")
			window.writeText(msg,True)
			return True

	if client.gui.block_styles:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'style':
				msg = Message(ERROR_MESSAGE,'',"Loading styles has been disabled.")
				window.writeText(msg,True)
				return True
	else:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'style' and len(tokens)==2:
				tokens.pop(0)
				file = tokens.pop(0)

				ffile = find_style_file(file,client.gui.styledir)
				if file!= None:
					window.loadNewStyle(ffile)
				else:
					msg = Message(ERROR_MESSAGE,'',f"Style file \"{file}\" not found.")
					window.writeText(msg,True)
				return True

		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'style' and len(tokens)!=2:
				msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"style FILENAME")
				window.writeText(msg,True)
				return True

	# The /msgbox command an only be called from scripts.
	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'msgbox':
			return True

	# The /wait command an only be called from scripts.
	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'wait':
			return True

	# The /unalias command an only be called from scripts.
	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'unalias':
			return True

	# The /alias command an only be called from scripts.
	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'alias':
			return True

	# The /_alias command an only be called from scripts.
	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'_alias':
			return True

	# The /argcount command an only be called from scripts.
	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'argcount':
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'preferences' and len(tokens)==1:
			window.prefDialog()
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'settings' and len(tokens)==1:
			window.prefDialog()
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'exit' and len(tokens)==1:
			window.parent.close()
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'exit' and len(tokens)!=1:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"exit")
			window.writeText(msg,True)
			return True

	# PRINT COMMAND

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'print' and len(tokens)>1:
			tokens.pop(0)
			pm = ' '.join(tokens)
			msg = Message(SYSTEM_MESSAGE,'',f"{pm}")
			window.writeText(msg,True)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'print' and len(tokens)==1:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"print MESSAGE")
			window.writeText(msg,True)
			return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'echo' and len(tokens)>1:
			tokens.pop(0)
			pm = ' '.join(tokens)
			msg = Message(SYSTEM_MESSAGE,'',f"{pm}")
			window.writeText(msg,True)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'echo' and len(tokens)==1:
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"echo MESSAGE")
			window.writeText(msg,True)
			return True

	# PRINT COMMAND

	if client.gui.block_editor:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'edit':
				msg = Message(ERROR_MESSAGE,'',"Script editor is disabled")
				window.writeText(msg,True)
				return True

	if client.gui.block_scripts:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'edit':
				msg = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'edit' and len(tokens)==1:
			if client.gui.seditors==None:
				client.gui.seditors = ScriptEditor(None,client.gui,client.gui.configfile,client.gui.scriptsdir,None)
				client.gui.seditors.resize(640,480)

				client.gui.seditors.clientsRefreshed(events.fetch_connections())
				return True
			else:
				client.gui.seditors.activateWindow()
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'edit' and len(tokens)==2:

			tokens.pop(0)
			file = tokens.pop(0)
			arguments = tokens

			scriptname = find_script_file(file,client.gui.scriptsdir)

			# if os.path.isfile(file):
			if scriptname!=None:
				if client.gui.seditors==None:

					client.gui.seditors = ScriptEditor(scriptname,client.gui,client.gui.configfile,client.gui.scriptsdir,None)
					client.gui.seditors.resize(640,480)

					client.gui.seditors.clientsRefreshed(events.fetch_connections())
					return True
				else:
					client.gui.seditors.openFile(scriptname)
					return True

			else:
				msg = Message(ERROR_MESSAGE,'',f"File \"{file}\" doesn't exist")
				window.writeText(msg,True)
				return True

	if client.gui.block_scripts:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connectscript':
				msg = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connectscript' and len(tokens)==3:
			tokens.pop(0)
			ip = tokens.pop(0)
			port = tokens.pop(0)

			script = load_auto_script(ip,port,client.gui.scriptsdir)
			if script==None:
				msg = Message(ERROR_MESSAGE,'',"Script for "+ip+":"+port+" not found.")
				window.writeText(msg,True)
				return True
			else:
				scriptname = get_auto_script_name(ip,port,client.gui.scriptsdir)
				base_scriptname = os.path.basename(scriptname)

				# Generate a random script ID
				scriptID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

				# Create a thread for the script and run it
				scriptThread = ScriptThreadWindow(window,client,script,scriptID,base_scriptname,dict(VARIABLE_TABLE),[])
				scriptThread.execLine.connect(execute_script_line)
				scriptThread.scriptEnd.connect(execute_script_end)
				scriptThread.scriptErr.connect(execute_script_error)
				scriptThread.msgBox.connect(execute_script_msgbox)
				scriptThread.unalias.connect(execute_script_unalias)
				scriptThread.start()

				# Store the thread so it doesn't get garbage collected
				entry = [scriptID,scriptThread]
				SCRIPT_THREADS.append(entry)

				return True


	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connectscript' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			if ':' in host:
				p = host.split(':')
				if len(p)!=2:
					msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"connectscript SERVER [PORT]")
					window.writeText(msg,True)
					return True
				ip = p[0]
				port = p[1]
			else:
				ip = host
				port = "6667"

			script = load_auto_script(ip,port,client.gui.scriptsdir)
			if script==None:
				msg = Message(ERROR_MESSAGE,'',"Script for "+ip+":"+port+" not found.")
				window.writeText(msg,True)
				return True
			else:
				scriptname = get_auto_script_name(ip,port,client.gui.scriptsdir)
				base_scriptname = os.path.basename(scriptname)

				# Generate a random script ID
				scriptID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

				# Create a thread for the script and run it
				scriptThread = ScriptThreadWindow(window,client,script,scriptID,base_scriptname,dict(VARIABLE_TABLE),[])
				scriptThread.execLine.connect(execute_script_line)
				scriptThread.scriptEnd.connect(execute_script_end)
				scriptThread.scriptErr.connect(execute_script_error)
				scriptThread.msgBox.connect(execute_script_msgbox)
				scriptThread.unalias.connect(execute_script_unalias)
				scriptThread.start()

				# Store the thread so it doesn't get garbage collected
				entry = [scriptID,scriptThread]
				SCRIPT_THREADS.append(entry)

				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connectscript':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"connectscript SERVER [PORT]")
			window.writeText(msg,True)
			return True


	if client.gui.block_scripts:
		if len(tokens)>0:
			if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'script':
				msg = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(msg,True)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'script' and len(tokens)>=2:

			tokens.pop(0)
			file = tokens.pop(0)
			arguments = tokens

			scriptname = find_script_file(file,client.gui.scriptsdir)

			# if os.path.isfile(file):
			if scriptname!=None:

				base_scriptname = os.path.basename(scriptname)

				# Read in the script
				s = open(scriptname,"r")
				script = s.read()
				s.close()

				# Generate a random script ID
				scriptID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

				# Create a thread for the script and run it
				scriptThread = ScriptThreadWindow(window,client,script,scriptID,base_scriptname,dict(VARIABLE_TABLE),arguments)
				scriptThread.execLine.connect(execute_script_line)
				scriptThread.scriptEnd.connect(execute_script_end)
				scriptThread.scriptErr.connect(execute_script_error)
				scriptThread.msgBox.connect(execute_script_msgbox)
				scriptThread.unalias.connect(execute_script_unalias)
				scriptThread.start()

				# Store the thread so it doesn't get garbage collected
				entry = [scriptID,scriptThread]
				SCRIPT_THREADS.append(entry)

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
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'switch' and len(tokens)==1:
			channels = window.channelList()
			privates = window.privateList()
			dl = channels + privates
			if len(dl>0):
				msg = Message(SYSTEM_MESSAGE,'',"Available chats: "+', '.join(dl))
				window.writeText(msg,True)
				return True
			else:
				msg = Message(SYSTEM_MESSAGE,'',"No available chats.")
				window.writeText(msg,True)
				return True
		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'switch':
			msg = Message(ERROR_MESSAGE,'',"Usage: "+config.INPUT_COMMAND_SYMBOL+"switch [CHAT_NAME]")
			window.writeText(msg,True)
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

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False,False)
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

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False,False)
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

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False,False)
			window.doConnect(info)
			return True

			# RECONNECT

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'reconnect' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True,False)
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

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True,False)
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

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True,False)
			window.doConnect(info)
			return True

			#ssl

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ssl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6697
			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False,False)
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

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False,False)
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

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[],False,False)
			window.doConnect(info)
			return True

			#ressl

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ressl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6697
			user = get_user(client.gui.userfile)

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True,False)
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

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True,False)
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

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[],True,False)
			window.doConnect(info)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'connect':
			window.connectDialogCmd(None,None)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'reconnect':
			window.connectDialogCmd(None,True)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ssl':
			window.connectDialogCmd(True,None)
			return True

		if tokens[0].lower()==config.INPUT_COMMAND_SYMBOL+'ressl':
			window.connectDialogCmd(True,True)
			return True

	return False

def execute_code(script,client,err_func,end_func):

	window = events.fetch_console_window(client)

	# Generate a random script ID
	scriptID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

	# Create a thread for the script and run it
	scriptThread = ScriptThreadWindow(window,client,script,scriptID,'Editor',dict(VARIABLE_TABLE),[])
	scriptThread.execLine.connect(execute_script_line)
	scriptThread.scriptEnd.connect(execute_script_end)
	scriptThread.scriptEnd.connect(end_func)
	scriptThread.scriptErr.connect(err_func)
	scriptThread.msgBox.connect(execute_script_msgbox)
	scriptThread.unalias.connect(execute_script_unalias)
	scriptThread.start()

	# Store the thread so it doesn't get garbage collected
	entry = [scriptID,scriptThread]
	SCRIPT_THREADS.append(entry)

def execute_script(filename,window,client):

	scriptname = find_script_file(filename,client.gui.scriptsdir)

	# if os.path.isfile(file):
	if scriptname!=None:

		base_scriptname = os.path.basename(scriptname)

		# Read in the script
		s = open(scriptname,"r")
		script = s.read()
		s.close()

		# Generate a random script ID
		scriptID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

		# Create a thread for the script and run it
		scriptThread = ScriptThreadWindow(window,client,script,scriptID,base_scriptname,dict(VARIABLE_TABLE),[])
		scriptThread.execLine.connect(execute_script_line)
		scriptThread.scriptEnd.connect(execute_script_end)
		scriptThread.scriptErr.connect(execute_script_error)
		scriptThread.msgBox.connect(execute_script_msgbox)
		scriptThread.unalias.connect(execute_script_unalias)
		scriptThread.start()

		# Store the thread so it doesn't get garbage collected
		entry = [scriptID,scriptThread]
		SCRIPT_THREADS.append(entry)

# Executes a single line from a script's thread
def execute_script_line(data):
	window = data[0]
	client = data[1]
	line = data[2]

	#line = interpolate_for_script(client,line)

	handle_input(window,client,line,True,True)

# When a script completes, this is called which deletes the
# script's thread
def execute_script_end(data):
	mid = data[0]
	vtable = data[1]

	global SCRIPT_THREADS
	clean = []
	for e in SCRIPT_THREADS:
		if e[0]==mid:
			del e[1]
			continue
		clean.append(e)
	SCRIPT_THREADS = clean

	if config.GLOBALIZE_ALL_SCRIPT_ALIASES:
		VARIABLE_TABLE.update(vtable)

# Triggers every time there's a script error
def execute_script_error(data):
	window = data[0]
	errmsg = data[1]
	msg = Message(ERROR_MESSAGE,'',errmsg)
	window.writeText(msg,True)

def execute_script_msgbox(data):
	scriptname = data[0]
	msg = data[1]

	x = QMessageBox()
	x.setText(msg)
	x.setWindowTitle(scriptname)
	x.exec_()

def execute_script_unalias(data):
	scriptname = data[0]
	alias = data[1]

	global VARIABLE_TABLE
	if alias in VARIABLE_TABLE:
		VARIABLE_TABLE.pop(alias)