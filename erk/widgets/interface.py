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

import re
from datetime import datetime
import fnmatch

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from spellchecker import SpellChecker

from erk.files import *
from erk.resources import *
from erk.objects import *
import erk.config
import erk.format
import erk.input
import erk.macros

from erk.dialogs import KeyDialog

class Window(QMainWindow):

	def closeEvent(self, event):
		# Logs
		if self.type==erk.config.CHANNEL_WINDOW:
			if erk.config.SAVE_CHANNEL_LOGS:
				saveLog(self.client.network,self.name,self.newLog)

		if self.type==erk.config.PRIVATE_WINDOW:
			if erk.config.SAVE_PRIVATE_LOGS:
				saveLog(self.client.network,self.name,self.newLog)

	def handleTopicInput(self):
		#print(self.topic.text())
		self.client.topic(self.name,self.topic.text())

		# Move the cursor back to the input widget
		self.input.setFocus()

	def handleUserInput(self):
		user_input = self.input.text()
		self.input.setText('')

		# ================================
		# BEGIN COMMAND HISTORY MANAGEMENT
		# ================================

		if erk.config.TRACK_COMMAND_HISTORY:
			# Remove blank entries from history
			clean = []
			for c in self.history_buffer:
				if c=='': continue
				clean.append(c)
			self.history_buffer = clean

			# Insert current input into the history,
			# right at the beginning
			self.history_buffer.insert(0,user_input)

			# If history is larger than it's supposed to be,
			# remove the last entry
			if len(self.history_buffer)>erk.config.HISTORY_LENGTH:
				self.history_buffer.pop()

			# "Zero" the history buffer pointer
			self.history_buffer_pointer = -1

			# Add a blank entry to the history;
			# this represents (to the user) the current
			# "blank" input
			self.history_buffer.append('')

			# Remove consecutive repeated commands
			self.history_buffer = [self.history_buffer[i] for i in range(len(self.history_buffer)) if (i==0) or self.history_buffer[i] != self.history_buffer[i-1]]

		# ==============================
		# END COMMAND HISTORY MANAGEMENT
		# ==============================

		erk.input.handle_input(self,self.client,user_input)

	def keyPressDown(self):
		if erk.config.TRACK_COMMAND_HISTORY:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer - 1
			if self.history_buffer_pointer < 0:
				self.history_buffer_pointer = len(self.history_buffer) - 1
			self.input.setText(self.history_buffer[self.history_buffer_pointer])
			self.input.moveCursor(QTextCursor.End)

	def keyPressUp(self):
		if erk.config.TRACK_COMMAND_HISTORY:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer + 1
			if len(self.history_buffer) - 1 < self.history_buffer_pointer:
				self.history_buffer_pointer = 0
			self.input.setText(self.history_buffer[self.history_buffer_pointer])
			self.input.moveCursor(QTextCursor.End)

	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.chat.setSource(QUrl())
			self.chat.moveCursor(QTextCursor.End)
		else:
			link = url.toString()
			self.chat.setSource(QUrl())
			self.chat.moveCursor(QTextCursor.End)


	def resizeEvent(self, event):

		if self.type==erk.config.CHANNEL_WINDOW:
       
			# QSplitter dynamically changes widget sizes on a resize
			# event; this makes the userlist widget get wider or less wide
			# depending on the new widget size. This code makes sure that
			# the userlist maintains the same width during resize events

			# Calculate the width of the chat display widget
			chat_width = self.width() - self.userlist_width - (erk.config.CHAT_WINDOW_WIDGET_SPACING * 3)

			# Resize the userlist widget with the width value saved in
			# the splitter resize event
			self.userlist.resize(self.userlist_width,self.userlist.height())

			# Resize the chat display to compensate for the changed
			# userlist size
			self.chat.resize(chat_width,self.chat.height())

			# Move the userlist so it's along side the chat display
			self.userlist.move(chat_width + 3,self.userlist.y())

			# Move the QSplitter handle to match the new widget sizes
			self.horizontalSplitter.setSizes([self.chat.width(), self.userlist.width()])

		return super(Window, self).resizeEvent(event)


	def splitterResize(self,position,index):

		# Save the width of the userlist for the resize event
		self.userlist_width = self.userlist.width()

	def _handleDoubleClick(self,item):
		item.setSelected(False)
		user = item.text()
		user = user.replace('@','')
		user = user.replace('+','')
		if user==self.client.nickname: return
		self.parent.open_private_window(self.client,user)

	def __init__(self,name,client,wtype,app,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.client = client
		self.parent = parent
		self.type = wtype
		self.app = app

		self.log = []
		self.newLog = []

		self.channel_topic = ''

		self.modeson = ''
		self.modesoff = ''
		self.key = ''

		self.users = []
		self.nicks = []
		self.hostmasks = {}
		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False

		self.language = erk.config.SPELLCHECK_LANGUAGE

		self.history_buffer = ['']
		self.history_buffer_pointer = 0
		# self.history_buffer_max = erk.config.HISTORY_LENGTH

		self.userlist_width = 0

		self.commands = {}

		if self.type==erk.config.CHANNEL_WINDOW: self.commands.update(erk.input.CHANNEL_COMMANDS)
		if self.type==erk.config.PRIVATE_WINDOW: self.commands.update(erk.input.PRIVATE_COMMANDS)

		self.commands.update(erk.input.COMMON_COMMANDS)

		self.chat = QTextBrowser(self)
		self.chat.setFocusPolicy(Qt.NoFocus)
		self.chat.anchorClicked.connect(self.linkClicked)

		self.chat.setContextMenuPolicy(Qt.CustomContextMenu)
		self.chat.customContextMenuRequested.connect(self.chatMenu)

		if self.type==erk.config.CHANNEL_WINDOW:

			self.topic = TopicEdit()
			self.topic.returnPressed.connect(self.handleTopicInput)
			self.topic.setStyleSheet("border: 0px; background-color: transparent;")
			self.topic.setReadOnly(True)

			self.userlist = QListWidget(self)
			self.userlist.setFocusPolicy(Qt.NoFocus)
			self.userlist.itemDoubleClicked.connect(self._handleDoubleClick)
			self.userlist.installEventFilter(self)

			# Make sure that user status icons are just a little
			# bigger than the user entry text
			fm = QFontMetrics(self.chat.font())
			fheight = fm.height() + 2
			self.userlist.setIconSize(QSize(fheight,fheight))

			# Make userlist font bold
			f = self.chat.font()
			f.setBold(True)
			self.userlist.setFont(f)

			# Save userlist width
			self.userlist_width = self.userlist.width()

		self.input = SpellTextEdit(self)
		self.input.returnPressed.connect(self.handleUserInput)
		self.input.keyUp.connect(self.keyPressUp)
		self.input.keyDown.connect(self.keyPressDown)

		# Text input widget should only be one line
		fm = self.input.fontMetrics()
		self.input.setFixedHeight(fm.height()+9)
		self.input.setWordWrapMode(QTextOption.NoWrap)
		self.input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.input.changeLanguage(self.language)

		if self.type==erk.config.SERVER_WINDOW:
			self.name_display = QLabel("<b>Server</b>")
		else:
			self.name_display = QLabel("<b>"+self.name+"</b>")

		# self.name_display = QLabel("<b>"+self.name+"</b>")
		self.name_display.setStyleSheet("border: 1px solid black; padding: 2px;")

		if self.type!=erk.config.CHANNEL_WINDOW:

			nameLayout = QHBoxLayout()
			nameLayout.addWidget(self.name_display)
			nameLayout.addStretch()

			finalLayout = QVBoxLayout()
			finalLayout.setSpacing(erk.config.CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.setContentsMargins(erk.config.CHAT_WINDOW_WIDGET_SPACING,erk.config.CHAT_WINDOW_WIDGET_SPACING,erk.config.CHAT_WINDOW_WIDGET_SPACING,erk.config.CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.addLayout(nameLayout)
			finalLayout.addWidget(self.chat)
			finalLayout.addWidget(self.input)
		else:
			self.horizontalSplitter = QSplitter(Qt.Horizontal)
			self.horizontalSplitter.addWidget(self.chat)
			self.horizontalSplitter.addWidget(self.userlist)
			self.horizontalSplitter.splitterMoved.connect(self.splitterResize)

			# Set the initial splitter ratio
			ulwidth = (fm.width('X') + 2) + (fm.width('X')*18)
			mwidth = self.width()-ulwidth
			self.horizontalSplitter.setSizes([mwidth,ulwidth])

			# Set the starting width of the userlist
			self.userlist.resize(ulwidth,self.height())
			self.userlist_width = ulwidth

			# self.show_status_in_nick_display

			self.user_icon = QLabel()
			pixmap = QPixmap(NICK_ICON)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.user_icon.setPixmap(pixmap)

			# Load status icons for the nick display into memory
			self.op_icon = QLabel(self)
			pixmap = QPixmap(USERLIST_OPERATOR_ICON)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.op_icon.setPixmap(pixmap)

			self.user_op = QLabel()
			self.user_op.setPixmap(pixmap)

			self.voice_icon = QLabel(self)
			pixmap = QPixmap(USERLIST_VOICED_ICON)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.voice_icon.setPixmap(pixmap)

			self.user_voice = QLabel()
			self.user_voice.setPixmap(pixmap)

			self.owner_icon = QLabel(self)
			pixmap = QPixmap(USERLIST_OWNER_ICON)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.owner_icon.setPixmap(pixmap)

			self.user_owner = QLabel()
			self.user_owner.setPixmap(pixmap)

			self.admin_icon = QLabel(self)
			pixmap = QPixmap(USERLIST_ADMIN_ICON)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.admin_icon.setPixmap(pixmap)

			self.user_admin = QLabel()
			self.user_admin.setPixmap(pixmap)

			self.halfop_icon = QLabel(self)
			pixmap = QPixmap(USERLIST_HALFOP_ICON)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.halfop_icon.setPixmap(pixmap)

			self.user_halfop = QLabel()
			self.user_halfop.setPixmap(pixmap)

			self.op_icon.hide()
			self.voice_icon.hide()
			self.owner_icon.hide()
			self.admin_icon.hide()
			self.halfop_icon.hide()

			self.nick_display = QLabel(" <b>"+self.client.nickname+"</b> ")

			if not erk.config.DISPLAY_NICKNAME_ON_CHANNEL: self.nick_display.hide()

			nicknameLayout = QHBoxLayout()
			nicknameLayout.addWidget(self.op_icon)
			nicknameLayout.addWidget(self.voice_icon)
			nicknameLayout.addWidget(self.owner_icon)
			nicknameLayout.addWidget(self.admin_icon)
			nicknameLayout.addWidget(self.halfop_icon)
			nicknameLayout.addWidget(self.nick_display)
			nicknameLayout.setAlignment(Qt.AlignVCenter)

			inputLayout = QHBoxLayout()
			# inputLayout.addWidget(self.nick_display)
			inputLayout.addLayout(nicknameLayout)
			inputLayout.addWidget(self.input)

			#inputLayout.setAlignment(Qt.AlignVCenter)

			self.key_display = QLabel(self)
			pixmap = QPixmap(KEY_ICON)

			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled((fm.height() + 2), (fm.height() + 2), Qt.KeepAspectRatio, Qt.SmoothTransformation)

			self.key_display.setPixmap(pixmap)

			self.key_display.hide()

			topicLayout = QHBoxLayout()
			# self.name_display = QLabel(" <b>"+self.name+"</b> ")
			topicLayout.addWidget(self.key_display)
			topicLayout.addWidget(self.name_display)
			topicLayout.addWidget(self.topic)

			finalLayout = QVBoxLayout()
			finalLayout.setSpacing(erk.config.CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.setContentsMargins(erk.config.CHAT_WINDOW_WIDGET_SPACING,erk.config.CHAT_WINDOW_WIDGET_SPACING,erk.config.CHAT_WINDOW_WIDGET_SPACING,erk.config.CHAT_WINDOW_WIDGET_SPACING)
			#finalLayout.addWidget(self.topic)
			finalLayout.addLayout(topicLayout)
			finalLayout.addWidget(self.horizontalSplitter)
			#finalLayout.addWidget(self.input)
			finalLayout.addLayout(inputLayout)

		# Logs
		load_log_from_disk = False

		if self.type==erk.config.CHANNEL_WINDOW:
			if erk.config.LOAD_CHANNEL_LOGS:
				load_log_from_disk = True

		if self.type==erk.config.PRIVATE_WINDOW:
			if erk.config.LOAD_PRIVATE_LOGS:
				load_log_from_disk = True

		if load_log_from_disk:
			loadLog = readLog(self.client.network,self.name)
			if len(loadLog)>erk.config.LOG_LOAD_SIZE_MAX:
				loadLog = trimLog(loadLog,erk.config.LOG_LOAD_SIZE_MAX)

			if len(loadLog)>0:
				self.log = loadLog + self.log
				if erk.config.MARK_END_OF_LOADED_LOG:
					self.log.append(Message(HORIZONTAL_RULE_MESSAGE,'',''))

				if erk.config.DISPLAY_CHAT_RESUME_DATE_TIME:
					t = datetime.timestamp(datetime.now())
					pretty_timestamp = datetime.fromtimestamp(t).strftime('%m/%d/%Y, %H:%M:%S')
					m = Message(SYSTEM_MESSAGE,'',"Resumed on "+pretty_timestamp)
					self.writeText(m)

				self.rerender()


		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		# self.show()
		# self.input.setFocus()

	# BEGIN GUI METHODS

	def rebuildConnection(self):
		erk.events.build_connection_display(self.parent)

	def channelNickVisibility(self):
		if erk.config.DISPLAY_NICKNAME_ON_CHANNEL:
			self.nick_display.show()
		else:
			self.nick_display.hide()

	def connectDialog(self):
		self.parent.menuCombo()

	def doConnect(self,info):
		self.parent.connectToIRCServer(info)

	def doNick(self,client):
		self.parent.menuNick(client)

	def doJoin(self,client):
		self.parent.menuJoin(client)

	def newPrivate(self,target):
		erk.events.open_private_window(self.client,target)

	def leaveChannel(self,channel,msg=None):
		erk.events.close_channel_window(self.client,channel,msg)

	def channelList(self):
		return erk.events.fetch_channel_list(self.client)

	def privateList(self):
		return erk.events.fetch_private_list(self.client)

	def nameToChannel(self,channel):
		return erk.events.name_to_channel(self.client,channel)

	def nameToPrivate(self,channel):
		return erk.events.name_to_private(self.client,channel)

	def setKey(self,key):
		self.key = key
		self.key_display.setToolTip(key)

		if len(key)==0:
			self.key_display.hide()
		else:
			self.key_display.show()

	def nickDisplay(self,nick):
		self.nick_display.setText(" <b>"+nick+"</b> ")

	def setTopic(self,topic):

		if not hasattr(self,"topic"): return

		self.channel_topic = topic
		self.topic.setText(topic)
		self.topic.setCursorPosition(0)

	def reset_input(self):
		cursor = self.input.textCursor()
		user_input = self.input.text()
		self.input.setText('')
		self.input.setText(user_input)
		self.input.moveCursor(cursor.position())

	def changeSpellcheckLanguage(self,lang):

		# Set the new language
		self.language = lang
		self.input.changeLanguage(lang)

		# Rewrite whatever is in the input widget
		# so that it's spellchecked
		cursor = self.input.textCursor()
		user_input = self.input.text()
		self.input.setText('')
		self.input.setText(user_input)
		self.input.moveCursor(cursor.position())

	def writeText(self,message,do_not_save=False):

		d = erk.format.render_message(message)

		self.chat.append(d)
		self.chat.moveCursor(QTextCursor.End)

		self.log.append(message)

		if do_not_save: return 

		self.newLog.append(message)

	def rerender(self):
		self.chat.clear()

		for line in self.log:
			d = erk.format.render_message(line)
			self.chat.append(d)

		self.chat.moveCursor(QTextCursor.End)

	def rerender_userlist(self):
		self.writeUserlist(self.users)

	def writeUserlist(self,users):

		if not hasattr(self,"userlist"): return

		self.users = []
		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False

		self.userlist.clear()

		# Sort the user list
		owners = []
		admins = []
		ops = []
		halfops = []
		voiced = []
		normal = []

		for u in users:
			if len(u)<1: continue
			self.users.append(u)
			p = u.split("!")
			if len(p)==2:
				nickname = p[0]
				hostmask = p[1]
				self.hostmasks[nickname] = hostmask
			else:
				nickname = u
				hostmask = None

			#if self.plain_user_lists:
			if erk.config.PLAIN_USER_LISTS:
				if '@' in nickname:
					ops.append(nickname)
					if nickname==self.client.nickname: self.operator = True
				elif '+' in nickname:
					voiced.append(nickname)
					if nickname==self.client.nickname: self.voiced = True
				elif '~' in nickname:
					owners.append(nickname)
					if nickname==self.client.nickname: self.owner = True
				elif '&' in nickname:
					admins.append(nickname)
					if nickname==self.client.nickname: self.admin = True
				elif '%' in nickname:
					halfops.append(nickname)
					if nickname==self.client.nickname: self.halfop = True
				else:
					normal.append(nickname)
			else:
				if '@' in nickname:
					ops.append(nickname.replace('@',''))
					if nickname.replace('@','')==self.client.nickname: self.operator = True
				elif '+' in nickname:
					voiced.append(nickname.replace('+',''))
					if nickname.replace('+','')==self.client.nickname: self.voiced = True
				elif '~' in nickname:
					owners.append(nickname.replace('~',''))
					if nickname.replace('~','')==self.client.nickname: self.owner = True
				elif '&' in nickname:
					admins.append(nickname.replace('&',''))
					if nickname.replace('&','')==self.client.nickname: self.admin = True
				elif '%' in nickname:
					halfops.append(nickname.replace('%',''))
					if nickname.replace('%','')==self.client.nickname: self.halfop = True
				else:
					normal.append(nickname)

		# Store a list of the nicks in this channel
		self.nicks = owners + admins + halfops + ops + voiced + normal

		# Display nick status, if necessary
		if erk.config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY:

			self.op_icon.hide()
			self.voice_icon.hide()
			self.owner_icon.hide()
			self.admin_icon.hide()
			self.halfop_icon.hide()

			if self.operator: self.op_icon.show()
			if self.voiced: self.voice_icon.show()

			if self.owner: self.owner_icon.show()
			if self.admin: self.admin_icon.show()
			if self.halfop: self.halfop_icon.show()

		else:

			self.op_icon.hide()
			self.voice_icon.hide()
			self.owner_icon.hide()
			self.admin_icon.hide()
			self.halfop_icon.hide()

		# Add nicks to the spellchecker
		self.input.addNicks(self.nicks)

		# Alphabetize
		owners.sort()
		admins.sort()
		halfops.sort()
		ops.sort()
		voiced.sort()
		normal.sort()

		# Add owners
		for u in owners:
			ui = QListWidgetItem()
			if not erk.config.PLAIN_USER_LISTS: ui.setIcon(QIcon(USERLIST_OWNER_ICON))
			ui.setText(u)
			self.userlist.addItem(ui)

		# Add admins
		for u in admins:
			ui = QListWidgetItem()
			if not erk.config.PLAIN_USER_LISTS: ui.setIcon(QIcon(USERLIST_ADMIN_ICON))
			ui.setText(u)
			self.userlist.addItem(ui)

		# Add ops
		for u in ops:
			ui = QListWidgetItem()
			if not erk.config.PLAIN_USER_LISTS: ui.setIcon(QIcon(USERLIST_OPERATOR_ICON))
			ui.setText(u)
			self.userlist.addItem(ui)

		# Add halfops
		for u in halfops:
			ui = QListWidgetItem()
			if not erk.config.PLAIN_USER_LISTS: ui.setIcon(QIcon(USERLIST_HALFOP_ICON))
			ui.setText(u)
			self.userlist.addItem(ui)

		# Add voiced
		for u in voiced:
			ui = QListWidgetItem()
			if not erk.config.PLAIN_USER_LISTS: ui.setIcon(QIcon(USERLIST_VOICED_ICON))
			ui.setText(u)
			self.userlist.addItem(ui)

		# Add normal
		for u in normal:
			ui = QListWidgetItem()
			if not erk.config.PLAIN_USER_LISTS: ui.setIcon(QIcon(USERLIST_NORMAL_ICON))
			ui.setText(u)
			self.userlist.addItem(ui)

		self.userlist.update()

	def setChannelKey(self):
		newkey = KeyDialog()
		if newkey:
			self.client.mode(self.name,True,"k",None,newkey)


	def chatMenu(self,location):

		menu = self.chat.createStandardContextMenu()

		if self.operator:

			if self.type==erk.config.CHANNEL_WINDOW:

				opMenu = QMenu("Operator actions")
				opMenu.setIcon(QIcon(USERLIST_OPERATOR_ICON))
				menu.insertMenu(menu.actions()[0],opMenu)


				if self.key!='' or "k" in self.modeson:
					entry = QAction(QIcon(MINUS_ICON),"Remove channel key",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,False,"k",None,self.key))
				else:
					entry = QAction(QIcon(PLUS_ICON),"Set channel key",self)
					entry.triggered.connect(self.setChannelKey)
				opMenu.addAction(entry)

				if "m" in self.modeson:
					entry = QAction(QIcon(MINUS_ICON),"Unmoderate channel",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,False,"m",None,None))
				else:
					entry = QAction(QIcon(PLUS_ICON),"Moderate channel",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,True,"m",None,None))
				opMenu.addAction(entry)

				if "c" in self.modeson:
					entry = QAction(QIcon(MINUS_ICON),"Allow IRC colors",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,False,"c",None,None))
				else:
					entry = QAction(QIcon(PLUS_ICON),"Block IRC colors",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,True,"c",None,None))
				opMenu.addAction(entry)

				if "i" in self.modeson:
					entry = QAction(QIcon(MINUS_ICON),"Allow uninvited users",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,False,"i",None,None))
				else:
					entry = QAction(QIcon(PLUS_ICON),"Make channel invite only",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,True,"i",None,None))
				opMenu.addAction(entry)

				if "p" in self.modeson:
					entry = QAction(QIcon(MINUS_ICON),"Make channel public",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,False,"p",None,None))
				else:
					entry = QAction(QIcon(PLUS_ICON),"Make channel private",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,True,"p",None,None))
				opMenu.addAction(entry)

				if "s" in self.modeson:
					entry = QAction(QIcon(MINUS_ICON),"Make channel unsecret",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,False,"s",None,None))
				else:
					entry = QAction(QIcon(PLUS_ICON),"Make channel secret",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,True,"s",None,None))
				opMenu.addAction(entry)

				if "t" in self.modeson:
					entry = QAction(QIcon(MINUS_ICON),"Allow users to change topic",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,False,"t",None,None))
				else:
					entry = QAction(QIcon(PLUS_ICON),"Forbid non-ops from changing topic",self)
					entry.triggered.connect(lambda state: self.client.mode(self.name,True,"t",None,None))
				opMenu.addAction(entry)

		action = menu.exec_(self.chat.mapToGlobal(location))

	def eventFilter(self, source, event):

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.userlist):

			item = source.itemAt(event.pos())
			if item is None: return True

			user = item.text()

			user_nick = ''
			user_hostmask = None
			user_is_op = False
			user_is_voiced = False
			user_is_admin = False
			user_is_owner = False
			user_is_halfop = False

			raw_user = None

			for u in self.users:
				p = u.split('!')
				if len(p)==2:
					nick = p[0]
					hostmask = p[1]
				else:
					nick = u
					hostmask = None

				if '@' in nick:
					is_op = True
					nick = nick.replace('@','')
				else:
					is_op = False
				if '+' in nick:
					is_voiced = True
					nick = nick.replace('+','')
				else:
					is_voiced = False
				if '~' in nick:
					is_owner = True
					nick = nick.replace('~','')
				else:
					is_owner = False
				if '&' in nick:
					is_admin = True
					nick = nick.replace('&','')
				else:
					is_admin = False
				if '%' in nick:
					is_halfop = True
					nick = nick.replace('%','')
				else:
					is_halfop = False
				if nick==user:
					raw_user = u
					user_nick = nick
					if hostmask:
						user_hostmask = hostmask
					else:
						if nick in self.hostmasks:
							user_hostmask = self.hostmasks[nick]
					user_is_op = is_op
					user_is_voiced = is_voiced
					user_is_owner = is_owner
					user_is_admin = is_admin
					user_is_halfop = is_halfop
					break

			if len(user_nick.strip())==0:
				if '@' in user:
					user_is_op = True
					user = user.replace('@','')
				if '+' in user:
					user_is_voiced = True
					user = user.replace('+','')
				if '~' in user:
					user_is_owner = True
					user = user.replace('~','')
				if '&' in user:
					user_is_admin = True
					user = user.replace('&','')
				if '%' in user:
					user_is_halfop = True
					user = user.replace('%','')
				user_nick = user

				if user_nick in self.hostmasks:
					user_hostmask = self.hostmasks[user_nick]

			is_ignored = False
			for i in self.parent.ignore:
				if user_hostmask:
					if user_hostmask in i: is_ignored = True
				if i==user_nick: is_ignored = True
				if raw_user:
					if i==raw_user: is_ignored = True

			if user_nick==self.client.nickname:
				this_is_me = True
			else:
				this_is_me = False

			menu = QMenu(self)

			tsLabel = QLabel( "&nbsp;<big><b>"+user_nick+"</b></big>" )
			tsAction = QWidgetAction(self)
			tsAction.setDefaultWidget(tsLabel)
			menu.addAction(tsAction)

			if user_hostmask:
				max_length = 25
				if len(user_hostmask)>max_length:
					if len(user_hostmask)>=max_length+3:
						offset = max_length-3
					elif len(user_hostmask)==max_length+2:
						offset = max_length-2
					elif len(user_hostmask)==max_length+1:
						offset = max_length-1
					else:
						offset = max_length
					display_hostmask = user_hostmask[0:offset]+"..."
				else:
					display_hostmask = user_hostmask
				tsLabel = QLabel( "&nbsp;<i>"+display_hostmask+"</i>" )
				tsAction = QWidgetAction(self)
				tsAction.setDefaultWidget(tsLabel)
				menu.addAction(tsAction)

			statusLayout = QHBoxLayout()
			if user_is_op:
				statusLayout.addWidget(self.user_op)
				statusLayout.addWidget(QLabel(f"<i>"+"Channel Operator"+"</i>"))
			elif user_is_voiced:
				statusLayout.addWidget(self.user_voice)
				statusLayout.addWidget(QLabel(f"<i>"+"Voiced user"+"</i>"))
			elif user_is_owner:
				statusLayout.addWidget(self.user_owner)
				statusLayout.addWidget(QLabel(f"<i>"+"Channel Owner"+"</i>"))
			elif user_is_admin:
				statusLayout.addWidget(self.user_admin)
				statusLayout.addWidget(QLabel(f"<i>"+"Channel Admin"+"</i>"))
			elif user_is_halfop:
				statusLayout.addWidget(self.user_halfop)
				statusLayout.addWidget(QLabel(f"<i>"+"Channel Half-Operator"+"</i>"))
			else:
				statusLayout.addWidget(self.user_icon)
				statusLayout.addWidget(QLabel(f"<i>"+"Normal user"+"</i>"))
			statusLayout.addStretch()
			u = QWidget()
			u.setLayout(statusLayout)
			tsAction = QWidgetAction(self)
			tsAction.setDefaultWidget(u)
			menu.addAction(tsAction)

			menu.addSeparator()

			if self.operator:

				opMenu = menu.addMenu(QIcon(USERLIST_OPERATOR_ICON),"Operator actions")

				if user_is_op: actDeop = opMenu.addAction(QIcon(MINUS_ICON),"Take operator status")
				if not user_is_op: actOp = opMenu.addAction(QIcon(PLUS_ICON),"Give operator status")

				if not user_is_op:
					if user_is_voiced: actDevoice = opMenu.addAction(QIcon(MINUS_ICON),"Take voiced status")
					if not user_is_voiced: actVoice = opMenu.addAction(QIcon(PLUS_ICON),"Give voiced status")

				opMenu.addSeparator()

				actKick = opMenu.addAction(QIcon(KICK_ICON),"Kick")
				actBan = opMenu.addAction(QIcon(BAN_ICON),"Ban")
				actKickBan = opMenu.addAction(QIcon(KICKBAN_ICON),"Kick/Ban")

			if not this_is_me:
				if is_ignored:
					actIgnore = menu.addAction(QIcon(SHOW_ICON),"Unignore")
				else:
					actIgnore = menu.addAction(QIcon(HIDE_ICON),"Ignore")

			actWhois = menu.addAction(QIcon(WHOIS_ICON),"WHOIS")

			clipMenu = menu.addMenu(QIcon(CLIPBOARD_ICON),"Copy to clipboard")
			actCopyNick = clipMenu.addAction(QIcon(NICK_ICON),"User's nickname")
			if user_hostmask: actHostmask = clipMenu.addAction(QIcon(SERVER_ICON),"User's hostmask")

			action = menu.exec_(self.userlist.mapToGlobal(event.pos()))

			if not this_is_me:
				if action == actIgnore:
					if is_ignored:
						clean = []
						for i in self.parent.ignore:
							if user_hostmask:
								if user_hostmask in i: continue
							if i==user_nick: continue
							if raw_user:
								if i==raw_user: continue
							clean.append(i)
						self.parent.ignore = clean
						u = get_user()
						u["ignore"] = clean
						save_user(u)
						return True
					else:
						if user_hostmask:
							self.parent.ignore.append(user_hostmask)
						elif raw_user:
							self.parent.ignore.append(raw_user)
						else:
							self.parent.ignore.append(user_nick)
						u = get_user()
						u["ignore"] = self.parent.ignore
						save_user(u)
						return True

			if action == actWhois:
				self.client.sendLine("WHOIS "+user_nick)
				return True

			if action == actCopyNick:
				cb = QApplication.clipboard()
				cb.clear(mode=cb.Clipboard)
				cb.setText(f"{user_nick}", mode=cb.Clipboard)
				return True

			if user_hostmask:
				if action == actHostmask:
					cb = QApplication.clipboard()
					cb.clear(mode=cb.Clipboard)
					cb.setText(f"{user_hostmask}", mode=cb.Clipboard)
					return True

			if self.operator:

				if action == actKick:
					self.client.kick(self.name,user_nick)
					return True

				if action == actBan:
					if user_hostmask:
						h = user_hostmask.split('@')[1]
						banmask = "*@"+h
					else:
						banmask = user_nick
					self.client.mode(self.name,True,"b",None,None,banmask)
					return True

				if action == actKickBan:
					if user_hostmask:
						h = user_hostmask.split('@')[1]
						banmask = "*@"+h
					else:
						banmask = user_nick
					self.client.mode(self.name,True,"b",None,None,banmask)
					self.client.kick(self.name,user_nick)
					return True

				if user_is_op:
					if action == actDeop:
						self.client.mode(self.name,False,"o",None,user_nick)
						return True

				if not user_is_op:
					if user_is_voiced:
						if action == actDevoice:
							self.client.mode(self.name,False,"v",None,user_nick)
							return True

				if not user_is_op:
					if action == actOp:
						self.client.mode(self.name,True,"o",None,user_nick)
						return True

				if not user_is_op:
					if not user_is_voiced:
						if action == actVoice:
							self.client.mode(self.name,True,"v",None,user_nick)
							return True

			return True

		return super(Window, self).eventFilter(source, event)


