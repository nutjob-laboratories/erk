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
from ..objects import *
from ..files import *
from ..widgets import *
from ..strings import *
from ..dialogs import AddChannelDialog
from ..common import *

from .send_pm import Dialog as SendPM
from .pause import Dialog as PauseTime
from .comment import Dialog as Comment
from .print import Dialog as PrintMsg

class Dialog(QDialog):

	@staticmethod
	def get_connect_information(can_do_ssl,userfile,do_ssl=None,do_reconnect=None,block_scripts=False,scriptsdir='',parent=None):
		dialog = Dialog(can_do_ssl,userfile,do_ssl,do_reconnect,block_scripts,scriptsdir,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

	def return_info(self):

		try:
			port = int(self.port.text())
		except:
			ErrorDialog("Port must be a number")
			return None

		if len(self.password.text())>0:
			password = self.password.text()
		else:
			password = None

		user_history = self.user_info["history"]
		if self.SAVE_HISTORY:

			# make sure server isn't in the built-in list
			inlist = False
			# for s in self.built_in_server_list:
			# 	if s[0]==self.host.text():
			# 		if s[1]==self.port.text():
			# 			inlist = True

			# make sure server isn't in history
			inhistory = False
			for s in user_history:
				if s[0]==self.host.text():
					if s[1]==self.port.text():
						inhistory = True

			if inlist==False and inhistory==False:

				if self.DIALOG_CONNECT_VIA_SSL:
					ussl = "ssl"
				else:
					ussl = "normal"


				entry = [ self.host.text(),self.port.text(),UNKNOWN_NETWORK,ussl,self.password.text() ]
				user_history.append(entry)

		# Save disabled plugins
		disabled_plugins = self.user_info["disabled_plugins"]

		# Save user ignores
		ignored = self.user_info["ignore"]

		# Save user info
		user = {
			"nickname": self.nick.text(),
			"username": self.username.text(),
			"realname": self.realname.text(),
			"alternate": self.alternative.text(),
			"last_server": self.host.text(),
			"last_port": self.port.text(),
			"last_password": self.password.text(),
			"channels": self.autojoins,
			"ssl": self.DIALOG_CONNECT_VIA_SSL,
			"reconnect": self.RECONNECT,
			"autojoin": self.AUTOJOIN_CHANNELS,
			"history": user_history,
			"save_history": self.SAVE_HISTORY,
			"disabled_plugins": disabled_plugins,
			"ignore": ignored,
			"failreconnect": self.FAIL_RECONNECT,
			"auto_script": self.AUTOSCRIPT,
			"save_script": self.SAVE_SCRIPT,
		}
		save_user(user,self.userfile)

		if self.AUTOJOIN_CHANNELS:
			channels = self.autojoins
		else:
			channels = []

		if not self.block_scripts:

			# Autoscript
			if self.AUTOSCRIPT:
				script = self.scriptedit.toPlainText()

				if len(script)==0: script = None

			else:
				script = None

			if self.SAVE_SCRIPT:
				sscript = self.scriptedit.toPlainText()
				if len(sscript)==0:
					# Only save a blank script if the file already exists
					sfile = get_auto_script_name(self.host.text(),str(port),self.scriptsdir)
					if os.path.isfile(sfile):
						save_auto_script(self.host.text(),str(port),sscript,self.scriptsdir)
				else:
					save_auto_script(self.host.text(),str(port),sscript,self.scriptsdir)
		else:
			script = None

		retval = ConnectInfo(self.host.text(),port,password,self.DIALOG_CONNECT_VIA_SSL,self.nick.text(),self.alternative.text(),self.username.text(),self.realname.text(),self.RECONNECT,channels,self.FAIL_RECONNECT,True,script)

		return retval

	def clickScript(self,state):
		if state == Qt.Checked:
			self.AUTOSCRIPT = True
		else:
			self.AUTOSCRIPT = False

	def clickSaveScript(self,state):
		if state == Qt.Checked:
			self.SAVE_SCRIPT = True
		else:
			self.SAVE_SCRIPT = False

	def clickHistory(self,state):
		if state == Qt.Checked:
			self.SAVE_HISTORY = True
		else:
			self.SAVE_HISTORY = False

	def clickSSL(self,state):
		if state == Qt.Checked:
			self.DIALOG_CONNECT_VIA_SSL = True
		else:
			self.DIALOG_CONNECT_VIA_SSL = False

	def clickReconnect(self,state):
		if state == Qt.Checked:
			self.RECONNECT = True
			self.failrecon.setEnabled(True)
		else:
			self.RECONNECT = False
			self.failrecon.setEnabled(False)

	def clickChannels(self,state):
		if state == Qt.Checked:
			self.AUTOJOIN_CHANNELS = True
		else:
			self.AUTOJOIN_CHANNELS = False

	def clickFailrecon(self,state):
		if state == Qt.Checked:
			self.FAIL_RECONNECT = True
		else:
			self.FAIL_RECONNECT = False

	def setServer(self):

		if not len(self.user_info["last_server"])>0:
			if self.placeholder:
				self.servers.removeItem(0)
				self.StoredData.pop(0)
				self.placeholder = False

		self.StoredServer = self.servers.currentIndex()

		if self.StoredData[self.StoredServer][2]=="Last server":
			self.netType.setText("<big><b>"+self.user_info["last_server"]+"</b></big>")
		else:
			self.netType.setText("<big><b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b></big>")
		if "ssl" in self.StoredData[self.StoredServer][3]:
			self.connType.setText(f"<small><i>Connect via</i> <b>SSL/TLS</b> <i>to port</i> <b>{self.StoredData[self.StoredServer][1]}</b></small>")
		else:
			self.connType.setText(f"<small><i>Connect via</i> <b>TCP/IP</b> <i>to port</i> <b>{self.StoredData[self.StoredServer][1]}</b></small>")

		neturl = get_network_url(self.StoredData[self.StoredServer][2])
		if neturl:
			self.networkURL.setText(f"<small><a href=\"{neturl}\">{neturl}</a></small>")
		else:
			self.networkURL.setText(f"<small>&nbsp;</small>")

		visited = False
		for ent in self.prevVisit:
			if ent[0]==self.StoredData[self.StoredServer][0]:
				if ent[1]==self.StoredData[self.StoredServer][1]:
					if ent[2]==self.StoredData[self.StoredServer][2]:
						if ent[3]==self.StoredData[self.StoredServer][3]:
							visited = True

		if visited:
			self.visitbeforeType.setText("<small>Connected to previously</small>")
		else:
			# self.visitbeforeType.setText("<small>&nbsp;</small>")
			self.visitbeforeType.setText("<small>Never connected to before</small>")

		if self.StoredData[self.StoredServer][2]=="Last server":
			self.visitbeforeType.setText("<small>Last server connection</small>")


		# Fill in the server info
		h = self.StoredData[self.StoredServer]
		if "ssl" in h[3]:
			use_ssl = True
		else:
			use_ssl = False
		host = h[0]
		port = int(h[1])

		self.host.setText(host)
		self.port.setText(h[1])

		if len(h)==5:
			if h[4]=='':
				password = None
				self.password.setText('')
			else:
				password = h[4]
				self.password.setText(h[4])
		else:
			password = None
			self.password.setText('')

		if use_ssl:
			self.ssl.setCheckState(Qt.Checked)
		else:
			self.ssl.setCheckState(Qt.Unchecked)

	def serverEntered(self):
		serv = self.host.text()
		port = self.port.text()

		code = load_auto_script(serv,port,self.scriptsdir)
		if code!=None:
			self.scriptedit.setText(code)
		else:
			self.scriptedit.clear()

		self.scripttablabel.setText(f"<small><center>Execute these commands on connection to {serv}:{str(port)}</center></small>")
		self.scriptedit.moveCursor(QTextCursor.End)


	def __init__(self,can_do_ssl,userfile=USER_FILE,do_ssl=None,do_reconnect=None,block_scripts=False,scriptsdir='',parent=None):
		super(Dialog,self).__init__(parent)

		self.can_do_ssl = can_do_ssl
		self.parent = parent
		self.userfile = userfile

		self.block_scripts = block_scripts
		self.scriptsdir = scriptsdir

		self.autojoins = []

		self.StoredServer = 0
		self.StoredData = []

		self.prevVisit = []

		self.placeholder = False

		self.DIALOG_CONNECT_VIA_SSL = False
		self.RECONNECT = False
		self.AUTOJOIN_CHANNELS = False
		self.SAVE_HISTORY = False
		self.FAIL_RECONNECT = True
		self.AUTOSCRIPT = False
		self.SAVE_SCRIPT = False

		self.setWindowTitle(f"Connect to IRC")
		self.setWindowIcon(QIcon(CONNECT_MENU_ICON))

		self.user_info = get_user(self.userfile)

		self.tabs = QTabWidget()
		self.network_tab = QWidget()
		self.server_tab = QWidget()
		#self.user_tab = QWidget()
		self.channels_tab = QWidget()

		# self.script_tab = QWidget()

		self.tabs.addTab(self.server_tab,"Connect")
		self.tabs.addTab(self.network_tab,"Servers")
		#self.tabs.addTab(self.user_tab,"User")
		if not self.block_scripts:
			self.tabs.addTab(self.channels_tab,"Script")

		#self.tabs.addTab(self.script_tab,"Script")

		self.tabs.setStyleSheet("""
			QTabWidget::tab-bar { alignment: center; font: bold; }
			""")


		f = self.tabs.font()
		f.setBold(True)
		self.tabs.setFont(f)

		# NETWORK TAB BEGIN

		# Server information
		self.entryType = QLabel("")
		self.connType = QLabel("")
		self.netType = QLabel("")
		self.description = QLabel("<big><b>Select an IRC server</b></big>")
		self.description.setAlignment(Qt.AlignCenter)

		self.visitbeforeType = QLabel("<small>&nbsp;</small>")
		self.visitbeforeType.setAlignment(Qt.AlignCenter)

		self.networkURL = QLabel("<small>&nbsp;</small>")
		self.networkURL.setAlignment(Qt.AlignCenter)
		self.networkURL.setOpenExternalLinks(True)

		f = self.networkURL.font()
		f.setBold(True)
		self.networkURL.setFont(f)

		f = self.connType.font()
		f.setBold(False)
		self.connType.setFont(f)
		self.entryType.setFont(f)

		etLayout = QHBoxLayout()
		etLayout.addStretch()
		etLayout.addWidget(self.entryType)
		etLayout.addStretch()

		ntLayout = QHBoxLayout()
		ntLayout.addStretch()
		ntLayout.addWidget(self.netType)
		ntLayout.addStretch()

		ctLayout = QHBoxLayout()
		ctLayout.addStretch()
		ctLayout.addWidget(self.connType)
		ctLayout.addStretch()

		self.servers = QComboBox(self)
		self.servers.activated.connect(self.setServer)

		self.servers.setStyleSheet("QComboBox { font: bold; }")

		if self.user_info["ssl"]:
			dussl = "ssl"
		else:
			dussl = "normal"

		if len(self.user_info["last_server"])>0:
			self.StoredData.append( [ self.user_info["last_server"],self.user_info["last_port"],"Last server",dussl,self.user_info["last_password"] ]    )
			self.servers.addItem("Last server connection")
		else:
			self.StoredData.append( ['',"6667",'','normal','' ]    )
			self.servers.addItem("Servers")
			self.placeholder = True

		self.built_in_server_list = get_network_list()

		organized_list = []

		if len(self.user_info["history"])>0:
			# servers are in history
			for s in self.user_info["history"]:
				#self.built_in_server_list.append(s)

				builtin = False
				for entry in self.built_in_server_list:
					if entry[0]==s[0]:
						if entry[1]==s[1]:
							builtin = True

				if not builtin:
					self.built_in_server_list.insert(0,s)

		counter = -1
		for entry in self.built_in_server_list:
			counter = counter + 1
			if len(entry) < 4: continue

			if "ssl" in entry[3]:
				if not self.can_do_ssl: continue

			visited = False
			if len(self.user_info["history"])>0:
				for s in self.user_info["history"]:
					if s[0]==entry[0]:
						if s[1]==entry[1]:
							visited = True

			if visited:
				organized_list.append([True,entry])
			else:
				organized_list.append([False,entry])

		vserver = []
		nserver = []
		for x in organized_list:
			if x[0]:
				vserver.append(x)
			else:
				nserver.append(x)
		finallist = vserver + nserver
		
		for s in finallist:
			if s[0]:
				self.prevVisit.append(s[1])
				self.servers.addItem(QIcon(VISITED_ICON),s[1][2]+" - "+s[1][0])
			else:
				self.servers.addItem(QIcon(UNVISITED_ICON),s[1][2]+" - "+s[1][0])

			self.StoredData.append(s[1])

		self.StoredServer = self.servers.currentIndex()


		if len(self.user_info["last_server"])>0:
			if self.StoredData[self.StoredServer][2]=="Last server":
				self.netType.setText("<big><b>"+self.user_info["last_server"]+"</b></big>")
			else:
				self.netType.setText("<big><b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b></big>")

			if "ssl" in self.StoredData[self.StoredServer][3]:
				self.connType.setText(f"<small><i>Connect via</i> <b>SSL/TLS</b> <i>to port</i> <b>{self.StoredData[self.StoredServer][1]}</b></small>")
			else:
				self.connType.setText(f"<small><i>Connect via</i> <b>TCP/IP</b> <i>to por</i>t <b>{self.StoredData[self.StoredServer][1]}</b></small>")

			self.visitbeforeType.setText("<small>Last server connection</small>")

			neturl = get_network_url(self.StoredData[self.StoredServer][2])
			if neturl:
				self.networkURL.setText(f"<small><a href=\"{neturl}\">{neturl}</a></small>")
			else:
				self.networkURL.setText(f"<small>&nbsp;</small>")
		else:
			self.netType.setText("")


		# irc_image = QLabel()
		# pixmap = QPixmap(IRC_IMAGE)
		# irc_image.setPixmap(pixmap)
		# irc_image.setAlignment(Qt.AlignCenter)


		fstoreLayout = QVBoxLayout()
		fstoreLayout.addStretch()

		#fstoreLayout.addWidget(QLabel(' '))

		# fstoreLayout.addWidget(irc_image)


		fstoreLayout.addWidget(self.description)
		#fstoreLayout.addStretch()

		self.descMoreInfo = QLabel("""
			<small>
				Below is a list of IRC servers to connect to, as well as servers you've previously connected to. Select a
				server to see what IRC network that server may belong to and how to connect to it. Selecting a server will
				automatically load the appropriate settings into the "Connect" tab.
			</small>
		""")
		self.descMoreInfo.setAlignment(Qt.AlignJustify)
		self.descMoreInfo.setWordWrap(True)

		fstoreLayout.addWidget(self.descMoreInfo)

		fstoreLayout.addStretch()

		# MOVING THIS TO MAIN TAB
		fstoreLayout.addWidget(self.servers)

		#fstoreLayout.addStretch()

		#fstoreLayout.addWidget(QHLine())
		#fstoreLayout.addWidget(QLabel(' '))

		fstoreLayout.addStretch()
		fstoreLayout.addLayout(ntLayout)
		fstoreLayout.addLayout(ctLayout)
		fstoreLayout.addWidget(self.visitbeforeType)
		fstoreLayout.addWidget(self.networkURL)
		fstoreLayout.addLayout(etLayout)
		# fstoreLayout.addWidget(self.visitbeforeType)
		fstoreLayout.addStretch()

		self.network_tab.setLayout(fstoreLayout)


		# NETWORK TAB END

		# SERVER INFO BEGIN

		serverLayout = QFormLayout()
		self.host = QLineEdit(self.user_info["last_server"])
		self.port = QLineEdit(self.user_info["last_port"])
		self.password = QLineEdit(self.user_info["last_password"])
		self.password.setEchoMode(QLineEdit.Password)

		self.host.textChanged.connect(self.serverEntered)
		self.port.textChanged.connect(self.serverEntered)

		hostl = QLabel("Host")
		f = hostl.font()
		f.setBold(True)
		hostl.setFont(f)
		serverLayout.addRow(hostl, self.host)

		portl = QLabel("Port")
		portl.setFont(f)
		serverLayout.addRow(portl, self.port)

		passl = QLabel("Password")
		passl.setFont(f)
		serverLayout.addRow(passl, self.password)

		self.ssl = QCheckBox("Connect via SSL/TLS",self)
		self.ssl.stateChanged.connect(self.clickSSL)
		self.ssl.setFont(f)

		self.reconnect = QCheckBox("Reconnect on disconnection",self)
		self.reconnect.stateChanged.connect(self.clickReconnect)

		# SMALLER_CHECKBOX_SIZE = '15'

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		#SMALLER_CHECKBOX_SIZE = fheight-8

		SMALLER_CHECKBOX_SIZE = fheight * 0.50


		self.reconnect.setStyleSheet(f'QCheckBox {{ font-size: {SMALLER_CHECKBOX_SIZE}px; }} QCheckBox::indicator {{ width:  {SMALLER_CHECKBOX_SIZE}px; height: {SMALLER_CHECKBOX_SIZE}px;}}')

		self.failrecon = QCheckBox("Reconnect on failure",self)
		self.failrecon.stateChanged.connect(self.clickFailrecon)

		self.failrecon.setStyleSheet(f'QCheckBox {{ font-size: {SMALLER_CHECKBOX_SIZE}px; }} QCheckBox::indicator {{ width:  {SMALLER_CHECKBOX_SIZE}px; height: {SMALLER_CHECKBOX_SIZE}px;}}')

		if self.user_info["failreconnect"]:
			self.failrecon.toggle()

		if self.user_info["ssl"]:
			self.ssl.toggle()

		# Connect commands
		if do_ssl!=None:
			if do_ssl:
				if not self.user_info["ssl"]:
					self.ssl.toggle()

		if self.user_info["reconnect"]:
			self.reconnect.toggle()
		else:
			self.failrecon.setEnabled(False)

		# Connect command
		if do_reconnect!=None:
			if do_reconnect:
				if not self.user_info["reconnect"]:
					self.reconnect.toggle()

		if not self.can_do_ssl:
			self.DIALOG_CONNECT_VIA_SSL = False
			self.ssl.setEnabled(False)

		sslLayout = QHBoxLayout()
		#sslLayout = QVBoxLayout()
		sslLayout.addStretch()
		sslLayout.addWidget(self.ssl)
		sslLayout.addStretch()

		self.history = QCheckBox("Save server history",self)
		self.history.stateChanged.connect(self.clickHistory)

		self.history.setStyleSheet(f'QCheckBox {{ font-size: {SMALLER_CHECKBOX_SIZE}px; }} QCheckBox::indicator {{ width:  {SMALLER_CHECKBOX_SIZE}px; height: {SMALLER_CHECKBOX_SIZE}px;}}')

		if self.user_info["save_history"]:
			self.history.toggle()
		

		centServ = QHBoxLayout()
		centServ.addStretch()
		centServ.addLayout(serverLayout)
		centServ.addStretch()

		serverTabLayout = QVBoxLayout()
		serverTabLayout.addStretch()
		# serverTabLayout.addLayout(serverLayout)

		serverTabLayout.addLayout(centServ)
		serverTabLayout.addLayout(sslLayout)
		#serverTabLayout.addStretch()
		serverTabLayout.setAlignment(Qt.AlignCenter)

		serverConnectOptions = QVBoxLayout()
		serverConnectOptions.addWidget(self.reconnect)
		serverConnectOptions.addWidget(self.failrecon)
		serverConnectOptions.addWidget(self.history)
		serverConnectOptions.addStretch()
		# serverConnectOptions.setAlignment(Qt.AlignRight)

		# hisLayout = QVBoxLayout()
		# hisLayout.addWidget(self.history)
		# hisLayout.addStretch()

		# allSetLay = QHBoxLayout()
		# allSetLay.addLayout(serverConnectOptions)
		# allSetLay.addLayout(hisLayout)

		# column2 = QHBoxLayout()
		# column2.addLayout(serverConnectOptions)
		# column2.addWidget(self.history)

		finConnectOptions = QHBoxLayout()
		finConnectOptions.addStretch()
		finConnectOptions.addLayout(serverConnectOptions)
		#finConnectOptions.setAlignment(Qt.AlignLeft)
		finConnectOptions.addStretch()

		# serverTabLayout.addLayout(serverConnectOptions)

		# ssetBox = QGroupBox()
		# ssetBox.setAlignment(Qt.AlignHCenter)
		# ssetBox.setLayout(finConnectOptions)

		#serverTabLayout.addWidget(QLabel(' '))

		#serverTabLayout.addLayout(finConnectOptions)

		# serverTabLayout.addWidget(QLabel(" "))
		# serverTabLayout.addWidget(QLabel(" "))

		# serverTabLayout.addStretch()

		# serverTabLayout.addWidget(ssetBox)
		serverTabLayout.addLayout(finConnectOptions)

		#serverTabLayout.addStretch()




		# serverTabCenter = QHBoxLayout()
		# serverTabCenter.addStretch()
		# serverTabCenter.addLayout(serverTabLayout)
		# serverTabCenter.addStretch()

		# self.server_tab.setLayout(serverTabCenter)

		# SERVER INFO END

		# USER INFO BEGIN

		userLayout = QFormLayout()

		self.nick = QLineEdit(self.user_info["nickname"])
		self.alternative = QLineEdit(self.user_info["alternate"])
		self.username = QLineEdit(self.user_info["username"])
		self.realname = QLineEdit(self.user_info["realname"])

		nickl = QLabel("Nickname")
		f = nickl.font()
		f.setBold(True)
		nickl.setFont(f)

		altl = QLabel("Alternate")
		altl.setFont(f)

		usrl = QLabel("Username")
		usrl.setFont(f)

		reall = QLabel("Real name")
		reall.setFont(f)

		userLayout.addRow(nickl, self.nick)
		userLayout.addRow(altl, self.alternative)
		userLayout.addRow(usrl, self.username)
		userLayout.addRow(reall, self.realname)

		banner = QLabel()
		pixmap = QPixmap(BANNER_IMAGE)
		banner.setPixmap(pixmap)
		banner.setAlignment(Qt.AlignCenter)

		userTabLayout = QVBoxLayout()
		userTabLayout.addWidget(banner)
		userTabLayout.addStretch()
		userTabLayout.addLayout(userLayout)
		userTabLayout.addStretch()

		userTabCenter = QHBoxLayout()
		userTabCenter.addStretch()
		userTabCenter.addLayout(userTabLayout)
		userTabCenter.addStretch()

		# self.user_tab.setLayout(userTabCenter)

		# MOVE THIS TO THE SERVER TAB

		# QFrame *line;
		# line = new QFrame(Form);
		# line->setFrameShape(QFrame::HLine);
		# line->setFrameShadow(QFrame::Sunken);

		userBox = QGroupBox()
		userBox.setAlignment(Qt.AlignHCenter)
		userBox.setLayout(userTabCenter)

		servBox = QGroupBox()
		servBox.setAlignment(Qt.AlignHCenter)
		servBox.setLayout(serverTabLayout)



		finalServerTab = QVBoxLayout()
		finalServerTab.addStretch()

		# finalServerTab.addLayout(userTabCenter)
		# finalServerTab.addLayout(serverTabLayout)

		finalServerTab.addWidget(userBox)

		finalServerTab.addWidget(servBox)


		finalServerTab.addStretch()

		self.server_tab.setLayout(finalServerTab)

		# CHANNELS TAB

		self.do_autojoin = QCheckBox("Auto-join channels",self)
		self.do_autojoin.stateChanged.connect(self.clickChannels)

		if self.user_info["autojoin"]:
			self.do_autojoin.toggle()

		# NEW EDITOR START

		

		# NEW EDITOR END

		self.autoChannels = QListWidget(self)
		# self.autoChannels.setMaximumHeight(100)

		self.autoChannels.setMaximumHeight(125)

		self.addChannelButton = QPushButton("Add channel")
		self.addChannelButton.clicked.connect(self.buttonAdd)

		self.removeChannelButton = QPushButton("Remove channel")
		self.removeChannelButton.clicked.connect(self.buttonRemove)

		buttonLayout = QHBoxLayout()
		#buttonLayout.addStretch()
		buttonLayout.addWidget(self.addChannelButton)
		buttonLayout.addWidget(self.removeChannelButton)
		
		self.chantabTitle = QLabel("<big><center><b>Auto-Join Channels</b></center></big>")
		self.chantabLabel = QLabel("<small><center>Join these channels when connecting to any server</center></small>")

		autoJoinLayout = QVBoxLayout()
		autoJoinLayout.addWidget(self.chantabTitle)
		autoJoinLayout.addWidget(self.chantabLabel)
		autoJoinLayout.addWidget(self.autoChannels)
		autoJoinLayout.addLayout(buttonLayout)

		autoJoinCheckbox = QHBoxLayout()
		autoJoinCheckbox.addWidget(self.do_autojoin)
		autoJoinCheckbox.setAlignment(Qt.AlignLeft)

		#autoJoinLayout.addStretch()

		autoJoinLayout.addLayout(autoJoinCheckbox)

		#autoJoinLayout.addStretch()

		# self.channels_tab.setLayout(autoJoinLayout)

		
		for c in self.user_info["channels"]:
			channel = c[0]
			key = c[1]
			if key == "":
				item = QListWidgetItem(f"{channel}")
				item.setIcon(QIcon(CHANNEL_ICON))
				self.autoChannels.addItem(item)

			else:
				item = QListWidgetItem(f"{channel}")
				item.setIcon(QIcon(KEY_ICON))
				self.autoChannels.addItem(item)

			e = [channel,key]
			self.autojoins.append(e)


		# MOVED TO SERVER TAB
		fstoreLayout.addLayout(autoJoinLayout)


		self.scriptedit = QTextEdit(self)

		if len(self.user_info["last_server"])==0:
			self.scripttablabel = QLabel("<small><center>Execute these commands on connection to server</center></small>")
		else:
			serv = self.user_info["last_server"]
			port = str(self.user_info["last_port"])
			self.scripttablabel = QLabel(f"<small><center>Execute these commands on connection to {serv}:{port}</center></small>")

		# Load in script if there's one for the last entered server
		if len(self.user_info["last_server"])>0 and len(self.user_info["last_port"])>0:
			code = load_auto_script(self.user_info["last_server"],self.user_info["last_port"],self.scriptsdir)
			if code!=None:
				self.scriptedit.setText(code)

		self.scriptedit.moveCursor(QTextCursor.End)

		self.scripttabinfo = QLabel("<small><center><i>Any command usable in the client can be used. Insert comments between \"</i><b>/*</b><i>\" and \"</i><b>*/</b><i>\". To pause the script, call the \"</i><b>/wait</b><i>\" command with the number of seconds to pause as the only argument.</i></center></small>")
		self.scripttabinfo.setWordWrap(True)
		self.scripttabinfo.setAlignment(Qt.AlignJustify)

		autoScriptLayout = QVBoxLayout()
		#autoScriptLayout.addWidget(QLabel(' '))
		autoScriptLayout.addWidget(self.scripttablabel)
		autoScriptLayout.addWidget(self.scripttabinfo)
		autoScriptLayout.addWidget(self.scriptedit)

		self.saveScriptButton = QPushButton("Save")
		self.saveScriptButton.clicked.connect(self.saveScript)

		self.deleteScriptButton = QPushButton("Delete")
		self.deleteScriptButton.clicked.connect(self.deleteScript)

		self.clearScriptButton = QPushButton("Clear")
		self.clearScriptButton.clicked.connect(self.clearScript)

		self.checkScript = QCheckBox("Execute on connect",self)
		self.checkScript.stateChanged.connect(self.clickScript)

		if self.user_info["auto_script"]:
			self.checkScript.toggle()

		self.autoSaveScript = QCheckBox("Save on connect",self)
		self.autoSaveScript.stateChanged.connect(self.clickSaveScript)

		if self.user_info["save_script"]:
			self.autoSaveScript.toggle()

		self.reloadScriptButton = QPushButton("Reload")
		self.reloadScriptButton.clicked.connect(self.reloadScript)

		scriptControlsLayout = QHBoxLayout()
		scriptControlsLayout.addWidget(self.saveScriptButton)
		scriptControlsLayout.addWidget(self.reloadScriptButton)
		scriptControlsLayout.addWidget(self.clearScriptButton)
		scriptControlsLayout.addWidget(self.deleteScriptButton)
		#scriptControlsLayout.addWidget(self.checkScript)

		self.scriptJoinButton = QPushButton("Join a Channel")
		self.scriptJoinButton.clicked.connect(self.scriptJoin)

		self.scriptSendPM = QPushButton("Send a Message")
		self.scriptSendPM.clicked.connect(self.scriptPM)

		self.scriptInsertPause = QPushButton("Insert Pause")
		self.scriptInsertPause.clicked.connect(self.scriptTime)

		self.scriptInsertComment = QPushButton("Insert Comment")
		self.scriptInsertComment.clicked.connect(self.scriptComment)

		self.scriptInsertPrint = QPushButton("Insert Print")
		self.scriptInsertPrint.clicked.connect(self.scriptPrint)

		scriptAddLayout = QHBoxLayout()
		scriptAddLayout.addWidget(self.scriptJoinButton)
		scriptAddLayout.addWidget(self.scriptSendPM)

		scriptAddLayout2 = QHBoxLayout()
		scriptAddLayout2.addWidget(self.scriptInsertPause)
		scriptAddLayout2.addWidget(self.scriptInsertComment)
		scriptAddLayout2.addWidget(self.scriptInsertPrint)

		scriptInsertStuff = QVBoxLayout()
		scriptInsertStuff.addLayout(scriptAddLayout)
		scriptInsertStuff.addLayout(scriptAddLayout2)

		autoScriptLayout.addLayout(scriptInsertStuff)
		autoScriptLayout.addLayout(scriptControlsLayout)

		scriptToggles = QHBoxLayout()
		scriptToggles.addWidget(self.checkScript)
		scriptToggles.addWidget(self.autoSaveScript)

		autoScriptLayout.addLayout(scriptToggles)

		##

		#autoJoinLayout.addLayout(autoScriptLayout)

		# self.channels_tab.setLayout(autoJoinLayout)
		self.channels_tab.setLayout(autoScriptLayout)

		#self.script_tab.setLayout(autoScriptLayout)

		# CHANNELS TAB

		# SCRIPT TAB BEGIN

		

		# SCRIPT TAB END

		

		# USER INFO END

		vLayout = QVBoxLayout()
		vLayout.addWidget(self.tabs)

		#c1 = QVBoxLayout()
		#c1.addWidget(self.reconnect)
		#c1.addWidget(self.failrecon)

		#c2 = QVBoxLayout()
		# c2.addWidget(self.do_autojoin)
		#c2.addWidget(self.history)

		# c2 = QHBoxLayout()
		# c2.addLayout(finConnectOptions)
		# serverConnectOptions.addWidget(self.history)

		# serverConnectOptions.addWidget(self.history)

		

		#hOpts = QHBoxLayout()
		#hOpts.addLayout(c1)
		#hOpts.addLayout(c2)

		#vLayout.addLayout(hOpts)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Connect")

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(vLayout)
		finalLayout.addWidget(buttons)


		# print(finalLayout.sizeHint().width())
		# print(finalLayout.sizeHint().height())

		# self.resize(
		# 	finalLayout.sizeHint().width() + 1000,
		# 	finalLayout.sizeHint().height()
		# 	)

		# print(config.LOAD_AUTO_CONNECT_SCRIPTS)


		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def reloadScript(self):
		serv = self.host.text()
		port = self.port.text()

		code = load_auto_script(serv,port,self.scriptsdir)
		if code!=None:
			self.scriptedit.setText(code)
		else:
			self.scriptedit.clear()

	def clearScript(self):
		self.scriptedit.clear()

	def scriptTime(self):
		x = PauseTime()
		e = x.get_time_information()

		if not e: return

		self.scriptedit.insertPlainText("/wait "+str(e)+"\n")

	def scriptPM(self):
		x = SendPM()
		e = x.get_message_information()

		if not e: return

		target = e[0]
		msg = e[1]
		
		if len(target)>0 and len(msg)>0:
			self.scriptedit.insertPlainText("/msg "+target+" "+msg+"\n")

	def scriptComment(self):
		x = Comment()
		e = x.get_message_information()

		if not e: return

		if len(e)>0:
			self.scriptedit.insertPlainText("/* "+e+" */\n")

	def scriptPrint(self):
		x = PrintMsg()
		e = x.get_message_information()

		if not e: return

		if len(e)>0:
			self.scriptedit.insertPlainText("/print "+e+"\n")

	def scriptJoin(self):
		x = AddChannelDialog()
		e = x.get_channel_information()

		if not e: return

		channel = e[0]
		key = e[1]

		if len(key)==0:
			self.scriptedit.insertPlainText("/join "+channel+"\n")
		else:
			self.scriptedit.insertPlainText("/join "+channel+" "+key+"\n")

	def deleteScript(self):
		serv = self.host.text()
		port = self.port.text()
		self.scriptedit.setText('')

		sfile = get_auto_script_name(serv,port,self.scriptsdir)
		if os.path.isfile(sfile):
			os.remove(sfile)

	def saveScript(self):

		serv = self.host.text()
		port = self.port.text()
		script = self.scriptedit.toPlainText()

		if len(serv)>0 and len(port)>0:
			save_auto_script(serv,port,script,self.scriptsdir)

	def buttonAdd(self):
		#x = AddChannelDialog.Dialog()
		x = AddChannelDialog()
		e = x.get_channel_information()

		if not e: return

		channel = e[0]
		key = e[1]

		if len(channel)==0:
			self.error_dialog = QErrorMessage()
			self.error_dialog.showMessage("No channel entered!")
			self.close()
			return

		#print(channel,key)
		if key == "":
			item = QListWidgetItem(f"{channel}")
			item.setIcon(QIcon(CHANNEL_ICON))
			self.autoChannels.addItem(item)

		else:
			item = QListWidgetItem(f"{channel}")
			item.setIcon(QIcon(KEY_ICON))
			self.autoChannels.addItem(item)

		e = [channel,key]
		self.autojoins.append(e)

	def buttonRemove(self):
		#self.removeSel()
		try:
			channel = self.autoChannels.currentItem().text()
			i = self.autoChannels.currentRow()
			self.autoChannels.takeItem(i)

			clean = []
			for c in self.autojoins:
				if c[0]==channel: continue
				clean.append(c)
			self.autojoins = clean
		except:
			pass
