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

from collections import defaultdict
from datetime import datetime
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

SSL_IS_AVAILABLE = True

try:
	from twisted.internet import ssl
except ImportError as error:
	# Output expected ImportErrors.
	print(error.__class__.__name__ + ": " + error.message)
	SSL_IS_AVAILABLE = False
except Exception as exception:
	# Output unexpected Exceptions.
	print(exception, False)
	print(exception.__class__.__name__ + ": " + exception.message)
	SSL_IS_AVAILABLE = False

from erk.irc import connect,connectSSL,reconnect,reconnectSSL
from erk.uptime import UptimeHeartbeat

import erk.gui.window as Window

import erk.gui.dialogs.connect as ConnectDialog
import erk.gui.dialogs.networks as NetworkDialog
import erk.gui.dialogs.join as JoinDialog
import erk.gui.dialogs.nick as NickDialog
import erk.gui.dialogs.user as UserDialog
import erk.gui.dialogs.ignore as IgnoreDialog
import erk.gui.dialogs.colors as ColorDialog

import erk.gui.dialogs.about as AboutDialog

import erk.gui.dialogs.channellist as ChannelListDialog


from erk.common import *

class ErkGUI(QMainWindow):

	"""The GUI class for the main client.
	"""

	def changeEvent(self,event):

		if event.type() == QEvent.WindowStateChange:
			if event.oldState() and Qt.WindowMinimized:
				# window has been minimized
				pass
			elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
				# window is not minimized
				pass

	def __init__(self,app,config=None,display=None,parent=None):
		super(ErkGUI, self).__init__(parent)

		self.app = app
		self.parent = parent


		if config!=None:
			self.settingsFile = config
		else:
			self.settingsFile = SETTINGS_FILE

		if display!=None:
			self.displayFile = display
		else:
			self.displayFile = DISPLAY_CONFIGURATION

		self.disconnected_on_purpose = False

		self.commandlineJoinChannel = None
		self.commandlineJoinChannelKey = None

		# Setting defaults
		self.nickname = DEFAULT_NICKNAME
		self.username = DEFAULT_USERNAME
		self.realname = DEFAULT_IRCNAME
		self.alternate = DEFAULT_ALTERNATIVE

		self.heartbeatInterval = 120

		self.can_use_ssl = SSL_IS_AVAILABLE

		# Define attributes for later use

		self.connections = {}				# Where IRC server connections are stored
		self.windows = defaultdict(list)	# Where windows are stored
		self.toolbars = {}					# Stores server toolbars
		self.timers = {}					# Stores server timers
		self.plaintext = {}             	# Plain chat (non-html) storage
		self.windowcount = 0

		# Load in settings from files

		self.display = loadDisplay(self.displayFile)

		f = QFont()
		f.fromString(self.display["font"])
		self.font = f

		f = QFont()
		f.fromString(self.display["font"])
		self.fontBold = f
		self.fontBold.setBold(True)

		f = QFont()
		f.fromString(self.display["font"])
		self.fontitalic = f
		self.fontitalic.setItalic(True)

		f = QFont()
		f.fromString(self.display["font"])
		self.fontUsers = f
		self.fontUsers.setBold(True)
		self.fontUsers.setPointSize(self.fontUsers.pointSize()+ADDITIONAL_POINT_SIZE_FOR_USER_DISPLAY)

		app.setFont(self.font)

		self.ERK_ICON = QIcon(TRAY_ICON)
		self.FLASH_ICON = QIcon(FLASH_ICON)
		self.FLASH_STATE = 0
		self.IS_FLASHING = False

		self.FORCE_PROFANITY_FILTER = False
		self.FORCE_NOCOLORS = False

		self.displayTimestamp = True
		self.displayUptime = True
		self.keepAlive = True
		self.openWindowOnIncomingPrivate = True
		self.joinInvite = False
		self.initialWindowWidth = 500
		self.initialWindowHeight = 350
		self.prettyUserlist = True
		self.urlsToLinks = True
		self.titleActiveWindow = True
		self.logChatByNetwork = False
		self.displayConnectionLog = True
		self.channelListEnabled = False
		self.saveLogsOnExit = True
		self.spellCheck = True
		self.spellCheckLanguage = "en"
		self.autocompleteCommands = True
		self.autocompleteNicks = True
		self.highlightNickMessages = True
		self.enableStatusBar = True
		self.theme = USE_NO_THEME_SETTING
		self.themeIcons = True
		self.profanityFilter = False
		self.topicInTitle = True
		self.stripIRCcolor = False
		self.showTray = True
		self.flashTray = True
		self.menuTray = True
		self.emojis = False
		self.asciimojis = True
		self.loadLogsOnJoin = True
		self.maxlogsize = MAX_LOG_SIZE_DEFAULT
		self.windowToolbars = True

		self.saveServers = True

		self.settings = loadSettings(self.settingsFile)

		self.displayTimestamp = self.settings[TIMESTAMP_SETTING]
		self.displayUptime = self.settings[UPTIME_SETTING]
		self.keepAlive = self.settings[KEEPALIVE_SETTING]
		self.joinInvite = self.settings[INVITE_SETTING]
		self.openWindowOnIncomingPrivate = self.settings[PRIVATEWINDOW_SETTING]
		self.initialWindowWidth = self.settings[INITIALWIDTH_SETTING]
		self.initialWindowHeight = self.settings[INITIALHEIGHT_SETTING]
		self.prettyUserlist = self.settings[PRETTYUSER_SETTING]
		self.urlsToLinks = self.settings[DOLINKS_SETTING]
		self.titleActiveWindow = self.settings[TITLE_ACTIVE_WINDOW_SETTING]
		self.logChatByNetwork = self.settings[SAVE_LOGS_BY_NETWORK]
		self.channelListEnabled = self.settings[ENABLE_LIST_SETTING]
		self.saveLogsOnExit = self.settings[AUTO_SAVE_CHAT_LOGS]
		self.spellCheck = self.settings[ENABLE_SPELL_CHECK]
		self.spellCheckLanguage = self.settings[SPELL_CHECK_LANGUAGE]
		self.autocompleteCommands = self.settings[AUTOCOMPLETE_COMMANDS]
		self.autocompleteNicks = self.settings[AUTOCOMPLETE_ENTITIES]
		self.highlightNickMessages = self.settings[HIGHLIGHT_NICK_MESSAGE]
		self.enableStatusBar = self.settings[STATUS_BAR_SETTING]
		self.theme = self.settings[THEME_SETTING]
		self.themeIcons = self.settings[LOAD_THEME_ICONS_SETTING]
		self.profanityFilter = self.settings[PROFANITY_FILTER_SETTING]
		self.topicInTitle = self.settings[TOPIC_TITLE_SETTING]
		self.stripIRCcolor = self.settings[STRIP_IRC_COLORS_SETTING]
		self.showTray = self.settings[SYSTEM_TRAY_SETTING]
		self.flashTray = self.settings[SYSTEM_TRAY_FLASH_SETTING]
		self.loadLogsOnJoin = self.settings[LOAD_LOG_SETTING]
		self.maxlogsize = self.settings[LOAD_LOG_SIZE]
		self.menuTray = self.settings[SYSTEM_TRAY_MENU]
		self.emojis = self.settings[EMOJI_SETTING]
		self.asciimojis = self.settings[ASCIIEMOJI_SETTING]
		self.windowToolbars = self.settings[CHAT_TOOLBAR_SETTING]

		self.saveServers = self.settings[SAVE_SERVER_SETTING]

		self.maxnicklen = MAX_DEFAULT_NICKNAME_SIZE

		self.dockIsLoaded = False

		self.editorEnabled = True
		self.windowsEnabled = True
		self.themesEnabled = True

		self.themeList = getThemeList()

		# Load in icon resource file from theme, if possible
		# If not, load in the default resource file
		if self.themeIcons:
			importThemeResources(self.theme)
		else:
			importThemeResources(USE_NO_THEME_SETTING)

		self.ignore = get_ignore()

		# Start the uptime counter
		self.uptime = 0
		self.uptimeTimer = UptimeHeartbeat(self)
		self.uptimeTimer.beat.connect(self.heartbeat)
		self.uptimeTimer.start()

		self.connected = False

		self.editor_windows = []

		self.channel_list_windows = []

		self.cLog = []

		# Build the UI
		self.buildUI()

	def destroyTrayMenu(self):
		traymenu = QMenu()
		self.tray.setContextMenu(traymenu)

	def buildTrayMenu(self):
		traymenu = QMenu()

		trayLabel = QLabel(f"{APPLICATION_NAME} {APPLICATION_VERSION}")
		f = trayLabel.font()
		f.setBold(True)
		trayLabel.setFont(f)
		trayLabel.setAlignment(Qt.AlignCenter)
		trayLabelAction = QWidgetAction(self)
		trayLabelAction.setDefaultWidget(trayLabel)
		traymenu.addAction(trayLabelAction)	
		traymenu.addSeparator()

		traymenu.addAction(self.actConnect)
		traymenu.addAction(self.actNetwork)
		traymenu.addAction(self.actDisconnect)

		traymenu.addSeparator()

		self.stwinmenu = QMenu("Window")
		self.stwinmenu.setIcon(QIcon(RESTORE_ICON))

		trayMin = QAction(QIcon(MINIMIZE_ICON),f"Minimize",self)
		trayMin.triggered.connect(self.showMinimized)
		self.stwinmenu.addAction(trayMin)

		trayMin = QAction(QIcon(MAXIMIZE_ICON),f"Maximize",self)
		trayMin.triggered.connect(self.showMaximized)
		self.stwinmenu.addAction(trayMin)

		trayMin = QAction(QIcon(RESTORE_ICON),f"Normal",self)
		trayMin.triggered.connect(self.showNormal)
		self.stwinmenu.addAction(trayMin)

		traymenu.addMenu(self.stwinmenu)

		traymenu.addSeparator()

		traymenu.addAction(self.actExit)

		self.tray.setContextMenu(traymenu)

	def saveConnectionLog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save log As...",INSTALL_DIRECTORY,"Text Files (*.txt);;All Files (*)", options=options)
		if fileName:
			self.FILENAME = fileName
			if '.' in fileName:
				pass
			else:
				fileName = fileName + '.txt'
			chatlog = open(fileName,"w")
			l = convertLogToPlaintext(self.cLog)
			chatlog.write(l)
			chatlog.close()

	def saveConfigFile(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save log As...",INSTALL_DIRECTORY,"JSON Files (*.json);;All Files (*)", options=options)
		if fileName:
			self.FILENAME = fileName
			if '.' in fileName:
				pass
			else:
				fileName = fileName + '.json'
			saveSettings(self.settings,fileName)

	def buildUI(self):
		"""Builds the GUI for Erk.
		"""

		self.setWindowTitle(DEFAULT_WINDOW_TITLE)
		self.setWindowIcon(QIcon(ERK_ICON))

		# Create the MDI widget
		self.MDI = QMdiArea()
		self.setCentralWidget(self.MDI)

		# Track active window
		self.MDI.subWindowActivated.connect(self.updateActiveChild)

		pix = QPixmap(MDI_BACKGROUND)
		backgroundBrush = QBrush(pix)
		self.MDI.setBackground(backgroundBrush)

		# Create system tray icon
		self.tray = QSystemTrayIcon(self)
		self.tray.setIcon(self.ERK_ICON)
		
		# Create master log
		self.log = self.buildDockLog()
		self.addDockWidget(Qt.BottomDockWidgetArea,self.log)

		# Add background image to log.
		#css = "QTextEdit { background-image: url(:/logbg.png); background-attachment: fixed; background-repeat: no-repeat; background-position: right; }"
		
		css =  "QTextEdit { background-image: url(" + ERK_LOG_WATERMARK + "); background-attachment: fixed; background-repeat: no-repeat; background-position: right; }"

		self.logTxt.setStyleSheet(css)

		# Hide log if that's what the settings say
		if not self.displayConnectionLog:
			self.log.hide()

		# Creates the master menu
		menubar = self.menuBar()
		menubar.setContextMenuPolicy(Qt.PreventContextMenu)

		ircMenu = menubar.addMenu("IRC")

		self.actConnect = QAction(QIcon(SERVER_ICON),"Connect to Server",self)
		self.actConnect.triggered.connect(self.doConnectDialog)
		ircMenu.addAction(self.actConnect)
		

		self.actNetwork = QAction(QIcon(NETWORK_ICON),"Connect to Network",self)
		self.actNetwork.triggered.connect(self.doNetworkDialog)
		ircMenu.addAction(self.actNetwork)
		

		self.actDisconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		self.actDisconnect.triggered.connect(self.selectDisconnect)
		ircMenu.addAction(self.actDisconnect)
		self.actDisconnect.setEnabled(False)

		ircMenu.addSeparator()
		

		self.actExit = QAction(QIcon(EXIT_ICON),"Exit",self)
		self.actExit.triggered.connect(self.close)
		ircMenu.addAction(self.actExit)

		# self.viewMenu.addSeparator()

		self.optMenu = menubar.addMenu("Settings")

		self.actUser = QAction(QIcon(USER_ICON),"Edit default user information",self)
		self.actUser.triggered.connect(self.doUserDialog)
		self.optMenu.addAction(self.actUser)

		self.actIgnore = QAction(QIcon(IGNORE_ICON),"Edit ignored user list",self)
		self.actIgnore.triggered.connect(self.doIgnoreDialog)
		self.optMenu.addAction(self.actIgnore)

		self.saveLog = QAction(QIcon(SAVE_ICON),"Save connection log to file",self)
		self.saveLog.triggered.connect(self.saveConnectionLog)
		self.optMenu.addAction(self.saveLog)

		self.saveConfig = QAction(QIcon(JSON_ICON),"Export configuration",self)
		self.saveConfig.triggered.connect(self.saveConfigFile)
		self.optMenu.addAction(self.saveConfig)

		self.optMenu.addSeparator()

		self.faceMenu = self.optMenu.addMenu(QIcon(INTERFACE_ICON),"Interface")

		self.faceTrayMenu = self.faceMenu.addMenu(QIcon(SETTINGS_ICON),"System Tray")

		self.optSystray = QAction("Show icon in system tray",self,checkable=True)
		self.optSystray.setChecked(self.showTray)
		self.optSystray.triggered.connect(self.toggleTray)
		self.faceTrayMenu.addAction(self.optSystray)

		self.optFlash = QAction("Flash icon on message receipt",self,checkable=True)
		self.optFlash.setChecked(self.flashTray)
		self.optFlash.triggered.connect(self.toggleFlash)
		self.faceTrayMenu.addAction(self.optFlash)

		self.optTrayMenu = QAction("Right-click icon for menu",self,checkable=True)
		self.optTrayMenu.setChecked(self.menuTray)
		self.optTrayMenu.triggered.connect(self.toggleTrayMenu)
		self.faceTrayMenu.addAction(self.optTrayMenu)

		if not self.showTray: self.optFlash.setEnabled(False)
		if not self.showTray: self.optTrayMenu.setEnabled(False)

		self.widgetMenu = self.faceMenu.addMenu(QIcon(ERK_ICON),"Features")

		optStatus = QAction("Display status bar",self,checkable=True)
		optStatus.setChecked(self.enableStatusBar)
		optStatus.triggered.connect(self.toggleStatus)
		self.widgetMenu.addAction(optStatus)

		optUptime = QAction("Display connection uptime",self,checkable=True)
		optUptime.setChecked(self.displayUptime)
		optUptime.triggered.connect(self.toggleUptime)
		self.widgetMenu.addAction(optUptime)

		optPretty = QAction("HexChat style user lists",self,checkable=True)
		optPretty.setChecked(self.prettyUserlist)
		optPretty.triggered.connect(self.togglePrettyUsers)
		self.widgetMenu.addAction(optPretty)

		optEnableList = QAction("Enable channel listing",self,checkable=True)
		optEnableList.setChecked(self.channelListEnabled)
		optEnableList.triggered.connect(self.toggleListEnable)
		self.widgetMenu.addAction(optEnableList)

		self.winsetMenu = self.faceMenu.addMenu(QIcon(WINDOW_ICON),"Windows")

		topWinTool = QAction("Chat window toolbars",self,checkable=True)
		topWinTool.setChecked(self.windowToolbars)
		topWinTool.triggered.connect(self.toggleWinToolbars)
		self.winsetMenu.addAction(topWinTool)

		optTitle = QAction("Application title set to active user/channel title",self,checkable=True)
		optTitle.setChecked(self.titleActiveWindow)
		optTitle.triggered.connect(self.toggleTitle)
		self.winsetMenu.addAction(optTitle)

		self.winTopic = QAction("Display topic in channel window title",self,checkable=True)
		self.winTopic.setChecked(self.topicInTitle)
		self.winTopic.triggered.connect(self.toggleTopic)
		self.winsetMenu.addAction(self.winTopic)
		
		self.chatSettings = self.optMenu.addMenu(QIcon(CHANNEL_WINDOW_ICON),"IRC")

		optSaveServ = QAction("Save connected servers",self,checkable=True)
		optSaveServ.setChecked(self.saveServers)
		optSaveServ.triggered.connect(self.toggleSaveServ)
		self.chatSettings.addAction(optSaveServ)

		optAlive = QAction("Keep connection alive",self,checkable=True)
		optAlive.setChecked(self.keepAlive)
		optAlive.triggered.connect(self.toggleAlive)
		self.chatSettings.addAction(optAlive)

		optInvite = QAction("Automatic join on channel invite",self,checkable=True)
		optInvite.setChecked(self.joinInvite)
		optInvite.triggered.connect(self.toggleInvite)
		self.chatSettings.addAction(optInvite)

		self.msgMenu = self.optMenu.addMenu(QIcon(PUBLIC_ICON),"Messages")

		self.optStrip = QAction("Strip IRC colors",self,checkable=True)
		self.optStrip.setChecked(self.stripIRCcolor)
		self.optStrip.triggered.connect(self.toggleStrip)
		self.msgMenu.addAction(self.optStrip)

		self.optFilter = QAction("Censor profanity",self,checkable=True)
		self.optFilter.setChecked(self.profanityFilter)
		self.optFilter.triggered.connect(self.toggleFilter)
		self.msgMenu.addAction(self.optFilter)

		optLinks = QAction("Convert URLs to hyperlinks",self,checkable=True)
		optLinks.setChecked(self.urlsToLinks)
		optLinks.triggered.connect(self.toggleLinks)
		self.msgMenu.addAction(optLinks)

		optUptime = QAction("Display timestamps",self,checkable=True)
		optUptime.setChecked(self.displayTimestamp)
		optUptime.triggered.connect(self.toggleTimestamp)
		self.msgMenu.addAction(optUptime)

		optHightlightNick = QAction("Highlight messages containing your nickname",self,checkable=True)
		optHightlightNick.setChecked(self.highlightNickMessages)
		optHightlightNick.triggered.connect(self.toggleNickHighlight)
		self.msgMenu.addAction(optHightlightNick)

		optPrivate = QAction("Open windows for incoming private messages",self,checkable=True)
		optPrivate.setChecked(self.openWindowOnIncomingPrivate)
		optPrivate.triggered.connect(self.togglePrivateWindow)
		self.msgMenu.addAction(optPrivate)

		self.emojiSettings = self.optMenu.addMenu(QIcon(EMOJI_ICON),"Emojis")

		self.optEmoji = QAction("Use emoji colon codes",self,checkable=True)
		self.optEmoji.setChecked(self.emojis)
		self.optEmoji.triggered.connect(self.toggleEmoji)
		self.emojiSettings.addAction(self.optEmoji)

		# https://www.webfx.com/tools/emoji-cheat-sheet/
		helpLink = QAction(QIcon(LINK_ICON),"Emoji colon code list",self)
		helpLink.triggered.connect(lambda state,u="https://www.webfx.com/tools/emoji-cheat-sheet/": self.doOpenUrl(u))
		f = helpLink.font()
		f.setItalic(True)
		helpLink.setFont(f)
		self.emojiSettings.addAction(helpLink)

		self.emojiSettings.addSeparator()

		self.optAsciiMoji = QAction("Use ASCIImoji parentheses codes",self,checkable=True)
		self.optAsciiMoji.setChecked(self.asciimojis)
		self.optAsciiMoji.triggered.connect(self.toggleAsciiEmoji)
		self.emojiSettings.addAction(self.optAsciiMoji)

		helpLink = QAction(QIcon(LINK_ICON),"ASCIImoji parentheses code list",self)
		helpLink.triggered.connect(lambda state,u="http://asciimoji.com/": self.doOpenUrl(u))
		f = helpLink.font()
		f.setItalic(True)
		helpLink.setFont(f)
		self.emojiSettings.addAction(helpLink)

		self.spellMenu = self.optMenu.addMenu(QIcon(SPELL_ICON),"Spell check")

		self.optSpellCheck = QAction("Enabled",self,checkable=True)
		self.optSpellCheck.setChecked(self.spellCheck)
		self.optSpellCheck.triggered.connect(self.toggleSpellCheck)
		self.spellMenu.addAction(self.optSpellCheck)

		self.spellMenu.addSeparator()

		self.scEnglish = QAction("English",self,checkable=True)
		self.scEnglish.setChecked(False)
		self.scEnglish.triggered.connect(lambda state,l="en": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scEnglish)

		self.scFrench = QAction("French",self,checkable=True)
		self.scFrench.setChecked(False)
		self.scFrench.triggered.connect(lambda state,l="fr": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scFrench)

		self.scSpanish = QAction("Spanish",self,checkable=True)
		self.scSpanish.setChecked(False)
		self.scSpanish.triggered.connect(lambda state,l="es": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scSpanish)

		self.scGerman = QAction("German",self,checkable=True)
		self.scGerman.setChecked(False)
		self.scGerman.triggered.connect(lambda state,l="de": self.setSpellCheckLanguage(l) )
		self.spellMenu.addAction(self.scGerman)

		if self.spellCheckLanguage=="en": self.scEnglish.setChecked(True)
		if self.spellCheckLanguage=="fr": self.scFrench.setChecked(True)
		if self.spellCheckLanguage=="es": self.scSpanish.setChecked(True)
		if self.spellCheckLanguage=="de": self.scGerman.setChecked(True)

		self.autocompMenu = self.optMenu.addMenu(QIcon(AUTOCOMPLETE_ICON),"Auto-complete")

		optEnableAutoCommand = QAction("Auto-complete commands",self,checkable=True)
		optEnableAutoCommand.setChecked(self.autocompleteCommands)
		optEnableAutoCommand.triggered.connect(self.toggleAutoCommands)
		self.autocompMenu.addAction(optEnableAutoCommand)

		optEnableAutoNick = QAction("Auto-complete users/channels",self,checkable=True)
		optEnableAutoNick.setChecked(self.autocompleteNicks)
		optEnableAutoNick.triggered.connect(self.toggleAutoNick)
		self.autocompMenu.addAction(optEnableAutoNick)

		#self.optMenu.addSeparator()

		self.miscMenu = self.optMenu.addMenu(QIcon(LOG_ICON),"Logs")

		optNetworkChat = QAction("Save chat logs by network name",self,checkable=True)
		optNetworkChat.setChecked(self.logChatByNetwork)
		optNetworkChat.triggered.connect(self.toggleNetworkChat)
		self.miscMenu.addAction(optNetworkChat)

		self.optSaveChat = QAction("Save chat logs on window close",self,checkable=True)
		self.optSaveChat.setChecked(self.saveLogsOnExit)
		self.optSaveChat.triggered.connect(self.toggleSaveLogs)
		self.miscMenu.addAction(self.optSaveChat)

		optLoadChat = QAction("Automatically display saved logs in client",self,checkable=True)
		optLoadChat.setChecked(self.loadLogsOnJoin)
		optLoadChat.triggered.connect(self.toggleLoadChat)
		self.miscMenu.addAction(optLoadChat)

		self.logsizeMenu = self.miscMenu.addMenu(QIcon(LOG_ICON),"Log display size")

		self.sizeAll = QAction("All lines",self,checkable=True)
		self.sizeAll.triggered.connect(lambda state,l=0: self.setLoadLogSize(l) )
		self.logsizeMenu.addAction(self.sizeAll)

		self.logsizeMenu.addSeparator()

		self.sizeOne = QAction("100 lines",self,checkable=True)
		self.sizeOne.triggered.connect(lambda state,l=100: self.setLoadLogSize(l) )
		self.logsizeMenu.addAction(self.sizeOne)

		self.sizeTwo = QAction("200 lines",self,checkable=True)
		self.sizeTwo.triggered.connect(lambda state,l=200: self.setLoadLogSize(l) )
		self.logsizeMenu.addAction(self.sizeTwo)

		self.sizeThree = QAction("300 lines",self,checkable=True)
		self.sizeThree.triggered.connect(lambda state,l=300: self.setLoadLogSize(l) )
		self.logsizeMenu.addAction(self.sizeThree)

		self.sizeFour = QAction("400 lines",self,checkable=True)
		self.sizeFour.triggered.connect(lambda state,l=400: self.setLoadLogSize(l) )
		self.logsizeMenu.addAction(self.sizeFour)

		self.sizeFive = QAction("500 lines",self,checkable=True)
		self.sizeFive.triggered.connect(lambda state,l=500: self.setLoadLogSize(l) )
		self.logsizeMenu.addAction(self.sizeFive)

		if self.maxlogsize==0:
			self.sizeAll.setChecked(True)
		elif self.maxlogsize==100:
			self.sizeOne.setChecked(True)
		elif self.maxlogsize==200:
			self.sizeTwo.setChecked(True)
		elif self.maxlogsize==300:
			self.sizeThree.setChecked(True)
		elif self.maxlogsize==400:
			self.sizeFour.setChecked(True)
		elif self.maxlogsize==500:
			self.sizeFive.setChecked(True)

		# "Install" system tray menu
		if self.menuTray: self.buildTrayMenu()
		if self.showTray: self.tray.show()

		self.viewMenu = menubar.addMenu("Display")

		self.optShowLog = QAction(QIcon(NOCONSOLE_ICON),"Hide connection log",self)
		self.optShowLog.setChecked(self.displayConnectionLog)
		self.optShowLog.triggered.connect(self.toggleShowLog)
		self.viewMenu.addAction(self.optShowLog)

		self.viewMenu.addSeparator()

		self.optFont = QAction(QIcon(FONT_ICON),"Font",self)
		self.optFont.triggered.connect(self.getFont)
		self.viewMenu.addAction(self.optFont)

		pf = self.display["font"].split(',')
		mf = pf[0]
		ms = pf[1]
		self.optFont.setText(f"Font ({mf}, {ms}pt)")

		self.actColors = QAction(QIcon(COLOR_ICON),"Colors",self)
		self.actColors.triggered.connect(self.doColorDialog)
		self.viewMenu.addAction(self.actColors)

		self.themeMenu = self.viewMenu.addMenu(QIcon(THEME_ICON),"Theme")
		self.buildThemeMenu()


		self.windowMenu = menubar.addMenu("Windows")

		self.rebuildWindowMenu()

		self.helpMenu = menubar.addMenu("Help")

		helpLink = QAction(QIcon(ABOUT_ICON),f"About {APPLICATION_NAME}",self)
		helpLink.triggered.connect(self.doAbout)
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(ERK_ICON),f"{APPLICATION_NAME} source code repository",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/nutjob-laboratories/erk": self.doOpenUrl(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(THEME_ICON),f"{APPLICATION_NAME} theme compiler repository",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/nutjob-laboratories/erk-theme": self.doOpenUrl(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(OPEN_SOURCE_ICON),"GNU Public License 3",self)
		helpLink.triggered.connect(lambda state,u="https://www.gnu.org/licenses/gpl-3.0.en.html": self.doOpenUrl(u))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		self.rfcMenu = self.helpMenu.addMenu(QIcon(FILE_ICON),"IRC Protocol Documentation")

		helpLink = QAction(QIcon(LINK_ICON),"RFC 1459",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc1459": self.doOpenUrl(u))
		self.rfcMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"RFC 2812",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc2812": self.doOpenUrl(u))
		self.rfcMenu.addAction(helpLink)
	
		self.softwareMenu = self.helpMenu.addMenu(QIcon(GEARS_ICON),"Technology")

		helpLink = QAction(QIcon(PYICON_ICON),"Python",self)
		helpLink.triggered.connect(lambda state,u="https://www.python.org/": self.doOpenUrl(u))
		self.softwareMenu.addAction(helpLink)

		helpLink = QAction(QIcon(QTICON_ICON),"Qt",self)
		helpLink.triggered.connect(lambda state,u="https://www.qt.io/": self.doOpenUrl(u))
		self.softwareMenu.addAction(helpLink)

		helpLink = QAction(QIcon(PYQT_ICON),"PyQt5",self)
		helpLink.triggered.connect(lambda state,u="https://www.riverbankcomputing.com/software/pyqt/intro": self.doOpenUrl(u))
		self.softwareMenu.addAction(helpLink)

		helpLink = QAction(QIcon(TWISTED_IMAGE),"Twisted",self)
		helpLink.triggered.connect(lambda state,u="https://twistedmatrix.com/trac/": self.doOpenUrl(u))
		self.softwareMenu.addAction(helpLink)

		helpLink = QAction(QIcon(ICONS8_IMAGE),"Icons8",self)
		helpLink.triggered.connect(lambda state,u="https://icons8.com/": self.doOpenUrl(u))
		self.softwareMenu.addAction(helpLink)

		helpLink = QAction(QIcon(PYICON_ICON),"pyspellchecker",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/barrust/pyspellchecker": self.doOpenUrl(u))
		self.softwareMenu.addAction(helpLink)


# 		buttonSettings = QPushButton("")
# 		buttonSettings.setIcon(QIcon(ABOUT_ICON))

# 		buttonSettings.clicked.connect(self.doAbout)

# 		pbcss = """QPushButton {
# 	border: 0px;
# }
# QPushButton::menu-indicator {
# 	width: 0px;
# }
# """
# 		buttonSettings.setStyleSheet(pbcss)

# 		menubar.setCornerWidget(buttonSettings)

		# STATUS BAR
		self.status = self.statusBar()

		self.status.setStyleSheet('QStatusBar::item {border: None;}')

		self.CONNECTED_ICON = QIcon(CONNECTED_ICON).pixmap(16,16)
		self.DISCONNECTED_ICON = QIcon(DISCONNECT_ICON).pixmap(16,16)

		self.status_icon = QLabel()
		self.status_icon.setPixmap(self.DISCONNECTED_ICON)
		self.status_text = QLabel("<i>Disconnected</i>")
		self.status_text.setAlignment(Qt.AlignRight)

		self.status.addPermanentWidget(self.status_icon,0)
		self.status.addPermanentWidget(self.status_text,1)

		if not self.enableStatusBar:
			self.status.hide()

		# Load in theme
		if self.theme.lower() != "none":
			theme = getThemeQSS(self.theme)
			if theme != None:
				self.setStyleSheet(theme)
			themeArray = getThemeJSON(self.theme)
			if len(themeArray)==2:
				self.display = themeArray[0]
				self.displayFile = themeArray[1]

				self.setNewFont(self.display['font'])

		img = QImage(ERK_LOG_BANNER)
		cursor = QTextCursor(self.logTxt.document())
		cursor.insertImage(img)
		if len(self.display['banner-text'])>0:
			self.writeToLog(self.display['banner-text'])
		else:
			self.writeToLog(f"<i>&nbsp;&nbsp;\"It's how you pronounce IRC\"</i>")
			pass


	def updateStatusBar(self):
		servers = 0
		for c in self.connections:
			servers = servers + 1

		if servers>0:
			self.status_icon.setPixmap(self.CONNECTED_ICON)
			if servers==1:
				# one server connection
				display = "<i>Connected</i>"
			else:
				# more than one
				display = "<i>Connected to " + str(servers) +" servers</i>"
		else:
			self.status_icon.setPixmap(self.DISCONNECTED_ICON)
			display = "<i>Disconnected</i>"
			self.setWindowTitle(DEFAULT_WINDOW_TITLE)

		self.status_text.setText(display)

	def doOpenUrl(self,url):
		u = QUrl()
		u.setUrl(url)
		QDesktopServices.openUrl(u)

	# ===================================
	# Helper and Window Related Functions
	# ===================================

	def getChannelList(self,serverid):
		chanlist = []
		for w in self.connections:
			if w != serverid: continue
			for x in self.windows[w]:
				if x.window.is_channel:
					chanlist.append(x.window.name)
		return chanlist

	def getFullUserList(self):
		u = []
		for w in self.connections:
			for x in self.windows[w]:
				if x.window.is_channel:
					for n in x.window.getUserNicks():
						u.append(n)
		return u

	def forceNoIRCColors(self):
		self.FORCE_NOCOLORS = True
		self.optStrip.setChecked(True)
		self.optStrip.setEnabled(False)


	def forceProfanityFilter(self):
		self.FORCE_PROFANITY_FILTER = True
		self.optFilter.setChecked(True)
		self.optFilter.setEnabled(False)

	def disableSystray(self):
		self.showTray = False
		self.tray.hide()
		self.optSystray.setEnabled(False)
		self.optFlash.setEnabled(False)
		self.optTrayMenu.setEnabled(False)

	def disableThemes(self):
		self.themesEnabled = False
		self.buildThemeMenu()

	def disableWindowsMenu(self):
		self.windowsEnabled = False
		self.rebuildWindowMenu()

	def hideSettingsMenu(self):
		self.optMenu.clear()

		noSettingsLabel = QLabel("<i>&nbsp;&nbsp;Settings cannot be edited&nbsp;&nbsp;</i>")
		noSettingsAction = QWidgetAction(self)
		noSettingsAction.setDefaultWidget(noSettingsLabel)
		self.optMenu.addAction(noSettingsAction)

	def turnOffLogging(self):
		self.saveLogsOnExit = False
		self.optSaveChat.setChecked(False)
		self.optSaveChat.setEnabled(False)

	def updateActiveChild(self,subWindow):
		if not self.titleActiveWindow: return
		try:
			w = subWindow.windowTitle()
			# Ignore the about window
			if w==f" Version {APPLICATION_VERSION}":
				return
			self.setWindowTitle(w)
			for c in self.connections:
				for x in self.windows[c]:
					if x.subwindow.windowTitle()==w:
						x.window.active = True
						x.window.toolNameNormal()
					else:
						x.window.active = False
		except:
			self.setWindowTitle(DEFAULT_WINDOW_TITLE)

	def connectToIRC(self,connection_info,sreconnect=False):

		#sreconnect = self.doReconnect

		nick = connection_info[0]
		username = connection_info[1]
		realname = connection_info[2]
		alternate = connection_info[3]
		host = connection_info[4]
		port = connection_info[5]
		password = connection_info[6]
		use_ssl = connection_info[7]

		if len(connection_info)>8:
			recon = connection_info[8]

			if recon==1:
				sreconnect = True
			else:
				sreconnect = False

		if use_ssl==1:
			use_ssl = True
		else:
			use_ssl = False

		# Sanity check
		errs = []
		if len(nick)==0: errs.append("nickname not entered")
		if len(alternate)==0: errs.append("alternate not entered")
		if len(username)==0: errs.append("username not entered")
		if len(realname)==0: errs.append("real name not entered")
		if len(host)==0: errs.append("host not entered")
		if len(port)==0: errs.append("port not entered")
		if not is_integer(port): errs.append(f"invalid port \"{port}\"")
		if len(errs)>0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(ERK_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Missing or Invalid Input")
			es = ""
			for e in errs: es = es + f"<li>{e}</li>"
			msg.setInformativeText(f"<ul>{es}</ul>")
			msg.setWindowTitle("Can't connect to IRC")
			msg.exec_()
			return

		port = int(port)

		# Save server information
		if use_ssl:
			save_last_server( host, port, password, True )
		else:
			save_last_server( host, port, password, False )

		# Save user information
		user = {
			"nick": str(nick),
			"username": str(username),
			"realname": str(realname),
			"alternate": str(alternate)
		}
		save_user(user)

		self.nickname = nick
		self.username = username
		self.realname = realname
		self.alternate = alternate

		#sid = f"{host}:{str(port)}"

		if not use_ssl:
			if sreconnect:
				reconnect(host,port,nick,username,realname,self,password)
			else:
				connect(host,port,nick,username,realname,self,password)
		else:
			if sreconnect:
				reconnectSSL(host,port,nick,username,realname,self,password)
			else:
				connectSSL(host,port,nick,username,realname,self,password)

	def heartbeat(self):
		self.uptime = self.uptime + 1

		if not self.connected:
			self.setWindowTitle(DEFAULT_WINDOW_TITLE)

		y = 0
		for w in self.connections:
			for x in self.windows[w]: y = y + 1

		if y!=self.windowcount: self.rebuildWindowMenu()

		# Stop flashing tray icon if the window is no longer minimized
		if self.showTray:
			if self.flashTray:
				if not self.isMinimized():
					if self.IS_FLASHING:
						self.IS_FLASHING = False
						self.FLASH_STATE = 0
						self.tray.setIcon(self.ERK_ICON)
			else:
				if self.tray.icon() != self.ERK_ICON:
					self.tray.setIcon(self.ERK_ICON)


		# Flash tray icon
		if self.showTray:
			if self.flashTray:
				if self.IS_FLASHING:
					if self.FLASH_STATE==0:
						self.tray.setIcon(self.ERK_ICON)
						self.FLASH_STATE = 1
					else:
						self.tray.setIcon(self.FLASH_ICON)
						self.FLASH_STATE = 0
				else:
					if self.FLASH_STATE==1:
						self.FLASH_STATE = 0
						self.tray.setIcon(self.ERK_ICON)

	def servBeat(self,serverid):

		if not self.toolbars[serverid]: return

		if not self.displayUptime: return

		self.toolbars[serverid].stimecount = self.toolbars[serverid].stimecount + 1

		t = convertSeconds(self.toolbars[serverid].stimecount)
		hours = t[0]
		if len(str(hours))==1: hours = f"0{hours}"
		minutes = t[1]
		if len(str(minutes))==1: minutes = f"0{minutes}"
		seconds = t[2]
		if len(str(seconds))==1: seconds = f"0{seconds}"
		display = f"{hours}:{minutes}:{seconds}"

		self.toolbars[serverid].stimer.setText(display)

	def applyColors(self,text,display):

		text = text.replace(SYSTEM_COLOR,display["system"])
		text = text.replace(SELF_COLOR,display["self"])
		text = text.replace(USER_COLOR,display["user"])
		text = text.replace(ACTION_COLOR,display["action"])
		text = text.replace(NOTICE_COLOR,display["notice"])
		text = text.replace(ERROR_COLOR,display["error"])
		text = text.replace(HIGHLIGHT_COLOR,display["highlight"])
		text = text.replace(LINK_COLOR,display["link"])

		return text

	def closeEvent(self, event):

		# Close all windows
		for w in self.windows:
			for i in self.windows[w]:
				i.subwindow.close()
				i.window.close()

		self.uptimeTimer.stop()

		self.app.quit()

	def printToActiveWindow(self,txt):
		activeSubWindow = self.MDI.activeSubWindow()
		if activeSubWindow:
			x = activeSubWindow.widget()
			x.writeText(txt)

	def writeToChatWindow(self,serverid,target,text):
		for w in self.windows[serverid]:
			if w.window.name == target:
				w.window.writeText(text)

	def notifyChatWindow(self,serverid,target):
		for w in self.windows[serverid]:
			if w.window.name == target:
				if not w.window.active: w.window.toolNameRed()

	def writeToAll(self,serverid,text):
		for w in self.windows[serverid]:
			w.window.writeText(text)

	def writeToAllExisting(self,text):
		for c in self.connections:
			for w in self.windows[c]:
				w.window.writeText(text)

	def writeToLog(self,text):
		text = self.applyColors(text,self.display)

		# Add timestamp
		t = datetime.timestamp(datetime.now())
		pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')
		pretty = "&nbsp;" + pretty + "&nbsp;"
		tt = TIMESTAMP_TEMPLATE.replace("!TIME!",pretty)

		self.cLog.append([t,text])

		text = text.replace("!TIMESTAMP!",tt)

		#text = tt + text

		self.logTxt.append(text)
		self.logTxt.moveCursor(QTextCursor.End)

	def serverMessage(self,serverid,channel,message):
		for w in self.windows[serverid]:
				if w.window.name == channel:
					d = systemTextDisplay(message,self.maxnicklen,SYSTEM_COLOR)
					self.writeToChatWindow(serverid,channel,d)

	def serverAllMessage(self,serverid,message):
		for w in self.windows[serverid]:
			d = systemTextDisplay(message,self.maxnicklen,SYSTEM_COLOR)
			self.writeToChatWindow(serverid,w.window.name,d)
			self.writeToLog(d)

	def setToAway(self,serverid,msg=None):
		for w in self.windows[serverid]:
			w.window.setAway(msg)
		self.toolbars[serverid].awaylabel.setText("<i>(away)</i>")
		if msg != None:
			self.toolbars[serverid].awaylabel.setToolTip(msg)

	def setToBack(self,serverid):
		for w in self.windows[serverid]:
			w.window.setBack()
		self.toolbars[serverid].awaylabel.setText("")
		self.toolbars[serverid].awaylabel.setToolTip("")

	def destroyWindow(self,serverid,name):
		cleaned = []
		for w in self.windows[serverid]:
			if w.window.name == name: continue
			cleaned.append(w)
		self.windows[serverid] = cleaned

		self.updateActiveChild(self.MDI.activeSubWindow())

	# If users click on URLs, they will open in the default browser
	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.logTxt.setSource(QUrl())
			self.logTxt.moveCursor(QTextCursor.End)
		else:
			link = url.toString()
			d = decodeWindowLink(link)
			user = d[1]
			sid = d[0]

			self.createUserWindow(sid,user)

			self.logTxt.setSource(QUrl())
			self.logTxt.moveCursor(QTextCursor.End)

	def createUserWindow(self,serverid,user):
		for w in self.windows[serverid]:
			if w.window.name == user:
				return
		userWindow = Window.createNew(user,self.connections[serverid],serverid,self.MDI,self)
		self.windows[serverid].append(userWindow)
		userWindow.window.show()

	def createChannelListWindow(self,serverid):
		sw = QMdiSubWindow()
		w = ChannelListDialog.Dialog(self)

		sw.setWidget(w)
		w.subwindow = sw

		w.setWindowTitle(f"Channels on "+ self.connections[serverid].host+":"+str(self.connections[serverid].port))
		w.serverid = serverid

		self.MDI.addSubWindow(sw)
		sw.show()

		e = [sw,w,serverid]
		self.channel_list_windows.append(e)

	# ==============
	# Menu Functions
	# ==============

	def setLoadLogSize(self,s):
		self.maxlogsize = s
		self.settings[LOAD_LOG_SIZE] = self.maxlogsize
		saveSettings(self.settings,self.settingsFile)

		self.sizeAll.setChecked(False)
		self.sizeOne.setChecked(False)
		self.sizeTwo.setChecked(False)
		self.sizeThree.setChecked(False)
		self.sizeFour.setChecked(False)
		self.sizeFive.setChecked(False)

		if s == 0:
			self.sizeAll.setChecked(True)
		elif s == 100:
			self.sizeOne.setChecked(True)
		elif s == 200:
			self.sizeTwo.setChecked(True)
		elif s == 300:
			self.sizeThree.setChecked(True)
		elif s == 400:
			self.sizeFour.setChecked(True)
		elif s == 500:
			self.sizeFive.setChecked(True)

	def manualHideDock(self,visible):
		if visible:
			self.displayConnectionLog = True
			self.optShowLog.setText("Hide connection log")
			self.optShowLog.setIcon(QIcon(NOCONSOLE_ICON))
		else:
			self.displayConnectionLog = False
			self.optShowLog.setText("Show connection log")
			self.optShowLog.setIcon(QIcon(CONSOLE_ICON))
		#self.optShowLog.setChecked(self.displayConnectionLog)
		if not self.dockIsLoaded:
			self.dockIsLoaded = True
			# self.settings[DISPLAY_LOG_SETTING] = self.displayConnectionLog
			# saveSettings(self.settings,self.settingsFile)

	def toggleIcons(self):
		if self.themeIcons:
			self.themeIcons = False
		else:
			self.themeIcons = True
		self.settings[LOAD_THEME_ICONS_SETTING] = self.themeIcons
		saveSettings(self.settings,self.settingsFile)


	def toggleShowLog(self):
		if self.displayConnectionLog:
			self.displayConnectionLog = False
			self.log.hide()
			self.optShowLog.setText("Show connection log")
			self.optShowLog.setIcon(QIcon(CONSOLE_ICON))
		else:
			self.displayConnectionLog = True
			self.log.show()
			self.optShowLog.setText("Hide connection log")
			self.optShowLog.setIcon(QIcon(NOCONSOLE_ICON))
		# self.settings[DISPLAY_LOG_SETTING] = self.displayConnectionLog
		# saveSettings(self.settings,self.settingsFile)

	def togglePrettyUsers(self):
		if self.prettyUserlist:
			self.prettyUserlist = False
		else:
			self.prettyUserlist = True

		for c in self.connections:
			for w in self.windows[c]:
				if w.window.is_channel:
					w.window.redrawUserlist()
		self.settings[PRETTYUSER_SETTING] = self.prettyUserlist
		saveSettings(self.settings,self.settingsFile)

	def togglePrivateWindow(self):
		if self.openWindowOnIncomingPrivate:
			self.openWindowOnIncomingPrivate = False
		else:
			self.openWindowOnIncomingPrivate = True

		self.settings[PRIVATEWINDOW_SETTING] = self.openWindowOnIncomingPrivate
		saveSettings(self.settings,self.settingsFile)

	def getFont(self):
		font, ok = QFontDialog.getFont()
		if ok:

			self.setNewFont(font.toString())

			pf = self.display["font"].split(',')
			mf = pf[0]
			ms = pf[1]
			self.optFont.setText(f"Font ({mf}, {ms}pt)")

	def toggleSaveServ(self):
		if self.saveServers:
			self.saveServers = False
		else:
			self.saveServers = True

		self.settings[SAVE_SERVER_SETTING] = self.saveServers
		saveSettings(self.settings,self.settingsFile)

	def toggleInvite(self):

		if self.joinInvite:
			self.joinInvite = False
		else:
			self.joinInvite = True

		self.settings[INVITE_SETTING] = self.joinInvite
		saveSettings(self.settings,self.settingsFile)

	def toggleStrip(self):

		if self.stripIRCcolor:
			self.stripIRCcolor = False
		else:
			self.stripIRCcolor = True

		self.settings[STRIP_IRC_COLORS_SETTING] = self.stripIRCcolor
		saveSettings(self.settings,self.settingsFile)

	def toggleTopic(self):
		if self.topicInTitle:
			self.topicInTitle = False
			self.removeTitleTopic()
		else:
			self.topicInTitle = True
			self.restoreTitleTopic()

		self.settings[TOPIC_TITLE_SETTING] = self.topicInTitle
		saveSettings(self.settings,self.settingsFile)

	def toggleEmoji(self):
		if self.emojis:
			self.emojis = False
		else:
			self.emojis = True

		self.settings[EMOJI_SETTING] = self.emojis
		saveSettings(self.settings,self.settingsFile)

	def toggleAsciiEmoji(self):
		if self.asciimojis:
			self.asciimojis = False
		else:
			self.asciimojis = True

		self.settings[ASCIIEMOJI_SETTING] = self.asciimojis
		saveSettings(self.settings,self.settingsFile)


	def toggleFilter(self):
		if self.profanityFilter:
			self.profanityFilter = False
		else:
			self.profanityFilter = True

		self.settings[PROFANITY_FILTER_SETTING] = self.profanityFilter
		saveSettings(self.settings,self.settingsFile)

	def toggleAlive(self):
		if self.keepAlive:
			self.keepAlive = False
			for s in self.connections:
				if not self.connections[s].alive: continue
				self.connections[s].alive = False
				self.connections[s].stopHeartbeat()
		else:
			self.keepAlive = True
			for s in self.connections:
				if self.connections[s].alive: continue
				self.connections[s].alive = True
				self.connections[s].startHeartbeat()

		self.settings[KEEPALIVE_SETTING] = self.keepAlive
		saveSettings(self.settings,self.settingsFile)

	# def toggleReconnect(self):
	# 	if self.doReconnect:
	# 		self.doReconnect = False
	# 	else:
	# 		self.doReconnect = True

	# 	self.settings[RECONNECT_SETTING] = self.doReconnect
	# 	saveSettings(self.settings,self.settingsFile)

	def toggleUptime(self):
		if self.displayUptime:
			self.displayUptime = False
			for s in self.toolbars:
				self.toolbars[s].stimer.setText('')
		else:
			self.displayUptime = True
			for s in self.toolbars:
				self.toolbars[s].stimer.setText('00:00:00')

		self.settings[UPTIME_SETTING] = self.displayUptime
		saveSettings(self.settings,self.settingsFile)

	def toggleTimestamp(self):
		if self.displayTimestamp:
			self.displayTimestamp = False
			for s in self.connections:
				for w in self.windows[s]:
					w.window.displayTimestamp = False
					w.window.rerenderTextDisplay()
		else:
			self.displayTimestamp = True
			for s in self.connections:
				for w in self.windows[s]:
					w.window.displayTimestamp = True
					w.window.rerenderTextDisplay()

		self.settings[TIMESTAMP_SETTING] = self.displayTimestamp
		saveSettings(self.settings,self.settingsFile)

	def rebuildWindowMenu(self):

		if not self.windowsEnabled:
			self.windowMenu.clear()

			winDisabledLabel = QLabel("<i>&nbsp;&nbsp;Window selection has been disabled&nbsp;&nbsp;</i>")
			winDisabledAction = QWidgetAction(self)
			winDisabledAction.setDefaultWidget(winDisabledLabel)
			self.windowMenu.addAction(winDisabledAction)

			return

		self.windowMenu.clear()

		actCascade = QAction(QIcon(CASCADE_ICON),"Cascade Windows",self)
		actCascade.triggered.connect(lambda state: self.MDI.cascadeSubWindows())
		self.windowMenu.addAction(actCascade)

		actTile = QAction(QIcon(TILE_ICON),"Tile Windows",self)
		actTile.triggered.connect(lambda state: self.MDI.tileSubWindows())
		self.windowMenu.addAction(actTile)

		self.windowMenu.addSeparator()

		self.windowcount = 0
		
		for w in self.connections:
			serverhost = self.connections[w].hostname
			servMenu = self.windowMenu.addMenu(QIcon(SERVER_ICON),f"{serverhost}")
			chatcount = 0
			for x in self.windows[w]:
				chatcount = chatcount + 1
				if x.window.is_channel:
					win = QAction(QIcon(CHANNEL_WINDOW_ICON),x.window.name,self)
					self.windowcount = self.windowcount + 1
				else:
					win = QAction(QIcon(USER_WINDOW_ICON),x.window.name,self)
					self.windowcount = self.windowcount + 1
				win.triggered.connect(lambda state,f=x.window,y=x.subwindow: self.restoreChatWindow(f,y))
				servMenu.addAction(win)
			# Display if no chat windows are open
			if chatcount==0:
				win = QAction("No windows found.",self)
				f = win.font()
				f.setItalic(True)
				win.setFont(f)
				servMenu.addAction(win)

	def restoreChatWindow(self,win,subwin):
		# Unminimize window if the window is minimized
		win.setWindowState(win.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
		win.activateWindow()
		win.showNormal()

		# Bring the window to the front
		self.MDI.setActiveSubWindow(subwin)

	def setSpellCheckLanguage(self,lang):
		self.spellCheckLanguage = lang

		self.settings[SPELL_CHECK_LANGUAGE] = self.spellCheckLanguage
		saveSettings(self.settings,self.settingsFile)

		for w in self.connections:
			for x in self.windows[w]:
				x.window.userTextInput.changeLanguage(lang)

		if lang=="en":
			self.scEnglish.setChecked(True)
			self.scFrench.setChecked(False)
			self.scSpanish.setChecked(False)
			self.scGerman.setChecked(False)
			#self.scPortuguese.setChecked(False)
			return

		if lang=="fr":
			self.scEnglish.setChecked(False)
			self.scFrench.setChecked(True)
			self.scSpanish.setChecked(False)
			self.scGerman.setChecked(False)
			#self.scPortuguese.setChecked(False)
			return

		if lang=="es":
			self.scEnglish.setChecked(False)
			self.scFrench.setChecked(False)
			self.scSpanish.setChecked(True)
			self.scGerman.setChecked(False)
			#self.scPortuguese.setChecked(False)
			return

		if lang=="de":
			self.scEnglish.setChecked(False)
			self.scFrench.setChecked(False)
			self.scSpanish.setChecked(False)
			self.scGerman.setChecked(True)
			#self.scPortuguese.setChecked(False)
			return

		# if lang=="pt":
		# 	self.scEnglish.setChecked(False)
		# 	self.scFrench.setChecked(False)
		# 	self.scSpanish.setChecked(False)
		# 	self.scGerman.setChecked(False)
		# 	self.scPortuguese.setChecked(True)
		# 	return

	def toggleStatus(self):
		if self.enableStatusBar:
			self.enableStatusBar = False
			self.status.hide()
		else:
			self.enableStatusBar = True
			self.status.show()
		self.settings[STATUS_BAR_SETTING] = self.enableStatusBar
		saveSettings(self.settings,self.settingsFile)

	def toggleNickHighlight(self):
		if self.highlightNickMessages:
			self.highlightNickMessages = False
		else:
			self.highlightNickMessages = True
		self.settings[HIGHLIGHT_NICK_MESSAGE] = self.highlightNickMessages
		saveSettings(self.settings,self.settingsFile)

	def toggleAutoNick(self):
		if self.autocompleteNicks:
			self.autocompleteNicks = False
		else:
			self.autocompleteNicks = True
		self.settings[AUTOCOMPLETE_ENTITIES] = self.autocompleteNicks
		saveSettings(self.settings,self.settingsFile)

	def toggleAutoCommands(self):
		if self.autocompleteCommands:
			self.autocompleteCommands = False
		else:
			self.autocompleteCommands = True
		self.settings[AUTOCOMPLETE_COMMANDS] = self.autocompleteCommands
		saveSettings(self.settings,self.settingsFile)

	def toggleSpellCheck(self):
		if self.spellCheck:
			self.spellCheck = False
		else:
			self.spellCheck = True

		for w in self.connections:
			for x in self.windows[w]:
				t = x.window.userTextInput.toPlainText()
				x.window.userTextInput.setPlainText(t)
				x.window.userTextInput.moveCursor(QTextCursor.End)
		
		self.settings[ENABLE_SPELL_CHECK] = self.spellCheck
		saveSettings(self.settings,self.settingsFile)

	def toggleTrayMenu(self):
		if self.menuTray:
			self.menuTray = False
			self.destroyTrayMenu()
		else:
			self.menuTray = True
			self.buildTrayMenu()

		self.settings[SYSTEM_TRAY_MENU] = self.menuTray
		saveSettings(self.settings,self.settingsFile)

	def toggleTray(self):
		if self.showTray:
			self.showTray = False
			self.tray.hide()
			self.optFlash.setEnabled(False)
			self.optTrayMenu.setEnabled(False)
		else:
			self.showTray = True
			self.tray.show()
			self.optFlash.setEnabled(True)
			self.optTrayMenu.setEnabled(True)

		self.settings[SYSTEM_TRAY_SETTING] = self.showTray
		saveSettings(self.settings,self.settingsFile)

	def toggleFlash(self):
		if self.flashTray:
			self.flashTray = False
		else:
			self.flashTray = True

		self.settings[SYSTEM_TRAY_FLASH_SETTING] = self.flashTray
		saveSettings(self.settings,self.settingsFile)

	def toggleLoadChat(self):
		if self.loadLogsOnJoin:
			self.loadLogsOnJoin = False
		else:
			self.loadLogsOnJoin = True

		self.settings[LOAD_LOG_SETTING] = self.loadLogsOnJoin
		saveSettings(self.settings,self.settingsFile)

	def toggleSaveLogs(self):
		if self.saveLogsOnExit:
			self.saveLogsOnExit = False
		else:
			self.saveLogsOnExit = True
		
		self.settings[AUTO_SAVE_CHAT_LOGS] = self.saveLogsOnExit
		saveSettings(self.settings,self.settingsFile)

	def toggleWinToolbars(self):
		if self.windowToolbars:
			self.windowToolbars = False
		else:
			self.windowToolbars = True

		for c in self.connections:
			for x in self.windows[c]:
				if self.windowToolbars:
					x.window.showToolbar()
				else:
					x.window.showMenus()

		self.settings[CHAT_TOOLBAR_SETTING] = self.windowToolbars
		saveSettings(self.settings,self.settingsFile)

	def toggleListEnable(self):
		if self.channelListEnabled:
			self.channelListEnabled = False
		else:
			self.channelListEnabled = True
		self.settings[ENABLE_LIST_SETTING] = self.channelListEnabled
		saveSettings(self.settings,self.settingsFile)

		for sid in self.toolbars:
			#self.toolbars[sid].buttonList.setEnabled(self.channelListEnabled)
			self.rebuildServerInfoMenu(sid)



	def toggleNetworkChat(self):
		if self.logChatByNetwork:
			self.logChatByNetwork = False
		else:
			self.logChatByNetwork = True
		
		self.settings[SAVE_LOGS_BY_NETWORK] = self.logChatByNetwork
		saveSettings(self.settings,self.settingsFile)

	def toggleTitle(self):
		if self.titleActiveWindow:
			self.titleActiveWindow = False
			self.setWindowTitle(DEFAULT_WINDOW_TITLE)
		else:
			self.titleActiveWindow = True
			self.updateActiveChild(self.MDI.activeSubWindow())

		self.settings[TITLE_ACTIVE_WINDOW_SETTING] = self.titleActiveWindow
		saveSettings(self.settings,self.settingsFile)

	def toggleLinks(self):
		if self.urlsToLinks:
			self.urlsToLinks = False
		else:
			self.urlsToLinks = True
		self.settings[DOLINKS_SETTING] = self.urlsToLinks
		saveSettings(self.settings,self.settingsFile)

	def markMenuEntry(self,qa):
		f = qa.font()
		f.setBold(True)
		f.setItalic(True)
		qa.setFont(f)

	def buildThemeMenu(self):
		self.themeMenu.clear()

		if not self.themesEnabled:
			themeDisabledLabel = QLabel("<i>&nbsp;&nbsp;Themes have been disabled&nbsp;&nbsp;</i>")
			themeDisabledAction = QWidgetAction(self)
			themeDisabledAction.setDefaultWidget(themeDisabledLabel)
			self.themeMenu.addAction(themeDisabledAction)

			return

		if self.theme.lower() == USE_NO_THEME_SETTING:
			nme = QAction("Default theme",self,checkable=True)
		else:
			nme = QAction(QIcon(ERK_ICON),"Default theme",self)
		nme.triggered.connect(lambda state: self.applyTheme(USE_NO_THEME_SETTING) )
		self.themeMenu.addAction(nme)
		if self.theme.lower() == USE_NO_THEME_SETTING:
			nme.setChecked(True)
			self.markMenuEntry(nme)

		if len(self.themeList)>0: self.themeMenu.addSeparator()

		for t in self.themeList:

			icon = getThemeIcon(t)
			if icon:
				if self.theme == t:
					tme = QAction(t,self,checkable=True)
					tme.setChecked(True)
					self.markMenuEntry(tme)
				else:
					tme = QAction(QIcon(icon),t,self)
			else:
				if self.theme == t:
					tme = QAction(t,self,checkable=True)
					tme.setChecked(True)
					self.markMenuEntry(tme)
				else:
					tme = QAction(t,self)
			tme.triggered.connect(lambda state,f=t: self.applyTheme(f))
			self.themeMenu.addAction(tme)

		if self.theme.lower() == USE_NO_THEME_SETTING:
			self.themeMenu.setTitle("Theme")
		else:
			self.themeMenu.setTitle(f"Theme ({self.theme})")

		self.themeMenu.addSeparator()

		optIcons = QAction("Use theme icons",self,checkable=True)
		optIcons.setChecked(self.themeIcons)
		optIcons.triggered.connect(self.toggleIcons)
		self.themeMenu.addAction(optIcons)

		self.themeMenu.addSeparator()


		tme = QAction(QIcon(LOAD_ICON),"Scan for new themes",self)
		tme.triggered.connect(lambda state: self.reloadThemes())
		self.themeMenu.addAction(tme)

		prestart = QAction(QIcon(RESTART_ICON),f"Restart {APPLICATION_NAME}",self)
		prestart.triggered.connect(lambda state: restart_program())
		self.themeMenu.addAction(prestart)

	def reloadThemes(self):
		self.themeList = getThemeList()
		self.buildThemeMenu()

	def applyTheme(self,theme):
		if theme.lower() == USE_NO_THEME_SETTING:
			self.setStyleSheet("")
			self.theme = USE_NO_THEME_SETTING
			self.buildThemeMenu()
			self.settings[THEME_SETTING] = self.theme
			saveSettings(self.settings,self.settingsFile)
			self.displayFile = DISPLAY_CONFIGURATION
			self.display = loadDisplay(self.displayFile)
			importThemeResources(USE_NO_THEME_SETTING)

			# Rerender window text and icons
			for s in self.connections:
				for w in self.windows[s]:
					w.window.rerenderTextDisplay()
					if w.window.is_channel:
						w.window.redrawUserlist()
						w.window.setWindowIcon(QIcon(CHANNEL_WINDOW_ICON))
					else:
						w.window.setWindowIcon(QIcon(USER_WINDOW_ICON))
					w.window.hide()
					w.window.show()
			return
		importThemeResources(self.theme)
		themeFile = getThemeQSS(theme)
		if themeFile != None:
			self.theme = theme
			self.setStyleSheet(themeFile)
			self.buildThemeMenu()
			self.settings[THEME_SETTING] = self.theme
			saveSettings(self.settings,self.settingsFile)
		themeArray = getThemeJSON(theme)
		if len(themeArray)==2:
			self.display = themeArray[0]
			self.displayFile = themeArray[1]

			self.setNewFont(self.display['font'])

		# Rerender window text and icons
		for s in self.connections:
			for w in self.windows[s]:
				w.window.rerenderTextDisplay()
				if w.window.is_channel:
					w.window.redrawUserlist()
					w.window.setWindowIcon(QIcon(CHANNEL_WINDOW_ICON))
				else:
					w.window.setWindowIcon(QIcon(USER_WINDOW_ICON))
				w.window.hide()
				w.window.show()
	
	def generateNetworkLink(self,net):
		if net.lower() == "efnet":
			return f"<big><big><b><a href=\"http://www.efnet.org/\">EFnet</a></b></big></big><br><small>IRC Network</small>"
		if net.lower() == "quakenet":
			return f"<big><big><b><a href=\"https://www.quakenet.org/\">Quakenet</a></b></big></big><br><small>IRC Network</small>"
		if net.lower() == "dalnet":
			return f"<big><big><b><a href=\"https://www.dal.net/\">DALnet</a></b></big></big><br><small>IRC Network</small>"
		if net.lower() == "gamesurge":
			return f"<big><big><b><a href=\"https://gamesurge.net/\">Gamesurge</a></b></big></big><br><small>IRC Network</small>"
		if net.lower() == "freenode":
			return f"<big><big><b><a href=\"https://freenode.net/\">Freenode</a></b></big></big><br><small>IRC Network</small>"
		if net.lower() == "swiftirc":
			return f"<big><big><b><a href=\"https://www.swiftirc.net/\">SwiftIRC</a></b></big></big><br><small>IRC Network</small>"
		if net.lower() == "undernet":
			return f"<big><big><b><a href=\"http://www.undernet.org/\">Undernet</a></b></big></big><br><small>IRC Network</small>"
		if net.lower() == "ircnet":
			return f"<big><big><b><a href=\"http://www.ircnet.org/\">IRCnet</a></b></big></big><br><small>IRC Network</small>"
		return f"<big><big><b>{net}</b></big></big><br><small>IRC Network</small>"


	def rebuildServerInfoMenu(self,serverid):

		supports = self.connections[serverid].supports # list
		maxchannels = self.connections[serverid].maxchannels
		maxnicklen = self.connections[serverid].maxnicklen
		channellen = self.connections[serverid].channellen
		topiclen = self.connections[serverid].topiclen
		kicklen = self.connections[serverid].kicklen
		awaylen = self.connections[serverid].awaylen
		maxtargets = self.connections[serverid].maxtargets
		modes = self.connections[serverid].modes
		chanmodes = self.connections[serverid].chanmodes #list
		prefix = self.connections[serverid].prefix # list
		cmds = self.connections[serverid].cmds # list
		network = self.connections[serverid].network
		casemapping = self.connections[serverid].casemapping

		shost = self.connections[serverid].host
		sport = str(self.connections[serverid].port)

		maxmodes = self.connections[serverid].maxmodes

		self.toolbars[serverid].servinfo.clear()

		# Spacer
		el = QLabel("<i>&nbsp;</i>",self)
		el.setAlignment(Qt.AlignCenter)
		f = el.font()
		f.setPointSize(2)
		el.setFont(f)
		g = QWidgetAction(self)
		g.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(g)

		el = QLabel(self.generateNetworkLink(network),self)
		el.setOpenExternalLinks(True)
		el.setAlignment(Qt.AlignCenter)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		# Spacer
		self.toolbars[serverid].servinfo.addAction(g)

		self.toolbars[serverid].servinfo.addSeparator()

		joinChannel = QAction(QIcon(CHANNEL_WINDOW_ICON),"Join a channel",self)
		joinChannel.triggered.connect(lambda state,serv=serverid: self.doToolbarJoinKey(serv))
		self.toolbars[serverid].servinfo.addAction(joinChannel)

		changeNick = QAction(QIcon(USER_ICON),"Change your nickname",self)
		changeNick.triggered.connect(lambda state,serv=serverid: self.doNickChange(serv))
		self.toolbars[serverid].servinfo.addAction(changeNick)

		if self.channelListEnabled:
			listChannels = QAction(QIcon(LIST_ICON),"List channels",self)
			listChannels.triggered.connect(lambda state,serv=serverid: self.doToolbarListChannels(serv))
			self.toolbars[serverid].servinfo.addAction(listChannels)

		self.toolbars[serverid].servinfo.addSeparator()

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum channels:</b> {maxchannels}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum nick length:</b> {maxnicklen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum channel length:</b> {channellen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum topic length:</b> {topiclen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum kick length:</b> {kicklen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum away length:</b> {awaylen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum message targets:</b> {maxtargets}&nbsp;&nbsp;",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum modes per user:</b> {modes}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.toolbars[serverid].servinfo.addAction(e)

		self.toolbars[serverid].servinfo.addSeparator()

		maxmodesmenu = QMenu("Maximum modes",self)
		for c in maxmodes:
			e = QAction(F"{c[0]}: {c[1]}", self) 
			maxmodesmenu.addAction(e)
		self.toolbars[serverid].servinfo.addMenu(maxmodesmenu)

		cmdmenu = QMenu("Commands",self)
		for c in cmds:
			e = QAction(F"{c}", self) 
			cmdmenu.addAction(e)
		self.toolbars[serverid].servinfo.addMenu(cmdmenu)

		supportsmenu = QMenu("Supports",self)
		for c in supports:
			e = QAction(F"{c}", self) 
			supportsmenu.addAction(e)
		self.toolbars[serverid].servinfo.addMenu(supportsmenu)

		chanmodemenu = QMenu("Channel modes",self)
		ct = 0
		for c in chanmodes:
			if ct==0:
				ctype = "A"
			elif ct==1:
				ctype = "B"
			elif ct==2:
				ctype = "C"
			elif ct==3:
				ctype = "D"
			e = QAction(F"{ctype}: {c}", self) 
			chanmodemenu.addAction(e)
			ct = ct + 1
		self.toolbars[serverid].servinfo.addMenu(chanmodemenu)

		prefixmenu = QMenu("Prefixes",self)
		for c in prefix:
			m = c[0]
			s = c[1]
			if s=="&": s="&&"
			e = QAction(F"{m}: {s}", self)
			if m=="o": e.setIcon(QIcon(OPERATOR_ICON))
			if m=="v": e.setIcon(QIcon(VOICED_ICON))
			prefixmenu.addAction(e)
		self.toolbars[serverid].servinfo.addMenu(prefixmenu)

		# INSERT CHANNEL LIST

		

	# ========================
	# Special Widget Functions
	# ========================

	def buildDockLog(self):

		width = self.width()
		height = self.height() * 0.28

		class LogWidget(QTextBrowser):

			def __init__(self,parent=None):
				self.started = True
				super(LogWidget, self).__init__(parent)

			def sizeHint(self):
				if self.started:
					self.started = False
					return QSize(width, height)
				return QSize(self.width(), self.height())

		self.logTxt = LogWidget(self)
		self.logTxt.anchorClicked.connect(self.linkClicked)

		dock = QDockWidget(self)
		dock.setWidget(self.logTxt)
		dock.setFloating(False)

		dock.visibilityChanged.connect(self.manualHideDock)

		dock.setFeatures( QDockWidget.DockWidgetVerticalTitleBar | QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable )

		return dock

	def buildServerToolbar(self,serverid):
		servbar = QToolBar(self)
		self.addToolBar(Qt.TopToolBarArea,servbar)
		servbar.setIconSize(QSize(16,16))
		servbar.setFloatable(True)
		servbar.setAllowedAreas( Qt.TopToolBarArea | Qt.BottomToolBarArea )
		servbar.setContextMenuPolicy(Qt.PreventContextMenu)

		servbar.addWidget(QLabel(" "))

		serverhost = self.connections[serverid].hostname

		servbar.servLabel = QPushButton(f"{serverhost} ")

		pbcss = """QPushButton {
	border: 0px;
}/*
QPushButton::menu-indicator {
	width: 0px;
}*/
"""
		servbar.servLabel.setStyleSheet(pbcss)
		f = servbar.servLabel.font()
		f.setBold(True)
		servbar.servLabel.setFont(f)

		servbar.servinfo = QMenu(self)
		servbar.servLabel.setMenu(servbar.servinfo)

		servbar.addWidget(servbar.servLabel)

		servbar.addWidget(QLabel(" "))

		servbar.addSeparator()

		servbar.addWidget(QLabel(" "))

		n = self.connections[serverid].nickname
		servbar.nickname = QPushButton(" "+n)
		servbar.nickname.setStyleSheet(pbcss)
		servbar.nickname.clicked.connect(lambda state,serv=serverid: self.doNickChange(serv))

		f = servbar.nickname.font()
		f.setBold(True)
		servbar.nickname.setFont(f)

		servbar.nickname.setIcon(QIcon(USER_ICON))
		servbar.nickname.setIconSize(QSize(15,15))

		servbar.addWidget(servbar.nickname)

		servbar.addWidget(QLabel(" "))

		servbar.awaylabel = QLabel("")
		servbar.awaylabel.setAlignment(Qt.AlignCenter)
		#servbar.awaylabel.setVisible(False)
		servbar.addWidget(servbar.awaylabel)

		servbar.addWidget(QLabel(" "))

		servbar.addSeparator()

		servbar.addWidget(QLabel(" "))

		servbar.modelabel = QLabel("<b>Modes:</b>")
		servbar.modelabel.setAlignment(Qt.AlignCenter)
		servbar.addWidget(servbar.modelabel)

		servbar.addWidget(QLabel(" "))

		servbar.usermodes = QLabel(DEFAULT_USERMODE_DISPLAY)
		servbar.usermodes.setAlignment(Qt.AlignCenter)
		servbar.addWidget(servbar.usermodes)

		servbar.addWidget(QLabel("     "))

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		servbar.addWidget(spacer)

		if self.displayUptime:
			servbar.stimer = QLabel("00:00:00")
		else:
			servbar.stimer = QLabel(" ")
		servbar.stimer.setFont(self.fontBold)

		servbar.stimer.setAlignment(Qt.AlignCenter)

		servbar.stimecount = 0
		servbar.addWidget(servbar.stimer)
		servbar.addWidget(QLabel(" "))

		buttonDisco = QPushButton()
		buttonDisco.setIcon(QIcon(TOOLBAR_DISCONNECT_ICON))
		buttonDisco.setToolTip(f"Disconnect from {serverhost}")
		buttonDisco.clicked.connect(lambda state,serv=serverid: self.doToolbarDisconnect(serv))
		servbar.addWidget(buttonDisco)
		buttonDisco.setFixedHeight(TOOLBAR_BUTTON_HEIGHT)
		buttonDisco.setStyleSheet(pbcss)

		# Stack toolbars if there's more than one
		self.addToolBarBreak(Qt.TopToolBarArea)

		return servbar

	# ================
	# Dialog Functions
	# ================

	def doIgnoreDialog(self):

		x = QMdiSubWindow()
		y = IgnoreDialog.Dialog(self)
		y.setSubwindow(x)
		x.setWidget(y)
		x.setWindowFlags(
			Qt.WindowCloseButtonHint |
			Qt.WindowTitleHint )
		self.MDI.addSubWindow(x)


		# Center window
		wx = (self.MDI.width()/2)-(x.width()/2)
		wy = (self.MDI.height()/2)-(x.height()/2)
		x.move(wx,wy)

		x.setFixedSize(x.sizeHint())

		x.show()

	def doAbout(self):
		x = QMdiSubWindow()
		x.setWidget(AboutDialog.Dialog(self))
		x.setWindowFlags(
			Qt.WindowCloseButtonHint |
			Qt.WindowTitleHint )
		self.MDI.addSubWindow(x)

		# Center window
		wx = (self.MDI.width()/2)-(x.width()/2)
		wy = (self.MDI.height()/2)-(x.height()/2)
		x.move(wx,wy)

		x.setFixedSize(x.sizeHint())

		if self.isMaximized():
			self.showNormal()

		for c in self.connections:
			for w in self.windows[c]:
				if w.window.isMaximized(): w.window.showNormal()
				if w.subwindow.isMaximized(): w.subwindow.showNormal()

		x.show()

	def doAboutKod(self,cwin):
		x = QMdiSubWindow()
		x.setWidget(AboutKodDialog.Dialog(self))
		x.setWindowFlags(
			Qt.WindowCloseButtonHint |
			Qt.WindowTitleHint )
		self.MDI.addSubWindow(x)

		# Center window
		wx = (self.MDI.width()/2)-(x.width()/2)
		wy = (self.MDI.height()/2)-(x.height()/2)
		x.move(wx,wy)

		x.setFixedSize(x.sizeHint())

		if cwin.isMaximized():
			cwin.showNormal()

		x.show()

	def selectDisconnect(self):
		servers = []
		ids = []
		for w in self.connections: 
			servers.append(self.connections[w].nickname+" on "+self.connections[w].hostname)
			ids.append(w)

		#print(ids)

		# If there's only one connection active, disconnect it
		if len(servers)==1:
			self.disconnected_on_purpose = True
			self.connections[ids[0]].quit()
			return

		item, okPressed = QInputDialog.getItem(self,"Select Connection","Which server to disconnect from?",servers,0,False)
		if okPressed and item:
			self.disconnected_on_purpose = True
			c = 0
			for i in servers:
				if i==item:
					self.connections[ids[c]].quit()
					continue
				c = c + 1
			self.rebuildWindowMenu()

	def doSaveNick(self,n):
		nick = n.nickname.text()
		nick = nick.replace("&nbsp;","")
		nick = nick.replace("<b>","")
		nick = nick.replace("</b>","")
		#print(nick)
		s = get_user()
		s["nick"] = nick
		#print(s)
		save_user(s)

	def doToolbarListChannels(self,serverid):
		
		self.connections[serverid].sendLine("LIST")

	def doToolbarDisconnect(self,serverid):
		
		self.disconnected_on_purpose = True
		self.connections[serverid].quit()

	def doToolbarJoinKey(self,serverid):
		x = JoinDialog.Dialog()
		channel_info = x.get_channel_information(parent=self)

		# User cancled dialog
		if not channel_info: return

		channel = channel_info[0]
		password = channel_info[1]

		if channel.isspace() or len(channel)==0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(ERK_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("No channel entered")
			msg.setWindowTitle("Error")
			msg.exec_()
			return

		if password.isspace() or len(password)==0:
			self.connections[serverid].join(channel)
		else:
			self.connections[serverid].join(channel,password)

	def doChannelJoin(self,serverid,toolbar):

		chan = toolbar.channel.text()
		if len(chan)>0:
			if chan[0]=="#":
				self.connections[serverid].join(chan)
			else:
				chan = "#" + chan
				self.connections[serverid].join(chan)
			toolbar.channel.setText('')

	def doNickChange(self,serverid):

		x = NickDialog.Dialog()
		newnick = x.get_nick_information(parent=self)

		# User cancled dialog
		if not newnick: return

		if newnick.isspace() or len(newnick)==0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(ERK_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("No nick entered")
			msg.setWindowTitle("Error")
			msg.exec_()
			return

		oldnick = self.nickname

		self.connections[serverid].setNick(newnick)

	def doUserDialog(self):

		x = UserDialog.Dialog()
		user = x.get_user_information(parent=self)

		if not user: return

		nick = user[0]
		username = user[1]
		realname = user[2]
		alternate = user[3]

		errs = []
		if len(nick)==0: errs.append("nickname not entered")
		if len(alternate)==0: errs.append("alternate name not entered")
		if len(username)==0: errs.append("username not entered")
		if len(realname)==0: errs.append("real name not entered")
		if len(errs)>0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(ERK_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Missing or Invalid Input")
			es = ""
			for e in errs: es = es + f"<li>{e}</li>"
			msg.setInformativeText(f"<ul>{es}</ul>")
			msg.setWindowTitle("Faulty user information")
			msg.exec_()
			return

		si = {
			"nick": nick,
			"username": username,
			"realname": realname,
			"alternate": alternate,
		}

		save_user(si)

	def doColorDialog(self):
		
		# Show dialog, and get information from the user
		x = ColorDialog.Dialog(parent=self)
		display_colors = x.get_color_information(parent=self)

		# User cancled dialog
		if not display_colors: return

		# self.connectToIRC(connection_info)
		self.display = display_colors
		saveDisplay(self.display,self.displayFile)
		self.applyTheme(self.theme)

	def doConnectDialog(self):
		
		# Show dialog, and get information from the user
		x = ConnectDialog.Dialog(self.can_use_ssl,parent=self)
		connection_info = x.get_connect_information(self.can_use_ssl,parent=self)

		# User cancled dialog
		if not connection_info: return

		self.connectToIRC(connection_info)

	def doNetworkDialog(self):
		
		# Show dialog, and get information from the user
		x = NetworkDialog.Dialog(self.can_use_ssl,parent=self)
		connection_info = x.get_connect_information(self.can_use_ssl,parent=self)

		# User cancled dialog
		if not connection_info: return

		self.connectToIRC(connection_info)

	def setNewFont(self,font):
		f = QFont()
		f.fromString(font)

		self.app.setFont(f)
		self.logTxt.setFont(f)

		for c in self.connections:
			for w in self.windows[c]:
				w.window.channelChatDisplay.setFont(f)
				w.window.userTextInput.setFont(f)
				if w.window.is_channel:
					fb = f
					fb.setBold(True)
					w.window.channelUserDisplay.setFont(fb)

			fb = f
			fb.setBold(True)
			self.toolbars[c].stimer.setFont(fb)

		f = QFont()
		f.fromString(font)
		self.font = f
		self.font.setItalic(False)
		self.font.setBold(False)

		self.display["font"] = font
		saveDisplay(self.display,self.displayFile)

		f = QFont()
		f.fromString(font)
		self.fontBold = f
		self.fontBold.setBold(True)
		self.fontBold.setItalic(False)

		f = QFont()
		f.fromString(font)
		self.fontitalic = f
		self.fontitalic.setItalic(True)
		self.fontitalic.setBold(False)

	# ==========
	# IRC Events
	# ==========

	def renamed(self,serverid,nick,oldnick,displaytarget):

		isme = False
		if self.toolbars[serverid].nickname.text()==f" {oldnick}":
			self.toolbars[serverid].nickname.setText(f" {nick}")
			isme = True

		for w in self.windows[serverid]:

			if w.window.name==oldnick:
				w.window.name = nick
				w.window.setWindowTitle(" "+nick)
				w.subwindow.setWindowTitle(" "+nick)

			if w.window.is_channel:
				if isme:
					w.window.nickname = nick
				new_rl = []
				new_ul = []
				new_u = []
				for u in w.window.rawusers:
					p = u.split('!')
					if len(p)==2:
						user = p[0]
					else:
						user = p

					if type(user)==list:
						user = str( list(user).pop(0)  )

					if user[:1]=='@':
						if user[1:]==oldnick:
							e = u.replace(f"@{oldnick}",f"@{nick}",1)
							new_rl.append(e)
							new_ul.append(e[1:])
							new_u.append(f"@{nick}")
						else:
							new_rl.append(u)
							new_ul.append(u[1:])
							new_u.append(user)
					elif user[:1]=='+':
						if user[1:]==oldnick:
							e = u.replace(f"+{oldnick}",f"+{nick}",1)
							new_rl.append(e)
							new_ul.append(e[1:])
							new_u.append(f"+{nick}")
						else:
							new_rl.append(u)
							new_ul.append(u[1:])
							new_u.append(user)
					else:
						if user==oldnick:
							e = u.replace(oldnick,nick,1)
							new_rl.append(e)
							new_ul.append(e)
							new_u.append(nick)
						else:
							new_rl.append(u)
							new_ul.append(u)
							new_u.append(user)

				w.window.rawusers = new_rl
				w.window.userlist = new_ul
				w.window.users = new_u

				w.window.redrawUserlist()

		d = systemTextDisplay(f"{displaytarget} now known as \"{nick}\"",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)
		self.writeToAll(serverid,d)

	def connecting(self,serverid,obj,host,port):
		d = systemTextDisplay(f"Connecting to {host}:{str(port)}...",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)

	def connect(self,serverid,obj):

		# Store the connection
		self.connections[serverid] = obj

		serverhost = self.connections[serverid].hostname

		if serverhost == None:
			serverhost = obj.host + ":" + str(obj.port)

		self.connections[serverid].heartbeatInterval = self.heartbeatInterval

		self.timers[serverid] = UptimeHeartbeat(self)
		self.timers[serverid].beat.connect(lambda serverid=serverid: self.servBeat(serverid))

		# Display to the user that we're connected
		d = systemTextDisplay(f"Connected to {serverhost}!",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)

		# Display to the user that we're registering
		d = systemTextDisplay(f"Registering with {serverhost}...",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)

	def disconnect(self,serverid,reason):

		#serverhost = self.connections[serverid].hostname

		if self.connections[serverid].hostname == None:
			serverhost = self.connections[serverid].host + ":" + str(self.connections[serverid].port)
		else:
			serverhost = self.connections[serverid].hostname

		if "closed clean" in f"{reason}":
			reason = "Quit IRC"
		else:
			reason = "Connection error"

		if self.connections[serverid].alive:
			self.connections[serverid].stopHeartbeat()

		# Delete the stored connection
		del self.connections[serverid]

		# Close all windows associated with the connection
		for w in self.windows[serverid]:
			w.subwindow.close()
			w.window.close()

		# Close all channel list windows
		for w in self.channel_list_windows:
			if w[2]==serverid:
				w[0].close()
				w[1].close()

		# Delete stored windows
		del self.windows[serverid]

		if "closed clean" in f"{reason}":
			d = systemTextDisplay(f"Disconnected from {serverhost}.",self.maxnicklen,SYSTEM_COLOR)
		else:
			d = systemTextDisplay(f"Disconnected from {serverhost}: {reason}",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)

		# Disable "Disconnect" menu item if there's no active connections
		if len(self.connections)==0:
			self.actDisconnect.setEnabled(False)

		self.timers[serverid].stop()	# Stop the server uptime counter
		self.timers[serverid] = None

		# Destroy server toolbar
		self.toolbars[serverid].close()
		self.toolbars[serverid] = None

		if len(self.connections)==0:
			self.connected = False
			self.setWindowTitle(DEFAULT_WINDOW_TITLE)

		# Update status bar
		self.updateStatusBar()
		
	def registered(self,serverid):

		#serverhost = self.connections[serverid].hostname
		if self.connections[serverid].hostname == None:
			serverhost = self.connections[serverid].host + ":" + str(self.connections[serverid].port)
		else:
			serverhost = self.connections[serverid].hostname

		# We're connected, so make the "Disconnect" menu item enabled
		self.actDisconnect.setEnabled(True)

		d = systemTextDisplay(f"Registered with {serverhost}!",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)

		autojoins = get_autojoins(self.connections[serverid].host)
		for c in autojoins:
			p = c.split(AUTOJOIN_DELIMITER)
			if len(p)==2:
				# got a key
				self.connections[serverid].join(p[0],p[1])
			else:
				self.connections[serverid].join(c)

		self.timers[serverid].start()	# Start the server uptime counter

		self.toolbars[serverid] = self.buildServerToolbar(serverid)

		if self.keepAlive:
			self.connections[serverid].alive = True
			self.connections[serverid].startHeartbeat()
		else:
			self.connections[serverid].alive = False

		self.connected = True

		if self.commandlineJoinChannel!=None:
			if self.commandlineJoinChannelKey!=None:
				self.connections[serverid].join(self.commandlineJoinChannel,self.commandlineJoinChannelKey)
			else:
				self.connections[serverid].join(self.commandlineJoinChannel)
			self.commandlineJoinChannel = None
			self.commandlineJoinChannelKey = None

		# Update status bar
		self.updateStatusBar()

		# If we're not going to save the server, return
		if not self.saveServers: return

		# Don't save passwords that require a password
		if self.connections[serverid].password != '': return

		# Check to see if the server we're connected to is in the
		# IRC network list, and if not, save it
		netlist = []
		if os.path.isfile(SAVED_SERVERS_FILE):
			script = open(SAVED_SERVERS_FILE,"r")
			for line in script:
				x = line.split(":")
				if len(x) != 4: continue
				x[0].strip()	# host
				x[1].strip()	# port
				x[2].strip()	# network
				x[3].strip()	# "ssl" or "normal"

				if self.connections[serverid].host == x[0]:
					if self.connections[serverid].port == int(x[1]):
						# The server has been found, so return
						return
				#line.strip()
				netlist.append(line)
			script.close()

		# Build a server entry
		ent = self.connections[serverid].host + ":" + str(self.connections[serverid].port)
		if self.connections[serverid].network=="":
			cnet = UNKNOWN_NETWORK
		else:
			cnet = self.connections[serverid].network
		ent = ent + ":" + cnet + ":"

		if self.connections[serverid].usessl:
			ent = ent + "ssl"
		else:
			ent = ent + "normal"

		ent = ent + "\n"

		# Insert new server entry at the beginning of the network list
		if len(netlist)==0:
			netlist.append(ent)
		else:
			netlist.insert(0,ent)

		# Write the new network list to file
		script = open(SAVED_SERVERS_FILE,"w")
		script.write("".join(netlist))
		script.close()


	def joined(self,serverid,channel):

		# Create the channel window, store it, and show it
		chanWindow = Window.createNew(channel,self.connections[serverid],serverid,self.MDI,self)
		self.windows[serverid].append(chanWindow)
		chanWindow.window.show()

		d = systemTextDisplay(f"Joined {channel}.",self.maxnicklen,SYSTEM_COLOR)
		self.writeToChatWindow(serverid,channel,d)

		self.rebuildWindowMenu()

	def channelNames(self,serverid,channel,users):

		for w in self.windows[serverid]:
			if w.window.name == channel:
				w.window.setUserList(users)

	def publicMessage(self,serverid,channel,user,message):

		# Ignore messages from users on the ignore list
		i = user.split("!")
		for u in self.ignore:
			if len(i)==2:
				nick = i[0]
				hostmask = i[1]
				h = hostmask.split('@')
				username = h[0]
				host = h[1]

				if u==nick:
					return

				if u==host:
					return
			else:
				if u==i:
					return

		p = user.split("!")
		if len(p)==2: user = p[0]

		if self.stripIRCcolor:
			message = strip_color(message)
		elif self.FORCE_NOCOLORS:
			message = strip_color(message)

		if self.profanityFilter:
			message = filterProfanityFromText(message)
		elif self.FORCE_PROFANITY_FILTER:
			message = filterProfanityFromText(message)

		if self.isMinimized():
			self.IS_FLASHING = True

		if self.highlightNickMessages:
			if self.connections[serverid].nickname.lower() in message.lower():
				#d = chat_display(user,message,self.maxnicklen,self.urlsToLinks,self.display['user'],self.display['highlight'],self.display['background'],True)
				d = chat_display_highlight(user,message,self.maxnicklen,self.urlsToLinks,USER_COLOR,HIGHLIGHT_COLOR)
			else:
				d = chat_display(user,message,self.maxnicklen,self.urlsToLinks,USER_COLOR)
		else:
			d = chat_display(user,message,self.maxnicklen,self.urlsToLinks,USER_COLOR)

		self.writeToChatWindow(serverid,channel,d)
		self.notifyChatWindow(serverid,channel)

	def privateMessage(self,serverid,user,message):

		# Ignore messages from users on the ignore list
		i = user.split("!")
		for u in self.ignore:
			if len(i)==2:
				nick = i[0]
				hostmask = i[1]
				h = hostmask.split('@')
				username = h[0]
				host = h[1]

				if u==nick:
					return

				if u==host:
					return
			else:
				if u==i:
					return

		p = user.split("!")
		if len(p)==2: user = p[0]

		if self.stripIRCcolor:
			message = strip_color(message)
		elif self.FORCE_NOCOLORS:
			message = strip_color(message)

		if self.profanityFilter:
			message = filterProfanityFromText(message)
		elif self.FORCE_PROFANITY_FILTER:
			message = filterProfanityFromText(message)

		if self.isMinimized():
			self.IS_FLASHING = True

		for w in self.windows[serverid]:
			if w.window.name == user:

				if do_not_suppress:
					# Window exists
					d = chat_display(user,message,self.maxnicklen,self.urlsToLinks,USER_COLOR)
					self.writeToChatWindow(serverid,user,d)
					self.notifyChatWindow(serverid,user)
				return

		if self.openWindowOnIncomingPrivate:

			if do_not_suppress:
				# Window doesn't exist, so create it
				userWindow = Window.createNew(user,self.connections[serverid],serverid,self.MDI,self)
				self.windows[serverid].append(userWindow)
				userWindow.window.show()

				# Write to it
				d = chat_display(user,message,self.maxnicklen,self.urlsToLinks,USER_COLOR)
				self.writeToChatWindow(serverid,user,d)
				self.notifyChatWindow(serverid,user)

				self.rebuildWindowMenu()
		else:
			if do_not_suppress:
				link = encodeWindowLink(serverid,user)
				d = log_chat_display(f"<b>[{serverid}] <a href=\"{link}\">{user}</a></b>",message,self.maxnicklen,self.urlsToLinks,USER_COLOR)
				self.writeToLog(d)

	def noticeMessage(self,serverid,channel,user,message):

		# Ignore messages from users on the ignore list
		i = user.split("!")
		for u in self.ignore:
			if len(i)==2:
				nick = i[0]
				hostmask = i[1]
				h = hostmask.split('@')
				username = h[0]
				host = h[1]

				if u==nick:
					return

				if u==host:
					return
			else:
				if u==i:
					return

		p = user.split("!")
		if len(p)==2: user = p[0]

		if self.stripIRCcolor:
			message = strip_color(message)
		elif self.FORCE_NOCOLORS:
			message = strip_color(message)

		if self.profanityFilter:
			message = filterProfanityFromText(message)
		elif self.FORCE_PROFANITY_FILTER:
			message = filterProfanityFromText(message)

		if self.isMinimized():
			self.IS_FLASHING = True

		is_channel = True
		if len(channel)>1 and channel[0]!="#": is_channel = False

		if is_channel:
			for w in self.windows[serverid]:
				if w.window.name == channel:
					# Window exists
					d = notice_display(user,message,self.maxnicklen,self.urlsToLinks,NOTICE_COLOR)
					self.writeToChatWindow(serverid,channel,d)
					self.notifyChatWindow(serverid,channel)
					return

		# 
		if user=="":
			d = systemTextDisplay(message,self.maxnicklen,self.display['notice'])
		else:
			d = notice_display(user,message,self.maxnicklen,self.urlsToLinks,NOTICE_COLOR)
		self.writeToLog(d)

	def actionMessage(self,serverid,channel,user,message):

		# Ignore messages from users on the ignore list
		i = user.split("!")
		for u in self.ignore:
			if len(i)==2:
				nick = i[0]
				hostmask = i[1]
				h = hostmask.split('@')
				username = h[0]
				host = h[1]

				if u==nick:
					return

				if u==host:
					return
			else:
				if u==i:
					return

		p = user.split("!")
		if len(p)==2: user = p[0]

		if self.stripIRCcolor:
			message = strip_color(message)
		elif self.FORCE_NOCOLORS:
			message = strip_color(message)

		if self.profanityFilter:
			message = filterProfanityFromText(message)
		elif self.FORCE_PROFANITY_FILTER:
			message = filterProfanityFromText(message)

		if self.isMinimized():
			self.IS_FLASHING = True

		if channel==self.connections[serverid].nickname:
			channel = user

		for w in self.windows[serverid]:
			if w.window.name == channel:
				# Window exists

				if self.highlightNickMessages:
					d = action_display(user,message,self.urlsToLinks,ACTION_COLOR,True,HIGHLIGHT_COLOR,self.connections[serverid].nickname)
				else:
					d = action_display(user,message,self.urlsToLinks,ACTION_COLOR,False,HIGHLIGHT_COLOR,self.connections[serverid].nickname)

				self.writeToChatWindow(serverid,channel,d)
				self.notifyChatWindow(serverid,channel)
				return

		# Window doesn't exist, so create it
		chatWindow = Window.createNew(channel,self.connections[serverid],serverid,self.MDI,self)
		self.windows[serverid].append(chatWindow)
		chatWindow.window.show()

		# Write to it
		if self.highlightNickMessages:
			d = action_display(user,message,self.urlsToLinks,ACTION_COLOR,True,HIGHLIGHT_COLOR,self.connections[serverid].nickname)
		else:
			d = action_display(user,message,self.urlsToLinks,ACTION_COLOR,False,HIGHLIGHT_COLOR,self.connections[serverid].nickname)

		self.writeToChatWindow(serverid,channel,d)
		self.notifyChatWindow(serverid,channel)

	def userJoined(self,serverid,user,channel):

		p = user.split("!")
		duser = user
		if len(p)==2: duser = p[0]

		for w in self.windows[serverid]:
				if w.window.name == channel:
					d = systemTextDisplay(f"{duser} joined {channel}.",self.maxnicklen,SYSTEM_COLOR)
					self.writeToChatWindow(serverid,channel,d)
					self.writeToLog(d)
					w.window.addUser(user)

	def userParted(self,serverid,user,channel):

		p = user.split("!")
		if len(p)==2: user = p[0]

		for w in self.windows[serverid]:
				if w.window.name == channel:
					d = systemTextDisplay(f"{user} left {channel}.",self.maxnicklen,SYSTEM_COLOR)
					self.writeToChatWindow(serverid,channel,d)
					self.writeToLog(d)
					w.window.removeUser(user)

	def gotKicked(self,serverid,channel,kicker,message):

		# Close the channel window
		for w in self.windows[serverid]:
				if w.window.name == channel:
					w.window.kickClose()

		if message != "":
			d = systemTextDisplay(f"{kicker} kicked you from {channel} ({message}).",self.maxnicklen,SYSTEM_COLOR)
		else:
			d = systemTextDisplay(f"{kicker} kicked you from {channel}.",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)

	def userKicked(self,serverid,kickee,channel,kicker,message):

		# p = user.split("!")
		# if len(p)==2: user = p[0]

		for w in self.windows[serverid]:
				if w.window.name == channel:
					if message == "":
						d = systemTextDisplay(f"{kickee} was kicked from {channel} by {kicker}",self.maxnicklen,SYSTEM_COLOR)
					else:
						d = systemTextDisplay(f"{kickee} was kicked from {channel} by {kicker} ({message})",self.maxnicklen,SYSTEM_COLOR)
					self.writeToChatWindow(serverid,channel,d)
					self.writeToLog(d)
					w.window.removeUser(kickee)

	def setKey(self,serverid,channel,key):
		for w in self.windows[serverid]:
				if w.window.name == channel:
					w.window.key = key
					w.window.addModes("k")

	def unsetKey(self,serverid,channel):
		for w in self.windows[serverid]:
				if w.window.name == channel:
					w.window.key = ''
					w.window.removeModes("k")

	def gotBanlist(self,serverid,channel,banlist):
		for w in self.windows[serverid]:
				if w.window.name == channel:
					w.window.banlist = banlist
					w.window.rebuildBanMenu()

	def mode(self,serverid,user,channel,mset,modes,args):

		if len(modes)<1: return

		# self.toolbars[serverid].
		if channel == self.connections[serverid].nickname:
			m = self.toolbars[serverid].usermodes.text()
			m = m.replace(DEFAULT_USERMODE_DISPLAY,"")
			for ma in modes:
				if mset:
					if ma in m:
						pass
					else:
						m = m + ma
				else:
					if ma in m:
						m = m.replace(ma,'')
			if len(m)==0:
				m = DEFAULT_USERMODE_DISPLAY
			else:
				m = "+"+m

			self.toolbars[serverid].usermodes.setText(m)

		args = list(args)

		cleaned = []
		for a in args:
			if a == None: continue
			cleaned.append(a)
		args = cleaned

		p = user.split('!')
		if len(p)==2:
			user = p[0]

		reportadd = []
		reportremove = []

		changedUser = False

		for m in modes:

			if m=="k":
				if len(args)>0:
					n = args.pop(0)
				else:
					n = None
				if mset:
					if n:
						msg = f"{user} set {channel}'s channel key to \"{n}\""
						self.setKey(serverid,channel,n)
					else:
						msg = ''
				else:
					msg = f"{user} unset {channel}'s channel key"
					self.unsetKey(serverid,channel)
				if len(msg)>0:
					d = systemTextDisplay(msg,self.maxnicklen,SYSTEM_COLOR)
					self.writeToChatWindow(serverid,channel,d)
					self.writeToLog(d)
				continue

			if m=="o":
				if len(args)>0:
					n = args.pop(0)
				else:
					n = None
				if mset:
					if n:
						msg = f"{user} granted {channel} operator status to {n}"
					else:
						msg = ''
				else:
					if n:
						msg = f"{user} took {channel} operator status from {n}"
					else:
						msg = ''
				if len(msg)>0:
					d = systemTextDisplay(msg,self.maxnicklen,SYSTEM_COLOR)
					self.writeToChatWindow(serverid,channel,d)
					#self.connections[serverid].sendLine(f"NAMES {channel}")
					changedUser = True
					self.writeToLog(d)
				continue

			if m=="v":
				if len(args)>0:
					n = args.pop(0)
				else:
					n = None
				if mset:
					if n:
						msg = f"{user} granted {channel} voiced status to {n}"
					else:
						msg = ''
				else:
					if n:
						msg = f"{user} took {channel} voiced status from {n}"
					else:
						msg = ''
				if len(msg)>0:
					d = systemTextDisplay(msg,self.maxnicklen,SYSTEM_COLOR)
					self.writeToChatWindow(serverid,channel,d)
					#self.connections[serverid].sendLine(f"NAMES {channel}")
					changedUser = True
					self.writeToLog(d)
				continue

			if m=="c":
				for w in self.windows[serverid]:
					if w.window.name == channel:
						if mset:
							w.window.addModes("c")
							reportadd.append("c")
						else:
							w.window.removeModes("c")
							reportremove.append("c")
				continue

			if m=="C":
				for w in self.windows[serverid]:
					if w.window.name == channel:
						if mset:
							w.window.addModes("C")
							reportadd.append("C")
						else:
							w.window.removeModes("C")
							reportremove.append("C")
				continue

			if m=="m":
				for w in self.windows[serverid]:
					if w.window.name == channel:
						if mset:
							w.window.addModes("m")
							reportadd.append("m")
						else:
							w.window.removeModes("m")
							reportremove.append("m")
				continue

			if m=="n":
				for w in self.windows[serverid]:
					if w.window.name == channel:
						if mset:
							w.window.addModes("n")
							reportadd.append("n")
						else:
							w.window.removeModes("n")
							reportremove.append("n")
				continue

			if m=="p":
				for w in self.windows[serverid]:
					if w.window.name == channel:
						if mset:
							w.window.addModes("p")
							reportadd.append("p")
						else:
							w.window.removeModes("p")
							reportremove.append("p")
				continue

			if m=="s":
				for w in self.windows[serverid]:
					if w.window.name == channel:
						if mset:
							w.window.addModes("s")
							reportadd.append("s")
						else:
							w.window.removeModes("s")
							reportremove.append("s")
				continue

			if m=="t":
				for w in self.windows[serverid]:
					if w.window.name == channel:
						if mset:
							w.window.addModes("t")
							reportadd.append("t")
						else:
							w.window.removeModes("t")
							reportremove.append("t")
				continue

			if m=="b":
				if mset:
					for u in args:
						d = systemTextDisplay(f"{user} banned {u} from {channel}",self.maxnicklen,SYSTEM_COLOR)
						self.writeToChatWindow(serverid,channel,d)
						self.writeToLog(d)
				else:
					for u in args:
						d = systemTextDisplay(f"{user} unbanned {u} from {channel}",self.maxnicklen,SYSTEM_COLOR)
						self.writeToChatWindow(serverid,channel,d)
						self.writeToLog(d)
				continue

			if mset:
				reportadd.append(m)
			else:
				reportremove.append(m)

		if len(reportadd)>0 or len(reportremove)>0:
			if mset:
				d = systemTextDisplay(f"{user} set +{''.join(reportadd)} in {channel}",self.maxnicklen,SYSTEM_COLOR)
				self.writeToChatWindow(serverid,channel,d)
			else:
				d = systemTextDisplay(f"{user} set -{''.join(reportremove)} in {channel}",self.maxnicklen,SYSTEM_COLOR)
				self.writeToChatWindow(serverid,channel,d)
			self.writeToLog(d)

		if changedUser: self.connections[serverid].sendLine(f"NAMES {channel}")

	def ircQuit(self,serverid,user,message):

		p = user.split("!")
		if len(p)==2: user = p[0]

		found = []
		inchannel = False
		for w in self.connections:
			if w != serverid: continue
			for x in self.windows[w]:
				items = x.window.channelUserDisplay.findItems(f"*{user}",Qt.MatchWildcard)

				if len(items) > 0:
					found.append(x.name)
					inchannel = True

				if inchannel:
					self.connections[serverid].sendLine(f"NAMES {x.name}")
					inchannel = False


		if message!='':
			d = systemTextDisplay(f"{user} quit IRC ({message}).",self.maxnicklen,SYSTEM_COLOR)
		else:
			d = systemTextDisplay(f"{user} quit IRC.",self.maxnicklen,SYSTEM_COLOR)

		for chan in found:
			self.writeToChatWindow(serverid,chan,d)
		self.writeToLog(d)

	def removeTitleTopic(self):
		for s in self.connections:
			for w in self.windows[s]:
				w.window.setWindowTitle(f" {w.window.name}")

	def restoreTitleTopic(self):
		for s in self.connections:
			for w in self.windows[s]:
				if w.window.topic != '':
					w.window.setWindowTitle(f" {w.window.name} - {w.window.topic}")
				else:
					w.window.setWindowTitle(f" {w.window.name}")

	def topic(self,serverid,user,channel,topic):

		p = user.split('!')
		if len(p)--2: user = p[0]
		
		for w in self.windows[serverid]:
			if w.window.name == channel:
				w.window.topic = topic
				if topic != '':
					if self.topicInTitle:
						w.window.setWindowTitle(f" {w.window.name} - {topic}")
					else:
						w.window.setWindowTitle(f" {w.window.name}")
					d = systemTextDisplay(f"{user} set the channel topic to \"{topic}\".",self.maxnicklen,SYSTEM_COLOR)
				else:
					w.window.setWindowTitle(f" {w.window.name}")
					d = systemTextDisplay(f"{user} set the channel topic to nothing.",self.maxnicklen,SYSTEM_COLOR)
				self.writeToChatWindow(serverid,channel,d)

		# Make sure the app title is updated if necessary
		self.updateActiveChild(self.MDI.activeSubWindow())

	def invite(self,serverid,user,channel):

		p = user.split('!')
		if len(p)--2: user = p[0]

		d = systemTextDisplay(f"{user} invited you to {channel}.",self.maxnicklen,SYSTEM_COLOR)
		self.writeToAll(serverid,d)
		self.writeToLog(d)

		if self.joinInvite: self.connections[serverid].join(channel)

	def inviting(self,serverid,user,channel):

		p = user.split('!')
		if len(p)--2: user = p[0]

		d = systemTextDisplay(f"Invitation to {channel} sent to {user}.",self.maxnicklen,SYSTEM_COLOR)
		self.writeToLog(d)

	def whois(self,serverid,data):

		d = makeWhoisPretty(data)
		d = whois_display(d,self.maxnicklen,SYSTEM_COLOR)
		self.printToActiveWindow(d)

	def whowas(self,serverid,data):

		d = makeWhowasPretty(data)
		d = whowas_display(d,self.maxnicklen,SYSTEM_COLOR)
		self.printToActiveWindow(d)

	def motd(self,serverid,motd):

		# def motd_display(text,max,dolink,namecolor,foreground,background):
		motd = "<br>".join(motd)
		d = motd_display(motd,self.maxnicklen,self.urlsToLinks,SYSTEM_COLOR)
		self.writeToLog(d)

	def irc_raw(self,serverid,line):
		pass

	def channelListStart(self,serverid):
		self.createChannelListWindow(serverid)

	def channelListEnd(self,serverid):
		pass

	def channelListEntry(self,serverid,channel,usercount,topic):
		for e in self.channel_list_windows:
			if e[2]==serverid:
				e[1].addChannel(channel,usercount,topic)

	def channelListClickJoin(self,serverid,channel):
		if serverid in self.connections:
			self.connections[serverid].join(channel)


	def ircerror(self,serverid,text):
		serverhost = self.connections[serverid].hostname
		if serverhost:
			d = systemTextDisplay(f"{serverhost}: {text}",self.maxnicklen,ERROR_COLOR)
			self.printToActiveWindow(d)
			self.writeToLog(d)

	def executeMenuClick(self,pclass):
		pass


	def serveroptions(self,serverid,options):

		# Options are sent in chunks: not every option
		# will be set in each chunk

		supports = []
		maxchannels = 0
		maxnicklen = 0
		nicklen = 0
		channellen = 0
		topiclen = 0
		kicklen = 0
		awaylen = 0
		maxtargets = 0
		modes = 0
		maxmodes = []
		chanmodes = []
		prefix = []
		cmds = []
		network = ""
		casemapping = "none"

		for o in options:
			if "=" in o:
				p = o.split("=")
				if len(p)>1:
					if p[0].lower() == "maxchannels": maxchannels = int(p[1])
					if p[0].lower() == "maxnicklen": maxnicklen = int(p[1])
					if p[0].lower() == "nicklen": nicklen = int(p[1])
					if p[0].lower() == "channellen": channellen = int(p[1])
					if p[0].lower() == "topiclen": topiclen = int(p[1])
					if p[0].lower() == "kicklen": kicklen = int(p[1])
					if p[0].lower() == "awaylen": awaylen = int(p[1])
					if p[0].lower() == "maxtargets": maxtargets = int(p[1])
					if p[0].lower() == "modes": modes = int(p[1])
					if p[0].lower() == "network": network = p[1]
					if p[0].lower() == "casemapping": casemapping = p[1]

					if p[0].lower() == "cmds":
						for c in p[1].split(","):
							cmds.append(c)

					if p[0].lower() == "prefix":
						pl = p[1].split(")")
						if len(pl)>=2:
							pl[0] = pl[0][1:]	# get rid of prefixed (

							for i in range(len(pl[0])):
								entry = [ pl[0][i], pl[1][i] ]
								prefix.append(entry)

					if p[0].lower() == "chanmodes":
						for e in p[1].split(","):
							chanmodes.append(e)

					if p[0].lower() == "maxlist":
						for e in p[1].split(","):
							ml = e.split(':')
							if len(ml)==2:
								entry = [ml[0],int(ml[1])]
								maxmodes.append(entry)
			else:
				supports.append(o)

		if len(maxmodes)>0: self.connections[serverid].maxmodes = maxmodes

		if maxnicklen>0:
			if maxnicklen > MAX_SERVER_NICKNAME_SIZE: maxnicklen = MAX_SERVER_NICKNAME_SIZE
			if maxnicklen < self.maxnicklen:
				return
			self.maxnicklen = maxnicklen
			self.connections[serverid].maxnicklen = maxnicklen

		if network != "":
			servhost = self.connections[serverid].hostname
			self.connections[serverid].network = network

			# If the client is set to save connected servers,
			# update the server file
			if self.saveServers:

				# Don't update servers with a password
				if self.connections[serverid].password != '': return

				# Update the IRC network file with the network name
				# of the current connection
				if os.path.isfile(SAVED_SERVERS_FILE):
					changed = False
					script = open(SAVED_SERVERS_FILE,"r")
					netlist = []
					for line in script:
						x = line.split(":")
						if len(x) != 4: continue
						x[0].strip()	# host
						x[1].strip()	# port
						x[2].strip()	# network
						x[3].strip()	# "ssl" or "normal"

						if self.connections[serverid].host == x[0]:
							if self.connections[serverid].port == int(x[1]):
								if x[2] != UNKNOWN_NETWORK:
									break
								line = line.replace(x[2],network)
								changed = True
						#line.strip()
						netlist.append(line)
					script.close()

					if changed:
						# Write the new network list to file
						script = open(SAVED_SERVERS_FILE,"w")
						script.write("".join(netlist))
						script.close()

		if maxchannels > 0: self.connections[serverid].maxchannels = maxchannels
		if channellen > 0: self.connections[serverid].channellen = channellen
		if topiclen > 0: self.connections[serverid].topiclen = topiclen
		if kicklen > 0: self.connections[serverid].kicklen = kicklen
		if awaylen > 0: self.connections[serverid].awaylen = awaylen
		if maxtargets > 0: self.connections[serverid].maxtargets = maxtargets
		if modes > 0: self.connections[serverid].modes = modes

		if casemapping != "": self.connections[serverid].casemapping = casemapping

		if len(cmds)>0:
			for c in cmds:
				self.connections[serverid].cmds.append(c)
		if len(prefix)>0: self.connections[serverid].prefix = prefix
		if len(chanmodes)>0: self.connections[serverid].chanmodes = chanmodes
		if len(supports)>0:
			for s in supports:
				self.connections[serverid].supports.append(s)

		self.rebuildServerInfoMenu(serverid)


