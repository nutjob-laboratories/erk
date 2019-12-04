
import sys
import os
import json
import re
from collections import defaultdict
import string
import random
import glob

from erk.common import *

# Directories
INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")

SETTINGS_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "settings")
if not os.path.isdir(SETTINGS_DIRECTORY): os.mkdir(SETTINGS_DIRECTORY)

LOG_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "logs")
if not os.path.isdir(LOG_DIRECTORY): os.mkdir(LOG_DIRECTORY)

MACRO_DIRECTORY = os.path.join(SETTINGS_DIRECTORY, "macros")
if not os.path.isdir(MACRO_DIRECTORY): os.mkdir(MACRO_DIRECTORY)

USER_FILE = os.path.join(SETTINGS_DIRECTORY, "user.json")
TEXT_FORMAT_FILE = os.path.join(SETTINGS_DIRECTORY, "text.css")
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "settings.json")
IGNORE_FILE = os.path.join(SETTINGS_DIRECTORY, "ignored.json")

ASCIIEMOJI_LIST = os.path.join(DATA_DIRECTORY, "asciiemoji.json")
PROFANITY_LIST = os.path.join(DATA_DIRECTORY, "profanity.txt")
MINOR_VERSION_FILE = os.path.join(DATA_DIRECTORY, "minor.txt")
NETWORK_FILE = os.path.join(DATA_DIRECTORY, "servers.txt")
DEFAULT_TEXT_FORMAT_FILE = os.path.join(DATA_DIRECTORY, "text.css")

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

