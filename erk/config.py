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

import os
import json
from erk.files import SETTINGS_FILE

SERVER_WINDOW = 1
CHANNEL_WINDOW = 2
PRIVATE_WINDOW = 3

CHAT_WINDOW_WIDGET_SPACING = 5
SAVE_JOINED_CHANNELS = False

DISABLE_CONNECT_COMMANDS = False

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
AUTOCOMPLETE_EMOJI = True
FILTER_PROFANITY = False
PLAIN_USER_LISTS = False
DISPLAY_CHANNEL_STATUS_NICK_DISPLAY = True
DISPLAY_NICKNAME_ON_CHANNEL = True
EXPAND_SERVER_ON_CONNECT = True
TRACK_COMMAND_HISTORY = True
SAVE_CHANNEL_LOGS = True
LOAD_CHANNEL_LOGS = True
LOG_LOAD_SIZE_MAX = 300
MARK_END_OF_LOADED_LOG = True
DISPLAY_CHAT_RESUME_DATE_TIME = True
SAVE_PRIVATE_LOGS = False
LOAD_PRIVATE_LOGS = False
MARK_SYSTEM_MESSAGES_WITH_SYMBOL = True
PLUGINS_ENABLED = True
MACROS_ENABLED = True
DEVELOPER_MODE = False
USE_SPACES_FOR_INDENT = True
NUMBER_OF_SPACES_FOR_INDENT = 4
EDITOR_WORD_WRAP = False
ALWAYS_ON_TOP = False
SHOW_LOAD_ERRORS = True
DISPLAY_TIMESTAMP_SECONDS = False
EDITOR_AUTO_INDENT = True
EDITOR_FONT = ''
EDITOR_STATUS_BAR = True
EDITOR_SYNTAX_HIGHLIGHT = True
EDITOR_PROMPT_FOR_SAVE_ON_EXIT = True
JOIN_ON_INVITE = False

CLICKABLE_CHANNELS = True

