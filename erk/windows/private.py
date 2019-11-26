
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *
from erk.resources import *
from erk.strings import *
from erk.config import *
from erk.format import *
from erk.spelledit import *
import erk.events
import erk.input

class Window(QMainWindow):

	def set_uptime(self,uptime):

		self.uptime = uptime

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

	def closeEvent(self, event):

		erk.events.erk_parted_private(self.gui,self.client,self.name)

		if len(self.newlog)>0:
			if self.gui.save_private_logs:
				saveLog(self.client.network,self.name,self.newlog)

		if self.gui.title_from_active:
			self.gui.setWindowTitle(APPLICATION_NAME)

		self.subwindow.close()
		self.close()
		event.accept()

	def handleUserInput(self):
		user_input = self.userTextInput.text()
		self.userTextInput.setText('')

		if self.gui.window_command_history:
			# remove blank entry
			clean = []
			for c in self.history_buffer:
				if c=='': continue
				clean.append(c)
			self.history_buffer = clean

			self.history_buffer.insert(0,user_input)
			if len(self.history_buffer)>self.history_buffer_max:
				self.history_buffer.pop()
			self.history_buffer_pointer = -1

			# add blank entry
			self.history_buffer.append('')

			# remove commands that are repeated
			# one after the other
			self.history_buffer = [self.history_buffer[i] for i in range(len(self.history_buffer)) if (i==0) or self.history_buffer[i] != self.history_buffer[i-1]]

		erk.input.private_window_input(self.gui,self.client,self,user_input)

	def writeText(self,text):

		self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		self.channelChatDisplay.update()

	def rerenderText(self):

		self.channelChatDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])
		self.userTextInput.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		self.channelChatDisplay.clear()
		for entry in self.log:
			mtype = entry[0]
			user = entry[1]
			message = entry[2]
			timestamp = entry[3]

			line = render_message(
				self.gui.styles,
				mtype,
				user,
				message,
				timestamp,
				self.gui.max_nick_size,
				self.gui.strip_html,
				self.gui.irc_color,
				self.gui.create_links,
				self.gui.show_timestamps,
				self.gui.show_timestamp_seconds,
				self.gui.show_timestamp_24hour_clock,
				self.gui.filter_profanity,
				False,
			)

			self.channelChatDisplay.append(line)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

	def writeLog(self,mtype,user,message):

		is_unseen = self.gui.window_activity_is_unseen(self)

		if mtype==CHAT_MESSAGE or mtype==ACTION_MESSAGE or mtype==NOTICE_MESSAGE:
			self.gui.window_activity(self)

		if self.gui.window_activity_is_unseen(self)!=is_unseen:
			# Window *just* got added to the unseen list
			if self.gui.mark_unread_messages:
				self.channelChatDisplay.insertHtml(UNSEEN_MESSAGES_MARKER)
			if self.gui.flash_unread_private:
				self.gui.app.alert(self)

		timestamp = datetime.timestamp(datetime.now())

		line = render_message(
			self.gui.styles,
			mtype,
			user,
			message,
			timestamp,
			self.gui.max_nick_size,
			self.gui.strip_html,
			self.gui.irc_color,
			self.gui.create_links,
			self.gui.show_timestamps,
			self.gui.show_timestamp_seconds,
			self.gui.show_timestamp_24hour_clock,
			self.gui.filter_profanity,
			False,
		)

		self.channelChatDisplay.append(line)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		entry = [mtype,user,message,datetime.timestamp(datetime.now())]
		self.log.append(entry)
		self.newlog.append(entry)

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

		self.uptime = 0

		self.is_channel = False
		self.is_console = False
		self.is_user = True

		self.history_buffer = ['']
		self.history_buffer_pointer = 0
		# self.history_buffer_max = 20
		self.history_buffer_max = self.gui.window_command_history_length

		self.nicks = [self.name]

		self.log = []
		self.newlog = []

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(USER_WINDOW_ICON))

		self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)

		self.userTextInput = SpellTextEdit(self)
		self.userTextInput.setObjectName("userTextInput")
		self.userTextInput.returnPressed.connect(self.handleUserInput)

		# Text input widget should only be one line
		fm = self.userTextInput.fontMetrics()
		self.userTextInput.setFixedHeight(fm.height()+9)
		self.userTextInput.setWordWrapMode(QTextOption.NoWrap)
		self.userTextInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.userTextInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.userTextInput.changeLanguage(self.gui.spellCheckLanguage)

		self.userTextInput.keyUp.connect(self.keyPressUp)
		self.userTextInput.keyDown.connect(self.keyPressDown)

		self.channelChatDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])
		self.userTextInput.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		finalLayout.addWidget(self.channelChatDisplay)
		finalLayout.addWidget(self.userTextInput)

		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		# Load logs
		if self.gui.load_private_logs:
			self.log = loadLog(self.client.network,self.name)
			if len(self.log)>0:
				if len(self.log)>self.gui.load_log_max:
					self.log = trimLog(self.log,self.gui.load_log_max)
				self.rerenderText()

	def keyPressDown(self):
		if self.gui.window_command_history:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer - 1
			if self.history_buffer_pointer < 0:
				self.history_buffer_pointer = len(self.history_buffer) - 1
			self.userTextInput.setText(self.history_buffer[self.history_buffer_pointer])

	def keyPressUp(self):
		if self.gui.window_command_history:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer + 1
			if len(self.history_buffer) - 1 < self.history_buffer_pointer:
				self.history_buffer_pointer = 0
			self.userTextInput.setText(self.history_buffer[self.history_buffer_pointer])
