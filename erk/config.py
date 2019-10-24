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

import sys
import os
import json
from datetime import datetime
import shutil
import re
import string
import random
from itertools import combinations

# Directories
INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")
SETTINGS_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "settings")
LOG_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "logs")

USER_FILE = os.path.join(SETTINGS_DIRECTORY, "user.json")
LAST_SERVER_INFORMATION_FILE = os.path.join(SETTINGS_DIRECTORY, "lastserver.json")
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "erk.json")
TEXT_SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "style.json")
CHANNELS_FILE = os.path.join(SETTINGS_DIRECTORY, "channels.json")
IGNORE_FILE = os.path.join(SETTINGS_DIRECTORY, "ignore.json")
HISTORY_FILE = os.path.join(SETTINGS_DIRECTORY, "history.json")

MINOR_VERSION_FILE = os.path.join(DATA_DIRECTORY, "minor.txt")

NETWORK_FILE = os.path.join(DATA_DIRECTORY, "servers.txt")
ASCIIEMOJI_LIST = os.path.join(DATA_DIRECTORY, "asciiemoji.json")
PROFANITY_LIST = os.path.join(DATA_DIRECTORY, "profanity.txt")

AUTOCOMPLETE_DIRECTORY = os.path.join(DATA_DIRECTORY, "autocomplete")
ASCIIMOJI_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "asciimoji.txt")
EMOJI_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji2.txt")
EMOJI_ALIAS_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji1.txt")

mvf=open(MINOR_VERSION_FILE, "r")
MINOR_VERSION = mvf.read()
mvf.close()

if len(MINOR_VERSION)==1:
	MINOR_VERSION = "00"+MINOR_VERSION
elif len(MINOR_VERSION)==2:
	MINOR_VERSION = "0"+MINOR_VERSION

APPLICATION_NAME = "Ərk"
APPLICATION_MAJOR_VERSION = "0.500"
APPLICATION_VERSION = APPLICATION_MAJOR_VERSION+"."+MINOR_VERSION
OFFICIAL_REPOSITORY = "https://github.com/nutjob-laboratories/erk"
PROGRAM_FILENAME = "erk.py"
NORMAL_APPLICATION_NAME = "Erk"

