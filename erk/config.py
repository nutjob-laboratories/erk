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
from .files import SETTINGS_FILE

from .strings import *

SERVER_WINDOW = 1
CHANNEL_WINDOW = 2
PRIVATE_WINDOW = 3

CHAT_WINDOW_WIDGET_SPACING = 5
SAVE_JOINED_CHANNELS = False

DISABLE_CONNECT_COMMANDS = False

INPUT_COMMAND_SYMBOL = '/'

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
MARK_END_OF_LOADED_LOG = False
DISPLAY_CHAT_RESUME_DATE_TIME = True
SAVE_PRIVATE_LOGS = False
LOAD_PRIVATE_LOGS = False
MARK_SYSTEM_MESSAGES_WITH_SYMBOL = True
PLUGINS_ENABLED = True
DEVELOPER_MODE = False
USE_SPACES_FOR_INDENT = True
NUMBER_OF_SPACES_FOR_INDENT = 4
EDITOR_WORD_WRAP = False
SHOW_LOAD_ERRORS = True
DISPLAY_TIMESTAMP_SECONDS = False
EDITOR_AUTO_INDENT = True
EDITOR_FONT = ''
EDITOR_STATUS_BAR = True
EDITOR_SYNTAX_HIGHLIGHT = True
EDITOR_PROMPT_FOR_SAVE_ON_EXIT = True
JOIN_ON_INVITE = False
CLICKABLE_CHANNELS = True
CONNECTION_DISPLAY_WIDTH = None
SYSTEM_MESSAGE_PREFIX = "&diams;"
AUTOMATICALLY_FETCH_CHANNEL_LIST = True
CHANNEL_LIST_REFRESH_FREQUENCY = 3600
HIDE_MODE_DISPLAY = False
HIDE_TOPIC_MESSAGE = False
HIDE_QUIT_MESSAGE = False
HIDE_NICK_MESSAGE = False
HIDE_INVITE_MESSAGE = False
HIDE_PART_MESSAGE = False
HIDE_JOIN_MESSAGE = False
APP_TITLE_TO_CURRENT_CHAT = True
APP_TITLE_SHOW_TOPIC = False
CHAT_DISPLAY_INFO_BAR = True
DISPLAY_DATES_IN_CHANNEL_CHAT = True
SHOW_CONNECTION_LOST_ERROR = True
SHOW_CONNECTION_FAIL_ERROR = True
DISPLAY_USER_LIST = True
AUTOSAVE_LOGS = True
AUTOSAVE_LOG_TIME = 300
AUTOSAVE_CACHE_SIZE = 10
UNSEEN_MESSAGE_ANIMATION = True
UNSEEN_ANIMATION_LENGTH = 500
UNSEEN_ANIMATION_COLOR = 'system'
CONNECTION_MESSAGE_ANIMATION = True
CONNECTION_ANIMATION_LENGTH = 1000
CONNECTION_ANIMATION_COLOR = 'system'
SCHWA_ANIMATION = True
ASK_BEFORE_QUIT = True
MENU_BAR_MOVABLE = True
MENU_BAR_ORIENT = "top"
ENABLE_SCRIPTS = True
DOUBLECLICK_TO_CHANGE_NICK = True
SHOW_CONSOLE_BUTTONS = True
SCRIPT_INTERPOLATE_SYMBOL = '$'
GLOBALIZE_ALL_SCRIPT_ALIASES = True
USE_QMENUBAR_MENUS = False
ENABLE_SCRIPT_EDITOR = True

SCRIPT_SYNTAX_COMMENTS = 'darkMagenta'
SCRIPT_SYNTAX_COMMANDS = 'darkBlue'
SCRIPT_SYNTAX_TARGETS = 'darkRed'
SCRIPT_SYNTAX_ALIAS = 'darkGreen'

AUTOCOMPLETE_MACROS = True
SAVE_MACROS = True
SAVE_SCRIPT_ON_CLOSE = True
NOTIFY_SCRIPT_END = True

