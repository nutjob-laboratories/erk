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
from itertools import combinations_with_replacement
from zipfile import ZipFile
import shutil

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
from erk.widgets import *
from erk.files import *
from erk.common import *
from erk.plugins import PluginCollection,DISABLED_PLUGINS,save_disabled,PLUGIN_DIRECTORY,get_disabled
import erk.config
import erk.events
import erk.format

from erk.dialogs import(
	ComboDialog,
	JoinDialog,
	NickDialog,
	WindowSizeDialog,
	HistorySizeDialog,
	LogSizeDialog,
	FormatTextDialog,
	AboutDialog,
	MacroDialog,
	EditorDialog,
	ErrorDialog,
	ExportLogDialog,
	PrefixDialog,
	ListTimeDialog
	)

from erk.irc import(
	connect,
	connectSSL,
	reconnect,
	reconnectSSL
	)

class Erk(QMainWindow):

	# Occasionally, when restoring the main window, chat windows' text display
	# gets "zoomed in" on new text, for some reason. This prevents this from
	# being displayed to the user
	def changeEvent(self,event):
		if event.type() == QEvent.WindowStateChange:
			if event.oldState() and Qt.WindowMinimized:
				erk.events.resize_font_fix()
			elif event.oldState() == Qt.WindowNoState:
				erk.events.resize_font_fix()
			elif self.windowState() == Qt.WindowMaximized:
				erk.events.resize_font_fix()
		
		return QMainWindow.changeEvent(self, event)

	def newStyle(self,style):
		erk.events.apply_style(style)
		self.connection_display.setStyleSheet(style)

	def closeEvent(self, event):
		if not self.block_plugins:
			self.plugins.unload()
		erk.config.DEFAULT_APP_WIDTH = self.width()
		erk.config.DEFAULT_APP_HEIGHT = self.height()
		erk.config.save_settings(self.configfile)
		self.app.quit()

	def disconnect_current(self,msg=None):
		if self.current_client:
			erk.events.disconnect_from_server(self.current_client,msg)
			self.current_client = None
			if not self.block_toolbar: self.disconnect.setEnabled(False)

	def pageChange(self,index):

		window = self.stack.widget(index)

		self.current_page = window

		if hasattr(window,"client"):
			self.current_client = window.client
			if not self.block_toolbar: self.disconnect.setEnabled(True)
		else:
			self.current_client = None
			if not self.block_toolbar: self.disconnect.setEnabled(False)

		if hasattr(window,"name"):
			if window.name==MASTER_LOG_NAME:
				self.current_client = None
				if not self.block_toolbar: self.disconnect.setEnabled(False)
			else:
				self.setWindowTitle(window.name)

		if hasattr(window,"input"):
			# Set focus to the input widget
			window.input.setFocus()

		if hasattr(window,"client"): erk.events.clear_unseen(window)
		erk.events.build_connection_display(self)

	def connectionNodeSingleClicked(self,item,column):
		if erk.config.DOUBLECLICK_SWITCH: return
		if hasattr(item,"erk_widget"):
			if item.erk_widget:
				self.stack.setCurrentWidget(item.erk_widget)
				if hasattr(item,"erk_name"):
					if item.erk_name:
						self.setWindowTitle(item.erk_name)
		self.connection_display.clearSelection()

	def connectionNodeDoubleClicked(self,item):
		if not erk.config.DOUBLECLICK_SWITCH: return
		if hasattr(item,"erk_widget"):
			if item.erk_widget:
				self.stack.setCurrentWidget(item.erk_widget)
				if hasattr(item,"erk_name"):
					if item.erk_name:
						self.setWindowTitle(item.erk_name)
		self.connection_display.clearSelection()

	def start_spinner(self):
		if not self.block_toolbar: self.spinner.start()

	def stop_spinner(self):
		if not self.block_toolbar:
			self.spinner.stop()
			self.corner_widget.setIcon(QIcon(self.toolbar_icon))

	def registered(self,client):
		clean = []
		for c in self.connecting:
			host = c[0]
			port = c[1]
			if client.server==host and client.port == port:
				continue
			clean.append(c)

		self.connecting = clean

		if len(self.connecting)==0: self.stop_spinner()

	def display_load_errors(self):
		if len(self.plugins.errors())>0:
			errs = self.plugins.errors()
			if erk.config.SHOW_LOAD_ERRORS:
				total_errors = {}
				for e in errs:
					if e.package in total_errors:
						total_errors[e.package].append([e.classname,e.reason])
					else:
						total_errors[e.package] = []
						total_errors[e.package].append([e.classname,e.reason])
				
				ErrorDialog(self,total_errors)
			else:
				for e in errs:
					s = "Error loading package "+e.package+"!\n"
					s = s + e.classname+": "+e.reason
					print(s)

	def resizeEvent(self, event):
		self.winsizeMenuEntry.setText("Set window size ("+str(self.width())+" x "+str(self.height())+")")

	def __init__(self,app,info=None,block_plugins=False,block_macros=False,block_settings=False,block_toolbar=False,configfile=None,stylefile=STYLE_FILE,userfile=USER_FILE,parent=None):
		super(Erk, self).__init__(parent)

		self.app = app
		self.parent = parent

		self.editor = None

		self.quitting = []
		self.connecting = []

		self.uptimers = {}

		self.current_client = None

		self.block_plugins = block_plugins

		self.block_macros = block_macros

		self.block_settings = block_settings

		self.block_toolbar = block_toolbar

		self.fullscreen = False

		self.configfile = configfile

		self.stylefile = stylefile

		self.userfile = userfile

		erk.format.get_text_format_settings(self.stylefile)

		global DISABLED_PLUGINS
		DISABLED_PLUGINS = get_disabled(self.userfile)

		# Load application settings
		erk.config.load_settings(configfile)

		if self.block_macros: erk.config.MACROS_ENABLED = False
		if self.block_plugins: erk.config.PLUGINS_ENABLED = False

		u = get_user(self.userfile)
		self.ignore = u["ignore"]

		self.setWindowTitle(APPLICATION_NAME)
		self.setWindowIcon(QIcon(ERK_ICON))

		if erk.config.DISPLAY_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			self.font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.DISPLAY_FONT)
			self.font = f

		self.app.setFont(self.font)

		if erk.config.ALWAYS_ON_TOP:
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		self.stack = QStackedWidget(self)
		self.stack.currentChanged.connect(self.pageChange)
		self.setCentralWidget(self.stack)

		self.current_page = None

		if not self.block_toolbar:

			self.toolbar = generate_menu_toolbar(self)
			self.addToolBar(Qt.TopToolBarArea,self.toolbar)

			self.toolbar_icon = TOOLBAR_ICON
			self.corner_widget = add_toolbar_image(self.toolbar,self.toolbar_icon)
			self.spinner = QMovie(SPINNER_ANIMATION)
			self.spinner.frameChanged.connect(lambda state,b=self.corner_widget: self.corner_widget.setIcon( QIcon(self.spinner.currentPixmap()) ) )

		# Plugins
		if not self.block_plugins:
			self.plugins = PluginCollection("plugins")

			self.display_load_errors()

		# MENU TOOLBAR
		self.mainMenu = QMenu()
		self.settingsMenu = QMenu()
		self.logMenu = QMenu()
		self.helpMenu = QMenu()
		self.macroMenu = QMenu()
		self.pluginMenu = QMenu()
		self.displayMenu = QMenu()

		if not self.block_toolbar:

			self.buildToolbar()
		
		self.connection_display, self.connection_dock = buildConnectionDisplayWidget(self)

		if erk.config.CONNECTION_DISPLAY_LOCATION=="left":
			self.addDockWidget(Qt.LeftDockWidgetArea,self.connection_dock)
		elif erk.config.CONNECTION_DISPLAY_LOCATION=="right":
			self.addDockWidget(Qt.RightDockWidgetArea,self.connection_dock)

		if erk.config.CONNECTION_DISPLAY_MOVE:
			self.connection_dock.setFeatures(
				QDockWidget.DockWidgetMovable |
				QDockWidget.DockWidgetFloatable
				)
			self.connection_dock.setTitleBarWidget(None)
		else:
			self.connection_dock.setFeatures( QDockWidget.NoDockWidgetFeatures )
			self.connection_dock.setTitleBarWidget(QWidget())

		self.connection_display.installEventFilter(self)

		if erk.config.CONNECTION_DISPLAY_VISIBLE:
			self.connection_dock.show()
		else:
			self.connection_dock.hide()

		self.resize(int(erk.config.DEFAULT_APP_WIDTH),int(erk.config.DEFAULT_APP_HEIGHT))

		if info:
			self.connectToIRCServer(info)

		self.starter = QTextBrowser(self)
		self.starter.name = MASTER_LOG_NAME
		self.stack.addWidget(self.starter)

		css =  "QTextBrowser { background-image: url(" + LOGO_IMAGE + "); background-attachment: fixed; background-repeat: no-repeat; background-position: center middle; }"
		self.starter.setStyleSheet(css)

		self.starter.append("<p style=\"text-align: right;\"><small><b>Version "+APPLICATION_VERSION+ "&nbsp;&nbsp;</b></small></p>")

		self.starter.anchorClicked.connect(self.linkClicked)

	def spellcheck_language(self,setting):

		if erk.config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(UNCHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(UNCHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(UNCHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(UNCHECKED_ICON))

		erk.config.SPELLCHECK_LANGUAGE = setting
		erk.config.save_settings(self.configfile)
		erk.events.newspell_all(setting)

		if erk.config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(CHECKED_ICON))

	def buildToolbar(self):
		# mainMenu = QMenu()

		self.toolbar.clear()

		self.corner_widget = add_toolbar_image(self.toolbar,self.toolbar_icon)

		self.mainMenu.clear()

		add_toolbar_menu(self.toolbar,"IRC",self.mainMenu)

		entry = MenuAction(self,CONNECT_MENU_ICON,"Connect","Connect to an IRC server",25,self.menuCombo)
		self.mainMenu.addAction(entry)

		self.mainMenu.addSeparator()

		self.disconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		self.disconnect.triggered.connect(self.disconnect_current)
		self.mainMenu.addAction(self.disconnect)
		self.disconnect.setEnabled(False)

		self.mainMenu.addSeparator()
		
		entry = QAction(QIcon(RESTART_ICON),"Restart",self)
		entry.triggered.connect(lambda state: restart_program())
		self.mainMenu.addAction(entry)

		entry = QAction(QIcon(QUIT_ICON),"Exit",self)
		entry.triggered.connect(self.close)
		self.mainMenu.addAction(entry)

		self.displayMenu.clear()

		if not self.block_settings:

			add_toolbar_menu(self.toolbar,"Display",self.displayMenu)

			self.fontMenuEntry = QAction(QIcon(FONT_ICON),"Font",self)
			self.fontMenuEntry.triggered.connect(self.menuFont)
			self.displayMenu.addAction(self.fontMenuEntry)

			f = self.app.font()
			fs = f.toString()
			pfs = fs.split(',')
			font_name = pfs[0]
			font_size = pfs[1]

			self.fontMenuEntry.setText(f"Font ({font_name}, {font_size} pt)")

			entry = QAction(QIcon(FORMAT_ICON),"Text colors && formatting",self)
			entry.triggered.connect(lambda state,s=self: FormatTextDialog(s))
			self.displayMenu.addAction(entry)

			self.winsizeMenuEntry = QAction(QIcon(RESIZE_ICON),"Set window size",self)
			self.winsizeMenuEntry.triggered.connect(self.menuResize)
			self.displayMenu.addAction(self.winsizeMenuEntry)

			w = erk.config.DEFAULT_APP_WIDTH
			h =  erk.config.DEFAULT_APP_HEIGHT

			#self.winsizeMenuEntry.setText(f"Window size ({w} X {h})")

			self.displayMenu.addSeparator()

			self.set_ontop = QAction(QIcon(UNCHECKED_ICON),"Always on top",self)
			self.set_ontop.triggered.connect(lambda state,s="ontop": self.toggleSetting(s))
			self.displayMenu.addAction(self.set_ontop)

			if erk.config.ALWAYS_ON_TOP: self.set_ontop.setIcon(QIcon(CHECKED_ICON))

			self.set_full = QAction(QIcon(UNCHECKED_ICON),"Display full screen",self)
			self.set_full.triggered.connect(lambda state,s="fullscreen": self.toggleSetting(s))
			self.displayMenu.addAction(self.set_full)

			if self.fullscreen: self.set_full.setIcon(QIcon(CHECKED_ICON))

		# settingsMenu = QMenu()
		self.settingsMenu.clear()

		if not self.block_settings:

			add_toolbar_menu(self.toolbar,"Settings",self.settingsMenu)

			# Message display submenu

			messageMenu = self.settingsMenu.addMenu(QIcon(MESSAGE_ICON),"Messages")

			self.set_color = QAction(QIcon(UNCHECKED_ICON),"Display IRC colors",self)
			self.set_color.triggered.connect(lambda state,s="color": self.toggleSetting(s))
			messageMenu.addAction(self.set_color)

			if erk.config.DISPLAY_IRC_COLORS: self.set_color.setIcon(QIcon(CHECKED_ICON))

			self.set_links = QAction(QIcon(UNCHECKED_ICON),"Convert URLs to links",self)
			self.set_links.triggered.connect(lambda state,s="links": self.toggleSetting(s))
			messageMenu.addAction(self.set_links)

			if erk.config.CONVERT_URLS_TO_LINKS: self.set_links.setIcon(QIcon(CHECKED_ICON))

			self.set_profanity = QAction(QIcon(UNCHECKED_ICON),"Hide profanity",self)
			self.set_profanity.triggered.connect(lambda state,s="profanity": self.toggleSetting(s))
			messageMenu.addAction(self.set_profanity)

			if erk.config.FILTER_PROFANITY: self.set_profanity.setIcon(QIcon(CHECKED_ICON))

			self.set_privopen = QAction(QIcon(UNCHECKED_ICON),"Open new chat for private messages",self)
			self.set_privopen.triggered.connect(lambda state,s="privopen": self.toggleSetting(s))
			messageMenu.addAction(self.set_privopen)

			if erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS: self.set_privopen.setIcon(QIcon(CHECKED_ICON))

			self.set_chanlink = QAction(QIcon(UNCHECKED_ICON),"Convert channel names to links",self)
			self.set_chanlink.triggered.connect(lambda state,s="chanlink": self.toggleSetting(s))
			messageMenu.addAction(self.set_chanlink)

			if erk.config.CLICKABLE_CHANNELS: self.set_chanlink.setIcon(QIcon(CHECKED_ICON))

			self.set_sysprefix = QAction(QIcon(UNCHECKED_ICON),"Add prefix to system messages",self)
			self.set_sysprefix.triggered.connect(lambda state,s="sysprefix": self.toggleSetting(s))
			messageMenu.addAction(self.set_sysprefix)

			if erk.config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL: self.set_sysprefix.setIcon(QIcon(CHECKED_ICON))

			self.set_prefix_char = QAction(QIcon(PREFIX_ICON),"Set system message prefix",self)
			self.set_prefix_char.triggered.connect(lambda state,s="setsysprefix": self.toggleSetting(s))
			messageMenu.addAction(self.set_prefix_char)

			if not erk.config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL: self.set_prefix_char.setEnabled(False)

			# Channel display submenu

			channelMenu = self.settingsMenu.addMenu(QIcon(CHANNEL_ICON),"Chat displays")

			self.set_modes = QAction(QIcon(UNCHECKED_ICON),"Display channel modes",self)
			self.set_modes.triggered.connect(lambda state,s="modes": self.toggleSetting(s))
			channelMenu.addAction(self.set_modes)

			if erk.config.DISPLAY_CHANNEL_MODES: self.set_modes.setIcon(QIcon(CHECKED_ICON))

			self.set_plainusers = QAction(QIcon(UNCHECKED_ICON),"Text-only user lists",self)
			self.set_plainusers.triggered.connect(lambda state,s="plainlists": self.toggleSetting(s))
			channelMenu.addAction(self.set_plainusers)

			if erk.config.PLAIN_USER_LISTS: self.set_plainusers.setIcon(QIcon(CHECKED_ICON))

			self.set_displaystatus = QAction(QIcon(UNCHECKED_ICON),"Display status",self)
			self.set_displaystatus.triggered.connect(lambda state,s="display_status": self.toggleSetting(s))
			channelMenu.addAction(self.set_displaystatus)

			if erk.config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY: self.set_displaystatus.setIcon(QIcon(CHECKED_ICON))

			self.set_displaynick = QAction(QIcon(UNCHECKED_ICON),"Display nickname",self)
			self.set_displaynick.triggered.connect(lambda state,s="display_nick": self.toggleSetting(s))
			channelMenu.addAction(self.set_displaynick)

			if erk.config.DISPLAY_NICKNAME_ON_CHANNEL: self.set_displaynick.setIcon(QIcon(CHECKED_ICON))

			self.set_autohostmask = QAction(QIcon(UNCHECKED_ICON),"Get hostmasks on channel join",self)
			self.set_autohostmask.triggered.connect(lambda state,s="autohostmask": self.toggleSetting(s))
			channelMenu.addAction(self.set_autohostmask)

			if erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN: self.set_autohostmask.setIcon(QIcon(CHECKED_ICON))

			# Connection display submenu

			connectionDisplayMenu = self.settingsMenu.addMenu(QIcon(CONNECTION_DISPLAY_ICON),"Connection display")

			self.set_cvisible = QAction(QIcon(UNCHECKED_ICON),"Enabled",self)
			self.set_cvisible.triggered.connect(lambda state,s="cvisible": self.toggleSetting(s))
			connectionDisplayMenu.addAction(self.set_cvisible)

			if erk.config.CONNECTION_DISPLAY_VISIBLE: self.set_cvisible.setIcon(QIcon(CHECKED_ICON))

			self.set_float = QAction(QIcon(UNCHECKED_ICON),"Floatable",self)
			self.set_float.triggered.connect(lambda state,s="float": self.toggleSetting(s))
			connectionDisplayMenu.addAction(self.set_float)

			if erk.config.CONNECTION_DISPLAY_MOVE: self.set_float.setIcon(QIcon(CHECKED_ICON))

			self.set_uptime = QAction(QIcon(UNCHECKED_ICON),"Show uptimes",self)
			self.set_uptime.triggered.connect(lambda state,s="uptime": self.toggleSetting(s))
			connectionDisplayMenu.addAction(self.set_uptime)

			if erk.config.DISPLAY_CONNECTION_UPTIME: self.set_uptime.setIcon(QIcon(CHECKED_ICON))

			self.set_doubleclickswitch = QAction(QIcon(UNCHECKED_ICON),"Double click to switch chats",self)
			self.set_doubleclickswitch.triggered.connect(lambda state,s="dcswitch": self.toggleSetting(s))
			connectionDisplayMenu.addAction(self.set_doubleclickswitch)

			if erk.config.DOUBLECLICK_SWITCH: self.set_doubleclickswitch.setIcon(QIcon(CHECKED_ICON))

			self.set_connectexpand = QAction(QIcon(UNCHECKED_ICON),"Expand server on connect",self)
			self.set_connectexpand.triggered.connect(lambda state,s="connexpand": self.toggleSetting(s))
			connectionDisplayMenu.addAction(self.set_connectexpand)

			if erk.config.EXPAND_SERVER_ON_CONNECT: self.set_connectexpand.setIcon(QIcon(CHECKED_ICON))

			connectionDisplayMenu.addSeparator()

			self.set_location = QAction(QIcon(RIGHT_ICON),"Display on left",self)
			self.set_location.triggered.connect(lambda state,s="location": self.toggleSetting(s))
			connectionDisplayMenu.addAction(self.set_location)

			if erk.config.CONNECTION_DISPLAY_LOCATION=="right":
				self.set_location.setText("Display on left")
				self.set_location.setIcon(QIcon(LEFT_ICON))
			else:
				self.set_location.setText("Display on right")
				self.set_location.setIcon(QIcon(RIGHT_ICON))

			if not erk.config.CONNECTION_DISPLAY_VISIBLE:
				self.set_float.setEnabled(False)
				self.set_uptime.setEnabled(False)
				self.set_doubleclickswitch.setEnabled(False)
				self.set_location.setEnabled(False)

			# Autocomplete submenu

			autocompleteMenu = self.settingsMenu.addMenu(QIcon(AUTOCOMPLETE_ICON),"Autocomplete")

			self.set_autonick = QAction(QIcon(UNCHECKED_ICON),"Nicknames",self)
			self.set_autonick.triggered.connect(lambda state,s="autonick": self.toggleSetting(s))
			autocompleteMenu.addAction(self.set_autonick)

			if erk.config.AUTOCOMPLETE_NICKNAMES: self.set_autonick.setIcon(QIcon(CHECKED_ICON))

			self.set_autocmd = QAction(QIcon(UNCHECKED_ICON),"Commands",self)
			self.set_autocmd.triggered.connect(lambda state,s="autocmd": self.toggleSetting(s))
			autocompleteMenu.addAction(self.set_autocmd)

			if erk.config.AUTOCOMPLETE_COMMANDS: self.set_autocmd.setIcon(QIcon(CHECKED_ICON))

			self.set_autoemoji = QAction(QIcon(UNCHECKED_ICON),"Emoji shortcodes",self)
			self.set_autoemoji.triggered.connect(lambda state,s="autoemoji": self.toggleSetting(s))
			autocompleteMenu.addAction(self.set_autoemoji)

			if erk.config.AUTOCOMPLETE_EMOJI: self.set_autoemoji.setIcon(QIcon(CHECKED_ICON))

			# Spellcheck submenu

			spellcheckMenu = self.settingsMenu.addMenu(QIcon(SPELLCHECK_ICON),"Spellcheck")

			self.set_spellcheck = QAction(QIcon(UNCHECKED_ICON),"Enabled",self)
			self.set_spellcheck.triggered.connect(lambda state,s="spellcheck": self.toggleSetting(s))
			spellcheckMenu.addAction(self.set_spellcheck)

			if erk.config.SPELLCHECK_INPUT: self.set_spellcheck.setIcon(QIcon(CHECKED_ICON))

			self.set_spellnicks = QAction(QIcon(UNCHECKED_ICON),"Ignore nicknames",self)
			self.set_spellnicks.triggered.connect(lambda state,s="spellnicks": self.toggleSetting(s))
			spellcheckMenu.addAction(self.set_spellnicks)

			if erk.config.SPELLCHECK_IGNORE_NICKS: self.set_spellnicks.setIcon(QIcon(CHECKED_ICON))

			spellcheckMenu.addSeparator()

			self.spell_en = QAction(QIcon(UNCHECKED_ICON),"English",self)
			self.spell_en.triggered.connect(lambda state,s="en": self.spellcheck_language(s))
			spellcheckMenu.addAction(self.spell_en)

			self.spell_fr = QAction(QIcon(UNCHECKED_ICON),"French",self)
			self.spell_fr.triggered.connect(lambda state,s="fr": self.spellcheck_language(s))
			spellcheckMenu.addAction(self.spell_fr)

			self.spell_es = QAction(QIcon(UNCHECKED_ICON),"Spanish",self)
			self.spell_es.triggered.connect(lambda state,s="es": self.spellcheck_language(s))
			spellcheckMenu.addAction(self.spell_es)

			self.spell_de = QAction(QIcon(UNCHECKED_ICON),"German",self)
			self.spell_de.triggered.connect(lambda state,s="de": self.spellcheck_language(s))
			spellcheckMenu.addAction(self.spell_de)

			if erk.config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(CHECKED_ICON))
			if erk.config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(CHECKED_ICON))
			if erk.config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(CHECKED_ICON))
			if erk.config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(CHECKED_ICON))

			if not erk.config.SPELLCHECK_INPUT:
				self.spell_en.setEnabled(False)
				self.spell_fr.setEnabled(False)
				self.spell_es.setEnabled(False)
				self.spell_de.setEnabled(False)

			timestampMenu = self.settingsMenu.addMenu(QIcon(TIMESTAMP_ICON),"Timestamps")

			self.set_timestamps = QAction(QIcon(UNCHECKED_ICON),"Display",self)
			self.set_timestamps.triggered.connect(lambda state,s="timestamp": self.toggleSetting(s))
			timestampMenu.addAction(self.set_timestamps)

			if erk.config.DISPLAY_TIMESTAMP: self.set_timestamps.setIcon(QIcon(CHECKED_ICON))

			self.set_24hr = QAction(QIcon(UNCHECKED_ICON),"Use 24hr clock",self)
			self.set_24hr.triggered.connect(lambda state,s="24hr": self.toggleSetting(s))
			timestampMenu.addAction(self.set_24hr)

			if erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS: self.set_24hr.setIcon(QIcon(CHECKED_ICON))

			self.set_seconds = QAction(QIcon(UNCHECKED_ICON),"Show seconds",self)
			self.set_seconds.triggered.connect(lambda state,s="tsseconds": self.toggleSetting(s))
			timestampMenu.addAction(self.set_seconds)

			if erk.config.DISPLAY_TIMESTAMP_SECONDS: self.set_24hr.setIcon(QIcon(CHECKED_ICON))

			# Entry submenu

			entryMenu = self.settingsMenu.addMenu(QIcon(ENTRY_ICON),"Input")

			self.set_emoji = QAction(QIcon(UNCHECKED_ICON),"Use emoji shortcodes",self)
			self.set_emoji.triggered.connect(lambda state,s="emoji": self.toggleSetting(s))
			entryMenu.addAction(self.set_emoji)

			if erk.config.USE_EMOJIS: self.set_emoji.setIcon(QIcon(CHECKED_ICON))

			self.set_history = QAction(QIcon(UNCHECKED_ICON),"Track input history",self)
			self.set_history.triggered.connect(lambda state,s="history": self.toggleSetting(s))
			entryMenu.addAction(self.set_history)

			if erk.config.TRACK_COMMAND_HISTORY: self.set_history.setIcon(QIcon(CHECKED_ICON))

			self.historySize = QAction(QIcon(HISTORY_LENGTH_ICON),"Set history length",self)
			self.historySize.triggered.connect(self.menuHistoryLength)
			entryMenu.addAction(self.historySize)

			self.historySize.setText("Set history length ("+str(erk.config.HISTORY_LENGTH)+" lines)")

			# Hide menu

			hideMenu = self.settingsMenu.addMenu(QIcon(HIDE_ICON),"Hide Messages")

			self.hide_mode = QAction(QIcon(UNCHECKED_ICON),"Mode",self)
			self.hide_mode.triggered.connect(lambda state,s="hide_mode": self.toggleSetting(s))
			hideMenu.addAction(self.hide_mode)

			if erk.config.HIDE_MODE_DISPLAY: self.hide_mode.setIcon(QIcon(CHECKED_ICON))

			self.hide_topic = QAction(QIcon(UNCHECKED_ICON),"Topic",self)
			self.hide_topic.triggered.connect(lambda state,s="hide_topic": self.toggleSetting(s))
			hideMenu.addAction(self.hide_topic)

			if erk.config.HIDE_TOPIC_MESSAGE: self.hide_topic.setIcon(QIcon(CHECKED_ICON))

			self.hide_quit = QAction(QIcon(UNCHECKED_ICON),"Quit",self)
			self.hide_quit.triggered.connect(lambda state,s="hide_quit": self.toggleSetting(s))
			hideMenu.addAction(self.hide_quit)

			if erk.config.HIDE_QUIT_MESSAGE: self.hide_quit.setIcon(QIcon(CHECKED_ICON))

			self.hide_nick = QAction(QIcon(UNCHECKED_ICON),"Nick",self)
			self.hide_nick.triggered.connect(lambda state,s="hide_nick": self.toggleSetting(s))
			hideMenu.addAction(self.hide_nick)

			if erk.config.HIDE_NICK_MESSAGE: self.hide_nick.setIcon(QIcon(CHECKED_ICON))

			self.hide_invite = QAction(QIcon(UNCHECKED_ICON),"Invite",self)
			self.hide_invite.triggered.connect(lambda state,s="hide_invite": self.toggleSetting(s))
			hideMenu.addAction(self.hide_invite)

			if erk.config.HIDE_INVITE_MESSAGE: self.hide_invite.setIcon(QIcon(CHECKED_ICON))

			self.hide_part = QAction(QIcon(UNCHECKED_ICON),"Part",self)
			self.hide_part.triggered.connect(lambda state,s="hide_part": self.toggleSetting(s))
			hideMenu.addAction(self.hide_part)

			if erk.config.HIDE_PART_MESSAGE: self.hide_part.setIcon(QIcon(CHECKED_ICON))

			self.hide_join = QAction(QIcon(UNCHECKED_ICON),"Join",self)
			self.hide_join.triggered.connect(lambda state,s="hide_join": self.toggleSetting(s))
			hideMenu.addAction(self.hide_join)

			if erk.config.HIDE_JOIN_MESSAGE: self.hide_join.setIcon(QIcon(CHECKED_ICON))

			# Miscellaneous settings

			#self.settingsMenu.addSeparator()

			miscMenu = self.settingsMenu.addMenu(QIcon(MISC_ICON),"Miscellaneous")

			self.set_autoinvite = QAction(QIcon(UNCHECKED_ICON),"Join on channel invite",self)
			self.set_autoinvite.triggered.connect(lambda state,s="autoinvite": self.toggleSetting(s))
			miscMenu.addAction(self.set_autoinvite)

			if erk.config.JOIN_ON_INVITE: self.set_autoinvite.setIcon(QIcon(CHECKED_ICON))

			self.set_autoswitch = QAction(QIcon(UNCHECKED_ICON),"Switch to new chats",self)
			self.set_autoswitch.triggered.connect(lambda state,s="autoswitch": self.toggleSetting(s))
			miscMenu.addAction(self.set_autoswitch)

			if erk.config.SWITCH_TO_NEW_WINDOWS: self.set_autoswitch.setIcon(QIcon(CHECKED_ICON))

			miscMenu.addSeparator()

			self.set_fetchlist = QAction(QIcon(UNCHECKED_ICON),"Retrieve channel list on connect",self)
			self.set_fetchlist.triggered.connect(lambda state,s="autofetch": self.toggleSetting(s))
			miscMenu.addAction(self.set_fetchlist)

			if erk.config.AUTOMATICALLY_FETCH_CHANNEL_LIST: self.set_fetchlist.setIcon(QIcon(CHECKED_ICON))


			self.fetch_time = QAction(QIcon(TIMESTAMP_ICON),"Set list refresh",self)
			self.fetch_time.triggered.connect(self.menuSetListTime)
			miscMenu.addAction(self.fetch_time)

			self.fetch_time.setText("Set list refresh ("+str(erk.config.CHANNEL_LIST_REFRESH_FREQUENCY)+" seconds)")

			miscMenu.addSeparator()

			self.set_macroenable = QAction(QIcon(UNCHECKED_ICON),"Enable macros",self)
			self.set_macroenable.triggered.connect(lambda state,s="enablemacros": self.toggleSetting(s))
			miscMenu.addAction(self.set_macroenable)

			if erk.config.MACROS_ENABLED: self.set_macroenable.setIcon(QIcon(CHECKED_ICON))
			if self.block_macros: self.set_macroenable.setIcon(QIcon(UNCHECKED_ICON))

			entry = QAction(QIcon(UNCHECKED_ICON),"Enable plugins",self)
			entry.triggered.connect(lambda state,s="pluginenable": self.toggleSetting(s))
			miscMenu.addAction(entry)

			if erk.config.PLUGINS_ENABLED: entry.setIcon(QIcon(CHECKED_ICON))
			if self.block_plugins: entry.setIcon(QIcon(UNCHECKED_ICON))

			# Log menu

			# logMenu = QMenu()
			self.logMenu.clear()

			add_toolbar_menu(self.toolbar,"Logs",self.logMenu)

			channelMenu = self.logMenu.addMenu(QIcon(CHANNEL_ICON),"Channels")

			self.set_chanlogsave = QAction(QIcon(UNCHECKED_ICON),"Automatic save",self)
			self.set_chanlogsave.triggered.connect(lambda state,s="chanlogsave": self.toggleSetting(s))
			channelMenu.addAction(self.set_chanlogsave)

			if erk.config.SAVE_CHANNEL_LOGS: self.set_chanlogsave.setIcon(QIcon(CHECKED_ICON))

			self.set_chanlogload = QAction(QIcon(UNCHECKED_ICON),"Automatic load",self)
			self.set_chanlogload.triggered.connect(lambda state,s="chanlogload": self.toggleSetting(s))
			channelMenu.addAction(self.set_chanlogload)

			if erk.config.LOAD_CHANNEL_LOGS: self.set_chanlogload.setIcon(QIcon(CHECKED_ICON))

			privateMenu = self.logMenu.addMenu(QIcon(NICK_ICON),"Private messages")

			self.set_privlogsave = QAction(QIcon(UNCHECKED_ICON),"Automatic save",self)
			self.set_privlogsave.triggered.connect(lambda state,s="privlogsave": self.toggleSetting(s))
			privateMenu.addAction(self.set_privlogsave)

			if erk.config.SAVE_PRIVATE_LOGS: self.set_privlogsave.setIcon(QIcon(CHECKED_ICON))

			self.set_privlogload = QAction(QIcon(UNCHECKED_ICON),"Automatic load",self)
			self.set_privlogload.triggered.connect(lambda state,s="privlogload": self.toggleSetting(s))
			privateMenu.addAction(self.set_privlogload)

			if erk.config.LOAD_PRIVATE_LOGS: self.set_privlogload.setIcon(QIcon(CHECKED_ICON))

			self.logMenu.addSeparator()

			self.set_marklogend = QAction(QIcon(UNCHECKED_ICON),"Mark end of loaded log",self)
			self.set_marklogend.triggered.connect(lambda state,s="marklogend": self.toggleSetting(s))
			self.logMenu.addAction(self.set_marklogend)

			if erk.config.MARK_END_OF_LOADED_LOG: self.set_marklogend.setIcon(QIcon(CHECKED_ICON))

			self.set_logresume = QAction(QIcon(UNCHECKED_ICON),"Display log resume date/time",self)
			self.set_logresume.triggered.connect(lambda state,s="logresume": self.toggleSetting(s))
			self.logMenu.addAction(self.set_logresume)

			if erk.config.DISPLAY_CHAT_RESUME_DATE_TIME: self.set_logresume.setIcon(QIcon(CHECKED_ICON))

			self.logSize = QAction(QIcon(LOG_ICON),"Set log display size",self)
			self.logSize.triggered.connect(self.menuLogSize)
			self.logMenu.addAction(self.logSize)

			self.logSize.setText("Set log display size ("+str(erk.config.LOG_LOAD_SIZE_MAX)+" lines)")

			self.logMenu.addSeparator()

			entry = QAction(QIcon(EXPORT_ICON),"Export log",self)
			entry.triggered.connect(self.menuExportLog)
			self.logMenu.addAction(entry)

		# Macro menu

		# self.macroMenu = QMenu()
		self.macroMenu.clear()

		if not self.block_macros:
			add_toolbar_menu(self.toolbar,"Macros",self.macroMenu)

			self.rebuildMacroMenu()

		# Plugin menu
		self.pluginMenu.clear()

		if not self.block_plugins:

			add_toolbar_menu(self.toolbar,"Plugins",self.pluginMenu)

			self.rebuildPluginMenu()

		# Help menu

		# helpMenu = QMenu()
		self.helpMenu.clear()

		add_toolbar_menu(self.toolbar,"Help",self.helpMenu)

		self.about = QAction(QIcon(ABOUT_ICON),"About",self)
		self.about.triggered.connect(self.menuAbout)
		self.helpMenu.addAction(self.about)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(DOCUMENT_ICON),"RFC 1459",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc1459": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(DOCUMENT_ICON),"RFC 2812",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc2812": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(LINK_ICON),"List of emoji shortcodes",self)
		helpLink.triggered.connect(lambda state,u="https://www.webfx.com/tools/emoji-cheat-sheet/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		# End of menus
		end_toolbar_menu(self.toolbar)

	def menuExportLog(self):
		d = ExportLogDialog(self)
		if d:
			elog = d[0]
			dlog = d[1]
			llog = d[2]
			do_json = d[3]
			do_epoch = d[4]
			if not do_json:
				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(self,"Save export As...",INSTALL_DIRECTORY,"Text File (*.txt);;All Files (*)", options=options)
				if fileName:
					extension = os.path.splitext(fileName)[1]
					if extension.lower()!='txt': fileName = fileName + ".txt"
					dump = dumpLog(elog,dlog,llog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()
			else:
				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(self,"Save export As...",INSTALL_DIRECTORY,"JSON File (*.json);;All Files (*)", options=options)
				if fileName:
					extension = os.path.splitext(fileName)[1]
					if extension.lower()!='json': fileName = fileName + ".json"
					#dump = dumpLog(elog,dlog,llog)
					dump = dumpLogJson(elog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()

	def rebuildPluginMenu(self):

		self.pluginMenu.clear()

		if not hasattr(self,"plugins"):
			self.plugins = PluginCollection("plugins")
			self.display_load_errors()

		self.pluginMenu.addSeparator()

		if len(self.plugins.plugins)==0:

			l1 = QLabel("<br>&nbsp;<b>No plugins installed</b>&nbsp;")
			l1.setAlignment(Qt.AlignCenter)
			entry = QWidgetAction(self)
			entry.setDefaultWidget(l1)
			self.pluginMenu.addAction(entry)

			self.pluginMenu.addSeparator()

			#return
		else:
			s = textSeparator(self,"Installed plugins")
			self.pluginMenu.addAction(s)

		plist = {}

		for p in self.plugins.plugins:

			if p._package in plist:
				plist[p._package].append(p)
			else:
				plist[p._package] = []
				plist[p._package].append(p)

		for pack in plist:

			m = self.pluginMenu.addMenu(QIcon(PACKAGE_ICON),pack)

			for p in plist[pack]: plugdir = p._packdir
			plugtype = "package"

			if plugdir==PLUGIN_DIRECTORY:
				plugdir = p.__file__
				plugtype = "plugin"
				m.setIcon(QIcon(PLUGIN_ICON))

			if not erk.config.PLUGINS_ENABLED:
				m.setEnabled(False)

			for p in plist[pack]:

				if os.path.isfile(p._packicon): m.setIcon(QIcon(p._packicon))

				if os.path.isfile(p._icon):
					icon = p._icon
				else:
					icon = PLUGIN_ICON

				args = []
				if p.version:
					PLUGIN_VERSION = p.version + " "
				else:
					PLUGIN_VERSION = ''

				if p.author and p.author!="Unknown":
					args.append(p.author)

				if p.website:
					args.append(f"<a href=\"{p.website}\">Website</a>")

				if p.source:
					args.append(f"<a href=\"{p.source}\">Source Code</a>")

				max_length = 40
				if len(p.description)>max_length:
					if len(p.description)>=max_length+3:
						offset = max_length-3
					elif len(p.description)==max_length+2:
						offset = max_length-2
					elif len(p.description)==max_length+1:
						offset = max_length-1
					else:
						offset = max_length
					display_description = p.description[0:offset]+"..."
				else:
					display_description = p.description


				if len(args)==3:
					entry = Menu5Action(self,icon,p.name+" "+PLUGIN_VERSION,display_description,*args,25)
				elif len(args)==2:
					entry = Menu4Action(self,icon,p.name+" "+PLUGIN_VERSION,display_description,*args,25)
				elif len(args)==1:
					entry = Menu3Action(self,icon,p.name+" "+PLUGIN_VERSION,display_description,*args,25)
				else:
					entry = MenuNoAction(self,icon,p.name+" "+PLUGIN_VERSION,display_description,25)

				m.addAction(entry)

				if erk.config.DEVELOPER_MODE:

					entry = QAction(QIcon(EDITOR_ICON),"Edit "+os.path.basename(p.__file__),self)
					entry.triggered.connect(lambda state,f=p.__file__: self.editPlugin(f))
					m.addAction(entry)

					if hasattr(p,"load"):

						entry = QAction(QIcon(LAMBDA_ICON),"Execute load()",self)
						entry.triggered.connect(lambda state,f=p.name: self.plugins.forceload(f))
						m.addAction(entry)

					if hasattr(p,"unload"):

						entry = QAction(QIcon(LAMBDA_ICON),"Execute unload()",self)
						entry.triggered.connect(lambda state,f=p.name: self.plugins.forceunload(f))
						m.addAction(entry)

				if p.name in DISABLED_PLUGINS:
					enabled = False
					entry = QAction(QIcon(UNCHECKED_ICON),"Enabled",self)
				else:
					enabled = True
					entry = QAction(QIcon(CHECKED_ICON),"Enabled",self)

				entry.triggered.connect(lambda state,n=p.name: self.toggle_plugin(n))
				m.addAction(entry)

				m.addSeparator()

			entry = QAction(QIcon(UNINSTALL_ICON),"Uninstall \""+pack+"\"",self)
			entry.triggered.connect(lambda state,f=plugdir,p=pack: self.uninstall_plugin(f,p))
			m.addAction(entry)

		self.pluginMenu.addSeparator()

		m = self.pluginMenu.addMenu(QIcon(OPTIONS_ICON),"Options && tools")

		entry = MenuAction(self,MENU_INSTALL_ICON,"Install","Install a plugin",25,self.menuInstall)
		m.addAction(entry)

		if not erk.config.PLUGINS_ENABLED:
			entry.setEnabled(False)

		entry = MenuAction(self,MENU_EDITOR_ICON,"Editor","Create or edit plugins",25,self.menuEditor)
		m.addAction(entry)

		if not erk.config.PLUGINS_ENABLED:
			entry.setEnabled(False)

		m.addSeparator()

		entry = QAction(QIcon(UNCHECKED_ICON),"Development mode",self)
		entry.triggered.connect(lambda state,s="plugindev": self.toggleSetting(s))
		# self.pluginMenu.addAction(entry)
		m.addAction(entry)

		if erk.config.DEVELOPER_MODE: entry.setIcon(QIcon(CHECKED_ICON))

		if not erk.config.PLUGINS_ENABLED:
			entry.setEnabled(False)

		entry = QAction(QIcon(UNCHECKED_ICON),"Show plugin load errors",self)
		entry.triggered.connect(lambda state,s="showplugerrors": self.toggleSetting(s))
		#self.pluginMenu.addAction(entry)
		m.addAction(entry)

		if erk.config.SHOW_LOAD_ERRORS: entry.setIcon(QIcon(CHECKED_ICON))

		if not erk.config.PLUGINS_ENABLED:
			entry.setEnabled(False)

		entry = QAction(QIcon(DIRECTORY_ICON),"Open plugin directory",self)
		entry.triggered.connect(lambda state,s=PLUGIN_DIRECTORY: os.startfile(s))
		#self.pluginMenu.addAction(entry)
		m.addAction(entry)

		if not erk.config.PLUGINS_ENABLED:
			entry.setEnabled(False)

		entry = QAction(QIcon(RESTART_ICON),"Reload plugins",self)
		entry.triggered.connect(self.menuReloadPlugins)
		self.pluginMenu.addAction(entry)

		if not erk.config.PLUGINS_ENABLED:
			entry.setEnabled(False)

	def uninstall_plugin(self,directory,upack):

		# Find the pack we're uninstalling
		plist = {}

		for p in self.plugins.plugins:

			if p._package in plist:
				plist[p._package].append(p)
			else:
				plist[p._package] = []
				plist[p._package].append(p)

		for pack in plist:
			if pack==upack:
				# Found it!
				for p in plist[pack]:
					# Execute unload()
					self.plugins.uninstall_forceunload(p.name)

		if os.path.isdir(directory):
			shutil.rmtree(directory)
		elif os.path.isfile(directory):
			os.remove(directory)

		self.plugins.reload_plugins(True)
		self.rebuildPluginMenu()

	def menuInstall(self):
		# PLUGIN_DIRECTORY
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Select Plugin Package", None,"Zip File (*.zip);;All Files (*)", options=options)
		if fileName:
			with ZipFile(fileName,'r') as zipObj:
				zipObj.extractall(PLUGIN_DIRECTORY)
			self.plugins.reload_plugins(True)
			self.rebuildPluginMenu()

	def menuInstallMacro(self):
		# erk.macros.MACRO_DIRECTORY
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Select Macro", None,"JSON File (*.json);;All Files (*)", options=options)
		if fileName:

			mfile = os.path.basename(fileName)
			outfile = os.path.join(erk.macros.MACRO_DIRECTORY, mfile)
			
			shutil.copy(fileName, outfile)

			self.menuReloadMacros()
			self.menuReloadPlugins()


	def menuEditor(self):
		x = EditorDialog(self,None,None,self.configfile)
		w = erk.config.DEFAULT_APP_WIDTH
		h = erk.config.DEFAULT_APP_HEIGHT
		x.resize(w,h)
		x.show()

	def editPlugin(self,filename):
		x = EditorDialog(self,filename,None,self.configfile)
		w = erk.config.DEFAULT_APP_WIDTH
		h = erk.config.DEFAULT_APP_HEIGHT
		x.resize(w,h)
		x.show()

	def toggle_plugin(self,name):
		if name in DISABLED_PLUGINS:
			DISABLED_PLUGINS.remove(name)
		else:
			DISABLED_PLUGINS.append(name)
		save_disabled(self.userfile)
		self.plugins.load()
		self.rebuildPluginMenu()

	def menuReloadPlugins(self):
		self.plugins.reset_errors()
		self.plugins.reload_plugins(True)

		self.display_load_errors()

		self.rebuildPluginMenu()

	def create_new_macro(self):
		MacroDialog(self)

	def open_macro_dir(self):
		os.startfile(erk.macros.MACRO_DIRECTORY)

	def rebuildMacroMenu(self):

		self.macroMenu.clear()

		# self.macroMenu.addSeparator()

		if len(erk.macros.MACROS)>0:

			s = textSeparator(self,"Installed macros")
			self.macroMenu.addAction(s)

			for m in erk.macros.MACROS:
				trigger = m["trigger"]
				filename = m["filename"]

				entry = QAction(QIcon(MACRO_FILE_ICON),trigger,self)
				entry.triggered.connect(lambda state,s=self,f=filename: MacroDialog(s,f))
				self.macroMenu.addAction(entry)

				if not erk.config.MACROS_ENABLED: entry.setEnabled(False)

			self.macroMenu.addSeparator()

		else:
			l1 = QLabel("<br>&nbsp;<b>No macros installed</b>&nbsp;")
			l1.setAlignment(Qt.AlignCenter)
			entry = QWidgetAction(self)
			entry.setDefaultWidget(l1)
			self.macroMenu.addAction(entry)

			self.macroMenu.addSeparator()

		m = self.macroMenu.addMenu(QIcon(OPTIONS_ICON),"Options && tools")

		entry = MenuAction(self,MENU_MACRO_ICON,"New macro","Create a new macro",25,self.create_new_macro)
		m.addAction(entry)

		if not erk.config.MACROS_ENABLED:
			entry.setEnabled(False)

		m.addSeparator()

		ircMenu_Macro = QAction(QIcon(DIRECTORY_ICON),"Open macro directory",self)
		ircMenu_Macro.triggered.connect(lambda state,s=erk.macros.MACRO_DIRECTORY: os.startfile(s))
		m.addAction(ircMenu_Macro)

		if not erk.config.MACROS_ENABLED: ircMenu_Macro.setEnabled(False)

		ircMenu_Macro = QAction(QIcon(RESTART_ICON),"Reload macros",self)
		ircMenu_Macro.triggered.connect(self.menuReloadMacros)
		self.macroMenu.addAction(ircMenu_Macro)

		if not erk.config.MACROS_ENABLED: ircMenu_Macro.setEnabled(False)

	def menuReloadMacros(self):
		erk.macros.load_macros()
		self.rebuildMacroMenu()

	def toggleSetting(self,setting):

		if setting=="hide_join":
			if erk.config.HIDE_JOIN_MESSAGE:
				erk.config.HIDE_JOIN_MESSAGE = False
				self.hide_join.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.HIDE_JOIN_MESSAGE = True
				self.hide_join.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="hide_part":
			if erk.config.HIDE_PART_MESSAGE:
				erk.config.HIDE_PART_MESSAGE = False
				self.hide_part.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.HIDE_PART_MESSAGE = True
				self.hide_part.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="hide_invite":
			if erk.config.HIDE_INVITE_MESSAGE:
				erk.config.HIDE_INVITE_MESSAGE = False
				self.hide_invite.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.HIDE_INVITE_MESSAGE = True
				self.hide_invite.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="hide_nick":
			if erk.config.HIDE_NICK_MESSAGE:
				erk.config.HIDE_NICK_MESSAGE = False
				self.hide_nick.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.HIDE_NICK_MESSAGE = True
				self.hide_nick.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="hide_quit":
			if erk.config.HIDE_QUIT_MESSAGE:
				erk.config.HIDE_QUIT_MESSAGE = False
				self.hide_quit.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.HIDE_QUIT_MESSAGE = True
				self.hide_quit.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="hide_topic":
			if erk.config.HIDE_TOPIC_MESSAGE:
				erk.config.HIDE_TOPIC_MESSAGE = False
				self.hide_topic.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.HIDE_TOPIC_MESSAGE = True
				self.hide_topic.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="hide_mode":
			if erk.config.HIDE_MODE_DISPLAY:
				erk.config.HIDE_MODE_DISPLAY = False
				self.hide_mode.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.HIDE_MODE_DISPLAY = True
				self.hide_mode.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="autofetch":
			if erk.config.AUTOMATICALLY_FETCH_CHANNEL_LIST:
				erk.config.AUTOMATICALLY_FETCH_CHANNEL_LIST = False
				self.set_fetchlist.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.AUTOMATICALLY_FETCH_CHANNEL_LIST = True
				self.set_fetchlist.setIcon(QIcon(CHECKED_ICON))

				for c in erk.events.fetch_connections():
					if c.last_fetch < c.uptime:
						c.sendLine("LIST")

			erk.config.save_settings(self.configfile)
			return

		if setting=="setsysprefix":
			n = PrefixDialog()
			if n:
				if len(n.strip())>0:
					erk.config.SYSTEM_MESSAGE_PREFIX = n
					erk.config.save_settings(self.configfile)
					erk.events.rerender_all()
			return


		if setting=="chanlink":
			if erk.config.CLICKABLE_CHANNELS:
				erk.config.CLICKABLE_CHANNELS = False
				self.set_chanlink.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.CLICKABLE_CHANNELS = True
				self.set_chanlink.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return


		if setting=="autoinvite":
			if erk.config.JOIN_ON_INVITE:
				erk.config.JOIN_ON_INVITE = False
				self.set_autoinvite.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.JOIN_ON_INVITE = True
				self.set_autoinvite.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="tsseconds":
			if erk.config.DISPLAY_TIMESTAMP_SECONDS:
				erk.config.DISPLAY_TIMESTAMP_SECONDS = False
				self.set_seconds.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_TIMESTAMP_SECONDS = True
				self.set_seconds.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="showplugerrors":
			if erk.config.SHOW_LOAD_ERRORS:
				erk.config.SHOW_LOAD_ERRORS = False
			else:
				erk.config.SHOW_LOAD_ERRORS = True
			erk.config.save_settings(self.configfile)
			self.rebuildPluginMenu()
			return

		if setting=="fullscreen":
			if self.fullscreen:
				self.fullscreen = False
				self.showNormal()
				self.set_full.setIcon(QIcon(UNCHECKED_ICON))
			else:
				self.fullscreen = True
				self.showFullScreen()
				self.set_full.setIcon(QIcon(CHECKED_ICON))
			return

		if setting=="ontop":
			if erk.config.ALWAYS_ON_TOP:
				erk.config.ALWAYS_ON_TOP = False
				self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
				self.set_ontop.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.ALWAYS_ON_TOP = True
				self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
				self.set_ontop.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			self.show()
			return

		if setting=="plugindev":
			if erk.config.DEVELOPER_MODE:
				erk.config.DEVELOPER_MODE = False
			else:
				erk.config.DEVELOPER_MODE = True
			erk.config.save_settings(self.configfile)
			self.rebuildPluginMenu()
			return

		# if setting=="enablemacros":
		# 	if erk.config.MACROS_ENABLED:
		# 		erk.config.MACROS_ENABLED = False
		# 		self.set_macroenable.setIcon(QIcon(UNCHECKED_ICON))
		# 	else:
		# 		erk.config.MACROS_ENABLED = True
		# 		self.set_macroenable.setIcon(QIcon(CHECKED_ICON))
		# 	erk.config.save_settings(self.configfile)
		# 	self.rebuildMacroMenu()
		# 	return

		if setting=="enablemacros":
			if erk.config.MACROS_ENABLED:
				erk.config.MACROS_ENABLED = False
				#self.set_macroenable.setIcon(QIcon(UNCHECKED_ICON))
				self.block_macros = True
			else:
				erk.config.MACROS_ENABLED = True
				#self.set_macroenable.setIcon(QIcon(CHECKED_ICON))
				self.block_macros = False
			erk.config.save_settings(self.configfile)
			self.rebuildMacroMenu()
			self.buildToolbar()
			return

		# if setting=="pluginenable":
		# 	if erk.config.PLUGINS_ENABLED:
		# 		erk.config.PLUGINS_ENABLED = False
		# 	else:
		# 		erk.config.PLUGINS_ENABLED = True
		# 	erk.config.save_settings(self.configfile)
		# 	self.rebuildPluginMenu()
		# 	return

		if setting=="pluginenable":
			if erk.config.PLUGINS_ENABLED:
				erk.config.PLUGINS_ENABLED = False
				self.block_plugins = True
			else:
				erk.config.PLUGINS_ENABLED = True
				self.block_plugins = False
			erk.config.save_settings(self.configfile)
			self.rebuildPluginMenu()
			self.buildToolbar()
			return

		if setting=="sysprefix":
			if erk.config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL:
				erk.config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL = False
				self.set_sysprefix.setIcon(QIcon(UNCHECKED_ICON))
				self.set_prefix_char.setEnabled(False)
			else:
				erk.config.MARK_SYSTEM_MESSAGES_WITH_SYMBOL = True
				self.set_sysprefix.setIcon(QIcon(CHECKED_ICON))
				self.set_prefix_char.setEnabled(True)
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="privlogsave":
			if erk.config.SAVE_PRIVATE_LOGS:
				erk.config.SAVE_PRIVATE_LOGS = False
				self.set_privlogsave.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.SAVE_PRIVATE_LOGS = True
				self.set_privlogsave.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="privlogload":
			if erk.config.LOAD_PRIVATE_LOGS:
				erk.config.LOAD_PRIVATE_LOGS = False
				self.set_privlogload.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.LOAD_PRIVATE_LOGS = True
				self.set_privlogload.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="logresume":
			if erk.config.DISPLAY_CHAT_RESUME_DATE_TIME:
				erk.config.DISPLAY_CHAT_RESUME_DATE_TIME = False
				self.set_logresume.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_CHAT_RESUME_DATE_TIME = True
				self.set_logresume.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="marklogend":
			if erk.config.MARK_END_OF_LOADED_LOG:
				erk.config.MARK_END_OF_LOADED_LOG = False
				self.set_marklogend.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.MARK_END_OF_LOADED_LOG = True
				self.set_marklogend.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="chanlogload":
			if erk.config.LOAD_CHANNEL_LOGS:
				erk.config.LOAD_CHANNEL_LOGS = False
				self.set_chanlogload.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.LOAD_CHANNEL_LOGS = True
				self.set_chanlogload.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="chanlogsave":
			if erk.config.SAVE_CHANNEL_LOGS:
				erk.config.SAVE_CHANNEL_LOGS = False
				self.set_chanlogsave.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.SAVE_CHANNEL_LOGS = True
				self.set_chanlogsave.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="history":
			if erk.config.TRACK_COMMAND_HISTORY:
				erk.config.TRACK_COMMAND_HISTORY = False
				self.set_history.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.TRACK_COMMAND_HISTORY = True
				self.set_history.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.reset_history()
			return

		if setting=="connexpand":
			if erk.config.EXPAND_SERVER_ON_CONNECT:
				erk.config.EXPAND_SERVER_ON_CONNECT = False
				self.set_connectexpand.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.EXPAND_SERVER_ON_CONNECT = True
				self.set_connectexpand.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="display_nick":
			if erk.config.DISPLAY_NICKNAME_ON_CHANNEL:
				erk.config.DISPLAY_NICKNAME_ON_CHANNEL = False
				self.set_displaynick.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_NICKNAME_ON_CHANNEL = True
				self.set_displaynick.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_channel_nickname()
			return

		if setting=="display_status":
			if erk.config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY:
				erk.config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY = False
				self.set_displaystatus.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_CHANNEL_STATUS_NICK_DISPLAY = True
				self.set_displaystatus.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_userlists()
			return

		if setting=="plainlists":
			if erk.config.PLAIN_USER_LISTS:
				erk.config.PLAIN_USER_LISTS = False
				self.set_plainusers.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.PLAIN_USER_LISTS = True
				self.set_plainusers.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_userlists()
			return

		if setting=="profanity":
			if erk.config.FILTER_PROFANITY:
				erk.config.FILTER_PROFANITY = False
				self.set_profanity.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.FILTER_PROFANITY = True
				self.set_profanity.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="autoemoji":
			if erk.config.AUTOCOMPLETE_EMOJI:
				erk.config.AUTOCOMPLETE_EMOJI = False
				self.set_autoemoji.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.AUTOCOMPLETE_EMOJI = True
				self.set_autoemoji.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="emoji":
			if erk.config.USE_EMOJIS:
				erk.config.USE_EMOJIS = False
				self.set_emoji.setIcon(QIcon(UNCHECKED_ICON))
				self.set_autoemoji.setEnabled(False)
			else:
				erk.config.USE_EMOJIS = True
				self.set_emoji.setIcon(QIcon(CHECKED_ICON))
				self.set_autoemoji.setEnabled(True)
			erk.config.save_settings(self.configfile)
			return

		if setting=="spellnicks":
			if erk.config.SPELLCHECK_IGNORE_NICKS:
				erk.config.SPELLCHECK_IGNORE_NICKS = False
				self.set_spellnicks.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.SPELLCHECK_IGNORE_NICKS = True
				self.set_spellnicks.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.toggle_nickspell()
			erk.events.resetinput_all()
			return

		if setting=="autocmd":
			if erk.config.AUTOCOMPLETE_COMMANDS:
				erk.config.AUTOCOMPLETE_COMMANDS = False
				self.set_autocmd.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.AUTOCOMPLETE_COMMANDS = True
				self.set_autocmd.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="autonick":
			if erk.config.AUTOCOMPLETE_NICKNAMES:
				erk.config.AUTOCOMPLETE_NICKNAMES = False
				self.set_autonick.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.AUTOCOMPLETE_NICKNAMES = True
				self.set_autonick.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="autoswitch":
			if erk.config.SWITCH_TO_NEW_WINDOWS:
				erk.config.SWITCH_TO_NEW_WINDOWS = False
				self.set_autoswitch.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.SWITCH_TO_NEW_WINDOWS = True
				self.set_autoswitch.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			return

		if setting=="modes":
			if erk.config.DISPLAY_CHANNEL_MODES:
				erk.config.DISPLAY_CHANNEL_MODES = False
				self.set_modes.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_CHANNEL_MODES = True
				self.set_modes.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.toggle_channel_mode_display()
			return

		if setting=="cvisible":
			if erk.config.CONNECTION_DISPLAY_VISIBLE:
				erk.config.CONNECTION_DISPLAY_VISIBLE = False
				self.set_cvisible.setIcon(QIcon(UNCHECKED_ICON))
				self.connection_dock.hide()
				self.set_float.setEnabled(False)
				self.set_uptime.setEnabled(False)
				self.set_doubleclickswitch.setEnabled(False)
				self.set_location.setEnabled(False)
			else:
				erk.config.CONNECTION_DISPLAY_VISIBLE = True
				self.set_cvisible.setIcon(QIcon(CHECKED_ICON))
				self.connection_dock.show()
				self.set_float.setEnabled(True)
				self.set_uptime.setEnabled(True)
				self.set_doubleclickswitch.setEnabled(True)
				self.set_location.setEnabled(True)
			erk.config.save_settings(self.configfile)
			return

		if setting=="float":
			if erk.config.CONNECTION_DISPLAY_MOVE:
				erk.config.CONNECTION_DISPLAY_MOVE = False
				self.set_float.setIcon(QIcon(UNCHECKED_ICON))

				self.connection_dock.hide()
				self.connection_dock.setFloating(False)
				if erk.config.CONNECTION_DISPLAY_LOCATION=="left":
					self.removeDockWidget(self.connection_dock)
					self.addDockWidget(Qt.LeftDockWidgetArea,self.connection_dock)
					self.connection_dock.show()
				else:
					self.removeDockWidget(self.connection_dock)
					self.addDockWidget(Qt.RightDockWidgetArea,self.connection_dock)
					self.connection_dock.show()
				self.connection_dock.setFeatures( QDockWidget.NoDockWidgetFeatures )
				self.connection_dock.setTitleBarWidget(QWidget())
				erk.events.resize_font_fix()
			else:
				erk.config.CONNECTION_DISPLAY_MOVE = True
				self.set_float.setIcon(QIcon(CHECKED_ICON))
				self.connection_dock.setFeatures(
					QDockWidget.DockWidgetMovable |
					QDockWidget.DockWidgetFloatable
					)
				self.connection_dock.setTitleBarWidget(None)
			erk.config.save_settings(self.configfile)
			erk.events.build_connection_display(self)
			return

		if setting=="uptime":
			if erk.config.DISPLAY_CONNECTION_UPTIME:
				erk.config.DISPLAY_CONNECTION_UPTIME = False
				self.set_uptime.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_CONNECTION_UPTIME = True
				self.set_uptime.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.build_connection_display(self)
			return

		if setting=="location":
			if erk.config.CONNECTION_DISPLAY_LOCATION=="left":
				erk.config.CONNECTION_DISPLAY_LOCATION = "right"
				self.set_location.setIcon(QIcon(LEFT_ICON))
				self.set_location.setText("Display on left")
				self.removeDockWidget(self.connection_dock)
				self.addDockWidget(Qt.RightDockWidgetArea,self.connection_dock)
				self.connection_dock.show()
			else:
				erk.config.CONNECTION_DISPLAY_LOCATION = "left"
				self.set_location.setIcon(QIcon(RIGHT_ICON))
				self.set_location.setText("Display on right")
				self.removeDockWidget(self.connection_dock)
				self.addDockWidget(Qt.LeftDockWidgetArea,self.connection_dock)
				self.connection_dock.show()
			erk.config.save_settings(self.configfile)
			return

		if setting=="spellcheck":
			if erk.config.SPELLCHECK_INPUT:
				erk.config.SPELLCHECK_INPUT = False
				self.set_spellcheck.setIcon(QIcon(UNCHECKED_ICON))
				self.spell_en.setEnabled(False)
				self.spell_fr.setEnabled(False)
				self.spell_es.setEnabled(False)
				self.spell_de.setEnabled(False)
			else:
				erk.config.SPELLCHECK_INPUT = True
				self.set_spellcheck.setIcon(QIcon(CHECKED_ICON))
				self.spell_en.setEnabled(True)
				self.spell_fr.setEnabled(True)
				self.spell_es.setEnabled(True)
				self.spell_de.setEnabled(True)
			erk.config.save_settings(self.configfile)
			erk.events.resetinput_all()
			return

		if setting=="autohostmask":
			if erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
				erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN = False
				self.set_autohostmask.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN = True
				self.set_autohostmask.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="privopen":
			if erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
				erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS = False
				self.set_privopen.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS = True
				self.set_privopen.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="dcswitch":
			if erk.config.DOUBLECLICK_SWITCH:
				erk.config.DOUBLECLICK_SWITCH = False
				self.set_doubleclickswitch.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DOUBLECLICK_SWITCH = True
				self.set_doubleclickswitch.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="links":
			if erk.config.CONVERT_URLS_TO_LINKS:
				erk.config.CONVERT_URLS_TO_LINKS = False
				self.set_links.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.CONVERT_URLS_TO_LINKS = True
				self.set_links.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="color":
			if erk.config.DISPLAY_IRC_COLORS:
				erk.config.DISPLAY_IRC_COLORS = False
				self.set_color.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_IRC_COLORS = True
				self.set_color.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="24hr":
			if erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS:
				erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS = False
				self.set_24hr.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS = True
				self.set_24hr.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

		if setting=="timestamp":
			if erk.config.DISPLAY_TIMESTAMP:
				erk.config.DISPLAY_TIMESTAMP = False
				self.set_timestamps.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_TIMESTAMP = True
				self.set_timestamps.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings(self.configfile)
			erk.events.rerender_all()
			return

	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.starter.setSource(QUrl())
			self.starter.moveCursor(QTextCursor.End)

	def open_link_in_browser(self,url):
		u = QUrl()
		u.setUrl(url)
		QDesktopServices.openUrl(u)

	def menuAbout(self):
		self.about_dialog = AboutDialog()

	def reload_all_text(self):
		erk.events.rerender_all()

	def menuLogSize(self):
		info = LogSizeDialog()
		if info!=None:
			erk.config.LOG_LOAD_SIZE_MAX = info
			erk.config.save_settings(self.configfile)
		self.logSize.setText("Set log display size ("+str(erk.config.LOG_LOAD_SIZE_MAX)+" lines)")

	def menuSetListTime(self):
		info = ListTimeDialog()
		if info!=None:
			erk.config.CHANNEL_LIST_REFRESH_FREQUENCY = info
			erk.config.save_settings(self.configfile)
		self.fetch_time.setText("Set list refresh ("+str(erk.config.CHANNEL_LIST_REFRESH_FREQUENCY)+" seconds)")

	def menuHistoryLength(self):
		info = HistorySizeDialog()
		if info!=None:
			erk.config.HISTORY_LENGTH = info
			erk.config.save_settings(self.configfile)
		self.historySize.setText("Set history length ("+str(erk.config.HISTORY_LENGTH)+" lines)")

	def menuCombo(self):
		info = ComboDialog(self.userfile)
		if info!=None:
			self.connectToIRCServer(info)

	def menuFont(self):
		font, ok = QFontDialog.getFont()
		if ok:
			erk.config.DISPLAY_FONT = font.toString()
			erk.config.save_settings(self.configfile)

			self.font = font
			self.app.setFont(self.font)
			erk.events.set_fonts_all(self.font)

			pfs = erk.config.DISPLAY_FONT.split(',')
			font_name = pfs[0]
			font_size = pfs[1]

			self.fontMenuEntry.setText(f"Font ({font_name}, {font_size} pt)")

	def menuJoin(self,client):
		info = JoinDialog()
		if info!=None:
			channel = info[0]
			key = info[1]
			client.join(channel,key)

	def menuNick(self,client):
		info = NickDialog(client.nickname,self)
		if info!=None:
			client.setNick(info)

	def menuResize(self):
		info = WindowSizeDialog(self)
		if info!=None:
			erk.config.DEFAULT_APP_WIDTH = info[0]
			erk.config.DEFAULT_APP_HEIGHT = info[1]
			erk.config.save_settings(self.configfile)
			self.resize(info[0],info[1])

			w = erk.config.DEFAULT_APP_WIDTH
			h =  erk.config.DEFAULT_APP_HEIGHT

			#self.winsizeMenuEntry.setText(f"Window size ({w} X {h})")

	def eventFilter(self, source, event):

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.connection_display):

			item = source.itemAt(event.pos())
			if item is None: return True

			if hasattr(item,"erk_widget"):
				if item.erk_widget:
					if hasattr(item,"erk_channel"):
						menu = QMenu(self)

						#if item.text(0)==SERVER_CONSOLE_NAME:
						if item.erk_console:

							entryLabel = QLabel(f"&nbsp;<big><b>"+item.erk_client.server+":"+str(item.erk_client.port)+"</b></big>",self)
							entry = QWidgetAction(self)
							entry.setDefaultWidget(entryLabel)
							menu.addAction(entry)

							if item.erk_client.hostname:
								entryLabel = QLabel(f"&nbsp;<small>"+item.erk_client.hostname+"</small>",self)
								entry = QWidgetAction(self)
								entry.setDefaultWidget(entryLabel)
								menu.addAction(entry)

							menu.addSeparator()

							# get_network_url(net)
							if item.erk_client.network:
								link = get_network_url(item.erk_client.network)
								if link:
									entry = QAction(QIcon(LINK_ICON),item.erk_client.network+" website",self)
									entry.triggered.connect(lambda state,u=link: self.open_link_in_browser(u))
									menu.addAction(entry)


							settingsMenu = buildServerSettingsMenu(self,item.erk_client)
							settingsMenu.setIcon(QIcon(SETTINGS_ICON))

							menu.addMenu(settingsMenu)

							menu.addSeparator()

							entry = QAction(QIcon(NICK_ICON),"Change nickname",self)
							entry.triggered.connect(lambda state,client=item.erk_client: self.menuNick(client))
							menu.addAction(entry)

							entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
							entry.triggered.connect(lambda state,client=item.erk_client: self.menuJoin(client))
							menu.addAction(entry)

							menu.addSeparator()

							entry = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
							entry.triggered.connect(lambda state,client=item.erk_client: erk.events.disconnect_from_server(client))
							menu.addAction(entry)
						else:
							if item.erk_channel:

								channel = item.text(0)

								entry = QAction(QIcon(EXIT_ICON),"Leave channel",self)
								entry.triggered.connect(lambda state,client=item.erk_client,name=channel: erk.events.close_channel_window(client,name))
								menu.addAction(entry)
							else:

								channel = item.text(0)

								entry = QAction(QIcon(EXIT_ICON),"Close private chat",self)
								entry.triggered.connect(lambda state,client=item.erk_client,name=channel: erk.events.close_private_window(client,name))
								menu.addAction(entry)

				else:
					return True
			else:
				return True

			action = menu.exec_(self.connection_display.mapToGlobal(event.pos()))

			self.connection_display.clearSelection()

			return True




		return super(Erk, self).eventFilter(source, event)

	def open_private_window(self,client,nickname):
		erk.events.open_private_window(client,nickname)

	def connectToIRCServer(self,info):
		if info.ssl:
			if info.reconnect:
				reconnectSSL(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=True,
					autojoin=info.autojoin
				)
			else:
				connectSSL(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=False,
					autojoin=info.autojoin
				)
		else:
			if info.reconnect:
				reconnect(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=True,
					autojoin=info.autojoin
				)
			else:
				connect(
					nickname=info.nickname,
					server=info.server,
					port=info.port,
					alternate=info.alternate,
					password=info.password,
					username=info.username,
					realname=info.realname,
					ssl=info.ssl,
					gui=self,
					reconnect=False,
					autojoin=info.autojoin
				)

# SERVER SETTINGS MENU

def buildServerSettingsMenu(self,client):

	supports = client.supports # list
	maxchannels = client.maxchannels
	maxnicklen = client.maxnicklen
	channellen = client.channellen
	topiclen = client.topiclen
	kicklen = client.kicklen
	awaylen = client.awaylen
	maxtargets = client.maxtargets
	modes = client.modes
	chanmodes = client.chanmodes #list
	prefix = client.prefix # list
	cmds = client.cmds # list
	casemapping = client.casemapping
	maxmodes = client.maxmodes

	#self.config.clear()

	optionsMenu = QMenu("Server options")

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum channels"+f":</b> {maxchannels}",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum nickname length"+f":</b> {maxnicklen}",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum channel length"+f":</b> {channellen}",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum topic length"+f":</b> {topiclen}",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum kick length"+f":</b> {kicklen}",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum away length"+f":</b> {awaylen}",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum message targets"+f":</b> {maxtargets}&nbsp;&nbsp;",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	el = QLabel(f"&nbsp;&nbsp;<b>"+"Maximum modes per user"+f":</b> {modes}",self)
	e = QWidgetAction(self)
	e.setDefaultWidget(el)
	optionsMenu.addAction(e)

	optionsMenu.addSeparator()

	maxmodesmenu = QMenu("Maximum modes",self)
	for c in maxmodes:
		e = QAction(F"{c[0]}: {c[1]}", self) 
		maxmodesmenu.addAction(e)
	optionsMenu.addMenu(maxmodesmenu)

	cmdmenu = QMenu("Commands",self)
	for c in cmds:
		e = QAction(F"{c}", self) 
		cmdmenu.addAction(e)
	optionsMenu.addMenu(cmdmenu)

	supportsmenu = QMenu("Supports",self)
	for c in supports:
		e = QAction(F"{c}", self) 
		supportsmenu.addAction(e)
	optionsMenu.addMenu(supportsmenu)

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
	optionsMenu.addMenu(chanmodemenu)

	prefixmenu = QMenu("Status prefixes",self)
	for c in prefix:
		m = c[0]
		s = c[1]
		if s=="&": s="&&"
		e = QAction(F"{m}: {s}", self)
		if m=="o": e.setIcon(QIcon(USERLIST_OPERATOR_ICON))
		if m=="v": e.setIcon(QIcon(USERLIST_VOICED_ICON))
		if m=="a": e.setIcon(QIcon(USERLIST_ADMIN_ICON))
		if m=="q": e.setIcon(QIcon(USERLIST_OWNER_ICON))
		if m=="h": e.setIcon(QIcon(USERLIST_HALFOP_ICON))
		prefixmenu.addAction(e)
	optionsMenu.addMenu(prefixmenu)

	return optionsMenu
