
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
from erk.widgets import *
from erk.files import *
from erk.common import *
import erk.config
import erk.events

from erk.dialogs import(
	ComboDialog,
	JoinDialog,
	NickDialog,
	WindowSizeDialog
	)

from erk.irc import(
	connect,
	connectSSL,
	reconnect,
	reconnectSSL
	)

class ErkMenuStyle(QProxyStyle):
	def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

		if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
			return 22
		else:
			return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)

class Erk(QMainWindow):

	def closeEvent(self, event):
		self.app.quit()

	def disconnect_current(self):
		if self.current_client:
			erk.events.disconnect_from_server(self.current_client)
			self.current_client = None
			self.disconnect.setEnabled(False)

	def pageChange(self,index):
		window = self.stack.widget(index)

		self.current_page = window

		if hasattr(window,"client"):
			self.current_client = window.client
			self.disconnect.setEnabled(True)
		else:
			self.current_client = None
			self.disconnect.setEnabled(False)

		if hasattr(window,"name"):
			if window.name==MASTER_LOG_NAME:
				self.current_client = None
				self.disconnect.setEnabled(False)
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
		self.spinner.start()

	def stop_spinner(self):
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


	def __init__(self,app,info=None,parent=None):
		super(Erk, self).__init__(parent)

		self.app = app
		self.parent = parent

		self.quitting = []
		self.connecting = []

		self.uptimers = {}

		self.current_client = None

		# Load application settings
		erk.config.load_settings()

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

		self.stack = QStackedWidget(self)
		self.stack.currentChanged.connect(self.pageChange)
		self.setCentralWidget(self.stack)

		self.current_page = None

		self.toolbar = generate_menu_toolbar(self)
		self.addToolBar(Qt.TopToolBarArea,self.toolbar)

		self.toolbar_icon = TOOLBAR_ICON
		self.corner_widget = add_toolbar_image(self.toolbar,self.toolbar_icon)
		self.spinner = QMovie(SPINNER_ANIMATION)
		self.spinner.frameChanged.connect(lambda state,b=self.corner_widget: self.corner_widget.setIcon( QIcon(self.spinner.currentPixmap())    ) )

		# MENU TOOLBAR

		mainMenu = QMenu()

		add_toolbar_menu(self.toolbar,"IRC",mainMenu)

		entry = MenuAction(self,CONNECT_MENU_ICON,"Connect","Connect to an IRC server",25,self.menuCombo)
		mainMenu.addAction(entry)

		mainMenu.addSeparator()

		self.disconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		self.disconnect.triggered.connect(self.disconnect_current)
		mainMenu.addAction(self.disconnect)
		self.disconnect.setEnabled(False)

		mainMenu.addSeparator()
		
		entry = QAction(QIcon(RESTART_ICON),"Restart",self)
		entry.triggered.connect(lambda state: restart_program())
		mainMenu.addAction(entry)

		entry = QAction(QIcon(QUIT_ICON),"Exit",self)
		entry.triggered.connect(self.close)
		mainMenu.addAction(entry)

		displayMenu = QMenu()

		add_toolbar_menu(self.toolbar,"Display",displayMenu)

		entry = QAction(QIcon(FONT_ICON),"Font",self)
		entry.triggered.connect(self.menuFont)
		displayMenu.addAction(entry)

		entry = QAction(QIcon(RESIZE_ICON),"Initial window size",self)
		entry.triggered.connect(self.menuResize)
		displayMenu.addAction(entry)

		timestampMenu = displayMenu.addMenu(QIcon(TIMESTAMP_ICON),"Timestamps")

		self.set_timestamps = QAction(QIcon(UNCHECKED_ICON),"Display",self)
		self.set_timestamps.triggered.connect(lambda state,s="timestamp": self.toggleSetting(s))
		timestampMenu.addAction(self.set_timestamps)

		if erk.config.DISPLAY_TIMESTAMP: self.set_timestamps.setIcon(QIcon(CHECKED_ICON))

		self.set_24hr = QAction(QIcon(UNCHECKED_ICON),"Use 24hr clock",self)
		self.set_24hr.triggered.connect(lambda state,s="24hr": self.toggleSetting(s))
		timestampMenu.addAction(self.set_24hr)

		if erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS: self.set_24hr.setIcon(QIcon(CHECKED_ICON))

		self.set_color = QAction(QIcon(UNCHECKED_ICON),"IRC color codes",self)
		self.set_color.triggered.connect(lambda state,s="color": self.toggleSetting(s))
		displayMenu.addAction(self.set_color)

		if erk.config.DISPLAY_IRC_COLORS: self.set_color.setIcon(QIcon(CHECKED_ICON))

		self.set_links = QAction(QIcon(UNCHECKED_ICON),"Convert URLs to links",self)
		self.set_links.triggered.connect(lambda state,s="links": self.toggleSetting(s))
		displayMenu.addAction(self.set_links)

		if erk.config.DISPLAY_IRC_COLORS: self.set_links.setIcon(QIcon(CHECKED_ICON))


		self.set_profanity = QAction(QIcon(UNCHECKED_ICON),"Hide profanity",self)
		self.set_profanity.triggered.connect(lambda state,s="profanity": self.toggleSetting(s))
		displayMenu.addAction(self.set_profanity)

		if erk.config.FILTER_PROFANITY: self.set_profanity.setIcon(QIcon(CHECKED_ICON))




		self.set_modes = QAction(QIcon(UNCHECKED_ICON),"Display channel modes",self)
		self.set_modes.triggered.connect(lambda state,s="modes": self.toggleSetting(s))
		displayMenu.addAction(self.set_modes)

		if erk.config.DISPLAY_CHANNEL_MODES: self.set_modes.setIcon(QIcon(CHECKED_ICON))

		settingsMenu = QMenu()
		add_toolbar_menu(self.toolbar,"Settings",settingsMenu)


		spellcheckMenu = settingsMenu.addMenu(QIcon(SPELLCHECK_ICON),"Spellcheck")

		self.set_spellcheck = QAction(QIcon(UNCHECKED_ICON),"Enabled",self)
		self.set_spellcheck.triggered.connect(lambda state,s="spellcheck": self.toggleSetting(s))
		spellcheckMenu.addAction(self.set_spellcheck)

		if erk.config.SPELLCHECK_INPUT: self.set_spellcheck.setIcon(QIcon(CHECKED_ICON))


		self.set_spellnicks = QAction(QIcon(UNCHECKED_ICON),"Ignore nicknames",self)
		self.set_spellnicks.triggered.connect(lambda state,s="spellnicks": self.toggleSetting(s))
		spellcheckMenu.addAction(self.set_spellnicks)

		if erk.config.SPELLCHECK_IGNORE_NICKS: self.set_spellnicks.setIcon(QIcon(CHECKED_ICON))


		spelllanguageMenu = spellcheckMenu.addMenu(QIcon(LANGUAGE_ICON),"Language")

		self.spell_en = QAction(QIcon(UNCHECKED_ICON),"English",self)
		self.spell_en.triggered.connect(lambda state,s="en": self.spellcheck_language(s))
		spelllanguageMenu.addAction(self.spell_en)

		self.spell_fr = QAction(QIcon(UNCHECKED_ICON),"French",self)
		self.spell_fr.triggered.connect(lambda state,s="fr": self.spellcheck_language(s))
		spelllanguageMenu.addAction(self.spell_fr)

		self.spell_es = QAction(QIcon(UNCHECKED_ICON),"Spanish",self)
		self.spell_es.triggered.connect(lambda state,s="es": self.spellcheck_language(s))
		spelllanguageMenu.addAction(self.spell_es)

		self.spell_de = QAction(QIcon(UNCHECKED_ICON),"German",self)
		self.spell_de.triggered.connect(lambda state,s="de": self.spellcheck_language(s))
		spelllanguageMenu.addAction(self.spell_de)

		if erk.config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(CHECKED_ICON))

		if not erk.config.SPELLCHECK_INPUT:
			self.spell_en.setEnabled(False)
			self.spell_fr.setEnabled(False)
			self.spell_es.setEnabled(False)
			self.spell_de.setEnabled(False)


		connectionDisplayMenu = settingsMenu.addMenu(QIcon(CONNECTION_DISPLAY_ICON),"Connection display")

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

		autocompleteMenu = settingsMenu.addMenu(QIcon(AUTOCOMPLETE_ICON),"Autocomplete")

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

		self.set_autoasciimoji = QAction(QIcon(UNCHECKED_ICON),"ASCIImoji shortcodes",self)
		self.set_autoasciimoji.triggered.connect(lambda state,s="autoasciimoji": self.toggleSetting(s))
		autocompleteMenu.addAction(self.set_autoasciimoji)

		if erk.config.AUTOCOMPLETE_ASCIIMOJI: self.set_autoasciimoji.setIcon(QIcon(CHECKED_ICON))







		emojiMenu = settingsMenu.addMenu(QIcon(EMOJI_ICON),"Emojis")

		self.set_emoji = QAction(QIcon(UNCHECKED_ICON),"Use emojis",self)
		self.set_emoji.triggered.connect(lambda state,s="emoji": self.toggleSetting(s))
		emojiMenu.addAction(self.set_emoji)

		if erk.config.USE_EMOJIS: self.set_emoji.setIcon(QIcon(CHECKED_ICON))

		self.set_asciimoji = QAction(QIcon(UNCHECKED_ICON),"Use ASCIImojis",self)
		self.set_asciimoji.triggered.connect(lambda state,s="asciimoji": self.toggleSetting(s))
		emojiMenu.addAction(self.set_asciimoji)

		if erk.config.USE_ASCIIMOJIS: self.set_asciimoji.setIcon(QIcon(CHECKED_ICON))






		self.set_privopen = QAction(QIcon(UNCHECKED_ICON),"Private messages in new chats",self)
		self.set_privopen.triggered.connect(lambda state,s="privopen": self.toggleSetting(s))
		settingsMenu.addAction(self.set_privopen)

		if erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS: self.set_privopen.setIcon(QIcon(CHECKED_ICON))

		self.set_autohostmask = QAction(QIcon(UNCHECKED_ICON),"Get hostmasks on channel join",self)
		self.set_autohostmask.triggered.connect(lambda state,s="autohostmask": self.toggleSetting(s))
		settingsMenu.addAction(self.set_autohostmask)

		if erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN: self.set_autohostmask.setIcon(QIcon(CHECKED_ICON))

		self.set_autoswitch = QAction(QIcon(UNCHECKED_ICON),"Automatically switch to new chats",self)
		self.set_autoswitch.triggered.connect(lambda state,s="autoswitch": self.toggleSetting(s))
		settingsMenu.addAction(self.set_autoswitch)

		if erk.config.SWITCH_TO_NEW_WINDOWS: self.set_autoswitch.setIcon(QIcon(CHECKED_ICON))

		# End of menus
		end_toolbar_menu(self.toolbar)

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

		self.starter.append(START_BANNER)
		self.starter.append("&nbsp;<b><a href=\"https://github.com/nutjob-laboratories/erk\">https://github.com/nutjob-laboratories/erk</a></b>")
		self.starter.append("")
		self.starter.append("&nbsp;<i>Click <b>Connect</b> in the <b>IRC</b> menu to connect to IRC!</i>")
		self.starter.append("")

		self.starter.anchorClicked.connect(self.linkClicked)

	def spellcheck_language(self,setting):

		if erk.config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(UNCHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(UNCHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(UNCHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(UNCHECKED_ICON))

		erk.config.SPELLCHECK_LANGUAGE = setting
		erk.config.save_settings()
		erk.events.newspell_all(setting)

		if erk.config.SPELLCHECK_LANGUAGE=="en": self.spell_en.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="fr": self.spell_fr.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="es": self.spell_es.setIcon(QIcon(CHECKED_ICON))
		if erk.config.SPELLCHECK_LANGUAGE=="de": self.spell_de.setIcon(QIcon(CHECKED_ICON))


	# self.set_profanity = QAction(QIcon(UNCHECKED_ICON),"Hide profanity",self)
	# 	self.set_profanity.triggered.connect(lambda state,s="profanity": self.toggleSetting(s))
	# 	displayMenu.addAction(self.set_profanity)

	# 	if erk.config.FILTER_PROFANITY: self.set_profanity.setIcon(QIcon(CHECKED_ICON))

	def toggleSetting(self,setting):

		if setting=="profanity":
			if erk.config.FILTER_PROFANITY:
				erk.config.FILTER_PROFANITY = False
				self.set_profanity.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.FILTER_PROFANITY = True
				self.set_profanity.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

		if setting=="autoasciimoji":
			if erk.config.AUTOCOMPLETE_ASCIIMOJI:
				erk.config.AUTOCOMPLETE_ASCIIMOJI = False
				self.set_autoasciimoji.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.AUTOCOMPLETE_ASCIIMOJI = True
				self.set_autoasciimoji.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			return

		if setting=="autoemoji":
			if erk.config.AUTOCOMPLETE_EMOJI:
				erk.config.AUTOCOMPLETE_EMOJI = False
				self.set_autoemoji.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.AUTOCOMPLETE_EMOJI = True
				self.set_autoemoji.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			return

		if setting=="asciimoji":
			if erk.config.USE_ASCIIMOJIS:
				erk.config.USE_ASCIIMOJIS = False
				self.set_asciimoji.setIcon(QIcon(UNCHECKED_ICON))
				self.set_autoasciimoji.setEnabled(False)
			else:
				erk.config.USE_ASCIIMOJIS = True
				self.set_asciimoji.setIcon(QIcon(CHECKED_ICON))
				self.set_autoasciimoji.setEnabled(True)
			erk.config.save_settings()
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
			erk.config.save_settings()
			return

		if setting=="spellnicks":
			if erk.config.SPELLCHECK_IGNORE_NICKS:
				erk.config.SPELLCHECK_IGNORE_NICKS = False
				self.set_spellnicks.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.SPELLCHECK_IGNORE_NICKS = True
				self.set_spellnicks.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
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
			erk.config.save_settings()
			return

		if setting=="autonick":
			if erk.config.AUTOCOMPLETE_NICKNAMES:
				erk.config.AUTOCOMPLETE_NICKNAMES = False
				self.set_autonick.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.AUTOCOMPLETE_NICKNAMES = True
				self.set_autonick.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			return

		if setting=="autoswitch":
			if erk.config.SWITCH_TO_NEW_WINDOWS:
				erk.config.SWITCH_TO_NEW_WINDOWS = False
				self.set_autoswitch.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.SWITCH_TO_NEW_WINDOWS = True
				self.set_autoswitch.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			return

		if setting=="modes":
			if erk.config.DISPLAY_CHANNEL_MODES:
				erk.config.DISPLAY_CHANNEL_MODES = False
				self.set_modes.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_CHANNEL_MODES = True
				self.set_modes.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
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
			erk.config.save_settings()
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

			else:
				erk.config.CONNECTION_DISPLAY_MOVE = True
				self.set_float.setIcon(QIcon(CHECKED_ICON))
				self.connection_dock.setFeatures(
					QDockWidget.DockWidgetMovable |
					QDockWidget.DockWidgetFloatable
					)
				self.connection_dock.setTitleBarWidget(None)
			erk.config.save_settings()
			erk.events.build_connection_display(self)
			return

		if setting=="uptime":
			if erk.config.DISPLAY_CONNECTION_UPTIME:
				erk.config.DISPLAY_CONNECTION_UPTIME = False
				self.set_uptime.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_CONNECTION_UPTIME = True
				self.set_uptime.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
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
			erk.config.save_settings()
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
			erk.config.save_settings()
			erk.events.resetinput_all()
			return

		if setting=="autohostmask":
			if erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
				erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN = False
				self.set_autohostmask.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.GET_HOSTMASKS_ON_CHANNEL_JOIN = True
				self.set_autohostmask.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

		if setting=="privopen":
			if erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
				erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS = False
				self.set_privopen.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS = True
				self.set_privopen.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

		if setting=="dcswitch":
			if erk.config.DOUBLECLICK_SWITCH:
				erk.config.DOUBLECLICK_SWITCH = False
				self.set_doubleclickswitch.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DOUBLECLICK_SWITCH = True
				self.set_doubleclickswitch.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

		if setting=="links":
			if erk.config.CONVERT_URLS_TO_LINKS:
				erk.config.CONVERT_URLS_TO_LINKS = False
				self.set_links.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.CONVERT_URLS_TO_LINKS = True
				self.set_links.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

		if setting=="color":
			if erk.config.DISPLAY_IRC_COLORS:
				erk.config.DISPLAY_IRC_COLORS = False
				self.set_color.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_IRC_COLORS = True
				self.set_color.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

		if setting=="24hr":
			if erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS:
				erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS = False
				self.set_24hr.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.USE_24HOUR_CLOCK_FOR_TIMESTAMPS = True
				self.set_24hr.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

		if setting=="timestamp":
			if erk.config.DISPLAY_TIMESTAMP:
				erk.config.DISPLAY_TIMESTAMP = False
				self.set_timestamps.setIcon(QIcon(UNCHECKED_ICON))
			else:
				erk.config.DISPLAY_TIMESTAMP = True
				self.set_timestamps.setIcon(QIcon(CHECKED_ICON))
			erk.config.save_settings()
			erk.events.rerender_all()
			return

	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.starter.setSource(QUrl())
			self.starter.moveCursor(QTextCursor.End)

	def menuCombo(self):
		info = ComboDialog()
		if info!=None:
			self.connectToIRCServer(info)

	def menuFont(self):
		font, ok = QFontDialog.getFont()
		if ok:
			erk.config.DISPLAY_FONT = font.toString()
			erk.config.save_settings()

			self.font = font
			self.app.setFont(self.font)
			erk.events.set_fonts_all(self.font)

	def menuJoin(self,client):
		info = JoinDialog()
		if info!=None:
			channel = info[0]
			key = info[1]
			client.join(channel,key)

	def menuNick(self,client):
		info = NickDialog(client.nickname)
		if info!=None:
			client.setNick(info)

	def menuResize(self):
		info = WindowSizeDialog()
		if info!=None:
			erk.config.DEFAULT_APP_WIDTH = info[0]
			erk.config.DEFAULT_APP_HEIGHT = info[1]
			erk.config.save_settings()
			self.resize(info[0],info[1])

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

							entry = QAction(QIcon(NICK_ICON),"Change nickname",self)
							entry.triggered.connect(lambda state,client=item.erk_client: self.menuNick(client))
							menu.addAction(entry)

							entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
							entry.triggered.connect(lambda state,client=item.erk_client: self.menuJoin(client))
							menu.addAction(entry)

							menu.addSeparator()

							entry = QAction(QIcon(EXIT_ICON),"Disconnect",self)
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

					# entry = QAction(QIcon(EXIT_ICON),CONNECTIONS_MENU_DISCONNECT,self)
					# entry.triggered.connect(lambda state,id=item.erk_client.id,cmd='disconnect': self.connectionEntryClick(id,cmd))
					# menu.addAction(entry)
				else:
					return True
			else:
				return True

			action = menu.exec_(self.connection_display.mapToGlobal(event.pos()))

			return True




		return super(Erk, self).eventFilter(source, event)

	def open_private_window(self,client,nickname):
		#print("heh "+nickname)
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

