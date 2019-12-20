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
import erk.dialogs.about as About

import erk.dialogs.macro as Macro

def MacroDialog(obj,filename=None):
	x = Macro.Dialog(filename,obj)
	x.show()

def AboutDialog():
	x = About.Dialog()
	x.show()
	return x

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