def save_ignore(settings,filename=IGNORE_FILE):
	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def load_ignore(filename=IGNORE_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as igfile:
			data = json.load(igfile)
			return data
	else:
		return {}

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

def inject_asciiemojis(data):
	for key in ASCIIEMOJIS:
		for word in ASCIIEMOJIS[key]["words"]:
			data = data.replace("("+word+")",ASCIIEMOJIS[key]["ascii"])
	return data

def load_asciimoji_autocomplete():
	ASCIIMOJI_AUTOCOMPLETE = []
	with open(ASCIIMOJI_AUTOCOMPLETE_FILE) as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			ASCIIMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	return ASCIIMOJI_AUTOCOMPLETE

def load_emoji_autocomplete():
	EMOJI_AUTOCOMPLETE = []
	with open(EMOJI_ALIAS_AUTOCOMPLETE_FILE) as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			EMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	with open(EMOJI_AUTOCOMPLETE_FILE) as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			EMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	return EMOJI_AUTOCOMPLETE

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

SETTING_FONT = "font"
SETTING_MAX_NICK_SIZE = "maximum_display_nickname_size"
SETTING_STRIP_HTML = "strip_html_from_messages"
SETTING_IRC_COLOR = "display_irc_color_codes"
SETTING_LINKS = "automatically_turn_urls_into_hyperlinks"
SETTING_TIMESTAMPS = "display_timestamps"
SETTING_TIMESTAMP_SECONDS = "display_seconds_in_timestamps"
SETTING_TIMESTAMP_24HOUR_CLOCK = "display_timestamps_with_24hour_clocks"
SETTING_INITIAL_WINDOW_WIDTH = "initial_subwindow_width"
SETTING_INITIAL_WINDOW_HEIGHT = "initial_subwindow_height"
SETTING_FILTER_PROFANITY = "filter_profanity_from_messages"
SETTING_INJECT_EMOJIS = "use_emoji_shortcodes_in_outgoing_messages"
SETTING_INJECT_ASCIIMOJIS = "use_asciimoji_shortcodes_in_outgoing_messages"
SETTING_AUTOCOMPLETE_NICKS = "autocomplete_nicknames"
SETTING_AUTOCOMPLETE_EMOJIS = "autocomplete_emojis"
SETTING_AUTOCOMPLETE_ASCIIMOJIS = "autocomplete_asciimojis"
SETTING_AUTOCOMPLETE_COMMANDS = "autocomplete_commands"
SETTING_PLAIN_USER_LISTS = "channels_use_plain_user_lists"
SETTING_CONNECTION_DISPLAY_LOCATION = "connection_display_location"
SETTING_CONNECTION_DISPLAY_VISIBLE = "connection_display_is_visible"
SETTING_SPELLCHECK = "enable_spell_check"
SETTING_SPELLCHECK_LANGUAGE = "spell_check_language"
SETTING_MARK_UNSEEN_CHAT_IN_WINDOWS = "mark_unread_messages_in_chat_windows"
SETTING_UNSEEN_MESSAGE_DISPLAY_COLOR = "unread_message_color_in_connection_display"
SETTING_APPLICATION_TITLE_FROM_ACTIVE = "set_window_title_from_active_window"
SETTING_CREATE_PRIVATE_WINDOWS = "automatically_create_incoming_private_message_windows"
SETTING_FLASH_TASKBAR_PRIVATE = "flash_taskbar_on_unread_private_message"
SETTING_EXPAND_SERVER_ON_CONNECT = "connection_display_expand_node_on_connect"
SETTING_CLICKABLE_USERNAMES = "click_chat_usernames_for_private_window"
SETTING_DOUBLECLICK_USERNAMES = "double_click_nickname_in_userlist_for_private_window"
SETTING_DISPLAY_UPTIME_IN_CONNECTION_DISPLAY = "display_uptime_in_connection_display"
SETTING_SAVE_JOINED_CHANNELS = "save_joined_channels_to_autojoin"
SETTING_ALWAYS_ON_TOP = "application_window_always_on_top"
SETTING_DISPLAY_NICK_ON_CHANNEL_WINDOWS = "display_current_nickname_on_channel_windows"
SETTING_CLICK_NICK_FOR_NICKCHANGE = "click_channel_nickname_display_to_change_nick"
SETTING_SAVE_HISTORY = "save_connection_history"
SETTING_NOTIFY_FAIL = "notify_user_of_failed_connections"
SETTING_NOTIFY_LOST = "notify_user_of_lost_connections"
SETTING_SAVE_CHANNEL_LOGS = "save_channel_logs"
SETTING_LOAD_CHANNEL_LOGS = "load_channel_logs"
SETTING_SAVE_SERVER_LOGS = "save_console_logs"
SETTING_LOAD_SERVER_LOGS = "load_console_logs"
SETTING_SAVE_PRIVATE_LOGS = "save_private_message_logs"
SETTING_LOAD_PRIVATE_LOGS = "load_private_message_logs"
SETTING_LOAD_LOG_MAX_SIZE = "maximum_lines_displayed_from_saved_logs"
SETTING_MARK_END_OF_LOADED_LOGS = "mark_end_of_loaded_logs"
SETTING_FETCH_HOSTMASKS = "retrieve_hostmasks_on_join_if_needed"
SETTING_MAX_LINES_IN_IO = "maximum_number_of_lines_displayed_in_io_window"
SETTING_SHOW_NET_TRAFFIC_FROM_CONNECTION = "io_window_shows_traffic_starting_at_connection"
SETTING_CHANNEL_WINDOW_MODES = "show_mode_menu_in_channel_windows"
SETTING_CHANNEL_WINDOW_BANS = "show_bans_menu_in_channel_windows"
SETTING_CMD_HISTORY = "input_command_history"
SETTING_CMG_HISTORY_LENGTH = "maximum_size_of_input_command_history"
SETTING_CHANNEL_IGNORE_JOIN = "channels_do_not_display_join_messages"
SETTING_CHANNEL_IGNORE_PART = "channels_do_not_display_part_messages"
SETTING_CHANNEL_IGNORE_RENAME = "channels_do_not_display_rename_messages"
SETTING_CHANNEL_IGNORE_TOPIC = "channels_do_not_display_topic_messages"
SETTING_CHANNEL_IGNORE_MODE = "channels_do_not_display_mode_messages"

SETTING_SAVE_IGNORE = "save_ignore_data_to_file"

def patch_config_file(data):
	s = len(data)
	if not SETTING_FONT in data: data[SETTING_FONT] = ""
	if not SETTING_MAX_NICK_SIZE in data: data[SETTING_MAX_NICK_SIZE] = 16
	if not SETTING_STRIP_HTML in data: data[SETTING_STRIP_HTML] = True
	if not SETTING_IRC_COLOR in data: data[SETTING_IRC_COLOR] = True
	if not SETTING_LINKS in data: data[SETTING_LINKS] = True
	if not SETTING_TIMESTAMPS in data: data[SETTING_TIMESTAMPS] = True
	if not SETTING_TIMESTAMP_SECONDS in data: data[SETTING_TIMESTAMP_SECONDS] = False
	if not SETTING_TIMESTAMP_24HOUR_CLOCK in data: data[SETTING_TIMESTAMP_24HOUR_CLOCK] = True
	if not SETTING_INITIAL_WINDOW_WIDTH in data: data[SETTING_INITIAL_WINDOW_WIDTH] = 500
	if not SETTING_INITIAL_WINDOW_HEIGHT in data: data[SETTING_INITIAL_WINDOW_HEIGHT] = 300
	if not SETTING_FILTER_PROFANITY in data: data[SETTING_FILTER_PROFANITY] = False
	if not SETTING_INJECT_EMOJIS in data: data[SETTING_INJECT_EMOJIS] = True
	if not SETTING_INJECT_ASCIIMOJIS in data: data[SETTING_INJECT_ASCIIMOJIS] = True
	if not SETTING_AUTOCOMPLETE_NICKS in data: data[SETTING_AUTOCOMPLETE_NICKS] = True
	if not SETTING_AUTOCOMPLETE_EMOJIS in data: data[SETTING_AUTOCOMPLETE_EMOJIS] = True
	if not SETTING_AUTOCOMPLETE_ASCIIMOJIS in data: data[SETTING_AUTOCOMPLETE_ASCIIMOJIS] = True
	if not SETTING_AUTOCOMPLETE_COMMANDS in data: data[SETTING_AUTOCOMPLETE_COMMANDS] = True
	if not SETTING_PLAIN_USER_LISTS in data: data[SETTING_PLAIN_USER_LISTS] = False
	if not SETTING_CONNECTION_DISPLAY_LOCATION in data: data[SETTING_CONNECTION_DISPLAY_LOCATION] = "left"
	if not SETTING_CONNECTION_DISPLAY_VISIBLE in data: data[SETTING_CONNECTION_DISPLAY_VISIBLE] = True
	if not SETTING_SPELLCHECK in data: data[SETTING_SPELLCHECK] = True
	if not SETTING_SPELLCHECK_LANGUAGE in data: data[SETTING_SPELLCHECK_LANGUAGE] = "en"
	if not SETTING_MARK_UNSEEN_CHAT_IN_WINDOWS in data: data[SETTING_MARK_UNSEEN_CHAT_IN_WINDOWS] = True
	if not SETTING_UNSEEN_MESSAGE_DISPLAY_COLOR in data: data[SETTING_UNSEEN_MESSAGE_DISPLAY_COLOR] = "#FF0000"
	if not SETTING_APPLICATION_TITLE_FROM_ACTIVE in data: data[SETTING_APPLICATION_TITLE_FROM_ACTIVE] = True
	if not SETTING_CREATE_PRIVATE_WINDOWS in data: data[SETTING_CREATE_PRIVATE_WINDOWS] = True
	if not SETTING_FLASH_TASKBAR_PRIVATE in data: data[SETTING_FLASH_TASKBAR_PRIVATE] = True
	if not SETTING_EXPAND_SERVER_ON_CONNECT in data: data[SETTING_EXPAND_SERVER_ON_CONNECT] = True
	if not SETTING_CLICKABLE_USERNAMES in data: data[SETTING_CLICKABLE_USERNAMES] = True
	if not SETTING_DOUBLECLICK_USERNAMES in data: data[SETTING_DOUBLECLICK_USERNAMES] = True
	if not SETTING_DISPLAY_UPTIME_IN_CONNECTION_DISPLAY in data: data[SETTING_DISPLAY_UPTIME_IN_CONNECTION_DISPLAY] = False
	if not SETTING_SAVE_JOINED_CHANNELS in data: data[SETTING_SAVE_JOINED_CHANNELS] = False
	if not SETTING_ALWAYS_ON_TOP in data: data[SETTING_ALWAYS_ON_TOP] = False
	if not SETTING_DISPLAY_NICK_ON_CHANNEL_WINDOWS in data: data[SETTING_DISPLAY_NICK_ON_CHANNEL_WINDOWS] = True
	if not SETTING_CLICK_NICK_FOR_NICKCHANGE in data: data[SETTING_CLICK_NICK_FOR_NICKCHANGE] = True
	if not SETTING_SAVE_HISTORY in data: data[SETTING_SAVE_HISTORY] = True
	if not SETTING_NOTIFY_FAIL in data: data[SETTING_NOTIFY_FAIL] = True
	if not SETTING_NOTIFY_LOST in data: data[SETTING_NOTIFY_LOST] = True
	if not SETTING_SAVE_CHANNEL_LOGS in data: data[SETTING_SAVE_CHANNEL_LOGS] = False
	if not SETTING_LOAD_CHANNEL_LOGS in data: data[SETTING_LOAD_CHANNEL_LOGS] = False
	if not SETTING_SAVE_SERVER_LOGS in data: data[SETTING_SAVE_SERVER_LOGS] = False
	if not SETTING_LOAD_SERVER_LOGS in data: data[SETTING_LOAD_SERVER_LOGS] = False
	if not SETTING_SAVE_PRIVATE_LOGS in data: data[SETTING_SAVE_PRIVATE_LOGS] = False
	if not SETTING_LOAD_PRIVATE_LOGS in data: data[SETTING_LOAD_PRIVATE_LOGS] = False
	if not SETTING_LOAD_LOG_MAX_SIZE in data: data[SETTING_LOAD_LOG_MAX_SIZE] = 500
	if not SETTING_MARK_END_OF_LOADED_LOGS in data: data[SETTING_MARK_END_OF_LOADED_LOGS] = True
	if not SETTING_FETCH_HOSTMASKS in data: data[SETTING_FETCH_HOSTMASKS] = True
	if not SETTING_MAX_LINES_IN_IO in data: data[SETTING_MAX_LINES_IN_IO] = 500
	if not SETTING_SHOW_NET_TRAFFIC_FROM_CONNECTION in data: data[SETTING_SHOW_NET_TRAFFIC_FROM_CONNECTION] = False
	if not SETTING_CHANNEL_WINDOW_MODES in data: data[SETTING_CHANNEL_WINDOW_MODES] = True
	if not SETTING_CHANNEL_WINDOW_BANS in data: data[SETTING_CHANNEL_WINDOW_BANS] = True
	if not SETTING_CMD_HISTORY in data: data[SETTING_CMD_HISTORY] = True
	if not SETTING_CMG_HISTORY_LENGTH in data: data[SETTING_CMG_HISTORY_LENGTH] = 20
	if not SETTING_CHANNEL_IGNORE_JOIN in data: data[SETTING_CHANNEL_IGNORE_JOIN] = False
	if not SETTING_CHANNEL_IGNORE_PART in data: data[SETTING_CHANNEL_IGNORE_PART] = False
	if not SETTING_CHANNEL_IGNORE_RENAME in data: data[SETTING_CHANNEL_IGNORE_RENAME] = False
	if not SETTING_CHANNEL_IGNORE_TOPIC in data: data[SETTING_CHANNEL_IGNORE_TOPIC] = False
	if not SETTING_CHANNEL_IGNORE_MODE in data: data[SETTING_CHANNEL_IGNORE_MODE] = False
	if not SETTING_SAVE_IGNORE in data: data[SETTING_SAVE_IGNORE] = True

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
			SETTING_FONT: "",
			SETTING_MAX_NICK_SIZE: 16,
			SETTING_STRIP_HTML: True,
			SETTING_IRC_COLOR: True,
			SETTING_LINKS: True,
			SETTING_TIMESTAMPS: True,
			SETTING_TIMESTAMP_SECONDS: False,
			SETTING_TIMESTAMP_24HOUR_CLOCK: True,
			SETTING_INITIAL_WINDOW_WIDTH: 500,
			SETTING_INITIAL_WINDOW_HEIGHT: 300,
			SETTING_FILTER_PROFANITY: False,
			SETTING_INJECT_EMOJIS: True,
			SETTING_INJECT_ASCIIMOJIS: True,
			SETTING_AUTOCOMPLETE_NICKS: True,
			SETTING_AUTOCOMPLETE_EMOJIS: True,
			SETTING_AUTOCOMPLETE_ASCIIMOJIS: True,
			SETTING_AUTOCOMPLETE_COMMANDS: True,
			SETTING_PLAIN_USER_LISTS: False,
			SETTING_CONNECTION_DISPLAY_LOCATION: "left",
			SETTING_CONNECTION_DISPLAY_VISIBLE: True,
			SETTING_SPELLCHECK: True,
			SETTING_SPELLCHECK_LANGUAGE: "en",
			SETTING_MARK_UNSEEN_CHAT_IN_WINDOWS: True,
			SETTING_UNSEEN_MESSAGE_DISPLAY_COLOR: "#FF0000",
			SETTING_APPLICATION_TITLE_FROM_ACTIVE: True,
			SETTING_CREATE_PRIVATE_WINDOWS: True,
			SETTING_FLASH_TASKBAR_PRIVATE: True,
			SETTING_EXPAND_SERVER_ON_CONNECT: True,
			SETTING_CLICKABLE_USERNAMES: True,
			SETTING_DOUBLECLICK_USERNAMES: True,
			SETTING_DISPLAY_UPTIME_IN_CONNECTION_DISPLAY: False,
			SETTING_SAVE_JOINED_CHANNELS: False,
			SETTING_ALWAYS_ON_TOP: False,
			SETTING_DISPLAY_NICK_ON_CHANNEL_WINDOWS: True,
			SETTING_CLICK_NICK_FOR_NICKCHANGE: True,
			SETTING_SAVE_HISTORY: True,
			SETTING_NOTIFY_LOST: True,
			SETTING_NOTIFY_FAIL: True,
			SETTING_SAVE_CHANNEL_LOGS: False,
			SETTING_LOAD_CHANNEL_LOGS: False,
			SETTING_SAVE_SERVER_LOGS: False,
			SETTING_LOAD_SERVER_LOGS: False,
			SETTING_SAVE_PRIVATE_LOGS: False,
			SETTING_LOAD_PRIVATE_LOGS: False,
			SETTING_LOAD_LOG_MAX_SIZE: 500,
			SETTING_MARK_END_OF_LOADED_LOGS: True,
			SETTING_FETCH_HOSTMASKS: True,
			SETTING_MAX_LINES_IN_IO: 500,
			SETTING_SHOW_NET_TRAFFIC_FROM_CONNECTION: False,
			SETTING_CHANNEL_WINDOW_MODES: True,
			SETTING_CHANNEL_WINDOW_BANS: True,
			SETTING_CMD_HISTORY: True,
			SETTING_CMG_HISTORY_LENGTH: 20,
			SETTING_CHANNEL_IGNORE_JOIN: False,
			SETTING_CHANNEL_IGNORE_PART: False,
			SETTING_CHANNEL_IGNORE_RENAME: False,
			SETTING_CHANNEL_IGNORE_TOPIC: False,
			SETTING_CHANNEL_IGNORE_MODE: False,
			SETTING_SAVE_IGNORE: True,
		}
		save_settings(si)
		return si

