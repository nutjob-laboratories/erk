
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *
from erk.resources import *
from erk.strings import *
from erk.config import *
import erk.events
import erk.input

from erk.format import *

from erk.spelledit import *

from erk.dialogs import NewNickDialog,JoinChannelDialog

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

		if self.do_actual_close:
			if len(self.newlog)>0:
				if self.gui.save_server_logs:
					saveLog(self.client.server+":"+str(self.client.port),None,self.newlog)
			if self.gui.title_from_active:
				self.gui.setWindowTitle(APPLICATION_NAME)
			self.subwindow.close()
			self.close()
			event.accept()
			self.gui.set_window_not_active(self)
			return

		if self.gui.title_from_active:
			self.gui.setWindowTitle(APPLICATION_NAME)

		self.subwindow.hide()
		self.hide()
		event.ignore()

		self.gui.set_window_not_active(self)

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

		erk.input.server_window_input(self.gui,self.client,self,user_input)

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
				self.gui.click_usernames,
			)

			self.channelChatDisplay.append(line)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

	def writeLog(self,mtype,user,message):

		if mtype==NOTICE_MESSAGE:
			if len(user.strip())==0:
				mtype = SYSTEM_MESSAGE

		is_unseen = self.gui.window_activity_is_unseen(self)

		if mtype==CHAT_MESSAGE or mtype==ACTION_MESSAGE:
			self.gui.window_activity(self)

		if self.gui.window_activity_is_unseen(self)!=is_unseen:
			# Window *just* got added to the unseen list
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
			self.gui.click_usernames,
		)

		self.channelChatDisplay.append(line)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		entry = [mtype,user,message,timestamp]
		self.log.append(entry)
		self.newlog.append(entry)

	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)
		else:
			link = url.toString()
			if self.gui.click_usernames:
				link = link.strip()
				erk.events.user_double_click(self.gui,self.client,link)
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
		self.is_console = True
		self.is_user = False

		self.do_actual_close = False

		self.history_buffer = ['']
		self.history_buffer_pointer = 0
		# self.history_buffer_max = 20
		self.history_buffer_max = self.gui.window_command_history_length

		self.nicks = []

		self.log = []
		self.newlog = []

		self.maxnicklen = 0
		self.maxchannels = 0
		self.channellen = 0
		self.topiclen = 0
		self.kicklen = 0
		self.awaylen = 0
		self.maxtargets = 0
		self.casemapping = ""
		self.cmds = []
		self.prefix = []
		self.chanmodes = []
		self.supports = []
		self.modes = 0
		self.maxmodes = []

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(CONSOLE_WINDOW_ICON))

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

		self.channelChatDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])
		self.userTextInput.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		self.userTextInput.keyUp.connect(self.keyPressUp)
		self.userTextInput.keyDown.connect(self.keyPressDown)

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		finalLayout.addWidget(self.channelChatDisplay)
		finalLayout.addWidget(self.userTextInput)

		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		self.menubar = self.menuBar()

		self.commands = self.menubar.addMenu(CONSOLE_COMMAND_MENU_NAME)

		entry = QAction(QIcon(USER_WINDOW_ICON),CONSOLE_MENU_CHANGE_NICK,self)
		entry.triggered.connect(lambda state,id=self.client.id,cmd='nick': self.connectionEntryClick(id,cmd))
		self.commands.addAction(entry)

		entry = QAction(QIcon(CHANNEL_WINDOW_ICON),CONSOLE_MENU_JOIN_CHANNEL,self)
		entry.triggered.connect(lambda state,id=self.client.id,cmd='join': self.connectionEntryClick(id,cmd))
		self.commands.addAction(entry)

		self.commands.addSeparator()

		entry = QAction(QIcon(EXIT_ICON),CONSOLE_MENU_DISCONNECT,self)
		entry.triggered.connect(lambda state,id=self.client.id,cmd='disconnect': self.connectionEntryClick(id,cmd))
		self.commands.addAction(entry)

		self.config = self.menubar.addMenu(CONSOLE_SERVER_CONFIG_MENU_NAME)

		self.rebuildConfigurationMenu()

		# Load logs
		if self.gui.load_server_logs:
			self.log = loadLog(self.client.server+":"+str(self.client.port),None)
			if len(self.log)>0:
				if len(self.log)>self.gui.load_log_max:
					self.log = trimLog(self.log,self.gui.load_log_max)
				# writeLog(self,mtype,user,message):
				if self.gui.mark_end_of_loaded_logs: self.writeLog(HR_MESSAGE,'','')
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

	def connectionEntryClick(self,cid,cmd):

		if cmd=="disconnect":
			for c in  erk.events.getConnections():
				if c.id==cid:
					self.gui.disconnecting.append(c.server+str(c.port))
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

	def rebuildConfigurationMenu(self):

		supports = self.supports # list
		maxchannels = self.maxchannels
		maxnicklen = self.maxnicklen
		channellen = self.channellen
		topiclen = self.topiclen
		kicklen = self.kicklen
		awaylen = self.awaylen
		maxtargets = self.maxtargets
		modes = self.modes
		chanmodes = self.chanmodes #list
		prefix = self.prefix # list
		cmds = self.cmds # list
		casemapping = self.casemapping
		maxmodes = self.maxmodes

		self.config.clear()

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_CHANNELS+f":</b> {maxchannels}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_NICK_LEN+f":</b> {maxnicklen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_CHANNEL_LEN+f":</b> {channellen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_TOPIC_LEN+f":</b> {topiclen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_KICK_LEN+f":</b> {kicklen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_AWAY_LEN+f":</b> {awaylen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_MSG_TARGETS+f":</b> {maxtargets}&nbsp;&nbsp;",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>"+CONFIG_MAX_MODES_PER_USER+f":</b> {modes}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		self.config.addAction(e)

		self.config.addSeparator()

		maxmodesmenu = QMenu(CONFIG_MAX_MODES,self)
		for c in maxmodes:
			e = QAction(F"{c[0]}: {c[1]}", self) 
			maxmodesmenu.addAction(e)
		self.config.addMenu(maxmodesmenu)

		cmdmenu = QMenu(CONFIG_COMMANDS,self)
		for c in cmds:
			e = QAction(F"{c}", self) 
			cmdmenu.addAction(e)
		self.config.addMenu(cmdmenu)

		supportsmenu = QMenu(CONFIG_SUPPORTS,self)
		for c in supports:
			e = QAction(F"{c}", self) 
			supportsmenu.addAction(e)
		self.config.addMenu(supportsmenu)

		chanmodemenu = QMenu(CONFIG_CHANNEL_MODES,self)
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
		self.config.addMenu(chanmodemenu)

		prefixmenu = QMenu(CONFIG_PREFIXES,self)
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
		self.config.addMenu(prefixmenu)

	def server_options(self,options):

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

		if len(maxmodes)>0: self.maxmodes = maxmodes
		if maxnicklen>0: self.maxnicklen = maxnicklen
		if maxchannels > 0: self.maxchannels = maxchannels
		if channellen > 0: self.channellen = channellen
		if topiclen > 0: self.topiclen = topiclen
		if kicklen > 0: self.kicklen = kicklen
		if awaylen > 0: self.awaylen = awaylen
		if maxtargets > 0: self.maxtargets = maxtargets
		if modes > 0: self.modes = modes
		if casemapping != "": self.casemapping = casemapping

		if len(cmds)>0:
			for c in cmds:
				self.cmds.append(c)

		if len(prefix)>0: self.prefix = prefix
		if len(chanmodes)>0: self.chanmodes = chanmodes
		if len(supports)>0:
			for s in supports:
				self.supports.append(s)

		self.rebuildConfigurationMenu()