
import fnmatch

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
from erk.strings import *
from erk.widgets import *
from erk.config import *

from erk.dialogs import (ConnectDialog,
						NetworkDialog,
						WindowSizeDialog,
						NewNickDialog,
						JoinChannelDialog,
						AboutDialog,
						FormatDialog,
						LogsizeDialog,
						IOsizeDialog,
						CmdHistoryLengthDialog,
						IgnoreDialog,
						MacroDialog)

from erk.irc import connect,connectSSL,reconnect,reconnectSSL

import erk.events
import erk.macro

class Erk(QMainWindow):

	def got_new_style(self):
		erk.events.rerenderAllText()

		text_color = get_style_attribute(self.styles[BASE_STYLE_NAME],"color")
		if not text_color: text_color = "#000000"

		BASE_COLOR = get_style_attribute(self.styles[BASE_STYLE_NAME],"background-color")
		if not BASE_COLOR: text_color = "#FFFFFF"

		DARKER_COLOR = color_variant(BASE_COLOR,-20)

		user_display_qss='''
			QTreeWidget::item::selected {
				border: 0px;
				background: !BASE!;
			}
			QTreeWidget::item:hover {
				border: 0px;
				background: !DARKER!;
			}
			QTreeWidget::item {
				border: 0px;
				color: !TEXT_COLOR!;
			}
			QTreeWidget::item::active {
				border: 0px;
				background: !DARKER!;
			}
			QTreeWidget::item::!active {
				border: 0px;
			}
			QTreeWidget {
				show-decoration-selected: 0;
			}
		'''
		user_display_qss = user_display_qss.replace('!DARKER!',DARKER_COLOR)
		user_display_qss = user_display_qss.replace('!BASE!',BASE_COLOR)
		user_display_qss = user_display_qss.replace('!TEXT_COLOR!',text_color)
		user_display_qss = user_display_qss + self.styles[BASE_STYLE_NAME]

		self.connectionTree.setStyleSheet(user_display_qss)

	def start_working(self):
		self.work_display.show()
		self.working.start()

	def stop_working(self):
		self.working.stop()
		self.work_display.hide()

	def client_disconnected(self,client):
		del self.uptimers[client.id]

		# If the client disconnected *on purpose*,
		# exit without displaying a warning
		cid = client.server+str(client.port)
		if cid in self.disconnecting: return

		if self.notify_lost:
			cfail = QMessageBox(self)
			cfail.setWindowIcon(QIcon(ERK_ICON))
			cfail.setWindowTitle(client.server)
			cfail.setText("<b>Connection lost</b>")
			cfail.setDetailedText("Disconnected from "+client.server+":"+str(client.port))
			cfail.setIcon(QMessageBox.Warning)
			cfail.exec()

	def connectionLost(self,server,port):
		#print("connection to "+server+":"+str(port)+" failed")
		pass
		
	def client_connected(self,client):

		clean = []
		found = False
		before = len(self.connecting)
		for e in self.connecting:
			if e[0]==client.server:
				if e[1]==client.port:
					if not found:
						found = True
						continue
			clean.append(e)
		self.connecting = clean
		after = len(self.connecting)

		if after==0: self.stop_working()

		

	def connectionFailed(self,server,port):

		clean = []
		found = False
		before = len(self.connecting)
		for e in self.connecting:
			if e[0]==server:
				if e[1]==port:
					if not found:
						found = True
						continue
			clean.append(e)
		self.connecting = clean
		after = len(self.connecting)

		if after==0: self.stop_working()

		# Remove from the "visited" list
		u = get_user()
		try:
			u["visited"].remove(server+":"+str(port))
			save_user(u)
		except:
			pass

		# Display message
		if self.notify_fail:
			cfail = QMessageBox(self)
			cfail.setWindowIcon(QIcon(ERK_ICON))
			cfail.setWindowTitle(server)
			cfail.setText("<b>Connection failed</b>")
			cfail.setDetailedText("Couldn't connect to "+server+":"+str(port))
			cfail.setIcon(QMessageBox.Warning)
			cfail.exec()

	# Occasionally, when restoring the main window, chat windows' text display
	# gets "zoomed in" on new text, for some reason. This prevents this from
	# being displayed to the user
	def changeEvent(self,event):
		if event.type() == QEvent.WindowStateChange:
			if event.oldState() and Qt.WindowMinimized:
				channels,privates,consoles = erk.events.getWindows()
				for w in channels:
					w.channelChatDisplay.zoomIn()
					w.channelChatDisplay.zoomOut()
					w.channelChatDisplay.moveCursor(QTextCursor.End)
				for w in privates:
					w.channelChatDisplay.zoomIn()
					w.channelChatDisplay.zoomOut()
					w.channelChatDisplay.moveCursor(QTextCursor.End)
				for w in consoles:
					w.channelChatDisplay.zoomIn()
					w.channelChatDisplay.zoomOut()
					w.channelChatDisplay.moveCursor(QTextCursor.End)
			elif event.oldState() == Qt.WindowNoState:
				pass
			elif self.windowState() == Qt.WindowMaximized:
				pass
		
		return QMainWindow.changeEvent(self, event)

	def restoreWindow(self,win,subwin):
		# Unminimize window if the window is minimized
		win.setWindowState(win.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
		win.activateWindow()
		win.showNormal()

		subwin.show()

		# Bring the window to the front
		self.MDI.setActiveSubWindow(subwin)

	def window_activity_is_unseen(self,window):
		for w in self.unseen:
			if window.name==w.name:
				if window.client.id==w.client.id:
					return True
		return False

	def window_activity(self,window):

		# Do not note window activity if it's from the
		# active window
		if window.name==self.active_window.name:
			if window.client.id==self.active_window.client.id:
				return

		# Check to see if the window is aleady in the
		# list of windows with unseen activity
		for w in self.unseen:
			if window.name==w.name:
				if window.client.id==w.client.id:
					return

		# Add the window to the unseen activity list
		self.unseen.append(window)

		# Iterate through the connection display, and
		# color the entry for this window
		iterator = QTreeWidgetItemIterator(self.connectionTree)
		while True:
			item = iterator.value()
			if item is not None:
				if hasattr(item,"erk_window"):
					if item.erk_window.name==window.name:
						if item.erk_window.client.id==window.client.id:
							color = QBrush(QColor(self.unread_messages_color))
							item.setForeground(0,color)
				iterator += 1
			else:
				break

	def set_window_not_active(self,window):
		clean = []
		for w in self.unseen:
			if window.name==w.name:
				if window.client.id==w.client.id: continue
			clean.append(w)
		self.unseen = clean

		iterator = QTreeWidgetItemIterator(self.connectionTree)
		while True:
			item = iterator.value()
			if item is not None:
				if hasattr(item,"erk_window"):
					if item.erk_window.name==window.name:
						if item.erk_window.client.id==window.client.id:
							f = item.font(0)
							f.setBold(False)
							item.setFont(0,f)
							if item.erk_channel:
								item.setIcon(0,QIcon(CHANNEL_WINDOW_ICON))
							elif item.erk_locked:
								item.setIcon(0,QIcon(LOCKED_CHANNEL_ICON))
							elif item.erk_private:
								item.setIcon(0,QIcon(USER_WINDOW_ICON))
							elif item.erk_console:
								item.setIcon(0,QIcon(CONSOLE_WINDOW_ICON))
							else:
								item.setIcon(0,QIcon(SERVER_ICON))
				iterator += 1
			else:
				break

	def got_uptime(self,client,uptime):

		self.uptimers[client.id] = uptime

		if len(self.connecting)==0: self.work_display.hide()

		if self.display_uptimes:
			iterator = QTreeWidgetItemIterator(self.connectionTree)
			while True:
				item = iterator.value()
				if item is not None:
					if hasattr(item,"erk_uptime"):
						if item.erk_uptime:
							if item.erk_client.id==client.id:
								item.setText(0,prettyUptime(uptime))
					iterator += 1
				else:
					break

	def populateConnectionDisplay(self,connections,channels,privates,consoles):

		# Rebuild the toolbar
		self.buildToolbar()

		# Make a list of expanded server nodes, and make sure they
		# are still expanded when we rewrite the display
		expanded = []
		iterator = QTreeWidgetItemIterator(self.connectionTree)
		while True:
			item = iterator.value()
			if item is not None:
				if hasattr(item,"erk_server"):
					if item.erk_server:
						if item.isExpanded(): expanded.append(item.erk_client.id)
				iterator += 1
			else:
				break

		clearQTreeWidget(self.connectionTree)

		root = self.connectionTree.invisibleRootItem()

		for c in connections:

			hostname = c.server+":"+str(c.port)

			parent = QTreeWidgetItem(root)

			icon = SERVER_ICON

			if c.hostname:
				if c.network:
					hostname = c.network
					icon = NETWORK_SERVER_ICON

			parent.setText(0,hostname)
			parent.setIcon(0,QIcon(icon))
			parent.erk_server = True
			parent.erk_channel = False
			parent.erk_private = False
			parent.erk_console = False
			parent.erk_locked = False
			parent.erk_client = c

			if self.display_uptimes:
				child = QTreeWidgetItem(parent)
				if c.id in self.uptimers:
					child.setText(0,prettyUptime(self.uptimers[c.id]))
				else:
					child.setText(0,"00:00:00")
				child.setIcon(0,QIcon(TIMESTAMP_ICON))
				child.erk_uptime = True
				child.erk_client = c

			if c.id in expanded:
				parent.setExpanded(True)

			for s in consoles:
				if c.id==s.client.id:
					child = QTreeWidgetItem(parent)
					if s.client.hostname:
						child.setText(0,s.client.hostname)
					else:
						child.setText(0,s.name)

					child.setIcon(0,QIcon(CONSOLE_WINDOW_ICON))
					child.erk_window = s
					child.erk_server = False
					child.erk_channel = False
					child.erk_private = False
					child.erk_console = True
					child.erk_locked = False
					child.erk_client = c

					if self.active_window:
						if self.active_window.name==s.name:
							if self.active_window.client.id==s.client.id:
								# Window is active
								f = child.font(0)
								f.setBold(True)
								child.setFont(0,f)
								child.setIcon(0,QIcon(ACTIVE_ICON))

					for window in self.unseen:
						if window.name==w.name:
							if window.client.id==w.client.id:
								child.setForeground(0,QColor(self.unread_messages_color))

			for w in channels:
				if c.id==w.client.id:
					child = QTreeWidgetItem(parent)
					child.setText(0,w.name)

					if w.key=='':
						child.setIcon(0,QIcon(CHANNEL_WINDOW_ICON))
						child.erk_channel = True
						child.erk_locked = False
					else:
						child.setIcon(0,QIcon(LOCKED_CHANNEL_ICON))
						child.erk_channel = False
						child.erk_locked = True

					child.erk_window = w
					child.erk_server = False
					child.erk_private = False
					child.erk_console = False
					child.erk_client = c

					if self.active_window:
						if self.active_window.name==w.name:
							if self.active_window.client.id==w.client.id:
								# Window is active
								f = child.font(0)
								f.setBold(True)
								child.setFont(0,f)
								child.setIcon(0,QIcon(ACTIVE_ICON))

					for window in self.unseen:
						if window.name==w.name:
							if window.client.id==w.client.id:
								child.setForeground(0,QColor(self.unread_messages_color))

			for p in privates:
				if c.id==p.client.id:
					nickname = p.name
					userinfo = nickname.split('!')
					if len(userinfo)==2:
						nickname = userinfo[0]
					child = QTreeWidgetItem(parent)
					child.setText(0,nickname)
					child.setIcon(0,QIcon(USER_WINDOW_ICON))
					child.erk_window = p
					child.erk_server = False
					child.erk_channel = False
					child.erk_private = True
					child.erk_console = False
					child.erk_locked = False
					child.erk_client = c

					if self.active_window:
						if self.active_window.name==p.name:
							if self.active_window.client.id==p.client.id:
								# Window is active
								f = child.font(0)
								f.setBold(True)
								child.setFont(0,f)
								child.setIcon(0,QIcon(ACTIVE_ICON))

					for window in self.unseen:
						if window.name==p.name:
							if window.client.id==p.client.id:
								child.setForeground(0,QColor(self.unread_messages_color))


	def closeEvent(self, event):
		self.app.quit()

	def is_ignored(self,client,user):

		if '*' in self.ignored:
			p = user.split('!')
			if p==2:
				for u in self.ignored["*"]:
					if fnmatch.fnmatch(p[0],u): return True
					if fnmatch.fnmatch(p[1],u): return True
			else:
				for u in self.ignored["*"]:
					#if user == u: return True
					if fnmatch.fnmatch(user,u): return True

		cid = client.server+":"+str(client.port)

		if not cid in self.ignored: return False

		p = user.split('!')
		if p==2:
			for u in self.ignored[cid]:

				if fnmatch.fnmatch(p[0],u): return True
				if fnmatch.fnmatch(p[1],u): return True

				# if p[0] == u: return True
				# if p[1] == u: return True
		else:
			for u in self.ignored[cid]:
				#if user == u: return True
				if fnmatch.fnmatch(user,u): return True
		return False

	def add_ignore(self,client,user):
		cid = client.server+":"+str(client.port)
		if not cid in self.ignored:
			self.ignored[cid] = []
			self.ignored[cid].append(user)
			self.ignored[cid] = list(dict.fromkeys(self.ignored[cid]))
			if self.save_ignored: save_ignore(self.ignored)
		else:
			self.ignored[cid].append(user)
			self.ignored[cid] = list(dict.fromkeys(self.ignored[cid]))
			if self.save_ignored: save_ignore(self.ignored)

	def remove_ignore(self,client,user):

		changed = False
		if '*' in self.ignored:
			clean = []
			for u in self.ignored["*"]:
				#if u==user: continue
				if fnmatch.fnmatch(user,u):
					changed = True
					continue
				clean.append(u)
			self.ignored = clean

		cid = client.server+":"+str(client.port)
		if not cid in self.ignored:
			if changed:
				if self.save_ignored: save_ignore(self.ignored)
			return
		clean = []
		for u in self.ignored[cid]:
			#if u==user: continue
			if fnmatch.fnmatch(user,u):
				changed = True
				continue
			clean.append(u)
		self.ignored[cid] = clean
		if changed:
			if self.save_ignored: save_ignore(self.ignored)

	def clientid_to_client(self,cid):
		return erk.events.clientid_to_client(cid)

	def does_server_support_cnotice(self,client):
		return erk.events.does_server_support_cnotice(client)

	def does_server_support_cprivmsg(self,client):
		return erk.events.does_server_support_cprivmsg(client)

	def does_server_support_knock(self,client):
		return erk.events.does_server_support_knock(client)

	def __init__(self,app,parent=None):
		super(Erk, self).__init__(parent)

		self.app = app
		self.parent = parent

		self.unseen = []

		self.uptimers = {}

		self.disconnecting = []
		self.connecting = []

		self.ignored = {}

		# Set default style
		self.app.setStyle(DEFAULT_APPLICATION_STYLE)

		self.setWindowTitle(APPLICATION_NAME)

		self.setWindowIcon(QIcon(ERK_ICON))

		self.styles = get_text_format_settings()
		self.settings = get_settings()

		self.ASCIIMOJI_AUTOCOMPLETE = load_asciimoji_autocomplete()
		self.EMOJI_AUTOCOMPLETE = load_emoji_autocomplete()

		# Load in settings from the settings file
		self.max_nick_size					= self.settings[SETTING_MAX_NICK_SIZE]
		self.strip_html						= self.settings[SETTING_STRIP_HTML]
		self.irc_color						= self.settings[SETTING_IRC_COLOR]
		self.create_links					= self.settings[SETTING_LINKS]
		self.show_timestamps				= self.settings[SETTING_TIMESTAMPS]
		self.show_timestamp_seconds			= self.settings[SETTING_TIMESTAMP_SECONDS]
		self.show_timestamp_24hour_clock	= self.settings[SETTING_TIMESTAMP_24HOUR_CLOCK]
		self.initial_window_width			= self.settings[SETTING_INITIAL_WINDOW_WIDTH]
		self.initial_window_height			= self.settings[SETTING_INITIAL_WINDOW_HEIGHT]
		self.filter_profanity				= self.settings[SETTING_FILTER_PROFANITY]
		self.use_emojis						= self.settings[SETTING_INJECT_EMOJIS]
		self.use_asciimojis					= self.settings[SETTING_INJECT_ASCIIMOJIS]
		self.autocomplete_nicks				= self.settings[SETTING_AUTOCOMPLETE_NICKS]
		self.autocomplete_emojis			= self.settings[SETTING_AUTOCOMPLETE_EMOJIS]
		self.autocomplete_asciimojis		= self.settings[SETTING_AUTOCOMPLETE_ASCIIMOJIS]
		self.autocomplete_commands			= self.settings[SETTING_AUTOCOMPLETE_COMMANDS]
		self.plain_user_lists				= self.settings[SETTING_PLAIN_USER_LISTS]
		self.connection_display_location	= self.settings[SETTING_CONNECTION_DISPLAY_LOCATION]
		self.connection_display_visible		= self.settings[SETTING_CONNECTION_DISPLAY_VISIBLE]
		self.spellcheck						= self.settings[SETTING_SPELLCHECK]
		self.spellCheckLanguage				= self.settings[SETTING_SPELLCHECK_LANGUAGE]
		self.mark_unread_messages			= self.settings[SETTING_MARK_UNSEEN_CHAT_IN_WINDOWS]
		self.unread_messages_color			= self.settings[SETTING_UNSEEN_MESSAGE_DISPLAY_COLOR]
		self.title_from_active				= self.settings[SETTING_APPLICATION_TITLE_FROM_ACTIVE]
		self.auto_create_private			= self.settings[SETTING_CREATE_PRIVATE_WINDOWS]
		self.flash_unread_private			= self.settings[SETTING_FLASH_TASKBAR_PRIVATE]
		self.connect_expand_node			= self.settings[SETTING_EXPAND_SERVER_ON_CONNECT]
		self.click_usernames				= self.settings[SETTING_CLICKABLE_USERNAMES]
		self.double_click_usernames			= self.settings[SETTING_DOUBLECLICK_USERNAMES]
		self.display_uptimes				= self.settings[SETTING_DISPLAY_UPTIME_IN_CONNECTION_DISPLAY]
		self.save_channels					= self.settings[SETTING_SAVE_JOINED_CHANNELS]
		self.top							= self.settings[SETTING_ALWAYS_ON_TOP]
		self.show_nick_on_channel_windows	= self.settings[SETTING_DISPLAY_NICK_ON_CHANNEL_WINDOWS]
		self.click_nick_change				= self.settings[SETTING_CLICK_NICK_FOR_NICKCHANGE]
		self.save_history					= self.settings[SETTING_SAVE_HISTORY]
		self.notify_fail					= self.settings[SETTING_NOTIFY_FAIL]
		self.notify_lost					= self.settings[SETTING_NOTIFY_LOST]
		self.save_logs						= self.settings[SETTING_SAVE_CHANNEL_LOGS]
		self.load_logs						= self.settings[SETTING_LOAD_CHANNEL_LOGS]
		self.save_server_logs				= self.settings[SETTING_SAVE_SERVER_LOGS]
		self.load_server_logs				= self.settings[SETTING_LOAD_SERVER_LOGS]
		self.save_private_logs				= self.settings[SETTING_SAVE_PRIVATE_LOGS]
		self.load_private_logs				= self.settings[SETTING_LOAD_PRIVATE_LOGS]
		self.load_log_max					= self.settings[SETTING_LOAD_LOG_MAX_SIZE]
		self.mark_end_of_loaded_logs		= self.settings[SETTING_MARK_END_OF_LOADED_LOGS]
		self.get_hostmasks_on_join			= self.settings[SETTING_FETCH_HOSTMASKS]
		self.max_lines_in_io_display		= self.settings[SETTING_MAX_LINES_IN_IO]
		self.show_net_traffic_from_connection = self.settings[SETTING_SHOW_NET_TRAFFIC_FROM_CONNECTION]
		self.show_channel_modes				= self.settings[SETTING_CHANNEL_WINDOW_MODES]
		self.show_channel_bans				= self.settings[SETTING_CHANNEL_WINDOW_BANS]
		self.window_command_history			= self.settings[SETTING_CMD_HISTORY]
		self.window_command_history_length	= self.settings[SETTING_CMG_HISTORY_LENGTH]

		self.ignore_join = self.settings[SETTING_CHANNEL_IGNORE_JOIN]
		self.ignore_part = self.settings[SETTING_CHANNEL_IGNORE_PART]
		self.ignore_rename = self.settings[SETTING_CHANNEL_IGNORE_RENAME]
		self.ignore_topic = self.settings[SETTING_CHANNEL_IGNORE_TOPIC]
		self.ignore_mode = self.settings[SETTING_CHANNEL_IGNORE_MODE]

		self.save_ignored = self.settings[SETTING_SAVE_IGNORE]

		self.autocomplete_macros = self.settings[SETTING_AUTO_MACRO]

		if self.save_ignored:
			self.ignored = load_ignore()

		# Load in font information from the settings file
		# If there is no font selected, load the default,
		# built-in font
		self.font							= self.settings[SETTING_FONT]
		if self.font=='':
			# Load in built-in font from the resource file
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			self.font = QFont(_fontstr,9)
		else:
			# Load the font from the stored font string
			f = QFont()
			f.fromString(self.font)
			self.font = f

		self.app.setFont(self.font)

		self.MDI = QMdiArea()
		self.setCentralWidget(self.MDI)

		self.active_window = None
		self.MDI.subWindowActivated.connect(self.updateActiveChild)

		pix = QPixmap(MDI_BACKGROUND)
		backgroundBrush = QBrush(pix)
		self.MDI.setBackground(backgroundBrush)

		# Build the connection display dock
		# Connection tree is in the self.connectionTree widget
		self.connectionDisplayDock = buildConnectionDisplay(self)

		self.connectionTree.installEventFilter(self)

		
		if self.connection_display_location=="right":
			self.addDockWidget(Qt.RightDockWidgetArea,self.connectionDisplayDock)
		elif self.connection_display_location=="left":
			self.addDockWidget(Qt.LeftDockWidgetArea,self.connectionDisplayDock)
		
		if not self.connection_display_visible:
			self.removeDockWidget(self.connectionDisplayDock)
		
		# This is only here to hold the "normalize, minimize, maximize" buttons
		# when a subwindow is maximized; it also displays the "connecting" graphic
		self.menubar = self.menuBar()
		self.menubar.setStyle(MainMenuBarStyle('Windows'))

		self.work_display = QLabel()
		self.working = QMovie(CONNECTING_ANIMATION)
		self.work_display.setMovie(self.working)
		self.work_display.hide()
		self.menubar.setCornerWidget(self.work_display)

		self.toolbar = generate_menu_toolbar(self)
		self.addToolBar(Qt.TopToolBarArea,self.toolbar)

		self.ircMenu = QMenu()
		#self.displayMenu = QMenu()
		self.settingsMenu = QMenu()
		self.helpMenu = QMenu()
		self.windowsMenu = QMenu()
		self.logMenu = QMenu()
		self.macroMenu = QMenu()
		self.connectionMenu = QMenu()

		self.toolMenuStyle = SmallerIconsMenuStyle('Windows')
		self.ircMenu.setStyle(self.toolMenuStyle)
		#self.displayMenu.setStyle(self.toolMenuStyle)
		self.settingsMenu.setStyle(self.toolMenuStyle)
		self.helpMenu.setStyle(self.toolMenuStyle)
		self.windowsMenu.setStyle(self.toolMenuStyle)
		self.logMenu.setStyle(self.toolMenuStyle)

		self.connectionMenu.setStyle(self.toolMenuStyle)

		self.buildToolbar()

		if self.top:
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
			self.show()

		
	def buildToolbar(self):

		self.toolbar.clear()
		self.ircMenu.clear()
		#self.displayMenu.clear()
		self.settingsMenu.clear()
		self.helpMenu.clear()
		self.windowsMenu.clear()
		self.logMenu.clear()
		self.connectionMenu.clear()
		self.macroMenu.clear()

		# Main menu
		add_toolbar_menu(self.toolbar,APPLICATION_NAME,self.ircMenu)

		ircMenu_Connect = fancyMenu(self,FANCY_SERVER,CONNECT_MENU_NAME,CONNECT_MENU_DESCRIPTION,self.ircMenu_Connect_Action)
		self.ircMenu.addAction(ircMenu_Connect)

		ircMenu_Network = fancyMenu(self,FANCY_NETWORK,NETWORK_MENU_NAME,NETWORK_MENU_DESCRIPTION,self.ircMenu_Network_Action)
		self.ircMenu.addAction(ircMenu_Network)

		#self.ircMenu.addSeparator()

		CONNECTIONS = erk.events.getConnections()

		if len(CONNECTIONS)==0: self.ircMenu.addSeparator()

		if len(CONNECTIONS)>0:

			entry = textSeparator(self,ACTIVE_CONNECTIONS_LABEL)
			self.ircMenu.addAction(entry)

			channels,privates,consoles = erk.events.getWindows()

			for c in CONNECTIONS:

				if c.hostname:
					title = c.hostname
				else:
					title = c.server+":"+str(c.port)

				connectionEntry_Submenu = self.ircMenu.addMenu(QIcon(SERVER_ICON),title)
				connectionEntry_Submenu.setStyle(self.toolMenuStyle)

				entry = textSeparator(self,"<b>"+c.network+"</b>")
				connectionEntry_Submenu.addAction(entry)

				entryLabel = QLabel( f"<center><small><b><i>{c.nickname}</i></b></small></center>" )
				entryAction = QWidgetAction(self)
				entryAction.setDefaultWidget(entryLabel)
				connectionEntry_Submenu.addAction(entryAction)

				entry = QAction(QIcon(IO_ICON),NET_TRAFFIC_MENU_NAME,self)
				entry.triggered.connect(lambda state,id=c.id,cmd='io': self.connectionEntryClick(id,cmd))
				connectionEntry_Submenu.addAction(entry)

				entry = QAction(QIcon(TEXT_WINDOW_ICON),MOTD_VIEW_MENU_NAME,self)
				entry.triggered.connect(lambda state,id=c.id,cmd='motd': self.connectionEntryClick(id,cmd))
				connectionEntry_Submenu.addAction(entry)

				connectionEntry_Submenu.addSeparator()

				entry = QAction(QIcon(USER_ICON),CONNECTIONS_MENU_CHANGE_NICK,self)
				entry.triggered.connect(lambda state,id=c.id,cmd='nick': self.connectionEntryClick(id,cmd))
				connectionEntry_Submenu.addAction(entry)

				entry = QAction(QIcon(CHANNEL_WINDOW_ICON),CONNECTIONS_MENU_JOIN_CHANNEL,self)
				entry.triggered.connect(lambda state,id=c.id,cmd='join': self.connectionEntryClick(id,cmd))
				connectionEntry_Submenu.addAction(entry)

				entry = QAction(QIcon(EXIT_ICON),CONNECTIONS_MENU_DISCONNECT,self)
				entry.triggered.connect(lambda state,id=c.id,cmd='disconnect': self.connectionEntryClick(id,cmd))
				connectionEntry_Submenu.addAction(entry)

			self.ircMenu.addSeparator()


		ircMenu_Restart = QAction(QIcon(RESTART_ICON),RESTART_MENU_NAME,self)
		ircMenu_Restart.triggered.connect(lambda state: restart_program())
		self.ircMenu.addAction(ircMenu_Restart)

		ircMenu_Exit = QAction(QIcon(EXIT_ICON),EXIT_MENU_NAME,self)
		ircMenu_Exit.triggered.connect(self.close)
		self.ircMenu.addAction(ircMenu_Exit)

		# Connection menu
		# self.connectionMenu

		add_toolbar_menu(self.toolbar,CONNECTION_MENU_NAME,self.connectionMenu)

		ircMenu_Ignore = QAction(QIcon(HIDE_ICON),IGNORE_MENU_NAME,self)
		ircMenu_Ignore.triggered.connect(lambda state,x=self: IgnoreDialog(x))
		self.connectionMenu.addAction(ircMenu_Ignore)

		self.connectionMenu.addSeparator()

		self.settingsMenu_FailLost_Marker = QAction(QIcon(UNCHECKED_ICON),NOTIFICATION_MENU_LOST,self)
		#self.settingsMenu_FailLost_Marker.setChecked(self.notify_lost)
		self.settingsMenu_FailLost_Marker.triggered.connect(lambda state,s="lost": self.settingsMenu_Setting(s))
		self.connectionMenu.addAction(self.settingsMenu_FailLost_Marker)

		if self.notify_lost:
			self.settingsMenu_FailLost_Marker.setIcon(QIcon(CHECKED_ICON))

		self.settingsMenu_FailNotify_Marker = QAction(QIcon(UNCHECKED_ICON),NOTIFICATION_MENU_FAILED,self)
		#self.settingsMenu_FailNotify_Marker.setChecked(self.notify_fail)
		self.settingsMenu_FailNotify_Marker.triggered.connect(lambda state,s="fail": self.settingsMenu_Setting(s))
		self.connectionMenu.addAction(self.settingsMenu_FailNotify_Marker)

		if self.notify_fail:
			self.settingsMenu_FailNotify_Marker.setIcon(QIcon(CHECKED_ICON))

		self.settingsMenu_Hostmasks = QAction(QIcon(UNCHECKED_ICON),GET_HOSTMASKS_MENU_NAME)
		#self.settingsMenu_Hostmasks.setChecked(self.get_hostmasks_on_join)
		self.settingsMenu_Hostmasks.triggered.connect(lambda state,s="hostmasks": self.settingsMenu_Setting(s))
		self.connectionMenu.addAction(self.settingsMenu_Hostmasks)

		if self.get_hostmasks_on_join:
			self.settingsMenu_Hostmasks.setIcon(QIcon(CHECKED_ICON))

		self.menuSaveIgnore = QAction(QIcon(UNCHECKED_ICON),SAVE_IGNORE_MENU_NAME,self)
		self.menuSaveIgnore.triggered.connect(lambda state,s="ignores": self.settingsMenu_Setting(s))
		self.connectionMenu.addAction(self.menuSaveIgnore)

		if self.save_ignored:
			self.menuSaveIgnore.setIcon(QIcon(CHECKED_ICON))

		self.menuSaveChannels = QAction(QIcon(UNCHECKED_ICON),SAVE_CHANNEL_MENU_NAME,self)
		self.menuSaveChannels.triggered.connect(self.menuSaveChannelsAction)
		self.connectionMenu.addAction(self.menuSaveChannels)

		if self.save_channels: self.menuSaveChannels.setIcon(QIcon(CHECKED_ICON))

		self.menuSaveHistory = QAction(QIcon(UNCHECKED_ICON),SAVE_HISTORY_MENU_NAME,self)
		self.menuSaveHistory.triggered.connect(self.menuSaveHistoryAction)
		self.connectionMenu.addAction(self.menuSaveHistory)

		if self.save_history: self.menuSaveHistory.setIcon(QIcon(CHECKED_ICON))

		# Display menu
		add_toolbar_menu(self.toolbar,DISPLAY_MENU_NAME,self.settingsMenu)

		f = self.app.font()
		s = f.toString()
		pf = s.split(',')
		font_name = pf[0]
		font_size = pf[1]

		self.menuFont = QAction(QIcon(FONT_ICON),FONT_MENU_NAME.format(font_name,font_size),self)
		self.menuFont.triggered.connect(self.displayMenu_Font_Action)
		self.settingsMenu.addAction(self.menuFont)

		entry = QAction(QIcon(FORMAT_ICON),FORMAT_MENU_NAME,self)
		entry.triggered.connect(self.menuFormat)
		self.settingsMenu.addAction(entry)

		entry = QAction(QIcon(RESIZE_ICON),WINSIZE_MENU_NAME,self)
		entry.triggered.connect(self.displayMenu_Resize_Action)
		self.settingsMenu.addAction(entry)

		self.settingsMenu.addSeparator()

		settingsMenu_Channel_Submenu = self.settingsMenu.addMenu(QIcon(CHANNEL_WINDOW_ICON),CHANNEL_WINDOW_MENU_NAME)

		channelMenu_Hide_Submenu = settingsMenu_Channel_Submenu.addMenu(QIcon(HIDE_ICON),SERVMSG_MENU_NAME)

		entry = QAction("JOIN",self,checkable=True)
		entry.setChecked(self.ignore_join)
		entry.triggered.connect(lambda state,s="ignore_join": self.settingsMenu_Setting(s))
		channelMenu_Hide_Submenu.addAction(entry)

		entry = QAction("PART",self,checkable=True)
		entry.setChecked(self.ignore_part)
		entry.triggered.connect(lambda state,s="ignore_part": self.settingsMenu_Setting(s))
		channelMenu_Hide_Submenu.addAction(entry)

		entry = QAction("NICK",self,checkable=True)
		entry.setChecked(self.ignore_rename)
		entry.triggered.connect(lambda state,s="ignore_rename": self.settingsMenu_Setting(s))
		channelMenu_Hide_Submenu.addAction(entry)

		entry = QAction("TOPIC",self,checkable=True)
		entry.setChecked(self.ignore_topic)
		entry.triggered.connect(lambda state,s="ignore_topic": self.settingsMenu_Setting(s))
		channelMenu_Hide_Submenu.addAction(entry)

		entry = QAction("MODE",self,checkable=True)
		entry.setChecked(self.ignore_mode)
		entry.triggered.connect(lambda state,s="ignore_mode": self.settingsMenu_Setting(s))
		channelMenu_Hide_Submenu.addAction(entry)

		settingsMenu_Channel_Submenu.addSeparator()

		settingsMenu_Channel_Modemenu = QAction(CHANNEL_MODE_MENU_NAME,self,checkable=True)
		settingsMenu_Channel_Modemenu.setChecked(self.show_channel_modes)
		settingsMenu_Channel_Modemenu.triggered.connect(lambda state,s="modemenu": self.settingsMenu_Setting(s))
		settingsMenu_Channel_Submenu.addAction(settingsMenu_Channel_Modemenu)

		settingsMenu_Channel_Banmenu = QAction(CHANNEL_BAN_MENU_NAME,self,checkable=True)
		settingsMenu_Channel_Banmenu.setChecked(self.show_channel_bans)
		settingsMenu_Channel_Banmenu.triggered.connect(lambda state,s="banmenu": self.settingsMenu_Setting(s))
		settingsMenu_Channel_Submenu.addAction(settingsMenu_Channel_Banmenu)

		settingMisc_Submenu_ChannelNick = QAction(DISPLAY_NICK_MENU_NAME,self,checkable=True)
		settingMisc_Submenu_ChannelNick.setChecked(self.show_nick_on_channel_windows)
		settingMisc_Submenu_ChannelNick.triggered.connect(lambda state,s="shownick": self.settingsMenu_Setting(s))
		settingsMenu_Channel_Submenu.addAction(settingMisc_Submenu_ChannelNick)

		self.settingMisc_Submenu_ClickNick = QAction(CLICK_NICK_MENU_NAME,self,checkable=True)
		self.settingMisc_Submenu_ClickNick.setChecked(self.click_nick_change)
		self.settingMisc_Submenu_ClickNick.triggered.connect(lambda state,s="clicknick": self.settingsMenu_Setting(s))
		settingsMenu_Channel_Submenu.addAction(self.settingMisc_Submenu_ClickNick)

		settingMenu_Message_Submenu = self.settingsMenu.addMenu(QIcon(CHAT_DISPLAY_ICON),MESSAGES_MENU_NAME)

		settingMenu_Auto_Private = QAction(MESSAGE_AUTO_CREATE_NAME,self,checkable=True)
		settingMenu_Auto_Private.setChecked(self.auto_create_private)
		settingMenu_Auto_Private.triggered.connect(lambda state,s="private": self.settingsMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingMenu_Auto_Private)

		settingsMenu_Flash_Private = QAction(MESSAGE_FLASH_PRIVATE_NAME,self,checkable=True)
		settingsMenu_Flash_Private.setChecked(self.flash_unread_private)
		settingsMenu_Flash_Private.triggered.connect(lambda state,s="flash": self.settingsMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingsMenu_Flash_Private)

		settingsMenu_Unseen_Marker = QAction(MESSAGE_MARK_UNSEEN_MENU_NAME,self,checkable=True)
		settingsMenu_Unseen_Marker.setChecked(self.mark_unread_messages)
		settingsMenu_Unseen_Marker.triggered.connect(lambda state,s="unseen": self.settingsMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingsMenu_Unseen_Marker)

		settingMenu_Click_Nick = QAction(MESSAGE_CLICKABLE_NICKNAME_NAME,self,checkable=True)
		settingMenu_Click_Nick.setChecked(self.click_usernames)
		settingMenu_Click_Nick.triggered.connect(lambda state,s="clicknick": self.displayMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingMenu_Click_Nick)

		settingMenu_IRC_Colors = QAction(MESSAGES_IRCCOLOR_MENU_NAME,self,checkable=True)
		settingMenu_IRC_Colors.setChecked(self.irc_color)
		settingMenu_IRC_Colors.triggered.connect(lambda state,s="irc_color": self.displayMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingMenu_IRC_Colors)

		settingMenu_HTML = QAction(MESSAGES_HTML_MENU_NAME,self,checkable=True)
		settingMenu_HTML.setChecked(self.strip_html)
		settingMenu_HTML.triggered.connect(lambda state,s="html": self.displayMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingMenu_HTML)

		settingMenu_Link = QAction(MESSAGE_LINK_MENU_NAME,self,checkable=True)
		settingMenu_Link.setChecked(self.create_links)
		settingMenu_Link.triggered.connect(lambda state,s="link": self.displayMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingMenu_Link)

		settingMenu_FilterProfanity = QAction(MESSAGE_PROFANITY_MENU_NAME,self,checkable=True)
		settingMenu_FilterProfanity.setChecked(self.filter_profanity)
		settingMenu_FilterProfanity.triggered.connect(lambda state,s="profanity": self.displayMenu_Setting(s))
		settingMenu_Message_Submenu.addAction(settingMenu_FilterProfanity)

		settingsMenu_Entry_Submenu = self.settingsMenu.addMenu(QIcon(ENTRY_ICON),TEXT_ENTRY_MENU_NAME)

		entry = QAction(ENABLE_CMD_HISTORY_MENU_NAME,self,checkable=True)
		entry.setChecked(self.window_command_history)
		entry.triggered.connect(lambda state,s="use_history": self.settingsMenu_Setting(s))
		settingsMenu_Entry_Submenu.addAction(entry)


		entry = QAction(QIcon(HISTORY_ICON),CMD_HISTORY_LEN_MENU_NAME,self)
		entry.triggered.connect(lambda state,s="cmdlen": self.settingsMenu_Setting(s))
		settingsMenu_Entry_Submenu.addAction(entry)

		settingsMenu_Entry_Submenu.addSeparator()


		settingsMenu_Emoji_Submenu = settingsMenu_Entry_Submenu.addMenu(QIcon(EMOJI_ICON),EMOJI_MENU_NAME)

		emojiSubmenu_Emojis = QAction(EMOJI_MENU_USE_EMOJIS_NAME,self,checkable=True)
		emojiSubmenu_Emojis.setChecked(self.use_emojis)
		emojiSubmenu_Emojis.triggered.connect(lambda state,s="use_emoji": self.settingsMenu_Setting(s))
		settingsMenu_Emoji_Submenu.addAction(emojiSubmenu_Emojis)

		asciimojiSubmenu_Emojis = QAction(EMOJI_MENU_USE_ASCIIMOJIS_NAME,self,checkable=True)
		asciimojiSubmenu_Emojis.setChecked(self.use_asciimojis)
		asciimojiSubmenu_Emojis.triggered.connect(lambda state,s="use_asciimojis": self.settingsMenu_Setting(s))
		settingsMenu_Emoji_Submenu.addAction(asciimojiSubmenu_Emojis)

		settingsMenu_Autocomplete_Submenu = settingsMenu_Entry_Submenu.addMenu(QIcon(AUTOCOMPLETE_ICON),AUTOCOMPLETE_MENU_NAME)

		self.autocompleteSubmenu_Macros = QAction("Macros",self,checkable=True)
		self.autocompleteSubmenu_Macros.setChecked(self.autocomplete_macros)
		self.autocompleteSubmenu_Macros.triggered.connect(lambda state,s="automacro": self.settingsMenu_Setting(s))
		settingsMenu_Autocomplete_Submenu.addAction(self.autocompleteSubmenu_Macros)

		self.autocompleteSubmenu_Commands = QAction(AUTOCOMPLETE_MENU_COMMANDS_NAME,self,checkable=True)
		self.autocompleteSubmenu_Commands.setChecked(self.autocomplete_commands)
		self.autocompleteSubmenu_Commands.triggered.connect(lambda state,s="autocommands": self.settingsMenu_Setting(s))
		settingsMenu_Autocomplete_Submenu.addAction(self.autocompleteSubmenu_Commands)

		autocompleteSubmenu_Nicks = QAction(AUTOCOMPLETE_MENU_NICKS_NAME,self,checkable=True)
		autocompleteSubmenu_Nicks.setChecked(self.autocomplete_nicks)
		autocompleteSubmenu_Nicks.triggered.connect(lambda state,s="autonick": self.settingsMenu_Setting(s))
		settingsMenu_Autocomplete_Submenu.addAction(autocompleteSubmenu_Nicks)

		self.autocompleteSubmenu_Emojis = QAction(AUTOCOMPLETE_MENU_EMOJIS_NAME,self,checkable=True)
		self.autocompleteSubmenu_Emojis.setChecked(self.autocomplete_emojis)
		self.autocompleteSubmenu_Emojis.triggered.connect(lambda state,s="autoemoji": self.settingsMenu_Setting(s))
		settingsMenu_Autocomplete_Submenu.addAction(self.autocompleteSubmenu_Emojis)

		self.autocompleteSubmenu_Asciimojis = QAction(AUTOCOMPLETE_MENU_ASCIIMOJIS_NAME,self,checkable=True)
		self.autocompleteSubmenu_Asciimojis.setChecked(self.autocomplete_asciimojis)
		self.autocompleteSubmenu_Asciimojis.triggered.connect(lambda state,s="autoasciimoji": self.settingsMenu_Setting(s))
		settingsMenu_Autocomplete_Submenu.addAction(self.autocompleteSubmenu_Asciimojis)

		settingsMenu_Spellcheck_Submenu = settingsMenu_Entry_Submenu.addMenu(QIcon(SPELLCHECK_ICON),SPELLCHECK_MENU_NAME)

		spellcheckSubmenu_Enable = QAction(SPELLCHECK_ENABLE_NAME,self,checkable=True)
		spellcheckSubmenu_Enable.setChecked(self.spellcheck)
		spellcheckSubmenu_Enable.triggered.connect(lambda state,s="spellcheck": self.settingsMenu_Setting(s))
		settingsMenu_Spellcheck_Submenu.addAction(spellcheckSubmenu_Enable)

		settingsMenu_Spellcheck_Submenu.addSeparator()

		spellcheckSubmenu_English = QAction(SPELLCHECK_LANGUAGE_ENGLISH,self,checkable=True)
		spellcheckSubmenu_English.setChecked(False)
		spellcheckSubmenu_English.triggered.connect(lambda state,l="en": self.setSpellCheckLanguage(l) )
		settingsMenu_Spellcheck_Submenu.addAction(spellcheckSubmenu_English)

		spellcheckSubmenu_French = QAction(SPELLCHECK_LANGUAGE_FRENCH,self,checkable=True)
		spellcheckSubmenu_French.setChecked(False)
		spellcheckSubmenu_French.triggered.connect(lambda state,l="fr": self.setSpellCheckLanguage(l) )
		settingsMenu_Spellcheck_Submenu.addAction(spellcheckSubmenu_French)

		spellcheckSubmenu_Spanish = QAction(SPELLCHECK_LANGUAGE_SPANISH,self,checkable=True)
		spellcheckSubmenu_Spanish.setChecked(False)
		spellcheckSubmenu_Spanish.triggered.connect(lambda state,l="es": self.setSpellCheckLanguage(l) )
		settingsMenu_Spellcheck_Submenu.addAction(spellcheckSubmenu_Spanish)

		spellcheckSubmenu_German = QAction(SPELLCHECK_LANGUAGE_GERMAN,self,checkable=True)
		spellcheckSubmenu_German.setChecked(False)
		spellcheckSubmenu_German.triggered.connect(lambda state,l="de": self.setSpellCheckLanguage(l) )
		settingsMenu_Spellcheck_Submenu.addAction(spellcheckSubmenu_German)

		if self.spellCheckLanguage=="en": spellcheckSubmenu_English.setChecked(True)
		if self.spellCheckLanguage=="fr": spellcheckSubmenu_French.setChecked(True)
		if self.spellCheckLanguage=="es": spellcheckSubmenu_Spanish.setChecked(True)
		if self.spellCheckLanguage=="de": spellcheckSubmenu_German.setChecked(True)

		if not self.spellcheck:
			spellcheckSubmenu_English.setEnabled(False)
			spellcheckSubmenu_French.setEnabled(False)
			spellcheckSubmenu_Spanish.setEnabled(False)
			spellcheckSubmenu_German.setEnabled(False)

		settingsMenu_Userlist_Submenu = self.settingsMenu.addMenu(QIcon(USERLIST_ICON),USERLIST_MENU_NAME)

		settingsUserlist_PlainUsers = QAction(PLAIN_USERS_MENU_NAME,self,checkable=True)
		settingsUserlist_PlainUsers.setChecked(self.plain_user_lists)
		settingsUserlist_PlainUsers.triggered.connect(self.togglePlainMenus)
		settingsMenu_Userlist_Submenu.addAction(settingsUserlist_PlainUsers)

		settingsUserlist_DoubleclickNick = QAction(MISC_DOUBLE_CLICK_NICKNAME_USERLIST,self,checkable=True)
		settingsUserlist_DoubleclickNick.setChecked(self.double_click_usernames)
		settingsUserlist_DoubleclickNick.triggered.connect(lambda state,s="doubleclick": self.settingsMenu_Setting(s))
		settingsMenu_Userlist_Submenu.addAction(settingsUserlist_DoubleclickNick)

		settingMenu_Connection_Submenu = self.settingsMenu.addMenu(QIcon(CONNECTION_DISPLAY_ICON),CONNECTION_DISPLAY_MENU_NAME)

		self.connectionSubmenu_Visible = QAction(CONNECTION_DISPLAY_VISIBLE,self,checkable=True)
		self.connectionSubmenu_Visible.setChecked(self.connection_display_visible)
		self.connectionSubmenu_Visible.triggered.connect(self.connectionSubmenu_Visible_Action)
		settingMenu_Connection_Submenu.addAction(self.connectionSubmenu_Visible)

		displayMisc_Submenu_ConnectExpand = QAction(MISC_EXPAND_NODE_ON_CONNECT,self,checkable=True)
		displayMisc_Submenu_ConnectExpand.setChecked(self.connect_expand_node)
		displayMisc_Submenu_ConnectExpand.triggered.connect(lambda state,s="expand": self.settingsMenu_Setting(s))
		settingMenu_Connection_Submenu.addAction(displayMisc_Submenu_ConnectExpand)

		displayMisc_Submenu_Uptime = QAction(CONNECTION_DISPLAY_UPTIME,self,checkable=True)
		displayMisc_Submenu_Uptime.setChecked(self.display_uptimes)
		displayMisc_Submenu_Uptime.triggered.connect(lambda state,s="uptime": self.settingsMenu_Setting(s))
		settingMenu_Connection_Submenu.addAction(displayMisc_Submenu_Uptime)

		settingMenu_Connection_Submenu.addSeparator()

		settingMenu_Connection_Submenu_Position = settingMenu_Connection_Submenu.addMenu(QIcon(POSITION_ICON),CONNECTION_DISPLAY_LOCATION)

		self.connectionSubmenu_Left = QAction(CONNECTION_DISPLAY_WEST,self,checkable=True)
		self.connectionSubmenu_Left.triggered.connect(lambda state,s="left": self.displayConnection_Setting(s))
		settingMenu_Connection_Submenu_Position.addAction(self.connectionSubmenu_Left)

		self.connectionSubmenu_Right = QAction(CONNECTION_DISPLAY_EAST,self,checkable=True)
		self.connectionSubmenu_Right.triggered.connect(lambda state,s="right": self.displayConnection_Setting(s))
		settingMenu_Connection_Submenu_Position.addAction(self.connectionSubmenu_Right)

		if self.connection_display_location=="right":
			self.connectionSubmenu_Right.setChecked(True)
		elif self.connection_display_location=="left":
			self.connectionSubmenu_Left.setChecked(True)

		settingMenu_Timestamp_Submenu = self.settingsMenu.addMenu(QIcon(TIMESTAMP_ICON),TIMESTAMP_MENU_NAME)

		timestampSubmenu_Visible = QAction(TIMESTAMP_DISPLAY_MENU_NAME,self,checkable=True)
		timestampSubmenu_Visible.setChecked(self.show_timestamps)
		timestampSubmenu_Visible.triggered.connect(lambda state,s="view_timestamp": self.displayMenu_Setting(s))
		settingMenu_Timestamp_Submenu.addAction(timestampSubmenu_Visible)

		timestampSubmenu_Seconds = QAction(TIMESTAMP_SECONDS_MENU_NAME,self,checkable=True)
		timestampSubmenu_Seconds.setChecked(self.show_timestamp_seconds)
		timestampSubmenu_Seconds.triggered.connect(lambda state,s="seconds_timestamp": self.displayMenu_Setting(s))
		settingMenu_Timestamp_Submenu.addAction(timestampSubmenu_Seconds)

		timestampSubmenu_24hour = QAction(TIMESTAMP_24HOUR_MENU_NAME,self,checkable=True)
		timestampSubmenu_24hour.setChecked(self.show_timestamp_24hour_clock)
		timestampSubmenu_24hour.triggered.connect(lambda state,s="24hr_timestamp": self.displayMenu_Setting(s))
		settingMenu_Timestamp_Submenu.addAction(timestampSubmenu_24hour)

		if not self.show_nick_on_channel_windows: self.settingMisc_Submenu_ClickNick.setEnabled(False)

		settingsMenu_Networking_Submenu = self.settingsMenu.addMenu(QIcon(NETWORKING_ICON),NETWORK_SETTINGS_MENU_NAME)

		self.settingsMenu_TrafficCon = QAction(TRAFFIC_START_MENU_NAME,self,checkable=True)
		self.settingsMenu_TrafficCon.setChecked(self.show_net_traffic_from_connection)
		self.settingsMenu_TrafficCon.triggered.connect(lambda state,s="traffic_connection": self.settingsMenu_Setting(s))
		settingsMenu_Networking_Submenu.addAction(self.settingsMenu_TrafficCon)

		settingsMenu_Networking_Submenu.addSeparator()

		self.settingsMenu_IOLength = QAction(QIcon(IO_ICON),TRAFFIC_MAX_LINE_MENU_NAME,self)
		self.settingsMenu_IOLength.triggered.connect(lambda state,s="io_length": self.settingsMenu_Setting(s))
		settingsMenu_Networking_Submenu.addAction(self.settingsMenu_IOLength)

		self.settingsMenu.addSeparator()

		self.menuAppTitle = QAction(QIcon(UNCHECKED_ICON),TITLE_FROM_ACTIVE_WINDOW_NAME,self)
		self.menuAppTitle.triggered.connect(self.menuWindowTitleAction)
		self.settingsMenu.addAction(self.menuAppTitle)

		if self.title_from_active: self.menuAppTitle.setIcon(QIcon(CHECKED_ICON))

		self.menuOnTop = QAction(QIcon(UNCHECKED_ICON),MENU_ALWAYS_ON_TOP,self)
		self.menuOnTop.triggered.connect(self.menuOnTopAction)
		self.settingsMenu.addAction(self.menuOnTop)

		if self.top:
			self.menuOnTop.setIcon(QIcon(CHECKED_ICON))

		# Log menu
		#settingsMenu_Logs_Submenu = self.settingsMenu.addMenu(QIcon(LOG_ICON),LOGGING_MENU_NAME)
		add_toolbar_menu(self.toolbar,LOGGING_MENU_NAME,self.logMenu)

		self.logSubmenu_Toggle = QAction(QIcon(UNCHECKED_ICON),LOGGING_MENU_SAVE_ALL_LOGS,self)
		self.logSubmenu_Toggle.triggered.connect(lambda state,s="all_log_on": self.settingsMenu_Setting(s))
		self.logMenu.addAction(self.logSubmenu_Toggle)

		if self.save_server_logs and self.save_logs and self.save_private_logs:
			self.logSubmenu_Toggle.setIcon(QIcon(CHECKED_ICON))

		self.logSubmenu_Toggle_Load = QAction(QIcon(UNCHECKED_ICON),LOGGING_MENU_LOAD_ALL_LOGS,self)
		self.logSubmenu_Toggle_Load.triggered.connect(lambda state,s="all_load_on": self.settingsMenu_Setting(s))
		self.logMenu.addAction(self.logSubmenu_Toggle_Load)

		if self.load_server_logs and self.load_logs and self.load_private_logs:
			self.logSubmenu_Toggle_Load.setIcon(QIcon(CHECKED_ICON))

		settingsMenu_Log_Length = QAction(QIcon(LOG_LENGTH_ICON),LOGGING_MENU_LENGTH,self)
		settingsMenu_Log_Length.triggered.connect(lambda state,s="log_length": self.settingsMenu_Setting(s))
		self.logMenu.addAction(settingsMenu_Log_Length)

		self.settingsMenu_Log_Mark_End = QAction(QIcon(UNCHECKED_ICON),LOGGING_MENU_MARK_END,self)
		self.settingsMenu_Log_Mark_End.triggered.connect(lambda state,s="mark_log_end": self.settingsMenu_Setting(s))
		self.logMenu.addAction(self.settingsMenu_Log_Mark_End)

		entry = textSeparator(self,"<i>"+LOGGING_WIN_TYPE_MENU_SEPARATOR+"</i>")
		self.logMenu.addAction(entry)

		logSubmenu_Console = self.logMenu.addMenu(QIcon(CONSOLE_WINDOW_ICON),LOGGING_MENU_CONSOLE)

		self.settingsMenu_Log_Console_Save = QAction(LOGGING_MENU_SAVE,self,checkable=True)
		self.settingsMenu_Log_Console_Save.setChecked(self.save_server_logs)
		self.settingsMenu_Log_Console_Save.triggered.connect(lambda state,s="console_save": self.settingsMenu_Setting(s))
		logSubmenu_Console.addAction(self.settingsMenu_Log_Console_Save)

		self.settingsMenu_Log_Console_Load = QAction(LOGGING_MENU_LOAD,self,checkable=True)
		self.settingsMenu_Log_Console_Load.setChecked(self.load_server_logs)
		self.settingsMenu_Log_Console_Load.triggered.connect(lambda state,s="console_load": self.settingsMenu_Setting(s))
		logSubmenu_Console.addAction(self.settingsMenu_Log_Console_Load)

		logSubmenu_Channel = self.logMenu.addMenu(QIcon(CHANNEL_WINDOW_ICON),LOGGING_MENU_CHANNEL)

		self.settingsMenu_Log_Channel_Save = QAction(LOGGING_MENU_SAVE,self,checkable=True)
		self.settingsMenu_Log_Channel_Save.setChecked(self.save_logs)
		self.settingsMenu_Log_Channel_Save.triggered.connect(lambda state,s="channel_save": self.settingsMenu_Setting(s))
		logSubmenu_Channel.addAction(self.settingsMenu_Log_Channel_Save)

		self.settingsMenu_Log_Channel_Load = QAction(LOGGING_MENU_LOAD,self,checkable=True)
		self.settingsMenu_Log_Channel_Load.setChecked(self.load_logs)
		self.settingsMenu_Log_Channel_Load.triggered.connect(lambda state,s="channel_load": self.settingsMenu_Setting(s))
		logSubmenu_Channel.addAction(self.settingsMenu_Log_Channel_Load)

		logSubmenu_Private = self.logMenu.addMenu(QIcon(USER_WINDOW_ICON),LOGGING_MENU_PRIVATE)

		self.settingsMenu_Log_Private_Save = QAction(LOGGING_MENU_SAVE,self,checkable=True)
		self.settingsMenu_Log_Private_Save.setChecked(self.save_private_logs)
		self.settingsMenu_Log_Private_Save.triggered.connect(lambda state,s="private_save": self.settingsMenu_Setting(s))
		logSubmenu_Private.addAction(self.settingsMenu_Log_Private_Save)

		self.settingsMenu_Log_Private_Load = QAction(LOGGING_MENU_LOAD,self,checkable=True)
		self.settingsMenu_Log_Private_Load.setChecked(self.load_private_logs)
		self.settingsMenu_Log_Private_Load.triggered.connect(lambda state,s="private_load": self.settingsMenu_Setting(s))
		logSubmenu_Private.addAction(self.settingsMenu_Log_Private_Load)

		if self.mark_end_of_loaded_logs:
			self.settingsMenu_Log_Mark_End.setIcon(QIcon(CHECKED_ICON))

		# Macro menu
		add_toolbar_menu(self.toolbar,"Macros",self.macroMenu)

		ircMenu_Macro = QAction(QIcon(MACRO_ICON),"Create new macro",self)
		ircMenu_Macro.triggered.connect(lambda state,s=self: MacroDialog(s))
		self.macroMenu.addAction(ircMenu_Macro)

		ircMenu_Macro = QAction(QIcon(DIRECTORY_ICON),"Open macro directory",self)
		ircMenu_Macro.triggered.connect(lambda state,s=MACRO_DIRECTORY: os.startfile(s))
		self.macroMenu.addAction(ircMenu_Macro)

		ircMenu_Macro = QAction(QIcon(RESTART_ICON),"Reload macros",self)
		ircMenu_Macro.triggered.connect(self.menuReloadMacros)
		self.macroMenu.addAction(ircMenu_Macro)

		act = self.active_window
		domax = False
		if act:
			if act.isMaximized() or act.subwindow.isMaximized(): domax = True

		erk.macro.MACROS = []
		target = os.path.join(erk.macro.MACRO_DIRECTORY, "*.json")
		for file in glob.glob(target):
			with open(file, "r") as macrofile:
				data = json.load(macrofile)
				data["filename"] = file
				erk.macro.MACROS.append(data)

		erk.macro.MACRO_LIST = {}
		for m in erk.macro.MACROS:
			erk.macro.MACRO_LIST[ m["trigger"] ] = m["trigger"]+" "

		if len(erk.macro.MACROS)>0:
			entry = textSeparator(self,"<i>Installed macros</i>")
			self.macroMenu.addAction(entry)

			for m in erk.macro.MACROS:
				macroname = m["trigger"]
				minargs = m["arguments"]["minimum"]
				maxargs = m["arguments"]["maximum"]
				filename = m["filename"]

				if maxargs==0:
					numargs = str(minargs)+"+ arguments"
				else:
					if minargs==maxargs:
						numargs = str(minargs)+" argument"
						if minargs>1: numargs = numargs + "S"
					else:
						numargs = str(minargs)+"-"+str(maxargs)+" argument"
						if maxargs>1: numargs = numargs +"s"


				# entry = QAction(QIcon(MACRO_ICON),macroname,self)
				# self.macroMenu.addAction(entry)

				tsLabel = QLabel("<span>&nbsp;"+macroname+"&nbsp;("+numargs+")&nbsp;</span>")
				tsAction = QWidgetAction(self)
				tsAction.setDefaultWidget(tsLabel)
				self.macroMenu.addAction(tsAction)

		if act:
			self.restoreWindow(act,act.subwindow)
			if domax: act.subwindow.showMaximized()

		# Windows menu
		add_toolbar_menu(self.toolbar,WINDOWS_MENU_NAME,self.windowsMenu)

		menuCascade = QAction(QIcon(CASCADE_ICON),MENU_CASCADE_WINDOWS_NAME,self)
		menuCascade.triggered.connect(lambda state: self.MDI.cascadeSubWindows())
		self.windowsMenu.addAction(menuCascade)

		menuTile = QAction(QIcon(TILE_ICON),MENU_TILE_WINDOWS_NAME,self)
		menuTile.triggered.connect(lambda state: self.MDI.tileSubWindows())
		self.windowsMenu.addAction(menuTile)

		menuCascade.setEnabled(False)
		menuTile.setEnabled(False)

		snetworks = {}
		channels,privates,consoles = erk.events.getWindows()
		ntwins = erk.events.getNetTraffics()

		if len(consoles)>0:
			menuCascade.setEnabled(True)
			menuTile.setEnabled(True)

		for w in channels:
			n = w.client.network
			if n in snetworks:
				snetworks[n].append(w)
			else:
				snetworks[n] = []
				snetworks[n].append(w)
		for w in privates:
			n = w.client.network
			if n in snetworks:
				snetworks[n].append(w)
			else:
				snetworks[n] = []
				snetworks[n].append(w)
		for w in consoles:
			n = w.client.network
			if n in snetworks:
				snetworks[n].append(w)
			else:
				snetworks[n] = []
				snetworks[n].append(w)
		for w in ntwins:
			if w.client.network:
				n = w.client.network
				if n in snetworks:
					snetworks[n].append(w)
				else:
					snetworks[n] = []
					snetworks[n].append(w)

		for net in snetworks:

			banner = textSeparator(self,"<b>"+net.upper()+"</b>")
			self.windowsMenu.addAction(banner)

			for window in snetworks[net]:
				if window.is_console:
					entry = QAction(QIcon(CONSOLE_WINDOW_ICON),window.name,self)
					entry.triggered.connect(lambda state,w=window,s=window.subwindow: self.restoreWindow(w,s))
					self.windowsMenu.addAction(entry)
			for window in snetworks[net]:
				if window.is_channel:
					entry = QAction(QIcon(CHANNEL_WINDOW_ICON),window.name,self)
					entry.triggered.connect(lambda state,w=window,s=window.subwindow: self.restoreWindow(w,s))
					self.windowsMenu.addAction(entry)
			for window in snetworks[net]:
				if window.is_user:
					entry = QAction(QIcon(USER_WINDOW_ICON),window.name,self)
					entry.triggered.connect(lambda state,w=window,s=window.subwindow: self.restoreWindow(w,s))
					self.windowsMenu.addAction(entry)

			for window in snetworks[net]:
				if not window.is_user and not window.is_channel and not window.is_console:
					entry = QAction(QIcon(IO_ICON),window.name+" traffic",self)
					entry.triggered.connect(lambda state,w=window,s=window.subwindow: self.restoreWindow(w,s))
					self.windowsMenu.addAction(entry)

		# Help menu
		add_toolbar_menu(self.toolbar,HELP_MENU_NAME,self.helpMenu)

		entry = QAction(QIcon(ABOUT_ICON),ABOUT_MENU_NAME,self)
		entry.triggered.connect(self.menuShowAbout)
		self.helpMenu.addAction(entry)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(LINK_ICON),"RFC 1459",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc1459": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),"RFC 2812",self)
		helpLink.triggered.connect(lambda state,u="https://tools.ietf.org/html/rfc2812": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		self.helpMenu.addSeparator()

		helpLink = QAction(QIcon(LINK_ICON),EMOJI_LIST_MENU_NAME,self)
		helpLink.triggered.connect(lambda state,u="https://www.webfx.com/tools/emoji-cheat-sheet/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		helpLink = QAction(QIcon(LINK_ICON),ASCIIMOJI_LIST_MENU_NAME,self)
		helpLink.triggered.connect(lambda state,u="http://asciimoji.com/": self.open_link_in_browser(u))
		self.helpMenu.addAction(helpLink)

		end_toolbar_menu(self.toolbar)

	def menuReloadMacros(self):

		act = self.active_window

		erk.macro.MACROS = []
		target = os.path.join(erk.macro.MACRO_DIRECTORY, "*.json")
		for file in glob.glob(target):
			with open(file, "r") as macrofile:
				data = json.load(macrofile)
				erk.macro.MACROS.append(data)

		erk.macro.MACRO_LIST = {}
		for m in erk.macro.MACROS:
			erk.macro.MACRO_LIST[ m["trigger"] ] = m["trigger"]+" "

		self.buildToolbar()

		if act:
			self.restoreWindow(act,act.subwindow)

	def open_link_in_browser(self,url):
		u = QUrl()
		u.setUrl(url)
		QDesktopServices.openUrl(u)

	def menuFormat(self):
		FormatDialog(self)

	def menuShowAbout(self):
		AboutDialog(self)

	def menuWindowTitleAction(self):
		if self.title_from_active:
			self.title_from_active = False
			self.menuAppTitle.setIcon(QIcon(UNCHECKED_ICON))
			self.setWindowTitle(APPLICATION_NAME)
		else:
			self.title_from_active = True
			self.menuAppTitle.setIcon(QIcon(CHECKED_ICON))
			self.MDI.subWindowActivated.connect(self.updateActiveChild)
		self.settings[SETTING_APPLICATION_TITLE_FROM_ACTIVE] = self.title_from_active
		save_settings(self.settings)

	def menuSaveHistoryAction(self):
		if self.save_history:
			self.save_history = False
			self.menuSaveHistory.setIcon(QIcon(UNCHECKED_ICON))
		else:
			self.save_history = True
			self.menuSaveHistory.setIcon(QIcon(CHECKED_ICON))
		self.settings[SETTING_SAVE_HISTORY] = self.save_history
		save_settings(self.settings)

	def menuSaveChannelsAction(self):
		if self.save_channels:
			self.save_channels = False
			self.menuSaveChannels.setIcon(QIcon(UNCHECKED_ICON))
		else:
			self.save_channels = True
			self.menuSaveChannels.setIcon(QIcon(CHECKED_ICON))
		self.settings[SETTING_SAVE_JOINED_CHANNELS] = self.save_channels
		save_settings(self.settings)

	def menuOnTopAction(self):
		if self.top:
			self.top = False
			self.menuOnTop.setIcon(QIcon(UNCHECKED_ICON))
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
			self.show()
		else:
			self.top = True
			self.menuOnTop.setIcon(QIcon(CHECKED_ICON))
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
			self.show()
		self.settings[SETTING_ALWAYS_ON_TOP] = self.top
		save_settings(self.settings)

	def connectionEntryClick(self,cid,cmd):

		for c in  erk.events.getConnections():
			if c.id==cid:
				if not c.registered: return

		if cmd=="motd":
			for c in  erk.events.getConnections():
				if c.id==cid:
					iowin = erk.events.hasMOTDWindow(c)
					if iowin:
						self.restoreWindow(iowin,iowin.subwindow)
						self.updateActiveChild(iowin.subwindow)
					else:
						erk.events.CreateMOTDWindow(self,c)

		if cmd=="io":
			for c in  erk.events.getConnections():
				if c.id==cid:
					iowin = erk.events.hasIOWindow(c)
					if iowin:
						self.restoreWindow(iowin,iowin.subwindow)
						self.updateActiveChild(iowin.subwindow)
					else:
						erk.events.CreateIOWindow(self,c)

		if cmd=="disconnect":
			for c in  erk.events.getConnections():
				if c.id==cid:
					self.disconnecting.append(c.server+str(c.port))
					c.quit()
					return
		
		if cmd=="nick":
			for c in  erk.events.getConnections():
				if c.id==cid:
					newnick = NewNickDialog(c.nickname,self)
					if newnick:
						c.setNick(newnick)
						return

		if cmd=="join":
			for c in  erk.events.getConnections():
				if c.id==cid:
					chaninfo = JoinChannelDialog(self)
					if chaninfo:
						channel = chaninfo[0]
						key = chaninfo[1]

						if key!='':
							c.join(channel,key)
						else:
							c.join(channel)
						return


	def setSpellCheckLanguage(self,lang):
		self.spellCheckLanguage = lang
		self.settings[SETTING_SPELLCHECK_LANGUAGE] = self.spellCheckLanguage
		save_settings(self.settings)

		if self.spellCheckLanguage=="en":
			spellcheckSubmenu_English.setChecked(True)
		else:
			spellcheckSubmenu_English.setChecked(False)

		if self.spellCheckLanguage=="fr":
			spellcheckSubmenu_French.setChecked(True)
		else:
			spellcheckSubmenu_French.setChecked(False)

		if self.spellCheckLanguage=="es":
			spellcheckSubmenu_Spanish.setChecked(True)
		else:
			spellcheckSubmenu_Spanish.setChecked(False)

		if self.spellCheckLanguage=="de":
			spellcheckSubmenu_German.setChecked(True)
		else:
			spellcheckSubmenu_German.setChecked(False)

		erk.events.setNewSpellCheckLanguage(lang)


	def updateActiveChild(self,subwindow):

		if hasattr(subwindow,"window"):
			self.active_window = subwindow.window

			if hasattr(subwindow.window,"do_actual_close"):
				if subwindow.window.do_actual_close: return

			if self.title_from_active:
				self.setWindowTitle(subwindow.windowTitle())

			# Remove window from the unseen list
			clean = []
			for win in self.unseen:
				if win.name==self.active_window.name:
					if win.client.id==self.active_window.client.id: continue
				clean.append(win)
			self.unseen = clean

			TEXT_COLOR = self.connectionTree.palette().color(QPalette.WindowText).name()
						
			# Update the connection/window display to show the
			# currently active window
			iterator = QTreeWidgetItemIterator(self.connectionTree)
			while True:
				item = iterator.value()
				if item is not None:
					if hasattr(item,"erk_window"):
						got_active = False
						if item.erk_window.name==self.active_window.name:
							if item.erk_window.client.id==self.active_window.client.id:
								item.setIcon(0,QIcon(ACTIVE_ICON))
								color = QBrush(QColor(TEXT_COLOR))
								item.setForeground(0,color)
								f = item.font(0)
								f.setBold(True)
								item.setFont(0,f)
								got_active = True
						if not got_active:
							f = item.font(0)
							f.setBold(False)
							item.setFont(0,f)
							if item.erk_channel:
								item.setIcon(0,QIcon(CHANNEL_WINDOW_ICON))
							elif item.erk_locked:
								item.setIcon(0,QIcon(LOCKED_CHANNEL_ICON))
							elif item.erk_private:
								item.setIcon(0,QIcon(USER_WINDOW_ICON))
							elif item.erk_console:
								item.setIcon(0,QIcon(CONSOLE_WINDOW_ICON))
							else:
								item.setIcon(0,QIcon(SERVER_ICON))

					iterator += 1
				else:
					break
		else:
			self.active_window = None

			if self.title_from_active:
				self.setWindowTitle(APPLICATION_NAME)

	def connectionSubmenu_Visible_Action(self):
		if self.connection_display_visible:
			self.connection_display_visible = False
			self.removeDockWidget(self.connectionDisplayDock)
		else:
			self.connection_display_visible = True
			if self.connection_display_location=="right":
				self.addDockWidget(Qt.RightDockWidgetArea,self.connectionDisplayDock)
				self.connectionDisplayDock.show()
			elif self.connection_display_location=="left":
				self.addDockWidget(Qt.LeftDockWidgetArea,self.connectionDisplayDock)
				self.connectionDisplayDock.show()

		self.settings[SETTING_CONNECTION_DISPLAY_VISIBLE] = self.connection_display_visible
		save_settings(self.settings)

	def displayConnection_Setting(self,setting):
		
		if setting=="right":
			self.removeDockWidget(self.connectionDisplayDock)
			self.addDockWidget(Qt.RightDockWidgetArea,self.connectionDisplayDock)
			self.connectionSubmenu_Right.setChecked(True)
			self.connectionSubmenu_Left.setChecked(False)
			self.connection_display_location = setting

			if not self.connection_display_visible:
				self.removeDockWidget(self.connectionDisplayDock)
			else:
				self.connectionDisplayDock.show()
		elif setting=="left":
			self.removeDockWidget(self.connectionDisplayDock)
			self.addDockWidget(Qt.LeftDockWidgetArea,self.connectionDisplayDock)
			self.connectionSubmenu_Right.setChecked(False)
			self.connectionSubmenu_Left.setChecked(True)
			self.connection_display_location = setting

			if not self.connection_display_visible:
				self.removeDockWidget(self.connectionDisplayDock)
			else:
				self.connectionDisplayDock.show()

		self.settings[SETTING_CONNECTION_DISPLAY_LOCATION] = self.connection_display_location
		save_settings(self.settings)

	def togglePlainMenus(self):
		if self.plain_user_lists:
			self.plain_user_lists = False
		else:
			self.plain_user_lists = True
		erk.events.togglePlainUserLists()

	def settingsMenu_Setting(self,setting):

		if setting=="automacro":
			if self.autocomplete_macros:
				self.autocomplete_macros = False
			else:
				self.autocomplete_macros = True
			self.settings[SETTING_AUTO_MACRO] = self.autocomplete_macros

		if setting=="ignores":
			if self.save_ignored:
				self.save_ignored = False
			else:
				self.save_ignored = True
				save_ignore(self.ignored)
			self.settings[SETTING_SAVE_IGNORE] = self.save_ignored

			if self.save_ignored:
				self.menuSaveIgnore.setIcon(QIcon(CHECKED_ICON))
			else:
				self.menuSaveIgnore.setIcon(QIcon(UNCHECKED_ICON))

		if setting=="ignore_mode":
			if self.ignore_mode:
				self.ignore_mode = False
			else:
				self.ignore_mode = True
			self.settings[SETTING_CHANNEL_IGNORE_MODE] = self.ignore_mode

		if setting=="ignore_topic":
			if self.ignore_topic:
				self.ignore_topic = False
			else:
				self.ignore_topic = True
			self.settings[SETTING_CHANNEL_IGNORE_TOPIC] = self.ignore_topic

		if setting=="ignore_rename":
			if self.ignore_rename:
				self.ignore_rename = False
			else:
				self.ignore_rename = True
			self.settings[SETTING_CHANNEL_IGNORE_RENAME] = self.ignore_rename

		if setting=="ignore_part":
			if self.ignore_part:
				self.ignore_part = False
			else:
				self.ignore_part = True
			self.settings[SETTING_CHANNEL_IGNORE_PART] = self.ignore_part

		if setting=="ignore_join":
			if self.ignore_join:
				self.ignore_join = False
			else:
				self.ignore_join = True
			self.settings[SETTING_CHANNEL_IGNORE_JOIN] = self.ignore_join

		if setting=="use_history":
			if self.window_command_history:
				self.window_command_history = False
				erk.events.reset_command_history()
			else:
				self.window_command_history = True
			self.settings[SETTING_CMD_HISTORY] = self.window_command_history

		if setting=="cmdlen":
			lsize = CmdHistoryLengthDialog(self)
			if lsize:
				self.window_command_history_length = lsize
				self.settings[SETTING_CMG_HISTORY_LENGTH] = self.window_command_history_length
				erk.events.set_command_history_length(self.window_command_history_length)

		if setting=="banmenu":
			if self.show_channel_bans:
				self.show_channel_bans = False
			else:
				self.show_channel_bans = True
			erk.events.rebuildChannelMenus()
			self.settings[SETTING_CHANNEL_WINDOW_BANS] = self.show_channel_bans

		if setting=="modemenu":
			if self.show_channel_modes:
				self.show_channel_modes = False
			else:
				self.show_channel_modes = True
			erk.events.rebuildChannelMenus()
			self.settings[SETTING_CHANNEL_WINDOW_MODES] = self.show_channel_modes

		if setting=="traffic_connection":
			if self.show_net_traffic_from_connection:
				self.show_net_traffic_from_connection = False
			else:
				self.show_net_traffic_from_connection = True
			self.settings[SETTING_SHOW_NET_TRAFFIC_FROM_CONNECTION] = self.show_net_traffic_from_connection

		if setting=="io_length":
			lsize = IOsizeDialog(self)
			if lsize:
				self.max_lines_in_io_display = lsize
				self.settings[SETTING_MAX_LINES_IN_IO] = self.max_lines_in_io_display

		if setting=="hostmasks":
			if self.get_hostmasks_on_join:
				self.get_hostmasks_on_join = False
			else:
				self.get_hostmasks_on_join = True
			self.settings[SETTING_FETCH_HOSTMASKS] = self.get_hostmasks_on_join

			if self.get_hostmasks_on_join:
				self.settingsMenu_Hostmasks.setIcon(QIcon(CHECKED_ICON))
			else:
				self.settingsMenu_Hostmasks.setIcon(QIcon(UNCHECKED_ICON))

		if setting=="all_load_on":
			if self.load_server_logs and self.load_logs and self.load_private_logs:
				self.load_server_logs = False
				self.settingsMenu_Log_Console_Load.setChecked(False)
				self.settings[SETTING_LOAD_SERVER_LOGS] = False

				self.load_logs = False
				self.settingsMenu_Log_Channel_Load.setChecked(False)
				self.settings[SETTING_LOAD_CHANNEL_LOGS] = False

				self.load_private_logs = False
				self.settingsMenu_Log_Private_Load.setChecked(False)
				self.settings[SETTING_LOAD_PRIVATE_LOGS] = False
			else:
				if not self.load_server_logs:
					self.load_server_logs = True
					self.settingsMenu_Log_Console_Load.setChecked(True)
					self.settings[SETTING_LOAD_SERVER_LOGS] = True
				if not self.load_logs:
					self.load_logs = True
					self.settingsMenu_Log_Channel_Load.setChecked(True)
					self.settings[SETTING_LOAD_CHANNEL_LOGS] = True
				if not self.load_private_logs:
					self.load_private_logs = True
					self.settingsMenu_Log_Private_Load.setChecked(True)
					self.settings[SETTING_LOAD_PRIVATE_LOGS] = True


		if setting=="all_log_on":
			if self.save_server_logs and self.save_logs and self.save_private_logs:
				self.save_server_logs = False
				self.settingsMenu_Log_Console_Save.setChecked(False)
				self.settings[SETTING_SAVE_SERVER_LOGS] = False

				self.save_logs = False
				self.settingsMenu_Log_Channel_Save.setChecked(False)
				self.settings[SETTING_SAVE_CHANNEL_LOGS] = False

				self.save_private_logs = False
				self.settingsMenu_Log_Private_Save.setChecked(False)
				self.settings[SETTING_SAVE_PRIVATE_LOGS] = False
			else:
				if not self.save_server_logs:
					self.save_server_logs = True
					self.settingsMenu_Log_Console_Save.setChecked(True)
					self.settings[SETTING_SAVE_SERVER_LOGS] = True
				if not self.save_logs:
					self.save_logs = True
					self.settingsMenu_Log_Channel_Save.setChecked(True)
					self.settings[SETTING_SAVE_CHANNEL_LOGS] = True
				if not self.save_private_logs:
					self.save_private_logs = True
					self.settingsMenu_Log_Private_Save.setChecked(True)
					self.settings[SETTING_SAVE_PRIVATE_LOGS] = True

		if setting=="log_length":
			lsize = LogsizeDialog(self)
			if lsize:
				self.load_log_max = lsize
				self.settings[SETTING_LOAD_LOG_MAX_SIZE] = self.load_log_max

		if setting=="mark_log_end":
			if self.mark_end_of_loaded_logs:
				self.mark_end_of_loaded_logs = False
			else:
				self.mark_end_of_loaded_logs = True
			self.settings[SETTING_MARK_END_OF_LOADED_LOGS] = self.mark_end_of_loaded_logs

		if setting=="private_save":
			if self.save_private_logs:
				self.save_private_logs = False
			else:
				self.save_private_logs = True
			self.settings[SETTING_SAVE_PRIVATE_LOGS] = self.save_private_logs

		if setting=="private_load":
			if self.load_private_logs:
				self.load_private_logs = False
			else:
				self.load_private_logs = True
			self.settings[SETTING_LOAD_PRIVATE_LOGS] = self.load_private_logs

		if setting=="channel_save":
			if self.save_logs:
				self.save_logs = False
			else:
				self.save_logs = True
			self.settings[SETTING_SAVE_CHANNEL_LOGS] = self.save_logs

		if setting=="channel_load":
			if self.load_logs:
				self.load_logs = False
			else:
				self.load_logs = True
			self.settings[SETTING_LOAD_CHANNEL_LOGS] = self.load_logs

		if setting=="console_save":
			if self.save_server_logs:
				self.save_server_logs = False
			else:
				self.save_server_logs = True
			self.settings[SETTING_SAVE_SERVER_LOGS] = self.save_server_logs

		if setting=="console_load":
			if self.load_server_logs:
				self.load_server_logs = False
			else:
				self.load_server_logs = True
			self.settings[SETTING_LOAD_SERVER_LOGS] = self.load_server_logs

		if setting=="fail":
			if self.notify_fail:
				self.notify_fail = False
			else:
				self.notify_fail = True
			self.settings[SETTING_NOTIFY_FAIL] = self.notify_fail

			if self.notify_fail:
				self.settingsMenu_FailNotify_Marker.setIcon(QIcon(CHECKED_ICON))
			else:
				self.settingsMenu_FailNotify_Marker.setIcon(QIcon(UNCHECKED_ICON))

		if setting=="lost":
			if self.notify_lost:
				self.notify_lost = False
			else:
				self.notify_lost = True
			self.settings[SETTING_NOTIFY_LOST] = self.notify_lost

			if self.notify_lost:
				self.settingsMenu_FailLost_Marker.setIcon(QIcon(CHECKED_ICON))
			else:
				self.settingsMenu_FailLost_Marker.setIcon(QIcon(UNCHECKED_ICON))

		if setting=="clicknick":
			if self.click_nick_change:
				self.click_nick_change = False
				erk.events.channelTurnOffNickClick()
			else:
				self.click_nick_change = True
				erk.events.channelTurnOnNickClick()
			self.settings[SETTING_CLICK_NICK_FOR_NICKCHANGE] = self.click_nick_change

		if setting=="shownick":
			if self.show_nick_on_channel_windows:
				self.show_nick_on_channel_windows = False
				erk.events.channelHideNicks()
				self.settingMisc_Submenu_ClickNick.setEnabled(False)
			else:
				self.show_nick_on_channel_windows = True
				erk.events.channelShowNicks()
				self.settingMisc_Submenu_ClickNick.setEnabled(True)
			self.settings[SETTING_DISPLAY_NICK_ON_CHANNEL_WINDOWS] = self.show_nick_on_channel_windows

		if setting=="uptime":
			if self.display_uptimes:
				self.display_uptimes = False
				erk.events.refreshDisplayConnection(self)
			else:
				self.display_uptimes = True
				erk.events.refreshDisplayConnection(self)
			self.settings[SETTING_DISPLAY_UPTIME_IN_CONNECTION_DISPLAY] = self.display_uptimes

		if setting=="doubleclick":
			if self.double_click_usernames:
				self.double_click_usernames = False
			else:
				self.double_click_usernames = True
			self.settings[SETTING_DOUBLECLICK_USERNAMES] = self.double_click_usernames

		if setting=="expand":
			if self.connect_expand_node:
				self.connect_expand_node = False
			else:
				self.connect_expand_node = True
			self.settings[SETTING_EXPAND_SERVER_ON_CONNECT] = self.connect_expand_node

		if setting=="flash":
			if self.flash_unread_private:
				self.flash_unread_private = False
			else:
				self.flash_unread_private = True
			self.settings[SETTING_FLASH_TASKBAR_PRIVATE] = self.flash_unread_private

		if setting=="private":
			if self.auto_create_private:
				self.auto_create_private = False
			else:
				self.auto_create_private = True
			self.settings[SETTING_CREATE_PRIVATE_WINDOWS] = self.auto_create_private

		# if setting=="title":
		# 	if self.title_from_active:
		# 		self.title_from_active = False
		# 	else:
		# 		self.title_from_active = True
		# 	self.settings[SETTING_APPLICATION_TITLE_FROM_ACTIVE] = self.title_from_active

		if setting=="unseen":
			if self.mark_unread_messages:
				self.mark_unread_messages = False
			else:
				self.mark_unread_messages = True
			self.settings[SETTING_MARK_UNSEEN_CHAT_IN_WINDOWS] = self.mark_unread_messages

		if setting=="spellcheck":
			if self.spellcheck:
				self.spellcheck = False
				spellcheckSubmenu_English.setEnabled(False)
				spellcheckSubmenu_French.setEnabled(False)
				spellcheckSubmenu_Spanish.setEnabled(False)
				spellcheckSubmenu_German.setEnabled(False)
			else:
				self.spellcheck = True
				spellcheckSubmenu_English.setEnabled(True)
				spellcheckSubmenu_French.setEnabled(True)
				spellcheckSubmenu_Spanish.setEnabled(True)
				spellcheckSubmenu_German.setEnabled(True)
			erk.events.toggleSpellcheck()
			self.settings[SETTING_SPELLCHECK] = self.spellcheck

		if setting=="autocommands":
			if self.autocomplete_commands:
				self.autocomplete_commands = False
			else:
				self.autocomplete_commands = True
			self.settings[SETTING_AUTOCOMPLETE_COMMANDS] = self.autocomplete_commands

		if setting=="autoasciimoji":
			if self.autocomplete_asciimojis:
				self.autocomplete_asciimojis = False
			else:
				self.autocomplete_asciimojis = True
			self.settings[SETTING_AUTOCOMPLETE_ASCIIMOJIS] = self.autocomplete_asciimojis

		if setting=="autoemoji":
			if self.autocomplete_emojis:
				self.autocomplete_emojis = False
			else:
				self.autocomplete_emojis = True
			self.settings[SETTING_AUTOCOMPLETE_EMOJIS] = self.autocomplete_emojis

		if setting=="autonick":
			if self.autocomplete_nicks:
				self.autocomplete_nicks = False
			else:
				self.autocomplete_nicks = True
			self.settings[SETTING_AUTOCOMPLETE_NICKS] = self.autocomplete_nicks

		if setting=="use_asciimojis":
			if self.use_asciimojis:
				self.use_asciimojis = False
				self.autocompleteSubmenu_Asciimojis.setEnabled(False)
			else:
				self.use_asciimojis = True
				self.autocompleteSubmenu_Asciimojis.setEnabled(True)
			self.settings[SETTING_INJECT_EMOJIS] = self.use_asciimojis

		if setting=="use_emoji":
			if self.use_emojis:
				self.use_emojis = False
				self.autocompleteSubmenu_Emojis.setEnabled(False)
			else:
				self.use_emojis = True
				self.autocompleteSubmenu_Emojis.setEnabled(True)
			self.settings[SETTING_INJECT_EMOJIS] = self.use_emojis

		if self.save_server_logs and self.save_logs and self.save_private_logs:
			self.logSubmenu_Toggle.setIcon(QIcon(CHECKED_ICON))
		else:
			self.logSubmenu_Toggle.setIcon(QIcon(UNCHECKED_ICON))

		if self.load_server_logs and self.load_logs and self.load_private_logs:
			self.logSubmenu_Toggle_Load.setIcon(QIcon(CHECKED_ICON))
		else:
			self.logSubmenu_Toggle_Load.setIcon(QIcon(UNCHECKED_ICON))

		if self.mark_end_of_loaded_logs:
			self.settingsMenu_Log_Mark_End.setIcon(QIcon(CHECKED_ICON))
		else:
			self.settingsMenu_Log_Mark_End.setIcon(QIcon(UNCHECKED_ICON))

		save_settings(self.settings)

	def displayMenu_Setting(self,setting):

		if setting=="clicknick":
			if self.click_usernames:
				self.click_usernames = False
			else:
				self.click_usernames = True
			self.settings[SETTING_CLICKABLE_USERNAMES] = self.click_usernames

		if setting=="profanity":
			if self.filter_profanity:
				self.filter_profanity = False
			else:
				self.filter_profanity = True
			self.settings[SETTING_FILTER_PROFANITY] = self.filter_profanity

		if setting=="24hr_timestamp":
			if self.show_timestamp_24hour_clock:
				self.show_timestamp_24hour_clock = False
			else:
				self.show_timestamp_24hour_clock = True
			self.settings[SETTING_TIMESTAMP_24HOUR_CLOCK] = self.show_timestamp_24hour_clock

		if setting=="seconds_timestamp":
			if self.show_timestamp_seconds:
				self.show_timestamp_seconds = False
			else:
				self.show_timestamp_seconds = True
			self.settings[SETTING_TIMESTAMP_SECONDS] = self.show_timestamp_seconds

		if setting=="view_timestamp":
			if self.show_timestamps:
				self.show_timestamps = False
			else:
				self.show_timestamps = True
			self.settings[SETTING_TIMESTAMPS] = self.show_timestamps

		if setting=="link":
			if self.create_links:
				self.create_links = False
			else:
				self.create_links = True
			self.settings[SETTING_LINKS] = self.create_links

		if setting=="irc_color":
			if self.irc_color:
				self.irc_color = False
			else:
				self.irc_color = True
			self.settings[SETTING_IRC_COLOR] = self.irc_color

		if setting=="html":
			if self.strip_html:
				self.strip_html = False
			else:
				self.strip_html = True
			self.settings[SETTING_STRIP_HTML] = self.strip_html

		save_settings(self.settings)
		erk.events.rerenderAllText()

	def connectionNodeDoubleClicked(self,item):
		if hasattr(item,"erk_window"):
			self.restoreWindow(item.erk_window,item.erk_window.subwindow)
			self.updateActiveChild(item.erk_window.subwindow)

	def displayMenu_Font_Action(self):
		font, ok = QFontDialog.getFont()
		if ok:
			# Save settings
			self.settings[SETTING_FONT] = font.toString()
			save_settings(self.settings)

			self.font = font
			erk.events.rerenderAllText_New_Font(self)

			self.app.setFont(self.font)

			s = self.font.toString()
			pf = s.split(',')
			font_name = pf[0]
			font_size = pf[1]

			self.menuFont.setText("Font" +" ("+font_name+", "+str(font_size)+"pt)")

	def displayMenu_Resize_Action(self):
		info = WindowSizeDialog(self)
		if info!=None:
			self.initial_window_width = info[0]
			self.initial_window_height = info[1]
			self.settings[SETTING_INITIAL_WINDOW_WIDTH] = self.initial_window_width
			self.settings[SETTING_INITIAL_WINDOW_HEIGHT] = self.initial_window_height
			save_settings(self.settings)

	def ircMenu_Connect_Action(self):
		info = ConnectDialog(self)
		if info!=None:
			self.connectToIRCServer(info)

	def ircMenu_Network_Action(self):
		info = NetworkDialog(self)
		if info!=None:
			self.connectToIRCServer(info)

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
				entry = [info.server,info.port]
				self.connecting.append(entry)
				self.start_working()
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
				entry = [info.server,info.port]
				self.connecting.append(entry)
				self.start_working()
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
				entry = [info.server,info.port]
				self.connecting.append(entry)
				self.start_working()
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
				entry = [info.server,info.port]
				self.connecting.append(entry)
				self.start_working()

	def eventFilter(self, source, event):

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.connectionTree):

			item = source.itemAt(event.pos())
			if item is None: return True

			if hasattr(item,"erk_server"):
				if item.erk_server:
					menu = QMenu(self)

					entry = QAction(QIcon(IO_ICON),NET_TRAFFIC_MENU_NAME,self)
					entry.triggered.connect(lambda state,id=item.erk_client.id,cmd='io': self.connectionEntryClick(id,cmd))
					menu.addAction(entry)

					entry = QAction(QIcon(TEXT_WINDOW_ICON),MOTD_VIEW_MENU_NAME,self)
					entry.triggered.connect(lambda state,id=item.erk_client.id,cmd='motd': self.connectionEntryClick(id,cmd))
					menu.addAction(entry)

					menu.addSeparator()
					
					entry = QAction(QIcon(USER_ICON),CONNECTIONS_MENU_CHANGE_NICK,self)
					entry.triggered.connect(lambda state,id=item.erk_client.id,cmd='nick': self.connectionEntryClick(id,cmd))
					menu.addAction(entry)

					entry = QAction(QIcon(CHANNEL_WINDOW_ICON),CONNECTIONS_MENU_JOIN_CHANNEL,self)
					entry.triggered.connect(lambda state,id=item.erk_client.id,cmd='join': self.connectionEntryClick(id,cmd))
					menu.addAction(entry)

					entry = QAction(QIcon(EXIT_ICON),CONNECTIONS_MENU_DISCONNECT,self)
					entry.triggered.connect(lambda state,id=item.erk_client.id,cmd='disconnect': self.connectionEntryClick(id,cmd))
					menu.addAction(entry)
				else:
					return True
			else:
				return True

			action = menu.exec_(self.connectionTree.mapToGlobal(event.pos()))

			return True




		return super(Erk, self).eventFilter(source, event)

