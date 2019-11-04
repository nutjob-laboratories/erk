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

from erk.common import *
import emoji

_GUI_OBJECT = None
_IRC_OBJECT = None

def SET_IRC_OBJECT(obj):
	global _IRC_OBJECT
	_IRC_OBJECT = obj

def SET_GUI_OBJECT(obj):
	global _GUI_OBJECT
	_GUI_OBJECT = obj

class ERKInterfaceObject():

	def __init__(self):
		pass

	def fetch(self,id):
		for c in _GUI_OBJECT.connections:
			if c.id==id:
				return IRCConnectionObject(c.connection)
		return None

	def fetchAll(self):
		conns = []
		for c in _GUI_OBJECT.connections:
			conns.append(IRCConnectionObject(c.connection))
		return conns

	def textWindow(self,title,contents=None):
		win = TextWindow(title,_GUI_OBJECT.MDI,None,_GUI_OBJECT)
		if contents: win.write(contents)
		return win

	def active(self,message,log=False):

		if _GUI_OBJECT.use_emojis: message = emoji.emojize(message,use_aliases=True)
		if _GUI_OBJECT.use_asciimojis: message = inject_asciiemojis(message)

		msg = render_system(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[SYSTEM_STYLE_NAME],message )
		try:
			w = _GUI_OBJECT.MDI.activeSubWindow()
			win = w.window
			win.writeText(msg)
			if log: win.add_to_log('',message)
		except:
			pass

	def channel(self,name,message,log=False):

		if _GUI_OBJECT.use_emojis: message = emoji.emojize(message,use_aliases=True)
		if _GUI_OBJECT.use_asciimojis: message = inject_asciiemojis(message)

		msg = render_system(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[SYSTEM_STYLE_NAME],message )
		_GUI_OBJECT.writeToChannel(_IRC_OBJECT,name,pmsg)
		if log: _GUI_OBJECT.writeToChannelLog(_IRC_OBJECT,name,GLYPH_ACTION+_IRC_OBJECT.nickname,msg)

	def console(self,message,log=False):

		if _GUI_OBJECT.use_emojis: message = emoji.emojize(message,use_aliases=True)
		if _GUI_OBJECT.use_asciimojis: message = inject_asciiemojis(message)

		msg = render_system(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[SYSTEM_STYLE_NAME],message )
		self.writeToConsole(_IRC_OBJECT,msg)
		if log: self.writeToConsoleLog(_IRC_OBJECT,'',message)