DEFAULT_QUIT_PART_MESSAGE = APPLICATION_NAME + " " + APPLICATION_MAJOR_VERSION + " - " + OFFICIAL_REPOSITORY_SHORT_CLEAN

def save_settings(filename=SETTINGS_FILE):

	if filename==None: filename = SETTINGS_FILE

	settings = {

		"default_quit_and_part_message": DEFAULT_QUIT_PART_MESSAGE,
		"notify_script_execution_end": NOTIFY_SCRIPT_END,
		"save_on_script_editor_close": SAVE_SCRIPT_ON_CLOSE,
		"save_macros": SAVE_MACROS,
		"autocomplete_macros": AUTOCOMPLETE_MACROS,
		"script_syntax_color_comments": SCRIPT_SYNTAX_COMMENTS,
		"script_syntax_color_commands": SCRIPT_SYNTAX_COMMANDS,
		"script_syntax_color_channels": SCRIPT_SYNTAX_TARGETS,
		"script_syntax_color_alias": SCRIPT_SYNTAX_ALIAS,
		"enable_script_editor": ENABLE_SCRIPT_EDITOR,
		"use_default_qmenubar": USE_QMENUBAR_MENUS,
		"all_script_aliases_are_global": GLOBALIZE_ALL_SCRIPT_ALIASES,
		"script_interpolation_symbol": SCRIPT_INTERPOLATE_SYMBOL,
		"display_console_buttons": SHOW_CONSOLE_BUTTONS,
		"double_click_nick_to_change_nicks": DOUBLECLICK_TO_CHANGE_NICK,
		"enable_scripts": ENABLE_SCRIPTS,
		"movable_menubar": MENU_BAR_MOVABLE,
		"menubar_location": MENU_BAR_ORIENT,
		"ask_before_quitting": ASK_BEFORE_QUIT,
		"schwa_corner_animation": SCHWA_ANIMATION,
		"animate_unseen_messages_in_connection_display": UNSEEN_MESSAGE_ANIMATION,
		"animate_connecting_messages_in_connection_display": CONNECTION_MESSAGE_ANIMATION,
		"autosave_cache_minimum_size": AUTOSAVE_CACHE_SIZE,
		"autosave_logs": AUTOSAVE_LOGS,
		"autosave_log_interval_in_seconds": AUTOSAVE_LOG_TIME,
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
		"plugin_developement_mode": DEVELOPER_MODE,
		"show_plugin_load_error": SHOW_LOAD_ERRORS,
		"show_timestamps_with_seconds": DISPLAY_TIMESTAMP_SECONDS,
		"editor_autoindent": EDITOR_AUTO_INDENT,
		"editor_font": EDITOR_FONT,
		"editor_status_bar": EDITOR_STATUS_BAR,
		"editor_syntax_highlighting": EDITOR_SYNTAX_HIGHLIGHT,
		"editor_prompt_for_save_on_exit": EDITOR_PROMPT_FOR_SAVE_ON_EXIT,
		"automatically_join_on_invite": JOIN_ON_INVITE,
		"create_links_for_channel_names": CLICKABLE_CHANNELS,
		"connection_display_width": CONNECTION_DISPLAY_WIDTH,
		"channel_list_refresh_in_seconds": CHANNEL_LIST_REFRESH_FREQUENCY,
		"system_message_prefix": SYSTEM_MESSAGE_PREFIX,
		"automatically_fetch_channel_list": AUTOMATICALLY_FETCH_CHANNEL_LIST,
		"hide_mode_messages": HIDE_MODE_DISPLAY,
		"hide_topic_messages": HIDE_TOPIC_MESSAGE,
		"hide_quit_messages": HIDE_QUIT_MESSAGE,
		"hide_nick_messages": HIDE_NICK_MESSAGE,
		"hide_invite_messages": HIDE_INVITE_MESSAGE,
		"hide_part_messages": HIDE_PART_MESSAGE,
		"hide_join_messages": HIDE_JOIN_MESSAGE,
		"set_application_title_to_current_chat_name": APP_TITLE_TO_CURRENT_CHAT,
		"show_channel_topic_in_title": APP_TITLE_SHOW_TOPIC,
		"chat_display_info_bar": CHAT_DISPLAY_INFO_BAR,
		"input_command_symbol": INPUT_COMMAND_SYMBOL,
		"display_dates_in_channel_chat": DISPLAY_DATES_IN_CHANNEL_CHAT,
		"show_connection_lost_dialog": SHOW_CONNECTION_LOST_ERROR,
		"show_connection_fail_dialog": SHOW_CONNECTION_FAIL_ERROR,
		"display_user_lists": DISPLAY_USER_LIST,
	}

	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def patch_settings(data):

	if not "default_quit_and_part_message" in data:
		data["default_quit_and_part_message"] = DEFAULT_QUIT_PART_MESSAGE

	if not "notify_script_execution_end" in data:
		data["notify_script_execution_end"] = NOTIFY_SCRIPT_END

	if not "save_on_script_editor_close" in data:
		data["save_on_script_editor_close"] = SAVE_SCRIPT_ON_CLOSE

	if not "save_macros" in data:
		data["save_macros"] = SAVE_MACROS

	if not "autocomplete_macros" in data:
		data["autocomplete_macros"] = AUTOCOMPLETE_MACROS

	if not "script_syntax_color_comments" in data:
		data["script_syntax_color_comments"] = SCRIPT_SYNTAX_COMMENTS

	if not "script_syntax_color_commands" in data:
		data["script_syntax_color_commands"] = SCRIPT_SYNTAX_COMMANDS

	if not "script_syntax_color_channels" in data:
		data["script_syntax_color_channels"] = SCRIPT_SYNTAX_TARGETS

	if not "script_syntax_color_alias" in data:
		data["script_syntax_color_alias"] = SCRIPT_SYNTAX_ALIAS

	if not "enable_script_editor" in data:
		data["enable_script_editor"] = ENABLE_SCRIPT_EDITOR

	if not "use_default_qmenubar" in data:
		data["use_default_qmenubar"] = USE_QMENUBAR_MENUS

	if not "all_script_aliases_are_global" in data:
		data["all_script_aliases_are_global"] = GLOBALIZE_ALL_SCRIPT_ALIASES

	if not "script_interpolation_symbol" in data:
		data["script_interpolation_symbol"] = SCRIPT_INTERPOLATE_SYMBOL

	if not "display_console_buttons" in data:
		data["display_console_buttons"] = SHOW_CONSOLE_BUTTONS

	if not "double_click_nick_to_change_nicks" in data:
		data["double_click_nick_to_change_nicks"] = DOUBLECLICK_TO_CHANGE_NICK

	if not "enable_scripts" in data:
		data["enable_scripts"] = ENABLE_SCRIPTS

	if not "movable_menubar" in data:
		data["movable_menubar"] = MENU_BAR_MOVABLE

	if not "menubar_location" in data:
		data["menubar_location"] = MENU_BAR_ORIENT

	if not "ask_before_quitting" in data:
		data["ask_before_quitting"] = ASK_BEFORE_QUIT

	if not "display_user_lists" in data:
		data["display_user_lists"] = DISPLAY_USER_LIST

	if not "show_connection_lost_dialog" in data:
		data["show_connection_lost_dialog"] = SHOW_CONNECTION_LOST_ERROR

	if not "show_connection_fail_dialog" in data:
		data["show_connection_fail_dialog"] = SHOW_CONNECTION_FAIL_ERROR

	if not "autosave_logs" in data:
		data["autosave_logs"] = AUTOSAVE_LOGS

	if not "autosave_log_interval_in_seconds" in data:
		data["autosave_log_interval_in_seconds"] = AUTOSAVE_LOG_TIME

	if not "autosave_cache_minimum_size" in data:
		data["autosave_cache_minimum_size"] = AUTOSAVE_CACHE_SIZE

	if not "schwa_corner_animation" in data:
		data["schwa_corner_animation"] = SCHWA_ANIMATION

	if not "animate_unseen_messages_in_connection_display" in data:
		data["animate_unseen_messages_in_connection_display"] = UNSEEN_MESSAGE_ANIMATION

	if not "animate_connecting_messages_in_connection_display" in data:
		data["animate_connecting_messages_in_connection_display"] = CONNECTION_MESSAGE_ANIMATION

	return data