def save_settings(settings,filename=SETTINGS_FILE):
	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def is_in_network_list(host,port,filename=NETWORK_FILE):
	for e in get_network_list(filename):
		if e[0]==host:
			if e[1]==str(port): return True
	return False

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

def update_user_history_network(host,port,network,filename=USER_FILE):
	u = get_user(filename)
	history = u["history"]
	edited = []
	for entry in history:
		if entry[0]==host:
			if entry[1]==str(port):
				if entry[2]=="Unknown":
					entry[2] = network
				else:
					return
		edited.append(entry)
	u["history"] = edited
	save_user(u,filename)

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
			"last_server": '',
			"last_port": "6667",
			"last_password": '',
			"channels": [],
			"ssl": False,
			"reconnect": False,
			"autojoin": False,
			"visited": [],
			"history": [],
		}
		return si

def save_user(user,filename=USER_FILE):
	with open(filename, "w") as write_data:
		json.dump(user, write_data, indent=4, sort_keys=True)


USERNAME_STYLE_NAME		= "username"
MESSAGE_STYLE_NAME		= "message"
SYSTEM_STYLE_NAME		= "system"
SELF_STYLE_NAME			= "self"
ACTION_STYLE_NAME		= "action"
NOTICE_STYLE_NAME		= "notice"
HYPERLINK_STYLE_NAME	= "hyperlink"
BASE_STYLE_NAME			= "all"
ERROR_STYLE_NAME		= "error"
TIMESTAMP_STYLE_NAME	= "timestamp"
MOTD_STYLE_NAME			= "motd"

