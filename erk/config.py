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
DISPLAY_TIMESTAMP_SECONDS = False
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
CONNECTION_MESSAGE_ANIMATION = True
CONNECTION_ANIMATION_LENGTH = 1000
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
AUTOCOMPLETE_MACROS = True
SAVE_MACROS = True
SAVE_SCRIPT_ON_CLOSE = True
NOTIFY_SCRIPT_END = True
DEFAULT_QUIT_PART_MESSAGE = APPLICATION_NAME + " " + APPLICATION_MAJOR_VERSION + " - " + OFFICIAL_REPOSITORY_SHORT_CLEAN
ENABLE_MACROS = True
AUTOCOMPLETE_CHANNELS = True
DICTIONARY = []
MACRO_INTERPOLATE_SYMBOL = "&"
ENABLE_IGNORE = True
IGNORE_PUBLIC = True
IGNORE_PRIVATE = True
IGNORE_NOTICE = True
WRITE_PRIVATE_TO_CONSOLE = True
WRITE_NOTICE_TO_CONSOLE = True
ENABLE_COMMANDS = True
ENABLE_PLUGINS = True
SHOW_PLUGINS_MENU = True
PLUGINS_CATCH_IGNORES = False
ALWAYS_ALLOW_ME = True
DISABLED_PLUGINS = []
SHOW_PLUGIN_INFO_IN_MENU = False
AUTOCOMPLETE_PLUGINS = True
PLUGIN_HELP = True
ADDITIONAL_PLUGIN_LOCATIONS = []
MARK_BEGINNING_AND_END_OF_LIST_SEARCH = True
LIMIT_LIST_SEARCH_TO_CHANNEL_NAME = False
LIST_SEARCH_CASE_SENSITIVE = False
ENABLE_ALIASES = True
ENABLE_PLUGIN_INPUT = True
SCROLL_CHAT_TO_BOTTOM = True
REJOIN_CHANNELS_ON_DISCONNECTIONS = True
PLUGIN_LOAD_ERRORS = True
CONNECTION_DISPLAY_BG_COLOR = "#FFFFFF"
CONNECTION_DISPLAY_TEXT_COLOR = "#000000"
SCRIPT_SYNTAX_COMMENTS = 'darkMagenta'
SCRIPT_SYNTAX_COMMANDS = 'darkBlue'
SCRIPT_SYNTAX_TARGETS = 'darkRed'
SCRIPT_SYNTAX_ALIAS = 'darkGreen'
SCRIPT_SYNTAX_BACKGROUND = "#FFFFFF"
SCRIPT_SYNTAX_TEXT = "#000000"
ENABLE_TOPIC_EDITOR = True
ENABLE_USERLIST_MENU = True
ENABLE_CONNECTION_CONTEXT = True
DISPLAY_MODES_ON_CHANNEL = True
LOAD_SERVER_LOGS = True
SAVE_SERVER_LOGS = True
UNSEEN_MESSAGE_COLOR = "#FF8C00"
CONNECTING_ANIMATION_COLOR = "#FF8C00"
CURSOR_WIDTH = 1
DO_NOT_TRIGGER_UNSEEN_TIME = 5
CONNECTION_DISPLAY_BRANCHES = False
CONNECTION_DISPLAY_COLLAPSE = True
UNDERLINE_CURRENT_CHAT = True
BOLD_CURRENT_CHAT = True
ITALIC_CURRENT_CHAT = False
SHOW_UPTIME_IN_SECONDS = False
SYSTRAY_ICON = True
CLICK_SYSTRAY_TO_HIDE = True
SYSTRAY_MENU = True
MARK_UNSEEN_SYSTRAY = True
SYSTRAY_ALLOW_DISCONNECT = True
SYSTRAY_ALLOW_CONNECT = True
SYSTRAY_SHOW_CONNECTIONS = True

ELIDE_TOPIC = True