def load_settings(filename=SETTINGS_FILE):
	if filename==None: filename = SETTINGS_FILE
	global SCHWA_ANIMATION
	global UNSEEN_MESSAGE_ANIMATION
	global CONNECTION_MESSAGE_ANIMATION
	global AUTOSAVE_CACHE_SIZE
	global AUTOSAVE_LOGS
	global AUTOSAVE_LOG_TIME
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
	global DEVELOPER_MODE
	global USE_SPACES_FOR_INDENT
	global NUMBER_OF_SPACES_FOR_INDENT
	global EDITOR_WORD_WRAP
	global SHOW_LOAD_ERRORS
	global DISPLAY_TIMESTAMP_SECONDS
	global EDITOR_AUTO_INDENT
	global EDITOR_FONT
	global EDITOR_STATUS_BAR
	global EDITOR_SYNTAX_HIGHLIGHT
	global EDITOR_PROMPT_FOR_SAVE_ON_EXIT
	global JOIN_ON_INVITE
	global CLICKABLE_CHANNELS
	global CONNECTION_DISPLAY_WIDTH
	global CHANNEL_LIST_REFRESH_FREQUENCY
	global SYSTEM_MESSAGE_PREFIX
	global AUTOMATICALLY_FETCH_CHANNEL_LIST
	global HIDE_MODE_DISPLAY
	global HIDE_TOPIC_MESSAGE
	global HIDE_QUIT_MESSAGE
	global HIDE_NICK_MESSAGE
	global HIDE_INVITE_MESSAGE
	global HIDE_PART_MESSAGE
	global HIDE_JOIN_MESSAGE
	global APP_TITLE_TO_CURRENT_CHAT
	global APP_TITLE_SHOW_TOPIC
	global CHAT_DISPLAY_INFO_BAR
	global INPUT_COMMAND_SYMBOL
	global DISPLAY_DATES_IN_CHANNEL_CHAT
	global SHOW_CONNECTION_LOST_ERROR
	global SHOW_CONNECTION_FAIL_ERROR
	global DISPLAY_USER_LIST
	global ASK_BEFORE_QUIT
	global MENU_BAR_MOVABLE
	global MENU_BAR_ORIENT
	global ENABLE_SCRIPTS
	global DOUBLECLICK_TO_CHANGE_NICK
	global SHOW_CONSOLE_BUTTONS
	global SCRIPT_INTERPOLATE_SYMBOL
	global GLOBALIZE_ALL_SCRIPT_ALIASES
	global USE_QMENUBAR_MENUS
	global ENABLE_SCRIPT_EDITOR
	global SCRIPT_SYNTAX_COMMENTS
	global SCRIPT_SYNTAX_COMMANDS
	global SCRIPT_SYNTAX_TARGETS
	global SCRIPT_SYNTAX_ALIAS
	global AUTOCOMPLETE_MACROS
	global SAVE_MACROS
	global SAVE_SCRIPT_ON_CLOSE
	global NOTIFY_SCRIPT_END
	global DEFAULT_QUIT_PART_MESSAGE

	# Load in settings if the settings file exists...
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)

			data = patch_settings(data)

			DEFAULT_QUIT_PART_MESSAGE = data["default_quit_and_part_message"]
			NOTIFY_SCRIPT_END = data["notify_script_execution_end"]
			SAVE_SCRIPT_ON_CLOSE = data["save_on_script_editor_close"]
			SAVE_MACROS = data["save_macros"]
			AUTOCOMPLETE_MACROS = data["autocomplete_macros"]
			SCRIPT_SYNTAX_COMMENTS = data["script_syntax_color_comments"]
			SCRIPT_SYNTAX_COMMANDS = data["script_syntax_color_commands"]
			SCRIPT_SYNTAX_TARGETS = data["script_syntax_color_channels"]
			SCRIPT_SYNTAX_ALIAS = data["script_syntax_color_alias"]
			ENABLE_SCRIPT_EDITOR = data["enable_script_editor"]
			USE_QMENUBAR_MENUS = data["use_default_qmenubar"]
			GLOBALIZE_ALL_SCRIPT_ALIASES = data["all_script_aliases_are_global"]
			SCRIPT_INTERPOLATE_SYMBOL = data["script_interpolation_symbol"]
			SHOW_CONSOLE_BUTTONS = data["display_console_buttons"]
			DOUBLECLICK_TO_CHANGE_NICK = data["double_click_nick_to_change_nicks"]
			MENU_BAR_MOVABLE = data["movable_menubar"]
			MENU_BAR_ORIENT = data["menubar_location"]
			ASK_BEFORE_QUIT = data["ask_before_quitting"]
			SHOW_CONNECTION_LOST_ERROR = data["show_connection_lost_dialog"]
			SHOW_CONNECTION_FAIL_ERROR = data["show_connection_fail_dialog"]
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
			DEVELOPER_MODE = data["plugin_developement_mode"]
			SHOW_LOAD_ERRORS = data["show_plugin_load_error"]
			DISPLAY_TIMESTAMP_SECONDS = data["show_timestamps_with_seconds"]
			EDITOR_AUTO_INDENT = data["editor_autoindent"]
			EDITOR_FONT = data["editor_font"]
			EDITOR_STATUS_BAR = data["editor_status_bar"]
			EDITOR_SYNTAX_HIGHLIGHT = data["editor_syntax_highlighting"]
			EDITOR_PROMPT_FOR_SAVE_ON_EXIT = data["editor_prompt_for_save_on_exit"]
			JOIN_ON_INVITE = data["automatically_join_on_invite"]
			CLICKABLE_CHANNELS = data["create_links_for_channel_names"]
			CONNECTION_DISPLAY_WIDTH = data["connection_display_width"]
			CHANNEL_LIST_REFRESH_FREQUENCY = data["channel_list_refresh_in_seconds"]
			SYSTEM_MESSAGE_PREFIX = data["system_message_prefix"]
			AUTOMATICALLY_FETCH_CHANNEL_LIST = data["automatically_fetch_channel_list"]
			HIDE_MODE_DISPLAY = data["hide_mode_messages"]
			HIDE_TOPIC_MESSAGE = data["hide_topic_messages"]
			HIDE_QUIT_MESSAGE = data["hide_quit_messages"]
			HIDE_NICK_MESSAGE = data["hide_nick_messages"]
			HIDE_INVITE_MESSAGE = data["hide_invite_messages"]
			HIDE_PART_MESSAGE = data["hide_part_messages"]
			HIDE_JOIN_MESSAGE = data["hide_join_messages"]
			APP_TITLE_TO_CURRENT_CHAT = data["set_application_title_to_current_chat_name"]
			APP_TITLE_SHOW_TOPIC = data["show_channel_topic_in_title"]
			CHAT_DISPLAY_INFO_BAR = data["chat_display_info_bar"]
			INPUT_COMMAND_SYMBOL = data["input_command_symbol"]
			DISPLAY_DATES_IN_CHANNEL_CHAT = data["display_dates_in_channel_chat"]
			DISPLAY_USER_LIST = data["display_user_lists"]
			AUTOSAVE_LOGS = data["autosave_logs"]
			AUTOSAVE_LOG_TIME = data["autosave_log_interval_in_seconds"]
			AUTOSAVE_CACHE_SIZE = data["autosave_cache_minimum_size"]
			SCHWA_ANIMATION =  data["schwa_corner_animation"]
			UNSEEN_MESSAGE_ANIMATION =  data["animate_unseen_messages_in_connection_display"]
			CONNECTION_MESSAGE_ANIMATION =  data["animate_connecting_messages_in_connection_display"]
			ENABLE_SCRIPTS = data["enable_scripts"]

	# ...or create the file with defaults if the settings
	# file doesn't exist
	else:
		save_settings(filename)
