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

from erk.common import *

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

		try:
			port = int(self.port.text())
		except:
			ErrorDialog("Port must be a number")
			return None

		if len(self.password.text())>0:
			password = self.password.text()
		else:
			password = None

		# Save user info
		user = {
			"nickname": self.nick.text(),
			"username": self.username.text(),
			"realname": self.realname.text(),
			"alternate": self.alternative.text(),
		}
		save_user(user)

		# Save channels
		saveChannels(self.autojoins)

		if self.AUTOJOIN_CHANNELS:
			channels = self.autojoins
		else:
			channels = []

		# Save server info
		save_last_server(self.host.text(),self.port.text(),self.password.text(),self.DIALOG_CONNECT_VIA_SSL,self.RECONNECT,self.AUTOJOIN_CHANNELS)

		# Save history
		if self.parent.save_server_history:
			add_history(self.host.text(),port,password,self.DIALOG_CONNECT_VIA_SSL,UNKNOWN_IRC_NETWORK)

		retval = ConnectInfo(self.host.text(),port,password,self.DIALOG_CONNECT_VIA_SSL,self.nick.text(),self.alternative.text(),self.username.text(),self.realname.text(),self.RECONNECT,channels)

		return retval

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

	def __init__(self,can_do_ssl,parent=None):
		super(Dialog,self).__init__(parent)

		self.can_do_ssl = can_do_ssl
		self.parent = parent

		self.autojoins = []

		self.DIALOG_CONNECT_VIA_SSL = False
		self.RECONNECT = False
		self.AUTOJOIN_CHANNELS = False

		self.setWindowTitle(f"Connect to IRC")
		self.setWindowIcon(QIcon(SERVER_ICON))

		self.user_info = get_user()
		last_server = get_last_server()
		channels = loadChannels()

		self.tabs = QTabWidget()
		self.server_tab = QWidget()
		self.user_tab = QWidget()
		self.channels_tab = QWidget()

		self.tabs.addTab(self.server_tab,"Server")
		self.tabs.addTab(self.user_tab,"User")
		self.tabs.addTab(self.channels_tab,"Channels")

		f = self.tabs.font()
		f.setBold(True)
		self.tabs.setFont(f)

		# SERVER INFO BEGIN

		hostLayout = QHBoxLayout()
		hostLayout.addStretch()
		self.hostLabel = QLabel("Host     ")
		self.host = QLineEdit(last_server["host"])
		hostLayout.addWidget(self.hostLabel)
		hostLayout.addWidget(self.host)
		hostLayout.addStretch()

		portLayout = QHBoxLayout()
		portLayout.addStretch()
		self.portLabel = QLabel("Port     ")
		self.port = QLineEdit(last_server["port"])
		portLayout.addWidget(self.portLabel)
		portLayout.addWidget(self.port)
		portLayout.addStretch()

		passLayout = QHBoxLayout()
		passLayout.addStretch()
		self.passLabel = QLabel("Password ")
		self.password = QLineEdit(last_server["password"])
		self.password.setEchoMode(QLineEdit.Password)
		passLayout.addWidget(self.passLabel)
		passLayout.addWidget(self.password)
		passLayout.addStretch()

		self.ssl = QCheckBox("Connect via SSL",self)
		self.ssl.stateChanged.connect(self.clickSSL)

		self.reconnect = QCheckBox("Reconnect on disconnection",self)
		self.reconnect.stateChanged.connect(self.clickReconnect)

		if last_server["ssl"]:
			self.ssl.toggle()

		if last_server["reconnect"]:
			self.reconnect.toggle()

		if not self.can_do_ssl:
			self.DIALOG_CONNECT_VIA_SSL = False
			self.ssl.setEnabled(False)

		servLayout = QVBoxLayout()
		servLayout.addStretch()
		servLayout.addLayout(hostLayout)
		servLayout.addLayout(portLayout)
		servLayout.addLayout(passLayout)
		servLayout.addWidget(self.ssl)
		# servLayout.addWidget(self.reconnect)
		servLayout.addStretch()

		#servBox = QGroupBox("IRC Server")
		#servBox.setLayout(servLayout)

		self.server_tab.setLayout(servLayout)

		# SERVER INFO END

		# USER INFO BEGIN

		nickLayout = QHBoxLayout()
		nickLayout.addStretch()
		self.nickLabel = QLabel("Nickname  ")
		self.nick = QLineEdit(self.user_info["nickname"])
		#self.nick = QLineEdit()
		nickLayout.addWidget(self.nickLabel)
		#nickLayout.addStretch()
		nickLayout.addWidget(self.nick)
		nickLayout.addStretch()

		self.nick.setMaximumWidth( self.calculate_text_entry_size(self.nick,20)  )

		alternateLayout = QHBoxLayout()
		alternateLayout.addStretch()
		self.altLabel = QLabel("Alternate ")
		self.alternative = QLineEdit(self.user_info["alternate"])
		#self.alternative = QLineEdit()
		alternateLayout.addWidget(self.altLabel)
		#alternateLayout.addStretch()
		alternateLayout.addWidget(self.alternative)
		alternateLayout.addStretch()

		self.alternative.setMaximumWidth( self.calculate_text_entry_size(self.alternative,20)  )

		userLayout = QHBoxLayout()
		userLayout.addStretch()
		self.userLabel = QLabel("Username  ")
		self.username = QLineEdit(self.user_info["username"])
		#self.username = QLineEdit()
		userLayout.addWidget(self.userLabel)
		#userLayout.addStretch()
		userLayout.addWidget(self.username)
		userLayout.addStretch()

		self.username.setMaximumWidth( self.calculate_text_entry_size(self.username,20)  )

		realLayout = QHBoxLayout()
		realLayout.addStretch()
		self.realLabel = QLabel("Real Name ")
		self.realname = QLineEdit(self.user_info["realname"])
		#self.realname = QLineEdit()
		realLayout.addWidget(self.realLabel)
		#realLayout.addStretch()
		realLayout.addWidget(self.realname)
		realLayout.addStretch()

		self.realname.setMaximumWidth( self.calculate_text_entry_size(self.realname,20)  )

		nurLayout = QVBoxLayout()
		nurLayout.addLayout(nickLayout)
		nurLayout.addLayout(alternateLayout)
		nurLayout.addLayout(userLayout)
		nurLayout.addLayout(realLayout)

		#nickBox = QGroupBox("User Information")
		#nickBox.setLayout(nurLayout)

		self.user_tab.setLayout(nurLayout)

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

		# USER INFO END

		vLayout = QVBoxLayout()
		#vLayout.addWidget(nickBox)
		#vLayout.addWidget(servBox)
		vLayout.addWidget(self.tabs)

		vLayout.addWidget(self.reconnect)
		vLayout.addWidget(self.do_autojoin)

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

	def calculate_text_entry_size(self,widget,size=20):
		fm = widget.fontMetrics()
		m = widget.textMargins()
		c = widget.contentsMargins()
		w = size*fm.width('x')+m.left()+m.right()+c.left()+c.right()
		return w