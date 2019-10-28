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

from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *
import erk.input

from erk.spelledit import *

import erk.dialogs.add_channel as AddChannelDialog
import erk.dialogs.new_nick as NicknameDialog
import erk.dialogs.channel_key as ChannelKeyDialog

class Window(QMainWindow):

	def add_to_log(self,user,msg):
		t = datetime.timestamp(datetime.now())
		e = [t,user,msg]
		self.log.append(e)
		self.newlog.append(e)

	def closeEvent(self, event):
		# Part channel
		if not self.gui.quitting:
			self.client.part(self.name)
			self.gui.irc_parting(self.client,self.name)

		# Save log
		if self.gui.save_logs_on_quit:
			if len(self.newlog)>0:
				saveLog(self.client.network,self.name,self.newlog)

		if not self.gui.quitting: self.gui.buildWindowMenu()

		self.subwindow.close()
		event.accept()

	def handleUserInput(self):
		user_input = self.userTextInput.text()
		self.userTextInput.setText('')

		#print(user_input)
		erk.input.handle_chat_input(self,user_input)

	def writeText(self,text):

		self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		self.channelChatDisplay.update()

	def writeTopic(self,topic):
		self.topic = topic
		if topic!='':
			self.setWindowTitle(" "+self.name+" - "+topic)
		else:
			self.setWindowTitle(" "+self.name)

	def refreshUserlist(self):
		self.writeUserlist(self.users)

	def getUserNicks(self):
		nicklist = []
		hostmasks = []

		for u in self.users:
			if len(u)<1: continue
			p = u.split('!')
			if len(p)==2:
				p[0] = p[0].replace('@','')
				p[0] = p[0].replace('+','')
				nicklist.append(p[0])
				hostmasks.append(p[1])
			else:
				nicklist.append(u)

		return nicklist + hostmasks

	def writeUserlist(self,users):

		self.users = []
		self.operator = False

		self.channelUserDisplay.clear()

		# Sort the user list
		ops = []
		voiced = []
		normal = []

		for u in users:
			if len(u)<1: continue
			self.users.append(u)
			p = u.split("!")
			if len(p)==2:
				nickname = p[0]
				hostmask = p[1]
			else:
				nickname = u
				hostmask = None

			if self.gui.plain_user_lists:
				if '@' in nickname:
					ops.append(nickname)
					if nickname==self.client.nickname: self.operator = True
				elif '+' in nickname:
					voiced.append(nickname)
				else:
					normal.append(nickname)
			else:
				if '@' in nickname:
					ops.append(nickname.replace('@',''))
					if nickname.replace('@','')==self.client.nickname: self.operator = True
				elif '+' in nickname:
					voiced.append(nickname.replace('+',''))
				else:
					normal.append(nickname)

		# Alphabetize
		ops.sort()
		voiced.sort()
		normal.sort()

		# Add ops
		for u in ops:
			ui = QListWidgetItem()
			if not self.gui.plain_user_lists: ui.setIcon(QIcon(USER_OPERATOR))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		# Add voiced
		for u in voiced:
			ui = QListWidgetItem()
			if not self.gui.plain_user_lists: ui.setIcon(QIcon(USER_VOICED))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		# Add normal
		for u in normal:
			ui = QListWidgetItem()
			if not self.gui.plain_user_lists: ui.setIcon(QIcon(USER_NORMAL))
			ui.setText(u)
			self.channelUserDisplay.addItem(ui)

		self.channelUserDisplay.update()

		
		if self.operator:
			self.buildOperatorMenus()
		else:
			self.buildUserMenus()

	def _handleDoubleClick(self, item):
		#color = item.background()
		#item.setBackground(self._red if color == self._green else self._green)
		item.setSelected(False)
		self.gui.double_click_user(self.client,item.text())

	def updateTopic(self,topic):
		self.topic = topic
		if topic=="":
			self.setWindowTitle(" "+self.name)
		else:
			self.setWindowTitle(" "+self.name+" - "+self.topic)

	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)
		else:
			link = url.toString()

			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)

	def addModes(self,modes):
		for l in modes.split():
			if l in self.modesoff:
				self.modesoff = self.modesoff.replace(l,'')
			if l in self.modeson:
				pass
			else:
				self.modeson = self.modeson + l
		self.rebuildModesMenu()
		if self.operator: self.rebuildAdminMenu()

	def removeModes(self,modes):
		for l in modes.split():
			if l in self.modeson:
				self.modeson = self.modeson.replace(l,'')
			if l in self.modesoff:
				pass
			else:
				self.modesoff = self.modesoff + l
		self.rebuildModesMenu()
		if self.operator: self.rebuildAdminMenu()

	def setKey(self,key):
		self.key = key
		self.rebuildModesMenu()
		if self.operator: self.rebuildAdminMenu()

		if self.key=='':
			self.subwindow.setWindowIcon(QIcon(CHANNEL_WINDOW))
		else:
			self.subwindow.setWindowIcon(QIcon(LOCKED_CHANNEL))
		self.gui.buildWindowMenu()

	def update_nick(self,newnick):
		if self.is_away:
			self.status_nick.setText("&nbsp;<b><small>"+newnick+" (away)</small></b>")
		else:
			self.status_nick.setText("&nbsp;<b><small>"+newnick+"</small></b>")

	def uptime_display(self,text):
		# self.uptime = QLabel('<b>00:00:00</b>&nbsp;')
		self.uptime.setText('<b>'+text+'</b>')

	def hide_uptime(self):
		self.uptime.setVisible(False)

	def show_uptime(self):
		self.uptime.setVisible(True)

	def buildUserMenus(self):
		self.menubar.clear()

		self.actModes = self.menubar.addMenu("Modes")
		self.actModes.setStyle(self.gui.menu_style)
		self.rebuildModesMenu()

		self.actBans = self.menubar.addMenu("Bans")
		self.actBans.setStyle(self.gui.menu_style)
		self.rebuildBanMenu()

	def buildOperatorMenus(self):
		self.menubar.clear()

		self.actModes = self.menubar.addMenu("Modes")
		self.actModes.setStyle(self.gui.menu_style)
		self.rebuildModesMenu()

		self.actBans = self.menubar.addMenu("Bans")
		self.actBans.setStyle(self.gui.menu_style)
		self.rebuildBanMenu()

		self.actAdmin = self.menubar.addMenu("Operator")
		self.actAdmin.setStyle(self.gui.menu_style)
		self.rebuildAdminMenu()

	def __init__(self,name,window_margin,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.is_channel = True
		self.is_console = False

		self.users = []
		self.topic = ''
		self.log = []
		self.newlog = []
		self.banlist = []

		self.modeson = ''
		self.modesoff = ''
		self.key = ''

		self.is_away = False

		self.operator = False

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(CHANNEL_WINDOW))

		self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)
		self.channelChatDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		self.channelUserDisplay = QListWidget(self)
		self.channelUserDisplay.setObjectName("channelUserDisplay")
		self.channelUserDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelUserDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])
		self.channelUserDisplay.installEventFilter(self)

		self.channelUserDisplay.itemDoubleClicked.connect(self._handleDoubleClick)

		ufont = self.channelUserDisplay.font()
		ufont.setBold(True)
		self.channelUserDisplay.setFont(ufont)

		self.userTextInput = SpellTextEdit(self)
		self.userTextInput.setObjectName("userTextInput")
		self.userTextInput.returnPressed.connect(self.handleUserInput)
		self.userTextInput.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		# Text input widget should only be one line
		fm = self.userTextInput.fontMetrics()
		self.userTextInput.setFixedHeight(fm.height()+9)
		self.userTextInput.setWordWrapMode(QTextOption.NoWrap)
		self.userTextInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.userTextInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.horizontalSplitter = QSplitter(Qt.Horizontal)
		self.horizontalSplitter.addWidget(self.channelChatDisplay)
		self.horizontalSplitter.addWidget(self.channelUserDisplay)
		self.horizontalSplitter.setSizes([450,150])

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		finalLayout.addWidget(self.horizontalSplitter)
		finalLayout.addWidget(self.userTextInput)

		
		# Status bar
		self.status = self.statusBar()
		self.status.setStyleSheet('QStatusBar::item {border: None;}')
		if self.client.hostname!=self.client.server:
			self.status_text = QLabel("<i><small>"+self.client.hostname+" ("+self.client.network+") - "+self.client.server+":"+str(self.client.port)+"</small></i>&nbsp;")
		else:
			self.status_text = QLabel("<i>"+self.client.hostname+" ("+self.client.network+")</i>&nbsp;")
		self.status_text.setAlignment(Qt.AlignRight)

		self.status_nick = QLabel("&nbsp;<b><small>"+self.client.nickname+"</small></b>")
		self.status_nick.setAlignment(Qt.AlignLeft)

		# self.status.addPermanentWidget(self.status_text,1)
		self.status.addPermanentWidget(self.status_nick,0)
		self.status.addPermanentWidget(QLabel(" "),1)
		self.status.addPermanentWidget(self.status_text,1)

		if not self.gui.display_status_bar_on_chat_windows: self.status.hide()

		self.menubar = self.menuBar()
		menuBoldText = self.menubar.font()
		menuBoldText.setBold(True)

		if self.gui.display_uptime_seconds:
			self.uptime = QLabel('<b>00:00:00</b>',self)
		else:
			self.uptime = QLabel('<b>00:00</b>',self)

		self.menubar.setCornerWidget(self.uptime,Qt.TopRightCorner)

		self.uptime.setStyleSheet('padding: 2px;')

		if not self.gui.display_uptime_chat: self.uptime.setVisible(False)

		# self.actModes = self.menubar.addMenu("Modes")
		# self.rebuildModesMenu()

		# self.actBans = self.menubar.addMenu("Bans")
		# self.rebuildBanMenu()

		# self.actAdmin = self.menubar.addMenu("Administrate")
		# self.rebuildAdminMenu()

		self.buildUserMenus()

		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		# Load logs if necessary
		if self.gui.load_logs_on_start:
			self.log = loadLog(self.client.network,self.name)

			if len(self.log)>self.gui.max_displayed_log:
				self.log = trimLog(self.log,self.gui.max_displayed_log)

			# for line in self.log:
			for line in self.log:
				timestamp = line[0]
				user = line[1]
				message = line[2]

				if len(user)>0:
					if GLYPH_ACTION in user:
						user = user.replace(GLYPH_ACTION,'')
						msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ACTION_STYLE_NAME],user+" "+message,timestamp )
					elif GLYPH_NOTICE in user:
						user = user.replace(GLYPH_NOTICE,'')
						msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[NOTICE_STYLE_NAME],user,self.gui.styles[NOTICE_TEXT_STYLE_NAME],message,timestamp )
					elif GLYPH_RESUME in user:
						user = user.replace(GLYPH_RESUME,'')
						msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[RESUME_STYLE_NAME],message,timestamp )
					elif GLYPH_ERROR in user:
						user = user.replace(GLYPH_ERROR,'')
						msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ERROR_STYLE_NAME],message,timestamp )
					else:
						if GLYPH_SELF in user:
							user = user.replace(GLYPH_SELF,'')
							ustyle = self.gui.styles[SELF_STYLE_NAME]
						else:
							ustyle = self.gui.styles[USERNAME_STYLE_NAME]
						msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],ustyle,user,self.gui.styles[MESSAGE_STYLE_NAME],message,timestamp )
				else:
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[SYSTEM_STYLE_NAME],message,timestamp )
				self.writeText(msg)

			if len(self.log)>0:

				t = datetime.timestamp(datetime.now())
				pretty = datetime.fromtimestamp(t).strftime('%B %d, %Y at %H:%M:%S')

				f = self.font()
				ptsize = f.pointSize() - 2

				self.channelChatDisplay.insertHtml(HORIZONTAL_RULE)
				self.add_to_log(GLYPH_RESUME, f"Resumed on {pretty.upper()}" )


	def rerenderText(self):
		self.channelChatDisplay.clear()

		for line in self.log:
			timestamp = line[0]
			user = line[1]
			message = line[2]

			if len(user)>0:
				if GLYPH_ACTION in user:
					user = user.replace(GLYPH_ACTION,'')
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ACTION_STYLE_NAME],user+" "+message,timestamp )
				elif GLYPH_NOTICE in user:
					user = user.replace(GLYPH_NOTICE,'')
					msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[NOTICE_STYLE_NAME],user,self.gui.styles[NOTICE_TEXT_STYLE_NAME],message,timestamp )
				elif GLYPH_RESUME in user:
					user = user.replace(GLYPH_RESUME,'')
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[RESUME_STYLE_NAME],message,timestamp )
				elif GLYPH_ERROR in user:
					user = user.replace(GLYPH_ERROR,'')
					msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[ERROR_STYLE_NAME],message,timestamp )
				else:
					if GLYPH_SELF in user:
						user = user.replace(GLYPH_SELF,'')
						ustyle = self.gui.styles[SELF_STYLE_NAME]
					else:
						ustyle = self.gui.styles[USERNAME_STYLE_NAME]
					msg = render_message(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],ustyle,user,self.gui.styles[MESSAGE_STYLE_NAME],message,timestamp )
			else:
				msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[SYSTEM_STYLE_NAME],message,timestamp )
			self.writeText(msg)

	def doAdminAdd(self,mode):
		if mode=="k":
			x = ChannelKeyDialog.Dialog()
			key = x.get_channel_information()

			if not key: return
			self.client.sendLine(f"MODE {self.name} +k {key}")
			return
		self.client.mode(self.name,True,mode,None,None)

	def doAdminRemove(self,mode):
		if mode=="k":
			self.client.sendLine(f"MODE {self.name} -k {self.key}")
			return
		self.client.mode(self.name,False,mode,None,None)

	def rebuildAdminMenu(self):
		self.actAdmin.clear()
		mset = list(dict.fromkeys(self.modeson))

		if 'k' in mset:
			mMode = QAction(QIcon(CHANNEL_WINDOW),f"Remove channel key",self)
			mMode.triggered.connect(lambda state,l="k": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(LOCKED_CHANNEL),f"Set channel key",self)
			mMode.triggered.connect(lambda state,l="k": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)

		if 'c' in mset:
			mMode = QAction(QIcon(CHANNEL_WINDOW),f"Allow IRC colors",self)
			mMode.triggered.connect(lambda state,l="c": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(BAN_ICON),f"Forbid IRC colors",self)
			mMode.triggered.connect(lambda state,l="c": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)

		if 'C' in mset:
			mMode = QAction(QIcon(CHAT_ICON),f"Allow CTCP",self)
			mMode.triggered.connect(lambda state,l="C": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(BAN_ICON),f"Forbid CTCP",self)
			mMode.triggered.connect(lambda state,l="C": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)

		if 'm' in mset:
			mMode = QAction(QIcon(CHANNEL_WINDOW),f"Turn off moderation",self)
			mMode.triggered.connect(lambda state,l="m": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(MODERATED_ICON),f"Turn on moderation",self)
			mMode.triggered.connect(lambda state,l="m": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)

		if 'n' in mset:
			mMode = QAction(QIcon(CHAT_ICON),f"Allow external messages",self)
			mMode.triggered.connect(lambda state,l="n": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(BAN_ICON),f"Forbid external messages",self)
			mMode.triggered.connect(lambda state,l="n": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)

		if 'p' in mset:
			mMode = QAction(QIcon(CHANNEL_WINDOW),f"Make channel public",self)
			mMode.triggered.connect(lambda state,l="p": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(P_ICON),f"Make channel private",self)
			mMode.triggered.connect(lambda state,l="p": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)

		if 's' in mset:
			mMode = QAction(QIcon(CHANNEL_WINDOW),f"Make channel not secret",self)
			mMode.triggered.connect(lambda state,l="s": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(S_ICON),f"Make channel secret",self)
			mMode.triggered.connect(lambda state,l="s": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)

		if 't' in mset:
			mMode = QAction(QIcon(CHANNEL_WINDOW),f"Allow anyone to change topic",self)
			mMode.triggered.connect(lambda state,l="t": self.doAdminRemove(l) )
			self.actAdmin.addAction(mMode)
		else:
			mMode = QAction(QIcon(T_ICON),f"Allow only operators to change topic",self)
			mMode.triggered.connect(lambda state,l="t": self.doAdminAdd(l) )
			self.actAdmin.addAction(mMode)


	def rebuildModesMenu(self):
		self.actModes.clear()

		mset = ''

		for l in self.modeson:

			if l == "k":
				if "k" in mset: continue
				mMode = QAction(QIcon(LOCKED_CHANNEL),f"Channel key: \"{self.key}\"",self)
				self.actModes.addAction(mMode)
				mset = mset + "k"
				continue

			if l == "c":
				if "c" in mset: continue
				mMode = QAction(QIcon(BAN_ICON),"Colors forbidden",self)
				self.actModes.addAction(mMode)
				mset = mset + "c"
				continue

			if l == "C":
				if "C" in mset: continue
				mMode = QAction(QIcon(BAN_ICON),"CTCP forbidden",self)
				self.actModes.addAction(mMode)
				mset = mset + "C"
				continue

			if l == "m":
				if "m" in mset: continue
				mMode = QAction(QIcon(MODERATED_ICON),"Moderation on",self)
				self.actModes.addAction(mMode)
				mset = mset + "m"
				continue

			if l == "n":
				if "n" in mset: continue
				mMode = QAction(QIcon(BAN_ICON),"External messages forbidden",self)
				self.actModes.addAction(mMode)
				mset = mset + "n"
				continue

			if l == "p":
				if "p" in mset: continue
				mMode = QAction(QIcon(P_ICON),"Channel is private",self)
				self.actModes.addAction(mMode)
				mset = mset + "p"
				continue

			if l == "s":
				if "s" in mset: continue
				mMode = QAction(QIcon(S_ICON),"Channel is secret",self)
				self.actModes.addAction(mMode)
				mset = mset + "s"
				continue

			if l == "t":
				if "t" in mset: continue
				mMode = QAction(QIcon(T_ICON),"Only ops can change topic",self)
				self.actModes.addAction(mMode)
				mset = mset + "t"
				continue

		if len(mset)==0:
			mMode = QAction("Unknown",self)
			f = mMode.font()
			f.setItalic(True)
			mMode.setFont(f)
			self.actModes.addAction(mMode)

	def rebuildBanMenu(self):
		self.actBans.clear()

		if len(self.banlist)==0:
			mBan = QAction("None",self)
			f = mBan.font()
			f.setItalic(True)
			mBan.setFont(f)
			self.actBans.addAction(mBan)
			return

		for b in self.banlist:
			ban = b[0]
			banner = b[1]

			if '@' in ban:
				# host ban
				mBan = QAction(QIcon(HOST_ICON),f"{ban} (by {banner})",self)
			else:
				# nick ban
				mBan = QAction(QIcon(USER_ICON),f"{ban} (by {banner})",self)
			self.actBans.addAction(mBan)

	def menuDisconnect(self):
		self.gui.disconnectFromIRC(self.client)

	def menuJoin(self):
		x = AddChannelDialog.Dialog()
		e = x.get_channel_information()

		if not e: return

		channel = e[0]
		key = e[1]

		if len(key)>0:
			self.client.join(channel,key)
		else:
			self.client.join(channel)

	def menuNick(self):
		x = NicknameDialog.Dialog()
		nick = x.get_nick_information()

		if not nick: return

		self.client.setNick(nick)

	def eventFilter(self, source, event):

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.channelUserDisplay):

			item = source.itemAt(event.pos())
			if item is None: return True

			user = item.text()

			user_nick = ''
			user_hostmask = ''
			user_is_op = False
			user_is_voiced = False

			client_is_op = False

			if self.gui.plain_user_lists:
				for u in self.users:
					p = u.split('!')
					if len(p)==2:
						nick = p[0]
						hostmask = p[1]
					else:
						nick = u
						hostmask = None

					is_op = False
					is_voiced = False

					if '@' in nick:
						tnick = nick.replace('@','')
						if tnick==self.client.nickname:
							client_is_op = True

					if nick==user:
						if '@' in nick:
							nick = nick.replace('@','')
							is_op = True
						if '+' in nick:
							nick = nick.replace('+','')
							is_voiced = True
						user_nick = nick
						user_hostmask = hostmask
						user_is_op = is_op
						user_is_voiced = is_voiced
			else:
				for u in self.users:
					p = u.split('!')
					if len(p)==2:
						nick = p[0]
						hostmask = p[1]
					else:
						nick = u
						hostmask = None

					is_op = False
					is_voiced = False

					if '@' in nick:
						tnick = nick.replace('@','')
						if tnick==self.client.nickname:
							client_is_op = True

					if '@' in nick:
						is_op = True
						nick = nick.replace('@','')

					if '+' in nick:
						is_voiced = True
						nick = nick.replace('+','')

					if nick==user:
						user_nick = nick
						user_hostmask = hostmask
						user_is_op = is_op
						user_is_voiced = is_voiced

			if user_hostmask:
				is_ignored = self.gui.is_ignored(self.client,user_hostmask)
				p = user_hostmask.split('@')
				ignoremask = '*@'+p[1]
				banmask = '*!*@'+p[1]
			else:
				is_ignored = self.gui.is_ignored(self.client,user_nick)
				ignoremask = user_nick
				banmask = user_nick

			# Menu for clicking on own nickname
			if user_nick == self.client.nickname:
				menu = QMenu(self)
				menu.setStyle(self.gui.menu_style)

				if user_is_op: actDeop = menu.addAction(QIcon(MINUS_ICON),'Take op status')
				if user_is_voiced: actDevoice = menu.addAction(QIcon(MINUS_ICON),'Take voiced status')

				if user_is_voiced or user_is_op: menu.addSeparator()

				clipMenu = menu.addMenu(QIcon(CLIPBOARD_ICON),"Copy to clipboard")
				actCopyNick = clipMenu.addAction(QIcon(USER_ICON),'Nickname')
				if user_hostmask: actHostmask = clipMenu.addAction(QIcon(HOST_ICON),'Hostmask')
				actUserlist = clipMenu.addAction(QIcon(LIST_ICON),'User list')

				action = menu.exec_(self.channelUserDisplay.mapToGlobal(event.pos()))

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

				if user_is_op:
					if action == actDeop:
						self.client.mode(self.name,False,"o",None,self.client.nickname)
						return True
				if user_is_voiced:
					if action == actDevoice:
						self.client.mode(self.name,False,"v",None,self.client.nickname)
						return True

				return True

			# Menu for everyone else
			menu = QMenu(self)
			menu.setStyle(self.gui.menu_style)

			if user_hostmask:
				hostmaskLabel = QLabel(f"&nbsp;<i><b>{user_hostmask}</b></i>&nbsp;")
				hostmaskAction = QWidgetAction(self)
				hostmaskAction.setDefaultWidget(hostmaskLabel)
				menu.addAction(hostmaskAction)

			if user_is_op:
				statusLabel = QLabel(f"&nbsp;<i>Channel operator</i>&nbsp;")
				statusAction = QWidgetAction(self)
				statusAction.setDefaultWidget(statusLabel)
				menu.addAction(statusAction)
			elif user_is_voiced:
				statusLabel = QLabel(f"&nbsp;<i>Voiced user</i>&nbsp;")
				statusAction = QWidgetAction(self)
				statusAction.setDefaultWidget(statusLabel)
				menu.addAction(statusAction)
			else:
				statusLabel = QLabel(f"&nbsp;<i>Normal user</i>&nbsp;")
				statusAction = QWidgetAction(self)
				statusAction.setDefaultWidget(statusLabel)
				menu.addAction(statusAction)

			menu.addSeparator()

			if client_is_op:
				opMenu = menu.addMenu(QIcon(USER_OPERATOR),"Operator Actions")

				if user_is_op: actDeop = opMenu.addAction(QIcon(MINUS_ICON),'Take op status')
				if not user_is_op: actOp = opMenu.addAction(QIcon(PLUS_ICON),'Give op status')

				if not user_is_op:
					if user_is_voiced: actDevoice = opMenu.addAction(QIcon(MINUS_ICON),'Take voiced status')
					if not user_is_voiced: actVoice = opMenu.addAction(QIcon(PLUS_ICON),'Give voiced status')

				actKick = opMenu.addAction(QIcon(KICK_ICON),'Kick')
				actBan = opMenu.addAction(QIcon(BAN_ICON),'Ban')
				actKickBan = opMenu.addAction(QIcon(KICKBAN_ICON),'Kick/Ban')

			if self.gui.allow_ignore:
				if is_ignored:
					actUnignore = menu.addAction(QIcon(UNIGNORE_ICON),'Unignore')
				else:
					actIgnore = menu.addAction(QIcon(IGNORE_ICON),'Ignore')

			actWhois = menu.addAction(QIcon(WHOIS_ICON),'WHOIS')

			menu.addSeparator()

			actOpenWindow = menu.addAction(QIcon(WINDOW_ICON),'Open chat window')
			actPrivate = menu.addAction(QIcon(CHAT_ICON),'Send private message')
			actNotice = menu.addAction(QIcon(CHAT_ICON),'Send notice')

			menu.addSeparator()

			clipMenu = menu.addMenu(QIcon(CLIPBOARD_ICON),"Copy to clipboard")
			actCopyNick = clipMenu.addAction(QIcon(USER_ICON),'Nickname')
			if user_hostmask: actHostmask = clipMenu.addAction(QIcon(HOST_ICON),'Hostmask')
			actUserlist = clipMenu.addAction(QIcon(LIST_ICON),'User list')

			action = menu.exec_(self.channelUserDisplay.mapToGlobal(event.pos()))

			if action == actWhois:
				self.client.sendLine(f"WHOIS {user_nick}")
				return True

			if self.gui.allow_ignore:
				if is_ignored:
					if action == actUnignore:
						if user_hostmask:
							self.gui.unignore_user(self.client,ignoremask)
						else:
							self.gui.unignore_user(self.client,ignoremask)
				else:
					if action == actIgnore:
						if user_hostmask:
							self.gui.ignore_user(self.client,ignoremask)
						else:
							self.gui.ignore_user(self.client,ignoremask)

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

			if action == actPrivate:
				self.userTextInput.setText("/msg "+user_nick+" ")
				self.userTextInput.setFocus()
				self.userTextInput.moveCursor(QTextCursor.End)
				return True

			if action == actNotice:
				self.userTextInput.setText("/notice "+user_nick+" ")
				self.userTextInput.setFocus()
				self.userTextInput.moveCursor(QTextCursor.End)
				return True

			if action == actOpenWindow:
				self.gui.double_click_user(self.client,user_nick)
				return True

			if client_is_op:

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


