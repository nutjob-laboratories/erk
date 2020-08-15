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

from ..resources import *
from ..objects import *
from ..files import *
from ..widgets import *
from ..strings import *
# import erk.config

from ..dialogs import AddChannelDialog


class Dialog(QDialog):

	@staticmethod
	def get_connect_information(can_do_ssl,parent=None):
		dialog = Dialog(can_do_ssl,parent)
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


				entry = [ self.host.text(),self.port.text(),UNKNOWN_NETWORK,ussl,self.password.text()    ]
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
		}
		save_user(user,self.userfile)

		if self.AUTOJOIN_CHANNELS:
			channels = self.autojoins
		else:
			channels = []

		retval = ConnectInfo(self.host.text(),port,password,self.DIALOG_CONNECT_VIA_SSL,self.nick.text(),self.alternative.text(),self.username.text(),self.realname.text(),self.RECONNECT,channels)

		return retval

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
		else:
			self.RECONNECT = False

	def clickChannels(self,state):
		if state == Qt.Checked:
			self.AUTOJOIN_CHANNELS = True
		else:
			self.AUTOJOIN_CHANNELS = False

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


	def __init__(self,can_do_ssl,userfile=USER_FILE,parent=None):
		super(Dialog,self).__init__(parent)

		self.can_do_ssl = can_do_ssl
		self.parent = parent
		self.userfile = userfile

		self.autojoins = []

		self.StoredServer = 0
		self.StoredData = []

		self.placeholder = False

		self.DIALOG_CONNECT_VIA_SSL = False
		self.RECONNECT = False
		self.AUTOJOIN_CHANNELS = False
		self.SAVE_HISTORY = False

		self.setWindowTitle(f"Connect")
		self.setWindowIcon(QIcon(CONNECT_MENU_ICON))

		self.user_info = get_user(self.userfile)

		self.tabs = QTabWidget()
		self.network_tab = QWidget()
		self.server_tab = QWidget()
		self.user_tab = QWidget()
		self.channels_tab = QWidget()

		self.tabs.addTab(self.server_tab,"Server")
		self.tabs.addTab(self.network_tab,"Networks")
		self.tabs.addTab(self.user_tab,"User")
		self.tabs.addTab(self.channels_tab,"Channels")

		f = self.tabs.font()
		f.setBold(True)
		self.tabs.setFont(f)

		# NETWORK TAB BEGIN

		# Server information
		self.entryType = QLabel("")
		self.connType = QLabel("")
		self.netType = QLabel("")
		self.description = QLabel("<big>Select an IRC server</big>")
		self.description.setAlignment(Qt.AlignCenter)

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

		# 	self.StoredData.append(entry)
		# 	if visited:
		# 		self.servers.addItem(QIcon(VISITED_ICON),entry[2] + " - " + entry[0])
		# 	else:
		# 		self.servers.addItem(QIcon(USERLIST_NORMAL_ICON),entry[2] + " - " + entry[0])

		# self.StoredServer = self.servers.currentIndex()

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
				self.servers.addItem(QIcon(VISITED_ICON),s[1][2]+" - "+s[1][0])
			else:
				self.servers.addItem(QIcon(UNVISITED_ICON),s[1][2]+" - "+s[1][0])

			self.StoredData.append(s[1])

		self.StoredServer = self.servers.currentIndex()


		if len(self.user_info["last_server"])>0:
			if self.StoredData[self.StoredServer][2]=="Last server":
				# self.netType.setText("<big><b>Last server</b></big>")
				self.netType.setText("<big><b>"+self.user_info["last_server"]+"</b></big>")
			else:
				self.netType.setText("<big><b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b></big>")

			if "ssl" in self.StoredData[self.StoredServer][3]:
				self.connType.setText(f"<small><i>Connect via</i> <b>SSL/TLS</b> <i>to port</i> <b>{self.StoredData[self.StoredServer][1]}</b></small>")
			else:
				self.connType.setText(f"<small><i>Connect via</i> <b>TCP/IP</b> <i>to por</i>t <b>{self.StoredData[self.StoredServer][1]}</b></small>")
		else:
			# self.netType.setText("<big><b>Choose an IRC server to connect to</b></big>")
			self.netType.setText("")




		fstoreLayout = QVBoxLayout()
		fstoreLayout.addStretch()
		fstoreLayout.addWidget(QLabel(' '))
		fstoreLayout.addWidget(self.description)
		#fstoreLayout.addStretch()
		fstoreLayout.addWidget(self.servers)
		fstoreLayout.addStretch()
		#fstoreLayout.addWidget(QHLine())
		fstoreLayout.addWidget(QLabel(' '))
		fstoreLayout.addStretch()
		fstoreLayout.addLayout(ntLayout)
		fstoreLayout.addLayout(ctLayout)
		fstoreLayout.addLayout(etLayout)
		fstoreLayout.addStretch()

		self.network_tab.setLayout(fstoreLayout)


		# NETWORK TAB END

		# SERVER INFO BEGIN

		serverLayout = QFormLayout()
		self.host = QLineEdit(self.user_info["last_server"])
		self.port = QLineEdit(self.user_info["last_port"])
		self.password = QLineEdit(self.user_info["last_password"])
		self.password.setEchoMode(QLineEdit.Password)

		serverLayout.addRow(QLabel("Host"), self.host)
		serverLayout.addRow(QLabel("Port"), self.port)
		serverLayout.addRow(QLabel("Password"), self.password)

		self.ssl = QCheckBox("Connect via SSL/TLS",self)
		self.ssl.stateChanged.connect(self.clickSSL)

		self.reconnect = QCheckBox("Reconnect on disconnection",self)
		self.reconnect.stateChanged.connect(self.clickReconnect)

		if self.user_info["ssl"]:
			self.ssl.toggle()

		if self.user_info["reconnect"]:
			self.reconnect.toggle()

		if not self.can_do_ssl:
			self.DIALOG_CONNECT_VIA_SSL = False
			self.ssl.setEnabled(False)

		sslLayout = QHBoxLayout()
		sslLayout.addStretch()
		sslLayout.addWidget(self.ssl)

		serverTabLayout = QVBoxLayout()
		serverTabLayout.addStretch()
		serverTabLayout.addLayout(serverLayout)
		serverTabLayout.addLayout(sslLayout)
		serverTabLayout.addStretch()

		serverTabCenter = QHBoxLayout()
		serverTabCenter.addStretch()
		serverTabCenter.addLayout(serverTabLayout)
		serverTabCenter.addStretch()

		self.server_tab.setLayout(serverTabCenter)

		# SERVER INFO END

		# USER INFO BEGIN

		userLayout = QFormLayout()

		self.nick = QLineEdit(self.user_info["nickname"])
		self.alternative = QLineEdit(self.user_info["alternate"])
		self.username = QLineEdit(self.user_info["username"])
		self.realname = QLineEdit(self.user_info["realname"])

		userLayout.addRow(QLabel("Nickname"), self.nick)
		userLayout.addRow(QLabel("Alternate"), self.alternative)
		userLayout.addRow(QLabel("Username"), self.username)
		userLayout.addRow(QLabel("Real name"), self.realname)

		userTabLayout = QVBoxLayout()
		userTabLayout.addStretch()
		userTabLayout.addLayout(userLayout)
		userTabLayout.addStretch()

		userTabCenter = QHBoxLayout()
		userTabCenter.addStretch()
		userTabCenter.addLayout(userTabLayout)
		userTabCenter.addStretch()

		self.user_tab.setLayout(userTabCenter)

		# CHANNELS TAB

		self.do_autojoin = QCheckBox("Automatically join channels",self)
		self.do_autojoin.stateChanged.connect(self.clickChannels)

		if self.user_info["autojoin"]:
			self.do_autojoin.toggle()

		self.autoChannels = QListWidget(self)
		self.autoChannels.setMaximumHeight(100)

		self.addChannelButton = QPushButton("+")
		self.addChannelButton.clicked.connect(self.buttonAdd)

		self.removeChannelButton = QPushButton("-")
		self.removeChannelButton.clicked.connect(self.buttonRemove)

		buttonLayout = QHBoxLayout()
		#buttonLayout.addStretch()
		buttonLayout.addWidget(self.addChannelButton)
		buttonLayout.addWidget(self.removeChannelButton)

		autoJoinLayout = QVBoxLayout()
		# autoJoinLayout.addWidget(self.do_autojoin)
		autoJoinLayout.addWidget(self.autoChannels)
		autoJoinLayout.addLayout(buttonLayout)

		self.channels_tab.setLayout(autoJoinLayout)

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

		# CHANNELS TAB

		self.history = QCheckBox("Save server history",self)
		self.history.stateChanged.connect(self.clickHistory)

		if self.user_info["save_history"]:
			self.history.toggle()

		# USER INFO END

		vLayout = QVBoxLayout()
		#vLayout.addWidget(nickBox)
		#vLayout.addWidget(servBox)
		vLayout.addWidget(self.tabs)

		vLayout.addWidget(self.reconnect)
		vLayout.addWidget(self.do_autojoin)
		vLayout.addWidget(self.history)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(vLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def buttonAdd(self):
		x = AddChannelDialog.Dialog()
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
