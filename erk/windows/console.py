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
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore

from erk.common import *
from erk.spelledit import *
import erk.input

import erk.dialogs.add_channel as AddChannelDialog
import erk.dialogs.new_nick as NicknameDialog

class Window(QMainWindow):

	def getUserNicks(self):
		return []

	def add_to_log(self,user,msg):
		t = datetime.timestamp(datetime.now())
		e = [t,user,msg]
		self.log.append(e)
		self.newlog.append(e)

	def closeEvent(self, event):

		if self.gui.quitting:

			cid = self.client.server+":"+str(self.client.port)

			self.subwindow.close()
			self.close()
			self.gui.triggerRebuildConnections()
			event.accept()
		elif self.gui.disconnecting:

			cid = self.client.server+":"+str(self.client.port)

			self.subwindow.close()
			self.close()
			self.gui.disconnecting = False
			self.gui.triggerRebuildConnections()
			event.accept()
		else:
			# Don't close the console, just hide it
			self.gui.triggerRebuildConnections()
			self.subwindow.hide()
			event.ignore()

	def handleUserInput(self):
		user_input = self.userTextInput.text()
		self.userTextInput.setText('')

		#print(user_input)
		erk.input.handle_console_input(self,user_input)

	def writeText(self,text):

		self.channelChatDisplay.append(text)
		self.channelChatDisplay.moveCursor(QTextCursor.End)

		self.channelChatDisplay.update()

	def linkClicked(self,url):
		if url.host():
			QDesktopServices.openUrl(url)
			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)
		else:
			link = url.toString()

			self.channelChatDisplay.setSource(QUrl())
			self.channelChatDisplay.moveCursor(QTextCursor.End)

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

		#self.rebuildServerInfoMenu()

	def __init__(self,name,window_margin,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.log = []
		self.newlog = []

		self.is_channel = False
		self.is_console = True

		self.network_url = None
		self.network = "Unknown"

		self.hostname = None

		# BEGIN IRC SERVER INFO

		self.maxnicklen = 0
		self.maxchannels = 0
		self.channellen = 0
		self.topiclen = 0
		self.kicklen = 0
		self.awaylen = 0
		self.maxtargets = 0
		#self.network = ""
		self.casemapping = ""
		self.cmds = []
		self.prefix = []
		self.chanmodes = []
		self.supports = []
		self.modes = 0
		self.maxmodes = []

		# END IRC SERVER INFO

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(CONSOLE_WINDOW))

		self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)
		self.channelChatDisplay.setStyleSheet(self.gui.styles["base"])

		self.userTextInput = SpellTextEdit(self)
		self.userTextInput.setObjectName("userTextInput")
		self.userTextInput.returnPressed.connect(self.handleUserInput)
		self.userTextInput.setStyleSheet(self.gui.styles["base"])

		# Text input widget should only be one line
		fm = self.userTextInput.fontMetrics()
		self.userTextInput.setFixedHeight(fm.height()+9)
		self.userTextInput.setWordWrapMode(QTextOption.NoWrap)
		self.userTextInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.userTextInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		finalLayout.addWidget(self.channelChatDisplay)
		finalLayout.addWidget(self.userTextInput)

		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		self.menubar = self.menuBar()
		menuBoldText = self.menubar.font()
		menuBoldText.setBold(True)

		# Load logs if necessary
		cid = self.client.server+":"+str(self.client.port)
		if self.gui.load_logs_on_start:
			self.log = loadLog(cid,None)

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
						msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["action"],user+" "+message,timestamp )
					elif GLYPH_NOTICE in user:
						user = user.replace(GLYPH_NOTICE,'')
						msg = render_message(self.gui, self.gui.styles["timestamp"],self.gui.styles["notice"],user,self.gui.styles["message"],message,timestamp )
					elif GLYPH_RESUME in user:
						user = user.replace(GLYPH_RESUME,'')
						msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["resume"],message,timestamp )
					elif GLYPH_ERROR in user:
						user = user.replace(GLYPH_ERROR,'')
						msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["error"],message,timestamp )
					else:
						if GLYPH_SELF in user:
							user = user.replace(GLYPH_SELF,'')
							ustyle = self.gui.styles["self"]
						else:
							ustyle = self.gui.styles["username"]
						msg = render_message(self.gui, self.gui.styles["timestamp"],ustyle,user,self.gui.styles["message"],message,timestamp )
				else:
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["system"],message,timestamp )
				self.writeText(msg)

			if len(self.log)>0:
				t = datetime.timestamp(datetime.now())
				# pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')
				pretty = datetime.fromtimestamp(t).strftime('%B %d, %Y at %H:%M:%S')
				msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["resume"],"Resumed on "+pretty )
				self.writeText(msg)
				self.add_to_log(GLYPH_RESUME,"Resumed on "+pretty )

	def rerenderText(self):
		self.channelChatDisplay.clear()
		for line in self.log:
			timestamp = line[0]
			user = line[1]
			message = line[2]

			if len(user)>0:
				if GLYPH_ACTION in user:
					user = user.replace(GLYPH_ACTION,'')
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["action"],user+" "+message,timestamp )
				elif GLYPH_NOTICE in user:
					user = user.replace(GLYPH_NOTICE,'')
					msg = render_message(self.gui, self.gui.styles["timestamp"],self.gui.styles["notice"],user,self.gui.styles["message"],message,timestamp )
				elif GLYPH_RESUME in user:
					user = user.replace(GLYPH_RESUME,'')
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["resume"],message,timestamp )
				elif GLYPH_ERROR in user:
					user = user.replace(GLYPH_ERROR,'')
					msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["error"],message,timestamp )
				else:
					if GLYPH_SELF in user:
						user = user.replace(GLYPH_SELF,'')
						ustyle = self.gui.styles["self"]
					else:
						ustyle = self.gui.styles["username"]
					msg = render_message(self.gui, self.gui.styles["timestamp"],ustyle,user,self.gui.styles["message"],message,timestamp )
			else:
				msg = render_system(self.gui, self.gui.styles["timestamp"],self.gui.styles["system"],message,timestamp )
			self.writeText(msg)

	def menuServNetLink(self):
		if self.network_url:
			u = QUrl()
			u.setUrl(self.network_url)
			QDesktopServices.openUrl(u)

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

	def closeMe(self):
		self.gui.closeConsole(self.client)

	def restoreMe(self):
		self.gui.restoreConsole(self.client)

	def buildConnectionMenu(self,mdimenu):

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

		if self.hostname:
			server_host = self.hostname
		else:
			p = self.name.split(":")
			if len(p)==2:
				server_host = p[0]
			else:
				server_host = self.name


		servName = QAction(QIcon(HOST_ICON),server_host,self)
		mdimenu.addAction(servName)

		servmenu = QMenu()
		servName.setMenu(servmenu)

		consoleC = QAction(QIcon(CONSOLE_WINDOW),"Console",self)
		consoleC.triggered.connect(self.restoreMe)
		servmenu.addAction(consoleC)

		infomenu = servmenu.addMenu("Server Settings")
		infomenu.setIcon(QIcon(SERVER_SETTINGS_ICON))

		if self.network_url:
			servNetLink = QAction(QIcon(LINK_ICON),self.network+" Website",self)
			servNetLink.triggered.connect(self.menuServNetLink)
			servmenu.addAction(servNetLink)

		servmenu.addSeparator()

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum channels:</b> {maxchannels}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum nick length:</b> {maxnicklen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum channel length:</b> {channellen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum topic length:</b> {topiclen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum kick length:</b> {kicklen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum away length:</b> {awaylen}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum message targets:</b> {maxtargets}&nbsp;&nbsp;",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		el = QLabel(f"&nbsp;&nbsp;<b>Maximum modes per user:</b> {modes}",self)
		e = QWidgetAction(self)
		e.setDefaultWidget(el)
		infomenu.addAction(e)

		infomenu.addSeparator()

		maxmodesmenu = QMenu("Maximum modes",self)
		for c in maxmodes:
			e = QAction(F"{c[0]}: {c[1]}", self) 
			maxmodesmenu.addAction(e)
		infomenu.addMenu(maxmodesmenu)

		cmdmenu = QMenu("Commands",self)
		for c in cmds:
			e = QAction(F"{c}", self) 
			cmdmenu.addAction(e)
		infomenu.addMenu(cmdmenu)

		supportsmenu = QMenu("Supports",self)
		for c in supports:
			e = QAction(F"{c}", self) 
			supportsmenu.addAction(e)
		infomenu.addMenu(supportsmenu)

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
		infomenu.addMenu(chanmodemenu)

		prefixmenu = QMenu("Prefixes",self)
		for c in prefix:
			m = c[0]
			s = c[1]
			if s=="&": s="&&"
			e = QAction(F"{m}: {s}", self)
			if m=="o": e.setIcon(QIcon(USER_OPERATOR))
			if m=="v": e.setIcon(QIcon(USER_VOICED))
			prefixmenu.addAction(e)
		infomenu.addMenu(prefixmenu)

		servmenu.addSeparator()

		conChangeNick = QAction(QIcon(USER_ICON),"Change Nickname",self)
		conChangeNick.triggered.connect(self.menuNick)
		servmenu.addAction(conChangeNick)

		conJoinChannel = QAction(QIcon(CHANNEL_WINDOW),"Join channel",self)
		conJoinChannel.triggered.connect(self.menuJoin)
		servmenu.addAction(conJoinChannel)

		conDisconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		conDisconnect.triggered.connect(self.menuDisconnect)
		servmenu.addAction(conDisconnect)

		#mdimenu.addSeparator()