def save_settings(filename=SETTINGS_FILE):

	if filename==None: filename = SETTINGS_FILE

	settings = {

		"elide_topic_display": ELIDE_TOPIC,
		"system_tray_display_connections": SYSTRAY_SHOW_CONNECTIONS,
		"system_tray_allow_connect": SYSTRAY_ALLOW_CONNECT,
		"system_tray_allow_disconnect": SYSTRAY_ALLOW_DISCONNECT,
		"system_tray_mark_unread": MARK_UNSEEN_SYSTRAY,
		"system_tray_icon_menu": SYSTRAY_MENU,
		"system_tray_icon_click_to_hide_or_show": CLICK_SYSTRAY_TO_HIDE,
		"system_tray_icon": SYSTRAY_ICON,
		"connection_display_uptime_in_seconds": SHOW_UPTIME_IN_SECONDS,
		"connection_display_italic_current_chat": ITALIC_CURRENT_CHAT,
		"connection_display_bold_current_chat": BOLD_CURRENT_CHAT,
		"connection_display_underline_current_chat": UNDERLINE_CURRENT_CHAT,
		"connection_display_visible_branches": CONNECTION_DISPLAY_BRANCHES,
		"connection_display_collapsable": CONNECTION_DISPLAY_COLLAPSE,
		"cursor_width": CURSOR_WIDTH,
		"unseen_messages_animation_color": UNSEEN_MESSAGE_COLOR,
		"connecting_animation_color": CONNECTING_ANIMATION_COLOR,
		"load_server_logs": LOAD_SERVER_LOGS,
		"save_server_logs": SAVE_SERVER_LOGS,
		"display_user_modes_on_channels": DISPLAY_MODES_ON_CHANNEL,
		"enable_connection_display_context_menu": ENABLE_CONNECTION_CONTEXT,
		"enable_userlist_menu": ENABLE_USERLIST_MENU,
		"enable_topic_editor": ENABLE_TOPIC_EDITOR,
		"script_syntax_color_background": SCRIPT_SYNTAX_BACKGROUND,
		"script_syntax_color_text": SCRIPT_SYNTAX_TEXT,
		"connection_display_background": CONNECTION_DISPLAY_BG_COLOR,
		"connection_display_text": CONNECTION_DISPLAY_TEXT_COLOR,
		"show_plugin_load_errors": PLUGIN_LOAD_ERRORS,
		"rejoin_channels_on_reconnection": REJOIN_CHANNELS_ON_DISCONNECTIONS,
		"scroll_to_bottom_on_chat_switch": SCROLL_CHAT_TO_BOTTOM,
		"enable_plugin_input_event": ENABLE_PLUGIN_INPUT,
		"enable_script_aliases": ENABLE_ALIASES,
		"case_sensitive_list_search": LIST_SEARCH_CASE_SENSITIVE,
		"mark_beginning_and_end_of_list_search": MARK_BEGINNING_AND_END_OF_LIST_SEARCH,
		"limit_list_search_to_names": LIMIT_LIST_SEARCH_TO_CHANNEL_NAME,
		"additional_plugin_locations": ADDITIONAL_PLUGIN_LOCATIONS,
		"plugins_can_add_to_help": PLUGIN_HELP,
		"autocomplete_for_plugins": AUTOCOMPLETE_PLUGINS,
		"show_plugin_details_in_menu_entry": SHOW_PLUGIN_INFO_IN_MENU,
		"disabled_plugins": DISABLED_PLUGINS,
		"always_allow_ctcp_action_command": ALWAYS_ALLOW_ME,
		"plugins_catch_ignored_messages": PLUGINS_CATCH_IGNORES,
		"show_plugins_menu": SHOW_PLUGINS_MENU,
		"enable_plugins": ENABLE_PLUGINS,
		"enable_user_commands": ENABLE_COMMANDS,
		"write_private_messages_to_console": WRITE_PRIVATE_TO_CONSOLE,
		"write_notice_messages_to_console": WRITE_NOTICE_TO_CONSOLE,
		"ignore_public_messages": IGNORE_PUBLIC,
		"ignore_private_messages": IGNORE_PRIVATE,
		"ignore_notice_messages": IGNORE_NOTICE,
		"enable_user_ignore": ENABLE_IGNORE,
		"macro_interpolation_symbol": MACRO_INTERPOLATE_SYMBOL,
		"dictionary": DICTIONARY,
		"autocomplete_channels": AUTOCOMPLETE_CHANNELS,
		"enable_macros": ENABLE_MACROS,
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
		"show_timestamps_with_seconds": DISPLAY_TIMESTAMP_SECONDS,
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

	if not "elide_topic_display" in data:
		data["elide_topic_display"] = ELIDE_TOPIC

	if not "system_tray_display_connections" in data:
		data["system_tray_display_connections"] = SYSTRAY_SHOW_CONNECTIONS

	if not "system_tray_allow_connect" in data:
		data["system_tray_allow_connect"] = SYSTRAY_ALLOW_CONNECT

	if not "system_tray_allow_disconnect" in data:
		data["system_tray_allow_disconnect"] = SYSTRAY_ALLOW_DISCONNECT

	if not "system_tray_mark_unread" in data:
		data["system_tray_mark_unread"] = MARK_UNSEEN_SYSTRAY

	if not "system_tray_icon_menu" in data:
		data["system_tray_icon_menu"] = SYSTRAY_MENU

	if not "system_tray_icon_click_to_hide_or_show" in data:
		data["system_tray_icon_click_to_hide_or_show"] = CLICK_SYSTRAY_TO_HIDE

	if not "system_tray_icon" in data:
		data["system_tray_icon"] = SYSTRAY_ICON

	if not "connection_display_uptime_in_seconds" in data:
		data["connection_display_uptime_in_seconds"] = SHOW_UPTIME_IN_SECONDS

	if not "connection_display_italic_current_chat" in data:
		data["connection_display_italic_current_chat"] = ITALIC_CURRENT_CHAT

	if not "connection_display_bold_current_chat" in data:
		data["connection_display_bold_current_chat"] = BOLD_CURRENT_CHAT

	if not "connection_display_underline_current_chat" in data:
		data["connection_display_underline_current_chat"] = UNDERLINE_CURRENT_CHAT

	if not "connection_display_visible_branches" in data:
		data["connection_display_visible_branches"] = CONNECTION_DISPLAY_BRANCHES

	if not "connection_display_collapsable" in data:
		data["connection_display_collapsable"] = CONNECTION_DISPLAY_COLLAPSE

	if not "cursor_width" in data:
		data["cursor_width"] = CURSOR_WIDTH

	if not "unseen_messages_animation_color" in data:
		data["unseen_messages_animation_color"] = UNSEEN_MESSAGE_COLOR

	if not "connecting_animation_color" in data:
		data["connecting_animation_color"] = CONNECTING_ANIMATION_COLOR

	if not "load_server_logs" in data:
		data["load_server_logs"] = LOAD_SERVER_LOGS

	if not "save_server_logs" in data:
		data["save_server_logs"] = SAVE_SERVER_LOGS

	if not "display_user_modes_on_channels" in data:
		data["display_user_modes_on_channels"] = DISPLAY_MODES_ON_CHANNEL

	if not "enable_connection_display_context_menu" in data:
		data["enable_connection_display_context_menu"] = ENABLE_CONNECTION_CONTEXT

	if not "enable_userlist_menu" in data:
		data["enable_userlist_menu"] = ENABLE_USERLIST_MENU

	if not "enable_topic_editor" in data:
		data["enable_topic_editor"] = ENABLE_TOPIC_EDITOR

	if not "script_syntax_color_background" in data:
		data["script_syntax_color_background"] = SCRIPT_SYNTAX_BACKGROUND

	if not "script_syntax_color_text" in data:
		data["script_syntax_color_text"] = SCRIPT_SYNTAX_TEXT

	if not "connection_display_text" in data:
		data["connection_display_text"] = CONNECTION_DISPLAY_TEXT_COLOR

	if not "connection_display_background" in data:
		data["connection_display_background"] = CONNECTION_DISPLAY_BG_COLOR

	if not "show_plugin_load_errors" in data:
		data["show_plugin_load_errors"] = PLUGIN_LOAD_ERRORS

	if not "rejoin_channels_on_reconnection" in data:
		data["rejoin_channels_on_reconnection"] = REJOIN_CHANNELS_ON_DISCONNECTIONS

	if not "scroll_to_bottom_on_chat_switch" in data:
		data["scroll_to_bottom_on_chat_switch"] = SCROLL_CHAT_TO_BOTTOM

	if not "enable_plugin_input_event" in data:
		data["enable_plugin_input_event"] = ENABLE_PLUGIN_INPUT

	if not "enable_script_aliases" in data:
		data["enable_script_aliases"] = ENABLE_ALIASES

	if not "case_sensitive_list_search" in data:
		data["case_sensitive_list_search"] = LIST_SEARCH_CASE_SENSITIVE

	if not "mark_beginning_and_end_of_list_search" in data:
		data["mark_beginning_and_end_of_list_search"] = MARK_BEGINNING_AND_END_OF_LIST_SEARCH

	if not "limit_list_search_to_names" in data:
		data["limit_list_search_to_names"] = LIMIT_LIST_SEARCH_TO_CHANNEL_NAME

	if not "additional_plugin_locations" in data:
		data["additional_plugin_locations"] = ADDITIONAL_PLUGIN_LOCATIONS

	if not "plugins_can_add_to_help" in data:
		data["plugins_can_add_to_help"] = PLUGIN_HELP

	if not "autocomplete_for_plugins" in data:
		data["autocomplete_for_plugins"] = AUTOCOMPLETE_PLUGINS

	if not "show_plugin_details_in_menu_entry" in data:
		data["show_plugin_details_in_menu_entry"] = SHOW_PLUGIN_INFO_IN_MENU

	if not "disabled_plugins" in data:
		data["disabled_plugins"] = DISABLED_PLUGINS

	if not "always_allow_ctcp_action_command" in data:
		data["always_allow_ctcp_action_command"] = ALWAYS_ALLOW_ME

	if not "plugins_catch_ignored_messages" in data:
		data["plugins_catch_ignored_messages"] = PLUGINS_CATCH_IGNORES

	if not "show_plugins_menu" in data:
		data["show_plugins_menu"] = SHOW_PLUGINS_MENU

	if not "enable_plugins" in data:
		data["enable_plugins"] = ENABLE_PLUGINS

	if not "enable_user_commands" in data:
		data["enable_user_commands"] = ENABLE_COMMANDS

	if not "write_private_messages_to_console" in data:
		data["write_private_messages_to_console"] = WRITE_PRIVATE_TO_CONSOLE

	if not "write_notice_messages_to_console" in data:
		data["write_notice_messages_to_console"] = WRITE_NOTICE_TO_CONSOLE

	if not "ignore_public_messages" in data:
		data["ignore_public_messages"] = IGNORE_PUBLIC

	if not "ignore_private_messages" in data:
		data["ignore_private_messages"] = IGNORE_PRIVATE

	if not "ignore_notice_messages" in data:
		data["ignore_notice_messages"] = IGNORE_NOTICE

	if not "enable_user_ignore" in data:
		data["enable_user_ignore"] = ENABLE_IGNORE

	if not "macro_interpolation_symbol" in data:
		data["macro_interpolation_symbol"] = MACRO_INTERPOLATE_SYMBOL

	if not "dictionary" in data:
		data["dictionary"] = DICTIONARY

	if not "autocomplete_channels" in data:
		data["autocomplete_channels"] = AUTOCOMPLETE_CHANNELS

	if not "enable_macros" in data:
		data["enable_macros"] = ENABLE_MACROS

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

	if not "schwa_corner_animation" in data:
		data["schwa_corner_animation"] = SCHWA_ANIMATION

	if not "animate_unseen_messages_in_connection_display" in data:
		data["animate_unseen_messages_in_connection_display"] = UNSEEN_MESSAGE_ANIMATION

	if not "animate_connecting_messages_in_connection_display" in data:
		data["animate_connecting_messages_in_connection_display"] = CONNECTION_MESSAGE_ANIMATION

	if not "autosave_cache_minimum_size" in data:
		data["autosave_cache_minimum_size"] = AUTOSAVE_CACHE_SIZE

	if not "autosave_logs" in data:
		data["autosave_logs"] = AUTOSAVE_LOGS

	if not "autosave_log_interval_in_seconds" in data:
		data["autosave_log_interval_in_seconds"] = AUTOSAVE_LOG_TIME

	if not "command_history_length" in data:
		data["command_history_length"] = HISTORY_LENGTH

	if not "chat_display_widget_spacing" in data:
		data["chat_display_widget_spacing"] = CHAT_WINDOW_WIDGET_SPACING

	if not "get_hostmasks_on_channel_join" in data:
		data["get_hostmasks_on_channel_join"] = GET_HOSTMASKS_ON_CHANNEL_JOIN

	if not "save_joined_channels" in data:
		data["save_joined_channels"] = SAVE_JOINED_CHANNELS

	if not "starting_app_width" in data:
		data["starting_app_width"] = DEFAULT_APP_WIDTH

	if not "starting_app_height" in data:
		data["starting_app_height"] = DEFAULT_APP_HEIGHT

	if not "spellcheck_input" in data:
		data["spellcheck_input"] = SPELLCHECK_INPUT

	if not "spellcheck_language" in data:
		data["spellcheck_language"] = SPELLCHECK_LANGUAGE

	if not "open_window_for_new_private_messages" in data:
		data["open_window_for_new_private_messages"] = OPEN_NEW_PRIVATE_MESSAGE_WINDOWS

	if not "minimum_nickname_display_width" in data:
		data["minimum_nickname_display_width"] = NICK_DISPLAY_WIDTH

	if not "show_timestamps" in data:
		data["show_timestamps"] = DISPLAY_TIMESTAMP

	if not "use_24hour_clock_for_timestamps" in data:
		data["use_24hour_clock_for_timestamps"] = USE_24HOUR_CLOCK_FOR_TIMESTAMPS

	if not "display_irc_color_codes" in data:
		data["display_irc_color_codes"] = DISPLAY_IRC_COLORS

	if not "convert_urls_in_messages_to_links" in data:
		data["convert_urls_in_messages_to_links"] = CONVERT_URLS_TO_LINKS

	if not "doubleclick_to_switch_chat_windows" in data:
		data["doubleclick_to_switch_chat_windows"] = DOUBLECLICK_SWITCH

	if not "font" in data:
		data["font"] = DISPLAY_FONT

	if not "display_connection_uptime" in data:
		data["display_connection_uptime"] = DISPLAY_CONNECTION_UPTIME

	if not "connection_display_location" in data:
		data["connection_display_location"] = CONNECTION_DISPLAY_LOCATION

	if not "is_connection_display_moveable" in data:
		data["is_connection_display_moveable"] = CONNECTION_DISPLAY_MOVE

	if not "connection_display_visible" in data:
		data["connection_display_visible"] = CONNECTION_DISPLAY_VISIBLE

	if not "display_channel_modes" in data:
		data["display_channel_modes"] = DISPLAY_CHANNEL_MODES

	if not "switch_to_new_chats" in data:
		data["switch_to_new_chats"] = SWITCH_TO_NEW_WINDOWS

	if not "autocomplete_nicknames" in data:
		data["autocomplete_nicknames"] = AUTOCOMPLETE_NICKNAMES

	if not "autocomplete_commands" in data:
		data["autocomplete_commands"] = AUTOCOMPLETE_COMMANDS

	if not "spellcheck_ignore_nicknames" in data:
		data["spellcheck_ignore_nicknames"] = SPELLCHECK_IGNORE_NICKS

	if not "use_emoji_shortcodes" in data:
		data["use_emoji_shortcodes"] = USE_EMOJIS

	if not "autocomplete_emoji" in data:
		data["autocomplete_emoji"] = AUTOCOMPLETE_EMOJI

	if not "filter_profanity" in data:
		data["filter_profanity"] = FILTER_PROFANITY

	if not "text_only_channel_user_lists" in data:
		data["text_only_channel_user_lists"] = PLAIN_USER_LISTS

	if not "display_channel_status" in data:
		data["display_channel_status"] = DISPLAY_CHANNEL_STATUS_NICK_DISPLAY

	if not "display_nickname_on_channels" in data:
		data["display_nickname_on_channels"] = DISPLAY_NICKNAME_ON_CHANNEL

	if not "expand_server_node_on_connection" in data:
		data["expand_server_node_on_connection"] = EXPAND_SERVER_ON_CONNECT

	if not "enable_command_history" in data:
		data["enable_command_history"] = TRACK_COMMAND_HISTORY

	if not "save_channel_logs" in data:
		data["save_channel_logs"] = SAVE_CHANNEL_LOGS

	if not "load_channel_logs" in data:
		data["load_channel_logs"] = LOAD_CHANNEL_LOGS

	if not "maximum_log_display_size" in data:
		data["maximum_log_display_size"] = LOG_LOAD_SIZE_MAX

	if not "mark_end_of_loaded_log" in data:
		data["mark_end_of_loaded_log"] = MARK_END_OF_LOADED_LOG

	if not "display_date_and_time_of_channel_log_resume" in data:
		data["display_date_and_time_of_channel_log_resume"] = DISPLAY_CHAT_RESUME_DATE_TIME

	if not "save_private_logs" in data:
		data["save_private_logs"] = SAVE_PRIVATE_LOGS

	if not "load_private_logs" in data:
		data["load_private_logs"] = LOAD_PRIVATE_LOGS

	if not "show_system_messages_prefix" in data:
		data["show_system_messages_prefix"] = MARK_SYSTEM_MESSAGES_WITH_SYMBOL

	if not "show_timestamps_with_seconds" in data:
		data["show_timestamps_with_seconds"] = DISPLAY_TIMESTAMP_SECONDS

	if not "automatically_join_on_invite" in data:
		data["automatically_join_on_invite"] = JOIN_ON_INVITE

	if not "create_links_for_channel_names" in data:
		data["create_links_for_channel_names"] = CLICKABLE_CHANNELS

	if not "connection_display_width" in data:
		data["connection_display_width"] = CONNECTION_DISPLAY_WIDTH

	if not "channel_list_refresh_in_seconds" in data:
		data["channel_list_refresh_in_seconds"] = CHANNEL_LIST_REFRESH_FREQUENCY

	if not "system_message_prefix" in data:
		data["system_message_prefix"] = SYSTEM_MESSAGE_PREFIX

	if not "automatically_fetch_channel_list" in data:
		data["automatically_fetch_channel_list"] = AUTOMATICALLY_FETCH_CHANNEL_LIST

	if not "hide_mode_messages" in data:
		data["hide_mode_messages"] = HIDE_MODE_DISPLAY

	if not "hide_topic_messages" in data:
		data["hide_topic_messages"] = HIDE_TOPIC_MESSAGE

	if not "hide_quit_messages" in data:
		data["hide_quit_messages"] = HIDE_QUIT_MESSAGE

	if not "hide_nick_messages" in data:
		data["hide_nick_messages"] = HIDE_NICK_MESSAGE

	if not "hide_invite_messages" in data:
		data["hide_invite_messages"] = HIDE_INVITE_MESSAGE

	if not "hide_part_messages" in data:
		data["hide_part_messages"] = HIDE_PART_MESSAGE

	if not "hide_join_messages" in data:
		data["hide_join_messages"] = HIDE_JOIN_MESSAGE

	if not "set_application_title_to_current_chat_name" in data:
		data["set_application_title_to_current_chat_name"] = APP_TITLE_TO_CURRENT_CHAT

	if not "show_channel_topic_in_title" in data:
		data["show_channel_topic_in_title"] = APP_TITLE_SHOW_TOPIC

	if not "chat_display_info_bar" in data:
		data["chat_display_info_bar"] = CHAT_DISPLAY_INFO_BAR

	if not "input_command_symbol" in data:
		data["input_command_symbol"] = INPUT_COMMAND_SYMBOL

	if not "display_dates_in_channel_chat" in data:
		data["display_dates_in_channel_chat"] = DISPLAY_DATES_IN_CHANNEL_CHAT

	if not "show_connection_lost_dialog" in data:
		data["show_connection_lost_dialog"] = SHOW_CONNECTION_LOST_ERROR

	if not "show_connection_fail_dialog" in data:
		data["show_connection_fail_dialog"] = SHOW_CONNECTION_FAIL_ERROR

	if not "display_user_lists" in data:
		data["display_user_lists"] = DISPLAY_USER_LIST

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
	global DISPLAY_TIMESTAMP_SECONDS
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
	global ENABLE_MACROS
	global AUTOCOMPLETE_CHANNELS
	global DICTIONARY
	global MACRO_INTERPOLATE_SYMBOL
	global ENABLE_IGNORE
	global IGNORE_PUBLIC
	global IGNORE_PRIVATE
	global IGNORE_NOTICE
	global WRITE_PRIVATE_TO_CONSOLE
	global WRITE_NOTICE_TO_CONSOLE
	global ENABLE_COMMANDS
	global ENABLE_PLUGINS
	global SHOW_PLUGINS_MENU
	global PLUGINS_CATCH_IGNORES
	global ALWAYS_ALLOW_ME
	global DISABLED_PLUGINS
	global SHOW_PLUGIN_INFO_IN_MENU
	global AUTOCOMPLETE_PLUGINS
	global PLUGIN_HELP
	global ADDITIONAL_PLUGIN_LOCATIONS
	global MARK_BEGINNING_AND_END_OF_LIST_SEARCH
	global LIMIT_LIST_SEARCH_TO_CHANNEL_NAME
	global LIST_SEARCH_CASE_SENSITIVE
	global ENABLE_ALIASES
	global ENABLE_PLUGIN_INPUT
	global SCROLL_CHAT_TO_BOTTOM
	global REJOIN_CHANNELS_ON_DISCONNECTIONS
	global PLUGIN_LOAD_ERRORS
	global CONNECTION_DISPLAY_BG_COLOR
	global CONNECTION_DISPLAY_TEXT_COLOR
	global SCRIPT_SYNTAX_BACKGROUND
	global SCRIPT_SYNTAX_TEXT
	global ENABLE_TOPIC_EDITOR
	global ENABLE_USERLIST_MENU
	global ENABLE_CONNECTION_CONTEXT
	global DISPLAY_MODES_ON_CHANNEL
	global LOAD_SERVER_LOGS
	global SAVE_SERVER_LOGS
	global UNSEEN_MESSAGE_COLOR
	global CONNECTING_ANIMATION_COLOR
	global CURSOR_WIDTH
	global CONNECTION_DISPLAY_BRANCHES
	global CONNECTION_DISPLAY_COLLAPSE
	global BOLD_CURRENT_CHAT
	global UNDERLINE_CURRENT_CHAT
	global ITALIC_CURRENT_CHAT
	global SHOW_UPTIME_IN_SECONDS
	global SYSTRAY_ICON
	global CLICK_SYSTRAY_TO_HIDE
	global SYSTRAY_MENU
	global MARK_UNSEEN_SYSTRAY
	global SYSTRAY_ALLOW_DISCONNECT
	global SYSTRAY_ALLOW_CONNECT
	global SYSTRAY_SHOW_CONNECTIONS
	global ELIDE_TOPIC

	# Load in settings if the settings file exists...
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)

			data = patch_settings(data)

			ELIDE_TOPIC = data["elide_topic_display"]
			SYSTRAY_SHOW_CONNECTIONS = data["system_tray_display_connections"]
			SYSTRAY_ALLOW_CONNECT = data["system_tray_allow_connect"]
			SYSTRAY_ALLOW_DISCONNECT = data["system_tray_allow_disconnect"]
			MARK_UNSEEN_SYSTRAY = data["system_tray_mark_unread"]
			SYSTRAY_MENU = data["system_tray_icon_menu"]
			CLICK_SYSTRAY_TO_HIDE = data["system_tray_icon_click_to_hide_or_show"]
			SYSTRAY_ICON = data["system_tray_icon"]
			SHOW_UPTIME_IN_SECONDS = data["connection_display_uptime_in_seconds"]
			ITALIC_CURRENT_CHAT = data["connection_display_italic_current_chat"]
			BOLD_CURRENT_CHAT = data["connection_display_bold_current_chat"]
			UNDERLINE_CURRENT_CHAT = data["connection_display_underline_current_chat"]
			CONNECTION_DISPLAY_BRANCHES = data["connection_display_visible_branches"]
			CONNECTION_DISPLAY_COLLAPSE = data["connection_display_collapsable"]
			CURSOR_WIDTH = data["cursor_width"]
			UNSEEN_MESSAGE_COLOR = data["unseen_messages_animation_color"]
			CONNECTING_ANIMATION_COLOR = data["connecting_animation_color"]
			LOAD_SERVER_LOGS = data["load_server_logs"]
			SAVE_SERVER_LOGS = data["save_server_logs"]
			DISPLAY_MODES_ON_CHANNEL = data["display_user_modes_on_channels"]
			ENABLE_CONNECTION_CONTEXT = data["enable_connection_display_context_menu"]
			ENABLE_USERLIST_MENU = data["enable_userlist_menu"]
			ENABLE_TOPIC_EDITOR = data["enable_topic_editor"]
			SCRIPT_SYNTAX_BACKGROUND = data["script_syntax_color_background"]
			SCRIPT_SYNTAX_TEXT = data["script_syntax_color_text"]
			CONNECTION_DISPLAY_BG_COLOR = data["connection_display_background"]
			CONNECTION_DISPLAY_TEXT_COLOR = data["connection_display_text"]
			PLUGIN_LOAD_ERRORS = data["show_plugin_load_errors"]
			REJOIN_CHANNELS_ON_DISCONNECTIONS = data["rejoin_channels_on_reconnection"]
			SCROLL_CHAT_TO_BOTTOM = data["scroll_to_bottom_on_chat_switch"]
			ENABLE_PLUGIN_INPUT = data["enable_plugin_input_event"]
			ENABLE_ALIASES = data["enable_script_aliases"]
			LIST_SEARCH_CASE_SENSITIVE = data["case_sensitive_list_search"]
			MARK_BEGINNING_AND_END_OF_LIST_SEARCH = data["mark_beginning_and_end_of_list_search"]
			LIMIT_LIST_SEARCH_TO_CHANNEL_NAME = data["limit_list_search_to_names"]
			ADDITIONAL_PLUGIN_LOCATIONS = data["additional_plugin_locations"]
			PLUGIN_HELP = data["plugins_can_add_to_help"]
			AUTOCOMPLETE_PLUGINS = data["autocomplete_for_plugins"]
			SHOW_PLUGIN_INFO_IN_MENU = data["show_plugin_details_in_menu_entry"]
			DISABLED_PLUGINS = data["disabled_plugins"]
			ALWAYS_ALLOW_ME = data["always_allow_ctcp_action_command"]
			PLUGINS_CATCH_IGNORES = data["plugins_catch_ignored_messages"]
			SHOW_PLUGINS_MENU = data["show_plugins_menu"]
			ENABLE_PLUGINS = data["enable_plugins"]
			ENABLE_COMMANDS = data["enable_user_commands"]
			WRITE_PRIVATE_TO_CONSOLE = data["write_private_messages_to_console"]
			WRITE_NOTICE_TO_CONSOLE = data["write_notice_messages_to_console"]
			IGNORE_PUBLIC = data["ignore_public_messages"]
			IGNORE_PRIVATE = data["ignore_private_messages"]
			IGNORE_NOTICE = data["ignore_notice_messages"]
			ENABLE_IGNORE = data["enable_user_ignore"]
			MACRO_INTERPOLATE_SYMBOL = data["macro_interpolation_symbol"]
			DICTIONARY = data["dictionary"]
			AUTOCOMPLETE_CHANNELS = data["autocomplete_channels"]
			ENABLE_MACROS = data["enable_macros"]
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
			DISPLAY_TIMESTAMP_SECONDS = data["show_timestamps_with_seconds"]
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


