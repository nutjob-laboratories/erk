
from erk.config import *

APPLICATION_NAME = "Ərk"
APPLICATION_MAJOR_VERSION = "0.600"
APPLICATION_VERSION = APPLICATION_MAJOR_VERSION + "." + MINOR_VERSION
OFFICIAL_REPOSITORY = "https://github.com/nutjob-laboratories/erk"
PROGRAM_FILENAME = "erk.py"
NORMAL_APPLICATION_NAME = "Erk"

CONNECT_MENU_NAME = "Connect"
CONNECT_MENU_DESCRIPTION = "Connect to an IRC server"

NETWORK_MENU_NAME = "Networks"
NETWORK_MENU_DESCRIPTION = "Select server from a list"

RESTART_MENU_NAME = "Restart"

EXIT_MENU_NAME = "Exit"

DISPLAY_MENU_NAME = "Settings"

WINDOWS_MENU_NAME = "Windows"

FONT_MENU_NAME = "Font"
FONT_MENU_DESCRIPTION = "Set application font"

WINDOW_SIZE_MENU_NAME = "Window size"
WINDOW_SIZE_MENU_DESCRIPTION = "Set initial window size"

MESSAGES_MENU_NAME = "Message displays"

MESSAGES_IRCCOLOR_MENU_NAME = "Display IRC colors"
MESSAGES_HTML_MENU_NAME = "Strip HTML from messages"
MESSAGE_LINK_MENU_NAME = "Convert URLs into hyperlinks"
MESSAGE_PROFANITY_MENU_NAME = "Filter profanity"
MESSAGE_AUTO_CREATE_NAME = "Create windows for incoming private messages"
MESSAGE_FLASH_PRIVATE_NAME = "Unread private messages flash taskbar"

MESSAGE_MARK_UNSEEN_MENU_NAME = "Mark unread messages"

MESSAGE_CLICKABLE_NICKNAME_NAME = "Clickable nicknames"

MISC_DOUBLE_CLICK_NICKNAME_USERLIST = "Double click nickname to open private window"

TIMESTAMP_MENU_NAME = "Timestamps"

TIMESTAMP_DISPLAY_MENU_NAME = "Display"
TIMESTAMP_SECONDS_MENU_NAME = "Show seconds"
TIMESTAMP_24HOUR_MENU_NAME = "24-hour clock"

USERLIST_MENU_NAME = "User displays"

CONNECTION_DISPLAY_MENU_NAME = "Connection display"
CONNECTION_DISPLAY_WEST = "left side"
CONNECTION_DISPLAY_EAST = "right side"
CONNECTION_DISPLAY_VISIBLE = "Enabled"

MISC_EXPAND_NODE_ON_CONNECT = "Expand servers on connection"
CONNECTION_DISPLAY_UPTIME = "Display server uptime"
CONNECTION_DISPLAY_LOCATION = "Put display on the..."

SAVE_CHANNEL_MENU_NAME = "Save joined channels"
SAVE_HISTORY_MENU_NAME = "Save connection history"

MISC_MENU_NAME = "Miscellaneous"
PLAIN_USERS_MENU_NAME = "Text only"

TEXT_ENTRY_MENU_NAME = "Text entry"

DISPLAY_NICK_MENU_NAME = "Display nickname"
CLICK_NICK_MENU_NAME = "Click nickname to change"

MENU_ALWAYS_ON_TOP = "Always on top"

TITLE_FROM_ACTIVE_WINDOW_NAME = "Set title from active window"

SPELLCHECK_MENU_NAME = "Spell Check"
SPELLCHECK_ENABLE_NAME = "Enable"

SPELLCHECK_LANGUAGE_ENGLISH = "English"
SPELLCHECK_LANGUAGE_FRENCH = "French"
SPELLCHECK_LANGUAGE_SPANISH = "Spanish"
SPELLCHECK_LANGUAGE_GERMAN = "German"

ADD_CHANNEL_DIALOG_TITLE = "Add channel"
ADD_CHANNEL_DIALOG_CHANNEL_NAME = "Channel"
ADD_CHANNEL_DIALOG_CHANNEL_KEY = "Key"

CONNECT_DIALOG_TITLE = "Connect to IRC"

CONNECT_DIALOG_SSL_NAME = "Connect via SSL/TLS"

CONNECT_AND_NETWORK_DIALOG_RECONNECT_NAME = "Reconnect on disconnection"
CONNECT_AND_NETWORK_DIALOG_AUTOJOIN_NAME = "Automatically join channels"