def save_settings(filename=SETTINGS_FILE):

	if filename==None: filename = SETTINGS_FILE

	settings = {
		"use_spaces_for_indent": USE_SPACES_FOR_INDENT,
		"number_of_indent_spaces": NUMBER_OF_SPACES_FOR_INDENT,
		"editor_word_wrap": EDITOR_WORD_WRAP,
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
		"autocomplete_emoji": AUTOCOMPLETE_EMOJI,
		"filter_profanity": FILTER_PROFANITY,
		"text_only_channel_user_lists": PLAIN_USER_LISTS,
		"display_channel_status": DISPLAY_CHANNEL_STATUS_NICK_DISPLAY,
		"display_nickname_on_channels": DISPLAY_NICKNAME_ON_CHANNEL,
		"expand_server_node_on_connection": EXPAND_SERVER_ON_CONNECT,
		"enable_command_history": TRACK_COMMAND_HISTORY,
		"save_channel_logs": SAVE_CHANNEL_LOGS,
		"load_channel_logs": LOAD_CHANNEL_LOGS,
		"maximum_log_display_size": LOG_LOAD_SIZE_MAX,
		"mark_end_of_loaded_log": MARK_END_OF_LOADED_LOG,
		"display_date_and_time_of_channel_log_resume": DISPLAY_CHAT_RESUME_DATE_TIME,
		"save_private_logs": SAVE_PRIVATE_LOGS,
		"load_private_logs": LOAD_PRIVATE_LOGS,
		"show_system_messages_prefix": MARK_SYSTEM_MESSAGES_WITH_SYMBOL,
		"enable_plugins": PLUGINS_ENABLED,
		"enable_macros": MACROS_ENABLED,
		"plugin_developement_mode": DEVELOPER_MODE,
		"always_on_top": ALWAYS_ON_TOP,
		"show_plugin_load_error": SHOW_LOAD_ERRORS,
		"show_timestamps_with_seconds": DISPLAY_TIMESTAMP_SECONDS,
		"editor_autoindent": EDITOR_AUTO_INDENT,
		"editor_font": EDITOR_FONT,
		"editor_status_bar": EDITOR_STATUS_BAR,
		"editor_syntax_highlighting": EDITOR_SYNTAX_HIGHLIGHT,
		"editor_prompt_for_save_on_exit": EDITOR_PROMPT_FOR_SAVE_ON_EXIT,
		"automatically_join_on_invite": JOIN_ON_INVITE,
		"create_links_for_channel_names": CLICKABLE_CHANNELS,
	}

	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def load_settings(filename=SETTINGS_FILE):
	if filename==None: filename = SETTINGS_FILE
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
	global AUTOCOMPLETE_EMOJI
	global FILTER_PROFANITY
	global PLAIN_USER_LISTS
	global DISPLAY_CHANNEL_STATUS_NICK_DISPLAY
	global DISPLAY_NICKNAME_ON_CHANNEL
	global EXPAND_SERVER_ON_CONNECT
	global TRACK_COMMAND_HISTORY
	global SAVE_CHANNEL_LOGS
	global LOAD_CHANNEL_LOGS
	global LOG_LOAD_SIZE_MAX
	global MARK_END_OF_LOADED_LOG
	global DISPLAY_CHAT_RESUME_DATE_TIME
	global SAVE_PRIVATE_LOGS
	global LOAD_PRIVATE_LOGS
	global MARK_SYSTEM_MESSAGES_WITH_SYMBOL
	global PLUGINS_ENABLED
	global MACROS_ENABLED
	global DEVELOPER_MODE
	global USE_SPACES_FOR_INDENT
	global NUMBER_OF_SPACES_FOR_INDENT
	global EDITOR_WORD_WRAP
	global ALWAYS_ON_TOP
	global SHOW_LOAD_ERRORS
	global DISPLAY_TIMESTAMP_SECONDS
	global EDITOR_AUTO_INDENT
	global EDITOR_FONT
	global EDITOR_STATUS_BAR
	global EDITOR_SYNTAX_HIGHLIGHT
	global EDITOR_PROMPT_FOR_SAVE_ON_EXIT
	global JOIN_ON_INVITE
	global CLICKABLE_CHANNELS

	# Load in settings if the settings file exists...
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)

			USE_SPACES_FOR_INDENT = data["use_spaces_for_indent"]
			NUMBER_OF_SPACES_FOR_INDENT = data["number_of_indent_spaces"]
			EDITOR_WORD_WRAP = data["editor_word_wrap"]
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
			AUTOCOMPLETE_EMOJI = data["autocomplete_emoji"]
			FILTER_PROFANITY = data["filter_profanity"]
			PLAIN_USER_LISTS = data["text_only_channel_user_lists"]
			DISPLAY_CHANNEL_STATUS_NICK_DISPLAY = data["display_channel_status"]
			DISPLAY_NICKNAME_ON_CHANNEL = data["display_nickname_on_channels"]
			EXPAND_SERVER_ON_CONNECT = data["expand_server_node_on_connection"]
			TRACK_COMMAND_HISTORY = data["enable_command_history"]
			SAVE_CHANNEL_LOGS = data["save_channel_logs"]
			LOAD_CHANNEL_LOGS = data["load_channel_logs"]
			LOG_LOAD_SIZE_MAX = data["maximum_log_display_size"]
			MARK_END_OF_LOADED_LOG = data["mark_end_of_loaded_log"]
			DISPLAY_CHAT_RESUME_DATE_TIME = data["display_date_and_time_of_channel_log_resume"]
			SAVE_PRIVATE_LOGS = data["save_private_logs"]
			LOAD_PRIVATE_LOGS = data["load_private_logs"]
			MARK_SYSTEM_MESSAGES_WITH_SYMBOL = data["show_system_messages_prefix"]
			PLUGINS_ENABLED = data["enable_plugins"]
			MACROS_ENABLED = data["enable_macros"]
			DEVELOPER_MODE = data["plugin_developement_mode"]
			ALWAYS_ON_TOP = data["always_on_top"]
			SHOW_LOAD_ERRORS = data["show_plugin_load_error"]
			DISPLAY_TIMESTAMP_SECONDS = data["show_timestamps_with_seconds"]
			EDITOR_AUTO_INDENT = data["editor_autoindent"]
			EDITOR_FONT = data["editor_font"]
			EDITOR_STATUS_BAR = data["editor_status_bar"]
			EDITOR_SYNTAX_HIGHLIGHT = data["editor_syntax_highlighting"]
			EDITOR_PROMPT_FOR_SAVE_ON_EXIT = data["editor_prompt_for_save_on_exit"]
			JOIN_ON_INVITE = data["automatically_join_on_invite"]
			CLICKABLE_CHANNELS = data["create_links_for_channel_names"]

	# ...or create the file with defaults if the settings
	# file doesn't exist
	else:
		save_settings(filename)
