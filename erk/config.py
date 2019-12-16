
import os
import json
from erk.files import SETTINGS_FILE

SERVER_WINDOW = 1
CHANNEL_WINDOW = 2
PRIVATE_WINDOW = 3

CHAT_WINDOW_WIDGET_SPACING = 5
SAVE_JOINED_CHANNELS = False

# Settings changable in the UI
HISTORY_LENGTH = 20
DEFAULT_APP_WIDTH = 800
DEFAULT_APP_HEIGHT = 600
GET_HOSTMASKS_ON_CHANNEL_JOIN = True
SPELLCHECK_INPUT = True
SPELLCHECK_LANGUAGE = "en"
OPEN_NEW_PRIVATE_MESSAGE_WINDOWS = True
NICK_DISPLAY_WIDTH = 15
DISPLAY_TIMESTAMP = True
USE_24HOUR_CLOCK_FOR_TIMESTAMPS = True
DISPLAY_IRC_COLORS = True
CONVERT_URLS_TO_LINKS = True
DOUBLECLICK_SWITCH = False
DISPLAY_FONT = ''
DISPLAY_CONNECTION_UPTIME = False
CONNECTION_DISPLAY_LOCATION = "left"
CONNECTION_DISPLAY_MOVE = False
CONNECTION_DISPLAY_VISIBLE = True
DISPLAY_CHANNEL_MODES = False
SWITCH_TO_NEW_WINDOWS = True
AUTOCOMPLETE_NICKNAMES = True
AUTOCOMPLETE_COMMANDS = True
SPELLCHECK_IGNORE_NICKS = True
USE_EMOJIS = True
USE_ASCIIMOJIS = True
AUTOCOMPLETE_EMOJI = True
AUTOCOMPLETE_ASCIIMOJI = True
FILTER_PROFANITY = False
PLAIN_USER_LISTS = False
DISPLAY_CHANNEL_STATUS_NICK_DISPLAY = True
DISPLAY_NICKNAME_ON_CHANNEL = True
EXPAND_SERVER_ON_CONNECT = True
TRACK_COMMAND_HISTORY = True

SAVE_CHANNEL_LOGS = True
LOAD_CHANNEL_LOGS = True
CHANNEL_LOG_LOAD_SIZE_MAX = 500
MARK_END_OF_LOADED_LOG = True
DISPLAY_CHAT_RESUME_DATE_TIME = True

