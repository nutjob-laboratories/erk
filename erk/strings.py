
from erk.config import *

APPLICATION_NAME = "Ərk"
APPLICATION_MAJOR_VERSION = "0.600"
APPLICATION_VERSION = APPLICATION_MAJOR_VERSION + "." + MINOR_VERSION
OFFICIAL_REPOSITORY = "https://github.com/nutjob-laboratories/erk"
PROGRAM_FILENAME = "erk.py"
NORMAL_APPLICATION_NAME = "Erk"


IRC_MESSAGE_SELF_NAME_CHANGE = "You are now known as {}"
IRC_MESSAGE_CONNECTED = "Connected to {}"
IRC_MESSAGE_REGISTERED = "Registered with {}"
IRC_MESSAGE_MODE_SET = "Mode +{} set on {}"
IRC_MESSAGE_MODE_UNSET = "Mode -{} set on {}"

IRC_MESSAGE_KEY_SET = "{} set {}'s key to \"{}\""
IRC_MESSAGE_KEY_UNSET = "{} unset {}'s key"

IRC_MESSAGE_GRANT_OP = "{} granted {} operator status to {}"
IRC_MESSAGE_REMOVE_OP = "{} took {} operator status from {}"

IRC_MESSAGE_GRANT_VOICE = "{} granted {} voiced status to {}"
IRC_MESSAGE_REMOVE_VOICE = "{} took {} voiced status from {}"

IRC_MESSAGE_BAN = "{} banned {} from {}"
IRC_MESSAGE_UNBAN = "{} unbanned {} from {}"

IRC_MESSAGE_USER_MODE_SET =  "{} set +{} in {}"
IRC_MESSAGE_USER_MODE_UNSET =  "{} set -{} in {}"

IRC_MESSAGE_JOIN = "{} has joined {}"
IRC_MESSAGE_PART = "{} has left {}"

IRC_MESSAGE_RENAME = "{} is now known as {}"

IRC_MESSAGE_SET_TOPIC = "{} set the channel topic to \"{}\""
IRC_MESSAGE_NO_TOPIC = "{} set the channel topic to nothing"

IRC_MESSAGE_CLIENT_JOIN = "Joined {}"
IRC_MESSAGE_CLIENT_PART = "Left {}"

IRC_MESSAGE_QUIT_NO_MESSAGE = "{} quit IRC"
IRC_MESSAGE_QUIT = "{} quit IRC ({})"

# |=============|
# | GUI STRINGS |
# |=============|

CONNECT_MENU_NAME = "Connect"
CONNECT_MENU_DESCRIPTION = "Connect to an IRC server"

NETWORK_MENU_NAME = "Networks"
NETWORK_MENU_DESCRIPTION = "Select server from a list"

RESTART_MENU_NAME = "Restart"

EXIT_MENU_NAME = "Exit"

DISPLAY_MENU_NAME = "Settings"

WINDOWS_MENU_NAME = "Windows"

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

#MISC_MENU_NAME = "Miscellaneous"
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
FORMAT_DIALOG_WARNING = "<small>Some settings may require a restart to take effect</small>"

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

FORMAT_DIALOG_TITLE = "Text format"

LOGGING_MENU_NAME = "Logs"
LOGGING_MENU_CONSOLE = "Console windows"
LOGGING_MENU_CHANNEL = "Channel windows"
LOGGING_MENU_PRIVATE = "Private windows"
LOGGING_MENU_LENGTH = "Set log display length"
LOGGING_MENU_MARK_END = "Mark end of loaded logs"

LOGGING_MENU_SAVE = "Save logs"
LOGGING_MENU_LOAD = "Load logs"

NOTIFICATION_MENU_NAME = "Notifications"

NOTIFICATION_MENU_FAILED = "Notify on failed connections"
NOTIFICATION_MENU_LOST = "Notify on lost connections"

LOGGING_MENU_SAVE_ALL_LOGS = "Automatically save logs"
LOGGING_MENU_LOAD_ALL_LOGS = "Automatically load logs"

NETWORK_SETTINGS_MENU_NAME = "Network traffic display"
GET_HOSTMASKS_MENU_NAME = "Get hostmasks on channel join"

TRAFFIC_MAX_LINE_MENU_NAME = "Set maximum lines to display"
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

ACTIVE_CONNECTIONS_LABEL = "Connected Servers"

WHOIS_COMMAND = "/whois"
WHOIS_COMMAND_HELP = "Usage: /whois NICKNAME [SERVER]"

INVITE_COMMAND = "/invite"
INVITE_COMMAND_HELP = "Usage: /invite NICKNAME CHANNEL"

USERLIST_CONTEXT_OP = "Channel operator"
USERLIST_CONTEXT_VOICE = "Voiced user"
USERLIST_CONTEXT_NORMAL = "Normal user"

