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

import sys
import os
from datetime import datetime
import shlex

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore

from erk.common import *

from erk.gui.spelledit import *

import emoji

def getTimestamp():
	return datetime.timestamp(datetime.now())

def createNew(channel,client,serverid,MDI,parent=None):

		newSubwindow = QMdiSubWindow()
		newWindow = Interface(channel,client,serverid,newSubwindow,parent)
		newSubwindow.setWidget(newWindow)
		MDI.addSubWindow(newSubwindow)

		newSubwindow.resize(parent.initialWindowWidth,parent.initialWindowHeight)

		newSubwindow.show()

		q = ErkWindow(channel,serverid,newWindow,newSubwindow)

		return q

class Interface(QMainWindow):

	def changeEvent(self,event):

		# if event.type() == QEvent.WindowStateChange:
		# 	if event.oldState() and Qt.WindowMinimized:
		# 		# window has been minimized
		# 		self.stateMinimized = True
		# 		self.stateNormal = False
		# 		self.stateMaximized = False
		# 	elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
		# 		# window is not minimized
		# 		self.stateNormal = False
		# 		self.stateMinimized = False
		# 		self.stateMaximized = True
		# 	else:
		# 		self.stateNormal = True
		# 		self.stateMinimized = False
		# 		self.stateMaximized = False

		if self.loaded:
			self.channelChatDisplay.moveCursor(QTextCursor.End)
			self.channelChatDisplay.update()


	def toolMini(self):
		if self.isMinimized():
			self.showNormal()
		else:
			self.showMinimized()

	def toolMaxi(self):
		if self.isMaximized():
			self.showNormal()
		else:
			self.showMaximized()


	def __init__(self,name,client,serverid,subwindow,parent=None):
		super(Interface, self).__init__(parent)

		self.name = name
		self.client = client
		self.parent = parent
		self.serverid = serverid
		self.subwindow = subwindow

		self.stateNormal = True
		self.stateMinimized = False
		self.stateMaximized = False

		self.active = True

		self.topic = ''

		self.loaded = False
		self.ontop = False

		if parent.logChatByNetwork:
			self.serverhost = parent.connections[serverid].network
		else:
			self.serverhost = parent.connections[serverid].host + ":" + str(parent.connections[serverid].port)

		self.nickname = client.nickname

		# Load in any logs, if they exist
		#self.log = loadLog(self.serverhost,name)

		self.hidden = False

		if len(name)>0 and name[0]=='#':
			self.is_channel = True
		else:
			self.is_channel = False

		self.userlist = []		# User list with hostmasks
		self.users = []			# User list with nicknames and channel privs
		self.rawusers = []		# User list with hostmasks, nicknames, and channel privs

		self.history_buffer = []
		self.history_buffer_pointer = 0
		self.history_buffer_max = 20

		self.modeson = ''
		self.modesoff = ''
		self.key = ''

		self.kicked = False

		self.banlist = []

		self.displayTimestamp = parent.displayTimestamp

		self.is_op = False
		self.is_voiced = False
		self.away = False

		self.notified = False

		self.buildInterface()

	def addModes(self,modes):
		for l in modes.split():
			if l in self.modesoff:
				self.modesoff = self.modesoff.replace(l,'')
			if l in self.modeson:
				pass
			else:
				self.modeson = self.modeson + l

		self.rebuildModesMenu()

	def removeModes(self,modes):
		for l in modes.split():
			if l in self.modeson:
				self.modeson = self.modeson.replace(l,'')
			if l in self.modesoff:
				pass
			else:
				self.modesoff = self.modesoff + l

		self.rebuildModesMenu()

	def doTopicCopy(self):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(f"{self.topic}", mode=cb.Clipboard)

	def doUserCopy(self):
		users = self.parent.windows[self.name].users

		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText("\n".join(users), mode=cb.Clipboard)

	def doIRCUrlCopy(self):

		url = "irc://" + self.parent.connections[self.serverid].host + ":" + str(self.parent.connections[self.serverid].port) +"/" + self.name

		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(f"{url}", mode=cb.Clipboard)

	def rebuildBanMenu(self):
		self.actBans.clear()

		if len(self.banlist)==0:
			mBan = QAction("None",self)
			f = mBan.font()
			f.setItalic(True)
			mBan.setFont(f)
			self.actBans.addAction(mBan)
			return

		for b in self.banlist:
			ban = b[0]
			banner = b[1]

			if '@' in ban:
				# host ban
				mBan = QAction(QIcon(SERVER_ICON),f"{ban} (by {banner})",self)
			else:
				# nick ban
				mBan = QAction(QIcon(USER_ICON),f"{ban} (by {banner})",self)
			self.actBans.addAction(mBan)

	def rebuildModesMenu(self):
		self.actModes.clear()

		mset = ''

		for l in self.modeson:

			if l == "k":
				if "k" in mset: continue
				mMode = QAction(QIcon(LOCKED_ICON),f"Channel is locked (key: \"{self.key}\")",self)
				self.actModes.addAction(mMode)
				mset = mset + "k"
				continue

			if l == "c":
				if "c" in mset: continue
				mMode = QAction(QIcon(BAN_ICON),"Colors forbidden",self)
				self.actModes.addAction(mMode)
				mset = mset + "c"
				continue

			if l == "C":
				if "C" in mset: continue
				mMode = QAction(QIcon(BAN_ICON),"CTCP forbidden",self)
				self.actModes.addAction(mMode)
				mset = mset + "C"
				continue

			if l == "m":
				if "m" in mset: continue
				mMode = QAction(QIcon(MODERATED_ICON),"Moderation on",self)
				self.actModes.addAction(mMode)
				mset = mset + "m"
				continue

			if l == "n":
				if "n" in mset: continue
				mMode = QAction(QIcon(BAN_ICON),"External messages forbidden",self)
				self.actModes.addAction(mMode)
				mset = mset + "n"
				continue

			if l == "p":
				if "p" in mset: continue
				mMode = QAction(QIcon(CHANNEL_WINDOW_ICON),"Channel is private",self)
				self.actModes.addAction(mMode)
				mset = mset + "p"
				continue

			if l == "s":
				if "s" in mset: continue
				mMode = QAction(QIcon(CHANNEL_WINDOW_ICON),"Channel is secret",self)
				self.actModes.addAction(mMode)
				mset = mset + "s"
				continue

			if l == "t":
				if "t" in mset: continue
				mMode = QAction(QIcon(USER_ICON),"Only ops can change topic",self)
				self.actModes.addAction(mMode)
				mset = mset + "t"
				continue

		if len(mset)==0:
			mMode = QAction(QIcon(UNKNOWN_ICON),"Unknown",self)
			self.actModes.addAction(mMode)

	def setAway(self,msg=None):
		self.away = True
		if msg!=None:
			d = systemTextDisplay(f"You have been set as away ({msg}).",self.parent.maxnicklen,SYSTEM_COLOR)
			#self.menuAway.setText(f"You are away ({msg}).")
		else:
			d = systemTextDisplay(f"You have been set as away.",self.parent.maxnicklen,SYSTEM_COLOR)
			#self.menuAway.setText(f"You are away.")
		self.writeText(d)
		#self.menuAway.setVisible(True)

	def setBack(self):
		self.away = False
		#self.menuAway.setVisible(False)
		d = systemTextDisplay(f"You have been set as back.",self.parent.maxnicklen,SYSTEM_COLOR)
		self.writeText(d)

	def trimLog(self,ilog):
		count = 0
		shortlog = []
		for line in reversed(ilog):
			count = count + 1
			shortlog.append(line)
			if count >= self.parent.maxlogsize:
				break
		return list(reversed(shortlog))

	def toolNameRed(self):
		self.toolbarName.setStyleSheet("color: red;")
		if self.parent.unreadNotify:
			if not self.notified:
				self.notified = True

				# Don't play sound if sound is enabled
				if not self.parent.noSound:
					# Play notification sound
					self.parent.notifySound.play()

	def toolNameNormal(self):
		self.toolbarName.setStyleSheet("")
		self.notified = False

	def showMenus(self):
		self.menubar.setVisible(True)
		self.toolbar.setVisible(False)

	def showToolbar(self):
		self.menubar.setVisible(False)
		self.toolbar.setVisible(True)

	def toolbarMoved(self,moved):
		if moved:
			# toolbar is floating
			self.buttonMinimize.setEnabled(True)
			self.buttonMaximize.setEnabled(True)
			self.buttonNormalize.setEnabled(True)

			self.buttonMinimize.setIcon(QIcon(MINIMIZE_ICON))
			self.buttonMaximize.setIcon(QIcon(MAXIMIZE_ICON))
			self.buttonNormalize.setIcon(QIcon(RESTORE_ICON))
		else:
			# toolbar is fixed
			self.buttonMinimize.setEnabled(False)
			self.buttonMaximize.setEnabled(False)
			self.buttonNormalize.setEnabled(False)

			self.buttonMinimize.setIcon(QIcon(BLANK_ICON))
			self.buttonMaximize.setIcon(QIcon(BLANK_ICON))
			self.buttonNormalize.setIcon(QIcon(BLANK_ICON))

	def toolbarNameClicked(self):
		if not self.active:
			self.showNormal()
		
	def buildInterface(self):
		self.setWindowTitle(" "+self.name)

		self.status = self.statusBar()
		self.status.addPermanentWidget(QLabel(" "),0)

		servlabel = QLabel(f"{self.client.hostname}")
		servlabel.setAlignment(Qt.AlignRight)
		servlabel.setFont(self.parent.fontitalic)
		self.status.addPermanentWidget(servlabel,1)

		self.status.addPermanentWidget(QLabel(" "),0)

		self.status.setStyleSheet('QStatusBar::item {border: None;}')
		self.status.setSizeGripEnabled(False)

		self.toolbar = QToolBar(self)
		self.addToolBar(Qt.TopToolBarArea,self.toolbar)
		#self.toolbar.setIconSize(QSize(25,25))
		self.toolbar.setFloatable(True)
		self.toolbar.setAllowedAreas( Qt.TopToolBarArea | Qt.BottomToolBarArea )
		self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

		self.toolbar.topLevelChanged.connect(self.toolbarMoved)
		
		self.menubar = self.menuBar()

		class NameLabel(QLabel):
			clicked = pyqtSignal()

			def mousePressEvent(self,event):
				self.clicked.emit()

		self.toolbarName = NameLabel("&nbsp;<b><big>"+self.name+"</big></b>")
		self.toolbar.addWidget(self.toolbarName)

		self.toolbarName.clicked.connect(self.toolbarNameClicked)


		self.toolbar.addWidget(QLabel(" "))


		if self.is_channel:

			actMenu = self.menubar.addMenu("Channel")

			# self.menuAway = QAction(QIcon(USER_ICON),"You are away.",self)
			# self.menuAway.setFont(self.parent.fontitalic)
			# actMenu.addAction(self.menuAway)
			# self.menuAway.setVisible(False)

			self.actModes = actMenu.addMenu(QIcon(CHANNEL_WINDOW_ICON),"Modes")

			self.actBans = actMenu.addMenu(QIcon(BAN_ICON),"Bans")

			actMenu.addSeparator()

			self.actPart = QAction(QIcon(EXIT_ICON),"Leave channel",self)
			self.actPart.triggered.connect(self.close)
			actMenu.addAction(self.actPart)

			self.rebuildModesMenu()

			self.toolbarMain = QPushButton(" Modes ")
			self.toolbarMain.setToolTip(f"Channel modes")

			self.toolbarMain.setStyleSheet("QPushButton { border: 0px; }")
			self.toolbarMain.setMenu(self.actModes)

			self.toolbarBans = QPushButton(" Bans ")
			self.toolbarBans.setToolTip(f"Channel bans")

			self.toolbarBans.setStyleSheet("QPushButton { border: 0px; }")
			self.toolbarBans.setMenu(self.actBans)

			optMenu = self.menubar.addMenu("Options")

			optTime = QAction("Display timestamp",self,checkable=True)
			optTime.setChecked(self.displayTimestamp)
			optTime.triggered.connect(self.toggleTimestamp)
			optMenu.addAction(optTime)

			topOntop = QAction("Always on top",self,checkable=True)
			topOntop.setChecked(self.ontop)
			topOntop.triggered.connect(self.toggleTop)
			optMenu.addAction(topOntop)

			optMenu.addSeparator()

			self.actText = QAction(QIcon(SAVE_ICON),"Export log as plaintext",self)
			self.actText.triggered.connect(self.saveAsTextDialog)
			optMenu.addAction(self.actText)

			clipMenu = optMenu.addMenu(QIcon(CLIPBOARD_ICON),"Copy to clipboard")

			self.actSaveUrl = QAction(QIcon(SERVER_ICON),"IRC server/channel URL",self)
			self.actSaveUrl.triggered.connect(self.doIRCUrlCopy)
			clipMenu.addAction(self.actSaveUrl)

			self.actSaveTopic = QAction(QIcon(CHANNEL_WINDOW_ICON),"Topic",self)
			self.actSaveTopic.triggered.connect(self.doTopicCopy)
			clipMenu.addAction(self.actSaveTopic)

			self.actSaveUsers = QAction(QIcon(USERS_ICON),"User list",self)
			self.actSaveUsers.triggered.connect(self.doUserCopy)
			clipMenu.addAction(self.actSaveUsers)


			self.toolbarOptions = QPushButton(" Options ")
			self.toolbarOptions.setToolTip(f"Window options")
			self.toolbarOptions.setStyleSheet("QPushButton { border: 0px; }")
			self.toolbarOptions.setMenu(optMenu)

			self.toolbar.addSeparator()

			self.toolbar.addWidget(self.toolbarMain)
			self.toolbar.addWidget(self.toolbarBans)
			self.toolbar.addWidget(self.toolbarOptions)

		else:

			# User window
			actMenu = self.menubar.addMenu("Private")

			# self.menuAway = QAction(QIcon(USER_ICON),"You are away.",self)
			# actMenu.addAction(self.menuAway)
			# self.menuAway.setVisible(False)

			# actMenu.addSeparator()

			self.actPart = QAction(QIcon(EXIT_ICON),"Close Window",self)
			self.actPart.triggered.connect(self.close)
			actMenu.addAction(self.actPart)

			optMenu = self.menubar.addMenu("Options")

			optTime = QAction("Display timestamp",self,checkable=True)
			optTime.setChecked(self.displayTimestamp)
			optTime.triggered.connect(self.toggleTimestamp)
			optMenu.addAction(optTime)

			topOntop = QAction("Always on top",self,checkable=True)
			topOntop.setChecked(self.ontop)
			topOntop.triggered.connect(self.toggleTop)
			optMenu.addAction(topOntop)

			optMenu.addSeparator()

			self.actText = QAction(QIcon(SAVE_ICON),"Export log as plaintext",self)
			self.actText.triggered.connect(self.saveAsTextDialog)
			optMenu.addAction(self.actText)

			self.toolbarOptions = QPushButton(" Options ")
			self.toolbarOptions.setStyleSheet("QPushButton { border: 0px; }")
			self.toolbarOptions.setMenu(optMenu)
			#self.toolbarOptions.setIcon(QIcon(SETTINGS_ICON))

			self.toolbar.addWidget(self.toolbarOptions)

		self.toolbar.addWidget(QLabel("     "))

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.toolbar.addWidget(spacer)

		# WINDOW CONTROLS

		self.buttonMinimize = QPushButton()
		self.buttonMinimize.setIcon(QIcon(BLANK_ICON))
		# self.buttonMinimize.clicked.connect(self.showMinimized)
		self.buttonMinimize.clicked.connect(self.toolMini)
		self.buttonMinimize.setFixedHeight(25)
		self.buttonMinimize.setStyleSheet("QPushButton { border: 0px; }")

		self.buttonMaximize = QPushButton()
		self.buttonMaximize.setIcon(QIcon(BLANK_ICON))
		# self.buttonMaximize.clicked.connect(self.showMaximized)
		self.buttonMaximize.clicked.connect(self.toolMaxi)
		self.buttonMaximize.setFixedHeight(25)
		self.buttonMaximize.setStyleSheet("QPushButton { border: 0px; }")

		self.buttonNormalize = QPushButton()
		self.buttonNormalize.setIcon(QIcon(BLANK_ICON))
		self.buttonNormalize.clicked.connect(self.showNormal)
		self.buttonNormalize.setFixedHeight(25)
		self.buttonNormalize.setStyleSheet("QPushButton { border: 0px; }")

		self.buttonMinimize.setEnabled(False)
		self.buttonMaximize.setEnabled(False)
		self.buttonNormalize.setEnabled(False)

		self.toolbar.addWidget(self.buttonMinimize)
		self.toolbar.addWidget(self.buttonMaximize)
		self.toolbar.addWidget(self.buttonNormalize)

		self.toolbar.addWidget(QLabel("  "))

		# WINDOW CONTROLS

		buttonLeave = QPushButton()
		buttonLeave.setIcon(QIcon(TOOLBAR_DISCONNECT_ICON))
		buttonLeave.setToolTip(f"Leave {self.name}")
		buttonLeave.clicked.connect(self.close)
		self.toolbar.addWidget(buttonLeave)
		buttonLeave.setFixedHeight(25)
		buttonLeave.setStyleSheet("QPushButton { border: 0px; }")

		if self.parent.windowToolbars:
			self.menubar.setVisible(False)
			self.toolbar.setVisible(True)
		else:
			self.menubar.setVisible(True)
			self.toolbar.setVisible(False)

		if self.is_channel:
			self.setWindowIcon(QIcon(CHANNEL_WINDOW_ICON))
			#self.setWindowIcon(self.parent.CHANNEL_WINDOW_ICON)
		else:
			#self.setWindowIcon(self.parent.USER_WINDOW_ICON)
			self.setWindowIcon(QIcon(USER_WINDOW_ICON))

		# Main window

		self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)

		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)

		if self.is_channel:
			self.channelUserDisplay = QListWidget(self)
			self.channelUserDisplay.setObjectName("channelUserDisplay")
			self.channelUserDisplay.setFont(self.parent.fontUsers)
			self.channelUserDisplay.installEventFilter(self)

		self.userTextInput = SpellTextEdit(self)
		self.userTextInput.setObjectName("userTextInput")
		self.userTextInput.returnPressed.connect(self.handleUserInput)

		self.userTextInput.keyUp.connect(self.keyPressUp)
		self.userTextInput.keyDown.connect(self.keyPressDown)

		# Text input widget should only be one line
		fm = self.userTextInput.fontMetrics()
		self.userTextInput.setFixedHeight(fm.height()+9)
		self.userTextInput.setWordWrapMode(QTextOption.NoWrap)
		self.userTextInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.userTextInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		# Layout
		if self.is_channel:
			self.horizontalSplitter = QSplitter(Qt.Horizontal)
			self.horizontalSplitter.addWidget(self.channelChatDisplay)
			self.horizontalSplitter.addWidget(self.channelUserDisplay)
			self.horizontalSplitter.setSizes([390,110])

		self.verticalSplitter = QSplitter(Qt.Vertical)
		if self.is_channel:
			self.verticalSplitter.addWidget(self.horizontalSplitter)
		else:
			self.verticalSplitter.addWidget(self.channelChatDisplay)
		self.verticalSplitter.addWidget(self.userTextInput)
		self.verticalSplitter.setSizes([475,25])

		# Make sure the background and text color is from the colors.json
		# This is loaded into the parent at startup
		# self.channelChatDisplay.setStyleSheet(f"background-color: {self.parent.display['background']}; color: {self.parent.display['text']};")
		# self.userTextInput.setStyleSheet(f"background-color: {self.parent.display['background']}; color: {self.parent.display['text']};")
		# if self.is_channel: self.channelUserDisplay.setStyleSheet(f"background-color: {self.parent.display['background']}; color: {self.parent.display['text']};")

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(0, 0, 0, 0)
		finalLayout.addWidget(self.verticalSplitter)

		x = QWidget()
		x.setLayout(finalLayout)
		self.setCentralWidget(x)

		self.userTextInput.setFocus()

		self.newChatDivider = NEW_CHAT_DIVIDER

		# Inject chat divider custom colors
		#self.newChatDivider = self.newChatDivider.replace(NEW_CHAT_DIVIDER_TEXT_COLOR,self.parent.display["new-chat-divider-text"])
		#self.newChatDivider = self.newChatDivider.replace(NEW_CHAT_DIVIDER_BACKGROUND_COLOR,self.parent.display["new-chat-divider"])

		if self.parent.loadLogsOnJoin:

			# Load in any logs, if they exist
			self.log = loadLog(self.serverhost,self.name)

			# Limit the size of the loaded log
			if self.parent.maxlogsize <= 0:
				shortlog = self.log
			elif len(self.log)>self.parent.maxlogsize:
				shortlog = self.trimLog(self.log)
			else:
				shortlog = self.log

			# Now, load in logs
			# if len(self.log)>0:
			# 	for line in self.log:

			if len(shortlog)>0:
				for line in shortlog:

					if len(line[LOG_TEXT])>0:
						text = line[LOG_TEXT]
						timestamp = line[LOG_TIMESTAMP]

						if self.displayTimestamp:
							#pretty = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
							if self.parent.timestampSeconds:
								secs = ':%S'
							else:
								secs = ''
							if self.parent.timestamp24:
								pretty = datetime.fromtimestamp(timestamp).strftime('%H:%M' + secs)
							else:
								pretty = datetime.fromtimestamp(timestamp).strftime('%I:%M' + secs)

							#pretty = "&nbsp;" + pretty + "&nbsp;"
							tt = TIMESTAMP_TEMPLATE.replace("!TIME!",pretty)
							text = text.replace("!TIMESTAMP!",tt)
						else:
							text = text.replace("!TIMESTAMP!","")

						# Apply colors
						text = self.applyColors(text,self.parent.display)

						self.channelChatDisplay.append(text)

				chatDivider = self.applyColors(self.newChatDivider,self.parent.display)

				self.channelChatDisplay.append(chatDivider)
				e = [0,self.newChatDivider]
				self.log.append(e)
				self.channelChatDisplay.moveCursor(QTextCursor.End)
		else:
			self.log = []

		# Interface is built and loaded
		self.loaded = True

	def rerenderTextDisplay(self):

		self.channelChatDisplay.clear()

		if len(self.log)>self.parent.maxlogsize:
			shortlog = self.trimLog(self.log)
		else:
			shortlog = self.log

		# for line in self.log:
		for line in shortlog:

			if len(line[LOG_TEXT])>0:
				text = line[LOG_TEXT]
				timestamp = line[LOG_TIMESTAMP]

				if timestamp == 0:
					# Apply colors
					text = self.applyColors(text,self.parent.display)
					self.channelChatDisplay.append(text)
					continue

				if self.displayTimestamp:
					# pretty = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')

					#pretty = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

					if self.parent.timestampSeconds:
						secs = ':%S'
					else:
						secs = ''
					if self.parent.timestamp24:
						pretty = datetime.fromtimestamp(timestamp).strftime('%H:%M' + secs)
					else:
						pretty = datetime.fromtimestamp(timestamp).strftime('%I:%M' + secs)

					#pretty = "&nbsp;" + pretty + "&nbsp;"
					tt = TIMESTAMP_TEMPLATE.replace("!TIME!",pretty)
					text = text.replace("!TIMESTAMP!",tt)
				else:
					text = text.replace("!TIMESTAMP!","")

				# Apply colors
				text = self.applyColors(text,self.parent.display)

				self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)


	def toggleTimestamp(self):
		if self.displayTimestamp:
			self.displayTimestamp = False
		else:
			self.displayTimestamp = True

		self.rerenderTextDisplay()

	def toggleTop(self):
		if self.ontop:
			self.ontop = False
			self.subwindow.setWindowFlags(self.subwindow.windowFlags() & ~Qt.WindowStaysOnTopHint)
		else:
			self.ontop = True
			self.subwindow.setWindowFlags(self.subwindow.windowFlags() | Qt.WindowStaysOnTopHint)


	def getUserHostmask(self,nick):
		for u in self.userlist:
			if '!' in u:
				up = u.split('!')
				if nick == up[0]:
					m = up[1].split('@')
					return m[1]
		return None

	def setUserList(self,ulist):
		self.channelUserDisplay.clear()
		self.userlist = []
		self.users = []
		self.rawusers = ulist
		for n in ulist:
			p = n.split('!')

			# Strip channel status symbols for storage
			ue = n
			if ue[0]=='@': ue = ue.replace('@','',1)
			if ue[0]=='+': ue = ue.replace('+','',1)
			if ue[0]=='~': ue = ue.replace('~','',1)
			if ue[0]=='&': ue = ue.replace('&','',1)
			if ue[0]=='%': ue = ue.replace('%','',1)
			self.userlist.append(ue)

			# Check for client channel status
			if p[0] == self.nickname:
				self.is_op = False
				self.is_voiced = False
			if p[0] == f"+{self.nickname}": self.is_voiced = True
			if p[0] == f"@{self.nickname}": self.is_op = True

			# Store user list
			self.users.append(p[0])

			self.redrawUserlist()

	def redrawUserlist(self):

		self.channelUserDisplay.clear()
		for u in self.rawusers:
			p = u.split('!')
			if len(p)==2:
				user = p[0]
			else:
				user = p

			if type(user)==list:
				user = str( list(user).pop(0)  )

			ui = QListWidgetItem()
			if user[:1]=='@':
				if self.parent.prettyUserlist:

					ui.setIcon(QIcon(OPERATOR_ICON))
					#ui.setIcon(self.parent.OPERATOR_ICON)

					user = user.replace('@','')
			elif user[:1]=='+':
				if self.parent.prettyUserlist:

					ui.setIcon(QIcon(VOICED_ICON))
					#ui.setIcon(self.parent.VOICED_ICON)

					user = user.replace('+','')
			else:
				if self.parent.prettyUserlist:

					ui.setIcon(QIcon(NORMAL_ICON))
					#ui.setIcon(self.parent.NORMAL_ICON)

			ui.setText(user)
			self.channelUserDisplay.addItem(ui)


	def cleanUserList(self,ulist):
		self.channelUserDisplay.clear()

	def addUser(self,data):
		#self.channelUserDisplay.addItem(data)
		self.rawusers.append(data)

		p = data.split('!')
		if len(p)==2:
			self.users.append(p[0])
		else:
			self.users.append(data)

		if data[0]=='@': data = data.replace('@','',1)
		if data[0]=='+': data = data.replace('+','',1)
		if data[0]=='~': data = data.replace('~','',1)
		if data[0]=='&': data = data.replace('&','',1)
		if data[0]=='%': data = data.replace('%','',1)
		self.userlist.append(str(data))

		#print(data)

		self.redrawUserlist()

	def hasUser( self, text ):
		for u in [str(self.channelUserDisplay.item(i).text()) for i in range(self.channelUserDisplay.count())]:
			u = u.replace('@','')
			u = u.replace('+','')
			u = u.replace('~','')
			u = u.replace('&','')
			u = u.replace('%','')
			if u == text: return True
		return False

	def getUserNicks(self):
		ulist = []
		ulist.append(self.serverid)
		if self.is_channel:
			for u in [str(self.channelUserDisplay.item(i).text()) for i in range(self.channelUserDisplay.count())]:
				u = u.replace('@','')
				u = u.replace('+','')
				u = u.replace('~','')
				u = u.replace('&','')
				u = u.replace('%','')
				ulist.append(u)
		# ulist.append(self.name)
		# for u in self.parent.getChannelList(self.serverid):
		# 	ulist.append(u)
		return ulist

	def removeUser( self, text ):

		c = []
		ul = []
		ull = []

		for e in self.rawusers:
			if e==text: continue
			p = e.split('!')
			if len(p)==2:
				u = p[0]
			else:
				u = e
			if u[0]=='@': u = u.replace('@','',1)
			if u[0]=='+': u = u.replace('+','',1)
			if u[0]=='~': u = u.replace('~','',1)
			if u[0]=='&': u = u.replace('&','',1)
			if u[0]=='%': u = u.replace('%','',1)
			if u == text: continue
			c.append(e)
			ul.append(u)
			if e[0]=='@': e = e.replace('@','',1)
			if e[0]=='+': e = e.replace('+','',1)
			if e[0]=='~': e = e.replace('~','',1)
			if e[0]=='&': e = e.replace('&','',1)
			if e[0]=='%': e = e.replace('%','',1)
			ull.append(e)
		self.rawusers = c
		self.users = ul
		self.userlist = ull

		self.redrawUserlist()

	def writeText(self,text):

		t = getTimestamp()
		self.log.append([t,text])

		if self.displayTimestamp:
			#pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')
			if self.parent.timestampSeconds:
				secs = ':%S'
			else:
				secs = ''
			if self.parent.timestamp24:
				pretty = datetime.fromtimestamp(t).strftime('%H:%M' + secs)
			else:
				pretty = datetime.fromtimestamp(t).strftime('%I:%M' + secs)
			#pretty = "&nbsp;" + pretty + "&nbsp;"
			tt = TIMESTAMP_TEMPLATE.replace("!TIME!",pretty)
			text = text.replace("!TIMESTAMP!",tt)
		else:
			text = text.replace("!TIMESTAMP!","")

		# Apply colors
		text = self.applyColors(text,self.parent.display)

		self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		self.channelChatDisplay.update()

	def keyPressDown(self):
		if len(self.history_buffer) == 0: return
		self.history_buffer_pointer = self.history_buffer_pointer - 1
		if self.history_buffer_pointer < 0:
			self.history_buffer_pointer = len(self.history_buffer) - 1
		self.userTextInput.setText(self.history_buffer[self.history_buffer_pointer])

	def keyPressUp(self):
		if len(self.history_buffer) == 0: return
		self.history_buffer_pointer = self.history_buffer_pointer + 1
		if len(self.history_buffer) - 1 < self.history_buffer_pointer:
			self.history_buffer_pointer = 0
		self.userTextInput.setText(self.history_buffer[self.history_buffer_pointer])

	# Handle user input
	def handleUserInput(self):

		user_input = self.userTextInput.text()
		self.userTextInput.setText('')

		self.history_buffer.insert(0,user_input)
		if len(self.history_buffer)>self.history_buffer_max:
			self.history_buffer.pop()
		self.history_buffer_pointer = -1

		# Inject emojis
		if self.parent.emojis:
			user_input = emoji.emojize(user_input,use_aliases=True)

		# Inject ASCIImojis
		if self.parent.asciimojis:
			user_input = inject_asciiemojis(user_input)

		# COMMANDS BEGIN

		try:
			tokens = shlex.split(user_input)
		except ValueError:
			tokens = user_input.split(' ')

		if len(tokens)>0:

			if tokens[0].lower() == "/help":

				h = "<br>".join(cmdHelp())
				d = systemTextDisplay(h,self.parent.maxnicklen,SYSTEM_COLOR)
				self.writeText(d)
				return

			# /color
			if tokens[0].lower() == "/color":
				if len(tokens)>=3:
					tokens.pop(0)
					fore = tokens.pop(0)
					back = tokens.pop(0)

					if is_integer(back):
						if is_integer(fore):

							if int(fore)>=0:
								if int(fore)<=15:
									# valid color
									pass
								else:
									d = systemTextDisplay(f"\"{fore}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
									self.writeText(d)
									return
							else:
								d = systemTextDisplay(f"\"{fore}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
								self.writeText(d)
								return

							if int(back)>=0:
								if int(back)<=15:
									# valid color
									pass
								else:
									d = systemTextDisplay(f"\"{back}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
									self.writeText(d)
									return
							else:
								d = systemTextDisplay(f"\"{back}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
								self.writeText(d)
								return
							
							msg = ' '.join(tokens)
							html = irc_color_full(int(fore),int(back),msg)
							if len(back)==1: back = f"0{back}"
							if len(fore)==1: fore = f"0{fore}"
							msg = chr(3) + fore + ',' + back + msg + chr(3)
							self.client.msg(self.name,msg)

							d = chat_display_no_strip(self.nickname,html,self.parent.maxnicklen,self.parent.urlsToLinks,SELF_COLOR)
							self.parent.writeToChatWindow(self.serverid,self.name,d)
							return
						else:
							d = systemTextDisplay(f"\"{fore}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
							self.writeText(d)
							return
					else:
						if is_integer(fore):

							if int(fore)>=0:
								if int(fore)<=15:
									# valid color
									pass
								else:
									d = systemTextDisplay(f"\"{fore}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
									self.writeText(d)
									return
							else:
								d = systemTextDisplay(f"\"{fore}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
								self.writeText(d)
								return

							msg = back + " " + ' '.join(tokens)
							html = irc_color(int(fore),msg)
							msg = chr(3) + fore + msg + chr(3)
							self.client.msg(self.name,msg)

							d = chat_display_no_strip(self.nickname,html,self.parent.maxnicklen,self.parent.urlsToLinks,SELF_COLOR)
							self.parent.writeToChatWindow(self.serverid,self.name,d)
							return
						else:
							d = systemTextDisplay(f"\"{fore}\" is not a valid color",self.parent.maxnicklen,SYSTEM_COLOR)
							self.writeText(d)
							return

			# /nick
			if tokens[0].lower() == "/nick":
				if len(tokens)==2:
					newnick = tokens[1]
					self.client.setNick(newnick)
					return
				else:
					d = systemTextDisplay(f"USAGE: /nick NEW_NICKNAME<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /quit
			if tokens[0].lower() == "/quit":
				if len(tokens)==1:
					self.parent.disconnected_on_purpose = True
					self.client.quit()
					return
				else:
					tokens.pop(0)
					message = ' '.join(tokens)
					self.parent.disconnected_on_purpose = True
					self.client.quit(message)
					return

			# /whowas
			if tokens[0].lower() == "/whowas":
				if len(tokens)==2:
					target = tokens[1]
					self.client.sendLine(f"WHOWAS {target}")
					return
				else:
					d = systemTextDisplay(f"USAGE: /whowas USER<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /oper
			if tokens[0].lower() == "/oper":
				if len(tokens)==3:
					tokens.pop(0)
					username = tokens.pop(0)
					password = tokens.pop(0)
					self.client.sendLine(f"OPER {username} {password}")
					return
				else:
					d = systemTextDisplay(f"USAGE: /oper USERNAME PASSWORD<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /topic
			if tokens[0].lower() == "/topic":
				if len(tokens)>=2:
					tokens.pop(0)
					targ = tokens[0]
					# if tokens[0][0]=="#":
					if len(targ)>0 and targ[0]=="#":
						channel = tokens.pop(0)
						topic = ' '.join(tokens)
						self.client.topic(channel,topic)
						return
					else:
						if self.is_channel:
							topic = ' '.join(tokens)
							self.client.topic(self.name,topic)
							return
						else:
							d = systemTextDisplay(f"\"{self.name}\" is not a channel.",self.parent.maxnicklen,SYSTEM_COLOR)
							self.writeText(d)
							return
				else:
					d = systemTextDisplay(f"USAGE: /topic [CHANNEL] NEW_TOPIC<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /kick
			if tokens[0].lower() == "/kick":
				if len(tokens)==2:
					if self.is_channel:
						target = tokens[1]
						self.client.kick(self.name,target)
						return
					else:
						d = systemTextDisplay(f"\"{self.name}\" is not a channel.",self.parent.maxnicklen,SYSTEM_COLOR)
						self.writeText(d)
						return
				elif len(tokens)>=3:
					if self.is_channel:
						if len(tokens[1])>0 and tokens[1][0] != "#":
							tokens.pop(0)
							target = tokens.pop(0)
							reason = ' '.join(tokens)
							self.client.kick(self.name,target,reason)
							return
						else:
							tokens.pop(0)
							channel = tokens.pop(0)
							target = tokens.pop(0)
							reason = ' '.join(tokens)
							self.client.kick(channel,target,reason)
							return
					else:
						tokens.pop(0)
						channel = tokens.pop(0)
						target = tokens.pop(0)
						reason = ' '.join(tokens)
						self.client.kick(channel,target,reason)
						return
				else:
					if self.is_channel:
						d = systemTextDisplay(f"USAGE: /kick [CHANNEL] USER [REASON]<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
						self.writeText(d)
					else:
						d = systemTextDisplay(f"USAGE: /kick CHANNEL USER [REASON]<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
						self.writeText(d)
					return

			# /invite
			if tokens[0].lower() == "/invite":
				if len(tokens)==2:
					if self.is_channel:
						target = tokens[1]
						self.client.invite(target,self.name)
						return
					else:
						d = systemTextDisplay(f"\"{self.name}\" is not a channel.",self.parent.maxnicklen,SYSTEM_COLOR)
						self.writeText(d)
						return
				elif len(tokens)==3:
					target = tokens[1]
					channel = tokens[2]
					self.client.invite(target,channel)
					return
				else:
					if self.is_channel:
						d = systemTextDisplay(f"USAGE: /invite USER [CHANNEL]<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
						self.writeText(d)
					else:
						d = systemTextDisplay(f"USAGE: /invite USER CHANNEL<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
						self.writeText(d)
					return

			# /away
			if tokens[0].lower() == "/away":
				if len(tokens)==1:
					if not self.away:
						self.parent.setToAway(self.serverid)
						self.client.away()
					return
				elif len(tokens)>1:
					if not self.away:
						tokens.pop(0)
						msg = ' '.join(tokens)
						self.parent.setToAway(self.serverid,msg)
						self.client.away(msg)
						return
				else:
					d = systemTextDisplay(f"USAGE: /away [MESSAGE]<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /back
			if tokens[0].lower() == "/back":
				if len(tokens)==1:
					if self.away:
						#self.setBack()
						self.parent.setToBack(self.serverid)
						self.client.back()
					return
				else:
					d = systemTextDisplay(f"USAGE: /back<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /part
			if tokens[0].lower() == "/part":
				if len(tokens)==1:
					self.close()
					return
				if len(tokens)==2:
					tokens.pop(0)
					channel = tokens.pop(0)
					for w in self.parent.windows[self.serverid]:
						if w.window.name == channel:
							w.window.close()
							w.subwindow.close()
					return
				d = systemTextDisplay(f"USAGE: /part [CHANNEL] [KEY]<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
				self.writeText(d)
				return

			# /join
			if tokens[0].lower() == "/join":
				if len(tokens)==2:
					channel = tokens[1]
					self.client.join(channel)
					return
				elif len(tokens)==3:
					channel = tokens[1]
					key = tokens[2]
					self.client.join(channel,key)
					return
				else:
					d = systemTextDisplay(f"USAGE: /join CHANNEL [KEY]<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /me
			if tokens[0].lower() == "/me":
				if len(tokens)>=2:
					tokens.pop(0)
					msg = " ".join(tokens)
					self.client.describe(self.name,msg)
					# d = action_display(self.nickname,msg,self.parent.urlsToLinks,self.parent.display['action'],self.parent.display['background'])
					d = action_display(self.nickname,msg,self.parent.urlsToLinks,ACTION_COLOR,False,"","")
					self.parent.writeToChatWindow(self.serverid,self.name,d)
					return
				else:
					d = systemTextDisplay(f"USAGE: /me MESSAGE<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /msg
			if tokens[0].lower() == "/msg":
				if len(tokens)>=3:
					tokens.pop(0)
					target = tokens.pop(0)
					msg = ' '.join(tokens)
					self.client.msg(target,msg)
					if target[0]!="#":
						self.parent.createUserWindow(self.serverid,target)
					d = chat_display(self.nickname,msg,self.parent.maxnicklen,self.parent.urlsToLinks,SELF_COLOR)
					self.parent.writeToChatWindow(self.serverid,target,d)
					return
				else:
					d = systemTextDisplay(f"USAGE: /msg TARGET MESSAGE<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

			# /notice
			if tokens[0].lower() == "/notice":
				if len(tokens)>=3:
					tokens.pop(0)
					target = tokens.pop(0)
					msg = ' '.join(tokens)
					self.client.notice(target,msg)
					if target[0]!="#":
						self.parent.createUserWindow(self.serverid,target)
					d = notice_display(self.nickname,msg,self.parent.maxnicklen,self.parent.urlsToLinks,NOTICE_COLOR)
					self.parent.writeToChatWindow(self.serverid,target,d)
					return
				else:
					d = systemTextDisplay(f"USAGE: /notice TARGET MESSAGE<br>Enter /help for more information",self.parent.maxnicklen,SYSTEM_COLOR)
					self.writeText(d)
					return

		# COMMANDS END

		dosend = True
		if user_input.isspace(): dosend = False
		if user_input.strip() == "": dosend = False
		if user_input == "": dosend = False

		if not dosend: return

		self.client.msg(self.name,user_input)
		d = chat_display(self.nickname,user_input,self.parent.maxnicklen,self.parent.urlsToLinks,SELF_COLOR)
		self.writeText(d)

	def setTopic(self,topic):
		self.setWindowTitle(" "+f"{self.name} - {topic}")
		self.topic = topic

	def clearTopic(self):
		self.setWindowTitle(" "+self.name)

	# If users click on URLs, they will open in the default browser
	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)
		else:
			link = url.toString()

			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)

	def kickClose(self):
		self.kicked = True
		self.close()

	def closeEvent(self, event):

		cleaned = []
		for line in self.log:
			if self.newChatDivider in line[LOG_TEXT]: continue
			cleaned.append(line)
		self.log = cleaned

		if self.parent.saveLogsOnExit:
		# saveLog(self.serverid,self.name,self.log)
			if self.parent.loadLogsOnJoin:
				saveLog(self.serverhost,self.name,self.log)
			else:
				# appendLog(self.serverhost,self.name,self.log)
				oldlog = loadLog(self.serverhost,self.name)
				for line in self.log:
					if line in oldlog: continue
					oldlog.append(line)
				#oldlog.extend(self.log)

				saveLog(self.serverhost,self.name,oldlog)

		# If this is a channel window closing, part the channel
		if self.is_channel:
			if self.kicked:
				self.kicked = False
			else:
				self.client.part(self.name)

		self.toolbar.close()

		self.subwindow.close()
		self.close()

		self.parent.destroyWindow(self.serverid,self.name)

		self.parent.rebuildWindowMenu()

		if self.parent.windowcount==0:
			self.parent.setWindowTitle(DEFAULT_WINDOW_TITLE)

	def applyColors(self,text,display):

		text = text.replace(SYSTEM_COLOR,display["system"])
		text = text.replace(SELF_COLOR,display["self"])
		text = text.replace(USER_COLOR,display["user"])
		text = text.replace(ACTION_COLOR,display["action"])
		text = text.replace(NOTICE_COLOR,display["notice"])
		text = text.replace(ERROR_COLOR,display["error"])
		text = text.replace(HIGHLIGHT_COLOR,display["highlight"])
		text = text.replace(LINK_COLOR,display["link"])

		text = text.replace(NEW_CHAT_DIVIDER_TEXT_COLOR,display["new-chat-divider-text"])
		text = text.replace(NEW_CHAT_DIVIDER_BACKGROUND_COLOR,display["new-chat-divider"])

		return text

	def saveAsTextDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Chat As...",INSTALL_DIRECTORY,"Text Files (*.txt);;All Files (*)", options=options)
		if fileName:
			self.FILENAME = fileName
			if '.' in fileName:
				pass
			else:
				fileName = fileName + '.txt'
			chatlog = open(fileName,"w")
			l = convertLogToPlaintext(self.log)
			chatlog.write(l)
			chatlog.close()

	def eventFilter(self, source, event):

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.channelUserDisplay):

			item = source.itemAt(event.pos())
			if item is None: return True

			#self.channelUserDisplay.clearSelection()

			user = item.text()

			if self.parent.prettyUserlist:
				if f"@{user}" in self.users:
					user_op = True
				else:
					user_op = False

				if f"+{user}" in self.users:
					user_voiced = True
				else:
					user_voiced = False
			else:
				if '@' in user:
					user_op = True
				else:
					user_op = False
				if '+' in user:
					user_voiced = True
				else:
					user_voiced = False

				user = user.replace("@","")
				user = user.replace("+","")
				user = user.replace("%","")
				user = user.replace("~","")
			user = user.replace("&","")

			host = self.getUserHostmask(user)

			ignored = False
			for ui in self.parent.ignore:
					if ui==user: ignored = True
					if ui==host: ignored = True

			if user == self.nickname:
				menu = QMenu(self)

				if self.is_op:
					infoChan = OPERATOR_MENU_TITLE
					utitle = "<i>&nbsp;Channel operator</i>"
				elif self.is_voiced:
					infoChan = VOICED_MENU_TITLE
					utitle = "<i>&nbsp;Voiced user</i>"
				else:
					infoChan = USER_MENU_TITLE
					utitle = "<i>&nbsp;Normal user</i>"

				infoChan = infoChan.replace('!USER!',self.nickname)
				infoChan = infoChan.replace('!SPACER!',("&nbsp;"*(len("Open dialog window")-len(self.nickname))))
				userTitleLabel = QLabel(infoChan)
				userTitleLabelAction = QWidgetAction(self)
				userTitleLabelAction.setDefaultWidget(userTitleLabel)
				menu.addAction(userTitleLabelAction)

				userDescriptionLabel = QLabel(utitle)
				userDescriptionAction = QWidgetAction(self)
				userDescriptionAction.setDefaultWidget(userDescriptionLabel)
				menu.addAction(userDescriptionAction)

				menu.addSeparator()
				
				if self.is_op:
					actDeop = menu.addAction(QIcon(MINUS_ICON),'De-op self')
				if self.is_voiced:
					actDevoice = menu.addAction(QIcon(MINUS_ICON),'De-voice self')

				action = menu.exec_(self.channelUserDisplay.mapToGlobal(event.pos()))
				if self.is_op:
					if action == actDeop:
						self.client.mode(self.name,False,"o",None,self.nickname)
						return True
				if self.is_voiced:
					if action == actDevoice:
						self.client.mode(self.name,False,"v",None,self.nickname)
						return True
				return True

			menu = QMenu(self)

			if user_op:
				infoChan = OPERATOR_MENU_TITLE
				utitle = "<i>&nbsp;Channel operator</i>"
			elif user_voiced:
				infoChan = VOICED_MENU_TITLE
				utitle = "<i>&nbsp;Voiced user</i>"
			else:
				infoChan = USER_MENU_TITLE
				utitle = "<i>&nbsp;Normal user</i>"

			infoChan = infoChan.replace('!USER!',user)
			infoChan = infoChan.replace('!SPACER!',"")
			userTitleLabel = QLabel(infoChan)
			userTitleLabelAction = QWidgetAction(self)
			userTitleLabelAction.setDefaultWidget(userTitleLabel)
			menu.addAction(userTitleLabelAction)

			userDescriptionLabel = QLabel(utitle)
			userDescriptionAction = QWidgetAction(self)
			userDescriptionAction.setDefaultWidget(userDescriptionLabel)
			menu.addAction(userDescriptionAction)

			# if self.is_op: menu.addSeparator()
			menu.addSeparator()

			if not self.parent.disable_ignore:
				actIgnore = menu.addAction(QIcon(IGNORE_ICON),'Ignore user')

			if not self.parent.disable_ignore:
				actUnIgnore = menu.addAction(QIcon(UNIGNORE_ICON),'Unignore user')

			actOp = menu.addAction(QIcon(PLUS_ICON),'Give ops')
			actDeop = menu.addAction(QIcon(MINUS_ICON),'Take ops')

			actVoice = menu.addAction(QIcon(PLUS_ICON),'Give voice')
			actDevoice = menu.addAction(QIcon(MINUS_ICON),'Take voice')

			actKick = menu.addAction(QIcon(KICK_ICON),'Kick user')

			actBan = menu.addAction(QIcon(BAN_ICON),'Ban user')
			actUnban = menu.addAction(QIcon(BAN_ICON),'Unban user')

			actKickBan = menu.addAction(QIcon(KICKBAN_ICON),'Kick/Ban user')

			actWhois = menu.addAction(QIcon(WHOIS_ICON),'Whois user')

			menu.addSeparator()

			actNewWindow = menu.addAction(QIcon(NEW_WINDOW_ICON),'Open dialog window')

			if user_op:
				actOp.setVisible(False)
			else:
				actDeop.setVisible(False)

			if user_voiced:
				actVoice.setVisible(False)
			else:
				actDevoice.setVisible(False)

			banned = False
			for u in self.banlist:
				if host != "":
					u[0] = u[0].replace('*','')
					u[0] = u[0].replace('!','')
					u[0] = u[0].replace('@','')
					if host in u[0]:
						banned = True
				else:
					if u[0] == user:
						banned = True


			if not self.is_op:
				actOp.setVisible(False)
				actDeop.setVisible(False)
				actVoice.setVisible(False)
				actDevoice.setVisible(False)
				actKick.setVisible(False)
				actUnban.setVisible(False)
				actBan.setVisible(False)
				actKickBan.setVisible(False)
			else:
				if banned:
					actUnban.setVisible(True)
					actBan.setVisible(False)
					actKickBan.setVisible(False)
				else:
					actBan.setVisible(True)
					actUnban.setVisible(False)
					actKickBan.setVisible(True)

			if not self.parent.disable_ignore:
				if ignored:
					actIgnore.setVisible(False)
					actUnIgnore.setVisible(True)
				else:
					actIgnore.setVisible(True)
					actUnIgnore.setVisible(False)


			action = menu.exec_(self.channelUserDisplay.mapToGlobal(event.pos()))

			if not self.parent.disable_ignore:
				if action == actUnIgnore:
					clean = []
					for ui in self.parent.ignore:
						if ui==user: continue
						if ui==host: continue
						clean.append(ui)
					self.parent.ignore = clean
					save_ignore(self.parent.ignore)
					return True

				if action == actIgnore:
					if len(host)>0:
						self.parent.ignore.append(host)
					else:
						self.parent.ignore.append(user)
					save_ignore(self.parent.ignore)
				return True

			if action == actKickBan:
				if host != "":
					self.client.mode(self.name,True,"b",None,None,f"*!*@{host}")
				else:
					self.client.mode(self.name,True,"b",None,user)
				self.client.kick(self.name,user)
				return True

			if action == actBan:
				if host != "":
					self.client.mode(self.name,True,"b",None,None,f"*!*@{host}")
				else:
					self.client.mode(self.name,True,"b",None,user)
				return True

			if action == actUnban:
				if host != "":
					self.client.mode(self.name,False,"b",None,None,f"*!*@{host}")
				else:
					self.client.mode(self.name,False,"b",None,user)
				return True

			if action == actOp:
				self.client.mode(self.name,True,"o",None,user)
				return True

			if action == actDeop:
				self.client.mode(self.name,False,"o",None,user)
				return True

			if action == actVoice:
				self.client.mode(self.name,True,"v",None,user)
				return True

			if action == actDevoice:
				self.client.mode(self.name,False,"v",None,user)
				return True

			if action == actNewWindow:
				self.parent.createUserWindow(self.serverid,user)
				return True

			if action == actWhois:
				self.client.whois(user)
				return True

			if action == actKick:
				self.client.kick(self.name,user)
				return True

		return super(Interface, self).eventFilter(source, event)