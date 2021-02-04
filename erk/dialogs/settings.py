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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from ..resources import *
from ..files import *
from .. import config
from .. import events

from .prefix import Dialog as Prefix
from .history_size import Dialog as HistorySize
from .format import Dialog as FormatText
from .list_time import Dialog as ListTime
from .quitpart import Dialog as QuitPart

from .autosave_freq import Dialog as Autosave

from .log_size import Dialog as LogSize

class Dialog(QDialog):

	def setPrefix(self):
		x = Prefix()
		info = x.get_system_information()
		del x

		if not info: return
		self.systemPrefix = info
		self.do_rerender = True

		self.prefDisplay.setText("Prefix: <b>"+self.systemPrefix+"</b>*")

	def setHistory(self):
		x = HistorySize()
		info = x.get_entry_information()
		del x

		if not info: self.historySize = None
		self.historySize = info

		self.historyLabel.setText("Command history: <b>"+str(self.historySize)+" lines</b>*")

	def selectorClick(self,item):
		self.stack.setCurrentWidget(item.widget)

	def setRerender(self,state):
		self.do_rerender = True

	def setReset(self,state):
		self.resetHistory = True

	def selEnglish(self,selected):
		if selected: self.sclanguage = "en"

	def selFrench(self,selected):
		if selected: self.sclanguage = "fr"

	def selSpanish(self,selected):
		if selected: self.sclanguage = "es"
	def selGerman(self,selected):
		if selected: self.sclanguage = "de"

	def connectionclickLeft(self,state):
		if state == Qt.Checked:
			self.rightConnection.setChecked(False)

	def connectionclickRight(self,state):
		if state == Qt.Checked:
			self.leftConnection.setChecked(False)

	def menuFont(self):
		font, ok = QFontDialog.getFont()
		if ok:

			self.newfont = font

			f = font.toString()
			pfs = f.split(',')
			font_name = pfs[0]
			font_size = pfs[1]

			self.fontLabel.setText(f"<center><b>{font_name}, {font_size} pt</b>*</center>")

	def menuFormat(self):
		x = FormatText(self.parent)
		x.show()

	def setQuitMsg(self):
		x = QuitPart()
		info = x.get_message_information()
		del x

		if not info: return None

		self.default_quit_part = info
		self.partMsg.setText("<b>"+str(info)+"</b>*")


	def setListRefresh(self):
		x = ListTime()
		info = x.get_entry_information()
		del x

		if not info: return None
		self.configRefresh = info
		#self.refreshButton.setText("Set channel list refresh rate\n ("+str(self.configRefresh)+" seconds)")

		self.listFreq.setText("Refresh list every <b>"+str(self.configRefresh)+"</b> seconds*")


	def setSaveFreq(self):

		x = Autosave()
		f = x.get_entry_information()
		if f:
			self.autosave_time = f
			self.autoLogLabel.setText("Autosave logs every <b>"+str(self.autosave_time)+"</b> seconds*")


	def setLogSize(self):
		x = LogSize()
		info = x.get_entry_information()
		if info:
			self.logDisplayLines = info
			self.logSizeLabel.setText("Load <b>"+str(self.logDisplayLines)+"</b> lines for display*")


	def __init__(self,configfile=USER_FILE,parent=None):
		super(Dialog,self).__init__(parent)

		self.config = configfile
		self.parent = parent

		self.newfont = None

		self.logDisplayLines = config.LOG_LOAD_SIZE_MAX

		self.autosave_time = config.AUTOSAVE_LOG_TIME

		self.systemPrefix = config.SYSTEM_MESSAGE_PREFIX
		self.configRefresh = config.CHANNEL_LIST_REFRESH_FREQUENCY

		self.default_quit_part = config.DEFAULT_QUIT_PART_MESSAGE

		self.do_rerender = False

		self.setWindowTitle("Preferences")
		self.setWindowIcon(QIcon(SETTINGS_ICON))

		self.selector = QListWidget(self)
		self.stack = QStackedWidget(self)

		fm = QFontMetrics(self.font())
		fwidth = fm.width('X') * 27
		self.selector.setMaximumWidth(fwidth)

		self.selector.itemClicked.connect(self.selectorClick)

		self.selector.setStyleSheet("background-color: transparent;")

		# Display page

		self.displayPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Application")
		entry.widget = self.displayPage
		entry.setIcon(QIcon(FONT_ICON))
		self.selector.addItem(entry)
		self.selector.setCurrentItem(entry)

		self.stack.addWidget(self.displayPage)
		self.stack.setCurrentWidget(self.displayPage)

		f = self.font()
		fs = f.toString()
		pfs = fs.split(',')
		font_name = pfs[0]
		font_size = pfs[1]

		self.fontLabel = QLabel(f"<center><b>{font_name}, {font_size} pt</b></center>",self)

		fontButton = QPushButton("Change font")
		fontButton.clicked.connect(self.menuFont)
		fontButton.setAutoDefault(False)

		formatButton = QPushButton("Style Editor")
		formatButton.clicked.connect(self.menuFormat)
		formatButton.setAutoDefault(False)

		if self.parent.block_styles: formatButton.setVisible(False)

		self.nametitleMisc = QCheckBox("Show chat name in title",self)
		if config.APP_TITLE_TO_CURRENT_CHAT: self.nametitleMisc.setChecked(True)

		self.topicMisc = QCheckBox("Show channel topic in title",self)
		if config.APP_TITLE_SHOW_TOPIC: self.topicMisc.setChecked(True)

		self.askMisc = QCheckBox("Ask before quitting",self)
		if config.ASK_BEFORE_QUIT: self.askMisc.setChecked(True)

		pb2Layout = QHBoxLayout()
		pb2Layout.addStretch()
		pb2Layout.addWidget(fontButton)
		pb2Layout.addWidget(formatButton)
		pb2Layout.addStretch()

		tsLay = QVBoxLayout()
		tsLay.addWidget(self.fontLabel)
		tsLay.addLayout(pb2Layout)

		clLayout = QGroupBox("Text Settings",self)
		clLayout.setLayout(tsLay)

		clLayout.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		clLayout.setAlignment(Qt.AlignHCenter)

		self.lostErrors = QCheckBox("Show connection lost errors",self)
		if config.SHOW_CONNECTION_LOST_ERROR: self.lostErrors.setChecked(True)

		self.failErrors = QCheckBox("Show connection fail errors",self)
		if config.SHOW_CONNECTION_FAIL_ERROR: self.failErrors.setChecked(True)

		mpLayout = QVBoxLayout()

		mpLayout.addWidget(clLayout)
		mpLayout.addWidget(self.nametitleMisc)
		mpLayout.addWidget(self.topicMisc)
		mpLayout.addWidget(self.askMisc)

		mpLayout.addWidget(self.lostErrors)
		mpLayout.addWidget(self.failErrors)

		mpLayout.addStretch()

		self.displayPage.setLayout(mpLayout)

		# MENUBAR PAGE

		self.menubarPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Menu Bar")
		entry.widget = self.menubarPage
		entry.setIcon(QIcon(MENU_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.menubarPage)

		self.showSchwa = QCheckBox("Animated menu bar logo",self)
		if config.SCHWA_ANIMATION: self.showSchwa.setChecked(True)


		self.showMenu = QCheckBox("Moveable menu bar",self)
		if config.MENU_BAR_MOVABLE: self.showMenu.setChecked(True)

		self.menuMisc = QCheckBox("Use Qt menus rather than a menu bar\n(requires a restart to take effect)",self)
		if config.USE_QMENUBAR_MENUS: self.menuMisc.setChecked(True)

		self.menuMisc.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		if self.parent.force_qmenu:
			self.menuMisc.setEnabled(False)
			self.showSchwa.setEnabled(False)
			self.showMenu.setEnabled(False)

		if config.USE_QMENUBAR_MENUS:
			self.showSchwa.setEnabled(False)
			self.showMenu.setEnabled(False)

		mbLay = QVBoxLayout()
		mbLay.addWidget(self.menuMisc)
		mbLay.addWidget(self.showMenu)
		mbLay.addWidget(self.showSchwa)

		mbLay.addStretch()

		self.menubarPage.setLayout(mbLay)

		# Message settings page

		self.messagesPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Messages")
		entry.widget = self.messagesPage
		entry.setIcon(QIcon(MESSAGE_ICON))
		self.selector.addItem(entry)
		#self.selector.setCurrentItem(entry)

		self.stack.addWidget(self.messagesPage)
		#self.stack.setCurrentWidget(self.messagesPage)

		self.showDates = QCheckBox("Display dates in channel chat",self)
		if config.DISPLAY_DATES_IN_CHANNEL_CHAT: self.showDates.setChecked(True)
		self.showDates.stateChanged.connect(self.setRerender)

		self.showColors = QCheckBox("Display IRC colors",self)
		if config.DISPLAY_IRC_COLORS: self.showColors.setChecked(True)
		self.showColors.stateChanged.connect(self.setRerender)

		self.showLinks = QCheckBox("Convert URLs to links",self)
		if config.CONVERT_URLS_TO_LINKS: self.showLinks.setChecked(True)
		self.showLinks.stateChanged.connect(self.setRerender)

		self.hideProfanity = QCheckBox("Hide profanity",self)
		if config.FILTER_PROFANITY: self.hideProfanity.setChecked(True)
		self.hideProfanity.stateChanged.connect(self.setRerender)

		self.openNew = QCheckBox("Open new chat for private messages",self)
		if config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS: self.openNew.setChecked(True)

		self.channelLinks = QCheckBox("Convert channel names to links",self)
		if config.CLICKABLE_CHANNELS: self.channelLinks.setChecked(True)
		self.channelLinks.stateChanged.connect(self.setRerender)

		self.addPrefixes = QCheckBox("Add prefix to system messages",self)
		if config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL: self.addPrefixes.setChecked(True)
		self.addPrefixes.stateChanged.connect(self.setRerender)

		prefixButton = QPushButton("Set prefix")
		prefixButton.clicked.connect(self.setPrefix)
		prefixButton.setAutoDefault(False)

		# pbLayout = QHBoxLayout()
		# pbLayout.addWidget(prefixButton)
		# pbLayout.addStretch()

		self.prefDisplay = QLabel("Prefix: <b>"+config.SYSTEM_MESSAGE_PREFIX+"</b>")

		tsLay = QVBoxLayout()
		tsLay.addWidget(self.addPrefixes)
		tsLay.addWidget(self.prefDisplay)
		tsLay.addWidget(prefixButton)

		clLayout = QGroupBox("System Messages",self)
		clLayout.setLayout(tsLay)

		clLayout.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		# self.chansaveLog = QCheckBox("Save channel chat logs",self)
		# if config.SAVE_CHANNEL_LOGS: self.chansaveLog.setChecked(True)

		# self.chanloadLog = QCheckBox("Load channel chat logs",self)
		# if config.LOAD_CHANNEL_LOGS: self.chanloadLog.setChecked(True)

		# self.privsaveLog = QCheckBox("Save private chat logs",self)
		# if config.SAVE_PRIVATE_LOGS: self.privsaveLog.setChecked(True)

		# self.privloadLog = QCheckBox("Load private chat logs",self)
		# if config.LOAD_PRIVATE_LOGS: self.privloadLog.setChecked(True)

		mpLayout = QVBoxLayout()
		mpLayout.addWidget(clLayout)
		mpLayout.addWidget(self.showDates)
		mpLayout.addWidget(self.showColors)
		mpLayout.addWidget(self.showLinks)
		mpLayout.addWidget(self.hideProfanity)
		mpLayout.addWidget(self.openNew)
		mpLayout.addWidget(self.channelLinks)

		# mpLayout.addWidget(self.chansaveLog)
		# mpLayout.addWidget(self.chanloadLog)
		# mpLayout.addWidget(self.privsaveLog)
		# mpLayout.addWidget(self.privloadLog)

		mpLayout.addStretch()

		self.messagesPage.setLayout(mpLayout)

		# LOGS PAGE

		self.logsPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Logs")
		entry.widget = self.logsPage
		entry.setIcon(QIcon(LOG_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.logsPage)

		self.chansaveLog = QCheckBox("Save channel chat",self)
		if config.SAVE_CHANNEL_LOGS: self.chansaveLog.setChecked(True)

		self.chanloadLog = QCheckBox("Load channel chat",self)
		if config.LOAD_CHANNEL_LOGS: self.chanloadLog.setChecked(True)

		self.privsaveLog = QCheckBox("Save private chat",self)
		if config.SAVE_PRIVATE_LOGS: self.privsaveLog.setChecked(True)

		self.privloadLog = QCheckBox("Load private chat",self)
		if config.LOAD_PRIVATE_LOGS: self.privloadLog.setChecked(True)

		self.markLog = QCheckBox("Mark end of loaded log",self)
		if config.MARK_END_OF_LOADED_LOG: self.markLog.setChecked(True)
		self.markLog.stateChanged.connect(self.setRerender)

		

		self.resumeLog = QCheckBox("Display chat resume date and time",self)
		if config.DISPLAY_CHAT_RESUME_DATE_TIME: self.resumeLog.setChecked(True)
		self.resumeLog.stateChanged.connect(self.setRerender)

		# self.autoLog = QCheckBox("Autosave logs every "+str(config.AUTOSAVE_LOG_TIME)+" seconds",self)
		self.autoLog = QCheckBox("",self)
		self.autoLogLabel = QLabel("Autosave logs every <b>"+str(config.AUTOSAVE_LOG_TIME)+"</b> seconds")
		if config.AUTOSAVE_LOGS: self.autoLog.setChecked(True)

		self.hsButton = QPushButton("")
		self.hsButton.clicked.connect(self.setSaveFreq)
		self.hsButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.hsButton.setFixedSize(fheight +10,fheight + 10)
		self.hsButton.setIcon(QIcon(TIMESTAMP_ICON))
		self.hsButton.setToolTip("Set frequency")


		ltLayout = QHBoxLayout()
		ltLayout.addWidget(self.autoLog)
		ltLayout.addWidget(self.autoLogLabel)
		ltLayout.addWidget(self.hsButton)
		ltLayout.addStretch()


		self.logSizeLabel = QLabel("Load <b>"+str(config.LOG_LOAD_SIZE_MAX)+"</b> lines for display")

		self.slsButton = QPushButton("")
		self.slsButton.clicked.connect(self.setLogSize)
		self.slsButton.setAutoDefault(False)

		self.slsButton.setFixedSize(fheight +10,fheight + 10)
		self.slsButton.setIcon(QIcon(EDIT_ICON))
		self.slsButton.setToolTip("Set length")

		llLayout = QHBoxLayout()
		llLayout.addWidget(self.slsButton)
		llLayout.addWidget(self.logSizeLabel)
		
		llLayout.addStretch()
		


		slLayout = QVBoxLayout()
		slLayout.addWidget(self.chansaveLog)
		slLayout.addWidget(self.privsaveLog)
		slLayout.addLayout(ltLayout)

		saveLayout = QGroupBox("Save",self)
		saveLayout.setLayout(slLayout)


		saveLayout.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")


		loadLoglay = QVBoxLayout()
		loadLoglay.addWidget(self.chanloadLog)
		loadLoglay.addWidget(self.privloadLog)
		loadLoglay.addWidget(self.markLog)
		loadLoglay.addWidget(self.resumeLog)
		loadLoglay.addLayout(llLayout)

		loadLayout = QGroupBox("Load",self)
		loadLayout.setLayout(loadLoglay)


		loadLayout.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")


		mpLayout = QVBoxLayout()
		mpLayout.addWidget(saveLayout)
		mpLayout.addWidget(loadLayout)
		#mpLayout.addWidget(self.chansaveLog)
		#mpLayout.addWidget(self.chanloadLog)
		#mpLayout.addWidget(self.privsaveLog)
		#mpLayout.addWidget(self.privloadLog)
		#mpLayout.addLayout(llLayout)
		#mpLayout.addWidget(self.markLog)
		#mpLayout.addWidget(self.resumeLog)

		# mpLayout.addWidget(self.autoLog)
		# mpLayout.addWidget(self.hsButton)
		#mpLayout.addLayout(ltLayout)

		# mpLayout.addWidget(self.logSizeLabel)
		# mpLayout.addWidget(self.slsButton)
		#mpLayout.addLayout(llLayout)

		mpLayout.addStretch()

		self.logsPage.setLayout(mpLayout)

		# LOGS PAGE

		# Channel settings

		self.channelPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Chats")
		entry.widget = self.channelPage
		entry.setIcon(QIcon(CHANNEL_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.channelPage)

		self.channelInfo = QCheckBox("Show name && topic",self)
		if config.CHAT_DISPLAY_INFO_BAR: self.channelInfo.setChecked(True)

		self.channelModes = QCheckBox("Show modes",self)
		if config.DISPLAY_CHANNEL_MODES: self.channelModes.setChecked(True)

		self.textUserlist = QCheckBox("Text-only",self)
		if config.PLAIN_USER_LISTS: self.textUserlist.setChecked(True)

		self.displayUserlists = QCheckBox("Display",self)
		if config.DISPLAY_USER_LIST: self.displayUserlists.setChecked(True)

		self.displayStatus = QCheckBox("Display channel status",self)
		if config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY: self.displayStatus.setChecked(True)

		self.displayNickname = QCheckBox("Display nickname",self)
		if config.DISPLAY_NICKNAME_ON_CHANNEL: self.displayNickname.setChecked(True)

		self.displayChange = QCheckBox("Double-click nickname to change nickname",self)
		if config.DOUBLECLICK_TO_CHANGE_NICK: self.displayChange.setChecked(True)


		nnbLay = QVBoxLayout()
		nnbLay.addWidget(self.displayNickname)
		nnbLay.addWidget(self.displayStatus)
		nnbLay.addWidget(self.displayChange)

		nickBox = QGroupBox("Nickname Display",self)
		nickBox.setLayout(nnbLay)

		nickBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")


		ubLay = QHBoxLayout()
		ubLay.addStretch()
		ubLay.addWidget(self.displayUserlists)
		ubLay.addWidget(self.textUserlist)
		ubLay.addStretch()

		userBox = QGroupBox("Channel User Lists",self)
		userBox.setLayout(ubLay)

		userBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")


		cbLay = QHBoxLayout()
		cbLay.addStretch()
		cbLay.addWidget(self.channelInfo)
		cbLay.addWidget(self.channelModes)
		cbLay.addStretch()

		chanBox = QGroupBox("Channel Information",self)
		chanBox.setLayout(cbLay)

		chanBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(nickBox)
		cpLayout.addWidget(userBox)
		cpLayout.addWidget(chanBox)
		cpLayout.addStretch()

		self.channelPage.setLayout(cpLayout)

		# Connection display settings

		self.connectionPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Connection Display")
		entry.widget = self.connectionPage
		entry.setIcon(QIcon(CONNECTION_DISPLAY_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.connectionPage)

		self.enableConnection = QCheckBox("Enabled",self)
		if config.CONNECTION_DISPLAY_VISIBLE: self.enableConnection.setChecked(True)

		self.floatConnection = QCheckBox("Floatable",self)
		if config.CONNECTION_DISPLAY_MOVE: self.floatConnection.setChecked(True)

		self.uptimesConnection = QCheckBox("Display uptimes",self)
		if config.DISPLAY_CONNECTION_UPTIME: self.uptimesConnection.setChecked(True)

		self.doubleConnection = QCheckBox("Double-click to switch chats",self)
		if config.DOUBLECLICK_SWITCH: self.doubleConnection.setChecked(True)

		self.expandConnection = QCheckBox("Expand server node on connection",self)
		if config.EXPAND_SERVER_ON_CONNECT: self.expandConnection.setChecked(True)

		self.unseenConnection = QCheckBox("Animate unseen message notification",self)
		if config.UNSEEN_MESSAGE_ANIMATION: self.unseenConnection.setChecked(True)

		self.animateConnection = QCheckBox("Animate connection notification",self)
		if config.CONNECTION_MESSAGE_ANIMATION: self.animateConnection.setChecked(True)

		self.leftRadio = QRadioButton("Left")
		self.rightRadio = QRadioButton("Right")

		if config.CONNECTION_DISPLAY_LOCATION=="left": self.leftRadio.setChecked(True)
		if config.CONNECTION_DISPLAY_LOCATION=="right": self.rightRadio.setChecked(True)

		if self.parent.block_connectiondisplay:
			self.enableConnection.setEnabled(False)
			self.floatConnection.setEnabled(False)
			self.uptimesConnection.setEnabled(False)
			self.doubleConnection.setEnabled(False)
			self.expandConnection.setEnabled(False)
			self.unseenConnection.setEnabled(False)
			self.animateConnection.setEnabled(False)
			self.leftRadio.setEnabled(False)
			self.rightRadio.setEnabled(False)

		cgbLayout = QHBoxLayout()
		cgbLayout.addStretch()
		cgbLayout.addWidget(self.leftRadio)
		cgbLayout.addWidget(self.rightRadio)
		cgbLayout.addStretch()

		clLayout = QGroupBox("Default Location",self)
		clLayout.setLayout(cgbLayout)

		clLayoutH = QHBoxLayout()
		clLayoutH.addStretch()
		clLayoutH.addWidget(clLayout)
		clLayoutH.addStretch()

		clLayout.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		if self.parent.block_connectiondisplay: clLayout.setEnabled(False)

		cpLayout = QVBoxLayout()
		cpLayout.addLayout(clLayoutH)
		cpLayout.addWidget(self.enableConnection)
		cpLayout.addWidget(self.floatConnection)
		cpLayout.addWidget(self.uptimesConnection)
		cpLayout.addWidget(self.doubleConnection)
		cpLayout.addWidget(self.expandConnection)
		cpLayout.addWidget(self.unseenConnection)
		cpLayout.addWidget(self.animateConnection)

		cpLayout.addStretch()

		self.connectionPage.setLayout(cpLayout)

		# Input settings

		self.inputPage = QWidget()

		self.resetHistory = False
		self.historySize = None

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Text input")
		entry.widget = self.inputPage
		entry.setIcon(QIcon(ENTRY_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.inputPage)

		self.trackInput = QCheckBox("Track input history",self)
		if config.TRACK_COMMAND_HISTORY: self.trackInput.setChecked(True)
		self.trackInput.stateChanged.connect(self.setReset)

		hsButton = QPushButton("Set history size")
		hsButton.clicked.connect(self.setHistory)
		hsButton.setAutoDefault(False)

		self.historyLabel = QLabel("Command history: <b>"+str(config.HISTORY_LENGTH)+" lines</b>")

		histLayout = QVBoxLayout()
		histLayout.addWidget(self.trackInput)
		histLayout.addWidget(self.historyLabel)
		histLayout.addWidget(hsButton)

		histBox = QGroupBox("Input History",self)
		histBox.setLayout(histLayout)

		histBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		self.nickComplete = QCheckBox("Nicknames",self)
		if config.AUTOCOMPLETE_NICKNAMES: self.nickComplete.setChecked(True)

		self.cmdComplete = QCheckBox("Commands",self)
		if config.AUTOCOMPLETE_COMMANDS: self.cmdComplete.setChecked(True)

		self.channelComplete = QCheckBox("Channels",self)
		if config.AUTOCOMPLETE_CHANNELS: self.channelComplete.setChecked(True)

		autoLayout = QHBoxLayout()
		autoLayout.addStretch()
		autoLayout.addWidget(self.cmdComplete)
		autoLayout.addWidget(self.nickComplete)
		autoLayout.addWidget(self.channelComplete)
		autoLayout.addStretch()

		autoBox = QGroupBox("Auto-Complete",self)
		autoBox.setLayout(autoLayout)

		autoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		cpLayout = QVBoxLayout()

		cpLayout.addWidget(histBox)
		cpLayout.addWidget(autoBox)
		cpLayout.addStretch()

		self.inputPage.setLayout(cpLayout)

		# EMOJI SETTINGS
		self.emojiPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Emojis")
		entry.widget = self.emojiPage
		entry.setIcon(QIcon(EMOJI_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.emojiPage)

		self.emojiComplete = QCheckBox("Auto-complete emoji shortcodes",self)
		if config.AUTOCOMPLETE_EMOJI: self.emojiComplete.setChecked(True)

		self.emojiInput = QCheckBox("Enable emoji shortcodes",self)
		if config.USE_EMOJIS: self.emojiInput.setChecked(True)

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.emojiInput)
		cpLayout.addWidget(self.emojiComplete)
		cpLayout.addStretch()

		self.emojiPage.setLayout(cpLayout)

		# Spellcheck settings

		self.sclanguage = config.SPELLCHECK_LANGUAGE

		self.spellcheckPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Spellcheck")
		entry.widget = self.spellcheckPage
		entry.setIcon(QIcon(SPELLCHECK_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.spellcheckPage)

		self.enabledSpellcheck = QCheckBox("Enabled",self)
		if config.SPELLCHECK_INPUT: self.enabledSpellcheck.setChecked(True)

		self.nickSpellcheck = QCheckBox("Ignore nicknames",self)
		if config.SPELLCHECK_IGNORE_NICKS: self.nickSpellcheck.setChecked(True)

		self.englishSC = QRadioButton("English")
		self.englishSC.toggled.connect(self.selEnglish)

		self.frenchSC = QRadioButton("French")
		self.frenchSC.toggled.connect(self.selFrench)

		self.spanishSC = QRadioButton("Spanish")
		self.spanishSC.toggled.connect(self.selSpanish)

		self.germanSC = QRadioButton("German")
		self.germanSC.toggled.connect(self.selGerman)


		if config.SPELLCHECK_LANGUAGE=="en": self.englishSC.setChecked(True)
		if config.SPELLCHECK_LANGUAGE=="fr": self.frenchSC.setChecked(True)
		if config.SPELLCHECK_LANGUAGE=="es": self.spanishSC.setChecked(True)
		if config.SPELLCHECK_LANGUAGE=="de": self.germanSC.setChecked(True)

		langLayout = QFormLayout()
		langLayout.addRow(self.englishSC, self.frenchSC)
		langLayout.addRow(self.spanishSC, self.germanSC)

		langBox = QGroupBox("Language",self)
		langBox.setLayout(langLayout)

		langBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		lLayout = QHBoxLayout()
		lLayout.addStretch()
		lLayout.addWidget(langBox)
		lLayout.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addLayout(lLayout)
		cpLayout.addWidget(self.enabledSpellcheck)
		cpLayout.addWidget(self.nickSpellcheck)
		#cpLayout.addStretch()
		
		cpLayout.addStretch()

		self.spellcheckPage.setLayout(cpLayout)

		# Timestamp settings

		self.timestampPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Timestamps")
		entry.widget = self.timestampPage
		entry.setIcon(QIcon(TIMESTAMP_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.timestampPage)

		self.enabledTimestamp = QCheckBox("Enabled",self)
		if config.DISPLAY_TIMESTAMP: self.enabledTimestamp.setChecked(True)
		self.enabledTimestamp.stateChanged.connect(self.setRerender)

		self.twentyfourTimestamp = QCheckBox("Use 24-hour clock",self)
		if config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS: self.twentyfourTimestamp.setChecked(True)
		self.twentyfourTimestamp.stateChanged.connect(self.setRerender)

		self.secondsTimestamp = QCheckBox("Display seconds",self)
		if config.DISPLAY_TIMESTAMP_SECONDS: self.secondsTimestamp.setChecked(True)
		self.secondsTimestamp.stateChanged.connect(self.setRerender)

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.enabledTimestamp)
		cpLayout.addWidget(self.twentyfourTimestamp)
		cpLayout.addWidget(self.secondsTimestamp)
		cpLayout.addStretch()

		self.timestampPage.setLayout(cpLayout)

		# Features settings

		self.featuresPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Extensions")
		entry.widget = self.featuresPage
		entry.setIcon(QIcon(SCRIPT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.featuresPage)

		self.scriptMisc = QCheckBox("Enable scripts",self)
		if config.ENABLE_SCRIPTS: self.scriptMisc.setChecked(True)

		if self.parent.cmdline_script:
			self.scriptMisc.setEnabled(False)

		self.pluginFeatures = QCheckBox("Enable plugins",self)
		if config.PLUGINS_ENABLED: self.pluginFeatures.setChecked(True)

		if self.parent.cmdline_plugin:
			self.pluginFeatures.setEnabled(False)

		self.pluginErrors = QCheckBox("Show plugin load errors",self)
		if config.SHOW_LOAD_ERRORS: self.pluginErrors.setChecked(True)

		self.pluginDevmode = QCheckBox("Plugin development mode",self)
		if config.DEVELOPER_MODE: self.pluginDevmode.setChecked(True)

		if self.parent.cmdline_plugin:
			self.pluginErrors.setEnabled(False)
			self.pluginDevmode.setEnabled(False)

		self.sglobalMisc = QCheckBox("All aliases are global",self)
		if config.GLOBALIZE_ALL_SCRIPT_ALIASES: self.sglobalMisc.setChecked(True)

		if self.parent.cmdline_script:
			self.sglobalMisc.setEnabled(False)

		self.seditMisc = QCheckBox("Enable script editor",self)
		if config.ENABLE_SCRIPT_EDITOR: self.seditMisc.setChecked(True)

		if self.parent.cmdline_script:
			self.seditMisc.setEnabled(False)

		if self.parent.cmdline_editor:
			self.seditMisc.setEnabled(False)


		self.autoMacros = QCheckBox("Auto-complete macros",self)
		if config.AUTOCOMPLETE_MACROS: self.autoMacros.setChecked(True)

		if self.parent.cmdline_script:
			self.autoMacros.setEnabled(False)

		self.saveMacros = QCheckBox("Save macros",self)
		if config.SAVE_MACROS: self.saveMacros.setChecked(True)

		if self.parent.cmdline_script:
			self.saveMacros.setEnabled(False)

		self.enableMacros = QCheckBox("Enable macros",self)
		if config.ENABLE_MACROS: self.enableMacros.setChecked(True)

		if self.parent.cmdline_script:
			self.enableMacros.setEnabled(False)

		cgbLayout = QVBoxLayout()
		cgbLayout.addWidget(self.pluginFeatures)
		cgbLayout.addWidget(self.pluginErrors)
		cgbLayout.addWidget(self.pluginDevmode)

		plugBox = QGroupBox("Plugin Settings",self)
		plugBox.setLayout(cgbLayout)

		plugBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		if self.parent.cmdline_plugin:
			plugBox.setEnabled(False)

		scgbLayout = QVBoxLayout()
		scgbLayout.addWidget(self.scriptMisc)
		scgbLayout.addWidget(self.seditMisc)
		scgbLayout.addWidget(self.sglobalMisc)
		scgbLayout.addWidget(self.enableMacros)
		scgbLayout.addWidget(self.saveMacros)
		scgbLayout.addWidget(self.autoMacros)

		scriptBox = QGroupBox("Script Settings",self)
		scriptBox.setLayout(scgbLayout)

		scriptBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		if self.parent.cmdline_script:
			scriptBox.setEnabled(False)

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(scriptBox)
		cpLayout.addWidget(plugBox)
		cpLayout.addStretch()

		self.featuresPage.setLayout(cpLayout)

		# Miscellaneous settings

		self.initial_fetch_list = config.AUTOMATICALLY_FETCH_CHANNEL_LIST

		self.miscPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Miscellaneous")
		entry.widget = self.miscPage
		entry.setIcon(QIcon(MISC_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.miscPage)

		self.buttonsMisc = QCheckBox("Show \"Run Script\" and \"Disconnect\"\nbuttons on server displays",self)
		if config.SHOW_CONSOLE_BUTTONS: self.buttonsMisc.setChecked(True)

		self.buttonsMisc.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.switchMisc = QCheckBox("Auto-switch to new chats",self)
		if config.SWITCH_TO_NEW_WINDOWS: self.switchMisc.setChecked(True)

		self.listMisc = QCheckBox("Fetch channel list on connect",self)
		if config.AUTOMATICALLY_FETCH_CHANNEL_LIST: self.listMisc.setChecked(True)

		self.refreshButton = QPushButton("")
		self.refreshButton.clicked.connect(self.setListRefresh)
		self.refreshButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.refreshButton.setFixedSize(fheight +10,fheight + 10)
		self.refreshButton.setIcon(QIcon(EDIT_ICON))
		self.refreshButton.setToolTip("Set refresh rate")

		# self.lostErrors = QCheckBox("Show connection lost errors",self)
		# if config.SHOW_CONNECTION_LOST_ERROR: self.lostErrors.setChecked(True)

		# self.failErrors = QCheckBox("Show connection fail errors",self)
		# if config.SHOW_CONNECTION_FAIL_ERROR: self.failErrors.setChecked(True)


		self.listFreq = QLabel("Refresh list every <b>"+str(config.CHANNEL_LIST_REFRESH_FREQUENCY)+"</b> seconds")

		refRateLayout = QHBoxLayout()
		refRateLayout.addWidget(self.refreshButton)
		refRateLayout.addWidget(self.listFreq)

		refRateLayout.addStretch()

		cgbLayout = QVBoxLayout()
		cgbLayout.addWidget(self.listMisc)
		# cgbLayout.addWidget(self.listFreq)
		# cgbLayout.addWidget(self.refreshButton)
		cgbLayout.addLayout(refRateLayout)


		listBox = QGroupBox("Channel List",self)
		listBox.setLayout(cgbLayout)

		listBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")


		self.fetchMisc = QCheckBox("Fetch hostmasks on channel join",self)
		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN: self.fetchMisc.setChecked(True)
		self.fetchMisc.stateChanged.connect(self.setRerender)

		self.joinMisc = QCheckBox("Auto-join on channel invite",self)
		if config.JOIN_ON_INVITE: self.joinMisc.setChecked(True)

		self.partMsg = QLabel("<b>"+str(config.DEFAULT_QUIT_PART_MESSAGE)+"</b>")

		self.setPartMsg = QPushButton("")
		self.setPartMsg.clicked.connect(self.setQuitMsg)
		self.setPartMsg.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setPartMsg.setFixedSize(fheight +10,fheight + 10)
		self.setPartMsg.setIcon(QIcon(EDIT_ICON))
		self.setPartMsg.setToolTip("Set quit/part message")

		cgbLayout = QHBoxLayout()
		cgbLayout.addWidget(self.setPartMsg)
		cgbLayout.addWidget(self.partMsg)
		cgbLayout.addStretch()


		quitPartBox = QGroupBox("Default Quit/Part Message",self)
		quitPartBox.setLayout(cgbLayout)

		quitPartBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")


		# hsLayout = QHBoxLayout()
		# hsLayout.addWidget(self.refreshButton)
		# hsLayout.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(listBox)
		cpLayout.addWidget(quitPartBox)
		cpLayout.addWidget(self.buttonsMisc)
		# cpLayout.addWidget(self.lostErrors)
		# cpLayout.addWidget(self.failErrors)
		cpLayout.addWidget(self.switchMisc)

		cpLayout.addWidget(self.fetchMisc)
		cpLayout.addWidget(self.joinMisc)

		#cpLayout.addWidget(self.listMisc)
		#cpLayout.addLayout(hsLayout)
		

		cpLayout.addWidget(QLabel(' '))
		cpLayout.addWidget(QLabel(' '))

		cpLayout.addStretch()

		self.miscPage.setLayout(cpLayout)


		# Buttons and main layout

		saveButton = QPushButton("Save")
		saveButton.clicked.connect(self.save)
		saveButton.setAutoDefault(False)

		cancelButton = QPushButton("Cancel")
		cancelButton.clicked.connect(self.close)

		dialogButtonsLayout = QHBoxLayout()
		dialogButtonsLayout.addStretch()
		dialogButtonsLayout.addWidget(saveButton)
		dialogButtonsLayout.addWidget(cancelButton)

		mainLayout = QHBoxLayout()
		mainLayout.addWidget(self.selector)
		mainLayout.addWidget(self.stack)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(mainLayout)
		finalLayout.addLayout(dialogButtonsLayout)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())

	def save(self):

		config.LOG_LOAD_SIZE_MAX = self.logDisplayLines

		config.AUTOSAVE_LOG_TIME = self.autosave_time

		config.AUTOSAVE_LOGS = self.autoLog.isChecked()

		config.DISPLAY_CHAT_RESUME_DATE_TIME = self.resumeLog.isChecked()

		config.MARK_END_OF_LOADED_LOG = self.markLog.isChecked()

		config.SAVE_CHANNEL_LOGS = self.chansaveLog.isChecked()
		config.LOAD_CHANNEL_LOGS = self.chanloadLog.isChecked()
		config.SAVE_PRIVATE_LOGS = self.privsaveLog.isChecked()
		config.LOAD_PRIVATE_LOGS = self.privloadLog.isChecked()

		config.AUTOCOMPLETE_CHANNELS = self.channelComplete.isChecked()

		config.ENABLE_MACROS = self.enableMacros.isChecked()

		config.DEFAULT_QUIT_PART_MESSAGE = self.default_quit_part

		config.SAVE_MACROS = self.saveMacros.isChecked()

		config.AUTOCOMPLETE_MACROS = self.autoMacros.isChecked()

		config.ENABLE_SCRIPT_EDITOR = self.seditMisc.isChecked()
		if config.ENABLE_SCRIPT_EDITOR:
			self.parent.block_editor = False
		else:
			self.parent.block_editor = True

		config.USE_QMENUBAR_MENUS = self.menuMisc.isChecked()

		config.GLOBALIZE_ALL_SCRIPT_ALIASES = self.sglobalMisc.isChecked()

		config.SHOW_CONSOLE_BUTTONS = self.buttonsMisc.isChecked()
		if config.SHOW_CONSOLE_BUTTONS:
			events.show_all_console_buttons()
		else:
			events.hide_all_console_buttons()

		config.DOUBLECLICK_TO_CHANGE_NICK = self.displayChange.isChecked()

		config.ENABLE_SCRIPTS = self.scriptMisc.isChecked()
		if config.ENABLE_SCRIPTS:
			self.parent.block_scripts = False
			events.enable_all_runscript()
		else:
			self.parent.block_scripts = True
			events.disable_all_runscript()

		config.MENU_BAR_MOVABLE = self.showMenu.isChecked()

		if config.MENU_BAR_MOVABLE:
			self.parent.set_menubar_moveable(True)
		else:
			self.parent.set_menubar_moveable(False)

		config.ASK_BEFORE_QUIT = self.askMisc.isChecked()

		config.SCHWA_ANIMATION = self.showSchwa.isChecked()

		config.UNSEEN_MESSAGE_ANIMATION = self.unseenConnection.isChecked()
		config.CONNECTION_MESSAGE_ANIMATION = self.animateConnection.isChecked()

		config.DEVELOPER_MODE = self.pluginDevmode.isChecked()

		config.SHOW_CONNECTION_FAIL_ERROR = self.failErrors.isChecked()
		config.SHOW_CONNECTION_LOST_ERROR = self.lostErrors.isChecked()

		config.SHOW_LOAD_ERRORS = self.pluginErrors.isChecked()

		config.PLUGINS_ENABLED = self.pluginFeatures.isChecked()
		if config.PLUGINS_ENABLED:
			self.parent.block_plugins = False
		else:
			self.parent.block_plugins = True
		self.parent.rebuildPluginMenu()

		config.CHANNEL_LIST_REFRESH_FREQUENCY = self.configRefresh

		config.AUTOMATICALLY_FETCH_CHANNEL_LIST = self.listMisc.isChecked()

		if config.AUTOMATICALLY_FETCH_CHANNEL_LIST!=self.initial_fetch_list:
			if config.AUTOMATICALLY_FETCH_CHANNEL_LIST:
				for c in events.fetch_connections():
					if c.last_fetch < c.uptime:
						c.sendLine("LIST")

		if self.newfont!=None:
			config.DISPLAY_FONT = self.newfont.toString()
			self.parent.app.setFont(self.newfont)
			events.set_fonts_all(self.newfont)

		if self.historySize!=None: config.HISTORY_LENGTH = self.historySize

		if self.resetHistory: events.reset_history()

		config.TRACK_COMMAND_HISTORY = self.trackInput.isChecked()
		config.USE_EMOJIS = self.emojiInput.isChecked()

		config.GET_HOSTMASKS_ON_CHANNEL_JOIN = self.fetchMisc.isChecked()
		config.SWITCH_TO_NEW_WINDOWS = self.switchMisc.isChecked()
		config.JOIN_ON_INVITE = self.joinMisc.isChecked()
		config.APP_TITLE_SHOW_TOPIC = self.topicMisc.isChecked()
		config.APP_TITLE_TO_CURRENT_CHAT = self.nametitleMisc.isChecked()

		config.DISPLAY_TIMESTAMP_SECONDS = self.secondsTimestamp.isChecked()
		config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS = self.twentyfourTimestamp.isChecked()
		config.DISPLAY_TIMESTAMP = self.enabledTimestamp.isChecked()

		if self.sclanguage!=config.SPELLCHECK_LANGUAGE:
			config.SPELLCHECK_LANGUAGE = self.sclanguage
			events.newspell_all(self.sclanguage)

		config.SPELLCHECK_IGNORE_NICKS = self.nickSpellcheck.isChecked()
		config.SPELLCHECK_INPUT = self.enabledSpellcheck.isChecked()

		config.AUTOCOMPLETE_EMOJI = self.emojiComplete.isChecked()
		config.AUTOCOMPLETE_COMMANDS = self.cmdComplete.isChecked()
		config.AUTOCOMPLETE_NICKNAMES = self.nickComplete.isChecked()

		if self.leftRadio.isChecked():
			config.CONNECTION_DISPLAY_LOCATION = 'left'
		else:
			config.CONNECTION_DISPLAY_LOCATION = 'right'

		config.EXPAND_SERVER_ON_CONNECT = self.expandConnection.isChecked()
		config.DOUBLECLICK_SWITCH = self.doubleConnection.isChecked()
		config.DISPLAY_CONNECTION_UPTIME = self.uptimesConnection.isChecked()
		config.CONNECTION_DISPLAY_MOVE = self.floatConnection.isChecked()
		config.CONNECTION_DISPLAY_VISIBLE = self.enableConnection.isChecked()
		
		config.DISPLAY_DATES_IN_CHANNEL_CHAT = self.showDates.isChecked()
		config.DISPLAY_IRC_COLORS = self.showColors.isChecked()
		config.CONVERT_URLS_TO_LINKS = self.showLinks.isChecked()
		config.FILTER_PROFANITY = self.hideProfanity.isChecked()
		config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS = self.openNew.isChecked()
		config.CLICKABLE_CHANNELS = self.channelLinks.isChecked()
		config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL = self.addPrefixes.isChecked()
		config.SYSTEM_MESSAGE_PREFIX = self.systemPrefix

		config.CHAT_DISPLAY_INFO_BAR = self.channelInfo.isChecked()
		config.DISPLAY_CHANNEL_MODES = self.channelModes.isChecked()
		config.PLAIN_USER_LISTS = self.textUserlist.isChecked()
		config.DISPLAY_USER_LIST = self.displayUserlists.isChecked()
		config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY = self.displayStatus.isChecked()
		config.DISPLAY_NICKNAME_ON_CHANNEL = self.displayNickname.isChecked()

		if self.do_rerender: events.rerender_all()

		self.parent.buildMenuInterface()
		events.toggle_name_topic_display()
		events.toggle_channel_mode_display()
		events.rerender_userlists()
		events.toggle_userlist()
		events.rerender_channel_nickname()
		self.parent.refresh_application_title()
		events.resetinput_all()

		if config.CONNECTION_DISPLAY_VISIBLE:
			self.parent.connection_dock.show()
		else:
			self.parent.connection_dock.hide()

		if config.CONNECTION_DISPLAY_MOVE:
			self.parent.connection_dock.setFeatures(
					QDockWidget.DockWidgetMovable |
					QDockWidget.DockWidgetFloatable
				)
			self.parent.connection_dock.setTitleBarWidget(None)
		else:
			self.parent.connection_dock.setFloating(False)
			self.parent.connection_dock.setFeatures( QDockWidget.NoDockWidgetFeatures )
			self.parent.connection_dock.setTitleBarWidget(QWidget())
			events.resize_font_fix()

		if config.CONNECTION_DISPLAY_LOCATION=="left":
			self.parent.removeDockWidget(self.parent.connection_dock)
			self.parent.addDockWidget(Qt.LeftDockWidgetArea,self.parent.connection_dock)
			self.parent.connection_dock.show()
		else:
			self.parent.removeDockWidget(self.parent.connection_dock)
			self.parent.addDockWidget(Qt.RightDockWidgetArea,self.parent.connection_dock)
			self.parent.connection_dock.show()

		events.build_connection_display(self.parent)

		config.save_settings(self.config)

		self.close()