USERNAME_STYLE = "font-weight: bold; color: blue;"
MESSAGE_STYLE = ""
SYSTEM_STYLE = "font-style: italic; font-weight: bold; color: orange;"
SELF_STYLE = "font-weight: bold; color: red;"
ACTION_STYLE = "font-style: italic; font-weight: bold; color: green;"
NOTICE_STYLE = "font-weight: bold; color: purple;"
HYPERLINK_STYLE = "text-decoration: underline; font-weight: bold; color: blue;"
BASE_STYLE = 'background-color: white; color: black;'
ERROR_STYLE = "font-style: italic; font-weight: bold; color: red;"
TIMESTAMP_STYLE = "font-weight: bold;"
MOTD_STYLE = "font-weight: bold; color: blue;"

def get_text_format_settings(filename=TEXT_FORMAT_FILE):
	if os.path.isfile(filename):
		data = read_style_file(filename)
		patched,data = patch_text_format_settings(data)
		if patched: write_style_file(data,filename)
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
			HYPERLINK_STYLE_NAME: HYPERLINK_STYLE,
			BASE_STYLE_NAME: BASE_STYLE,
			ERROR_STYLE_NAME: ERROR_STYLE,
			MOTD_STYLE_NAME: MOTD_STYLE,
		}
		write_style_file(si,filename)
		return si

