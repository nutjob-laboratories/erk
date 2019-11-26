
SSL_AVAILABLE = True
try:
	import ssl
except ImportError:
	SSL_AVAILABLE = False

import erk.dialogs.add_channel as AddChannelDialog
import erk.dialogs.connect as Connect
import erk.dialogs.network as Network
import erk.dialogs.window_size as WindowSize
import erk.dialogs.new_nick as NewNick
import erk.dialogs.join_channel as JoinChannel
import erk.dialogs.about as About
import erk.dialogs.format as Format
import erk.dialogs.log_display_size as Linecount
import erk.dialogs.topic as Topic
import erk.dialogs.key as Key

from erk.resources import *


def CmdHistoryLengthDialog(obj):
	x = Linecount.Dialog("Command history size",obj.window_command_history_length,ERK_ICON,obj)
	info = x.get_length_information("Command history size",obj.window_command_history_length,ERK_ICON,obj)
	del x

	if not info: return None
	return info


def KeyDialog(obj):
	x = Key.Dialog(obj)
	info = x.get_key_information(obj)
	del x

	if not info: return None
	return info

def TopicDialog(topic,obj):
	x = Topic.Dialog(topic,obj)
	info = x.get_topic_information(topic,obj)
	del x

	if not info: return None
	return info

def IOsizeDialog(obj):
	x = Linecount.Dialog("Maximum lines displayed",obj.max_lines_in_io_display,IO_ICON,obj)
	info = x.get_length_information("Maximum lines displayed",obj.max_lines_in_io_display,IO_ICON,obj)
	del x

	if not info: return None
	return info

def LogsizeDialog(obj):
	x = Linecount.Dialog("Log display size",obj.load_log_max,LOG_ICON,obj)
	info = x.get_length_information("Log display size",obj.load_log_max,LOG_ICON,obj)
	del x

	if not info: return None
	return info

def FormatDialog(obj):
	x = Format.Dialog(obj)
	x.show()

def AboutDialog(obj):
	x = About.Dialog(obj)
	x.show()

def ConnectDialog(obj):
	x = Connect.Dialog(SSL_AVAILABLE,obj)
	info = x.get_connect_information(SSL_AVAILABLE,obj)
	del x

	if not info: return None
	return info

def NetworkDialog(obj):
	x = Network.Dialog(SSL_AVAILABLE,obj)
	info = x.get_connect_information(SSL_AVAILABLE,obj)
	del x

	if not info: return None
	return info

def WindowSizeDialog(obj):
	x = WindowSize.Dialog(obj)
	info = x.get_window_information(obj)
	del x

	if not info: return None
	return info

def NewNickDialog(nick,obj):
	x = NewNick.Dialog(nick,obj)
	info = x.get_nick_information(nick,obj)
	del x

	if not info: return None
	return info

def JoinChannelDialog(obj):
	x = JoinChannel.Dialog(obj)
	info = x.get_channel_information(obj)
	del x

	if not info: return None
	return info