GPL_NOTIFICATION = """Ərk IRC Client
Copyright (C) 2019  Dan Hetrick

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

DEFAULT_WINDOW_TITLE = APPLICATION_NAME

DEFAULT_NICKNAME = "erk"+str(random.randint(100,1000000))
DEFAULT_ALTERNATIVE = DEFAULT_NICKNAME+"_"
DEFAULT_USERNAME = "erk"
DEFAULT_IRCNAME = APPLICATION_NAME+" IRC Client v"+APPLICATION_MAJOR_VERSION

SETTING_OPEN_PRIVATE_WINDOWS		= "open_windows_for_private_messages"
SETTING_CHAT_STATUS_BARS			= "display_chat_window_status_bars"
SETTING_PLAIN_USER_LISTS			= "plain_user_lists"
SETTING_APPLICATION_FONT			= "font"
SETTING_DISPLAY_TIMESTAMPS			= 'display_chat_timestamps'
SETTING_24HOUR_TIMESTAMPS			= 'use_24_hour_clock_timestamps'
SETTING_DISPLAY_TIMESTAMP_SECONDS	= 'display_seconds_in_timestamps'
SETTING_SAVE_LOGS_ON_EXIT			= 'automatically_save_logs'
SETTING_LOAD_LOGS_ON_START			= 'automatically_load_logs'
SETTING_SPELL_CHECK					= "spell_check"
SETTING_SPELL_CHECK_LANGUAGE		= "spell_check_language"
SETTING_EMOJI						= "enable_emojis"
SETTING_ASCIIMOJI					= "enable_asciimoji"
SETTING_LOADED_LOG_LENGTH			= "maximum_displayed_log_length"
SETTING_MAX_NICK_LENGTH				= "maximum_nickname_displayed_length"
SETTING_SET_WINDOW_TITLE_TO_ACTIVE	= "set_application_title_to_active_window_title"
SETTING_WINDOW_WIDTH				= "default_window_width"
SETTING_WINDOW_HEIGHT				= "default_window_height"
SETTING_AUTOCOMPLETE_CMDS			= "autocomplete_commands"
SETTING_AUTOCOMPLETE_NICKS			= "autocomplete_nicknames_and_channels"
SETTING_HYPERLINKS					= "link_urls_in_chat"
SETTING_STRIP_HTML					= "strip_html_from_chat"
SETTING_PROFANITY_FILTER			= "do_not_display_profanity"
SETTING_LOG_PRIVATE_CHAT			= "save_private_chat_logs"
SETTING_HIDE_PRIVATE_CHAT			= "hide_private_chat_on_close"
SETTING_SAVE_HISTORY				= "save_server_history"
SETTING_ASCIIMOJI_AUTOCOMPLETE		= "autocomplete_asciimojis"
SETTING_EMOJI_AUTOCOMPLETE			= "autocomplete_emojis"
SETTING_DISPLAY_UPTIME_CONSOLE		= "display_uptime_on_console"
SETTING_DISPLAY_UPTIME_CHAT			= "display_uptime_on_chat_windows"
SETTING_UPTIME_SECONDS				= "diplay_seconds_in_uptime"
SETTING_KEEP_ALIVE					= "keep_connection_alive"
SETTING_DISPLAY_IRC_COLOR			= "display_irc_colors_in_chat"

SETTING_ENABLE_IGNORE				= "enable_user_ignore"

UNKNOWN_IRC_NETWORK = "Unknown"

DEFAULT_KEEPALIVE_INTERVAL = 120

IRC_00 = "#FFFFFF"
IRC_01 = "#000000"
IRC_02 = "#0000FF"
IRC_03 = "#008000"
IRC_04 = "#FF0000"
IRC_05 = "#A52A2A"
IRC_06 = "#800080"
IRC_07 = "#FFA500"
IRC_08 = "#FFFF00"
IRC_09 = "#90EE90"
IRC_10 = "#008080"
IRC_11 = "#00FFFF"
IRC_12 = "#ADD8E6"
IRC_13 = "#FFC0CB"
IRC_14 = "#808080"
IRC_15 = "#D3D3D3"

TIMESTAMP_STYLE_NAME	= "timestamp"
USERNAME_STYLE_NAME		= "username"
MESSAGE_STYLE_NAME		= "message"
SYSTEM_STYLE_NAME		= "system"
SELF_STYLE_NAME			= "self"
ACTION_STYLE_NAME		= "action"
NOTICE_STYLE_NAME		= "notice"
RESUME_STYLE_NAME		= "resume"
HYPERLINK_STYLE_NAME	= "hyperlink"
BASE_STYLE_NAME			= "base"
ERROR_STYLE_NAME		= "error"
WHOIS_STYLE_NAME		= "whois"
WHOIS_TEXT_STYLE_NAME	= "whois-text"

# Create any necessary directories if they don't exist
if not os.path.isdir(SETTINGS_DIRECTORY): os.mkdir(SETTINGS_DIRECTORY)
if not os.path.isdir(LOG_DIRECTORY): os.mkdir(LOG_DIRECTORY)

# Read in the ascii emoji list
ASCIIEMOJIS = {}
with open(ASCIIEMOJI_LIST, "r",encoding="utf-8") as read_emojis:
	ASCIIEMOJIS = json.load(read_emojis)

# Load in the profanity data file
f = open(PROFANITY_LIST,"r")
cursewords = f.read()
f.close()

PROFANITY = cursewords.split("\n")
PROFANITY_SYMBOLS = ["#","!","@","&","%","$","?","+","*"]

def censorWord(word,punc=True):
	result = ''
	last = '+'
	for letter in word:
		if punc:
			random.shuffle(PROFANITY_SYMBOLS)		
			nl = random.choice(PROFANITY_SYMBOLS)
			while nl == last:
				nl = random.choice(PROFANITY_SYMBOLS)
			last = nl
			result = result + nl
		else:
			result = result + "*"
	return result

def filterProfanityFromText(text,punc=True):
	clean = []
	for word in text.split(' '):
		nopunc = word.translate(str.maketrans("","", string.punctuation))
		if nopunc in PROFANITY:
			word = censorWord(word,punc)
		clean.append(word)
	return ' '.join(clean)

def get_ignore():
	if os.path.isfile(IGNORE_FILE):
		with open(IGNORE_FILE, "r") as read_ignore:
			data = json.load(read_ignore)
			return data
	else:
		return []

def save_ignore(data):
	with open(IGNORE_FILE, "w") as write_data:
		json.dump(data, write_data, indent=4, sort_keys=True)

def inject_asciiemojis(data):
	for key in ASCIIEMOJIS:
		for word in ASCIIEMOJIS[key]["words"]:
			data = data.replace("("+word+")",ASCIIEMOJIS[key]["ascii"])
	return data

def loadChannels(filename=CHANNELS_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as channel_data:
			data = json.load(channel_data)
			return data
	else:
		return []

def saveChannels(autojoins,filename=CHANNELS_FILE):
	with open(filename, "w") as writelog:
		json.dump(autojoins, writelog, indent=4, sort_keys=True)

def trimLog(ilog,maxsize):
	count = 0
	shortlog = []
	for line in reversed(ilog):
		count = count + 1
		shortlog.append(line)
		if count >= maxsize:
			break
	return list(reversed(shortlog))

def encodeLogName(serverid,name=None):
	serverid = serverid.replace(":","-")
	if name==None:
		return f"{serverid}.json"
	else:
		return f"{serverid}-{name}.json"

def saveLog(serverid,name,logs):
	f = encodeLogName(serverid,name)
	logfile = os.path.join(LOG_DIRECTORY,f)

	slog = loadLog(serverid,name)
	for e in logs:
		slog.append(e)

	with open(logfile, "w") as writelog:
		json.dump(slog, writelog, indent=4, sort_keys=True)

def loadLog(serverid,name):
	f = encodeLogName(serverid,name)
	logfile = os.path.join(LOG_DIRECTORY,f)

	if os.path.isfile(logfile):
		with open(logfile, "r") as logentries:
			data = json.load(logentries)
			return data
	else:
		return []

def patch_config_file(data):
	s = len(data)
	if not SETTING_OPEN_PRIVATE_WINDOWS in data: data[SETTING_OPEN_PRIVATE_WINDOWS] = True
	if not SETTING_CHAT_STATUS_BARS in data: data[SETTING_CHAT_STATUS_BARS] = True
	if not SETTING_PLAIN_USER_LISTS in data: data[SETTING_PLAIN_USER_LISTS] = False
	if not SETTING_APPLICATION_FONT in data: data[SETTING_APPLICATION_FONT] = "Consolas,10,-1,5,50,0,0,0,0,0,Regular"
	if not SETTING_DISPLAY_TIMESTAMPS in data: data[SETTING_DISPLAY_TIMESTAMPS] = True
	if not SETTING_24HOUR_TIMESTAMPS in data: data[SETTING_24HOUR_TIMESTAMPS] = True
	if not SETTING_DISPLAY_TIMESTAMP_SECONDS in data: data[SETTING_DISPLAY_TIMESTAMP_SECONDS] = False
	if not SETTING_SAVE_LOGS_ON_EXIT in data: data[SETTING_SAVE_LOGS_ON_EXIT] = True
	if not SETTING_LOAD_LOGS_ON_START in data: data[SETTING_LOAD_LOGS_ON_START] = True
	if not SETTING_SPELL_CHECK in data: data[SETTING_SPELL_CHECK] = True
	if not SETTING_SPELL_CHECK_LANGUAGE in data: data[SETTING_SPELL_CHECK_LANGUAGE] = "en"
	if not SETTING_EMOJI in data: data[SETTING_EMOJI] = True
	if not SETTING_ASCIIMOJI in data: data[SETTING_ASCIIMOJI] = True
	if not SETTING_LOADED_LOG_LENGTH in data: data[SETTING_LOADED_LOG_LENGTH] = 300
	if not SETTING_MAX_NICK_LENGTH in data: data[SETTING_MAX_NICK_LENGTH] = 16
	if not SETTING_SET_WINDOW_TITLE_TO_ACTIVE in data: data[SETTING_SET_WINDOW_TITLE_TO_ACTIVE] = True
	if not SETTING_WINDOW_WIDTH in data: data[SETTING_WINDOW_WIDTH] = 500
	if not SETTING_WINDOW_HEIGHT in data: data[SETTING_WINDOW_HEIGHT] = 275
	if not SETTING_AUTOCOMPLETE_CMDS in data: data[SETTING_AUTOCOMPLETE_CMDS] = True
	if not SETTING_AUTOCOMPLETE_NICKS in data: data[SETTING_AUTOCOMPLETE_NICKS] = True
	if not SETTING_HYPERLINKS in data: data[SETTING_HYPERLINKS] = True
	if not SETTING_STRIP_HTML in data: data[SETTING_STRIP_HTML] = False
	if not SETTING_PROFANITY_FILTER in data: data[SETTING_PROFANITY_FILTER] = False
	if not SETTING_LOG_PRIVATE_CHAT in data: data[SETTING_LOG_PRIVATE_CHAT] = False
	if not SETTING_HIDE_PRIVATE_CHAT in data: data[SETTING_HIDE_PRIVATE_CHAT] = True
	if not SETTING_SAVE_HISTORY in data: data[SETTING_SAVE_HISTORY] = True
	if not SETTING_ASCIIMOJI_AUTOCOMPLETE in data: data[SETTING_ASCIIMOJI_AUTOCOMPLETE] = True
	if not SETTING_EMOJI_AUTOCOMPLETE in data: data[SETTING_EMOJI_AUTOCOMPLETE] = True
	if not SETTING_DISPLAY_UPTIME_CONSOLE in data: data[SETTING_DISPLAY_UPTIME_CONSOLE] = True
	if not SETTING_DISPLAY_UPTIME_CHAT in data: data[SETTING_DISPLAY_UPTIME_CHAT] = False
	if not SETTING_UPTIME_SECONDS in data: data[SETTING_UPTIME_SECONDS] = True
	if not SETTING_KEEP_ALIVE in data: data[SETTING_KEEP_ALIVE] = True
	if not SETTING_DISPLAY_IRC_COLOR in data: data[SETTING_DISPLAY_IRC_COLOR] = True
	if not SETTING_ENABLE_IGNORE in data: data[SETTING_ENABLE_IGNORE] = True

	if len(data)>s:
		return [True,data]
	else:
		return [False,data]

def get_settings(filename=SETTINGS_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)
			patched,data = patch_config_file(data)
			if patched: save_settings(data)
			return data
	else:
		si = {
			SETTING_OPEN_PRIVATE_WINDOWS: True,
			SETTING_CHAT_STATUS_BARS: True,
			SETTING_PLAIN_USER_LISTS: False,
			SETTING_APPLICATION_FONT: "Consolas,10,-1,5,50,0,0,0,0,0,Regular",
			SETTING_DISPLAY_TIMESTAMPS: True,
			SETTING_24HOUR_TIMESTAMPS: True,
			SETTING_DISPLAY_TIMESTAMP_SECONDS: False,
			SETTING_SAVE_LOGS_ON_EXIT: True,
			SETTING_LOAD_LOGS_ON_START: True,
			SETTING_SPELL_CHECK: True,
			SETTING_SPELL_CHECK_LANGUAGE: "en",
			SETTING_EMOJI: True,
			SETTING_ASCIIMOJI: True,
			SETTING_LOADED_LOG_LENGTH: 300,
			SETTING_MAX_NICK_LENGTH: 16,
			SETTING_SET_WINDOW_TITLE_TO_ACTIVE: True,
			SETTING_WINDOW_WIDTH: 500,
			SETTING_WINDOW_HEIGHT: 275,
			SETTING_AUTOCOMPLETE_CMDS: True,
			SETTING_AUTOCOMPLETE_NICKS: True,
			SETTING_HYPERLINKS: True,
			SETTING_STRIP_HTML: False,
			SETTING_PROFANITY_FILTER: False,
			SETTING_LOG_PRIVATE_CHAT: False,
			SETTING_HIDE_PRIVATE_CHAT: True,
			SETTING_SAVE_HISTORY: True,
			SETTING_ASCIIMOJI_AUTOCOMPLETE: True,
			SETTING_EMOJI_AUTOCOMPLETE: True,
			SETTING_DISPLAY_UPTIME_CONSOLE: True,
			SETTING_DISPLAY_UPTIME_CHAT: False,
			SETTING_UPTIME_SECONDS: True,
			SETTING_KEEP_ALIVE: True,
			SETTING_DISPLAY_IRC_COLOR: True,
			SETTING_ENABLE_IGNORE: True,
		}
		save_settings(si)
		return si

def save_settings(settings,filename=SETTINGS_FILE):
	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def get_network_list(filename=NETWORK_FILE):
	servlist = []
	with open(NETWORK_FILE) as fp:
		line = fp.readline()
		line=line.strip()
		while line:
			line=line.strip()
			p = line.split(':')
			servlist.append(p)
			line = fp.readline()
	return servlist

def get_history_list(filename=HISTORY_FILE):
	history_list = []
	h = get_history()
	for entry in h:
		if entry["ssl"]:
			s = 'ssl'
		else:
			s = 'normal'
		e = [ entry["server"],entry["port"],entry["network"],s,entry["password"] ]
		history_list.append(e)
	return history_list

def get_history(filename=HISTORY_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_history:
			data = json.load(read_history)
			return data
	else:
		return []

def update_history_network(server,port,network,filename=HISTORY_FILE):
	h = get_history()
	new_history = []
	found = False
	for entry in h:
		if entry["server"].lower()==server.lower():
			if entry["port"]==port:
				if entry["network"] == UNKNOWN_IRC_NETWORK:
					found = True
					entry["network"] = network
		new_history.append(entry)
	if found:
		with open(filename, "w") as write_data:
			json.dump(new_history, write_data, indent=4, sort_keys=True)
			return

def add_history(server,port,password,ssl,network,filename=HISTORY_FILE):
	# Make sure this isn't an entry in the network list
	for p in get_network_list():
		if len(p)>5: continue
		if len(p)<4: continue
		if p[0]==server:
			if p[1]==str(port):
				return
	if not password: password = ''
	h = get_history()
	new_history = []
	found = False
	for entry in h:
		if entry["server"].lower()==server.lower():
			if entry["port"]==port:
				found = True
				entry["password"] = password
				entry["ssl"] = ssl
		new_history.append(entry)
	if found:
		with open(filename, "w") as write_data:
			json.dump(new_history, write_data, indent=4, sort_keys=True)
			return
	entry = {
		"server": server,
		"port": port,
		"password": password,
		"ssl": ssl,
		"network": network,
	}
	new_history.insert(0,entry)
	with open(filename, "w") as write_data:
		json.dump(new_history, write_data, indent=4, sort_keys=True)


def get_user(filename=USER_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_user:
			data = json.load(read_user)
			return data
	else:
		si = {
			"nickname": DEFAULT_NICKNAME,
			"username": DEFAULT_USERNAME,
			"realname": DEFAULT_IRCNAME,
			"alternate": DEFAULT_ALTERNATIVE,
		}
		return si

def save_user(user,filename=USER_FILE):
	with open(filename, "w") as write_data:
		json.dump(user, write_data, indent=4, sort_keys=True)

def save_last_server(host,port,password,ssl,reconnect=False,autojoin=False):
	sinfo = {
			"host": host,
			"port": port,
			"password": password,
			"ssl": ssl,
			"reconnect": reconnect,
			"autojoin": autojoin
		}
	with open(LAST_SERVER_INFORMATION_FILE, "w") as write_data:
		json.dump(sinfo, write_data, indent=4, sort_keys=True)

def get_last_server():
	if os.path.isfile(LAST_SERVER_INFORMATION_FILE):
		with open(LAST_SERVER_INFORMATION_FILE, "r") as read_server:
			data = json.load(read_server)
			return data
	else:
		si = {
			"host": '',
			"port": '',
			"password": '',
			"ssl": False,
			"reconnect": False,
			"autojoin": False
		}
		return si

# Text display

TIMESTAMP_STYLE = "font-weight: bold;"
USERNAME_STYLE = "font-weight: bold; color: blue;"
MESSAGE_STYLE = ""
SYSTEM_STYLE = "font-style: italic; font-weight: bold; color: orange;"
SELF_STYLE = "font-weight: bold; color: red;"
ACTION_STYLE = "font-style: italic; font-weight: bold; color: green;"
NOTICE_STYLE = "font-weight: bold; color: purple;"
RESUME_STYLE = "font-weight: bold; font-style: italic; color: #707070;"
HYPERLINK_STYLE = "text-decoration: underline; font-weight: bold; color: blue;"
BASE_STYLE = 'background-color: white; color: black;'
ERROR_STYLE = "font-style: italic; font-weight: bold; color: red;"
WHOIS_STYLE = "font-style: italic; font-weight: bold; color: blue;"
WHOIS_TEXT_STYLE = "font-weight: bold;"

TIMESTAMP_TEMPLATE = """<td style="vertical-align:top; font-size:small; text-align:left;"><div style="!TIMESTAMP_STYLE!">[!TIME!]</div></td><td style="font-size:small;">&nbsp;</td>"""

MESSAGE_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: right; vertical-align: top;"><div style="!ID_STYLE!">!ID!</div></td>
		<td style="text-align: left; vertical-align: top;">&nbsp;</td>
		!INSERT_MESSAGE_TEMPLATE!
	</tr>
	</tbody>
</table>
"""