def patch_text_format_settings(data):
	s = len(data)
	if not NOTICE_STYLE_NAME in data: data[NOTICE_STYLE_NAME] = NOTICE_STYLE
	if not USERNAME_STYLE_NAME in data: data[USERNAME_STYLE_NAME] = USERNAME_STYLE
	if not MESSAGE_STYLE_NAME in data: data[MESSAGE_STYLE_NAME] = MESSAGE_STYLE
	if not SYSTEM_STYLE_NAME in data: data[SYSTEM_STYLE_NAME] = SYSTEM_STYLE
	if not SELF_STYLE_NAME in data: data[SELF_STYLE_NAME] = SELF_STYLE
	if not ACTION_STYLE_NAME in data: data[ACTION_STYLE_NAME] = ACTION_STYLE
	if not TIMESTAMP_STYLE_NAME in data: data[TIMESTAMP_STYLE_NAME] = TIMESTAMP_STYLE
	if not HYPERLINK_STYLE_NAME in data: data[HYPERLINK_STYLE_NAME] = HYPERLINK_STYLE
	if not BASE_STYLE_NAME in data: data[BASE_STYLE_NAME] = BASE_STYLE
	if not ERROR_STYLE_NAME in data: data[ERROR_STYLE_NAME] = ERROR_STYLE
	if not MOTD_STYLE_NAME in data: data[MOTD_STYLE_NAME] = MOTD_STYLE
	if len(data)>s:
		return [True,data]
	else:
		return [False,data]