USERLIST_CONTEXT_OP_ACT = "Operator Actions"
USERLIST_CONTEXT_TAKE_OP = "Take op status"
USERLIST_CONTEXT_GIVE_OP = "Give op status"
USERLIST_CONTEXT_TAKE_VOICE = "Take voiced status"
USERLIST_CONTEXT_GIVE_VOICE = "Give voiced status"
USERLIST_CONTEXT_KICK = "Kick"
USERLIST_CONTEXT_BAN = "Ban"
USERLIST_CONTEXT_KICK_BAN = "Kick/Ban"
USERLIST_CONTEXT_WHOIS = "WHOIS"
USERLIST_CONTEXT_OPEN_WIN = "Open chat window"
USERLIST_CONTEXT_PRIV = "Send private message"
USERLIST_CONTEXT_COPY = "Copy to clipboard"
USERLIST_CONTEXT_CNICK = "Nickname"
USERLIST_CONTEXT_CHOST = "Hostmask"
USERLIST_CONTEXT_CLIST = "User list"
USERLIST_CONTEXT_CTOPIC = "Channel topic"

OPER_COMMAND = "/oper"
OPER_COMMAND_HELP = "Usage: /oper USERNAME PASSWORD"

IGNORE_COMMAND = "/ignore"
IGNORE_COMMAND_HELP = "Usage: /ignore USER"

UNIGNORE_COMMAND = "/unignore"
UNIGNORE_COMMAND_HELP = "Usage: /unignore USER"

CPRIVMSG_COMMAND = "/cprivmsg"
CPRIVMSG_COMMAND_HELP = "Usage: /cprivmsg NICKNAME CHANNEL MESSAGE"

CNOTICE_COMMAND = "/cnotice"
CNOTICE_COMMAND_HELP = "Usage: /cnotice NICKNAME CHANNEL MESSAGE"

CPRIV_CNOTICE_NOT_SUPPORTED = "This server does not support the {} command"

TIME_COMMAND = "/time"
TIME_COMMAND_HELP = "Usage: /time [SERVER]"

BEGIN_USERHOST_DATA = "Begin userhost information"
END_USERHOST_DATA = "End userhost information"

USERHOST_COMMAND = "/userhost"
USERHOST_COMMAND_HELP = "Usage: /userhost NICK [NICK ...]"

KNOCK_COMMAND = "/knock"
KNOCK_COMMAND_HELP = "Usage: /knock CHANNEL [MESSAGE]"

MODE_INVITE_ONLY = "Channel is invite only"

FONT_MENU_NAME = "Font ({}, {}pt)"
FORMAT_MENU_NAME = "Text formatting"
WINSIZE_MENU_NAME = "Set initial window size"

SERVMSG_MENU_NAME = "Hide server messages"

CONNECTION_MENU_NAME = "Connections"
IGNORE_MENU_NAME = "Ignored users"

TRAFFIC_START_MENU_NAME = "Show on connection"

SAVE_IGNORE_MENU_NAME = "Save ignored users"

ENABLE_CMD_HISTORY_MENU_NAME = "Enable command history"
CMD_HISTORY_LEN_MENU_NAME = "Set command history length"

LOGGING_WIN_TYPE_MENU_SEPARATOR = "Settings by window type"

BAN_MENU_ENTRY = "<b>{}</b> (by {})"

USERLIST_CONTEXT_UNIGNORE = "Unignore user"
USERLIST_CONTEXT_IGNORE = "Ignore user"

CHAT_DISPLAY_CONTEXT_SET_TOPIC = "Set topic"
CHAT_DISPLAY_CONTEXT_RKEY = "Remove channel key"
CHAT_DISPLAY_CONTEXT_KEY = "Set channel key"
CHAT_DISPLAY_CONTEXT_ATOPIC = "Allow anyone to set topic"
CHAT_DISPLAY_CONTEXT_OTOPIC = "Allow only operators to set topic"
CHAT_DISPLAY_CONTEXT_UMOD = "Unmoderate channel"
CHAT_DISPLAY_CONTEXT_MOD = "Moderate channel"
CHAT_DISPLAY_CONTEXT_ACOLOR = "Allow IRC color codes"
CHAT_DISPLAY_CONTEXT_COLOR = "Forbid IRC color codes"
CHAT_DISPLAY_CONTEXT_AEXTMSG = "Allow external messages"
CHAT_DISPLAY_CONTEXT_EXT_MSG = "Forbid external messages"
CHAT_DISPLAY_CONTEXT_ACTCP = "Allow CTCP messages"
CHAT_DISPLAY_CONTEXT_CTCP = "Forbid CTCP messages"
CHAT_DISPLAY_CONTEXT_APUB = "Make channel public"
CHAT_DISPLAY_CONTEXT_PUB = "Make channel secret"
CHAT_DISPLAY_CONTEXT_AINVITE = "Remove channel invite requirement"
CHAT_DISPLAY_CONTEXT_INVITE = "Make channel invite only"

MACRO_NOT_ENOUGH_ARGS = "Not enough arguments to {} (minimum {} argument(s))"
MACRO_TOO_MANY_ARGS = "Too many arguments to {} (minimum {} argument(s))"

NET_DISPLAY_HIDE_MENU_NAME = "Hide instead of closing window"