CONNECT_AND_NETWORK_DIALOG_SERVER_TAB_NAME = "Server"
CONNECT_AND_NETWORK_DIALOG_USER_TAB_NAME = "User"
CONNECT_AND_NETWORK_DIALOG_CHANNEL_TAB_NAME = "Channel"

NETWORK_DIALOG_TITLE = "Connect to IRC"

NETWORK_DIALOG_SELECT_TITLE = "Select an IRC server"

NETWORK_DIALOG_CONNECTION_VIA_SSL_TEXT = "<i>Connect via</i> <b>SSL/TLS</b> <i>to port</i> <b>{}</b>"
NETWORK_DIALOG_CONNECTION_VIA_TCP_TEXT = "<i>Connect via</i> <b>TCP/IP</b> <i>to port</i> <b>{}</b>"

WINDOW_SIZE_DIALOG_TITLE = "Initial window size"
WINDOW_SIZE_WIDTH_NAME = "Width"
WINDOW_SIZE_HEIGHT_NAME = "Height"

EMOJI_MENU_NAME = "Emoji shortcodes"
EMOJI_MENU_USE_EMOJIS_NAME = "Enable emoji shortcodes"
EMOJI_MENU_USE_ASCIIMOJIS_NAME = "Enable ASCIImoji shortcodes"

AUTOCOMPLETE_MENU_NAME = "Autocomplete"
AUTOCOMPLETE_MENU_NICKS_NAME = "Nicknames"
AUTOCOMPLETE_MENU_EMOJIS_NAME = "Emoji shortcodes"
AUTOCOMPLETE_MENU_ASCIIMOJIS_NAME = "ASCIImoji shortcodes"
AUTOCOMPLETE_MENU_COMMANDS_NAME = "Commands"

CONNECTIONS_MENU_CHANGE_NICK = "Change nickname"
CONNECTIONS_MENU_JOIN_CHANNEL = "Join a channel"
CONNECTIONS_MENU_DISCONNECT = "Disconnect"

MENU_CASCADE_WINDOWS_NAME = "Cascade windows"
MENU_TILE_WINDOWS_NAME = "Tile windows"

NICK_DIALOG_TITLE = "Change Nickname"
NICK_DIALOG_LABEL = "Nickname"
NICK_DIALOG_SAVE = "Save as new default"

JOIN_DIALOG_TITLE = "Join Channel"
JOIN_DIALOG_CHANNEL_LABEL = "Channel"
JOIN_DIALOG_KEY_LABEL = "Key"

JOIN_COMMAND_HELP = "Usage: /join CHANNEL [KEY]"
MSG_COMMAND_HELP = "Usage: /msg TARGET MESSAGE"
NICK_COMMAND_HELP = "Usage: /nick NICKNAME"
ME_COMMAND_HELP = "Usage: /me MESSAGE"
SEND_COMMAND_HELP = "Usage: /send MESSAGE"
PART_COMMAND_HELP = "Usage: /part CHANNEL [MESSAGE]"

JOIN_COMMAND = "/join"
MSG_COMMAND = "/msg"
NICK_COMMAND = "/nick"
ME_COMMAND = "/me"
SEND_COMMAND = "/send"
PART_COMMAND = "/part"
QUIT_COMMAND = "/quit"

CONSOLE_SERVER_CONFIG_MENU_NAME = "Configuration"
CONSOLE_COMMAND_MENU_NAME = "Commands"

CONFIG_MAX_CHANNELS = "Maximum channels"
CONFIG_MAX_NICK_LEN = "Maximum nickname length"
CONFIG_MAX_CHANNEL_LEN = "Maximum channel name length"
CONFIG_MAX_TOPIC_LEN = "Maximum topic length"
CONFIG_MAX_KICK_LEN = "Maximum kick message length"
CONFIG_MAX_AWAY_LEN = "Maximum away message length"
CONFIG_MAX_MSG_TARGETS = "Maximum number of message targets"
CONFIG_MAX_MODES_PER_USER = "Maximum modes per user"
CONFIG_MAX_MODES = "Maximum modes"
CONFIG_COMMANDS = "Commands"
CONFIG_SUPPORTS = "Supports"
CONFIG_CHANNEL_MODES = "Channel modes"
CONFIG_PREFIXES = "Status prefixes"

CONSOLE_MENU_CHANGE_NICK = "Change nickname"
CONSOLE_MENU_JOIN_CHANNEL = "Join a channel"
CONSOLE_MENU_DISCONNECT = "Disconnect"

LABEL_LENGTH = 10
NICK_LABEL = "Nickname"
ALTERNATE_LABEL = "Alternate"
USERNAME_LABEL = "Username"
REALNAME_LABEL = "Real Name"