class IRCConnectionObject():

	def __init__(self,connection=None):
		self.connection = connection

	def send(self,msg):
		if self.connection:
			self.connection.sendLine(msg)
		else:
			_IRC_OBJECT.sendLine(msg)

	def nickname(self):
		if self.connection:
			return self.connection.nickname
		else:
			return _IRC_OBJECT.nickname

	def id(self):
		if self.connection:
			return self.connection.id
		else:
			return _IRC_OBJECT.id

	def server(self):
		if self.connection:
			return self.connection.server
		else:
			return _IRC_OBJECT.server

	def port(self):
		if self.connection:
			return self.connection.port
		else:
			return _IRC_OBJECT.port

	def part(self,channel,msg=None):
		if msg:
			if _GUI_OBJECT.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if _GUI_OBJECT.use_asciimojis: msg = inject_asciiemojis(msg)
			if self.connection:
				self.connection.part(channel,msg)
				_GUI_OBJECT.irc_parting(self.connection,channel)
			else:
				_IRC_OBJECT.part(channel,msg)
				_GUI_OBJECT.irc_parting(_IRC_OBJECT,channel)
		else:
			if self.connection:
				self.connection.part(channel)
				_GUI_OBJECT.irc_parting(self.connection,channel)
			else:
				_IRC_OBJECT.part(channel)
				_GUI_OBJECT.irc_parting(_IRC_OBJECT,channel)
		

	def join(self,channel,key=None):
		if key:
			if self.connection:
				self.connection.join(channel,key)
			else:
				_IRC_OBJECT.join(channel,key)
		else:
			if self.connection:
				self.connection.join(channel)
			else:
				_IRC_OBJECT.join(channel)

	def action(self,target,message,display=True):

		if _GUI_OBJECT.use_emojis: message = emoji.emojize(message,use_aliases=True)
		if _GUI_OBJECT.use_asciimojis: message = inject_asciiemojis(message)

		if self.connection:
			# Send the IRC message
			self.connection.describe(target,message)
			
			if display:
				# Display it in the GUI
				msg = render_system(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[ACTION_STYLE_NAME],self.connection.nickname+" "+message )
				_GUI_OBJECT.writeToChannel(self.connection,obj.name,pmsg)
				_GUI_OBJECT.writeToChannelLog(self.connection,obj.name,GLYPH_ACTION+self.connection.nickname,msg)
		else:
			# Send the IRC message
			_IRC_OBJECT.describe(target,message)
			
			if display:
				# Display it in the GUI
				msg = render_system(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[ACTION_STYLE_NAME],_IRC_OBJECT.nickname+" "+message )
				_GUI_OBJECT.writeToChannel(_IRC_OBJECT,obj.name,pmsg)
				_GUI_OBJECT.writeToChannelLog(_IRC_OBJECT,obj.name,GLYPH_ACTION+_IRC_OBJECT.nickname,msg)

	def notice(self,target,message,display=True):

		if _GUI_OBJECT.use_emojis: message = emoji.emojize(message,use_aliases=True)
		if _GUI_OBJECT.use_asciimojis: message = inject_asciiemojis(message)

		if self.connection:
			# Send the IRC message
			self.connection.notice(target,message)
			
			if display:
				# Display it in the GUI
				msg = render_message(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[SELF_STYLE_NAME],self.connection.nickname,_GUI_OBJECT.styles[NOTICE_TEXT_STYLE_NAME],message )
				_GUI_OBJECT.writeToChannel(self.connection,target,msg)
				_GUI_OBJECT.writeToChannelLog(self.connection,target,GLYPH_SELF+self.connection.nickname,message)
		else:
			# Send the IRC message
			_IRC_OBJECT.notice(target,message)
			
			if display:
				# Display it in the GUI
				msg = render_message(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[SELF_STYLE_NAME],_IRC_OBJECT.nickname,_GUI_OBJECT.styles[NOTICE_TEXT_STYLE_NAME],message )
				_GUI_OBJECT.writeToChannel(_IRC_OBJECT,target,msg)
				_GUI_OBJECT.writeToChannelLog(_IRC_OBJECT,target,GLYPH_SELF+_IRC_OBJECT.nickname,message)

	def privmsg(self,target,message,display=True):

		if _GUI_OBJECT.use_emojis: message = emoji.emojize(message,use_aliases=True)
		if _GUI_OBJECT.use_asciimojis: message = inject_asciiemojis(message)

		if self.connection:
			# Send the IRC message
			self.connection.msg(target,message)
			
			if display:
				# Display it in the GUI
				msg = render_message(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[SELF_STYLE_NAME],self.connection.nickname,_GUI_OBJECT.styles[MESSAGE_STYLE_NAME],message )
				_GUI_OBJECT.writeToChannel(self.connection,target,msg)
				_GUI_OBJECT.writeToChannelLog(self.connection,target,GLYPH_SELF+self.connection.nickname,message)
		else:
			# Send the IRC message
			_IRC_OBJECT.msg(target,message)
			
			if display:
				# Display it in the GUI
				msg = render_message(_GUI_OBJECT, _GUI_OBJECT.styles[TIMESTAMP_STYLE_NAME],_GUI_OBJECT.styles[SELF_STYLE_NAME],_IRC_OBJECT.nickname,_GUI_OBJECT.styles[MESSAGE_STYLE_NAME],message )
				_GUI_OBJECT.writeToChannel(_IRC_OBJECT,target,msg)
				_GUI_OBJECT.writeToChannelLog(_IRC_OBJECT,target,GLYPH_SELF+_IRC_OBJECT.nickname,message)

ERK = ERKInterfaceObject()
IRC = IRCConnectionObject()
HEAP = {}