def check_settings(filename):
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)

			data = patch_settings(data)

			check = 0
			if "additional_plugin_locations" in data: check = check + 1
			if "all_script_aliases_are_global" in data: check = check + 1
			if "always_allow_ctcp_action_command" in data: check = check + 1
			if "animate_connecting_messages_in_connection_display" in data: check = check + 1
			if "animate_unseen_messages_in_connection_display" in data: check = check + 1
			if "ask_before_quitting" in data: check = check + 1
			if "autocomplete_channels" in data: check = check + 1
			if "autocomplete_commands" in data: check = check + 1
			if "autocomplete_emoji" in data: check = check + 1
			if "autocomplete_for_plugins" in data: check = check + 1
			if "autocomplete_macros" in data: check = check + 1
			if "autocomplete_nicknames" in data: check = check + 1
			if "automatically_fetch_channel_list" in data: check = check + 1
			if "automatically_join_on_invite" in data: check = check + 1
			if "autosave_cache_minimum_size" in data: check = check + 1
			if "autosave_log_interval_in_seconds" in data: check = check + 1
			if "autosave_logs" in data: check = check + 1
			if "channel_list_refresh_in_seconds" in data: check = check + 1
			if "chat_display_info_bar" in data: check = check + 1
			if "chat_display_widget_spacing" in data: check = check + 1
			if "command_history_length" in data: check = check + 1
			if "connection_display_location" in data: check = check + 1
			if "connection_display_visible" in data: check = check + 1
			if "connection_display_width" in data: check = check + 1
			if "convert_urls_in_messages_to_links" in data: check = check + 1
			if "create_links_for_channel_names" in data: check = check + 1
			if "default_quit_and_part_message" in data: check = check + 1
			if "dictionary" in data: check = check + 1
			if "disabled_plugins" in data: check = check + 1
			if "display_channel_modes" in data: check = check + 1
			if "display_channel_status" in data: check = check + 1
			if "display_connection_uptime" in data: check = check + 1
			if "display_console_buttons" in data: check = check + 1
			if "display_date_and_time_of_channel_log_resume" in data: check = check + 1
			if "display_dates_in_channel_chat" in data: check = check + 1
			if "display_irc_color_codes" in data: check = check + 1
			if "display_nickname_on_channels" in data: check = check + 1
			if "display_user_lists" in data: check = check + 1
			if "double_click_nick_to_change_nicks" in data: check = check + 1
			if "doubleclick_to_switch_chat_windows" in data: check = check + 1
			if "enable_command_history" in data: check = check + 1
			if "enable_macros" in data: check = check + 1
			if "enable_plugins" in data: check = check + 1
			if "enable_script_editor" in data: check = check + 1
			if "enable_scripts" in data: check = check + 1
			if "enable_user_commands" in data: check = check + 1
			if "enable_user_ignore" in data: check = check + 1
			if "expand_server_node_on_connection" in data: check = check + 1
			if "filter_profanity" in data: check = check + 1
			if "font " in data: check = check + 1
			if "get_hostmasks_on_channel_join" in data: check = check + 1
			if "hide_invite_messages" in data: check = check + 1
			if "hide_join_messages" in data: check = check + 1
			if "hide_mode_messages" in data: check = check + 1
			if "hide_nick_messages" in data: check = check + 1
			if "hide_part_messages" in data: check = check + 1
			if "hide_quit_messages" in data: check = check + 1
			if "hide_topic_messages" in data: check = check + 1
			if "ignore_notice_messages" in data: check = check + 1
			if "ignore_private_messages" in data: check = check + 1
			if "ignore_public_messages" in data: check = check + 1
			if "input_command_symbol" in data: check = check + 1
			if "is_connection_display_moveable" in data: check = check + 1
			if "limit_list_search_to_names" in data: check = check + 1
			if "load_channel_logs" in data: check = check + 1
			if "load_private_logs" in data: check = check + 1
			if "macro_interpolation_symbol" in data: check = check + 1
			if "mark_beginning_and_end_of_list_search" in data: check = check + 1
			if "mark_end_of_loaded_log" in data: check = check + 1
			if "maximum_log_display_size" in data: check = check + 1
			if "menubar_location" in data: check = check + 1
			if "minimum_nickname_display_width" in data: check = check + 1
			if "movable_menubar" in data: check = check + 1
			if "notify_script_execution_end" in data: check = check + 1
			if "open_window_for_new_private_messages" in data: check = check + 1
			if "plugins_can_add_to_help" in data: check = check + 1
			if "plugins_catch_ignored_messages" in data: check = check + 1
			if "save_channel_logs" in data: check = check + 1
			if "save_joined_channels" in data: check = check + 1
			if "save_macros" in data: check = check + 1
			if "save_on_script_editor_close" in data: check = check + 1
			if "save_private_logs" in data: check = check + 1
			if "schwa_corner_animation" in data: check = check + 1
			if "script_interpolation_symbol" in data: check = check + 1
			if "script_syntax_color_alias" in data: check = check + 1
			if "script_syntax_color_channels" in data: check = check + 1
			if "script_syntax_color_commands" in data: check = check + 1
			if "script_syntax_color_comments" in data: check = check + 1
			if "set_application_title_to_current_chat_name" in data: check = check + 1
			if "show_channel_topic_in_title" in data: check = check + 1
			if "show_connection_fail_dialog" in data: check = check + 1
			if "show_connection_lost_dialog" in data: check = check + 1
			if "show_plugin_details_in_menu_entry" in data: check = check + 1
			if "show_plugins_menu" in data: check = check + 1
			if "show_system_messages_prefix" in data: check = check + 1
			if "show_timestamps" in data: check = check + 1
			if "show_timestamps_with_seconds" in data: check = check + 1
			if "spellcheck_ignore_nicknames" in data: check = check + 1
			if "spellcheck_input" in data: check = check + 1
			if "spellcheck_language" in data: check = check + 1
			if "starting_app_height" in data: check = check + 1
			if "starting_app_width" in data: check = check + 1
			if "switch_to_new_chats" in data: check = check + 1
			if "system_message_prefix" in data: check = check + 1
			if "text_only_channel_user_lists" in data: check = check + 1
			if "use_24hour_clock_for_timestamps" in data: check = check + 1
			if "use_default_qmenubar" in data: check = check + 1
			if "use_emoji_shortcodes" in data: check = check + 1
			if "write_notice_messages_to_console" in data: check = check + 1
			if "write_private_messages_to_console" in data: check = check + 1
			if "case_sensitive_list_search" in data: check = check + 1
			if "enable_script_aliases" in data: check = check + 1
			if "enable_plugin_input_event" in data: check = check + 1
			if "scroll_to_bottom_on_chat_switch" in data: check = check + 1
			if "rejoin_channels_on_reconnection" in data: check = check + 1
			if "show_plugin_load_errors" in data: check = check + 1
			if "connection_display_background" in data: check = check + 1
			if "connection_display_text" in data: check = check + 1
			if "script_syntax_color_background" in data: check = check + 1
			if "script_syntax_color_text" in data: check = check + 1
			if "enable_topic_editor" in data: check = check + 1
			if "enable_userlist_menu" in data: check = check + 1
			if "enable_connection_display_context_menu" in data: check = check + 1
			if "display_user_modes_on_channels" in data: check = check + 1
			if "load_server_logs" in data: check = check + 1
			if "save_server_logs" in data: check = check + 1
			if "unseen_messages_animation_color" in data: check = check + 1
			if "connecting_animation_color" in data: check = check + 1
			if "cursor_width" in data: check = check + 1
			if "connection_display_visible_branches" in data: check = check + 1
			if "connection_display_collapsable" in data: check = check + 1
			if "connection_display_bold_current_chat" in data: check = check + 1
			if "connection_display_underline_current_chat" in data: check = check + 1
			if "connection_display_italic_current_chat" in data: check = check + 1
			if "connection_display_uptime_in_seconds" in data: check = check + 1
			if "system_tray_icon" in data: check = check + 1
			if "system_tray_icon_click_to_hide_or_show" in data: check = check + 1
			if "system_tray_icon_menu" in data: check = check + 1
			if "system_tray_mark_unread" in data: check = check + 1
			if "system_tray_allow_disconnect" in data: check = check + 1
			if "system_tray_allow_connect" in data: check = check + 1
			if "system_tray_display_connections" in data: check = check + 1
			if "elide_topic_display" in data: check = check + 1

			if check == 142:
				return True
			else:
				return False
	return False