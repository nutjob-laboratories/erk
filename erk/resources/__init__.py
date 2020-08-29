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

# Load in resource file
globals()["erk.resources.resources"] = __import__("erk.resources.resources")

ERK_ICON = ":/gui-erk.png"
LOGO_IMAGE = ":/gui-logo.png"
DEFAULT_FONT = ":/font-DejaVuSansMono.ttf"

USERLIST_OPERATOR_ICON		= ":/gui-ulist_op.png"
USERLIST_VOICED_ICON		= ":/gui-ulist_voice.png"
USERLIST_OWNER_ICON 		= ":/gui-ulist_owner.png"
USERLIST_ADMIN_ICON 		= ":/gui-ulist_admin.png"
USERLIST_HALFOP_ICON 		= ":/gui-ulist_halfop.png"
USERLIST_NORMAL_ICON		= ":/gui-chanuser.png"

HORIZONTAL_RULE_BACKGROUND = ":/gui-horizontal_rule.png"

MENU_INSTALL_ICON = ":/install.png"
MENU_EDITOR_ICON = ":/editor.png"
MENU_MACRO_ICON = ":/macro.png"
MENU_PACKAGE_ICON = ":/package.png"
MENU_ARCHIVE_ICON = ":/archive.png"
MENU_INSERT_ICON = ":/insert.png"

PDF_ICON = ":/gui-pdf.png"

RCHECKED_ICON = ":/gui-rchecked.png"
RUNCHECKED_ICON = ":/gui-runchecked.png"

SERVER_ICON = ":/gui-server.png"
CHANNEL_ICON = ":/gui-channel.png"
EXIT_ICON = ":/gui-exit.png"
NICK_ICON = ":/gui-nick.png"
CHECKED_ICON = ":/gui-checked.png"
UNCHECKED_ICON = ":/gui-unchecked.png"
QUIT_ICON = ":/gui-quit.png"
TIMESTAMP_ICON = ":/gui-timestamp.png"
SPELLCHECK_ICON = ":/gui-spellcheck.png"
FONT_ICON = ":/gui-font.png"
SPINNER_ANIMATION = ":/gui-spinner.gif"
TOOLBAR_ICON = ":/gui-toolbar.png"
CONNECT_MENU_ICON = ":/connect.png"
UPTIME_ICON = ":/gui-uptime.png"
LEFT_ICON = ":/gui-left.png"
RIGHT_ICON = ":/gui-right.png"
CONNECTION_DISPLAY_ICON = ":/gui-connection_display.png"
RESIZE_ICON = ":/gui-resize.png"
RESTART_ICON = ":/gui-restart.png"
LOG_ICON = ":/gui-log.png"
KEY_ICON = ":/gui-key.png"
NETWORK_ICON = ":/gui-network.png"
AUTOCOMPLETE_ICON = ":/gui-autocomplete.png"
DISCONNECT_ICON = ":/gui-disconnect.png"
MESSAGE_ICON = ":/gui-message.png"
ENTRY_ICON = ":/gui-entry.png"
PLUS_ICON = ":/gui-plus.png"
MINUS_ICON = ":/gui-minus.png"
KICK_ICON = ":/gui-kick.png"
BAN_ICON = ":/gui-ban.png"
KICKBAN_ICON = ":/gui-kickban.png"
CLIPBOARD_ICON = ":/gui-clipboard.png"
WHOIS_ICON = ":/gui-whois.png"
HISTORY_LENGTH_ICON = ":/gui-history_length.png"
FORMAT_ICON = ":/gui-format.png"
ERK_BIG_ICON = ":/gui-erk_button.png"
ABOUT_ICON = ":/gui-about.png"
DOCUMENT_ICON = ":/gui-document.png"
LINK_ICON = ":/gui-link.png"
SETTINGS_ICON = ":/gui-settings.png"
MACRO_ICON = ":/gui-macro.png"
MACRO_FILE_ICON = ":/gui-macro_file.png"
DIRECTORY_ICON = ":/gui-directory.png"
PLUGIN_ICON = ":/gui-plugin.png"
PACKAGE_ICON = ":/gui-package.png"
EDITOR_ICON = ":/gui-editor.png"
NEWFILE_ICON = ":/gui-new_file.png"
OPENFILE_ICON = ":/gui-open_file.png"
SAVEFILE_ICON = ":/gui-save_file.png"
SAVEASFILE_ICON = ":/gui-saveas_file.png"
SELECTALL_ICON = ":/gui-select_all.png"
UNDO_ICON = ":/gui-undo.png"
REDO_ICON = ":/gui-redo.png"
CUT_ICON = ":/gui-cut.png"
COPY_ICON = ":/gui-copy.png"
PASTE_ICON = ":/gui-paste.png"
INDENT_ICON = ":/gui-indent.png"
INSERT_ICON = ":/gui-insert.png"
VISITED_ICON = ":/gui-visited.png"
UNVISITED_ICON = ":/gui-unvisited.png"
LAMBDA_ICON = ":/gui-lambda.png"
ARCHIVE_ICON = ":/gui-archive.png"
INSTALL_ICON = ":/gui-install.png"
UNINSTALL_ICON = ":/gui-uninstall.png"
ERROR_ICON = ":/gui-error.png"
SPACES_ICON = ":/gui-spaces.png"
TABS_ICON = ":/gui-tabs.png"
SHOW_ICON = ":/gui-show.png"
HIDE_ICON = ":/gui-hide.png"
REPLACE_ICON = ":/gui-replace.png"
PRINT_ICON = ":/gui-print.png"
CONSOLE_ICON = ":/gui-console.png"
WINDOW_ICON = ":/gui-window.png"
VERTICAL_RULE_BACKGROUND = ":/gui-vertical_rule.png"
EXPORT_ICON = ":/gui-export.png"
OPTIONS_ICON = ":/gui-options.png"
CONNECTING_ICON = ":/gui-connecting.png"
PREFIX_ICON = ":/gui-prefix.png"
MISC_ICON = ":/gui-misc.png"
