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

import os

from ..resources import *
from ..files import *
from .. import config
from .. import events
from .. import userinput
from .. import plugins

from .prefix import Dialog as Prefix
from .history_size import Dialog as HistorySize
from .format import Dialog as FormatText
from .list_time import Dialog as ListTime
from .quitpart import Dialog as QuitPart
from .autosave_freq import Dialog as Autosave
from .log_size import Dialog as LogSize
from .cursor_width import Dialog as CursorWidth

class Dialog(QDialog):

	def setPrefix(self):
		x = Prefix()
		info = x.get_system_information()
		del x

		if not info: return
		self.systemPrefix = info
		self.do_rerender = True

		self.prefDisplay.setText("Prefix: <b>"+self.systemPrefix+"</b>")

	def setHistory(self):
		x = HistorySize()
		info = x.get_entry_information()
		del x

		if not info: return
		self.historySize = info

		self.historyLabel.setText("Command history: <b>"+str(self.historySize)+" lines</b>")

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

			self.fontLabel.setText(f"Font: <b>{font_name}, {font_size} pt</b>")

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

		self.listFreq.setText("Refresh list every <b>"+str(self.configRefresh)+"</b> seconds")


	def setSaveFreq(self):

		x = Autosave()
		f = x.get_entry_information()
		if f:
			self.autosave_time = f
			self.autoLogLabel.setText("Autosave logs every <b>"+str(self.autosave_time)+"</b> seconds")


	def setLogSize(self):
		x = LogSize()
		info = x.get_entry_information()
		if info:
			self.logDisplayLines = info
			self.logSizeLabel.setText("Load <b>"+str(self.logDisplayLines)+"</b> lines for display")

	def closeEvent(self, event):

		if self.app != None:
			self.app.quit()

		event.accept()
		self.close()

	def backgroundColor(self):
		newcolor = QColorDialog.getColor(QColor(self.connection_background_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.connection_background_color = ncolor
			self.setBg.setStyleSheet(f'background-color: {ncolor};')

			self.bgLabel.setText("Background color: <b>"+ncolor+"</b>")

	def textColor(self):
		newcolor = QColorDialog.getColor(QColor(self.connection_text_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.connection_text_color = ncolor
			self.setFg.setStyleSheet(f'background-color: {ncolor};')

			self.fgLabel.setText("Text color: <b>"+ncolor+"</b>")

	def syntaxBackground(self):
		newcolor = QColorDialog.getColor(QColor(self.syntax_background_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.syntax_background_color = ncolor
			self.setSyntaxBg.setStyleSheet(f'background-color: {ncolor};')

			self.syntaxBgLabel.setText("Background color: <b>"+ncolor+"</b>")

	def syntaxText(self):
		newcolor = QColorDialog.getColor(QColor(self.syntax_text_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.syntax_text_color = ncolor
			self.setSyntaxFg.setStyleSheet(f'background-color: {ncolor};')

			self.syntaxFgLabel.setText("Text color: <b>"+ncolor+"</b>")

	def syntaxComment(self):
		newcolor = QColorDialog.getColor(QColor(self.syntax_comment_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.syntax_comment_color = ncolor
			self.setSyntaxComment.setStyleSheet(f'background-color: {ncolor};')

			self.syntaxCommentLabel.setText("Comments: <b>"+ncolor+"</b>")

	def syntaxCommand(self):
		newcolor = QColorDialog.getColor(QColor(self.syntax_command_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.syntax_command_color = ncolor
			self.setSyntaxCommand.setStyleSheet(f'background-color: {ncolor};')

			self.syntaxCommandLabel.setText("Commands: <b>"+ncolor+"</b>")

	def syntaxTarget(self):
		newcolor = QColorDialog.getColor(QColor(self.syntax_target_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.syntax_target_color = ncolor
			self.setSyntaxTarget.setStyleSheet(f'background-color: {ncolor};')

			self.syntaxTargetLabel.setText("Channels: <b>"+ncolor+"</b>")

	def syntaxAlias(self):
		newcolor = QColorDialog.getColor(QColor(self.syntax_alias_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.syntax_alias_color = ncolor
			self.setSyntaxAlias.setStyleSheet(f'background-color: {ncolor};')

			self.syntaxAliasLabel.setText("Aliases: <b>"+ncolor+"</b>")

	def unseenColor(self):
		newcolor = QColorDialog.getColor(QColor(self.unseen_message_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.unseen_message_color = ncolor
			self.setUnseen.setStyleSheet(f'background-color: {ncolor};')

			self.unseenLabel.setText("Unseen messages color: <b>"+ncolor+"</b>")

	def connectingColor(self):
		newcolor = QColorDialog.getColor(QColor(self.connecting_anim_color))

		if newcolor.isValid():
			ncolor = newcolor.name()
			self.connecting_anim_color = ncolor
			self.setConnecting.setStyleSheet(f'background-color: {ncolor};')

			self.connectingLabel.setText("Connecting color: <b>"+ncolor+"</b>")

	def setLogSize(self):
		x = CursorWidth()
		info = x.get_entry_information()
		if info:
			self.cursor_width = info
			if self.cursor_width>1:
				self.cursorWidthLabel.setText("Cursor width: <b>"+str(self.cursor_width)+" pixels</b>")
			else:
				self.cursorWidthLabel.setText("Cursor width: <b>"+str(self.cursor_width)+" pixel</b>")


	def __init__(self,configfile=USER_FILE,parent=None,app=None,opento=None):
		super(Dialog,self).__init__(parent)

		self.config = configfile
		self.parent = parent
		self.app = app
		self.saved = False
		self.opento = opento

		self.newfont = None

		self.logDisplayLines = config.LOG_LOAD_SIZE_MAX

		self.autosave_time = config.AUTOSAVE_LOG_TIME

		self.systemPrefix = config.SYSTEM_MESSAGE_PREFIX
		self.configRefresh = config.CHANNEL_LIST_REFRESH_FREQUENCY

		self.default_quit_part = config.DEFAULT_QUIT_PART_MESSAGE

		self.do_rerender = False

		self.setWindowTitle("Preferences")
		self.setWindowIcon(QIcon(SETTINGS_ICON))

		if self.parent==None:
			if self.config!=SETTINGS_FILE:
				self.setWindowTitle("Editing "+os.path.basename(self.config))
			else:
				self.setWindowTitle(APPLICATION_NAME+" Preferences")


		self.selector = QListWidget(self)
		self.stack = QStackedWidget(self)

		fm = QFontMetrics(self.font())
		fwidth = fm.width('X') * 27
		self.selector.setMaximumWidth(fwidth)

		self.selector.itemClicked.connect(self.selectorClick)

		self.selector.setStyleSheet("background-color: transparent; border-width: 0px; border-color: transparent;")

		# Display page

		self.displayPage = QWidget()
		self.menuPage = QWidget()

		self.displayTabs = QTabWidget()

		self.displayTabs.addTab(self.displayPage, QIcon(WINDOW_ICON), "Application")
		self.displayTabs.addTab(self.menuPage, QIcon(MENU_ICON), "Menu")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Application")
		entry.widget = self.displayTabs
		entry.setIcon(QIcon(WINDOW_ICON))
		self.selector.addItem(entry)
		self.selector.setCurrentItem(entry)

		self.stack.addWidget(self.displayTabs)
		self.stack.setCurrentWidget(self.displayTabs)

		f = self.font()
		fs = f.toString()
		pfs = fs.split(',')
		font_name = pfs[0]
		font_size = pfs[1]

		self.fontLabel = QLabel(f"Font: <b>{font_name}, {font_size} pt</b>",self)

		fontButton = QPushButton("")
		fontButton.clicked.connect(self.menuFont)
		fontButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		fontButton.setFixedSize(fheight +10,fheight + 10)
		fontButton.setIcon(QIcon(EDIT_ICON))
		fontButton.setToolTip("Change font")

		formatButton = QPushButton("Style Editor")
		formatButton.clicked.connect(self.menuFormat)
		formatButton.setAutoDefault(False)

		if self.parent!= None:
			if self.parent.block_styles: formatButton.setVisible(False)

		self.nametitleMisc = QCheckBox("Show chat name in title",self)
		if config.APP_TITLE_TO_CURRENT_CHAT: self.nametitleMisc.setChecked(True)

		self.topicMisc = QCheckBox("Show channel topic in title",self)
		if config.APP_TITLE_SHOW_TOPIC: self.topicMisc.setChecked(True)

		self.askMisc = QCheckBox("Ask before quitting",self)
		if config.ASK_BEFORE_QUIT: self.askMisc.setChecked(True)

		fbLay = QHBoxLayout()
		fbLay.addWidget(fontButton)
		fbLay.addWidget(self.fontLabel)
		fbLay.addStretch()

		self.lostErrors = QCheckBox("Show connection lost errors",self)
		if config.SHOW_CONNECTION_LOST_ERROR: self.lostErrors.setChecked(True)

		self.failErrors = QCheckBox("Show connection fail errors",self)
		if config.SHOW_CONNECTION_FAIL_ERROR: self.failErrors.setChecked(True)

		self.showSchwa = QCheckBox("Animated menu bar logo",self)
		if config.SCHWA_ANIMATION: self.showSchwa.setChecked(True)

		self.showMenu = QCheckBox("Moveable menu bar",self)
		if config.MENU_BAR_MOVABLE: self.showMenu.setChecked(True)

		if self.parent==None:
			self.menuMisc = QCheckBox("Use Qt menus rather than a menu bar",self)
		else:
			self.menuMisc = QCheckBox("Use Qt menus rather than a menu bar\n(requires a restart to take effect)",self)
		if config.USE_QMENUBAR_MENUS: self.menuMisc.setChecked(True)

		self.menuMisc.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		if self.parent!= None:
			if self.parent.force_qmenu:
				self.menuMisc.setEnabled(False)
				self.showSchwa.setEnabled(False)
				self.showMenu.setEnabled(False)

		if config.USE_QMENUBAR_MENUS:
			self.showSchwa.setEnabled(False)
			self.showMenu.setEnabled(False)

		mpLayout = QVBoxLayout()
		mpLayout.addLayout(fbLay)
		mpLayout.addWidget(self.nametitleMisc)
		mpLayout.addWidget(self.topicMisc)
		mpLayout.addWidget(self.askMisc)
		mpLayout.addWidget(self.lostErrors)
		mpLayout.addWidget(self.failErrors)
		mpLayout.addStretch()

		menuPageLayout = QVBoxLayout()
		menuPageLayout.addWidget(self.menuMisc)
		menuPageLayout.addWidget(self.showMenu)
		menuPageLayout.addWidget(self.showSchwa)
		menuPageLayout.addStretch()

		self.menuPage.setLayout(menuPageLayout)

		self.displayPage.setLayout(mpLayout)

		# Message settings page

		self.messagesPage = QWidget()
		self.systemMessPage = QWidget()
		self.timestampPage = QWidget()

		self.messagesTabs = QTabWidget()

		self.messagesTabs.addTab(self.messagesPage, QIcon(MESSAGE_ICON), "Messages")
		self.messagesTabs.addTab(self.systemMessPage, QIcon(MISC_ICON), "System")
		self.messagesTabs.addTab(self.timestampPage, QIcon(CLOCK_ICON), "Timestamps")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Messages")
		entry.widget = self.messagesTabs
		entry.setIcon(QIcon(MESSAGE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.messagesTabs)

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

		self.channelLinks = QCheckBox("Convert channel names to links",self)
		if config.CLICKABLE_CHANNELS: self.channelLinks.setChecked(True)
		self.channelLinks.stateChanged.connect(self.setRerender)

		self.writeNotice = QCheckBox("Write all notices to console",self)
		if config.WRITE_NOTICE_TO_CONSOLE: self.writeNotice.setChecked(True)

		self.writePrivate = QCheckBox("Write all private messages to console",self)
		if config.WRITE_PRIVATE_TO_CONSOLE: self.writePrivate.setChecked(True)

		self.addPrefixes = QCheckBox("Add prefix to system messages",self)
		if config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL: self.addPrefixes.setChecked(True)
		self.addPrefixes.stateChanged.connect(self.setRerender)

		prefixButton = QPushButton("")
		prefixButton.clicked.connect(self.setPrefix)
		prefixButton.setAutoDefault(False)

		self.prefDisplay = QLabel("Prefix: <b>"+config.SYSTEM_MESSAGE_PREFIX+"</b>")

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		prefixButton.setFixedSize(fheight +10,fheight + 10)
		prefixButton.setIcon(QIcon(EDIT_ICON))
		prefixButton.setToolTip("Set prefix")

		psLayout = QHBoxLayout()
		psLayout.addWidget(prefixButton)
		psLayout.addWidget(self.prefDisplay)
		psLayout.addStretch()

		tsLay = QVBoxLayout()
		tsLay.addWidget(self.addPrefixes)
		tsLay.addLayout(psLayout)
		tsLay.addStretch()

		self.enabledTimestamp = QCheckBox("Enabled",self)
		if config.DISPLAY_TIMESTAMP: self.enabledTimestamp.setChecked(True)
		self.enabledTimestamp.stateChanged.connect(self.setRerender)

		self.twentyfourTimestamp = QCheckBox("Use 24-hour clock",self)
		if config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS: self.twentyfourTimestamp.setChecked(True)
		self.twentyfourTimestamp.stateChanged.connect(self.setRerender)

		self.secondsTimestamp = QCheckBox("Display seconds",self)
		if config.DISPLAY_TIMESTAMP_SECONDS: self.secondsTimestamp.setChecked(True)
		self.secondsTimestamp.stateChanged.connect(self.setRerender)

		tsBoxLayout = QVBoxLayout()
		tsBoxLayout.addWidget(self.enabledTimestamp)
		tsBoxLayout.addWidget(self.twentyfourTimestamp)
		tsBoxLayout.addWidget(self.secondsTimestamp)
		tsBoxLayout.addStretch()

		mpLayout = QVBoxLayout()
		mpLayout.addWidget(self.showDates)
		mpLayout.addWidget(self.showColors)
		mpLayout.addWidget(self.showLinks)
		mpLayout.addWidget(self.hideProfanity)
		mpLayout.addWidget(self.channelLinks)
		mpLayout.addWidget(self.writePrivate)
		mpLayout.addWidget(self.writeNotice)
		mpLayout.addStretch()

		self.timestampPage.setLayout(tsBoxLayout)

		self.systemMessPage.setLayout(tsLay)

		self.messagesPage.setLayout(mpLayout)

		# HIDE NOTIFICATIONS PAGE

		self.notificationsPage = QWidget()
		self.hidePage = QWidget()

		self.notificationsTabs = QTabWidget()

		self.notificationsTabs.addTab(self.notificationsPage, QIcon(HIDE_ICON), "Ignore")
		self.notificationsTabs.addTab(self.hidePage, QIcon(HIDE_ICON), "Hide")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Hide & Ignore")
		entry.widget = self.notificationsTabs
		entry.setIcon(QIcon(HIDE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.notificationsTabs)

		self.noteIgnore = QCheckBox("Enabled",self)
		if config.ENABLE_IGNORE: self.noteIgnore.setChecked(True)

		self.notePublic = QCheckBox("Ignore public messages",self)
		if config.IGNORE_PUBLIC: self.notePublic.setChecked(True)

		self.notePrivate = QCheckBox("Ignore private messages",self)
		if config.IGNORE_PRIVATE: self.notePrivate.setChecked(True)

		self.noteNotice = QCheckBox("Ignore notice messages",self)
		if config.IGNORE_NOTICE: self.noteNotice.setChecked(True)

		c1 = QVBoxLayout()
		c1.addWidget(self.noteIgnore)
		c1.addWidget(self.notePublic)
		c1.addWidget(self.notePrivate)
		c1.addWidget(self.noteNotice)
		c1.addStretch()


		self.noteJoin = QCheckBox("JOIN messages",self)
		if config.HIDE_JOIN_MESSAGE: self.noteJoin.setChecked(True)
		self.noteJoin.stateChanged.connect(self.setRerender)

		self.notePart = QCheckBox("PART messages",self)
		if config.HIDE_PART_MESSAGE: self.notePart.setChecked(True)
		self.notePart.stateChanged.connect(self.setRerender)

		self.noteInvite = QCheckBox("INVITE messages",self)
		if config.HIDE_INVITE_MESSAGE: self.noteInvite.setChecked(True)
		self.noteInvite.stateChanged.connect(self.setRerender)

		self.noteNick = QCheckBox("NICK messages",self)
		if config.HIDE_NICK_MESSAGE: self.noteNick.setChecked(True)
		self.noteNick.stateChanged.connect(self.setRerender)

		self.noteQuit = QCheckBox("QUIT messages",self)
		if config.HIDE_QUIT_MESSAGE: self.noteQuit.setChecked(True)
		self.noteQuit.stateChanged.connect(self.setRerender)

		self.noteTopic = QCheckBox("TOPIC messages",self)
		if config.HIDE_TOPIC_MESSAGE: self.noteTopic.setChecked(True)
		self.noteTopic.stateChanged.connect(self.setRerender)

		self.noteMode = QCheckBox("MODE messages",self)
		if config.HIDE_MODE_DISPLAY: self.noteMode.setChecked(True)
		self.noteMode.stateChanged.connect(self.setRerender)

		hc1 = QVBoxLayout()
		hc1.addWidget(self.noteJoin)
		hc1.addWidget(self.notePart)
		hc1.addWidget(self.noteInvite)
		hc1.addWidget(self.noteNick)
		hc1.addWidget(self.noteQuit)
		hc1.addWidget(self.noteTopic)
		hc1.addWidget(self.noteMode)
		hc1.addStretch()

		self.hidePage.setLayout(hc1)

		self.notificationsPage.setLayout(c1)

		# LOGS PAGE

		self.logsPage = QWidget()
		self.loadPage = QWidget()

		self.logsTabs = QTabWidget()

		self.logsTabs.addTab(self.logsPage, QIcon(EXPORT_ICON), "Save")
		self.logsTabs.addTab(self.loadPage, QIcon(LOG_ICON), "Load")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Logs")
		entry.widget = self.logsTabs
		entry.setIcon(QIcon(LOG_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.logsTabs)

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

		self.autoLog = QCheckBox("",self)
		self.autoLogLabel = QLabel("Autosave logs every <b>"+str(config.AUTOSAVE_LOG_TIME)+"</b> seconds")
		if config.AUTOSAVE_LOGS: self.autoLog.setChecked(True)

		self.servSaveLog = QCheckBox("Save server logs",self)
		if config.SAVE_SERVER_LOGS: self.servSaveLog.setChecked(True)

		self.servLoadLog = QCheckBox("Load server logs",self)
		if config.LOAD_SERVER_LOGS: self.servLoadLog.setChecked(True)

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
		slLayout.addWidget(self.servSaveLog)
		slLayout.addLayout(ltLayout)
		slLayout.addStretch()

		loadLoglay = QVBoxLayout()
		loadLoglay.addWidget(self.chanloadLog)
		loadLoglay.addWidget(self.privloadLog)
		loadLoglay.addWidget(self.servLoadLog)
		loadLoglay.addWidget(self.markLog)
		loadLoglay.addWidget(self.resumeLog)
		loadLoglay.addLayout(llLayout)
		loadLoglay.addStretch()

		if self.parent!=None:
			if self.parent.block_logs:
				self.autoLog.setEnabled(False)
				self.autoLogLabel.setEnabled(False)
				self.hsButton.setEnabled(False)
				self.slsButton.setEnabled(False)
				self.logSizeLabel.setEnabled(False)
				self.chansaveLog.setEnabled(False)
				self.privsaveLog.setEnabled(False)
				self.servSaveLog.setEnabled(False)
				self.chanloadLog.setEnabled(False)
				self.privloadLog.setEnabled(False)
				self.servLoadLog.setEnabled(False)
				self.markLog.setEnabled(False)
				self.resumeLog.setEnabled(False)

			if self.parent.block_load:
				self.chanloadLog.setEnabled(False)
				self.privloadLog.setEnabled(False)
				self.servLoadLog.setEnabled(False)
				self.markLog.setEnabled(False)
				self.resumeLog.setEnabled(False)
				self.slsButton.setEnabled(False)
				self.logSizeLabel.setEnabled(False)

			if self.parent.block_write:
				self.chansaveLog.setEnabled(False)
				self.privsaveLog.setEnabled(False)
				self.servSaveLog.setEnabled(False)
				self.autoLog.setEnabled(False)
				self.autoLogLabel.setEnabled(False)
				self.hsButton.setEnabled(False)



		self.loadPage.setLayout(loadLoglay)

		self.logsPage.setLayout(slLayout)

		# LOGS PAGE

		# Channel settings

		self.channelPage = QWidget()
		self.nickPage = QWidget()
		self.infoPage = QWidget()

		self.channelTabs = QTabWidget()

		self.channelTabs.addTab(self.channelPage, QIcon(CHATS_ICON), "Chats")
		self.channelTabs.addTab(self.infoPage, QIcon(CHANNEL_ICON), "Channel")
		self.channelTabs.addTab(self.nickPage, QIcon(NICK_ICON), "Nick Display")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Chats")
		entry.widget = self.channelTabs
		entry.setIcon(QIcon(CHATS_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.channelTabs)

		self.channelInfo = QCheckBox("Show name && topic",self)
		if config.CHAT_DISPLAY_INFO_BAR: self.channelInfo.setChecked(True)

		self.channelModes = QCheckBox("Show modes",self)
		if config.DISPLAY_CHANNEL_MODES: self.channelModes.setChecked(True)

		self.textUserlist = QCheckBox("Text-only user list",self)
		if config.PLAIN_USER_LISTS: self.textUserlist.setChecked(True)

		self.displayUserlists = QCheckBox("Display user list",self)
		if config.DISPLAY_USER_LIST: self.displayUserlists.setChecked(True)

		self.displayStatus = QCheckBox("Display channel status",self)
		if config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY: self.displayStatus.setChecked(True)

		self.displayNickname = QCheckBox("Display nickname",self)
		if config.DISPLAY_NICKNAME_ON_CHANNEL: self.displayNickname.setChecked(True)

		self.displayChange = QCheckBox("Double-click nickname to change nickname",self)
		if config.DOUBLECLICK_TO_CHANGE_NICK: self.displayChange.setChecked(True)

		self.channelLatest = QCheckBox("Display latest messages on chat switch",self)
		if config.SCROLL_CHAT_TO_BOTTOM: self.channelLatest.setChecked(True)

		self.openNew = QCheckBox("Open new chat for private messages",self)
		if config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS: self.openNew.setChecked(True)

		self.channelTopic = QCheckBox("Enable topic editor",self)
		if config.ENABLE_TOPIC_EDITOR: self.channelTopic.setChecked(True)

		self.channelUserMenu = QCheckBox("Enable user list context menu",self)
		if config.ENABLE_USERLIST_MENU: self.channelUserMenu.setChecked(True)

		self.displayUserModes = QCheckBox("Display user modes",self)
		if config.DISPLAY_MODES_ON_CHANNEL: self.displayUserModes.setChecked(True)

		self.cursor_width = config.CURSOR_WIDTH

		if self.cursor_width>1:
			self.cursorWidthLabel = QLabel("Cursor width: <b>"+str(config.CURSOR_WIDTH)+" pixels</b>")
		else:
			self.cursorWidthLabel = QLabel("Cursor width: <b>"+str(config.CURSOR_WIDTH)+" pixel</b>")

		self.cursorWidthButton = QPushButton("")
		self.cursorWidthButton.clicked.connect(self.setLogSize)
		self.cursorWidthButton.setAutoDefault(False)

		self.cursorWidthButton.setFixedSize(fheight +10,fheight + 10)
		self.cursorWidthButton.setIcon(QIcon(EDIT_ICON))
		self.cursorWidthButton.setToolTip("Set cursor width")

		cursorWidthLayout = QHBoxLayout()
		cursorWidthLayout.addWidget(self.cursorWidthButton)
		cursorWidthLayout.addWidget(self.cursorWidthLabel)
		cursorWidthLayout.addStretch()

		nnbLay = QVBoxLayout()
		nnbLay.addWidget(self.displayNickname)
		nnbLay.addWidget(self.displayUserModes)
		nnbLay.addWidget(self.displayStatus)
		nnbLay.addWidget(self.displayChange)
		nnbLay.addStretch()

		cbLay = QVBoxLayout()
		cbLay.addWidget(self.channelInfo)
		cbLay.addWidget(self.channelModes)
		cbLay.addWidget(self.channelTopic)
		cbLay.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.displayUserlists)
		cpLayout.addWidget(self.textUserlist)
		cpLayout.addWidget(self.channelUserMenu)
		cpLayout.addWidget(self.channelLatest)
		cpLayout.addWidget(self.openNew)
		cpLayout.addLayout(cursorWidthLayout)
		cpLayout.addStretch()

		self.infoPage.setLayout(cbLay)

		self.nickPage.setLayout(nnbLay)

		self.channelPage.setLayout(cpLayout)

		# Connection display settings

		self.connectionPage = QWidget()
		self.customConnectionPage = QWidget()

		self.connectionTabs = QTabWidget()

		self.connectionTabs.addTab(self.connectionPage, QIcon(CONNECTION_DISPLAY_ICON), "Connection Display")
		self.connectionTabs.addTab(self.customConnectionPage, QIcon(FORMAT_ICON), "Appearance")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Connection Display")
		entry.widget = self.connectionTabs
		entry.setIcon(QIcon(CONNECTION_DISPLAY_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.connectionTabs)

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

		self.menuConnection = QCheckBox("Enable context menu",self)
		if config.ENABLE_CONNECTION_CONTEXT: self.menuConnection.setChecked(True)

		self.leftRadio = QRadioButton("Left")
		self.rightRadio = QRadioButton("Right")

		if config.CONNECTION_DISPLAY_LOCATION=="left": self.leftRadio.setChecked(True)
		if config.CONNECTION_DISPLAY_LOCATION=="right": self.rightRadio.setChecked(True)

		self.connection_background_color = config.CONNECTION_DISPLAY_BG_COLOR
		self.connection_text_color = config.CONNECTION_DISPLAY_TEXT_COLOR

		self.setBg = QPushButton("")
		self.setBg.clicked.connect(self.backgroundColor)
		self.setBg.setStyleSheet(f'background-color: {config.CONNECTION_DISPLAY_BG_COLOR};')

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setBg.setFixedSize(fheight +10,fheight + 10)

		self.bgLabel = QLabel("Background color: <b>"+config.CONNECTION_DISPLAY_BG_COLOR+"</b>")

		bgColorLayout = QHBoxLayout()
		bgColorLayout.addWidget(self.setBg)
		bgColorLayout.addWidget(self.bgLabel)

		self.setFg = QPushButton("")
		self.setFg.clicked.connect(self.textColor)
		self.setFg.setStyleSheet(f'background-color: {config.CONNECTION_DISPLAY_TEXT_COLOR};')

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setFg.setFixedSize(fheight +10,fheight + 10)

		self.fgLabel = QLabel("Text color: <b>"+config.CONNECTION_DISPLAY_TEXT_COLOR+"</b>")

		fgColorLayout = QHBoxLayout()
		fgColorLayout.addWidget(self.setFg)
		fgColorLayout.addWidget(self.fgLabel)

		self.unseen_message_color = config.UNSEEN_MESSAGE_COLOR
		self.connecting_anim_color = config.CONNECTING_ANIMATION_COLOR

		self.setUnseen = QPushButton("")
		self.setUnseen.clicked.connect(self.unseenColor)
		self.setUnseen.setStyleSheet(f'background-color: {config.UNSEEN_MESSAGE_COLOR};')

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setUnseen.setFixedSize(fheight +10,fheight + 10)

		self.unseenLabel = QLabel("Unseen messages color: <b>"+config.UNSEEN_MESSAGE_COLOR+"</b>")

		unseenColorLayout = QHBoxLayout()
		unseenColorLayout.addWidget(self.setUnseen)
		unseenColorLayout.addWidget(self.unseenLabel)

		self.setConnecting = QPushButton("")
		self.setConnecting.clicked.connect(self.connectingColor)
		self.setConnecting.setStyleSheet(f'background-color: {config.CONNECTING_ANIMATION_COLOR};')

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setConnecting.setFixedSize(fheight +10,fheight + 10)

		self.connectingLabel = QLabel("Connecting color: <b>"+config.CONNECTING_ANIMATION_COLOR+"</b>")

		connectingColorLayout = QHBoxLayout()
		connectingColorLayout.addWidget(self.setConnecting)
		connectingColorLayout.addWidget(self.connectingLabel)

		self.collapseConnection = QCheckBox("Entries are collapsable",self)
		if config.CONNECTION_DISPLAY_COLLAPSE: self.collapseConnection.setChecked(True)

		self.branchConnection = QCheckBox("Display branches",self)
		if config.CONNECTION_DISPLAY_BRANCHES: self.branchConnection.setChecked(True)

		self.underlineConnection = QCheckBox("Current display is underlined",self)
		if config.UNDERLINE_CURRENT_CHAT: self.underlineConnection.setChecked(True)

		self.boldConnection = QCheckBox("Current display is in bold",self)
		if config.BOLD_CURRENT_CHAT: self.boldConnection.setChecked(True)

		self.italicConnection = QCheckBox("Current display is in italics",self)
		if config.ITALIC_CURRENT_CHAT: self.italicConnection.setChecked(True)

		if self.parent!= None:
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
				self.setBg.setEnabled(False)
				self.bgLabel.setEnabled(False)
				self.setfg.setEnabled(False)
				self.fgLabel.setEnabled(False)
				self.menuConnection.setEnabled(False)
				self.setConnecting.setEnabled(False)
				self.connectingLabel.setEnabled(False)
				self.setUnseen.setEnabled(False)
				self.unseenLabel.setEnabled(False)
				self.collapseConnection.setEnabled(False)
				self.branchConnection.setEnabled(False)
				self.underlineConnection.setEnabled(False)
				self.boldConnection.setEnabled(False)
				self.italicConnection.setEnabled(False)

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

		if self.parent!= None:
			if self.parent.block_connectiondisplay: clLayout.setEnabled(False)

		condisLayout = QVBoxLayout()
		condisLayout.addLayout(clLayoutH)
		condisLayout.addWidget(self.enableConnection)
		condisLayout.addWidget(self.menuConnection)
		condisLayout.addWidget(self.floatConnection)
		condisLayout.addWidget(self.uptimesConnection)
		condisLayout.addWidget(self.doubleConnection)
		condisLayout.addWidget(self.expandConnection)
		condisLayout.addWidget(self.collapseConnection)
		condisLayout.addStretch()

		appearanceLayout = QVBoxLayout()
		appearanceLayout.addLayout(bgColorLayout)
		appearanceLayout.addLayout(fgColorLayout)
		appearanceLayout.addWidget(self.unseenConnection)
		appearanceLayout.addLayout(unseenColorLayout)
		appearanceLayout.addWidget(self.animateConnection)
		appearanceLayout.addLayout(connectingColorLayout)
		appearanceLayout.addWidget(self.branchConnection)
		appearanceLayout.addWidget(self.underlineConnection)
		appearanceLayout.addWidget(self.boldConnection)
		appearanceLayout.addWidget(self.italicConnection)
		appearanceLayout.addStretch()


		self.customConnectionPage.setLayout(appearanceLayout)

		self.connectionPage.setLayout(condisLayout)


		# Input settings

		self.inputPage = QWidget()
		self.historyPage = QWidget()
		self.emojiPage = QWidget()

		self.inputTabs = QTabWidget()

		self.inputTabs.addTab(self.inputPage, QIcon(ENTRY_ICON), "Text Input")
		self.inputTabs.addTab(self.emojiPage, QIcon(EMOJI_ICON), "Emojis")
		self.inputTabs.addTab(self.historyPage, QIcon(HISTORY_LENGTH_ICON), "History")

		self.resetHistory = False
		self.historySize = None

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Text Input")
		entry.widget = self.inputTabs
		entry.setIcon(QIcon(ENTRY_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.inputTabs)

		self.trackInput = QCheckBox("Track input history",self)
		if config.TRACK_COMMAND_HISTORY: self.trackInput.setChecked(True)
		self.trackInput.stateChanged.connect(self.setReset)

		hsButton = QPushButton("")
		hsButton.clicked.connect(self.setHistory)
		hsButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		hsButton.setFixedSize(fheight +10,fheight + 10)
		hsButton.setIcon(QIcon(EDIT_ICON))
		hsButton.setToolTip("Set history length")

		self.historyLabel = QLabel("Input history length: <b>"+str(config.HISTORY_LENGTH)+" lines</b>")

		histEdLayout = QHBoxLayout()
		histEdLayout.addWidget(hsButton)
		histEdLayout.addWidget(self.historyLabel)
		histEdLayout.addStretch()

		histLayout = QVBoxLayout()
		histLayout.addWidget(self.trackInput)
		histLayout.addLayout(histEdLayout)
		histLayout.addStretch()

		self.nickComplete = QCheckBox("Auto-complete nicknames",self)
		if config.AUTOCOMPLETE_NICKNAMES: self.nickComplete.setChecked(True)

		self.cmdComplete = QCheckBox("Auto-complete commands",self)
		if config.AUTOCOMPLETE_COMMANDS: self.cmdComplete.setChecked(True)

		self.channelComplete = QCheckBox("Auto-complete channels",self)
		if config.AUTOCOMPLETE_CHANNELS: self.channelComplete.setChecked(True)

		self.inputCommands = QCheckBox("Enable command input",self)
		if config.ENABLE_COMMANDS: self.inputCommands.setChecked(True)

		self.inputMe = QCheckBox("Always allow "+config.INPUT_COMMAND_SYMBOL+"me command",self)
		if config.ALWAYS_ALLOW_ME: self.inputMe.setChecked(True)

		if self.parent!=None:
			if self.parent.block_commands:
				self.inputCommands.setEnabled(False)

		self.emojiComplete = QCheckBox("Auto-complete emoji shortcodes",self)
		if config.AUTOCOMPLETE_EMOJI: self.emojiComplete.setChecked(True)

		self.emojiInput = QCheckBox("Enable emoji shortcodes",self)
		if config.USE_EMOJIS: self.emojiInput.setChecked(True)

		ebLayout = QVBoxLayout()
		ebLayout.addWidget(self.emojiInput)
		ebLayout.addWidget(self.emojiComplete)
		ebLayout.addStretch()

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(self.inputCommands)
		cpLayout.addWidget(self.inputMe)
		cpLayout.addWidget(self.cmdComplete)
		cpLayout.addWidget(self.nickComplete)
		cpLayout.addWidget(self.channelComplete)
		cpLayout.addStretch()

		self.emojiPage.setLayout(ebLayout)

		self.historyPage.setLayout(histLayout)

		self.inputPage.setLayout(cpLayout)

		# Spellcheck settings

		self.sclanguage = config.SPELLCHECK_LANGUAGE

		self.spellcheckPage = QWidget()

		self.spellTabs = QTabWidget()

		self.spellTabs.addTab(self.spellcheckPage, QIcon(SPELLCHECK_ICON), "Spellcheck")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Spellcheck")
		entry.widget = self.spellTabs
		entry.setIcon(QIcon(SPELLCHECK_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.spellTabs)

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
		
		cpLayout.addStretch()

		self.spellcheckPage.setLayout(cpLayout)

		# Features settings

		self.featuresPage = QWidget()
		self.scriptFeatures = QWidget()
		self.highlightPage = QWidget()

		self.featuresTabs = QTabWidget()

		self.featuresTabs.addTab(self.featuresPage, QIcon(SCRIPT_ICON), "Scripting")
		self.featuresTabs.addTab(self.scriptFeatures, QIcon(FEATURES_ICON), "Features")
		self.featuresTabs.addTab(self.highlightPage, QIcon(MISC_ICON), "Highlighting")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Scripting")
		entry.widget = self.featuresTabs
		entry.setIcon(QIcon(SCRIPT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.featuresTabs)

		self.scriptMisc = QCheckBox("Enable scripting",self)
		if config.ENABLE_SCRIPTS: self.scriptMisc.setChecked(True)

		self.enableAliasMisc = QCheckBox("Enable aliases",self)
		if config.ENABLE_ALIASES: self.enableAliasMisc.setChecked(True)

		self.sglobalMisc = QCheckBox("Aliases are global",self)
		if config.GLOBALIZE_ALL_SCRIPT_ALIASES: self.sglobalMisc.setChecked(True)

		self.seditMisc = QCheckBox("Enable script editor",self)
		if config.ENABLE_SCRIPT_EDITOR: self.seditMisc.setChecked(True)

		if self.parent!= None:
			if self.parent.cmdline_editor:
				self.seditMisc.setEnabled(False)

		self.autoMacros = QCheckBox("Auto-complete macros",self)
		if config.AUTOCOMPLETE_MACROS: self.autoMacros.setChecked(True)

		self.saveMacros = QCheckBox("Save macros",self)
		if config.SAVE_MACROS: self.saveMacros.setChecked(True)

		self.enableMacros = QCheckBox("Enable macros",self)
		if config.ENABLE_MACROS: self.enableMacros.setChecked(True)

		scriptLayout = QVBoxLayout()
		scriptLayout.addWidget(self.scriptMisc)
		scriptLayout.addWidget(self.seditMisc)
		scriptLayout.addStretch()

		if self.parent!= None:
			if self.parent.cmdline_script:
				self.scriptMisc.setEnabled(False)
				self.sglobalMisc.setEnabled(False)
				self.seditMisc.setEnabled(False)
				self.autoMacros.setEnabled(False)
				self.saveMacros.setEnabled(False)
				self.enableMacros.setEnabled(False)
				self.enableAliasMisc.setEnabled(False)

		aliasLayout = QVBoxLayout()
		aliasLayout.addWidget(self.enableAliasMisc)
		aliasLayout.addWidget(self.sglobalMisc)

		aliasBox = QGroupBox("Aliases",self)
		aliasBox.setLayout(aliasLayout)

		aliasBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		macroLayout = QVBoxLayout()
		macroLayout.addWidget(self.enableMacros)
		macroLayout.addWidget(self.saveMacros)
		macroLayout.addWidget(self.autoMacros)

		macroBox = QGroupBox("Macros",self)
		macroBox.setLayout(macroLayout)

		macroBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		featuresLayout = QVBoxLayout()
		featuresLayout.addWidget(aliasBox)
		featuresLayout.addWidget(macroBox)
		featuresLayout.addStretch()

		self.syntax_background_color = config.SCRIPT_SYNTAX_BACKGROUND
		self.syntax_text_color = config.SCRIPT_SYNTAX_TEXT

		self.setSyntaxBg = QPushButton("")
		self.setSyntaxBg.clicked.connect(self.syntaxBackground)
		self.setSyntaxBg.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_BACKGROUND};')

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setSyntaxBg.setFixedSize(fheight +10,fheight + 10)

		self.syntaxBgLabel = QLabel("Background color: <b>"+config.SCRIPT_SYNTAX_BACKGROUND+"</b>")

		syntaxBgLayout = QHBoxLayout()
		syntaxBgLayout.addWidget(self.setSyntaxBg)
		syntaxBgLayout.addWidget(self.syntaxBgLabel)

		self.setSyntaxFg = QPushButton("")
		self.setSyntaxFg.clicked.connect(self.syntaxText)
		self.setSyntaxFg.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_TEXT};')

		self.setSyntaxFg.setFixedSize(fheight +10,fheight + 10)

		self.syntaxFgLabel = QLabel("Text color: <b>"+config.SCRIPT_SYNTAX_TEXT+"</b>")

		syntaxFgLayout = QHBoxLayout()
		syntaxFgLayout.addWidget(self.setSyntaxFg)
		syntaxFgLayout.addWidget(self.syntaxFgLabel)


		self.syntax_comment_color = config.SCRIPT_SYNTAX_COMMENTS

		self.setSyntaxComment = QPushButton("")
		self.setSyntaxComment.clicked.connect(self.syntaxComment)
		self.setSyntaxComment.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_COMMENTS};')

		self.setSyntaxComment.setFixedSize(fheight +10,fheight + 10)

		self.syntaxCommentLabel = QLabel("Comments: <b>"+config.SCRIPT_SYNTAX_COMMENTS+"</b>")

		syntaxCommentLayout = QHBoxLayout()
		syntaxCommentLayout.addWidget(self.setSyntaxComment)
		syntaxCommentLayout.addWidget(self.syntaxCommentLabel)

		self.syntax_command_color = config.SCRIPT_SYNTAX_COMMANDS

		self.setSyntaxCommand = QPushButton("")
		self.setSyntaxCommand.clicked.connect(self.syntaxCommand)
		self.setSyntaxCommand.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_COMMANDS};')

		self.setSyntaxCommand.setFixedSize(fheight +10,fheight + 10)

		self.syntaxCommandLabel = QLabel("Commands: <b>"+config.SCRIPT_SYNTAX_COMMANDS+"</b>")

		syntaxCommandLayout = QHBoxLayout()
		syntaxCommandLayout.addWidget(self.setSyntaxCommand)
		syntaxCommandLayout.addWidget(self.syntaxCommandLabel)

		self.syntax_target_color = config.SCRIPT_SYNTAX_TARGETS

		self.setSyntaxTarget = QPushButton("")
		self.setSyntaxTarget.clicked.connect(self.syntaxTarget)
		self.setSyntaxTarget.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_TARGETS};')

		self.setSyntaxTarget.setFixedSize(fheight +10,fheight + 10)

		self.syntaxTargetLabel = QLabel("Channels: <b>"+config.SCRIPT_SYNTAX_TARGETS+"</b>")

		syntaxTargetLayout = QHBoxLayout()
		syntaxTargetLayout.addWidget(self.setSyntaxTarget)
		syntaxTargetLayout.addWidget(self.syntaxTargetLabel)


		self.syntax_alias_color = config.SCRIPT_SYNTAX_ALIAS

		self.setSyntaxAlias = QPushButton("")
		self.setSyntaxAlias.clicked.connect(self.syntaxAlias)
		self.setSyntaxAlias.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_ALIAS};')

		self.setSyntaxAlias.setFixedSize(fheight +10,fheight + 10)

		self.syntaxAliasLabel = QLabel("Aliases: <b>"+config.SCRIPT_SYNTAX_ALIAS+"</b>")

		syntaxAliasLayout = QHBoxLayout()
		syntaxAliasLayout.addWidget(self.setSyntaxAlias)
		syntaxAliasLayout.addWidget(self.syntaxAliasLabel)


		self.syntaxInfo = QLabel("""
			<small>

			These are the colors used to highlight Ərk scripts in the script editor, and in the connection dialog. If the editor or the
			connection dialog are open when you are changing colors, you will have to restart the editor or close and re-open the connection
			dialog to see any changes.

			</small><br>
			""")
		self.syntaxInfo.setWordWrap(True)
		self.syntaxInfo.setAlignment(Qt.AlignJustify)

		syntaxLayout = QVBoxLayout()
		syntaxLayout.addWidget(self.syntaxInfo)
		syntaxLayout.addLayout(syntaxBgLayout)
		syntaxLayout.addLayout(syntaxFgLayout)
		syntaxLayout.addLayout(syntaxCommentLayout)
		syntaxLayout.addLayout(syntaxCommandLayout)
		syntaxLayout.addLayout(syntaxTargetLayout)
		syntaxLayout.addLayout(syntaxAliasLayout)
		syntaxLayout.addStretch()

		self.highlightPage.setLayout(syntaxLayout)

		self.scriptFeatures.setLayout(featuresLayout)

		self.featuresPage.setLayout(scriptLayout)

		# Plugins page

		self.pluginsPage = QWidget()
		self.pluginsFiles = QWidget()
		self.pluginsMenu = QWidget()

		self.pluginsTabs = QTabWidget()

		self.pluginsTabs.addTab(self.pluginsPage, QIcon(PLUGIN_ICON), "Plugins")
		self.pluginsTabs.addTab(self.pluginsMenu, QIcon(MENU_ICON), "Menu")
		self.pluginsTabs.addTab(self.pluginsFiles, QIcon(DIRECTORY_ICON), "Sources")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Plugins")
		entry.widget = self.pluginsTabs
		entry.setIcon(QIcon(PLUGIN_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.pluginsTabs)

		self.enPlugins = QCheckBox("Enable plugins",self)
		if config.ENABLE_PLUGINS: self.enPlugins.setChecked(True)

		self.showPlugins = QCheckBox("Show plugins menu",self)
		if config.SHOW_PLUGINS_MENU: self.showPlugins.setChecked(True)

		self.igPlugins = QCheckBox("Plugins catch ignored messages",self)
		if config.PLUGINS_CATCH_IGNORES: self.igPlugins.setChecked(True)

		self.detPlugins = QCheckBox("Show plugin details in menu",self)
		if config.SHOW_PLUGIN_INFO_IN_MENU: self.detPlugins.setChecked(True)

		self.autoPlugins = QCheckBox("Plugins can add to autocomplete",self)
		if config.AUTOCOMPLETE_PLUGINS: self.autoPlugins.setChecked(True)

		self.helpPlugins = QCheckBox("Plugins can add to /help",self)
		if config.PLUGIN_HELP: self.helpPlugins.setChecked(True)

		self.inputPlugins = QCheckBox("Enable plugin input events",self)
		if config.ENABLE_PLUGIN_INPUT: self.inputPlugins.setChecked(True)

		self.errorPlugins = QCheckBox("Display plugin loading errors",self)
		if config.PLUGIN_LOAD_ERRORS: self.errorPlugins.setChecked(True)

		self.plug_list = QListWidget(self)
		for e in config.ADDITIONAL_PLUGIN_LOCATIONS:
			item = QListWidgetItem(e)
			self.plug_list.addItem(item)

		fm = QFontMetrics(self.font())
		fheight = fm.height() * 7
		self.plug_list.setMaximumHeight(fheight)

		self.addDirectory = QPushButton("Add directory")
		self.addDirectory.clicked.connect(self.plugbuttonAdd)
		self.addDirectory.setAutoDefault(False)

		self.removeDirectory = QPushButton("Remove directory")
		self.removeDirectory.clicked.connect(self.plugbuttonRemove)
		self.removeDirectory.setAutoDefault(False)

		self.clearDirectories = QPushButton("Clear")
		self.clearDirectories.clicked.connect(self.plugbuttonClear)
		self.clearDirectories.setAutoDefault(False)

		aLayout = QHBoxLayout()
		aLayout.addWidget(self.addDirectory)
		aLayout.addWidget(self.removeDirectory)
		aLayout.addWidget(self.clearDirectories)
		
		bLayout = QVBoxLayout()
		bLayout.addWidget(self.plug_list)
		bLayout.addLayout(aLayout)

		plugBox = QGroupBox("Load additional plugins from...",self)
		plugBox.setLayout(bLayout)

		plugBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		plugLayout = QVBoxLayout()
		plugLayout.addWidget(self.enPlugins)
		plugLayout.addWidget(self.errorPlugins)
		plugLayout.addWidget(self.igPlugins)
		plugLayout.addWidget(self.autoPlugins)
		plugLayout.addWidget(self.helpPlugins)
		plugLayout.addWidget(self.inputPlugins)
		plugLayout.addStretch()

		if self.parent!= None:
			if self.parent.block_plugins:
				self.enPlugins.setEnabled(False)
				self.showPlugins.setEnabled(False)
				self.igPlugins.setEnabled(False)
				self.detPlugins.setEnabled(False)
				self.autoPlugins.setEnabled(False)
				self.helpPlugins.setEnabled(False)
				plugBox.setEnabled(False)
				self.errorPlugins.setEnabled(False)

		self.pluginsPage.setLayout(plugLayout)

		self.pluginFilesInfo = QLabel("""
			<center><big><b>Plugin Sources</b></big></center><br>
			<small>

			Plugins can be loaded from any directory, not just <b>.erk/plugins</b> in your home directory. Here you can select any other directories
			you'd like to load plugins from. Click the "Add Directory" button to add a directory. Select a directory, and click the "Remove Directory"
			button to remove it from the list. Click "Clear" to remove all directories from the list.

			</small>
			""")
		self.pluginFilesInfo.setWordWrap(True)
		self.pluginFilesInfo.setAlignment(Qt.AlignJustify)

		plugLocLayout = QVBoxLayout()
		plugLocLayout.addWidget(self.pluginFilesInfo)
		plugLocLayout.addStretch()
		plugLocLayout.addWidget(plugBox)

		plugMenuLayout = QVBoxLayout()
		plugMenuLayout.addWidget(self.showPlugins)
		plugMenuLayout.addWidget(self.detPlugins)
		plugMenuLayout.addStretch()

		self.pluginsMenu.setLayout(plugMenuLayout)

		self.pluginsFiles.setLayout(plugLocLayout)

		# Miscellaneous settings

		self.initial_fetch_list = config.AUTOMATICALLY_FETCH_CHANNEL_LIST

		self.miscPage = QWidget()
		self.listPage = QWidget()

		self.miscTabs = QTabWidget()

		self.miscTabs.addTab(self.miscPage, QIcon(MISC_ICON), "Miscellaneous")
		self.miscTabs.addTab(self.listPage, QIcon(CHANNEL_ICON), "Channel Search")

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Miscellaneous")
		entry.widget = self.miscTabs
		entry.setIcon(QIcon(MISC_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.miscTabs)

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

		self.listFreq = QLabel("Refresh list every <b>"+str(config.CHANNEL_LIST_REFRESH_FREQUENCY)+"</b> seconds")

		refRateLayout = QHBoxLayout()
		refRateLayout.addWidget(self.refreshButton)
		refRateLayout.addWidget(self.listFreq)
		refRateLayout.addStretch()

		self.listMark = QCheckBox("Mark beginning/end of list search",self)
		if config.MARK_BEGINNING_AND_END_OF_LIST_SEARCH: self.listMark.setChecked(True)

		self.listLimit = QCheckBox("Limit searches to channel names",self)
		if config.LIMIT_LIST_SEARCH_TO_CHANNEL_NAME: self.listLimit.setChecked(True)

		self.listCase = QCheckBox("Searches are case sensitive",self)
		if config.LIST_SEARCH_CASE_SENSITIVE: self.listCase.setChecked(True)

		chListLayout = QVBoxLayout()
		chListLayout.addWidget(self.listMisc)
		chListLayout.addLayout(refRateLayout)
		chListLayout.addWidget(self.listMark)
		chListLayout.addWidget(self.listLimit)
		chListLayout.addWidget(self.listCase)
		chListLayout.addStretch()

		self.fetchMisc = QCheckBox("Fetch hostmasks on channel join",self)
		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN: self.fetchMisc.setChecked(True)
		self.fetchMisc.stateChanged.connect(self.setRerender)

		self.joinMisc = QCheckBox("Auto-join on channel invite",self)
		if config.JOIN_ON_INVITE: self.joinMisc.setChecked(True)

		self.rejoinMisc = QCheckBox("Re-join channels upon reconnecting",self)
		if config.REJOIN_CHANNELS_ON_DISCONNECTIONS: self.rejoinMisc.setChecked(True)

		self.rejoinMisc.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

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

		cpLayout = QVBoxLayout()
		cpLayout.addWidget(quitPartBox)
		cpLayout.addWidget(self.buttonsMisc)
		cpLayout.addWidget(self.switchMisc)

		cpLayout.addWidget(self.fetchMisc)
		cpLayout.addWidget(self.joinMisc)
		cpLayout.addWidget(self.rejoinMisc)
		cpLayout.addStretch()

		self.listPage.setLayout(chListLayout)

		self.miscPage.setLayout(cpLayout)

		# Buttons and main layout

		loadButton = QPushButton("")
		loadButton.clicked.connect(self.loadConfig)
		loadButton.setAutoDefault(False)
		loadButton.setIcon(QIcon(IMPORT_ICON))
		loadButton.setToolTip("Import configuration file")

		exportButton = QPushButton("")
		exportButton.clicked.connect(self.saveConfig)
		exportButton.setAutoDefault(False)
		exportButton.setIcon(QIcon(EXPORT_ICON))
		exportButton.setToolTip("Export configuration file")

		saveButton = QPushButton("Apply")
		saveButton.clicked.connect(self.save)
		saveButton.setAutoDefault(False)

		if self.parent==None:
			if self.config!=SETTINGS_FILE:
				saveButton.setText("Save "+os.path.basename(self.config))
			else:
				saveButton.setText("Save")

		cancelButton = QPushButton("Cancel")
		cancelButton.clicked.connect(self.close)

		if self.parent==None:
			cancelButton.setText("Exit")

		dialogButtonsLayout = QHBoxLayout()
		dialogButtonsLayout.addWidget(loadButton)
		dialogButtonsLayout.addWidget(exportButton)
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

		if self.opento=="highlight":
			self.stack.setCurrentWidget(self.featuresTabs)
			self.selector.clearSelection()
			self.selector.setCurrentRow(9,QItemSelectionModel.SelectCurrent)
			self.featuresTabs.setCurrentIndex(2)

		if self.opento=="scriptfeatures":
			self.stack.setCurrentWidget(self.featuresTabs)
			self.selector.clearSelection()
			self.selector.setCurrentRow(9,QItemSelectionModel.SelectCurrent)
			self.featuresTabs.setCurrentIndex(1)

		if self.opento=="scriptsettings":
			self.stack.setCurrentWidget(self.featuresTabs)
			self.selector.clearSelection()
			self.selector.setCurrentRow(9,QItemSelectionModel.SelectCurrent)
			self.featuresTabs.setCurrentIndex(0)

	def plugbuttonAdd(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		options |= QFileDialog.ShowDirsOnly
		options |= QFileDialog.HideNameFilterDetails
		options |= QFileDialog.ReadOnly
		folderpath = QFileDialog.getExistingDirectory(self, 'Select Directory', str(Path.home()),options=options)
		if folderpath:
			self.plug_list.addItem(folderpath)

	def plugbuttonRemove(self):
		i = self.plug_list.currentRow()
		self.plug_list.takeItem(i)

	def plugbuttonClear(self):
		self.plug_list.clear()

	def save(self):

		self.saved = True

		config.ITALIC_CURRENT_CHAT = self.italicConnection.isChecked()

		config.UNDERLINE_CURRENT_CHAT = self.underlineConnection.isChecked()
		config.BOLD_CURRENT_CHAT = self.boldConnection.isChecked()

		config.CONNECTION_DISPLAY_COLLAPSE = self.collapseConnection.isChecked()

		config.CONNECTION_DISPLAY_BRANCHES = self.branchConnection.isChecked()

		config.CURSOR_WIDTH = self.cursor_width

		config.UNSEEN_MESSAGE_COLOR = self.unseen_message_color
		config.CONNECTING_ANIMATION_COLOR = self.connecting_anim_color

		config.LOAD_SERVER_LOGS = self.servLoadLog.isChecked()

		config.SAVE_SERVER_LOGS = self.servSaveLog.isChecked()

		config.DISPLAY_MODES_ON_CHANNEL = self.displayUserModes.isChecked()

		config.ENABLE_CONNECTION_CONTEXT = self.menuConnection.isChecked()

		config.ENABLE_USERLIST_MENU = self.channelUserMenu.isChecked()

		config.ENABLE_TOPIC_EDITOR = self.channelTopic.isChecked()

		config.SCRIPT_SYNTAX_ALIAS = self.syntax_alias_color

		config.SCRIPT_SYNTAX_TARGETS = self.syntax_target_color

		config.SCRIPT_SYNTAX_COMMENTS = self.syntax_comment_color

		config.SCRIPT_SYNTAX_COMMANDS = self.syntax_command_color

		config.SCRIPT_SYNTAX_BACKGROUND = self.syntax_background_color
		config.SCRIPT_SYNTAX_TEXT = self.syntax_text_color

		config.CONNECTION_DISPLAY_BG_COLOR = self.connection_background_color
		config.CONNECTION_DISPLAY_TEXT_COLOR = self.connection_text_color

		config.PLUGIN_LOAD_ERRORS = self.errorPlugins.isChecked()

		config.REJOIN_CHANNELS_ON_DISCONNECTIONS = self.rejoinMisc.isChecked()

		config.SCROLL_CHAT_TO_BOTTOM = self.channelLatest.isChecked()

		config.ENABLE_PLUGIN_INPUT = self.inputPlugins.isChecked()

		config.ENABLE_ALIASES = self.enableAliasMisc.isChecked()

		config.LIST_SEARCH_CASE_SENSITIVE = self.listCase.isChecked()

		config.MARK_BEGINNING_AND_END_OF_LIST_SEARCH = self.listMark.isChecked()
		config.LIMIT_LIST_SEARCH_TO_CHANNEL_NAME = self.listLimit.isChecked()

		plugDirectories =  [str(self.plug_list.item(i).text()) for i in range(self.plug_list.count())]
		# Remove duplicates from the list
		plugDirectories = list(dict.fromkeys(plugDirectories))
		config.ADDITIONAL_PLUGIN_LOCATIONS = plugDirectories

		config.PLUGIN_HELP = self.helpPlugins.isChecked()

		config.AUTOCOMPLETE_PLUGINS = self.autoPlugins.isChecked()

		config.SHOW_PLUGIN_INFO_IN_MENU = self.detPlugins.isChecked()

		config.ALWAYS_ALLOW_ME = self.inputMe.isChecked()

		config.PLUGINS_CATCH_IGNORES = self.igPlugins.isChecked()

		config.SHOW_PLUGINS_MENU = self.showPlugins.isChecked()

		config.ENABLE_PLUGINS = self.enPlugins.isChecked()

		if self.parent!= None:
			self.parent.reloadPlugins()

		config.ENABLE_COMMANDS = self.inputCommands.isChecked()

		config.WRITE_NOTICE_TO_CONSOLE = self.writeNotice.isChecked()
		config.WRITE_PRIVATE_TO_CONSOLE = self.writePrivate.isChecked()

		config.IGNORE_PUBLIC = self.notePublic.isChecked()
		config.IGNORE_PRIVATE = self.notePrivate.isChecked()
		config.IGNORE_NOTICE = self.noteNotice.isChecked()

		if self.parent!= None:

			if self.noteIgnore.isChecked() and not config.ENABLE_IGNORE:
				u = get_user(self.parent.userfile)
				self.parent.ignore = u["ignore"]
				events.recheck_userlists()

			if not self.noteIgnore.isChecked() and config.ENABLE_IGNORE:
				self.parent.ignore = []
				events.recheck_userlists()

		config.ENABLE_IGNORE = self.noteIgnore.isChecked()

		config.HIDE_JOIN_MESSAGE = self.noteJoin.isChecked()

		config.HIDE_PART_MESSAGE = self.notePart.isChecked()

		config.HIDE_INVITE_MESSAGE = self.noteInvite.isChecked()

		config.HIDE_NICK_MESSAGE = self.noteNick.isChecked()

		config.HIDE_QUIT_MESSAGE = self.noteQuit.isChecked()

		config.HIDE_TOPIC_MESSAGE = self.noteTopic.isChecked()

		config.HIDE_MODE_DISPLAY = self.noteMode.isChecked()

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

		if self.parent!= None:
			if config.ENABLE_SCRIPT_EDITOR:
				if not self.parent.cmdline_editor:
					self.parent.block_editor = False
			else:
				self.parent.block_editor = True

		config.USE_QMENUBAR_MENUS = self.menuMisc.isChecked()

		config.GLOBALIZE_ALL_SCRIPT_ALIASES = self.sglobalMisc.isChecked()

		config.SHOW_CONSOLE_BUTTONS = self.buttonsMisc.isChecked()

		if self.parent!= None:
			if config.SHOW_CONSOLE_BUTTONS:
				if config.ENABLE_COMMANDS:
					events.show_all_console_buttons()
				else:
					events.hide_all_console_buttons()
			else:
				events.hide_all_console_buttons()

		config.DOUBLECLICK_TO_CHANGE_NICK = self.displayChange.isChecked()

		config.ENABLE_SCRIPTS = self.scriptMisc.isChecked()

		if self.parent!= None:
			if config.ENABLE_SCRIPTS:
				if not self.parent.cmdline_script:
					self.parent.block_scripts = False
					events.enable_all_runscript()
			else:
				self.parent.block_scripts = True
				events.disable_all_runscript()

		config.MENU_BAR_MOVABLE = self.showMenu.isChecked()

		if self.parent!= None:
			if config.MENU_BAR_MOVABLE:
				self.parent.set_menubar_moveable(True)
			else:
				self.parent.set_menubar_moveable(False)

		config.ASK_BEFORE_QUIT = self.askMisc.isChecked()

		config.SCHWA_ANIMATION = self.showSchwa.isChecked()

		config.UNSEEN_MESSAGE_ANIMATION = self.unseenConnection.isChecked()
		config.CONNECTION_MESSAGE_ANIMATION = self.animateConnection.isChecked()

		config.SHOW_CONNECTION_FAIL_ERROR = self.failErrors.isChecked()
		config.SHOW_CONNECTION_LOST_ERROR = self.lostErrors.isChecked()

		config.CHANNEL_LIST_REFRESH_FREQUENCY = self.configRefresh

		config.AUTOMATICALLY_FETCH_CHANNEL_LIST = self.listMisc.isChecked()

		if self.parent!= None:
			if config.AUTOMATICALLY_FETCH_CHANNEL_LIST!=self.initial_fetch_list:
				if config.AUTOMATICALLY_FETCH_CHANNEL_LIST:
					for c in events.fetch_connections():
						if c.last_fetch < c.uptime:
							c.sendLine("LIST")

		if self.newfont!=None:
			config.DISPLAY_FONT = self.newfont.toString()
			if self.parent!= None:
				self.parent.app.setFont(self.newfont)
				events.set_fonts_all(self.newfont)

		if self.historySize!=None: config.HISTORY_LENGTH = self.historySize

		if self.parent!= None:
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
			if self.parent!= None: events.newspell_all(self.sclanguage)

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

		if self.parent!= None:

			plugins.load_plugins(self.parent.block_plugins,self.parent.more_plugins)

			if self.do_rerender: events.rerender_all()

			self.parent.buildMenuInterface()
			events.toggle_name_topic_display()
			events.toggle_channel_mode_display()
			events.rerender_userlists()
			events.toggle_userlist()
			events.rerender_channel_nickname()
			self.parent.refresh_application_title()
			events.resetinput_all()
			events.set_cursor_width()

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

			self.parent.connection_display.setItemsExpandable(config.CONNECTION_DISPLAY_COLLAPSE)

			self.parent.setConnectionColors(config.CONNECTION_DISPLAY_BG_COLOR,config.CONNECTION_DISPLAY_TEXT_COLOR)

			events.build_connection_display(self.parent)

			userinput.buildHelp()
			events.reload_commands_all()
			events.reset_topic_editor()
			events.refresh_all_topics()
			events.update_all_mode_displays()

		config.save_settings(self.config)

		self.close()

	def saveConfig(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Preferences As...","settings.json","JSON File (*.json);;All Files (*)", options=options)
		if fileName:
			efl = len("json")+1
			if fileName[-efl:].lower()!=f".json": fileName = fileName+f".json"
			config.save_settings(fileName)

	def loadConfig(self):

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Select Preferences File", INSTALL_DIRECTORY,"JSON File (*.json);;All Files (*)", options=options)
		if fileName:

			if config.check_settings(fileName):

				config.load_settings(fileName)
				self.nametitleMisc.setChecked(config.APP_TITLE_TO_CURRENT_CHAT)
				self.topicMisc.setChecked(config.APP_TITLE_SHOW_TOPIC)
				self.askMisc.setChecked(config.ASK_BEFORE_QUIT)
				self.lostErrors.setChecked(config.SHOW_CONNECTION_LOST_ERROR)
				self.failErrors.setChecked(config.SHOW_CONNECTION_FAIL_ERROR)
				self.showSchwa.setChecked(config.SCHWA_ANIMATION)
				self.showMenu.setChecked(config.MENU_BAR_MOVABLE)
				self.menuMisc.setChecked(config.USE_QMENUBAR_MENUS)
				self.showDates.setChecked(config.DISPLAY_DATES_IN_CHANNEL_CHAT)
				self.showColors.setChecked(config.DISPLAY_IRC_COLORS)
				self.showLinks.setChecked(config.CONVERT_URLS_TO_LINKS)
				self.hideProfanity.setChecked(config.FILTER_PROFANITY)
				self.openNew.setChecked(config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS)
				self.channelLinks.setChecked(config.CLICKABLE_CHANNELS)
				self.addPrefixes.setChecked(config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL)
				self.chansaveLog.setChecked(config.SAVE_CHANNEL_LOGS)
				self.chanloadLog.setChecked(config.LOAD_CHANNEL_LOGS)
				self.privsaveLog.setChecked(config.SAVE_PRIVATE_LOGS)
				self.privloadLog.setChecked(config.LOAD_PRIVATE_LOGS)
				self.markLog.setChecked(config.MARK_END_OF_LOADED_LOG)
				self.resumeLog.setChecked(config.DISPLAY_CHAT_RESUME_DATE_TIME)
				self.autoLog.setChecked(config.AUTOSAVE_LOGS)
				self.channelInfo.setChecked(config.CHAT_DISPLAY_INFO_BAR)
				self.channelModes.setChecked(config.DISPLAY_CHANNEL_MODES)
				self.textUserlist.setChecked(config.PLAIN_USER_LISTS)
				self.displayUserlists.setChecked(config.DISPLAY_USER_LIST)
				self.displayStatus.setChecked(config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY)
				self.displayNickname.setChecked(config.DISPLAY_NICKNAME_ON_CHANNEL)
				self.displayChange.setChecked(config.DOUBLECLICK_TO_CHANGE_NICK)
				self.enableConnection.setChecked(config.CONNECTION_DISPLAY_VISIBLE)
				self.floatConnection.setChecked(config.CONNECTION_DISPLAY_MOVE)
				self.uptimesConnection.setChecked(config.DISPLAY_CONNECTION_UPTIME)
				self.doubleConnection.setChecked(config.DOUBLECLICK_SWITCH)
				self.expandConnection.setChecked(config.EXPAND_SERVER_ON_CONNECT)
				self.unseenConnection.setChecked(config.UNSEEN_MESSAGE_ANIMATION)
				self.animateConnection.setChecked(config.CONNECTION_MESSAGE_ANIMATION)

				if config.CONNECTION_DISPLAY_LOCATION=="left":
					self.leftRadio.setChecked(True)
					self.rightRadio.setChecked(False)
				if config.CONNECTION_DISPLAY_LOCATION=="right":
					self.rightRadio.setChecked(True)
					self.leftRadio.setChecked(False)

				self.trackInput.setChecked(config.TRACK_COMMAND_HISTORY)
				self.nickComplete.setChecked(config.AUTOCOMPLETE_NICKNAMES)
				self.cmdComplete.setChecked(config.AUTOCOMPLETE_COMMANDS)
				self.channelComplete.setChecked(config.AUTOCOMPLETE_CHANNELS)
				self.emojiComplete.setChecked(config.AUTOCOMPLETE_EMOJI)
				self.emojiInput.setChecked(config.USE_EMOJIS)
				self.enabledSpellcheck.setChecked(config.SPELLCHECK_INPUT)
				self.nickSpellcheck.setChecked(config.SPELLCHECK_IGNORE_NICKS)

				if config.SPELLCHECK_LANGUAGE=="en": self.englishSC.setChecked(True)
				if config.SPELLCHECK_LANGUAGE=="fr": self.frenchSC.setChecked(True)
				if config.SPELLCHECK_LANGUAGE=="es": self.spanishSC.setChecked(True)
				if config.SPELLCHECK_LANGUAGE=="de": self.germanSC.setChecked(True)

				self.enabledTimestamp.setChecked(config.DISPLAY_TIMESTAMP)
				self.twentyfourTimestamp.setChecked(config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS)
				self.secondsTimestamp.setChecked(config.DISPLAY_TIMESTAMP_SECONDS)
				self.scriptMisc.setChecked(config.ENABLE_SCRIPTS)
				self.sglobalMisc.setChecked(config.GLOBALIZE_ALL_SCRIPT_ALIASES)
				self.seditMisc.setChecked(config.ENABLE_SCRIPT_EDITOR)
				self.autoMacros.setChecked(config.AUTOCOMPLETE_MACROS)
				self.saveMacros.setChecked(config.SAVE_MACROS)
				self.enableMacros.setChecked(config.ENABLE_MACROS)

				self.buttonsMisc.setChecked(config.SHOW_CONSOLE_BUTTONS)
				self.switchMisc.setChecked(config.SWITCH_TO_NEW_WINDOWS)
				self.listMisc.setChecked(config.AUTOMATICALLY_FETCH_CHANNEL_LIST)
				self.fetchMisc.setChecked(config.GET_HOSTMASKS_ON_CHANNEL_JOIN)
				self.joinMisc.setChecked(config.JOIN_ON_INVITE)

				self.logDisplayLines = config.LOG_LOAD_SIZE_MAX
				self.autosave_time = config.AUTOSAVE_LOG_TIME
				self.systemPrefix = config.SYSTEM_MESSAGE_PREFIX
				self.configRefresh = config.CHANNEL_LIST_REFRESH_FREQUENCY
				self.default_quit_part = config.DEFAULT_QUIT_PART_MESSAGE
				self.do_rerender = True

				if config.DISPLAY_FONT!='':
					f = QFont()
					f.fromString(config.DISPLAY_FONT)
					self.newfont = f

					pfs = config.DISPLAY_FONT.split(',')
					font_name = pfs[0]
					font_size = pfs[1]

					self.fontLabel.setText(f"Font: <b>{font_name}, {font_size} pt</b>")

				self.prefDisplay.setText("Prefix: <b>"+self.systemPrefix+"</b>")
				self.historyLabel.setText("Command history: <b>"+str(self.historySize)+" lines</b>")

				self.partMsg.setText("<b>"+str(self.default_quit_part)+"</b>")
				self.listFreq.setText("Refresh list every <b>"+str(self.configRefresh)+"</b> seconds")
				self.autoLogLabel.setText("Autosave logs every <b>"+str(self.autosave_time)+"</b> seconds")
				self.logSizeLabel.setText("Load <b>"+str(self.logDisplayLines)+"</b> lines for display")

				self.igPlugins.setChecked(config.PLUGINS_CATCH_IGNORES)
				self.showPlugins.setChecked(config.SHOW_PLUGINS_MENU)
				self.enPlugins.setChecked(config.ENABLE_PLUGINS)
				self.inputCommands.setChecked(config.ENABLE_COMMANDS)
				self.writeNotice.setChecked(config.WRITE_NOTICE_TO_CONSOLE)
				self.writePrivate.setChecked(config.WRITE_PRIVATE_TO_CONSOLE)
				self.notePublic.setChecked(config.IGNORE_PUBLIC)
				self.notePrivate.setChecked(config.IGNORE_PRIVATE)
				self.noteNotice.setChecked(config.IGNORE_NOTICE)
				self.noteIgnore.setChecked(config.ENABLE_IGNORE)
				self.noteJoin.setChecked(config.HIDE_JOIN_MESSAGE)
				self.notePart.setChecked(config.HIDE_PART_MESSAGE)
				self.noteInvite.setChecked(config.HIDE_INVITE_MESSAGE)
				self.noteNick.setChecked(config.HIDE_NICK_MESSAGE)
				self.noteQuit.setChecked(config.HIDE_QUIT_MESSAGE)
				self.noteTopic.setChecked(config.HIDE_TOPIC_MESSAGE)
				self.noteMode.setChecked(config.HIDE_MODE_DISPLAY)
				self.inputMe.setChecked(config.ALWAYS_ALLOW_ME)
				self.detPlugins.setChecked(config.SHOW_PLUGIN_INFO_IN_MENU)
				self.autoPlugins.setChecked(config.AUTOCOMPLETE_PLUGINS)
				self.helpPlugins.setChecked(config.PLUGIN_HELP)
				self.listMark.setChecked(config.MARK_BEGINNING_AND_END_OF_LIST_SEARCH)
				self.listLimit.setChecked(config.LIMIT_LIST_SEARCH_TO_CHANNEL_NAME)
				self.listCase.setChecked(config.LIST_SEARCH_CASE_SENSITIVE)
				self.enableAliasMisc.setChecked(config.ENABLE_ALIASES)
				self.inputPlugins.setChecked(config.ENABLE_PLUGIN_INPUT)
				self.channelLatest.setChecked(config.SCROLL_CHAT_TO_BOTTOM)
				self.rejoinMisc.setChecked(config.REJOIN_CHANNELS_ON_DISCONNECTIONS)
				self.errorPlugins.setChecked(config.PLUGIN_LOAD_ERRORS)

				self.connection_background_color = config.CONNECTION_DISPLAY_BG_COLOR
				self.connection_text_color = config.CONNECTION_DISPLAY_TEXT_COLOR
				self.setFg.setStyleSheet(f'background-color: {config.CONNECTION_DISPLAY_TEXT_COLOR};')
				self.setBg.setStyleSheet(f'background-color: {config.CONNECTION_DISPLAY_BG_COLOR};')
				self.bgLabel.setText("Background color: <b>"+config.CONNECTION_DISPLAY_BG_COLOR+"</b>")
				self.fgLabel.setText("Text color: <b>"+config.CONNECTION_DISPLAY_TEXT_COLOR+"</b>")

				self.syntax_background_color = config.SCRIPT_SYNTAX_BACKGROUND
				self.syntax_text_color = config.SCRIPT_SYNTAX_TEXT
				self.setSyntaxFg.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_TEXT};')
				self.setSyntaxBg.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_BACKGROUND};')
				self.syntaxBgLabel.setText("Background color: <b>"+config.SCRIPT_SYNTAX_BACKGROUND+"</b>")
				self.syntaxFgLabel.setText("Text color: <b>"+config.SCRIPT_SYNTAX_BACKGROUND+"</b>")

				self.syntax_comment_color = config.SCRIPT_SYNTAX_COMMENTS
				self.setSyntaxComment.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_COMMENTS};')
				self.syntaxCommentLabel.setText("Comments: <b>"+config.SCRIPT_SYNTAX_COMMENTS+"</b>")

				self.syntax_command_color = config.SCRIPT_SYNTAX_COMMANDS
				self.setSyntaxCommand.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_COMMANDS};')
				self.syntaxCommandLabel.setText("Commands: <b>"+config.SCRIPT_SYNTAX_COMMANDS+"</b>")

				self.syntax_target_color = config.SCRIPT_SYNTAX_TARGETS
				self.setSyntaxTarget.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_TARGETS};')
				self.syntaxTargetLabel.setText("Channels: <b>"+config.SCRIPT_SYNTAX_TARGETS+"</b>")

				self.syntax_alias_color = config.SCRIPT_SYNTAX_ALIAS
				self.setSyntaxAlias.setStyleSheet(f'background-color: {config.SCRIPT_SYNTAX_ALIAS};')
				self.syntaxAliasLabel.setText("Aliases: <b>"+config.SCRIPT_SYNTAX_ALIAS+"</b>")

				self.channelTopic.setChecked(config.ENABLE_TOPIC_EDITOR)
				self.channelUserMenu.setChecked(config.ENABLE_USERLIST_MENU)
				self.menuConnection.setChecked(config.ENABLE_CONNECTION_CONTEXT)

				self.displayUserModes.setChecked(config.DISPLAY_MODES_ON_CHANNEL)

				self.servSaveLog.setChecked(config.SAVE_SERVER_LOGS)
				self.servLoadLog.setChecked(config.LOAD_SERVER_LOGS)

				self.unseen_message_color = config.UNSEEN_MESSAGE_COLOR
				self.connecting_anim_color = config.CONNECTING_ANIMATION_COLOR
				self.setConnecting.setStyleSheet(f'background-color: {config.CONNECTING_ANIMATION_COLOR};')
				self.setUnseen.setStyleSheet(f'background-color: {config.UNSEEN_MESSAGE_COLOR};')
				self.unseenLabel.setText("Unseen messages color: <b>"+config.UNSEEN_MESSAGE_COLOR+"</b>")
				self.connectingLabel.setText("Connecting color: <b>"+config.CONNECTING_ANIMATION_COLOR+"</b>")

				self.cursor_width = config.CURSOR_WIDTH
				if self.cursor_width>1:
					self.cursorWidthLabel.setText("Cursor width: <b>"+str(config.CURSOR_WIDTH)+" pixels</b>")
				else:
					self.cursorWidthLabel.setText("Cursor width: <b>"+str(config.CURSOR_WIDTH)+" pixel</b>")

				self.collapseConnection.setChecked(config.CONNECTION_DISPLAY_COLLAPSE)
				self.branchConnection.setChecked(config.CONNECTION_DISPLAY_BRANCHES)

				self.underlineConnection.setChecked(config.UNDERLINE_CURRENT_CHAT)
				self.boldConnection.setChecked(config.BOLD_CURRENT_CHAT)

				self.italicConnection.setChecked(config.ITALIC_CURRENT_CHAT)

			else:
				msg = QMessageBox(self)
				msg.setIcon(QMessageBox.Critical)
				msg.setText("Import error!")
				msg.setInformativeText(fileName+" is not a valid "+APPLICATION_NAME+" configuration file")
				msg.setWindowTitle("Error")
				msg.exec_()