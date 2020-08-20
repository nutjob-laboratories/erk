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

from .add_channel import Dialog as AddChannelDialog
from .combo import Dialog as Combo
from .join_channel import Dialog as JoinChannel
from .new_nick import Dialog as Nick
from .window_size import Dialog as WindowSize
from .history_size import Dialog as HistorySize
from .log_size import Dialog as LogSize
from .format import Dialog as FormatText
from .about import Dialog as About
from .macro import Dialog as Macro
from .editor import Window as Editor
from .export_log import Dialog as ExportLog
from .key import Dialog as Key
from .error import Dialog as Error
from .prefix import Dialog as Prefix
from .list_time import Dialog as ListTime

from .plugin_input import Dialog as PluginInput

def PluginInputDialog(title,text):
	x = PluginInput(title,text)
	info = x.get_input_information(title,text)
	del x

	if not info: return None
	return info

def ListTimeDialog():
	x = ListTime()
	info = x.get_entry_information()
	del x

	if not info: return None
	return info

def PrefixDialog():
	x = Prefix()
	info = x.get_system_information()
	del x

	if not info: return None
	return info

def KeyDialog():
	x = Key()
	info = x.get_channel_information()
	del x

	if not info: return None
	return info

def ExportLogDialog(obj):
	x = ExportLog(obj)
	info = x.get_name_information(obj)
	del x

	if not info: return None
	return info

def ErrorDialog(obj,errlist=None):
	x = Error(errlist,obj)
	x.resize(400,250)
	x.show()

def EditorDialog(obj=None,filename=None,app=None,config=None):
	x = Editor(filename,obj,app,config)
	return x

def MacroDialog(obj,filename=None):
	x = Macro(filename,obj)
	x.show()

def AboutDialog():
	x = About()
	x.show()
	return x

def FormatTextDialog(obj):
	x = FormatText(obj)
	x.show()

def LogSizeDialog():
	x = LogSize()
	info = x.get_entry_information()
	del x

	if not info: return None
	return info

def HistorySizeDialog():
	x = HistorySize()
	info = x.get_entry_information()
	del x

	if not info: return None
	return info

def WindowSizeDialog(obj):
	x = WindowSize(obj)
	info = x.get_window_information(obj)
	del x

	if not info: return None
	return info

def NickDialog(nick,obj):
	x = Nick(nick,obj)
	info = x.get_nick_information(nick,obj)
	del x

	if not info: return None
	return info

def JoinDialog():
	x = JoinChannel()
	info = x.get_channel_information()
	del x

	if not info: return None
	return info

def ComboDialog(userfile):
	x = Combo(SSL_AVAILABLE,userfile)
	info = x.get_connect_information(SSL_AVAILABLE,userfile)
	del x

	if not info: return None
	return info


