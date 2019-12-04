
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *
from erk.resources import *
from erk.strings import *
from erk.config import *
from erk.spelledit import *
from erk.format import *
import erk.events
import erk.input

from erk.widgets import *

from erk.dialogs import NewNickDialog,TopicDialog,KeyDialog

class ChatDisplay(QTextBrowser):

	def __init__(self, *args):
		QTextBrowser.__init__(self, *args)

		self.parent = args[0]

	def contextMenuEvent(self, event):

		popup_menu = self.createStandardContextMenu()

		counter = 0

		if "t" in self.parent.modeson:
			if self.parent.operator:
				pmenuitem = QAction(QIcon(TOPIC_ICON),CHAT_DISPLAY_CONTEXT_SET_TOPIC,self)
				pmenuitem.triggered.connect(self.parent.setTopic)
				popup_menu.insertAction(popup_menu.actions()[counter],pmenuitem)
				counter = counter + 1
		else:
			pmenuitem = QAction(QIcon(TOPIC_ICON),CHAT_DISPLAY_CONTEXT_SET_TOPIC,self)
			pmenuitem.triggered.connect(self.parent.setTopic)
			popup_menu.insertAction(popup_menu.actions()[counter],pmenuitem)
			counter = counter + 1

		if self.parent.operator:

			cmodes = QMenu("Set modes")
			cmodes.setIcon(QIcon(CHANNEL_WINDOW_ICON))

			if "k" in self.parent.modeson:
				pmenuitem = QAction(QIcon(LOCKED_CHANNEL_ICON),CHAT_DISPLAY_CONTEXT_RKEY,self)
				pmenuitem.triggered.connect(lambda state,f="unlock": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(LOCKED_CHANNEL_ICON),CHAT_DISPLAY_CONTEXT_KEY,self)
				pmenuitem.triggered.connect(lambda state,f="lock": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			if "t" in self.parent.modeson:
				pmenuitem = QAction(QIcon(T_ICON),CHAT_DISPLAY_CONTEXT_ATOPIC,self)
				pmenuitem.triggered.connect(lambda state,f="yestopic": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(T_ICON),CHAT_DISPLAY_CONTEXT_OTOPIC,self)
				pmenuitem.triggered.connect(lambda state,f="notopic": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			if "m" in self.parent.modeson:
				pmenuitem = QAction(QIcon(M_ICON),CHAT_DISPLAY_CONTEXT_UMOD,self)
				pmenuitem.triggered.connect(lambda state,f="unmoderate": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(M_ICON),CHAT_DISPLAY_CONTEXT_MOD,self)
				pmenuitem.triggered.connect(lambda state,f="moderate": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			if "c" in self.parent.modeson:
				pmenuitem = QAction(QIcon(FANCY_COLOR),CHAT_DISPLAY_CONTEXT_ACOLOR,self)
				pmenuitem.triggered.connect(lambda state,f="yescolors": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(BAN_ICON),CHAT_DISPLAY_CONTEXT_COLOR,self)
				pmenuitem.triggered.connect(lambda state,f="nocolors": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			if "n" in self.parent.modeson:
				pmenuitem = QAction(QIcon(MESSAGE_ICON),CHAT_DISPLAY_CONTEXT_AEXTMSG,self)
				pmenuitem.triggered.connect(lambda state,f="yesx": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(BAN_ICON),CHAT_DISPLAY_CONTEXT_EXT_MSG,self)
				pmenuitem.triggered.connect(lambda state,f="nox": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			if "C" in self.parent.modeson:
				pmenuitem = QAction(QIcon(MESSAGE_ICON),CHAT_DISPLAY_CONTEXT_ACTCP,self)
				pmenuitem.triggered.connect(lambda state,f="yesctcp": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(BAN_ICON),CHAT_DISPLAY_CONTEXT_CTCP,self)
				pmenuitem.triggered.connect(lambda state,f="noctcp": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			if "s" in self.parent.modeson:
				pmenuitem = QAction(QIcon(S_ICON),CHAT_DISPLAY_CONTEXT_APUB,self)
				pmenuitem.triggered.connect(lambda state,f="yespub": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(S_ICON),CHAT_DISPLAY_CONTEXT_PUB,self)
				pmenuitem.triggered.connect(lambda state,f="nopub": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			if "i" in self.parent.modeson:
				pmenuitem = QAction(QIcon(I_ICON),CHAT_DISPLAY_CONTEXT_AINVITE,self)
				pmenuitem.triggered.connect(lambda state,f="yesinvite": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)
			else:
				pmenuitem = QAction(QIcon(I_ICON),CHAT_DISPLAY_CONTEXT_INVITE,self)
				pmenuitem.triggered.connect(lambda state,f="noinvite": self.parent.contextOpAction(f))
				cmodes.addAction(pmenuitem)

			popup_menu.insertMenu(popup_menu.actions()[counter],cmodes)
			counter = counter + 1

		if counter>0:
			popup_menu.insertSeparator(popup_menu.actions()[counter])

		popup_menu.exec_(event.globalPos())

		#return super().contextMenuEvent(event)

class Window(QMainWindow):

	def contextOpAction(self,function):
		if function=="noinvite":
			self.client.mode(self.name,True,"i")
			return
		if function=="yesinvite":
			self.client.mode(self.name,False,"i")
			return

		if function=="notopic":
			self.client.mode(self.name,True,"t")
			return
		if function=="yestopic":
			self.client.mode(self.name,False,"t")
			return

		if function=="nopub":
			self.client.mode(self.name,True,"s")
			return
		if function=="yespub":
			self.client.mode(self.name,False,"s")
			return

		if function=="noctcp":
			self.client.mode(self.name,True,"C")
			return
		if function=="yesctcp":
			self.client.mode(self.name,False,"C")
			return
		if function=="nox":
			self.client.mode(self.name,True,"n")
			return
		if function=="yesx":
			self.client.mode(self.name,False,"n")
			return
		if function=="yescolors":
			self.client.mode(self.name,False,"c")
			return
		if function=="nocolors":
			self.client.mode(self.name,True,"c")
			return
		if function=="lock":
			newkey = KeyDialog(self)
			if newkey:
				self.client.sendLine("MODE "+self.name+" +k "+newkey)
				return
		if function=="unlock":
			self.client.sendLine("MODE "+self.name+" -k "+self.key)
			return
		if function=="unmoderate":
			self.client.mode(self.name,False,"m")
			return
		if function=="moderate":
			self.client.mode(self.name,True,"m")
			return

	def setTopic(self):
		newtopic = TopicDialog(self.topic,self)
		if newtopic:
			self.client.topic(self.name,newtopic)

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

		if len(self.part_message)>0:
			self.client.sendLine("PART "+self.name+" "+self.part_message)
		else:
			self.client.sendLine("PART "+self.name)

		erk.events.erk_parted_channel(self.gui,self.client,self.name)

		if len(self.newlog)>0:
			if self.gui.save_logs:
				saveLog(self.client.network,self.name,self.newlog)

		if self.gui.title_from_active:
			self.gui.setWindowTitle(APPLICATION_NAME)

		if self.gui.save_channels:
			clean = []
			for e in self.client.kwargs["autojoin"]:
				if e[0]==self.name: continue
				clean.append(e)
			self.client.kwargs["autojoin"] = clean

		self.subwindow.close()
		event.accept()

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


		erk.input.channel_window_input(self.gui,self.client,self,user_input)

	def writeText(self,text):

		self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		self.channelChatDisplay.update()

	def rerenderText(self):
		self.reapplyStyles()
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

	def reapplyStyles(self):

		text_color = get_style_attribute(self.gui.styles[BASE_STYLE_NAME],"color")
		if not text_color: text_color = "#000000"

		self.channelUserDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])
		BASE_COLOR = self.channelUserDisplay.palette().color(QPalette.Base).name()
		DARKER_COLOR = color_variant(BASE_COLOR,-15)

		user_display_qss='''
			QListView::item::selected {
				border: 0px;
				background: !BASE!;
			}
			QListView::item:hover {
				background: !DARKER!;
			}
			QListView {
				show-decoration-selected: 0;
			}
			QListView::item {
				color: !TEXT_COLOR!;
			}
		'''
		user_display_qss = user_display_qss.replace('!DARKER!',DARKER_COLOR)
		user_display_qss = user_display_qss.replace('!BASE!',BASE_COLOR)
		user_display_qss = user_display_qss.replace('!TEXT_COLOR!',text_color)
		user_display_qss = user_display_qss + self.gui.styles[BASE_STYLE_NAME]

		self.channelUserDisplay.setStyleSheet(user_display_qss)

		self.channelChatDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])
		self.userTextInput.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])


	def writeLog(self,mtype,user,message):

		is_unseen = self.gui.window_activity_is_unseen(self)

		if mtype==CHAT_MESSAGE or mtype==ACTION_MESSAGE or mtype==NOTICE_MESSAGE:
			self.gui.window_activity(self)

		if self.gui.window_activity_is_unseen(self)!=is_unseen:
			# Window *just* got added to the unseen list
			if self.gui.mark_unread_messages:
				self.channelChatDisplay.insertHtml(UNSEEN_MESSAGES_MARKER)

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

		entry = [mtype,user,message,datetime.timestamp(datetime.now())]
		self.log.append(entry)
		self.newlog.append(entry)

	def writeTopic(self,topic):
		self.topic = topic
		if topic!='':
			self.setWindowTitle(" "+self.name+" - "+topic)
		else:
			self.setWindowTitle(" "+self.name)

	def refreshUserlist(self):
		self.writeUserlist(self.users)

	def part(self,nickname):
		del self.hostmasks[nickname]

	def join(self,nickname,hostmask):
		self.hostmasks[nickname] = hostmask

	def writeUserlist(self,users):

		self.users = []
		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False

		self.channelUserDisplay.clear()

		# Sort the user list
		owners = []
		admins = []
		ops = []
		halfops = []
		voiced = []
		normal = []

		for u in users:
			if len(u)<1: continue
			self.users.append(u)
			p = u.split("!")
			if len(p)==2:
				nickname = p[0]
				hostmask = p[1]
				self.hostmasks[nickname] = hostmask
			else:
				nickname = u
				hostmask = None

			if self.plain_user_lists:
				if '@' in nickname:
					ops.append(nickname)
					if nickname==self.client.nickname: self.operator = True
				elif '+' in nickname:
					voiced.append(nickname)
					if nickname==self.client.nickname: self.voiced = True
				elif '~' in nickname:
					owners.append(nickname)
					if nickname==self.client.nickname: self.owner = True
				elif '&' in nickname:
					admins.append(nickname)
					if nickname==self.client.nickname: self.admin = True
				elif '%' in nickname:
					halfops.append(nickname)
					if nickname==self.client.nickname: self.halfop = True
				else:
					normal.append(nickname)
			else:
				if '@' in nickname:
					ops.append(nickname.replace('@',''))
					if nickname.replace('@','')==self.client.nickname: self.operator = True
				elif '+' in nickname:
					voiced.append(nickname.replace('+',''))
					if nickname.replace('+','')==self.client.nickname: self.voiced = True
				elif '~' in nickname:
					owners.append(nickname.replace('~',''))
					if nickname.replace('~','')==self.client.nickname: self.owner = True
				elif '&' in nickname:
					admins.append(nickname.replace('&',''))
					if nickname.replace('&','')==self.client.nickname: self.admin = True
				elif '%' in nickname:
					halfops.append(nickname.replace('%',''))
					if nickname.replace('%','')==self.client.nickname: self.halfop = True
				else:
					normal.append(nickname)

		# Store a list of the nicks in this channel
		self.nicks = owners + admins + halfops + ops + voiced + normal

		# Alphabetize
		owners.sort()
		admins.sort()
		halfops.sort()
		ops.sort()
		voiced.sort()
		normal.sort()

		# Add owners
		for u in owners:
			ui = QListWidgetItem()
			if not self.plain_user_lists: ui.setIcon(QIcon(USERLIST_OWNER_ICON))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		# Add admins
		for u in admins:
			ui = QListWidgetItem()
			if not self.plain_user_lists: ui.setIcon(QIcon(USERLIST_ADMIN_ICON))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		# Add ops
		for u in ops:
			ui = QListWidgetItem()
			if not self.plain_user_lists: ui.setIcon(QIcon(USERLIST_OPERATOR_ICON))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		# Add halfops
		for u in halfops:
			ui = QListWidgetItem()
			if not self.plain_user_lists: ui.setIcon(QIcon(USERLIST_HALFOP_ICON))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		# Add voiced
		for u in voiced:
			ui = QListWidgetItem()
			if not self.plain_user_lists: ui.setIcon(QIcon(USERLIST_VOICED_ICON))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		# Add normal
		for u in normal:
			ui = QListWidgetItem()
			if not self.plain_user_lists: ui.setIcon(QIcon(USERLIST_NORMAL_ICON))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		self.channelUserDisplay.update()

	def _handleDoubleClick(self, item):
		item.setSelected(False)
		if self.gui.double_click_usernames:
			erk.events.user_double_click(self.gui,self.client,item.text())

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

	def setKey(self,key):
		self.key = key
		changed = []
		for e in self.client.kwargs["autojoin"]:
			if e[0]==self.name:
				e[1] = key
			changed.append(e)
		self.client.kwargs["autojoin"] = changed

		if self.key=='':
			self.subwindow.setWindowIcon(QIcon(CHANNEL_WINDOW_ICON))
		else:
			self.subwindow.setWindowIcon(QIcon(LOCKED_CHANNEL_ICON))
		#self.rebuildModesMenu()
		self.buildMenuBar()

	def nickClicked(self,link):
		newnick = NewNickDialog(self.client.nickname,self)
		if newnick:
			self.client.setNick(newnick)

	def __init__(self,name,window_margin,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.uptime = 0

		self.is_channel = True
		self.is_console = False
		self.is_user = False

		self.part_message = ''

		self.is_away = False

		# self.plain_user_lists = False
		self.plain_user_lists = self.gui.plain_user_lists

		self.users = []
		self.topic = ''

		self.nicks = []

		self.log = []
		self.newlog = []

		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False

		self.modeson = ''
		self.modesoff = ''
		self.key = ''

		self.banlist = []

		self.hostmasks = {}

		self.history_buffer = ['']
		self.history_buffer_pointer = 0
		# self.history_buffer_max = 20
		self.history_buffer_max = self.gui.window_command_history_length

		if self.gui.save_channels:
			found = False
			for e in self.client.kwargs["autojoin"]:
				if e[0]==self.name: found = True
			if not found: self.client.kwargs["autojoin"].append([self.name,self.key])

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(CHANNEL_WINDOW_ICON))

		self.channelChatDisplay = ChatDisplay(self)
		#self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)

		self.channelUserDisplay = QListWidget(self)
		self.channelUserDisplay.setObjectName("channelUserDisplay")
		self.channelUserDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelUserDisplay.installEventFilter(self)

		# Make sure that user status icons are just a little
		# bigger than the user entry text
		fm = QFontMetrics(self.channelChatDisplay.font())
		fheight = fm.height() + 2
		self.channelUserDisplay.setIconSize(QSize(fheight,fheight))

		self.channelUserDisplay.itemDoubleClicked.connect(self._handleDoubleClick)

		# User item background will darken slightly when hovered over
		self.channelUserDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		text_color = get_style_attribute(self.gui.styles[BASE_STYLE_NAME],"color")
		if not text_color: text_color = "#000000"

		BASE_COLOR = self.channelUserDisplay.palette().color(QPalette.Base).name()
		DARKER_COLOR = color_variant(BASE_COLOR,-15)

		user_display_qss='''
			QListView::item::selected {
				border: 0px;
				background: !BASE!;
			}
			QListView::item:hover {
				background: !DARKER!;
			}
			QListView {
				show-decoration-selected: 0;
			}
			QListView::item {
				color: !TEXT_COLOR!;
			}
		'''
		user_display_qss = user_display_qss.replace('!DARKER!',DARKER_COLOR)
		user_display_qss = user_display_qss.replace('!BASE!',BASE_COLOR)
		user_display_qss = user_display_qss.replace('!TEXT_COLOR!',text_color)
		user_display_qss = user_display_qss + self.gui.styles[BASE_STYLE_NAME]

		self.channelUserDisplay.setStyleSheet(user_display_qss)

		self.ufont = self.channelUserDisplay.font()
		self.ufont.setBold(True)
		self.channelUserDisplay.setFont(self.ufont)

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

		self.userTextInput.changeLanguage(self.gui.spellCheckLanguage)

		self.channelChatDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])
		self.userTextInput.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		self.horizontalSplitter = QSplitter(Qt.Horizontal)
		self.horizontalSplitter.addWidget(self.channelChatDisplay)
		self.horizontalSplitter.addWidget(self.channelUserDisplay)
		
		# Set the initial splitter ratio
		ulwidth = (fm.width('X') + 2) + (fm.width('X')*18)
		mwidth = self.gui.initial_window_width-ulwidth
		self.horizontalSplitter.setSizes([mwidth,ulwidth])

		# Set the userlist to be no larger than 16 characters + icon
		self.channelUserDisplay.setMaximumWidth(ulwidth)

		if self.gui.click_nick_change:
			#self.nick = QLabel("<a style=\"color:inherit; text-decoration: none;\" href=\"!\"><b><small> "+self.client.nickname+" </small></b></a>")
			l = self.create_nick_link().format(self.client.nickname)
			self.nick = QLabel(l)
		else:
			#self.nick = QLabel("<b><small> "+self.client.nickname+" </small></b>")
			l = self.create_nick_no_link().format(self.client.nickname)
			self.nick = QLabel(l)
		self.nick.linkActivated.connect(self.nickClicked)

		#self.nick.setFixedWidth(fm.width('X')*15)

		entryLayout = QHBoxLayout()
		entryLayout.setSpacing(window_margin)
		entryLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		entryLayout.addWidget(self.nick)
		entryLayout.addWidget(self.userTextInput)


		finalLayout = QVBoxLayout()
		finalLayout.setSpacing(window_margin)
		finalLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		finalLayout.addWidget(self.horizontalSplitter)
		# finalLayout.addWidget(self.userTextInput)
		finalLayout.addLayout(entryLayout)

		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		if not self.gui.show_nick_on_channel_windows: self.nick.hide()

		# Load logs
		if self.gui.load_logs:
			self.log = loadLog(self.client.network,self.name)
			if len(self.log)>0:
				if len(self.log)>self.gui.load_log_max:
					self.log = trimLog(self.log,self.gui.load_log_max)
				if self.gui.mark_end_of_loaded_logs: self.writeLog(HR_MESSAGE,'','')
				self.rerenderText()

		# Menubar
		self.menubar = self.menuBar()
		self.buildMenuBar()

	def keyPressDown(self):
		if self.gui.window_command_history:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer - 1
			if self.history_buffer_pointer < 0:
				self.history_buffer_pointer = len(self.history_buffer) - 1
			self.userTextInput.setText(self.history_buffer[self.history_buffer_pointer])
			self.userTextInput.moveCursor(QTextCursor.End)

	def keyPressUp(self):
		if self.gui.window_command_history:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer + 1
			if len(self.history_buffer) - 1 < self.history_buffer_pointer:
				self.history_buffer_pointer = 0
			self.userTextInput.setText(self.history_buffer[self.history_buffer_pointer])
			self.userTextInput.moveCursor(QTextCursor.End)
		

	def setAway(self):
		self.is_away = True
		#self.status_away.setText("<i>Away</i>")
		self.refresh_nick_display()

	def setUnaway(self):
		self.is_away = False
		#self.status_away.setText("")
		self.refresh_nick_display()

	def refresh_nick_display(self):
		if self.gui.click_nick_change:
			l = self.create_nick_link().format(self.client.nickname)
		else:
			l = self.create_nick_no_link().format(self.client.nickname)

		self.nick.setText(l)

	def create_nick_link(self):
		if self.is_away:
			return "<a style=\"color:inherit; text-decoration: none;\" href=\"!\"><small>&nbsp;<i>{}</i>&nbsp;</small></a>"
		else:
			return "<a style=\"color:inherit; text-decoration: none;\" href=\"!\"><b><small>&nbsp;{}&nbsp;</small></b></a>"

	def create_nick_no_link(self):
		if self.is_away:
			return "<small>&nbsp;<i>{}</i>&nbsp;</small>"
		else:
			return "<b><small>&nbsp;{}&nbsp;</small></b>"

	def setNick(self,nick):

		if self.gui.click_nick_change:
			l = self.create_nick_link().format(nick)
		else:
			l = self.create_nick_no_link().format(nick)

		self.nick.setText(l)

		# if self.gui.click_nick_change:
		# 	self.nick.setText("<a style=\"color:inherit; text-decoration: none;\" href=\"!\"><b><small> "+nick+" </small></b></a>")
		# else:
		# 	self.nick.setText("<b><small> "+nick+" </small></b>")

	def onNickClick(self):
		#self.nick.setText("<a style=\"color:inherit; text-decoration: none;\" href=\"!\"><b><small> "+self.client.nickname+" </small></b></a>")

		l = self.create_nick_link().format(self.client.nickname)
		self.nick.setText((l))

	def offNickClick(self):
		#self.nick.setText("<b><small> "+self.client.nickname+" </small></b>")
		l = self.create_nick_no_link().format(self.client.nickname)
		self.nick.setText((l))

	def buildMenuBar(self):
		self.menubar.clear()

		if self.gui.show_channel_modes:
			if len(self.modeson)>0:
				self.actModes = self.menubar.addMenu("Modes")
				self.rebuildModesMenu()

		if self.gui.show_channel_bans:
			if len(self.banlist)>0:
				self.actBans = self.menubar.addMenu("Bans")
				self.rebuildBanMenu()

	def rebuildBanMenu(self):
		self.actBans.clear()

		for b in self.banlist:
			ban = b[0]
			banner = b[1]
				
			# mBan = menuPlainLabel(self,f"<b>{ban}</b> (by {banner})")
			mBan = menuPlainLabel(self,BAN_MENU_ENTRY.format(ban,banner))
			self.actBans.addAction(mBan)

	def rebuildModesMenu(self):
		self.actModes.clear()

		mset = ''

		for l in self.modeson:

			if l == "k":
				if "k" in mset: continue
				#mMode = QAction(QIcon(K_ICON),f"Channel key: \"{self.key}\"",self)
				mMode = menuIconLabel(self,K_ICON,MODE_KEY+f" \"{self.key}\"")
				self.actModes.addAction(mMode)
				mset = mset + "k"
				continue

			if l == "c":
				if "c" in mset: continue
				#mMode = QAction(QIcon(BAN_ICON),"Colors forbidden",self)
				mMode = menuIconLabel(self,MODE_BAN_ICON,MODE_NO_COLORS)
				self.actModes.addAction(mMode)
				mset = mset + "c"
				continue

			if l == "C":
				if "C" in mset: continue
				#mMode = QAction(QIcon(BAN_ICON),"CTCP forbidden",self)
				mMode = menuIconLabel(self,MODE_BAN_ICON,MODE_CTCP_BAN)
				self.actModes.addAction(mMode)
				mset = mset + "C"
				continue

			if l == "m":
				if "m" in mset: continue
				#mMode = QAction(QIcon(M_ICON),"Moderation on",self)
				mMode = menuIconLabel(self,M_ICON,MODE_MODERATED)
				self.actModes.addAction(mMode)
				mset = mset + "m"
				continue

			if l == "n":
				if "n" in mset: continue
				#mMode = QAction(QIcon(BAN_ICON),"External messages forbidden",self)
				mMode = menuIconLabel(self,MODE_BAN_ICON,MODE_NO_EXTERNAL)
				self.actModes.addAction(mMode)
				mset = mset + "n"
				continue

			if l == "p":
				if "p" in mset: continue
				#mMode = QAction(QIcon(P_ICON),"Channel is private",self)
				mMode = menuIconLabel(self,P_ICON,MODE_PRIVATE)
				self.actModes.addAction(mMode)
				mset = mset + "p"
				continue

			if l == "s":
				if "s" in mset: continue
				#mMode = QAction(QIcon(S_ICON),"Channel is secret",self)
				mMode = menuIconLabel(self,S_ICON,MODE_SECRET)
				self.actModes.addAction(mMode)
				mset = mset + "s"
				continue

			if l == "t":
				if "t" in mset: continue
				#mMode = QAction(QIcon(T_ICON),"Only ops can change topic",self)
				mMode = menuIconLabel(self,T_ICON,MODE_OPS_TOPIC)
				self.actModes.addAction(mMode)
				mset = mset + "t"
				continue

			if l == "i":
				if "i" in mset: continue
				#mMode = QAction(QIcon(T_ICON),"Only ops can change topic",self)
				mMode = menuIconLabel(self,I_ICON,MODE_INVITE_ONLY)
				self.actModes.addAction(mMode)
				mset = mset + "i"
				continue

		if len(mset)==0:
			#mMode = QAction("Unknown",self)
			mMode = menuIconLabel(self,MODE_UNKNOWN_ICON,"<i>"+MODE_NO_KNOWN+"</i>")
			self.actModes.addAction(mMode)


	def eventFilter(self, source, event):

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.channelUserDisplay):

			item = source.itemAt(event.pos())
			if item is None: return True

			user = item.text()

			user_nick = ''
			user_hostmask = None
			user_is_op = False
			user_is_voiced = False
			user_is_ignored = False

			for u in self.users:
				p = u.split('!')
				if len(p)==2:
					nick = p[0]
					hostmask = p[1]
					if self.gui.is_ignored(self.client,nick):
						user_is_ignored = True
					elif self.gui.is_ignored(self.client,hostmask):
						user_is_ignored = True
				else:
					nick = u
					hostmask = None
					if self.gui.is_ignored(self.client,nick):
						user_is_ignored = True

				if '@' in nick:
					is_op = True
					nick = nick.replace('@','')
				else:
					is_op = False
				if '+' in nick:
					is_voiced = True
					nick = nick.replace('+','')
				else:
					is_voiced = False
				if nick==user:
					user_nick = nick
					if hostmask:
						user_hostmask = hostmask
					else:
						if nick in self.hostmasks:
							user_hostmask = self.hostmasks[nick]
					user_is_op = is_op
					user_is_voiced = is_voiced
					break

			# Menu for everyone else
			menu = QMenu(self)
			menu.setStyle(SmallerIconsMenuStyle("Windows"))

			banner = textSeparator(self,"<b>"+user_nick+"</b>")
			menu.addAction(banner)

			if user_hostmask:
				max_length = 32
				if len(user_hostmask)>max_length:
					if len(user_hostmask)>=max_length+3:
						offset = max_length-3
					elif len(user_hostmask)==max_length+2:
						offset = max_length-2
					elif len(user_hostmask)==max_length+1:
						offset = max_length-1
					else:
						offset = max_length
					display_hostmask = user_hostmask[0:offset]+"..."
				else:
					display_hostmask = user_hostmask
				tsLabel = QLabel( "<center><small>"+display_hostmask+"</small></center>" )
				tsAction = QWidgetAction(self)
				tsAction.setDefaultWidget(tsLabel)
				menu.addAction(tsAction)

			if user_is_op:
				statusLabel = QLabel(f"<center><small><i>"+USERLIST_CONTEXT_OP+"</i></small></center>")
				statusAction = QWidgetAction(self)
				statusAction.setDefaultWidget(statusLabel)
				menu.addAction(statusAction)
			elif user_is_voiced:
				statusLabel = QLabel(f"<center><small><i>"+USERLIST_CONTEXT_VOICE+"</i></small></center>")
				statusAction = QWidgetAction(self)
				statusAction.setDefaultWidget(statusLabel)
				menu.addAction(statusAction)
			else:
				statusLabel = QLabel(f"<center><small><i>"+USERLIST_CONTEXT_NORMAL+"</i></small></center>")
				statusAction = QWidgetAction(self)
				statusAction.setDefaultWidget(statusLabel)
				menu.addAction(statusAction)


			if self.operator:
				opMenu = menu.addMenu(QIcon(USERLIST_OPERATOR_ICON),USERLIST_CONTEXT_OP_ACT)

				if user_is_op: actDeop = opMenu.addAction(QIcon(MINUS_ICON),USERLIST_CONTEXT_TAKE_OP)
				if not user_is_op: actOp = opMenu.addAction(QIcon(PLUS_ICON),USERLIST_CONTEXT_GIVE_OP)

				if not user_is_op:
					if user_is_voiced: actDevoice = opMenu.addAction(QIcon(MINUS_ICON),USERLIST_CONTEXT_TAKE_VOICE)
					if not user_is_voiced: actVoice = opMenu.addAction(QIcon(PLUS_ICON),USERLIST_CONTEXT_GIVE_VOICE)

				actKick = opMenu.addAction(QIcon(KICK_ICON),USERLIST_CONTEXT_KICK)
				actBan = opMenu.addAction(QIcon(BAN_ICON),USERLIST_CONTEXT_BAN)
				actKickBan = opMenu.addAction(QIcon(KICKBAN_ICON),USERLIST_CONTEXT_KICK_BAN)

				menu.addSeparator()

			if user_is_ignored:
				actIgnore = menu.addAction(QIcon(HIDE_ICON),USERLIST_CONTEXT_UNIGNORE)
			else:
				actIgnore = menu.addAction(QIcon(HIDE_ICON),USERLIST_CONTEXT_IGNORE)

			actWhois = menu.addAction(QIcon(WHOIS_ICON),USERLIST_CONTEXT_WHOIS)
			actOpenWindow = menu.addAction(QIcon(USER_WINDOW_ICON),USERLIST_CONTEXT_OPEN_WIN)
			actPrivate = menu.addAction(QIcon(MESSAGE_ICON),USERLIST_CONTEXT_PRIV)

			clipMenu = menu.addMenu(QIcon(CLIPBOARD_ICON),USERLIST_CONTEXT_COPY)
			actCopyNick = clipMenu.addAction(QIcon(USER_ICON),USERLIST_CONTEXT_CNICK)
			if user_hostmask: actHostmask = clipMenu.addAction(QIcon(SERVER_ICON),USERLIST_CONTEXT_CHOST)
			actUserlist = clipMenu.addAction(QIcon(USERLIST_ICON),USERLIST_CONTEXT_CLIST)
			actTopic = clipMenu.addAction(QIcon(TOPIC_ICON),USERLIST_CONTEXT_CTOPIC)

			action = menu.exec_(self.channelUserDisplay.mapToGlobal(event.pos()))

			if action == actIgnore:
				if user_is_ignored:
					self.gui.remove_ignore(self.client,user_nick)
					if user_hostmask:
						self.gui.remove_ignore(self.client,user_hostmask)
					return True
				else:
					if user_hostmask:
						h = user_hostmask.split('@')[1]
						# self.gui.add_ignore(self.client,user_hostmask)
						self.gui.add_ignore(self.client,"*@"+h)
					else:
						self.gui.add_ignore(self.client,user_nick)
					return True

			if action == actWhois:
					self.client.sendLine("WHOIS "+user_nick)
					return True

			if action == actPrivate:
				self.userTextInput.setText("/msg "+user_nick+" ")
				self.userTextInput.setFocus()
				self.userTextInput.moveCursor(QTextCursor.End)
				return True

			if action == actOpenWindow:
				erk.events.user_double_click(self.gui,self.client,user_nick)
				return True

			if action == actTopic:
				cb = QApplication.clipboard()
				cb.clear(mode=cb.Clipboard)
				cb.setText(f"{self.topic}", mode=cb.Clipboard)
				return True

			if action == actUserlist:
				ulist = "\n".join(self.users)
				cb = QApplication.clipboard()
				cb.clear(mode=cb.Clipboard)
				cb.setText(f"{ulist}", mode=cb.Clipboard)
				return True

			if action == actCopyNick:
				cb = QApplication.clipboard()
				cb.clear(mode=cb.Clipboard)
				cb.setText(f"{user_nick}", mode=cb.Clipboard)
				return True

			if user_hostmask:
				if action == actHostmask:
					cb = QApplication.clipboard()
					cb.clear(mode=cb.Clipboard)
					cb.setText(f"{user_hostmask}", mode=cb.Clipboard)
					return True

			if self.operator:

				if action == actKick:
					self.client.kick(self.name,user_nick)
					return True

				if action == actBan:
					self.client.mode(self.name,True,"b",None,None,banmask)
					return True

				if action == actKickBan:
					self.client.mode(self.name,True,"b",None,None,banmask)
					self.client.kick(self.name,user_nick)
					return True

				if user_is_op:
					if action == actDeop:
						self.client.mode(self.name,False,"o",None,user_nick)
						return True

				if not user_is_op:
					if user_is_voiced:
						if action == actDevoice:
							self.client.mode(self.name,False,"v",None,user_nick)
							return True

				if not user_is_op:
					if action == actOp:
						self.client.mode(self.name,True,"o",None,user_nick)
						return True

				if not user_is_op:
					if not user_is_voiced:
						if action == actVoice:
							self.client.mode(self.name,True,"v",None,user_nick)
							return True

			return True



		return super(Window, self).eventFilter(source, event)