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
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore

from erk.common import *
from erk.config import *

import erk.dialogs.add_channel as AddChannelDialog

class ConnectInfo:

	def __init__(self,server,port,password,ssl,nick,alter,username,realname,reconnect,autojoin):
		self.server = server
		self.port = int(port)
		self.password = password
		self.ssl = ssl
		self.nickname = nick
		self.alternate = alter
		self.username = username
		self.realname = realname
		self.reconnect = reconnect
		self.autojoin = autojoin

class Dialog(QDialog):

	@staticmethod
	def get_connect_information(can_do_ssl,parent=None):
		dialog = Dialog(can_do_ssl,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

	def return_info(self):

		h = self.StoredData[self.StoredServer]
		if "ssl" in h[3]:
			use_ssl = True
		else:
			use_ssl = False
		host = h[0]
		port = int(h[1])

		# Save user info
		user = {
			"nickname": self.nick.text(),
			"username": self.username.text(),
			"realname": self.realname.text(),
			"alternate": self.alternative.text(),
		}
		save_user(user)

		# Save server info
		save_last_server(host,str(port),"",use_ssl,self.RECONNECT,self.AUTOJOIN_CHANNELS)

		# Save channels
		saveChannels(self.autojoins)

		if self.AUTOJOIN_CHANNELS:
			channels = self.autojoins
		else:
			channels = []

		retval = ConnectInfo(host,port,None,use_ssl,self.nick.text(),self.alternative.text(),self.username.text(),self.realname.text(),self.RECONNECT,channels)

		return retval

	def setServer(self):
		self.StoredServer = self.servers.currentIndex()

		self.netType.setText("<b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b>")
		if "ssl" in self.StoredData[self.StoredServer][3]:
			self.connType.setText(f"Connect via SSL to port {self.StoredData[self.StoredServer][1]}")
		else:
			self.connType.setText(f"Connect via TCP/IP to port {self.StoredData[self.StoredServer][1]}")

	def clickReconnect(self,state):
		if state == Qt.Checked:
			self.RECONNECT = True
		else:
			self.RECONNECT = False

	def calculate_text_entry_size(self,widget,size=20):
		fm = widget.fontMetrics()
		m = widget.textMargins()
		c = widget.contentsMargins()
		w = size*fm.width('x')+m.left()+m.right()+c.left()+c.right()
		return w

	def clickChannels(self,state):
		if state == Qt.Checked:
			self.AUTOJOIN_CHANNELS = True
		else:
			self.AUTOJOIN_CHANNELS = False

	def __init__(self,can_do_ssl,parent=None):
		super(Dialog,self).__init__(parent)

		self.can_do_ssl = can_do_ssl
		self.parent = parent

		self.RECONNECT = False
		self.AUTOJOIN_CHANNELS = False

		self.StoredServer = 0
		self.StoredData = []

		self.autojoins = []

		user_info = get_user()
		channels = loadChannels()
		last_server = get_last_server()

		self.setWindowTitle("Connect to Network")
		self.setWindowIcon(QIcon(NETWORK_ICON))

		self.tabs = QTabWidget()
		self.server_tab = QWidget()
		self.user_tab = QWidget()
		self.channels_tab = QWidget()

		self.tabs.addTab(self.server_tab,"Network")
		self.tabs.addTab(self.user_tab,"User")
		self.tabs.addTab(self.channels_tab,"Channels")

		f = self.tabs.font()
		f.setBold(True)
		self.tabs.setFont(f)

		# Server information
		self.connType = QLabel("")
		self.netType = QLabel("")
		self.description = QLabel("Select an IRC network")
		self.description.setAlignment(Qt.AlignCenter)

		ntLayout = QHBoxLayout()
		ntLayout.addStretch()
		ntLayout.addWidget(self.netType)
		ntLayout.addStretch()

		ctLayout = QHBoxLayout()
		ctLayout.addStretch()
		ctLayout.addWidget(self.connType)
		ctLayout.addStretch()

		# self.servers = HTMLComboBox(self)
		self.servers = QComboBox(self)
		self.servers.activated.connect(self.setServer)

		servlist = get_network_list()

		for entry in servlist:
			if len(entry) != 4: continue
			if "ssl" in entry[3]:
				if not self.can_do_ssl: continue

			self.StoredData.append(entry)
			# self.servers.addItem("<b>" + entry[2] + "</b> - <i>" + entry[0] + "</i> ")
			self.servers.addItem(entry[2] + " - " + entry[0])

		self.StoredServer = self.servers.currentIndex()

		self.netType.setText("<b>"+self.StoredData[self.StoredServer][2]+"</b>")
		if "ssl" in self.StoredData[self.StoredServer][3]:
			self.connType.setText(f"Connect via SSL to port {self.StoredData[self.StoredServer][1]}")
		else:
			self.connType.setText(f"Connect via TCP/IP to port {self.StoredData[self.StoredServer][1]}")

		self.reconnect = QCheckBox("Reconnect on disconnection",self)
		self.reconnect.stateChanged.connect(self.clickReconnect)

		if last_server["reconnect"]:
			self.reconnect.toggle()

		fstoreLayout = QVBoxLayout()
		fstoreLayout.addWidget(self.description)
		fstoreLayout.addWidget(self.servers)
		fstoreLayout.addLayout(ntLayout)
		fstoreLayout.addLayout(ctLayout)
		# fstoreLayout.addWidget(self.reconnect)

		#servBox = QGroupBox("IRC Network")
		#servBox.setLayout(fstoreLayout)
		self.server_tab.setLayout(fstoreLayout)

		# USER INFO BEGIN

		nickLayout = QHBoxLayout()
		nickLayout.addStretch()
		self.nickLabel = QLabel("Nickname  ")
		self.nick = QLineEdit(user_info["nickname"])
		nickLayout.addWidget(self.nickLabel)
		nickLayout.addWidget(self.nick)
		nickLayout.addStretch()

		self.nick.setMaximumWidth( self.calculate_text_entry_size(self.nick) )


		alternateLayout = QHBoxLayout()
		alternateLayout.addStretch()
		self.altLabel = QLabel("Alternate ")
		self.alternative = QLineEdit(user_info["alternate"])
		alternateLayout.addWidget(self.altLabel)
		alternateLayout.addWidget(self.alternative)
		alternateLayout.addStretch()

		self.alternative.setMaximumWidth(self.calculate_text_entry_size(self.alternative))

		userLayout = QHBoxLayout()
		userLayout.addStretch()
		self.userLabel = QLabel("Username  ")
		self.username = QLineEdit(user_info["username"])
		userLayout.addWidget(self.userLabel)
		userLayout.addWidget(self.username)
		userLayout.addStretch()

		self.username.setMaximumWidth(self.calculate_text_entry_size(self.username))

		realLayout = QHBoxLayout()
		realLayout.addStretch()
		self.realLabel = QLabel("Real Name ")
		self.realname = QLineEdit(user_info["realname"])
		realLayout.addWidget(self.realLabel)
		realLayout.addWidget(self.realname)
		realLayout.addStretch()

		self.realname.setMaximumWidth(self.calculate_text_entry_size(self.realname))

		nurLayout = QVBoxLayout()
		nurLayout.addLayout(nickLayout)
		nurLayout.addLayout(alternateLayout)
		nurLayout.addLayout(userLayout)
		nurLayout.addLayout(realLayout)

		#nickBox = QGroupBox("User Information")
		#nickBox.setLayout(nurLayout)

		self.user_tab.setLayout(nurLayout)

		# USER INFO END

		# CHANNELS TAB

		self.do_autojoin = QCheckBox("Automatically join channels",self)
		self.do_autojoin.stateChanged.connect(self.clickChannels)

		if last_server["autojoin"]:
			self.do_autojoin.toggle()

		self.autoChannels = QListWidget(self)
		self.autoChannels.setMaximumHeight(100)

		#self.autoChannels.setMaximumWidth( self.calculate_text_entry_size(self.realname,20)  )

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

		for c in channels:
			channel = c[0]
			key = c[1]
			if key == "":
				item = QListWidgetItem(f"{channel}")
				item.setIcon(QIcon(CHANNEL_WINDOW))
				self.autoChannels.addItem(item)

			else:
				item = QListWidgetItem(f"{channel}")
				item.setIcon(QIcon(LOCKED_CHANNEL))
				self.autoChannels.addItem(item)

			e = [channel,key]
			self.autojoins.append(e)

		# CHANNELS TAB

		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		vLayout = QVBoxLayout()
		#vLayout.addWidget(nickBox)
		#vLayout.addWidget(servBox)
		vLayout.addWidget(self.tabs)
		# vLayout.addWidget(self.reconnect)
		vLayout.addWidget(self.reconnect)
		vLayout.addWidget(self.do_autojoin)

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
			item.setIcon(QIcon(CHANNEL_WINDOW))
			self.autoChannels.addItem(item)

		else:
			item = QListWidgetItem(f"{channel}")
			item.setIcon(QIcon(LOCKED_CHANNEL))
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

