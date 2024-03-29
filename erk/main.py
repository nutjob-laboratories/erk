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
from zipfile import ZipFile
import shutil
import platform
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from .resources import *
from .widgets import *
from .files import *
from .common import *
from . import config
from . import events
from . import textformat
from . import userinput
from . import plugins

from .dialogs import(
	ComboDialog,
	JoinDialog,
	NickDialog,
	WindowSizeDialog,
	HistorySizeDialog,
	LogSizeDialog,
	FormatTextDialog,
	AboutDialog,
	ErrorDialog,
	ExportLogDialog,
	PrefixDialog,
	ListTimeDialog,
	InstallDialog,
	SettingsDialog,
	AutosaveDialog,
	ComboDialogCmd,
	FormatEditDialog,
	ScriptEditor,
	)

from .dialogs.blank import Dialog as Blank
from .dialogs.ignore import Dialog as Ignore

from .irc import(
	connect,
	connectSSL,
	reconnect,
	reconnectSSL
	)

USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR = False

DO_NOT_DISPLAY_MENUS_OR_TOOLBAR = False

class Erk(QMainWindow):

	# Occasionally, when restoring the main window, chat windows' text display
	# gets "zoomed in" on new text, for some reason. This prevents this from
	# being displayed to the user
	def changeEvent(self,event):
		if event.type() == QEvent.WindowStateChange:
			if event.oldState() and Qt.WindowMinimized:
				events.resize_font_fix()

				events.clear_current_unseen(self)
				self.buildSystrayMenu()

			elif event.oldState() == Qt.WindowNoState:
				events.resize_font_fix()
			elif self.windowState() == Qt.WindowMaximized:
				events.resize_font_fix()

		if event.type() == QEvent.ActivationChange and self.isActiveWindow():
			if self.current_page:
				if hasattr(self.current_page,"input"):
					if hasattr(self.current_page.input,"setFocus"):
						self.current_page.input.setFocus()

				events.clear_unseen(self.current_page)
				events.build_connection_display(self)

		
		return QMainWindow.changeEvent(self, event)

	def newStyle(self,style):
		events.apply_style(style)

	def closeEvent(self, event):

		do_quit = True

		if config.ASK_BEFORE_QUIT:

			num_servers = len(events.fetch_connections())

			if num_servers>0:

				msgBox = QMessageBox()
				msgBox.setIconPixmap(QPixmap(ERK_ICON))
				msgBox.setWindowIcon(QIcon(ERK_ICON))
				if num_servers==1:
					msgBox.setText("Are you sure you want to quit?")
				else:
					msgBox.setText("You are currently connected to "+str(num_servers)+" servers. Are you sure you want to quit?")
				msgBox.setWindowTitle("Quit "+APPLICATION_NAME)
				msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

				rval = msgBox.exec()

				if rval == QMessageBox.Cancel:
					do_quit = False

		if do_quit:

			if config.SAVE_MACROS:
				if len(userinput.MACROS)>0:
					save_macros(userinput.MACROS,self.macrofile)

			self.erk_is_quitting = True
			if self.fullscreen==False:
				config.DEFAULT_APP_WIDTH = self.width()
				config.DEFAULT_APP_HEIGHT = self.height()
				config.save_settings(self.configfile)

			plugins.exit(None)

			self.app.quit()
		else:
			event.ignore()

	def disconnect_current(self,msg=None):
		if self.current_client:

			if msg==None:
				msg = config.DEFAULT_QUIT_PART_MESSAGE

			events.disconnect_from_server(self.current_client,msg)
			self.current_client = None

			x = Blank()
			x.show()
			x.close()

	def disconnect_all(self):

		for connection in events.fetch_connections():
			events.disconnect_from_server(connection,config.DEFAULT_QUIT_PART_MESSAGE)

		self.current_client = None
		x = Blank()
		x.show()
		x.close()


	def refresh_application_title(self,item=None):

		# Fix for no connection
		if hasattr(self.current_page,"nothing_is_connected"):
			self.setWindowTitle(APPLICATION_NAME)

		if item!=None:

			topic = ''
			if hasattr(item.erk_widget,"channel_topic"):
				if len(item.erk_widget.channel_topic)>0:
					topic = item.erk_widget.channel_topic
			if not config.APP_TITLE_SHOW_TOPIC: topic = ''

			hasname = False
			if hasattr(item,"erk_name"):
				if config.APP_TITLE_TO_CURRENT_CHAT:
					if item.erk_name:
						hasname = True
						if len(topic)>0:
							self.setWindowTitle(item.erk_name+" - "+topic)
						else:
							self.setWindowTitle(item.erk_name)
				elif config.APP_TITLE_SHOW_TOPIC:
					self.setWindowTitle(topic)
				else:
					self.setWindowTitle(APPLICATION_NAME)

			if not config.APP_TITLE_TO_CURRENT_CHAT:
				if not hasname and topic=='':
					self.setWindowTitle(APPLICATION_NAME)

			return

		window = self.current_page

		topic = ''
		if hasattr(window,"channel_topic"):
			if len(window.channel_topic)>0:
				topic = window.channel_topic
		if not config.APP_TITLE_SHOW_TOPIC: topic = ''

		if hasattr(window,"name"):
			if window.name==MASTER_LOG_NAME:
				pass
			elif window.name==SERVER_CONSOLE_NAME:
				self.setWindowTitle(APPLICATION_NAME)
			else:
				if config.APP_TITLE_TO_CURRENT_CHAT:
					if len(topic)>0:
						self.setWindowTitle(window.name+" - "+topic)
					else:
						self.setWindowTitle(window.name)
				elif config.APP_TITLE_SHOW_TOPIC:
					self.setWindowTitle(topic)
				else:
					self.setWindowTitle(APPLICATION_NAME)

	def pageChange(self,index):

		window = self.stack.widget(index)

		self.current_page = window

		if hasattr(window,"client"):
			self.current_client = window.client
			if not DO_NOT_DISPLAY_MENUS_OR_TOOLBAR:
				#self.disconnect.setVisible(True)
				if not self.is_disconnect_showing:
					self.buildMenuInterface()
		else:
			self.current_client = None
			if not DO_NOT_DISPLAY_MENUS_OR_TOOLBAR:
				#self.disconnect.setVisible(False)
				if self.is_disconnect_showing:
					self.is_disconnect_showing = False
					self.buildMenuInterface()

		if hasattr(window,"name"):
			if window.name==MASTER_LOG_NAME:
				self.current_client = None
				if not DO_NOT_DISPLAY_MENUS_OR_TOOLBAR:
					#self.disconnect.setVisible(False)
					if self.is_disconnect_showing:
						self.is_disconnect_showing = False
						self.buildMenuInterface()

		if hasattr(window,"input"):
			# Set focus to the input widget
			window.input.setFocus()

			if config.SCROLL_CHAT_TO_BOTTOM:
				window.do_move_to_bottom(True)

		if hasattr(window,"client"): events.clear_unseen(window)

		events.build_connection_display(self)

		self.refresh_application_title()

		try:
			self.buildSystrayMenu()
		except:
			pass

	def connectionNodeSingleClicked(self,item,column):
		if config.DOUBLECLICK_SWITCH: return
		if hasattr(item,"erk_widget"):
			if item.erk_widget:
				self.stack.setCurrentWidget(item.erk_widget)
				self.refresh_application_title(item)

		self.connection_display.clearSelection()
		events.build_connection_display(self)

	def connectionNodeDoubleClicked(self,item):
		if not config.DOUBLECLICK_SWITCH: return
		if hasattr(item,"erk_widget"):
			if item.erk_widget:
				self.stack.setCurrentWidget(item.erk_widget)
				self.refresh_application_title(item)

		self.connection_display.clearSelection()
		events.build_connection_display(self)

	def start_spinner(self):
		if not config.SCHWA_ANIMATION: return
		if DO_NOT_DISPLAY_MENUS_OR_TOOLBAR: return
		if not USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR: self.spinner.start()

	def stop_spinner(self):
		if not config.SCHWA_ANIMATION: return
		if DO_NOT_DISPLAY_MENUS_OR_TOOLBAR: return
		if not USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:
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

	def resizeEvent(self, event):
		pass

	def connectionDisplayResized(self):
		events.build_connection_display(self)

		self.do_connection_display_width_save = self.total_uptime + 5

	def menuDocked(self,is_floating):
		if not is_floating:
			# menu bar has been docked
			p = self.toolBarArea(self.toolbar)
			if p == Qt.TopToolBarArea:
				config.MENU_BAR_ORIENT="top"
			else:
				config.MENU_BAR_ORIENT="bottom"
			config.save_settings(self.configfile)

	def set_menubar_moveable(self,is_moveable):
		if hasattr(self,'toolbar'):
			if is_moveable:
				self.toolbar.setMovable(True)
			else:
				self.toolbar.setMovable(False)
				if config.MENU_BAR_ORIENT.lower()=='top':
					self.addToolBar(Qt.TopToolBarArea,self.toolbar)
				else:
					self.addToolBar(Qt.BottomToolBarArea,self.toolbar)

	def showSettingsDialog(self):
		self._erk_this_is_the_settings_dialog_space = SettingsDialog(self.configfile,self)

	def __init__(
			self,
			app,
			info=None,
			block_settings=False,
			block_toolbar=False,
			configfile=None,
			stylefile=STYLE_FILE,
			userfile=USER_FILE,
			fullscreen=False,
			width=None,
			height=None,
			logdir=LOG_DIRECTORY,
			block_scripts=False,
			scriptdir=SCRIPTS_DIRECTORY,
			block_connectiondisplay=False,
			do_ontop=False,
			force_qmenu=False,
			style_dir=STYLES_DIRECTORY,
			no_styles=False,
			block_editor=False,
			macrofile=MACRO_SAVE_FILE,
			block_plugins=False,
			more_plugins=[],
			block_commands=False,
			block_logs=False,
			block_load=False,
			block_write=False,
			block_systray=False,
			block_traymenu=False,
			parent=None
		):
		
		super(Erk, self).__init__(parent)

		self.app = app
		self.parent = parent

		self.editor = None

		self.erk_is_quitting = False

		self.quitting = []
		self.connecting = []

		self.seditors = None

		self.uptimers = {}

		self.total_uptime = 0
		self.do_connection_display_width_save = 0

		self.current_client = None

		self.block_settings = block_settings

		self.block_toolbar = block_toolbar

		self.block_editor = block_editor

		self.fullscreen = fullscreen

		self.configfile = configfile

		self.stylefile = stylefile

		self.userfile = userfile

		self.logdir = logdir

		self.block_scripts = block_scripts

		self.scriptsdir = scriptdir

		self.styledir = style_dir

		self.do_ontop = do_ontop

		self.block_styles = no_styles

		self.macrofile = macrofile

		self.block_plugins = block_plugins

		self.more_plugins = more_plugins

		self.block_commands = block_commands

		self.is_disconnect_showing = False

		self.block_logs = block_logs

		self.block_load = block_load
		self.block_write = block_write

		self.block_systray = block_systray

		self.block_traymenu = block_traymenu

		self.cmdline_script = False
		self.cmdline_editor = False
		self.cmdline_plugins = False
		self.cmdline_logs = False

		if self.block_scripts: self.cmdline_script = True
		if self.block_editor: self.cmdline_editor = True
		if self.block_plugins: self.cmdline_plugins = True
		if self.block_logs: self.cmdline_logs = True

		self.force_qmenu = force_qmenu

		self.block_connectiondisplay = block_connectiondisplay

		global USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR

		if force_qmenu:
			USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR = True

		if config.USE_QMENUBAR_MENUS:
			USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR = True

		# Determine if window color is dark or light
		mbcolor = self.palette().color(QPalette.Window).name()
		c = tuple(int(mbcolor[i:i + 2], 16) / 255. for i in (1, 3, 5))
		luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
		luma = luma*100

		if luma>=40:
			self.is_light_colored = True
		else:
			self.is_light_colored = False

		self.style = textformat.get_text_format_settings(self.stylefile)

		# Load application settings
		config.load_settings(configfile)

		# Rebuild the command help, if a user has a different symbol
		# for executing commands
		userinput.CMDLINE_BLOCK_SCRIPTS = self.block_scripts
		userinput.CMDLINE_BLOCK_EDITOR = self.block_editor
		userinput.CMDLINE_BLOCK_STYLES = self.block_styles
		userinput.buildHelp()

		if not config.ENABLE_SCRIPT_EDITOR: self.block_editor = True

		# Load in script engine
		if not self.block_scripts:
			if config.SAVE_MACROS:
				macro_table = get_macros(self.macrofile)
				userinput.MACROS = list(macro_table)

		if width!=None:
			appwidth = width
		else:
			appwidth = int(config.DEFAULT_APP_WIDTH)

		if height!=None:
			appheight = height
		else:
			appheight = int(config.DEFAULT_APP_HEIGHT)

		if config.ENABLE_IGNORE:
			u = get_user(self.userfile)
			self.ignore = u["ignore"]
		else:
			self.ignore = []

		self.setWindowTitle(APPLICATION_NAME)
		self.setWindowIcon(QIcon(ERK_ICON))

		if config.DISPLAY_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)

			for f in OTHER_FONTS:
				QFontDatabase.addApplicationFont(f)

			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			self.font = QFont(_fontstr,DEFAULT_FONT_SIZE)
		else:
			f = QFont()
			f.fromString(config.DISPLAY_FONT)
			self.font = f

		self.app.setFont(self.font)

		if self.do_ontop:
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		self.stack = QStackedWidget(self)
		self.stack.currentChanged.connect(self.pageChange)
		self.setCentralWidget(self.stack)

		self.current_page = None

		# PLUGINS

		plugin_load_errors = plugins.load_plugins(self.block_plugins,self.more_plugins)
		if len(plugin_load_errors)>0:
			if config.PLUGIN_LOAD_ERRORS:
				ErrorDialog(self,plugin_load_errors)

		# PLUGINS

		if self.block_toolbar:
			global DO_NOT_DISPLAY_MENUS_OR_TOOLBAR
			DO_NOT_DISPLAY_MENUS_OR_TOOLBAR = True

		if not DO_NOT_DISPLAY_MENUS_OR_TOOLBAR:
			if USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:
				self.menubar = self.menuBar()
			else:
				self.toolbar = generate_menu_toolbar(self)

				if config.MENU_BAR_ORIENT.lower()=='top':
					self.addToolBar(Qt.TopToolBarArea,self.toolbar)
				else:
					self.addToolBar(Qt.BottomToolBarArea,self.toolbar)

				self.toolbar.topLevelChanged.connect(self.menuDocked)

				if config.MENU_BAR_MOVABLE:
					self.toolbar.setMovable(True)
				else:
					self.toolbar.setMovable(False)

				if self.is_light_colored:
					self.toolbar_icon = TOOLBAR_ICON
				else:
					self.toolbar_icon = LIGHT_TOOLBAR_ICON

				# MENU TOOLBAR
				self.mainMenu = QMenu()
				self.settingsMenu = QMenu()
				self.helpMenu = QMenu()
				self.toolsMenu = QMenu()
				self.pluginsMenu = QMenu()

		if not DO_NOT_DISPLAY_MENUS_OR_TOOLBAR:
			self.buildMenuInterface()
		
		self.connection_display, self.connection_dock = buildConnectionDisplayWidget(self)

		if config.CONNECTION_DISPLAY_LOCATION=="left":
			self.addDockWidget(Qt.LeftDockWidgetArea,self.connection_dock)
		elif config.CONNECTION_DISPLAY_LOCATION=="right":
			self.addDockWidget(Qt.RightDockWidgetArea,self.connection_dock)

		if config.CONNECTION_DISPLAY_MOVE:
			self.connection_dock.setFeatures(
				QDockWidget.DockWidgetMovable |
				QDockWidget.DockWidgetFloatable
				)
			self.connection_dock.setTitleBarWidget(None)
		else:
			self.connection_dock.setFeatures( QDockWidget.NoDockWidgetFeatures )
			self.connection_dock.setTitleBarWidget(QWidget())

		self.connection_display.installEventFilter(self)

		if config.CONNECTION_DISPLAY_VISIBLE:
			self.connection_dock.show()
		else:
			self.connection_dock.hide()

		if self.block_connectiondisplay:
			self.connection_dock.hide()
			self.connection_display.hide()

		self.resize(appwidth,appheight)

		if info:

			if type(info)==type(list()):
				for i in info:
					self.connectToIRCServer(i)
			else:
				self.connectToIRCServer(info)

		self.starter = QTextBrowser(self)
		self.starter.name = MASTER_LOG_NAME
		self.stack.addWidget(self.starter)
		self.starter.anchorClicked.connect(self.linkClicked)

		if self.is_light_colored:
			css =  "QTextBrowser { background-image: url(" + LOGO_IMAGE + "); background-attachment: fixed; background-repeat: no-repeat; background-position: center middle; }"
		else:
			css =  "QTextBrowser { background-image: url(" + LIGHT_LOGO_IMAGE + "); background-attachment: fixed; background-repeat: no-repeat; background-position: center middle; }"

		self.starter.setStyleSheet(css)

		self.starter.append("<p style=\"text-align: right;\"><small><b>Version "+APPLICATION_VERSION+ "&nbsp;&nbsp;</b><br><a href=\""+OFFICIAL_REPOSITORY+"\">"+OFFICIAL_REPOSITORY+"</a>&nbsp;&nbsp;</small></p>")

		self.starter.nothing_is_connected = True

		self.starter.anchorClicked.connect(self.linkClicked)

		if self.fullscreen:
			self.showFullScreen()

		# System Tray
		self.tray = QSystemTrayIcon() 
		self.tray.setIcon(QIcon(ERK_ICON)) 
		self.tray.setVisible(True)
		self.tray.setToolTip(APPLICATION_NAME+" IRC client")

		do_systray_menu = True
		if self.block_traymenu: do_systray_menu = False
		if self.block_toolbar: do_systray_menu = False

		if do_systray_menu:
			self.trayMenu = QMenu()
			self.tray.setContextMenu(self.trayMenu)
			self.buildSystrayMenu()

		self.tray.activated.connect(self.clickTray)

		if not config.SYSTRAY_ICON: self.tray.hide()

		self.hidden = False

		if self.block_systray: self.tray.hide()

	def clickTray(self,reason):
		if reason==QSystemTrayIcon.Trigger:
			# icon was clicked
			if config.CLICK_SYSTRAY_TO_HIDE:
				if self.hidden:
					self.hidden = False
					self.show()
					events.clear_current_unseen(self)
				else:
					self.hidden = True
					self.hide()
				self.buildSystrayMenu()

		if reason==QSystemTrayIcon.MiddleClick:
			# icon was middle clicked
			pass

	def setConnectionColors(self,bgcolor,fgcolor):

		mbcolor = QColor(bgcolor).name()
		c = tuple(int(mbcolor[i:i + 2], 16) / 255. for i in (1, 3, 5))
		luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
		luma = luma*100

		if luma>=40:
			is_light_colored = True
		else:
			is_light_colored = False

		if config.CONNECTION_DISPLAY_COLLAPSE:
			if is_light_colored:
				OPEN_ICON = CONNECTION_OPEN
				CLOSE_ICON = CONNECTION_CLOSED
			else:
				OPEN_ICON = LIGHT_CONNECTION_OPEN
				CLOSE_ICON = LIGHT_CONNECTION_CLOSED
		else:
			if is_light_colored:
				OPEN_ICON = DOT_ICON
				CLOSE_ICON = DOT_ICON
			else:
				OPEN_ICON = LIGHT_DOT_ICON
				CLOSE_ICON = LIGHT_DOT_ICON

		if config.CONNECTION_DISPLAY_BRANCHES:
			CONNECTION_DISPLAY_SS = f"""
				QTreeWidget {{
				    background-color: {bgcolor};
				    color: {fgcolor};
				}}

				QTreeWidget::branch:has-children:!has-siblings:closed,
				QTreeWidget::branch:closed:has-children:has-siblings {{
				        border-image: none;
				        image: url({CLOSE_ICON});
				}}

				QTreeWidget::branch:open:has-children:!has-siblings,
				QTreeWidget::branch:open:has-children:has-siblings  {{
				        border-image: none;
				        image: url({OPEN_ICON});
				}}

				QTreeWidget::branch:has-siblings:!adjoins-item {{
				    border-image: url({BRANCH_LINE}) 0;
				}}

				QTreeWidget::branch:has-siblings:adjoins-item {{
				    border-image: url({BRANCH_MORE}) 0;

				}}

				QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {{
				    border-image: url({BRANCH_END}) 0;
				}}
				"""

			LIGHT_CONNECTION_DISPLAY_SS = f"""
				QTreeWidget {{
				    background-color: {bgcolor};
				    color: {fgcolor};
				}}

				QTreeWidget::branch:has-children:!has-siblings:closed,
				QTreeWidget::branch:closed:has-children:has-siblings {{
				        border-image: none;
				        image: url({CLOSE_ICON});
				}}

				QTreeWidget::branch:open:has-children:!has-siblings,
				QTreeWidget::branch:open:has-children:has-siblings  {{
				        border-image: none;
				        image: url({OPEN_ICON});
				}}

				QTreeWidget::branch:has-siblings:!adjoins-item {{
				    border-image: url({LIGHT_BRANCH_LINE}) 0;
				}}

				QTreeWidget::branch:has-siblings:adjoins-item {{
				    border-image: url({LIGHT_BRANCH_MORE}) 0;

				}}

				QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {{
				    border-image: url({LIGHT_BRANCH_END}) 0;
				}}
				"""
		else:
			CONNECTION_DISPLAY_SS = f"""
				QTreeWidget {{
				    background-color: {bgcolor};
				    color: {fgcolor};
				}}

				QTreeWidget::branch:has-children:!has-siblings:closed,
				QTreeWidget::branch:closed:has-children:has-siblings {{
				        border-image: none;
				        image: url({CLOSE_ICON});
				}}

				QTreeWidget::branch:open:has-children:!has-siblings,
				QTreeWidget::branch:open:has-children:has-siblings  {{
				        border-image: none;
				        image: url({OPEN_ICON});
				}}
				"""

			LIGHT_CONNECTION_DISPLAY_SS = f"""
				QTreeWidget {{
				    background-color: {bgcolor};
				    color: {fgcolor};
				}}

				QTreeWidget::branch:has-children:!has-siblings:closed,
				QTreeWidget::branch:closed:has-children:has-siblings {{
				        border-image: none;
				        image: url({CLOSE_ICON});
				}}

				QTreeWidget::branch:open:has-children:!has-siblings,
				QTreeWidget::branch:open:has-children:has-siblings  {{
				        border-image: none;
				        image: url({OPEN_ICON});
				}}
				"""

		if is_light_colored:
			self.connection_display.setStyleSheet(CONNECTION_DISPLAY_SS)
		else:
			self.connection_display.setStyleSheet(LIGHT_CONNECTION_DISPLAY_SS)

	def spellcheck_language(self,setting):

		if config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(RUNCHECKED_ICON))
		if config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(RUNCHECKED_ICON))
		if config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(RUNCHECKED_ICON))
		if config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(RUNCHECKED_ICON))

		config.SPELLCHECK_LANGUAGE = setting
		config.save_settings(self.configfile)
		events.newspell_all(setting)

		if config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(RCHECKED_ICON))
		if config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(RCHECKED_ICON))
		if config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(RCHECKED_ICON))
		if config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(RCHECKED_ICON))

	
	def startScriptEditor(self):
		if self.seditors!= None:
			self.seditors.activateWindow()
			return

		self.seditors = ScriptEditor(None,self,self.configfile,self.scriptsdir,None)
		self.seditors.resize(640,480)

		self.seditors.clientsRefreshed(events.fetch_connections())

	def menuSwitch(self,client):

		if self.hidden:
			self.show()
			self.hidden = False

		win = events.fetch_console_window(client)
		self.stack.setCurrentWidget(win)
		events.WINDOW = win

		# Bring window to the front
		self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
		self.activateWindow()

	def menuMax(self):

		if self.windowState() == Qt.WindowMaximized:
			self.setWindowState(Qt.WindowNoState)
		else:
			self.setWindowState(Qt.WindowMaximized)

	def menuMin(self):

		if self.windowState() == Qt.WindowMinimized:
			self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
		else:
			self.setWindowState(Qt.WindowMinimized)

	def menuChanSwitch(self,client,channel):

		if self.hidden:
			self.show()
			self.hidden = False

		win = events.fetch_channel_window(client,channel)
		if win:
			self.stack.setCurrentWidget(win)
			events.WINDOW = win

			events.clear_current_unseen(self)
			self.buildSystrayMenu()

			# Bring window to the front
			self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
			self.activateWindow()
		else:
			self.buildSystrayMenu()

	def menuPrivSwitch(self,client,channel):

		if self.hidden:
			self.show()
			self.hidden = False

		win = events.fetch_private_window(client,channel)
		if win:
			self.stack.setCurrentWidget(win)
			events.WINDOW = win

			events.clear_current_unseen(self)
			self.buildSystrayMenu()

			# Bring window to the front
			self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
			self.activateWindow()
		else:
			self.buildSystrayMenu()

	def buildSystrayMenu(self):

		if self.block_toolbar: return
		if self.block_traymenu: return

		self.trayMenu.clear()

		if not config.SYSTRAY_MENU: return

		if config.SYSTRAY_SHOW_CONNECTIONS:

			c = events.fetch_connections()

			if len(c)>0:
				for s in c:
					active = False
					if self.current_client!=None:
						if self.current_client.id == s.id:
							active = True

					if s.hostname:
						name = s.hostname
					else:
						name = s.server+":"+str(s.port)

					nickname = s.nickname

					if active:
						menu = self.trayMenu.addMenu(QIcon(RCHECKED_ICON),name+" ("+nickname+")")
					else:
						menu = self.trayMenu.addMenu(QIcon(RUNCHECKED_ICON),name+" ("+nickname+")")

					entry = QAction(QIcon(CONSOLE_ICON),name,self)
					entry.triggered.connect(lambda state,u=s: self.menuSwitch(u))
					menu.addAction(entry)

					for chan in events.fetch_channel_list(s):

						if events.window_has_unseen(events.fetch_channel_window(s,chan),self):
							has_unseen = True
						else:
							has_unseen = False

						if config.MARK_UNSEEN_SYSTRAY:
							if has_unseen:
								icon = UNREAD_ICON
							else:
								icon = CHANNEL_ICON
						else:
							icon = CHANNEL_ICON

						entry = QAction(QIcon(icon),chan,self)
						entry.triggered.connect(lambda state,u=s,x=chan: self.menuChanSwitch(u,x))
						menu.addAction(entry)

					for chan in events.fetch_private_list(s):

						if events.window_has_unseen(events.fetch_private_window(s,chan),self):
							has_unseen = True
						else:
							has_unseen = False

						if config.MARK_UNSEEN_SYSTRAY:
							if has_unseen:
								icon = UNREAD_ICON
							else:
								icon = PRIVATE_ICON
						else:
							icon = PRIVATE_ICON

						entry = QAction(QIcon(icon),chan,self)
						entry.triggered.connect(lambda state,u=s,x=chan: self.menuPrivSwitch(u,x))
						menu.addAction(entry)

					menu.addSeparator()

					entry = QAction(QIcon(NICK_ICON),"Change nickname",self)
					entry.triggered.connect(lambda state,client=s: self.menuNick(client))
					menu.addAction(entry)

					entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
					entry.triggered.connect(lambda state,client=s: self.menuJoin(client))
					menu.addAction(entry)

					if config.SYSTRAY_ALLOW_DISCONNECT:
						entry = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
						entry.triggered.connect(lambda state,client=s: events.disconnect_from_server(client))
						menu.addAction(entry)

				self.trayMenu.addSeparator()

		if config.SYSTRAY_ALLOW_CONNECT:
			entry = QAction(QIcon(CONNECT_MENU_ICON),"Connect to a server",self)
			entry.triggered.connect(self.menuCombo)
			self.trayMenu.addAction(entry)

		if config.SYSTRAY_ALLOW_DISCONNECT:
			c = events.fetch_connections()
			if len(c)>0:
				if len(c)>1:

					if self.current_client!=None:
						if self.current_client.hostname:
							dname = self.current_client.hostname
						else:
							dname = self.current_client.server +":"+ str(self.current_client.port)

					entry = QAction(QIcon(DISCONNECT_MENU_ICON),"Disconnect from "+dname,self)
				else:
					entry = QAction(QIcon(DISCONNECT_MENU_ICON),"Disconnect from server",self)
				entry.triggered.connect(self.disconnect_current)
				self.trayMenu.addAction(entry)

				if len(c)>1:
					entry = QAction(QIcon(BAN_ICON),"Disconnect all servers",self)
					entry.triggered.connect(self.disconnect_all)
					self.trayMenu.addAction(entry)

		# Set the tooltip
		c = events.fetch_connections()
		if len(c)>0:
			if len(c)==1:

				if self.current_client!=None:
					if self.current_client.hostname:
						dname = self.current_client.hostname
					else:
						dname = self.current_client.server +":"+ str(self.current_client.port)

					self.tray.setToolTip("Connected to "+dname)
				else:
					self.tray.setToolTip("Connected to 1 server")
			else:
				self.tray.setToolTip( "Connected to "+str(len(c))+" servers")
		else:
			self.tray.setToolTip(APPLICATION_NAME+" IRC client")

		self.trayMenu.addSeparator()

		if not self.block_settings:
			entry = QAction(QIcon(OPTIONS_ICON),"Preferences",self)
			entry.triggered.connect(self.showSettingsDialog)
			self.trayMenu.addAction(entry)

		showEditor = True
		if self.block_editor: showEditor = False
		if self.block_scripts: showEditor = False

		showStyles = True
		if self.block_styles: showStyles = False
		
		showIgnore = True
		if not config.ENABLE_IGNORE: showIgnore = False

		toolsMenu = self.trayMenu.addMenu(QIcon(SETTINGS_ICON),"Tools")

		if showEditor:
			entry = QAction(QIcon(SCRIPT_ICON),"Script editor",self)
			entry.triggered.connect(self.showScriptEditor)
			toolsMenu.addAction(entry)

		if showStyles:
			entry = QAction(QIcon(FORMAT_ICON),"Style editor",self)
			entry.triggered.connect(self.showStyleDialog)
			toolsMenu.addAction(entry)

		if showIgnore:
			entry = QAction(QIcon(HIDE_ICON),"Ignore manager",self)
			entry.triggered.connect(self.menuIgnore)
			toolsMenu.addAction(entry)

		show_export = True
		if self.block_logs: show_export = False
		if self.block_load: show_export = False
		if self.block_write: show_export = False

		if show_export:
			entry = QAction(QIcon(EXPORT_ICON),"Export logs",self)
			entry.triggered.connect(self.menuExportLog)
			toolsMenu.addAction(entry)

		plugins_enabled = True
		if self.block_plugins: plugins_enabled = False
		if not config.ENABLE_PLUGINS: plugins_enabled = False

		if plugins_enabled:
			if config.SHOW_PLUGINS_MENU:

				pluginsMenu = self.trayMenu.addMenu(QIcon(PLUGIN_ICON),"Plugins")

				entry = QAction(QIcon(REDO_ICON),"Reload plugins",self)
				entry.triggered.connect(self.reloadPlugins)
				pluginsMenu.addAction(entry)

				entry = QAction(QIcon(LOAD_MENU_ICON),"Load plugins",self)
				entry.triggered.connect(self.menuLoadPlugins)
				pluginsMenu.addAction(entry)

				entry = QAction(QIcon(DIRECTORY_ICON),"Open plugin directory",self)
				entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+PLUGIN_DIRECTORY))))
				pluginsMenu.addAction(entry)

				pluginsMenu.addSeparator()

				entry = QAction(QIcon(ENABLE_ICON),"Enable all plugins",self)
				entry.triggered.connect(self.enable_all_plugins)
				pluginsMenu.addAction(entry)

				entry = QAction(QIcon(BAN_ICON),"Disable all plugins",self)
				entry.triggered.connect(self.disable_all_plugins)
				pluginsMenu.addAction(entry)

		docsMenu = self.trayMenu.addMenu(QIcon(PDF_ICON),"Documentation")

		entry = QAction(QIcon(PDF_ICON),"Command documentation",self)
		entry.triggered.connect(self.openCommandDocumentation)
		docsMenu.addAction(entry)

		entry = QAction(QIcon(PDF_ICON),"Plugin documentation",self)
		entry.triggered.connect(self.openPluginDocumentation)
		docsMenu.addAction(entry)
		
		linksMenu = self.trayMenu.addMenu(QIcon(LINK_ICON),"Links")

		helpLink = QAction(QIcon(LINK_ICON),"Official Ərk repository",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/nutjob-laboratories/erk": self.open_link_in_browser(u))
		linksMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"Official Ərk plugin repository",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/nutjob-laboratories/erk-plugins": self.open_link_in_browser(u))
		linksMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"GNU General Public License 3",self)
		helpLink.triggered.connect(lambda state,u="https://www.gnu.org/licenses/gpl-3.0.en.html": self.open_link_in_browser(u))
		linksMenu.addAction(helpLink)

		self.trayMenu.addSeparator()

		entry = QAction(QIcon(MAXIMIZE_ICON),"Maximize window",self)
		entry.triggered.connect(self.menuMax)
		self.trayMenu.addAction(entry)

		entry = QAction(QIcon(MINIMIZE_ICON),"Minimize window",self)
		entry.triggered.connect(self.menuMin)
		self.trayMenu.addAction(entry)

		self.trayMenu.addSeparator()

		entry = QAction(QIcon(QUIT_ICON),"Exit",self)
		entry.triggered.connect(self.close)
		self.trayMenu.addAction(entry)

	def buildMenuInterface(self):

		if USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:

			self.menubar.clear()
			self.mainMenu = self.menubar.addMenu("IRC")

		else:

			self.toolbar.clear()
			add_toolbar_spacer(self.toolbar)
			self.mainMenu.clear()
			add_toolbar_menu(self.toolbar,"IRC",self.mainMenu)

		entry = MenuAction(self,CONNECT_MENU_ICON,"Connect","Connect to an IRC server",25,self.menuCombo)
		self.mainMenu.addAction(entry)

		c = events.fetch_connections()
		if len(c)>0:
			if len(c)>1:
				self.disconnect = MenuAction(self,DISCONNECT_MENU_ICON,"Disconnect","Disconnect from the current server",25,self.disconnect_current)
			else:
				self.disconnect = MenuAction(self,DISCONNECT_MENU_ICON,"Disconnect","Disconnect from the server",25,self.disconnect_current)
			self.mainMenu.addAction(self.disconnect)
			self.is_disconnect_showing = True

			if len(c)>1:
				self.disconnect = MenuAction(self,EXIT_MENU_ICON,"Disconnect all","Disconnect from all servers",25,self.disconnect_all)
				self.mainMenu.addAction(self.disconnect)

		self.mainMenu.addSeparator()

		c = events.fetch_connections()
		if len(c)>0:
			txt = "Disconnect and exit "+APPLICATION_NAME
		else:
			txt = "Exit "+APPLICATION_NAME

		entry = MenuAction(self,QUIT_MENU_ICON,"Exit",txt,25,self.close)
		self.mainMenu.addAction(entry)

		if not self.block_settings:

			if USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:
				self.settingsMenu = self.menubar.addMenu("Settings")
			else:
				self.settingsMenu.clear()
				add_toolbar_menu(self.toolbar,"Settings",self.settingsMenu)

			entry = MenuAction(self,SETTINGS_MENU_ICON,"Preferences","Change "+APPLICATION_NAME+" settings",25,self.showSettingsDialog)
			self.settingsMenu.addAction(entry)

			self.winsizeMenuEntry = MenuAction(self,RESIZE_WINDOW_ICON,"Window size","Set initial window size",25,self.menuResize)
			self.settingsMenu.addAction(self.winsizeMenuEntry)

			if self.fullscreen: self.winsizeMenuEntry.setEnabled(False)

			l = lambda s="fullscreen": self.toggleSetting(s)

			entry = MenuAction(self,FULLSCREEN_WINDOW_ICON,"Full screen","Toggle full screen mode",25,l)
			self.settingsMenu.addAction(entry)

		# Tools menu
		# self.toolsMenu

		if USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:
			self.toolsMenu = self.menubar.addMenu("Tools")
		else:
			self.toolsMenu.clear()
			add_toolbar_menu(self.toolbar,"Tools",self.toolsMenu)

		showEditor = True
		if self.block_editor: showEditor = False
		if self.block_scripts: showEditor = False

		if showEditor:
			entry = MenuAction(self,SCRIPT_EDITOR_MENU_ICON,"Script editor","Create, edit, and run scripts",25,self.showScriptEditor)
			self.toolsMenu.addAction(entry)

		if not self.block_styles:
			entry = MenuAction(self,STYLE_MENU_ICON,"Style editor","Create and edit styles",25,self.showStyleDialog)
			self.toolsMenu.addAction(entry)

		if config.ENABLE_IGNORE:
			entry = MenuAction(self,HIDE_MENU_ICON,"Ignore manager","Add and remove ignore list entries",25,self.menuIgnore)
			self.toolsMenu.addAction(entry)

		show_export = True
		if self.block_logs: show_export = False
		if self.block_load: show_export = False
		if self.block_write: show_export = False

		if show_export:
			entry = MenuAction(self,EXPORT_MENU_ICON,"Export logs","Export chat logs to various formats",25,self.menuExportLog)
			self.toolsMenu.addAction(entry)

		# Plugins menu

		plugins_enabled = True
		if self.block_plugins: plugins_enabled = False
		if not config.ENABLE_PLUGINS: plugins_enabled = False

		if plugins_enabled:
			if config.SHOW_PLUGINS_MENU:
				#if len(plugins.PLUGINS)>0:

				if USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:
					self.pluginsMenu = self.menubar.addMenu("Plugins")
				else:
					self.pluginsMenu.clear()
					add_toolbar_menu(self.toolbar,"Plugins",self.pluginsMenu)

				self.buildPluginMenu()

		# Help menu

		if USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:
			self.helpMenu = self.menubar.addMenu("Help")
		else:
			self.helpMenu.clear()
			add_toolbar_menu(self.toolbar,"Help",self.helpMenu)

		entry = MenuAction(self,ERK_MENU_ICON,"About","About the "+APPLICATION_NAME+" IRC client",25,self.menuAbout)
		self.helpMenu.addAction(entry)

		idir = sys.path[0]
		DOCUMENTATION_DIRECTORY = os.path.join(idir, "documentation")

		entry = MenuAction(self,PDF_MENU_ICON,"Scripting & Commands","A guide to scripting and using "+APPLICATION_NAME,25,self.openCommandDocumentation)
		self.helpMenu.addAction(entry)

		entry = MenuAction(self,PDF_MENU_ICON,"Plugin Guide","A guide to writing and using "+APPLICATION_NAME+" plugins",25,self.openPluginDocumentation)
		self.helpMenu.addAction(entry)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(LINK_ICON),"Official Ərk repository",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/nutjob-laboratories/erk": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"Official Ərk plugin repository",self)
		helpLink.triggered.connect(lambda state,u="https://github.com/nutjob-laboratories/erk-plugins": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"GNU General Public License 3",self)
		helpLink.triggered.connect(lambda state,u="https://www.gnu.org/licenses/gpl-3.0.en.html": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		RFC_1459 = os.path.join(DOCUMENTATION_DIRECTORY, "rfc1459.pdf")
		RFC_2812 = os.path.join(DOCUMENTATION_DIRECTORY, "rfc2812.pdf")

		helpLink = QAction(QIcon(PDF_ICON),"RFC 1459",self)
		helpLink.triggered.connect(lambda state,s=RFC_1459: QDesktopServices.openUrl(QUrl("file:"+s)))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(PDF_ICON),"RFC 2812",self)
		helpLink.triggered.connect(lambda state,s=RFC_2812: QDesktopServices.openUrl(QUrl("file:"+s)))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(LINK_ICON),"List of emoji shortcodes",self)
		helpLink.triggered.connect(lambda state,u="https://www.webfx.com/tools/emoji-cheat-sheet/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		if not USE_QT5_QMENUBAR_INSTEAD_OF_TOOLBAR:

			if config.SCHWA_ANIMATION:
				add_toolbar_stretch(self.toolbar)
				self.corner_widget = add_toolbar_image(self.toolbar,self.toolbar_icon)

				if self.is_light_colored:
					ANIM = SPINNER_ANIMATION
				else:
					ANIM = LIGHT_SPINNER_ANIMATION

				self.spinner = QMovie(ANIM)

				self.spinner.frameChanged.connect(lambda state,b=self.corner_widget: self.corner_widget.setIcon( QIcon(self.spinner.currentPixmap()) ) )


	def menuLoadPlugins(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		options |= QFileDialog.ShowDirsOnly
		options |= QFileDialog.HideNameFilterDetails
		options |= QFileDialog.ReadOnly
		folderpath = QFileDialog.getExistingDirectory(self, 'Select Directory', str(Path.home()),options=options)
		if folderpath:
			self.more_plugins.append(folderpath)
			plugin_load_errors = plugins.load_plugins(self.block_plugins,self.more_plugins)
			if len(plugin_load_errors)>0:
				if config.PLUGIN_LOAD_ERRORS:
					ErrorDialog(self,plugin_load_errors)
			self.buildPluginMenu()

	def buildPluginMenu(self):

		self.pluginsMenu.clear()

		entry = MenuAction(self,RELOAD_MENU_ICON,"Reload plugins","Load any new plugins",25,self.reloadPlugins)
		self.pluginsMenu.addAction(entry)

		entry = MenuAction(self,LOAD_MENU_ICON,"Load plugins","Load plugins from a directory",25,self.menuLoadPlugins)
		self.pluginsMenu.addAction(entry)

		entry = MenuAction(self,DIRECTORY_MENU_ICON,"Open plugins","Open the plugins directory",25,(lambda s=PLUGIN_DIRECTORY: QDesktopServices.openUrl(QUrl("file:"+s))))
		self.pluginsMenu.addAction(entry)

		if len(plugins.PLUGINS)>0:

			#self.pluginsMenu.addSeparator()

			e = textSeparator(self,"Loaded Plugins")
			self.pluginsMenu.addAction(e)

			files = {}
			for p in plugins.PLUGINS:
				if p.filename in files:
					files[p.filename].append(p)
				else:
					files[p.filename] = [p]

			for file in files:

				e = (files[file][:1] or [None])[0]
				pname = e.package
				if pname==None: pname = os.path.basename(file)

				ico = e.icon
				if ico==None: ico = PLUGIN_MENU_ICON

				m = self.pluginsMenu.addMenu(QIcon(ico),pname)

				for p in files[file]:

					if plugins.is_plugin_disabled(p):
						disabled = True
					else:
						disabled = False

					if p.class_icon!=None:
						icon = p.class_icon
					else:
						icon = PLUGIN_ICON

					if p.plugin_description()!=None:
						entry = MenuNoActionRaw(self,icon,p.plugin_name()+" "+p.plugin_version()+"&nbsp;&nbsp;",p.plugin_description(),25)
					else:
						entry = MenuNoActionRaw(self,icon,p.plugin_name()+" "+p.plugin_version()+"&nbsp;&nbsp;",p.id(),25)

					m.addAction(entry)

					if config.SHOW_PLUGIN_INFO_IN_MENU:

						entryLabel = QLabel( "<small>&nbsp;&nbsp;&nbsp;<b>File:</b> "+os.path.basename(file)+"</small>" )
						entry = QWidgetAction(self)
						entry.setDefaultWidget(entryLabel)
						m.addAction(entry)

						entryLabel = QLabel( "<small>&nbsp;&nbsp;&nbsp;<b>Class:</b> "+p.class_name()+"</small>" )
						entry = QWidgetAction(self)
						entry.setDefaultWidget(entryLabel)
						m.addAction(entry)

						entryLabel = QLabel( "<small>&nbsp;&nbsp;&nbsp;<b>Size:</b> "+str(convert_size(os.path.getsize(file)))+"</small>" )
						entry = QWidgetAction(self)
						entry.setDefaultWidget(entryLabel)
						m.addAction(entry)

						entryLabel = QLabel( "<small>&nbsp;&nbsp;&nbsp;<b>Memory:</b> "+str(convert_size(p.size))+"</small>" )
						entry = QWidgetAction(self)
						entry.setDefaultWidget(entryLabel)
						m.addAction(entry)

						entryLabel = QLabel( "<small>&nbsp;&nbsp;&nbsp;<b>Events:</b> "+str(p.events)+"</b></small>" )
						entry = QWidgetAction(self)
						entry.setDefaultWidget(entryLabel)
						m.addAction(entry)

						if not p.is_home_plugin:
							entryLabel = QLabel( "<small>&nbsp;&nbsp;&nbsp;<b>Loaded from an external source</b></small>" )
							entry = QWidgetAction(self)
							entry.setDefaultWidget(entryLabel)
							m.addAction(entry)

						# entry = QAction(QIcon(EDIT_ICON),"Edit "+os.path.basename(file),self)
						# entry.triggered.connect(lambda state,u=file: self.openFile(u))
						# m.addAction(entry)

					if disabled:
						entry = QAction(QIcon(UNCHECKED_ICON),"Enabled",self)
						entry.triggered.connect(lambda state,u=p: self.enable_plugin(u))
					else:
						entry = QAction(QIcon(CHECKED_ICON),"Enabled",self)
						entry.triggered.connect(lambda state,u=p: self.disable_plugin(u))

					m.addAction(entry)

					m.addSeparator()

			# self.pluginsMenu.addSeparator()

			entry = QAction(QIcon(ENABLE_ICON),"Enable all plugins",self)
			entry.triggered.connect(self.enable_all_plugins)
			self.pluginsMenu.addAction(entry)

			entry = QAction(QIcon(BAN_ICON),"Disable all plugins",self)
			entry.triggered.connect(self.disable_all_plugins)
			self.pluginsMenu.addAction(entry)

	def disable_all_plugins(self):
		plugins.disable_all_plugins()
		config.save_settings(self.configfile)
		self.buildPluginMenu()

	def enable_all_plugins(self):
		plugins.enable_all_plugins()
		config.save_settings(self.configfile)
		self.buildPluginMenu()

	def disable_plugin(self,plugin):
		plugins.disable_plugin(plugin)
		config.save_settings(self.configfile)
		self.buildPluginMenu()

	def enable_plugin(self,plugin):
		plugins.enable_plugin(plugin)
		config.save_settings(self.configfile)
		self.buildPluginMenu()

	def reloadPlugins(self):
		plugin_load_errors = plugins.load_plugins(self.block_plugins,self.more_plugins)
		if len(plugin_load_errors)>0:
			if config.PLUGIN_LOAD_ERRORS:
				ErrorDialog(self,plugin_load_errors)

		x = Blank()
		x.show()
		x.close()

		self.buildMenuInterface()

	def openFile(self,file):

		QDesktopServices.openUrl(QUrl("file:"+file))

		x = Blank()
		x.show()
		x.close()


	def doNothing(self):
		x = Blank()
		x.show()
		x.close()

	def menuIgnore(self):
		x = Ignore(self)
		x.show()

	def openPluginDocumentation(self):
		idir = sys.path[0]
		DOCUMENTATION_DIRECTORY = os.path.join(idir, "documentation")
		DOCUMENTATION = os.path.join(DOCUMENTATION_DIRECTORY, "Erk_Plugin_Guide.pdf")

		QDesktopServices.openUrl(QUrl("file:"+DOCUMENTATION))

		x = Blank()
		x.show()
		x.close()


	def openCommandDocumentation(self):
		idir = sys.path[0]
		DOCUMENTATION_DIRECTORY = os.path.join(idir, "documentation")
		DOCUMENTATION = os.path.join(DOCUMENTATION_DIRECTORY, "Erk_Scripting_and_Commands.pdf")

		QDesktopServices.openUrl(QUrl("file:"+DOCUMENTATION))

		x = Blank()
		x.show()
		x.close()

	def showStyleDialog(self):
		FormatTextDialog(self)

	def showScriptEditor(self):
		if self.seditors:
			self.seditors.close()
		
		self.seditors = ScriptEditor(None,self,self.configfile,self.scriptsdir,None)
		self.seditors.resize(640,480)

		self.seditors.clientsRefreshed(events.fetch_connections())

	def menuExportLog(self):
		d = ExportLogDialog(self.logdir,None)
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
					# extension = os.path.splitext(fileName)[1]
					# if extension.lower()!='txt': fileName = fileName + ".txt"
					efl = len("txt")+1
					if fileName[-efl:].lower()!=f".txt": fileName = fileName+f".txt"
					dump = dumpLog(elog,dlog,llog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()
			else:
				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(self,"Save export As...",INSTALL_DIRECTORY,"JSON File (*.json);;All Files (*)", options=options)
				if fileName:
					# extension = os.path.splitext(fileName)[1]
					# if extension.lower()!='json': fileName = fileName + ".json"
					efl = len("json")+1
					if fileName[-efl:].lower()!=f".json": fileName = fileName+f".json"
					dump = dumpLogJson(elog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()

	def toggleSetting(self,setting):

		if setting=="fullscreen":
			if self.fullscreen:
				self.fullscreen = False
				self.showNormal()
				self.winsizeMenuEntry.setEnabled(True)
				events.move_all_to_bottom()
			else:
				self.fullscreen = True
				self.showFullScreen()
				self.winsizeMenuEntry.setEnabled(False)
				events.move_all_to_bottom()
			x = Blank()
			x.show()
			x.close()
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
		events.rerender_all()

	def menuCombo(self):
		info = ComboDialog(self.userfile,self.block_scripts,self.scriptsdir,self.configfile)
		if info!=None:
			self.connectToIRCServer(info)

	def menuComboCmd(self,do_ssl=None,do_reconnect=None):
		info = ComboDialogCmd(self.userfile,do_ssl,do_reconnect,self.block_scripts,self.scriptsdir,self.configfile)
		if info!=None:
			self.connectToIRCServer(info)

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
			config.DEFAULT_APP_WIDTH = info[0]
			config.DEFAULT_APP_HEIGHT = info[1]
			config.save_settings(self.configfile)
			self.resize(info[0],info[1])

	def eventFilter(self, source, event):

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.connection_display):

			if not config.ENABLE_CONNECTION_CONTEXT:
				return super(Erk, self).eventFilter(source, event)

			item = source.itemAt(event.pos())
			if item is None: return True

			if hasattr(item,"erk_widget"):
				if item.erk_widget:
					if hasattr(item,"erk_channel"):
						menu = QMenu(self)

						if item.erk_console:

							if item.erk_client.hostname:
								entry = MenuNoActionRaw(self,CONNECT_MENU_ICON,item.erk_client.server+":"+str(item.erk_client.port),item.erk_client.hostname,25)
								menu.addAction(entry)
							else:
								entry = MenuNoActionRaw(self,CONNECT_MENU_ICON,item.erk_client.server+":"+str(item.erk_client.port),'',25)
								menu.addAction(entry)

							menu.addSeparator()

							if item.erk_client.network:
								link = get_network_url(item.erk_client.network)
								if link:
									entry = QAction(QIcon(LINK_ICON),item.erk_client.network+" website",self)
									entry.triggered.connect(lambda state,u=link: self.open_link_in_browser(u))
									menu.addAction(entry)

							settingsMenu = buildServerSettingsMenu(self,item.erk_client)
							settingsMenu.setIcon(QIcon(SETTINGS_ICON))

							menu.addMenu(settingsMenu)

							if not self.block_styles:

								menu.addSeparator()

								entry = QAction(QIcon(FORMAT_ICON),"Load style",self)
								entry.triggered.connect(lambda state,client=item.erk_client: self.load_style_file_in_window_server(client))
								menu.addAction(entry)

								entry = QAction(QIcon(EDIT_ICON),"Edit style",self)
								entry.triggered.connect(lambda state,client=item.erk_client: self.edit_style_file_in_window(client,None))
								menu.addAction(entry)

								if events.using_custom_style_server(item.erk_client):
									entry = QAction(QIcon(UNDO_ICON),"Revert style to default",self)
									entry.triggered.connect(lambda state,client=item.erk_client: self.restore_style_file_in_window_server(client))
									menu.addAction(entry)

							menu.addSeparator()

							entry = QAction(QIcon(NICK_ICON),"Change nickname",self)
							entry.triggered.connect(lambda state,client=item.erk_client: self.menuNick(client))
							menu.addAction(entry)

							entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
							entry.triggered.connect(lambda state,client=item.erk_client: self.menuJoin(client))
							menu.addAction(entry)

							menu.addSeparator()

							entry = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
							entry.triggered.connect(lambda state,client=item.erk_client: events.disconnect_from_server(client))
							menu.addAction(entry)
						else:
							if not self.block_styles:
								entry = QAction(QIcon(FORMAT_ICON),"Load style",self)
								entry.triggered.connect(lambda state,client=item.erk_client,name=item.text(0): self.load_style_file_in_window(client,name))
								menu.addAction(entry)

								entry = QAction(QIcon(EDIT_ICON),"Edit style",self)
								entry.triggered.connect(lambda state,client=item.erk_client,name=item.text(0): self.edit_style_file_in_window(client,name))
								menu.addAction(entry)

								if events.using_custom_style(item.erk_client,item.text(0)):
									entry = QAction(QIcon(UNDO_ICON),"Revert style to default",self)
									entry.triggered.connect(lambda state,client=item.erk_client,name=item.text(0): self.restore_style_file_in_window(client,name))
									menu.addAction(entry)

								menu.addSeparator()

							if item.erk_channel:

								channel = item.text(0)

								if len(item.erk_widget.banlist)>0:

									bannedmenu = QMenu("Banned users",self)
									bannedmenu.setIcon(QIcon(BAN_ICON))
									for c in item.erk_widget.banlist:
										e = QAction(F"{c[0]}", self) 
										bannedmenu.addAction(e)
									menu.addMenu(bannedmenu)

								entry = QAction(QIcon(EXIT_ICON),"Leave channel",self)
								entry.triggered.connect(lambda state,client=item.erk_client,name=channel: self.doChannelPart(client,name))
								menu.addAction(entry)
							else:

								channel = item.text(0)

								entry = QAction(QIcon(EXIT_ICON),"Close private chat",self)
								entry.triggered.connect(lambda state,client=item.erk_client,name=channel: events.close_private_window(client,name))
								menu.addAction(entry)

				else:
					return True
			else:
				return True

			action = menu.exec_(self.connection_display.mapToGlobal(event.pos()))

			self.connection_display.clearSelection()

			return True

		return super(Erk, self).eventFilter(source, event)

	def doChannelPart(self,client,channel):
		client.erk_parted.append(channel)
		client.leave(channel,config.DEFAULT_QUIT_PART_MESSAGE)

	def edit_style_file_in_window(self,client,name):
		FormatEditDialog(self,client,name)

	def restore_style_file_in_window(self,client,name):
		events.restore_chat_style(client,name)

	def restore_style_file_in_window_server(self,client):
		events.restore_chat_style_server(client)

	def load_style_file_in_window(self,client,name):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Load Style File",self.styledir,f"{APPLICATION_NAME} Style File (*.{STYLE_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:
			events.load_chat_style(client,name,fileName)

	def load_style_file_in_window_server(self,client):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Load Style File",self.styledir,f"{APPLICATION_NAME} Style File (*.{STYLE_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:
			events.load_chat_style_server(client,fileName)

	def open_private_window(self,client,nickname):
		events.open_private_window(client,nickname)

	def connectToIRCServer(self,info):
		actual_connect_attempt = False
		using_ssl = False
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
					autojoin=info.autojoin,
					failreconnect=info.failreconnect,
					script=info.do_script,
				)
				actual_connect_attempt = True
				using_ssl = True
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
					autojoin=info.autojoin,
					failreconnect=info.failreconnect,
					script=info.do_script,
				)
				actual_connect_attempt = True
				using_ssl = True
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
					autojoin=info.autojoin,
					failreconnect=info.failreconnect,
					script=info.do_script,
				)
				actual_connect_attempt = True
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
					autojoin=info.autojoin,
					failreconnect=info.failreconnect,
					script=info.do_script,
				)
				actual_connect_attempt = True

		# Save connect attempts to the user history
		if actual_connect_attempt:
			user_info = get_user(self.userfile)
			if info.password:
				cpass = info.password
			else:
				cpass = ""
				
			if user_info["save_history"]:

				# Only make a save attemp if we're not using
				# the combo dialog to connect
				if not info.dialog:
					user_history = user_info["history"]

					# make sure server isn't in history
					inhistory = False
					for s in user_history:
						if s[0]==info.server:
							if s[1]==str(info.port):
								inhistory = True

					if inhistory==False:

						if using_ssl:
							ussl = "ssl"
						else:
							ussl = "normal"

						entry = [ info.server,str(info.port),UNKNOWN_NETWORK,ussl,cpass ]
						user_history.append(entry)

						user_info["history"] = user_history

			user_info["last_server"] = info.server
			user_info["last_port"] = str(info.port)
			user_info["last_password"] = cpass
			if using_ssl:
				user_info["ssl"] = True
			else:
				user_info["ssl"] = False

			save_user(user_info,self.userfile)

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

	optionsMenu = QMenu("Server settings")

	e = textSeparator(self,"Limits")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum channels"+f":</b> {maxchannels}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum nickname length"+f":</b> {maxnicklen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum channel length"+f":</b> {channellen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum topic length"+f":</b> {topiclen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum kick length"+f":</b> {kicklen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum away length"+f":</b> {awaylen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum message targets"+f":</b> {maxtargets}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum modes per user"+f":</b> {modes}")
	optionsMenu.addAction(e)

	e = textSeparator(self,"Miscellaneous")
	optionsMenu.addAction(e)

	if len(maxmodes)>0:
		maxmodesmenu = QMenu("Maximum modes",self)
		for c in maxmodes:
			e = QAction(F"{c[0]}: {c[1]}", self) 
			maxmodesmenu.addAction(e)
		optionsMenu.addMenu(maxmodesmenu)

	if len(cmds)>0:
		cmdmenu = QMenu("Commands",self)
		for c in cmds:
			e = QAction(F"{c}", self) 
			cmdmenu.addAction(e)
		optionsMenu.addMenu(cmdmenu)

	if len(supports)>0:
		supportsmenu = QMenu("Supports",self)
		for c in supports:
			e = QAction(F"{c}", self) 
			supportsmenu.addAction(e)
		optionsMenu.addMenu(supportsmenu)

	if len(chanmodes)>0:
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

	if len(prefix)>0:
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
