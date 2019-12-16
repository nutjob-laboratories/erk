
SSL_AVAILABLE = True
try:
	import ssl
except ImportError:
	SSL_AVAILABLE = False

import erk.dialogs.add_channel as AddChannelDialog
import erk.dialogs.combo as Combo
import erk.dialogs.join_channel as JoinChannel
import erk.dialogs.new_nick as Nick
import erk.dialogs.window_size as WindowSize
import erk.dialogs.history_size as HistorySize
import erk.dialogs.log_size as LogSize
import erk.dialogs.format as FormatText

def FormatTextDialog(obj):
	x = FormatText.Dialog(obj)
	x.show()

def LogSizeDialog():
	x = LogSize.Dialog()
	info = x.get_entry_information()
	del x

	if not info: return None
	return info

def HistorySizeDialog():
	x = HistorySize.Dialog()
	info = x.get_entry_information()
	del x

	if not info: return None
	return info

def WindowSizeDialog():
	x = WindowSize.Dialog()
	info = x.get_window_information()
	del x

	if not info: return None
	return info

def NickDialog(nick):
	x = Nick.Dialog(nick)
	info = x.get_nick_information(nick)
	del x

	if not info: return None
	return info

def JoinDialog():
	x = JoinChannel.Dialog()
	info = x.get_channel_information()
	del x

	if not info: return None
	return info

def ComboDialog():
	x = Combo.Dialog(SSL_AVAILABLE)
	info = x.get_connect_information(SSL_AVAILABLE)
	del x

	if not info: return None
	return info


