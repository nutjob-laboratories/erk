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

DEFAULT_NICKNAME = "erk_user"
DEFAULT_ALTERNATIVE = "3rk_us3r"
DEFAULT_USERNAME = "erk_user"
DEFAULT_IRCNAME = "Erk IRC Client"

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

NETWORK_FILE = os.path.join(DATA_DIRECTORY, "servers.txt")
ASCIIEMOJI_LIST = os.path.join(DATA_DIRECTORY, "asciiemoji.json")
PROFANITY_LIST = os.path.join(DATA_DIRECTORY, "profanity.txt")

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

UNKNOWN_IRC_NETWORK = "Unknown"

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
			SETTING_CHAT_STATUS_BARS: False,
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
	if gui.convert_links_in_chat: message = inject_www_links(message,gui.styles["hyperlink"])

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
	if gui.convert_links_in_chat: message = inject_www_links(message,gui.styles["hyperlink"])

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
	if not "notice" in data: data["notice"] = NOTICE_STYLE
	if not "username" in data: data["username"] = USERNAME_STYLE
	if not "message" in data: data["message"] = MESSAGE_STYLE
	if not "system" in data: data["system"] = SYSTEM_STYLE
	if not "self" in data: data["self"] = SELF_STYLE
	if not "action" in data: data["action"] = ACTION_STYLE
	if not "timestamp" in data: data["timestamp"] = TIMESTAMP_STYLE
	if not "resume" in data: data["resume"] = RESUME_STYLE
	if not "hyperlink" in data: data["hyperlink"] = HYPERLINK_STYLE
	if not "base" in data: data["base"] = BASE_STYLE
	if not "error" in data: data["error"] = ERROR_STYLE
	if not "whois" in data: data["whois"] = WHOIS_STYLE
	if not "whois-text" in data: data["whois-text"] = WHOIS_TEXT_STYLE
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
			"timestamp": TIMESTAMP_STYLE,
			"username": USERNAME_STYLE,
			"message": MESSAGE_STYLE,
			"system": SYSTEM_STYLE,
			"self": SELF_STYLE,
			"action": ACTION_STYLE,
			"notice": NOTICE_STYLE,
			"resume": RESUME_STYLE,
			"hyperlink": HYPERLINK_STYLE,
			"base": BASE_STYLE,
			"error": ERROR_STYLE,
			"whois": WHOIS_STYLE,
			"whois-text": WHOIS_TEXT_STYLE,
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