class TopicEdit(QLineEdit):
	def __init__(self, parent=None):
		super(QLineEdit, self).__init__(parent)
		self.readyToEdit = True

	def mousePressEvent(self, e, Parent=None):
		super(QLineEdit, self).mousePressEvent(e) #required to deselect on 2e click
		if self.readyToEdit:
			self.setReadOnly(False)
			self.selectAll()
			self.readyToEdit = False

	def focusOutEvent(self, e):
		super(QLineEdit, self).focusOutEvent(e) #required to remove cursor on focusOut
		self.deselect()
		self.readyToEdit = True
		self.setReadOnly(True)
		self.setCursorPosition(0)

# Text entry widget
class SpellTextEdit(QPlainTextEdit):

	returnPressed = pyqtSignal()
	keyUp = pyqtSignal()
	keyDown = pyqtSignal()

	def __init__(self, *args):
		QPlainTextEdit.__init__(self, *args)

		self.parent = args[0]

		self.dict = SpellChecker(language=self.parent.language,distance=1)

		self.highlighter = Highlighter(self.document())

		self.highlighter.setDict(self.dict)
		self.highlighter.setParent(self.parent)

		self.nicks = []

	def keyPressEvent(self,event):

		if event.key() == Qt.Key_Return:
			self.returnPressed.emit()
		elif event.key() == Qt.Key_Up:
			self.keyUp.emit()
		elif event.key() == Qt.Key_Down:
			self.keyDown.emit()
		elif event.key() == Qt.Key_Tab:
			cursor = self.textCursor()

			if self.toPlainText().strip()=='': return

			if erk.config.AUTOCOMPLETE_COMMANDS:

				# Auto-complete commands
				cursor.select(QTextCursor.BlockUnderCursor)
				self.setTextCursor(cursor)
				if self.textCursor().hasSelection():
					text = self.textCursor().selectedText()

					self.COMMAND_LIST = self.parent.commands

					self.COMMAND_LIST.update(erk.macros.MACRO_COMMANDS)

					for c in self.COMMAND_LIST:
						cmd = c
						rep = self.COMMAND_LIST[c]

						#if text in cmd:
						if fnmatch.fnmatch(cmd,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(rep)
							cursor.endEditBlock()
							return

			if erk.config.AUTOCOMPLETE_NICKNAMES:
				# Auto-complete nicks/channels
				cursor.select(QTextCursor.WordUnderCursor)
				self.setTextCursor(cursor)
				if self.textCursor().hasSelection():
					text = self.textCursor().selectedText()

					# Nicks
					chan_nicks = erk.events.full_nick_list(self.parent.client)
					for nick in chan_nicks:
						# Skip client's nickname
						if nick==self.parent.client.nickname:
							continue
						if fnmatch.fnmatch(nick,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(f"{nick}")
							cursor.endEditBlock()
							return

				if erk.config.AUTOCOMPLETE_EMOJI and erk.config.USE_EMOJIS:

					# Autocomplete emojis
					cursor.select(QTextCursor.WordUnderCursor)
					oldpos = cursor.position()
					cursor.select(QTextCursor.WordUnderCursor)
					newpos = cursor.selectionStart() - 1
					cursor.setPosition(newpos,QTextCursor.MoveAnchor)
					cursor.setPosition(oldpos,QTextCursor.KeepAnchor)
					self.setTextCursor(cursor)
					if self.textCursor().hasSelection():
						text = self.textCursor().selectedText()

						for c in EMOJI_AUTOCOMPLETE:

							# Case sensitive
							if fnmatch.fnmatchcase(c,f"{text}*"):
								cursor.beginEditBlock()
								cursor.insertText(c)
								cursor.endEditBlock()
								return

							# Case insensitive
							if fnmatch.fnmatch(c,f"{text}*"):
								cursor.beginEditBlock()
								cursor.insertText(c)
								cursor.endEditBlock()
								return

			cursor.movePosition(QTextCursor.End)
			self.setTextCursor(cursor)

		else:
			return super().keyPressEvent(event)

	def text(self):
		return self.toPlainText()

	def setText(self,text):
		self.setPlainText(text)

	def addNicks(self,nicks):
		if erk.config.SPELLCHECK_IGNORE_NICKS:
			if len(self.nicks)>0:
				self.dict.word_frequency.remove_words(self.nicks)
			self.nicks = nicks.copy()
			self.dict.word_frequency.load_words(nicks)
		else:
			if len(self.nicks)>0:
				self.dict.word_frequency.remove_words(self.nicks)
			self.nicks = []

	def changeLanguage(self,lang):
		self.dict = SpellChecker(language=lang,distance=1)
		self.highlighter.setDict(self.dict)

	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			# Rewrite the mouse event to a left button event so the cursor is
			# moved to the location of the pointer.
			event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
				Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
		QPlainTextEdit.mousePressEvent(self, event)

	def contextMenuEvent(self, event):

		if not erk.config.SPELLCHECK_INPUT:
			return super().contextMenuEvent(event)

		popup_menu = self.createStandardContextMenu()

		# Select the word under the cursor.
		cursor = self.textCursor()
		cursor.select(QTextCursor.WordUnderCursor)
		self.setTextCursor(cursor)

		# Check if the selected word is misspelled and offer spelling
		# suggestions if it is.
		if self.textCursor().hasSelection():
			text = self.textCursor().selectedText()

			misspelled = self.dict.unknown([text])
			if len(misspelled)>0:
				counter = 0
				for word in self.dict.candidates(text):
					action = SpellAction(word, popup_menu)
					action.correct.connect(self.correctWord)
					popup_menu.insertAction(popup_menu.actions()[0],action)
					counter = counter + 1
				if counter != 0:
					popup_menu.insertSeparator(popup_menu.actions()[counter])

		popup_menu.exec_(event.globalPos())

	def correctWord(self, word):
		'''
		Replaces the selected text with word.
		'''
		cursor = self.textCursor()
		cursor.beginEditBlock()

		cursor.removeSelectedText()
		cursor.insertText(word)

		cursor.endEditBlock()


class Highlighter(QSyntaxHighlighter):

	WORDS = u'(?iu)[\w\']+'

	def __init__(self, *args):
		QSyntaxHighlighter.__init__(self, *args)

		self.dict = None
		self.ulist = []

	def setParent(self,parent):
		self.parent = parent

	def setDict(self, dict):
		self.dict = dict

	def highlightBlock(self, text):
		if not self.dict:
			return

		# if not self.parent.gui.spellcheck:
		# 	return
		if not erk.config.SPELLCHECK_INPUT:
			return

		format = QTextCharFormat()
		format.setUnderlineColor(Qt.red)
		format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

		for word_object in re.finditer(self.WORDS, text):

			misspelled = self.dict.unknown([word_object.group()])
			if len(misspelled)>0:
				self.setFormat(word_object.start(), word_object.end() - word_object.start(), format)

class SpellAction(QAction):
	correct = pyqtSignal(str)

	def __init__(self, *args):
		QAction.__init__(self, *args)

		self.triggered.connect(lambda x: self.correct.emit(
			self.text()))