def write_style_file(style,filename=TEXT_FORMAT_FILE):
	output = "/*\n\tThis file uses a sub-set of CSS used by Qt called \"QSS\"\n\thttps://doc.qt.io/qt-5/stylesheet-syntax.html\n*/\n\n"

	for key in style:
		output = output + key + " {\n"
		for s in style[key].split(';'):
			s = s.strip()
			if len(s)==0: continue
			output = output + "\t" + s + ";\n"
		output = output + "}\n\n"

	f=open(filename, "w")
	f.write(output)
	f.close()

def read_style_file(filename=TEXT_FORMAT_FILE):

	# Read in the file
	f=open(filename, "r")
	text = f.read()
	f.close()

	# Strip comments
	text = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,text)

	# Tokenize the file
	buff = ''
	name = ''
	tokens = []
	inblock = False
	for char in text:
		if char=='{':
			if inblock:
				raise SyntaxError("Nested styles are forbidden")
			inblock = True
			name = buff.strip()
			buff = ''
			continue

		if char=='}':
			inblock = False
			section = [ name,buff.strip() ]
			tokens.append(section)
			buff = ''
			continue

		buff = buff + char

	# Check for an unclosed brace
	if inblock:
		raise SyntaxError("Unclosed brace")

	# Build output dict of lists
	style = defaultdict(list)
	for section in tokens:
		name = section[0]
		entry = []
		for l in section[1].split(";"):
			l = l.strip()
			if len(l)>0:
				entry.append(l)

		if name in style:
			raise SyntaxError("Styles can only be defined once")
		else:
			if len(entry)!=0:
				comp = "; ".join(entry) + ";"
				style[name] = comp
			else:
				style[name] = ''

	# Return the dict
	return style