HOST_LABEL = "Host"
PORT_LABEL = "Port"
PASSWORD_LABEL = "Password"

HELP_MENU_NAME = "Help"
ABOUT_MENU_NAME = "About "+APPLICATION_NAME

EMOJI_LIST_MENU_NAME = "Emoji shortcode list"
ASCIIMOJI_LIST_MENU_NAME = "ASCIImoji shortcode list"

FORMAT_MENU_NAME = "Text"
FORMAT_MENU_DESCRIPTION = "Set text colors & styles"

FORMAT_DIALOG_OK_BUTTON = "Apply"
FORMAT_DIALOG_RESTART_BUTTON = "Apply and Restart"
FORMAT_DIALOG_DEFAULTS_BUTTON = "Defaults"
FORMAT_DIALOG_CANCEL_BUTTON = "Cancel"
FORMAT_DIALOG_WARNING = "<small>Some settings may require restarting to take effect</small>"

FORMAT_DIALOG_NOTICE = "Notice usernames"
FORMAT_DIALOG_OTHER = "Other usernames"
FORMAT_DIALOG_SELF = "Your username"
FORMAT_DIALOG_EXAMPLE_TEXT = 'Lorem ipsum dolor sit amet'
FORMAT_DIALOG_MOTD = "An example of an MOTD message"
FORMAT_DIALOG_HYPERLINK = "An example hyperlink"
FORMAT_DIALOG_ERROR = "An example error message"
FORMAT_DIALOG_ACTION = "An example action message"

FORMAT_DIALOG_SYSTEM = "A example system message"
FORMAT_DIALOG_COLOR = "Color"
FORMAT_DIALOG_BOLD = "Bold"
FORMAT_DIALOG_ITALIC = "Italic"
FORMAT_DIALOG_BG_COLOR = "Background Color"
FORMAT_DIALOG_TXT_COLOR = "Text Color"

FORMAT_DIALOG_TITLE = "Text"

LOGGING_MENU_NAME = "Automatic logging"
LOGGING_MENU_CONSOLE = "Console windows"
LOGGING_MENU_CHANNEL = "Channel windows"
LOGGING_MENU_PRIVATE = "Private windows"
LOGGING_MENU_LENGTH = "Set log display length"
LOGGING_MENU_MARK_END = "Mark end of loaded logs"

LOGGING_MENU_SAVE = "Save logs"
LOGGING_MENU_LOAD = "Load and display logs"

NOTIFICATION_MENU_NAME = "Notifications"

NOTIFICATION_MENU_FAILED = "Notify on failed connections"
NOTIFICATION_MENU_LOST = "Notify on lost connections"

LOGGING_MENU_SAVE_ALL_LOGS = "Save all logs"
LOGGING_MENU_LOAD_ALL_LOGS = "Load and display all logs"

NETWORK_SETTINGS_MENU_NAME = "Network traffic display"
GET_HOSTMASKS_MENU_NAME = "Retrieve hostmasks on join"

TRAFFIC_MAX_LINE_MENU_NAME = "Set maximum line count in network traffic display"
NET_TRAFFIC_MENU_NAME = "View network traffic"
MOTD_VIEW_MENU_NAME = "View MOTD"

MODE_NO_KNOWN = "No known modes set"
MODE_OPS_TOPIC = "Only operators can change topic"
MODE_SECRET = "Channel is secret"
MODE_PRIVATE = "Channel is private"
MODE_NO_EXTERNAL = "External messages forbidden"
MODE_MODERATED = "Channel is moderated"
MODE_CTCP_BAN = "CTCP is forbidden"
MODE_NO_COLORS = "IRC colors forbidden"
MODE_KEY = "Channel key:"

TOPIC_COMMAND = "/topic"
TOPIC_COMMAND_HELP = "Usage: /topic [CHANNEL] TEXT"
TOPIC_COMMAND_PRIVATE_HELP = "Usage: /topic CHANNEL TEXT"
PRIVATE_TOPIC_ERROR = "Private message windows don't have a topic"
TOPIC_COMMAND_NOT_CHANNEL_ERROR = "\"{}\" is not a valid channel name"
CONSOLE_TOPIC_ERROR = "Server windows don't have a topic"

AWAY_COMMAND = "/away"
AWAY_COMMAND_DEFAULT_MESSAGE = "Away"

BACK_COMMAND = "/back"
BACK_COMMAND_HELP = "Usage: /back"

CHANNEL_WINDOW_MENU_NAME = "Channel windows"
CHANNEL_MODE_MENU_NAME = "Show channel mode menu"
CHANNEL_BAN_MENU_NAME = "Show channel ban menu"