SYSTEM_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		!INSERT_MESSAGE_TEMPLATE!
	</tr>
	</tbody>
</table>
"""

MESSAGE_STYLE_TEMPLATE = """<td style="text-align: left; vertical-align: top;"><div style="!MESSAGE_STYLE!">!MESSAGE!</div></td>"""
MESSAGE_NO_STYLE_TEMPLATE = """<td style="text-align: left; vertical-align: top;">!MESSAGE!</td>"""

def render_system(gui,timestamp_style,message_style,message,timestamp=None):

	if gui.filter_profanity: message = filterProfanityFromText(message)

	if gui.strip_html_from_chat: message = remove_html_markup(message)
	if gui.convert_links_in_chat: message = inject_www_links(message,gui.styles[HYPERLINK_STYLE_NAME])

	if gui.display_timestamp:
		if timestamp==None:
			t = datetime.timestamp(datetime.now())
		else:
			t = timestamp
		if gui.use_seconds_in_timestamp:
			secs = ':%S'
		else:
			secs = ''
		if gui.use_24_hour_timestamp:
			pretty = datetime.fromtimestamp(t).strftime('%H:%M' + secs)
		else:
			pretty = datetime.fromtimestamp(t).strftime('%I:%M' + secs)

		ts = TIMESTAMP_TEMPLATE.replace("!TIMESTAMP_STYLE!",timestamp_style)
		ts = ts.replace("!TIME!",pretty)
		msg = SYSTEM_TEMPLATE.replace("!TIMESTAMP!",ts)
	else:
		msg = SYSTEM_TEMPLATE.replace("!TIMESTAMP!",'')

	if message_style=="":
		msg = msg.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_NO_STYLE_TEMPLATE)
	else:
		msg = msg.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_STYLE_TEMPLATE)
		msg = msg.replace("!MESSAGE_STYLE!",message_style)

	msg = msg.replace("!MESSAGE!",message)
	return msg

def render_message(gui,timestamp_style,ident_style,ident,message_style,message,timestamp=None):

	if gui.filter_profanity: message = filterProfanityFromText(message)

	if gui.strip_html_from_chat: message = remove_html_markup(message)
	if gui.convert_links_in_chat: message = inject_www_links(message,gui.styles[HYPERLINK_STYLE_NAME])

	if gui.display_irc_colors:
		# render colors
		message = convert_irc_color_to_html(message)
	else:
		# strip colors
		message = strip_color(message)

	if gui.display_timestamp:
		if timestamp==None:
			t = datetime.timestamp(datetime.now())
		else:
			t = timestamp
		if gui.use_seconds_in_timestamp:
			secs = ':%S'
		else:
			secs = ''
		if gui.use_24_hour_timestamp:
			pretty = datetime.fromtimestamp(t).strftime('%H:%M' + secs)
		else:
			pretty = datetime.fromtimestamp(t).strftime('%I:%M' + secs)

		ts = TIMESTAMP_TEMPLATE.replace("!TIMESTAMP_STYLE!",timestamp_style)
		ts = ts.replace("!TIME!",pretty)
		msg = MESSAGE_TEMPLATE.replace("!TIMESTAMP!",ts)
	else:
		msg = MESSAGE_TEMPLATE.replace("!TIMESTAMP!",'')

	idl = gui.max_username_length - len(ident)
	if idl>0:
		ident = ('&nbsp;'*idl)+ident

	
	msg = msg.replace("!ID_STYLE!",ident_style)
	msg = msg.replace("!ID!",ident)
	
	if message_style=="":
		msg = msg.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_NO_STYLE_TEMPLATE)
	else:
		msg = msg.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_STYLE_TEMPLATE)
		msg = msg.replace("!MESSAGE_STYLE!",message_style)

	msg = msg.replace("!MESSAGE!",message)
	return msg

def patch_text_settings(data):
	s = len(data)
	if not NOTICE_STYLE_NAME in data: data[NOTICE_STYLE_NAME] = NOTICE_STYLE
	if not USERNAME_STYLE_NAME in data: data[USERNAME_STYLE_NAME] = USERNAME_STYLE
	if not MESSAGE_STYLE_NAME in data: data[MESSAGE_STYLE_NAME] = MESSAGE_STYLE
	if not SYSTEM_STYLE_NAME in data: data[SYSTEM_STYLE_NAME] = SYSTEM_STYLE
	if not SELF_STYLE_NAME in data: data[SELF_STYLE_NAME] = SELF_STYLE
	if not ACTION_STYLE_NAME in data: data[ACTION_STYLE_NAME] = ACTION_STYLE
	if not TIMESTAMP_STYLE_NAME in data: data[TIMESTAMP_STYLE_NAME] = TIMESTAMP_STYLE
	if not RESUME_STYLE_NAME in data: data[RESUME_STYLE_NAME] = RESUME_STYLE
	if not HYPERLINK_STYLE_NAME in data: data[HYPERLINK_STYLE_NAME] = HYPERLINK_STYLE
	if not BASE_STYLE_NAME in data: data[BASE_STYLE_NAME] = BASE_STYLE
	if not ERROR_STYLE_NAME in data: data[ERROR_STYLE_NAME] = ERROR_STYLE
	if not WHOIS_STYLE_NAME in data: data[WHOIS_STYLE_NAME] = WHOIS_STYLE
	if not WHOIS_TEXT_STYLE_NAME in data: data[WHOIS_TEXT_STYLE_NAME] = WHOIS_TEXT_STYLE
	if len(data)>s:
		return [True,data]
	else:
		return [False,data]

def get_text_settings(filename=TEXT_SETTINGS_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)
			patched,data = patch_text_settings(data)
			if patched:
				with open(filename, "w") as write_data:
					json.dump(data, write_data, indent=4, sort_keys=True)
			return data
	else:
		si = {
			TIMESTAMP_STYLE_NAME: TIMESTAMP_STYLE,
			USERNAME_STYLE_NAME: USERNAME_STYLE,
			MESSAGE_STYLE_NAME: MESSAGE_STYLE,
			SYSTEM_STYLE_NAME: SYSTEM_STYLE,
			SELF_STYLE_NAME: SELF_STYLE,
			ACTION_STYLE_NAME: ACTION_STYLE,
			NOTICE_STYLE_NAME: NOTICE_STYLE,
			RESUME_STYLE_NAME: RESUME_STYLE,
			HYPERLINK_STYLE_NAME: HYPERLINK_STYLE,
			BASE_STYLE_NAME: BASE_STYLE,
			ERROR_STYLE_NAME: ERROR_STYLE,
			WHOIS_STYLE_NAME: WHOIS_STYLE,
			WHOIS_TEXT_STYLE_NAME: WHOIS_TEXT_STYLE,
		}
		with open(filename, "w") as write_data:
			json.dump(si, write_data, indent=4, sort_keys=True)
		return si

def remove_html_markup(s):
	tag = False
	quote = False
	out = ""

	for c in s:
			if c == '<' and not quote:
				tag = True
			elif c == '>' and not quote:
				tag = False
			elif (c == '"' or c == "'") and tag:
				quote = not quote
			elif not tag:
				out = out + c

	return out

def inject_www_links(txt,style):
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', txt)
	for u in urls:
		u = re.sub('<[^<]+?>', '', u)
		link = f"<a href=\"{u}\"><span style=\"{style}\">{u}</span></a>"
		txt = txt.replace(u,link)
	return txt

def irc_color_full(fore,back,text):

	html_tag = "font"

	if fore==0: fore=IRC_00
	if fore==1: fore=IRC_01
	if fore==2: fore=IRC_02
	if fore==3: fore=IRC_03
	if fore==4: fore=IRC_04
	if fore==5: fore=IRC_05
	if fore==6: fore=IRC_06
	if fore==7: fore=IRC_07
	if fore==8: fore=IRC_08
	if fore==9: fore=IRC_09
	if fore==10: fore=IRC_10
	if fore==11: fore=IRC_11
	if fore==12: fore=IRC_12
	if fore==13: fore=IRC_13
	if fore==14: fore=IRC_14
	if fore==15: fore=IRC_15

	if back==0: back=IRC_00
	if back==1: back=IRC_01
	if back==2: back=IRC_02
	if back==3: back=IRC_03
	if back==4: back=IRC_04
	if back==5: back=IRC_05
	if back==6: back=IRC_06
	if back==7: back=IRC_07
	if back==8: back=IRC_08
	if back==9: back=IRC_09
	if back==10: back=IRC_10
	if back==11: back=IRC_11
	if back==12: back=IRC_12
	if back==13: back=IRC_13
	if back==14: back=IRC_14
	if back==15: back=IRC_15

	return f"<{html_tag} style=\"color: {fore}; background-color: {back}\">" + text + f"</{html_tag}>"

def irc_color(fore,text):

	html_tag = "font"

	if fore==0: fore=IRC_00
	if fore==1: fore=IRC_01
	if fore==2: fore=IRC_02
	if fore==3: fore=IRC_03
	if fore==4: fore=IRC_04
	if fore==5: fore=IRC_05
	if fore==6: fore=IRC_06
	if fore==7: fore=IRC_07
	if fore==8: fore=IRC_08
	if fore==9: fore=IRC_09
	if fore==10: fore=IRC_10
	if fore==11: fore=IRC_11
	if fore==12: fore=IRC_12
	if fore==13: fore=IRC_13
	if fore==14: fore=IRC_14
	if fore==15: fore=IRC_15

	return f"<{html_tag} style=\"color: {fore};\">" + text + f"</{html_tag}>"

def convert_irc_color_to_html(text):

	html_tag = "font"

	# other format tags
	fout = ''
	inbold = False
	initalic = False
	inunderline = False
	incolor = False
	for l in text:
		if l=="\x02":
			inbold = True
			fout = fout + "<b>"
			continue
		if l=="\x1D":
			initalic = True
			fout = fout + "<i>"
			continue
		if l=="\x1F":
			inunderline = True
			fout = fout + "<u>"
			continue
		if l=="\x03":
			incolor = True
			fout = fout + l
			continue

		if l=="\x0F":
			if incolor:
				incolor = False
				fout = fout + f"</{html_tag}>"
				continue
			if inbold:
				fout = fout + "</b>"
				inbold = False
				continue
			if initalic:
				fout = fout + "</i>"
				initalic = False
				continue
			if inunderline:
				fout = fout + "</u>"
				inunderline = False
				continue

		fout = fout + l

	if inbold: fout = fout + "</b>"
	if initalic: fout = fout + "</i>"
	if inunderline: fout = fout + "</u>"

	text = fout

	combos = list(combinations(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		if int(fore)==0: foreground = str(IRC_00)
		if int(fore)==1: foreground = str(IRC_01)
		if int(fore)==2: foreground = str(IRC_02)
		if int(fore)==3: foreground = str(IRC_03)
		if int(fore)==4: foreground = str(IRC_04)
		if int(fore)==5: foreground = str(IRC_05)
		if int(fore)==6: foreground = str(IRC_06)
		if int(fore)==7: foreground = str(IRC_07)
		if int(fore)==8: foreground = str(IRC_08)
		if int(fore)==9: foreground = str(IRC_09)
		if int(fore)==10: foreground = str(IRC_10)
		if int(fore)==11: foreground = str(IRC_11)
		if int(fore)==12: foreground = str(IRC_12)
		if int(fore)==13: foreground = str(IRC_13)
		if int(fore)==14: foreground = str(IRC_14)
		if int(fore)==15: foreground = str(IRC_15)

		if int(back)==0: background = str(IRC_00)
		if int(back)==1: background = str(IRC_01)
		if int(back)==2: background = str(IRC_02)
		if int(back)==3: background = str(IRC_03)
		if int(back)==4: background = str(IRC_04)
		if int(back)==5: background = str(IRC_05)
		if int(back)==6: background = str(IRC_06)
		if int(back)==7: background = str(IRC_07)
		if int(back)==8: background = str(IRC_08)
		if int(back)==9: background = str(IRC_09)
		if int(back)==10: background = str(IRC_10)
		if int(back)==11: background = str(IRC_11)
		if int(back)==12: background = str(IRC_12)
		if int(back)==13: background = str(IRC_13)
		if int(back)==14: background = str(IRC_14)
		if int(back)==15: background = str(IRC_15)

		t = f"\x03{fore},{back}"
		r = f"<{html_tag} style=\"color: {foreground}; background-color: {background}\">"
		text = text.replace(t,r)

	combos = list(combinations(["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		if int(fore)==0: foreground = str(IRC_00)
		if int(fore)==1: foreground = str(IRC_01)
		if int(fore)==2: foreground = str(IRC_02)
		if int(fore)==3: foreground = str(IRC_03)
		if int(fore)==4: foreground = str(IRC_04)
		if int(fore)==5: foreground = str(IRC_05)
		if int(fore)==6: foreground = str(IRC_06)
		if int(fore)==7: foreground = str(IRC_07)
		if int(fore)==8: foreground = str(IRC_08)
		if int(fore)==9: foreground = str(IRC_09)
		if int(fore)==10: foreground = str(IRC_10)
		if int(fore)==11: foreground = str(IRC_11)
		if int(fore)==12: foreground = str(IRC_12)
		if int(fore)==13: foreground = str(IRC_13)
		if int(fore)==14: foreground = str(IRC_14)
		if int(fore)==15: foreground = str(IRC_15)

		if int(back)==0: background = str(IRC_00)
		if int(back)==1: background = str(IRC_01)
		if int(back)==2: background = str(IRC_02)
		if int(back)==3: background = str(IRC_03)
		if int(back)==4: background = str(IRC_04)
		if int(back)==5: background = str(IRC_05)
		if int(back)==6: background = str(IRC_06)
		if int(back)==7: background = str(IRC_07)
		if int(back)==8: background = str(IRC_08)
		if int(back)==9: background = str(IRC_09)
		if int(back)==10: background = str(IRC_10)
		if int(back)==11: background = str(IRC_11)
		if int(back)==12: background = str(IRC_12)
		if int(back)==13: background = str(IRC_13)
		if int(back)==14: background = str(IRC_14)
		if int(back)==15: background = str(IRC_15)

		t = f"\x03{fore},{back}"
		r = f"<{html_tag} style=\"color: {foreground}; background-color: {background}\">"
		text = text.replace(t,r)

	text = text.replace("\x0310",f"<{html_tag} style=\"color: {IRC_10};\">")
	text = text.replace("\x0311",f"<{html_tag} style=\"color: {IRC_11};\">")
	text = text.replace("\x0312",f"<{html_tag} style=\"color: {IRC_12};\">")
	text = text.replace("\x0313",f"<{html_tag} style=\"color: {IRC_13};\">")
	text = text.replace("\x0314",f"<{html_tag} style=\"color: {IRC_14};\">")
	text = text.replace("\x0315",f"<{html_tag} style=\"color: {IRC_15};\">")

	text = text.replace("\x0300",f"<{html_tag} style=\"color: {IRC_00};\">")
	text = text.replace("\x0301",f"<{html_tag} style=\"color: {IRC_01};\">")
	text = text.replace("\x0302",f"<{html_tag} style=\"color: {IRC_02};\">")
	text = text.replace("\x0303",f"<{html_tag} style=\"color: {IRC_03};\">")
	text = text.replace("\x0304",f"<{html_tag} style=\"color: {IRC_04};\">")
	text = text.replace("\x0305",f"<{html_tag} style=\"color: {IRC_05};\">")
	text = text.replace("\x0306",f"<{html_tag} style=\"color: {IRC_06};\">")
	text = text.replace("\x0307",f"<{html_tag} style=\"color: {IRC_07};\">")
	text = text.replace("\x0308",f"<{html_tag} style=\"color: {IRC_08};\">")
	text = text.replace("\x0309",f"<{html_tag} style=\"color: {IRC_09};\">")

	text = text.replace("\x030",f"<{html_tag} style=\"color: {IRC_00};\">")
	text = text.replace("\x031",f"<{html_tag} style=\"color: {IRC_01};\">")
	text = text.replace("\x032",f"<{html_tag} style=\"color: {IRC_02};\">")
	text = text.replace("\x033",f"<{html_tag} style=\"color: {IRC_03};\">")
	text = text.replace("\x034",f"<{html_tag} style=\"color: {IRC_04};\">")
	text = text.replace("\x035",f"<{html_tag} style=\"color: {IRC_05};\">")
	text = text.replace("\x036",f"<{html_tag} style=\"color: {IRC_06};\">")
	text = text.replace("\x037",f"<{html_tag} style=\"color: {IRC_07};\">")
	text = text.replace("\x038",f"<{html_tag} style=\"color: {IRC_08};\">")
	text = text.replace("\x039",f"<{html_tag} style=\"color: {IRC_09};\">")

	text = text.replace("\x03",f"</{html_tag}>")

	# # close font tags
	# if f"<{html_tag} style=" in text:
	# 	if not f"</{html_tag}>" in text: text = text + f"</{html_tag}>"

	# out = []
	# indiv = False
	# for w in text.split(' '):

	# 	if indiv:
	# 		if w==f"<{html_tag}":
	# 			out.append(f"</{html_tag}>")

	# 	if w==f"<{html_tag}": indiv = True
	# 	if w==f"</{html_tag}>": indiv = False

	# 	out.append(w)

	# text = ' '.join(out)

	# close font tags
	if f"<{html_tag} style=" in text:
		if not f"</{html_tag}>" in text: text = text + f"</{html_tag}>"

	out = []
	indiv = False
	for w in text.split(' '):

		if indiv:
			if w==f"<{html_tag}":
				out.append(f"</{html_tag}>")

		if w==f"<{html_tag}": indiv = True
		if w==f"</{html_tag}>": indiv = False

		out.append(w)

	text = ' '.join(out)

	return text

def strip_color(text):

	html_tag = "font"

	combos = list(combinations(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	combos = list(combinations(["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	text = text.replace("\x0310","")
	text = text.replace("\x0311","")
	text = text.replace("\x0312","")
	text = text.replace("\x0313","")
	text = text.replace("\x0314","")
	text = text.replace("\x0315","")

	text = text.replace("\x0300","")
	text = text.replace("\x0301","")
	text = text.replace("\x0302","")
	text = text.replace("\x0303","")
	text = text.replace("\x0304","")
	text = text.replace("\x0305","")
	text = text.replace("\x0306","")
	text = text.replace("\x0307","")
	text = text.replace("\x0308","")
	text = text.replace("\x0309","")

	text = text.replace("\x030","")
	text = text.replace("\x031","")
	text = text.replace("\x032","")
	text = text.replace("\x033","")
	text = text.replace("\x034","")
	text = text.replace("\x035","")
	text = text.replace("\x036","")
	text = text.replace("\x037","")
	text = text.replace("\x038","")
	text = text.replace("\x039","")

	text = text.replace("\x03","")

	text = text.replace("\x02","")
	text = text.replace("\x1D","")
	text = text.replace("\x1F","")
	text = text.replace("\x0F","")

	return text
