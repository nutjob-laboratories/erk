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

class Dialog(QDialog):

	def setPrefix(self):
		x = Prefix()
		info = x.get_system_information()
		del x

		if not info: return
		self.systemPrefix = info
		self.do_rerender = True

	def setHistory(self):
		x = HistorySize()
		info = x.get_entry_information()
		del x

		if not info: self.historySize = None
		self.historySize = info

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

			self.fontLabel.setText(f"New font: {font_name}, {font_size} pt")

	def menuFormat(self):
		x = FormatText(self.parent)
		x.show()

	def setListRefresh(self):
		x = ListTime()
		info = x.get_entry_information()
		del x

		if not info: return None
		self.configRefresh = info
		self.refreshButton.setText("Set channel list refresh rate\n ("+str(self.configRefresh)+" seconds)")

	def __init__(self,configfile=USER_FILE,parent=None):
		super(Dialog,self).__init__(parent)

		self.config = configfile
		self.parent = parent

		self.newfont = None

		self.systemPrefix = config.SYSTEM_MESSAGE_PREFIX
		self.configRefresh = config.CHANNEL_LIST_REFRESH_FREQUENCY

		self.do_rerender = False

		self.setWindowTitle("Preferences")
		self.setWindowIcon(QIcon(SETTINGS_ICON))

		self.selector = QListWidget(self)
		self.stack = QStackedWidget(self)

		fm = QFontMetrics(self.font())
		fwidth = fm.width('X') * 27
		self.selector.setMaximumWidth(fwidth)

		self.selector.itemClicked.connect(self.selectorClick)

		# Display page

		self.displayPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Display")
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

		self.fontLabel = QLabel(f"Current font: {font_name}, {font_size} pt",self)

		fontButton = QPushButton("Set font")
		fontButton.clicked.connect(self.menuFont)
		fontButton.setAutoDefault(False)

		formatButton = QPushButton("Set text colors && formatting")
		formatButton.clicked.connect(self.menuFormat)
		formatButton.setAutoDefault(False)

		self.showSchwa = QCheckBox("Netscape-esque schwa animation",self)
		if config.SCHWA_ANIMATION: self.showSchwa.setChecked(True)


		self.showMenu = QCheckBox("Moveable menu bar",self)
		if config.MENU_BAR_MOVABLE: self.showMenu.setChecked(True)

		pbLayout = QHBoxLayout()
		pbLayout.addWidget(fontButton)
		pbLayout.addStretch()

		pb2Layout = QHBoxLayout()
		pb2Layout.addWidget(formatButton)
		pb2Layout.addStretch()

		mpLayout = QVBoxLayout()
		mpLayout.addWidget(self.fontLabel)
		mpLayout.addLayout(pbLayout)
		mpLayout.addLayout(pb2Layout)
		mpLayout.addWidget(self.showSchwa)
		mpLayout.addWidget(self.showMenu)
		mpLayout.addStretch()

		self.displayPage.setLayout(mpLayout)

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

		pbLayout = QHBoxLayout()
		pbLayout.addWidget(prefixButton)
		pbLayout.addStretch()

		mpLayout = QVBoxLayout()
		mpLayout.addWidget(self.showDates)
		mpLayout.addWidget(self.showColors)
		mpLayout.addWidget(self.showLinks)
		mpLayout.addWidget(self.hideProfanity)
		mpLayout.addWidget(self.openNew)
		mpLayout.addWidget(self.channelLinks)
		mpLayout.addWidget(self.addPrefixes)
		mpLayout.addLayout(pbLayout)
		mpLayout.addStretch()

		self.messagesPage.setLayout(mpLayout)

		# Channel settings

		self.channelPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Channels")
		entry.widget = self.channelPage
		entry.setIcon(QIcon(CHANNEL_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.channelPage)

		self.channelInfo = QCheckBox("Display channel info bar",self)
		if config.CHAT_DISPLAY_INFO_BAR: self.channelInfo.setChecked(True)

		self.channelModes = QCheckBox("Display channel modes",self)
		if config.DISPLAY_CHANNEL_MODES: self.channelModes.setChecked(True)

		self.textUserlist = QCheckBox("Text-only user lists",self)
		if config.PLAIN_USER_LISTS: self.textUserlist.setChecked(True)

		self.displayUserlists = QCheckBox("Display user lists",self)
		if config.DISPLAY_USER_LIST: self.displayUserlists.setChecked(True)

		self.displayStatus = QCheckBox("Display status",self)
		if config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY: self.displayStatus.setChecked(True)

		self.displayNickname = QCheckBox("Display nickname",self)
		if config.DISPLAY_NICKNAME_ON_CHANNEL: self.displayNickname.setChecked(True)

		self.displayChange = QCheckBox("Double-click nickname to change nickname",self)
		if config.DOUBLECLICK_TO_CHANGE_NICK: self.displayChange.setChecked(True)

		self.fetchMisc = QCheckBox("Fetch hostmasks on channel join",self)
		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN: self.fetchMisc.setChecked(True)
		self.fetchMisc.stateChanged.connect(self.setRerender)

		self.joinMisc = QCheckBox("Auto-join on channel invite",self)
		if config.JOIN_ON_INVITE: self.joinMisc.setChecked(True)

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.channelInfo)
		cpLayout.addWidget(self.channelModes)
		cpLayout.addWidget(self.textUserlist)
		cpLayout.addWidget(self.displayUserlists)
		cpLayout.addWidget(self.displayStatus)
		cpLayout.addWidget(self.displayNickname)
		cpLayout.addWidget(self.displayChange)
		cpLayout.addWidget(self.fetchMisc)
		cpLayout.addWidget(self.joinMisc)
		cpLayout.addStretch()

		self.channelPage.setLayout(cpLayout)

		# Connection display settings

		self.connectionPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Connections")
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

		cgbLayout = QHBoxLayout()
		cgbLayout.addStretch()
		cgbLayout.addWidget(self.leftRadio)
		cgbLayout.addWidget(self.rightRadio)
		cgbLayout.addStretch()

		clLayout = QGroupBox("Connection display location",self)
		clLayout.setLayout(cgbLayout)

		efLayout = QHBoxLayout()
		efLayout.addStretch()
		efLayout.addWidget(self.enableConnection)
		efLayout.addStretch()
		efLayout.addWidget(self.floatConnection)
		efLayout.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addLayout(efLayout)
		cpLayout.addWidget(clLayout)
		cpLayout.addWidget(self.uptimesConnection)
		cpLayout.addWidget(self.doubleConnection)
		cpLayout.addWidget(self.expandConnection)
		cpLayout.addWidget(self.unseenConnection)
		cpLayout.addWidget(self.animateConnection)

		cpLayout.addStretch()

		self.connectionPage.setLayout(cpLayout)

		# Autocomplete settings

		self.autocompletePage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Autocomplete")
		entry.widget = self.autocompletePage
		entry.setIcon(QIcon(AUTOCOMPLETE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.autocompletePage)

		self.nickComplete = QCheckBox("Autocomplete nicknames",self)
		if config.AUTOCOMPLETE_NICKNAMES: self.nickComplete.setChecked(True)

		self.cmdComplete = QCheckBox("Autocomplete commands",self)
		if config.AUTOCOMPLETE_COMMANDS: self.cmdComplete.setChecked(True)

		self.emojiComplete = QCheckBox("Autocomplete emoji shortcodes",self)
		if config.AUTOCOMPLETE_EMOJI: self.emojiComplete.setChecked(True)

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.nickComplete)
		cpLayout.addWidget(self.cmdComplete)
		cpLayout.addWidget(self.emojiComplete)
		cpLayout.addStretch()

		self.autocompletePage.setLayout(cpLayout)

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

		langBox = QGroupBox("Spellcheck Language",self)
		langBox.setLayout(langLayout)

		lLayout = QHBoxLayout()
		lLayout.addStretch()
		lLayout.addWidget(langBox)
		lLayout.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.enabledSpellcheck)
		cpLayout.addWidget(self.nickSpellcheck)
		#cpLayout.addStretch()
		cpLayout.addLayout(lLayout)
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

		self.emojiInput = QCheckBox("Enable emoji shortcodes",self)
		if config.USE_EMOJIS: self.emojiInput.setChecked(True)

		self.trackInput = QCheckBox("Track input history",self)
		if config.TRACK_COMMAND_HISTORY: self.trackInput.setChecked(True)
		self.trackInput.stateChanged.connect(self.setReset)

		hsButton = QPushButton("Set input history size")
		hsButton.clicked.connect(self.setHistory)
		hsButton.setAutoDefault(False)

		hsLayout = QHBoxLayout()
		hsLayout.addWidget(hsButton)
		hsLayout.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.emojiInput)
		cpLayout.addWidget(self.trackInput)
		cpLayout.addLayout(hsLayout)
		cpLayout.addStretch()

		self.inputPage.setLayout(cpLayout)

		# Features settings

		self.featuresPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Plugins & Macros")
		entry.widget = self.featuresPage
		entry.setIcon(QIcon(MACRO_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.featuresPage)

		self.macroFeatures = QCheckBox("Enable macros",self)
		if config.MACROS_ENABLED: self.macroFeatures.setChecked(True)

		if self.parent.cmdline_macro:
			self.macroFeatures.setEnabled(False)
			self.macroFeatures.setText("Enable macros (disabled)")

		self.pluginFeatures = QCheckBox("Enable plugins",self)
		if config.PLUGINS_ENABLED: self.pluginFeatures.setChecked(True)

		if self.parent.cmdline_plugin:
			self.pluginFeatures.setEnabled(False)
			self.pluginFeatures.setText("Enable plugins (disabled)")

		self.pluginErrors = QCheckBox("Show plugin load errors",self)
		if config.SHOW_LOAD_ERRORS: self.pluginErrors.setChecked(True)

		self.pluginDevmode = QCheckBox("Plugin development mode",self)
		if config.DEVELOPER_MODE: self.pluginDevmode.setChecked(True)

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.macroFeatures)
		cpLayout.addWidget(self.pluginFeatures)
		cpLayout.addWidget(self.pluginErrors)
		cpLayout.addWidget(self.pluginDevmode)
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

		self.scriptMisc = QCheckBox("Enable scripts",self)
		if config.ENABLE_SCRIPTS: self.scriptMisc.setChecked(True)

		if self.parent.cmdline_script:
			self.scriptMisc.setEnabled(False)
			self.scriptMisc.setText("Enable scripts (disabled)")

		self.askMisc = QCheckBox("Ask before quitting",self)
		if config.ASK_BEFORE_QUIT: self.askMisc.setChecked(True)

		self.nametitleMisc = QCheckBox("Show chat name in title",self)
		if config.APP_TITLE_TO_CURRENT_CHAT: self.nametitleMisc.setChecked(True)

		self.topicMisc = QCheckBox("Show channel topic in title",self)
		if config.APP_TITLE_SHOW_TOPIC: self.topicMisc.setChecked(True)

		self.switchMisc = QCheckBox("Auto-switch to new chats",self)
		if config.SWITCH_TO_NEW_WINDOWS: self.switchMisc.setChecked(True)

		self.listMisc = QCheckBox("Fetch channel list on connect",self)
		if config.AUTOMATICALLY_FETCH_CHANNEL_LIST: self.listMisc.setChecked(True)

		self.refreshButton = QPushButton("Set channel list refresh rate\n ("+str(config.CHANNEL_LIST_REFRESH_FREQUENCY)+" seconds)")
		self.refreshButton.clicked.connect(self.setListRefresh)
		self.refreshButton.setAutoDefault(False)

		self.lostErrors = QCheckBox("Show connection lost errors",self)
		if config.SHOW_CONNECTION_LOST_ERROR: self.lostErrors.setChecked(True)

		self.failErrors = QCheckBox("Show connection fail errors",self)
		if config.SHOW_CONNECTION_FAIL_ERROR: self.failErrors.setChecked(True)

		hsLayout = QHBoxLayout()
		hsLayout.addWidget(self.refreshButton)
		hsLayout.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.scriptMisc)
		cpLayout.addWidget(self.askMisc)
		cpLayout.addWidget(self.lostErrors)
		cpLayout.addWidget(self.failErrors)
		cpLayout.addWidget(self.nametitleMisc)
		cpLayout.addWidget(self.topicMisc)
		#cpLayout.addWidget(self.joinMisc)
		cpLayout.addWidget(self.switchMisc)

		#cpLayout.addWidget(self.showSchwa)

		cpLayout.addWidget(self.listMisc)
		cpLayout.addLayout(hsLayout)

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

		config.MACROS_ENABLED = self.macroFeatures.isChecked()
		if config.MACROS_ENABLED:
			self.parent.block_macros = False
		else:
			self.parent.block_macros = True
		self.parent.rebuildMacroMenu()

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