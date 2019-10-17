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

from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore

from erk.common import *
from erk.config import *
from erk.spelledit import *
import erk.input

import erk.dialogs.add_channel as AddChannelDialog
import erk.dialogs.new_nick as NicknameDialog

class Window(QMainWindow):

	def getUserNicks(self):
		return []

	def add_to_log(self,user,msg):
		t = datetime.timestamp(datetime.now())
		e = [t,user,msg]
		self.log.append(e)
		self.newlog.append(e)

	def closeEvent(self, event):

		if self.gui.quitting:

			cid = self.client.server+":"+str(self.client.port)

			self.subwindow.close()
			self.close()
			event.accept()
		elif self.gui.disconnecting:

			cid = self.client.server+":"+str(self.client.port)

			self.subwindow.close()
			self.close()
			self.gui.disconnecting = False
			event.accept()
		else:
			# Don't close the console, just hide it
			self.subwindow.hide()
			event.ignore()

	def handleUserInput(self):
		user_input = self.userTextInput.text()
		self.userTextInput.setText('')

		#print(user_input)
		erk.input.handle_console_input(self,user_input)

	def writeText(self,text):

		self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		self.channelChatDisplay.update()

	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)
		else:
			link = url.toString()

			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)

	def __init__(self,name,window_margin,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.log = []
		self.newlog = []

		self.is_channel = False
		self.is_console = True

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(CONSOLE_WINDOW))

		self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)
		self.channelChatDisplay.setStyleSheet(self.gui.styles["base"])

		self.userTextInput = SpellTextEdit(self)
		self.userTextInput.setObjectName("userTextInput")
		self.userTextInput.returnPressed.connect(self.handleUserInput)
		self.userTextInput.setStyleSheet(self.gui.styles["base"])

		# Text input widget should only be one line
		fm = self.userTextInput.fontMetrics()
		self.userTextInput.setFixedHeight(fm.height()+9)
		self.userTextInput.setWordWrapMode(QTextOption.NoWrap)
		self.userTextInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.userTextInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		finalLayout.addWidget(self.channelChatDisplay)
		finalLayout.addWidget(self.userTextInput)

		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		self.menubar = self.menuBar()
		menuBoldText = self.menubar.font()
		menuBoldText.setBold(True)

		serverMenu = self.menubar.addMenu("Server")
		serverMenu.setFont(menuBoldText)

		self.actNick = QAction(QIcon(USER_ICON),"Nickname",self)
		self.actNick.triggered.connect(self.menuNick)
		serverMenu.addAction(self.actNick)

		self.actJoin = QAction(QIcon(CHANNEL_WINDOW),"Join channel",self)
		self.actJoin.triggered.connect(self.menuJoin)
		serverMenu.addAction(self.actJoin)

		serverMenu.addSeparator()

		self.actDisconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		self.actDisconnect.triggered.connect(self.menuDisconnect)
		serverMenu.addAction(self.actDisconnect)

		# Load logs if necessary
		cid = self.client.server+":"+str(self.client.port)
		if self.gui.load_logs_on_start:
			self.log = loadLog(cid,None)

			if len(self.log)>self.gui.max_displayed_log:
				self.log = trimLog(self.log,self.gui.max_displayed_log)

			# for line in self.log:
			for line in self.log:
				timestamp = line[0]
				user = line[1]
				message = line[2]

				if len(user)>0:
					if GLYPH_ACTION in user:
						user = user.replace(GLYPH_ACTION,'')
						msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["action"],user+" "+message,timestamp )
					elif GLYPH_NOTICE in user:
						user = user.replace(GLYPH_NOTICE,'')
						msg = render_message(self.gui, self.gui.styles["timestamp"],self.gui.styles["notice"],user,self.gui.styles["message"],message,timestamp )
					elif GLYPH_RESUME in user:
						user = user.replace(GLYPH_RESUME,'')
						msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["resume"],message,timestamp )
					elif GLYPH_ERROR in user:
						user = user.replace(GLYPH_ERROR,'')
						msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["error"],message,timestamp )
					else:
						if GLYPH_SELF in user:
							user = user.replace(GLYPH_SELF,'')
							ustyle = self.gui.styles["self"]
						else:
							ustyle = self.gui.styles["username"]
						msg = render_message(self.gui, self.gui.styles["timestamp"],ustyle,user,self.gui.styles["message"],message,timestamp )
				else:
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["system"],message,timestamp )
				self.writeText(msg)

			if len(self.log)>0:
				t = datetime.timestamp(datetime.now())
				# pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')
				pretty = datetime.fromtimestamp(t).strftime('%B %d, %Y at %H:%M:%S')
				msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["resume"],"Resumed on "+pretty )
				self.writeText(msg)
				self.add_to_log(GLYPH_RESUME,"Resumed on "+pretty )

	def rerenderText(self):
		self.channelChatDisplay.clear()
		for line in self.log:
			timestamp = line[0]
			user = line[1]
			message = line[2]

			if len(user)>0:
				if GLYPH_ACTION in user:
					user = user.replace(GLYPH_ACTION,'')
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["action"],user+" "+message,timestamp )
				elif GLYPH_NOTICE in user:
					user = user.replace(GLYPH_NOTICE,'')
					msg = render_message(self.gui, self.gui.styles["timestamp"],self.gui.styles["notice"],user,self.gui.styles["message"],message,timestamp )
				elif GLYPH_RESUME in user:
					user = user.replace(GLYPH_RESUME,'')
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["resume"],message,timestamp )
				elif GLYPH_ERROR in user:
					user = user.replace(GLYPH_ERROR,'')
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["error"],message,timestamp )
				else:
					if GLYPH_SELF in user:
						user = user.replace(GLYPH_SELF,'')
						ustyle = self.gui.styles["self"]
					else:
						ustyle = self.gui.styles["username"]
					msg = render_message(self.gui, self.gui.styles["timestamp"],ustyle,user,self.gui.styles["message"],message,timestamp )
			else:
				msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["system"],message,timestamp )
			self.writeText(msg)

	def menuDisconnect(self):
		self.gui.disconnectFromIRC(self.client)

	def menuJoin(self):
		x = AddChannelDialog.Dialog()
		e = x.get_channel_information()

		if not e: return

		channel = e[0]
		key = e[1]

		if len(key)>0:
			self.client.join(channel,key)
		else:
			self.client.join(channel)

	def menuNick(self):
		x = NicknameDialog.Dialog()
		nick = x.get_nick_information()

		if not nick: return

		self.client.setNick(nick)