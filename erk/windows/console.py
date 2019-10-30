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

	def uptime_display(self,text):
		# self.uptime = QLabel('<b>00:00:00</b>&nbsp;')
		self.uptime.setText('<b>'+text+'</b>')

	def hide_uptime(self):
		self.menubar.setVisible(False)
		self.uptime.setVisible(False)

	def show_uptime(self):
		self.menubar.setVisible(True)
		self.uptime.setVisible(True)

	def writeLine(self,line,is_input=True):
		if self.io_hidden: return

		t = datetime.timestamp(datetime.now())
		pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')

		ui = QListWidgetItem()

		f = ui.font()
		f.setBold(False)
		
		if not is_input:
			ui.setBackground(QColor("#E7E7E7"))
			prefix = pretty +' <- '
		else:
			ui.setBackground(QColor("#FFFFFF"))
			ui.setFont(f)
			prefix = pretty +' -> '

		ui.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)

		ui.setText(prefix+line)
		self.ircLineDisplay.addItem(ui)

		self.ircLineDisplay.scrollToBottom()

		if self.ircLineDisplay.count()>self.maximum_dump_lines:
			self.ircLineDisplay.takeItem(0)

	def hideIOTab(self):
		self.io_hidden = True
		self.tabs.setTabEnabled(1,False)
		self.tabs.setStyleSheet('QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} QTabBar::tab::enabled {width: 0; height: 0; margin: 0; padding: 0; border: none;}')
		self.IOtab.setIcon(QIcon(PLUS_ICON))
		self.IOtab.setText("Show connection tab")
		self.IOtab2.setIcon(QIcon(PLUS_ICON))
		self.IOtab2.setText("Show connection tab")

	def showIOTab(self):
		self.ircLineDisplay.clear()
		self.io_hidden = False
		self.tabs.setTabEnabled(1,True)
		self.tabs.setStyleSheet('')
		self.IOtab.setIcon(QIcon(MINUS_ICON))
		self.IOtab.setText("Hide connection tab")
		self.IOtab2.setIcon(QIcon(MINUS_ICON))
		self.IOtab2.setText("Hide connection tab")

	def menuIOtab(self):
		if self.io_hidden:
			self.io_hidden = False
			self.showIOTab()
		else:
			self.io_hidden = True
			self.hideIOTab()

	def menuToggleSend(self):
		if self.enable_send:
			self.enable_send = False
		else:
			self.enable_send = True

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

		self.maximum_dump_lines = 300

		self.io_hidden = False

		self.enable_send = False

		# BEGIN IRC SERVER INFO

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

		# END IRC SERVER INFO

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(CONSOLE_WINDOW))

		self.channelChatDisplay = QTextBrowser(self)
		self.channelChatDisplay.setObjectName("channelChatDisplay")
		self.channelChatDisplay.setFocusPolicy(Qt.NoFocus)
		self.channelChatDisplay.anchorClicked.connect(self.linkClicked)

		css =  "QTextEdit { background-image: url(" + CONSOLE_BACKGROUND + "); background-attachment: fixed; background-repeat: no-repeat; background-position: top right; "+self.gui.styles[BASE_STYLE_NAME]+" }"
		self.channelChatDisplay.setStyleSheet(css)

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

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		finalLayout.addWidget(self.channelChatDisplay)
		finalLayout.addWidget(self.userTextInput)

		interface = QWidget()
		interface.setLayout(finalLayout)

		self.tabs = QTabWidget()
		self.tabs.addTab(interface,"Console")

		fontbold = self.tabs.font()
		fontbold.setBold(True)
		self.tabs.setFont(fontbold)

		fontnormal = self.tabs.font()
		fontnormal.setBold(False)

		self.ircLineDisplay = QListWidget(self)
		self.ircLineDisplay.setObjectName("ircLineDisplay")
		self.ircLineDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		self.ircLineDisplay.setIconSize(QSize(15, 15))
		self.ircLineDisplay.setWordWrap(True)

		ufont = self.ircLineDisplay.font()
		ufont.setBold(True)
		self.ircLineDisplay.setFont(ufont)

		dumpLayout = QVBoxLayout()
		dumpLayout.setContentsMargins(window_margin,window_margin,window_margin,window_margin)
		dumpLayout.addWidget(self.ircLineDisplay)

		interface = QWidget()
		interface.setLayout(dumpLayout)

		self.tabs.addTab(interface,"Connection")

		self.setCentralWidget(self.tabs)

		self.menubar = QMenuBar()
		self.menubar.setFont(fontnormal)
		self.tabs.widget(0).layout().setMenuBar(self.menubar)

		servermenu = self.menubar.addMenu("Server")
		servermenu.setStyle(self.gui.menu_style)

		conListChannels = QAction(QIcon(LIST_ICON),"List channels",self)
		conListChannels.triggered.connect(self.menuListChannels)
		servermenu.addAction(conListChannels)

		conChangeNick = QAction(QIcon(USER_ICON),"Change nickname",self)
		conChangeNick.triggered.connect(self.menuNick)
		servermenu.addAction(conChangeNick)

		conJoinChannel = QAction(QIcon(CHANNEL_WINDOW),"Join channel",self)
		conJoinChannel.triggered.connect(self.menuJoin)
		servermenu.addAction(conJoinChannel)

		servermenu.addSeparator()

		conDisconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		conDisconnect.triggered.connect(self.menuDisconnect)
		servermenu.addAction(conDisconnect)

		optionmenu = self.menubar.addMenu("Options")
		optionmenu.setStyle(self.gui.menu_style)

		self.IOtab = QAction(QIcon(MINUS_ICON),"Hide connection tab",self)
		self.IOtab.triggered.connect(self.menuIOtab)
		optionmenu.addAction(self.IOtab)

		optSend = QAction("Enable /send command",self,checkable=True)
		optSend.setChecked(self.enable_send)
		optSend.triggered.connect(self.menuToggleSend)
		optionmenu.addAction(optSend)

		self.menubar2 = QMenuBar()
		self.menubar2.setFont(fontnormal)
		self.tabs.widget(1).layout().setMenuBar(self.menubar2)

		servermenu = self.menubar2.addMenu("Server")
		servermenu.setStyle(self.gui.menu_style)

		conListChannels = QAction(QIcon(LIST_ICON),"List channels",self)
		conListChannels.triggered.connect(self.menuListChannels)
		servermenu.addAction(conListChannels)

		conChangeNick = QAction(QIcon(USER_ICON),"Change nickname",self)
		conChangeNick.triggered.connect(self.menuNick)
		servermenu.addAction(conChangeNick)

		conJoinChannel = QAction(QIcon(CHANNEL_WINDOW),"Join channel",self)
		conJoinChannel.triggered.connect(self.menuJoin)
		servermenu.addAction(conJoinChannel)

		servermenu.addSeparator()

		conDisconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		conDisconnect.triggered.connect(self.menuDisconnect)
		servermenu.addAction(conDisconnect)

		optionmenu = self.menubar2.addMenu("Options")
		optionmenu.setStyle(self.gui.menu_style)

		self.IOtab2 = QAction(QIcon(MINUS_ICON),"Hide connection tab",self)
		self.IOtab2.triggered.connect(self.menuIOtab)
		optionmenu.addAction(self.IOtab2)

		optSend = QAction("Enable /send command",self,checkable=True)
		optSend.setChecked(self.enable_send)
		optSend.triggered.connect(self.menuToggleSend)
		optionmenu.addAction(optSend)

		if self.gui.display_uptime_seconds:
			self.uptime = QLabel('<b>00:00:00</b>',self)
		else:
			self.uptime = QLabel('<b>00:00</b>',self)

		self.tabs.setCornerWidget(self.uptime,Qt.TopRightCorner)

		self.uptime.setStyleSheet('padding: 2px;')

		if not self.gui.display_uptime_console:
			self.menubar.setVisible(False)
			self.uptime.setVisible(False)

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
				# t = datetime.timestamp(datetime.now())
				# # pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')
				# pretty = datetime.fromtimestamp(t).strftime('%B %d, %Y at %H:%M:%S')
				# msg = render_system(self.gui, self.gui.styles[TIMESTAMP_STYLE_NAME],self.gui.styles[RESUME_STYLE_NAME],"Resumed on "+pretty )
				# self.writeText(msg)
				# self.add_to_log(GLYPH_RESUME,"Resumed on "+pretty )

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
		x = NicknameDialog.Dialog(self.client.nickname)
		nick = x.get_nick_information(self.client.nickname)

		if not nick: return

		self.client.setNick(nick)

	def closeMe(self):
		self.gui.closeConsole(self.client)

	def restoreMe(self):
		self.gui.restoreConsole(self.client)

	def menuListChannels(self):
		self.client.sendLine(f"LIST")

	def showMOTD(self):
		self.gui.view_motd(self.client)

	def open_link_in_browser(self,url):
		u = QUrl()
		u.setUrl(url)
		QDesktopServices.openUrl(u)

	def buildConnectionMenu(self,mdimenu,connection):

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

		if self.network_url:
			netname = textSeparator(self, f'''<b><a href="{self.network_url}">{self.network} Network</a></b>''')
			servmenu.addAction(netname)
		else:
			netname = textSeparator(self, f'''<b>{self.network} Network</b>''')
			servmenu.addAction(netname)

		if len(connection.modes)>0:
			snick = centerText(self,"<i>"+self.client.nickname+" +"+connection.modes+"</i>")
			servmenu.addAction(snick)
		else:
			snick = centerText(self,"<i>"+self.client.nickname+"</i>")
			servmenu.addAction(snick)

		consoleC = QAction(QIcon(CONSOLE_WINDOW),"Server console",self)
		consoleC.triggered.connect(self.restoreMe)
		servmenu.addAction(consoleC)

		motdMenu = QAction(QIcon(MOTD_ICON),"Message of the day",self)
		motdMenu.triggered.connect(self.showMOTD)
		servmenu.addAction(motdMenu)

		infomenu = servmenu.addMenu("Server Settings")
		infomenu.setIcon(QIcon(SERVER_SETTINGS_ICON))

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

		conListChannels = QAction(QIcon(LIST_ICON),"List channels",self)
		conListChannels.triggered.connect(self.menuListChannels)
		servmenu.addAction(conListChannels)

		conChangeNick = QAction(QIcon(USER_ICON),"Change nickname",self)
		conChangeNick.triggered.connect(self.menuNick)
		servmenu.addAction(conChangeNick)

		conJoinChannel = QAction(QIcon(CHANNEL_WINDOW),"Join channel",self)
		conJoinChannel.triggered.connect(self.menuJoin)
		servmenu.addAction(conJoinChannel)

		conDisconnect = QAction(QIcon(DISCONNECT_ICON),"Disconnect",self)
		conDisconnect.triggered.connect(self.menuDisconnect)
		servmenu.addAction(conDisconnect)

		#mdimenu.addSeparator()
