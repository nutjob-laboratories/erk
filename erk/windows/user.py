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
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *
from erk.spelledit import *
import erk.input

import erk.dialogs.add_channel as AddChannelDialog
import erk.dialogs.new_nick as NicknameDialog
import erk.dialogs.invite as InviteDialog

if WEB_AVAILABLE: import erk.windows.web as ViewWeb

def WebWindow(url,MDI,parent=None):
	if WEB_AVAILABLE:
		newSubwindow = QMdiSubWindow()
		newWindow = ViewWeb.Window(url,newSubwindow,parent)
		newSubwindow.setWidget(newWindow)
		newSubwindow.window = newWindow
		MDI.addSubWindow(newSubwindow)

		newSubwindow.resize(parent.default_window_width,parent.default_window_height)

		newSubwindow.show()

		return newWindow
	else:
		return None

class Window(QMainWindow):

	def changeEvent(self,event):

		if event.type() == QEvent.WindowStateChange:
			if event.oldState() and Qt.WindowMinimized:
				if self.subwindow.isMinimized():
					self.channelChatDisplay.moveCursor(QTextCursor.End)
				if self.subwindow.isMaximized():
					self.channelChatDisplay.moveCursor(QTextCursor.End)
			elif event.oldState() == Qt.WindowNoState:
				self.channelChatDisplay.moveCursor(QTextCursor.End)
			elif self.windowState() == Qt.WindowMaximized:
				if self.subwindow.isMinimized():
					self.channelChatDisplay.moveCursor(QTextCursor.End)
				if self.subwindow.isMaximized():
					self.channelChatDisplay.moveCursor(QTextCursor.End)
		
		return QMainWindow.changeEvent(self, event)

	def getUserNicks(self):
		return [self.name]

	def add_to_log(self,user,msg):
		t = datetime.timestamp(datetime.now())
		e = [t,user,msg]
		self.log.append(e)
		self.newlog.append(e)

	def menuClose(self):
		self.gui.irc_close_user_chat(self.client,self.name)

		# Save log
		if self.gui.log_private_chat:
			if self.gui.save_logs_on_quit:
				if len(self.newlog)>0:
					saveLog(self.client.network,self.name,self.newlog)

		self.gui.buildWindowMenu()

		self.subwindow.close()
		self.close()

	def closeEvent(self, event):

		if not self.gui.hide_private_chat:
			self.gui.irc_close_user_chat(self.client,self.name)

		# Save log
		if self.gui.log_private_chat:
			if self.gui.save_logs_on_quit:
				if len(self.newlog)>0:
					saveLog(self.client.network,self.name,self.newlog)

		if not self.gui.quitting: self.gui.buildWindowMenu()

		self.subwindow.close()
		self.close()
		event.accept()

	def handleUserInput(self):
		user_input = self.userTextInput.text()
		self.userTextInput.setText('')

		#print(user_input)
		erk.input.handle_chat_input(self,user_input,True)

	def writeText(self,text):

		self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		self.channelChatDisplay.update()

	def linkClicked(self,url):
		if url.host():
			# QDesktopServices.openUrl(url)
			# self.channelChatDisplay.setSource(QUrl())
			# self.channelChatDisplay.moveCursor(QTextCursor.End)

			if self.open_links_in_erk:
				#WebWindow(url.toString(),self.gui.MDI,self.gui)
				if self.gui.browser_window:
					self.gui.browser_window.navigate(url.toString())
				else:
					self.gui.browser_window = WebWindow(url.toString(),self.gui.MDI,self.gui)
			else:
				QDesktopServices.openUrl(url)
			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)
		else:
			link = url.toString()

			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)

	def update_nick(self,newnick):
		if self.is_away:
			self.status_nick.setText("&nbsp;<b><small>"+newnick+" (away)</small></b>")
		else:
			self.status_nick.setText("&nbsp;<b><small>"+newnick+"</small></b>")

	def uptime_display(self,text):
		# self.uptime = QLabel('<b>00:00:00</b>&nbsp;')
		self.uptime.setText('<b>'+text+'</b>')

	def hide_uptime(self):
		self.uptime.setVisible(False)

	def show_uptime(self):
		self.uptime.setVisible(True)

	def rename(self,nick):
		self.name = nick
		if self.hostmask:
			self.setWindowTitle(" "+self.name+" ("+self.hostmask+")")
		else:
			self.setWindowTitle(" "+self.name)

	def __init__(self,name,window_margin,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.log = []
		self.newlog = []

		self.is_channel = False
		self.is_console = False

		self.is_away = False

		self.open_links_in_erk = False

		# def get_user_hostmask(self,obj,tnick):
		self.hostmask = self.gui.get_user_hostmask(self.client,self.name)

		if self.hostmask:
			self.setWindowTitle(" "+self.name+" ("+self.hostmask+")")
		else:
			self.setWindowTitle(" "+self.name)

		self.setWindowIcon(QIcon(USER_WINDOW))

		self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)
		self.channelChatDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		self.userTextInput = SpellTextEdit(self)
		self.userTextInput.setObjectName("userTextInput")
		self.userTextInput.returnPressed.connect(self.handleUserInput)
		self.userTextInput.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

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

		# Status bar
		self.status = self.statusBar()
		self.status.setStyleSheet('QStatusBar::item {border: None;}')
		if self.client.hostname!=self.client.server:
			self.status_text = QLabel("<i>"+self.client.hostname+" ("+self.client.network+") - "+self.client.server+":"+str(self.client.port)+"</i>&nbsp;")
		else:
			self.status_text = QLabel("<i>"+self.client.hostname+" ("+self.client.network+")</i>&nbsp;")
		self.status_text.setAlignment(Qt.AlignRight)

		#self.status.addPermanentWidget(self.status_text,1)

		self.status_nick = QLabel("&nbsp;<b><small>"+self.client.nickname+"</small></b>")
		self.status_nick.setAlignment(Qt.AlignLeft)

		# self.status.addPermanentWidget(self.status_text,1)
		self.status.addPermanentWidget(self.status_nick,0)
		self.status.addPermanentWidget(QLabel(" "),1)
		self.status.addPermanentWidget(self.status_text,1)

		if not self.gui.display_status_bar_on_chat_windows: self.status.hide()

		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		self.menubar = self.menuBar()
		menuBoldText = self.menubar.font()
		menuBoldText.setBold(True)
		self.menubar.setStyle(self.gui.menu_style)

		if self.gui.display_uptime_seconds:
			self.uptime = QLabel('<b>00:00:00</b>',self)
		else:
			self.uptime = QLabel('<b>00:00</b>',self)
		
		self.menubar.setCornerWidget(self.uptime,Qt.TopRightCorner)

		self.uptime.setStyleSheet('padding: 2px;')

		if not self.gui.display_uptime_chat: self.uptime.setVisible(False)

		optionsMenu = self.menubar.addMenu("Private Chat")
		optionsMenu.setFont(menuBoldText)
		optionsMenu.setStyle(self.gui.menu_style)

		if WEB_AVAILABLE:
			self.actOpenLinks = QAction("Open links in "+APPLICATION_NAME,self,checkable=True)
			self.actOpenLinks.setChecked(self.open_links_in_erk)
			self.actOpenLinks.triggered.connect(self.menuOpenLinks)
			optionsMenu.addAction(self.actOpenLinks)


		uinvite = QAction(QIcon(INVITE_ICON),"Invite to channel",self)
		uinvite.triggered.connect(self.menuInvite)
		optionsMenu.addAction(uinvite)

		self.actWhois = QAction(QIcon(WHOIS_ICON),"WHOIS",self)
		self.actWhois.triggered.connect(self.menuWhois)
		optionsMenu.addAction(self.actWhois)

		optionsMenu.addSeparator()

		closechat = QAction(QIcon(PART_ICON),"Close chat",self)
		closechat.triggered.connect(self.menuClose)
		optionsMenu.addAction(closechat)

		# Load logs if necessary
		if self.gui.load_logs_on_start:
			self.log = loadLog(self.client.network,self.name)

			if len(self.log)>self.gui.max_displayed_log:
				self.log = trimLog(self.log,self.gui.max_displayed_log)

			for line in self.log:
				timestamp = line[0]
				user = line[1]
				message = line[2]

				if len(user)>0:
					if GLYPH_ACTION in user:
						user = user.replace(GLYPH_ACTION,'')
						msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ACTION_STYLE_NAME],user+" "+message,timestamp )
					elif GLYPH_NOTICE in user:
						user = user.replace(GLYPH_NOTICE,'')
						msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[NOTICE_STYLE_NAME],user,self.gui.styles[NOTICE_TEXT_STYLE_NAME],message,timestamp )
					elif GLYPH_RESUME in user:
						user = user.replace(GLYPH_RESUME,'')
						msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[RESUME_STYLE_NAME],message,timestamp )
					elif GLYPH_ERROR in user:
						user = user.replace(GLYPH_ERROR,'')
						msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ERROR_STYLE_NAME],message,timestamp )
					else:
						if GLYPH_SELF in user:
							user = user.replace(GLYPH_SELF,'')
							ustyle = self.gui.styles[SELF_STYLE_NAME]
						else:
							ustyle = self.gui.styles[USERNAME_STYLE_NAME]
						msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],ustyle,user,self.gui.styles[MESSAGE_STYLE_NAME],message,timestamp )
				else:
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[SYSTEM_STYLE_NAME],message,timestamp )
				self.writeText(msg)

			if len(self.log)>0:

				t = datetime.timestamp(datetime.now())
				pretty = datetime.fromtimestamp(t).strftime('%B %d, %Y at %H:%M:%S')

				f = self.font()
				ptsize = f.pointSize() - 2

				self.channelChatDisplay.insertHtml(HORIZONTAL_RULE)
				self.add_to_log(GLYPH_RESUME, f"Resumed on {pretty.upper()}" )

	def rerenderText(self):
		self.channelChatDisplay.clear()

		for line in self.log:
			timestamp = line[0]
			user = line[1]
			message = line[2]

			if len(user)>0:
				if GLYPH_ACTION in user:
					user = user.replace(GLYPH_ACTION,'')
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ACTION_STYLE_NAME],user+" "+message,timestamp )
				elif GLYPH_NOTICE in user:
					user = user.replace(GLYPH_NOTICE,'')
					msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[NOTICE_STYLE_NAME],user,self.gui.styles[NOTICE_TEXT_STYLE_NAME],message,timestamp )
				elif GLYPH_RESUME in user:
					user = user.replace(GLYPH_RESUME,'')
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[RESUME_STYLE_NAME],message,timestamp )
				elif GLYPH_ERROR in user:
					user = user.replace(GLYPH_ERROR,'')
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ERROR_STYLE_NAME],message,timestamp )
				else:
					if GLYPH_SELF in user:
						user = user.replace(GLYPH_SELF,'')
						ustyle = self.gui.styles[SELF_STYLE_NAME]
					else:
						ustyle = self.gui.styles[USERNAME_STYLE_NAME]
					msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],ustyle,user,self.gui.styles[MESSAGE_STYLE_NAME],message,timestamp )
			else:
				msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[SYSTEM_STYLE_NAME],message,timestamp )
			self.writeText(msg)

	def menuOpenLinks(self):
		if self.open_links_in_erk:
			self.open_links_in_erk = False
		else:
			self.open_links_in_erk = True

	def menuWhois(self):
		self.client.sendLine(f"WHOIS {self.name}")

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
		x = NicknameDialog.Dialog(self.client.nickname)
		nick = x.get_nick_information(self.client.nickname)

		if not nick: return

		self.client.setNick(nick)

	def menuInvite(self):
		x = InviteDialog.Dialog(self)
		ichan = x.get_invite_information(self)

		if not ichan: return

		self.client.invite(self.name,ichan)