def save_settings(filename=SETTINGS_FILE):

	settings = {
		"command_history_length": HISTORY_LENGTH,
		"chat_display_widget_spacing": CHAT_WINDOW_WIDGET_SPACING,
		"get_hostmasks_on_channel_join": GET_HOSTMASKS_ON_CHANNEL_JOIN,
		"save_joined_channels": SAVE_JOINED_CHANNELS,
		"starting_app_width": DEFAULT_APP_WIDTH,
		"starting_app_height": DEFAULT_APP_HEIGHT,
		"spellcheck_input": SPELLCHECK_INPUT,
		"spellcheck_language": SPELLCHECK_LANGUAGE,
		"open_window_for_new_private_messages": OPEN_NEW_PRIVATE_MESSAGE_WINDOWS,
		"minimum_nickname_display_width": NICK_DISPLAY_WIDTH,
		"show_timestamps": DISPLAY_TIMESTAMP,
		"use_24hour_clock_for_timestamps": USE_24HOUR_CLOCK_FOR_TIMESTAMPS,
		"display_irc_color_codes": DISPLAY_IRC_COLORS,
		"convert_urls_in_messages_to_links": CONVERT_URLS_TO_LINKS,
		"doubleclick_to_switch_chat_windows": DOUBLECLICK_SWITCH,
		"font": DISPLAY_FONT,
		"display_connection_uptime": DISPLAY_CONNECTION_UPTIME,
		"connection_display_location": CONNECTION_DISPLAY_LOCATION,
		"is_connection_display_moveable": CONNECTION_DISPLAY_MOVE,
		"connection_display_visible": CONNECTION_DISPLAY_VISIBLE,
		"display_channel_modes": DISPLAY_CHANNEL_MODES,
		"switch_to_new_chats": SWITCH_TO_NEW_WINDOWS,
		"autocomplete_nicknames": AUTOCOMPLETE_NICKNAMES,
		"autocomplete_commands": AUTOCOMPLETE_COMMANDS,
		"spellcheck_ignore_nicknames": SPELLCHECK_IGNORE_NICKS,
		"use_emoji_shortcodes": USE_EMOJIS,
		"use_asciimoji_shortcodes": USE_ASCIIMOJIS,
		"autocomplete_emoji": AUTOCOMPLETE_EMOJI,
		"autocomplete_asciimoji": AUTOCOMPLETE_ASCIIMOJI,
		"filter_profanity": FILTER_PROFANITY,
		"text_only_channel_user_lists": PLAIN_USER_LISTS,
		"display_channel_status": DISPLAY_CHANNEL_STATUS_NICK_DISPLAY,
		"display_nickname_on_channels": DISPLAY_NICKNAME_ON_CHANNEL,
		"expand_server_node_on_connection": EXPAND_SERVER_ON_CONNECT,
		"enable_command_history": TRACK_COMMAND_HISTORY,
		"save_channel_logs": SAVE_CHANNEL_LOGS,
		"load_channel_logs": LOAD_CHANNEL_LOGS,
		"maximum_channel_log_display_size": CHANNEL_LOG_LOAD_SIZE_MAX,
		"mark_end_of_loaded_log": MARK_END_OF_LOADED_LOG,
		"display_date_and_time_of_channel_log_resume": DISPLAY_CHAT_RESUME_DATE_TIME,
	}

	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def load_settings(filename=SETTINGS_FILE):
	global HISTORY_LENGTH
	global CHAT_WINDOW_WIDGET_SPACING
	global GET_HOSTMASKS_ON_CHANNEL_JOIN
	global SAVE_JOINED_CHANNELS
	global SPELLCHECK_INPUT
	global DEFAULT_APP_WIDTH
	global DEFAULT_APP_HEIGHT
	global SPELLCHECK_LANGUAGE
	global OPEN_NEW_PRIVATE_MESSAGE_WINDOWS
	global NICK_DISPLAY_WIDTH
	global DISPLAY_TIMESTAMP
	global USE_24HOUR_CLOCK_FOR_TIMESTAMPS
	global DISPLAY_IRC_COLORS
	global CONVERT_URLS_TO_LINKS
	global DOUBLECLICK_SWITCH
	global DISPLAY_FONT
	global DISPLAY_CONNECTION_UPTIME
	global CONNECTION_DISPLAY_LOCATION
	global CONNECTION_DISPLAY_MOVE
	global CONNECTION_DISPLAY_VISIBLE
	global DISPLAY_CHANNEL_MODES
	global SWITCH_TO_NEW_WINDOWS
	global AUTOCOMPLETE_NICKNAMES
	global AUTOCOMPLETE_COMMANDS
	global SPELLCHECK_IGNORE_NICKS
	global USE_EMOJIS
	global USE_ASCIIMOJIS
	global AUTOCOMPLETE_EMOJI
	global AUTOCOMPLETE_ASCIIMOJI
	global FILTER_PROFANITY
	global PLAIN_USER_LISTS
	global DISPLAY_CHANNEL_STATUS_NICK_DISPLAY
	global DISPLAY_NICKNAME_ON_CHANNEL
	global EXPAND_SERVER_ON_CONNECT
	global TRACK_COMMAND_HISTORY
	global SAVE_CHANNEL_LOGS
	global LOAD_CHANNEL_LOGS
	global CHANNEL_LOG_LOAD_SIZE_MAX
	global MARK_END_OF_LOADED_LOG
	global DISPLAY_CHAT_RESUME_DATE_TIME

	# Load in settings if the settings file exists...
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)
			HISTORY_LENGTH = data["command_history_length"]
			CHAT_WINDOW_WIDGET_SPACING = data["chat_display_widget_spacing"]
			GET_HOSTMASKS_ON_CHANNEL_JOIN = data["get_hostmasks_on_channel_join"]
			SAVE_JOINED_CHANNELS = data["save_joined_channels"]
			SPELLCHECK_INPUT = data["spellcheck_input"]
			DEFAULT_APP_WIDTH = data["starting_app_width"]
			DEFAULT_APP_HEIGHT = data["starting_app_height"]
			SPELLCHECK_LANGUAGE = data["spellcheck_language"]
			OPEN_NEW_PRIVATE_MESSAGE_WINDOWS = data["open_window_for_new_private_messages"]
			NICK_DISPLAY_WIDTH = data["minimum_nickname_display_width"]
			DISPLAY_TIMESTAMP = data["show_timestamps"]
			USE_24HOUR_CLOCK_FOR_TIMESTAMPS = data["use_24hour_clock_for_timestamps"]
			DISPLAY_IRC_COLORS = data["display_irc_color_codes"]
			CONVERT_URLS_TO_LINKS = data["convert_urls_in_messages_to_links"]
			DOUBLECLICK_SWITCH = data["doubleclick_to_switch_chat_windows"]
			DISPLAY_FONT = data["font"]
			DISPLAY_CONNECTION_UPTIME = data["display_connection_uptime"]
			CONNECTION_DISPLAY_LOCATION = data["connection_display_location"]
			CONNECTION_DISPLAY_MOVE = data["is_connection_display_moveable"]
			CONNECTION_DISPLAY_VISIBLE = data["connection_display_visible"]
			DISPLAY_CHANNEL_MODES = data["display_channel_modes"]
			SWITCH_TO_NEW_WINDOWS = data["switch_to_new_chats"]
			AUTOCOMPLETE_NICKNAMES = data["autocomplete_nicknames"]
			AUTOCOMPLETE_COMMANDS = data["autocomplete_commands"]
			SPELLCHECK_IGNORE_NICKS = data["spellcheck_ignore_nicknames"]
			USE_EMOJIS = data["use_emoji_shortcodes"]
			USE_ASCIIMOJIS = data["use_asciimoji_shortcodes"]
			AUTOCOMPLETE_EMOJI = data["autocomplete_emoji"]
			AUTOCOMPLETE_ASCIIMOJI = data["autocomplete_asciimoji"]
			FILTER_PROFANITY = data["filter_profanity"]
			PLAIN_USER_LISTS = data["text_only_channel_user_lists"]
			DISPLAY_CHANNEL_STATUS_NICK_DISPLAY = data["display_channel_status"]
			DISPLAY_NICKNAME_ON_CHANNEL = data["display_nickname_on_channels"]
			EXPAND_SERVER_ON_CONNECT = data["expand_server_node_on_connection"]
			TRACK_COMMAND_HISTORY = data["enable_command_history"]
			SAVE_CHANNEL_LOGS = data["save_channel_logs"]
			LOAD_CHANNEL_LOGS = data["load_channel_logs"]
			CHANNEL_LOG_LOAD_SIZE_MAX = data["maximum_channel_log_display_size"]
			MARK_END_OF_LOADED_LOG = data["mark_end_of_loaded_log"]
			DISPLAY_CHAT_RESUME_DATE_TIME = data["display_date_and_time_of_channel_log_resume"]

	# ...or create the file with defaults if the settings
	# file doesn't exist
	else:
		save_settings(filename)
