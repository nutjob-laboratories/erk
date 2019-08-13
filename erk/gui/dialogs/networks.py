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

import erk.gui.dialogs.add_channel as AddChannelDialog

from erk.gui.htmlwidgets import HTMLComboBox

class Dialog(QDialog):

	@staticmethod
	def get_connect_information(can_do_ssl,parent=None):
		dialog = Dialog(can_do_ssl,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_strings()
		return None

	def return_strings(self):

		items = [] 
		for index in range(self.autoChannels.count()): 
			 items.append(self.autoChannels.item(index).text())

		h = self.StoredData[self.StoredServer]
		if "ssl" in h[3]:
			use_ssl = 1
		else:
			use_ssl = 0
		host = h[0]
		port = int(h[1])

		if len(items)>0: save_autojoin_channels(host,items)

		if self.RECONNECT:
			recon = 1
		else:
			recon = 0

		retval = map(str, [self.nick.text(), self.username.text(), self.realname.text(), self.alternative.text(), host, port, ''])
		retval = list(retval)
		retval.append(str(use_ssl))
		retval.append(str(recon))
		return retval

	def setServer(self):
		self.StoredServer = self.servers.currentIndex()

		self.netType.setText("<b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b>")
		if "ssl" in self.StoredData[self.StoredServer][3]:
			self.connType.setText(f"Connect via SSL to port {self.StoredData[self.StoredServer][1]}")
		else:
			self.connType.setText(f"Connect via TCP/IP to port {self.StoredData[self.StoredServer][1]}")

		self.autoChannels.clear()
		host = self.StoredData[self.StoredServer][0]
		for c in get_autojoins(host):
			p = c.split('/')
			if len(p)==2:
				item = QListWidgetItem(c)
				item.setIcon(QIcon(LOCKED_ICON))
				self.autoChannels.addItem(item)
			else:
				item = QListWidgetItem(c)
				item.setIcon(QIcon(CHANNEL_WINDOW_ICON))
				self.autoChannels.addItem(item)

	def doAddChannel(self):
		self.x = AddChannelDialog.Dialog(self)
		self.x.show()

	def doRemoveChannel(self):
		self.removeSel()

	def removeSel(self):
	    listItems=self.autoChannels.selectedItems()
	    if not listItems: return        
	    for item in listItems:
	       self.autoChannels.takeItem(self.autoChannels.row(item))

	def clickRecon(self):
		if self.RECONNECT:
			self.RECONNECT = False
		else:
			self.RECONNECT = True

	def __init__(self,can_do_ssl,parent=None):
		super(Dialog,self).__init__(parent)

		self.can_do_ssl = can_do_ssl
		self.parent = parent

		self.RECONNECT = False

		self.StoredServer = 0
		self.StoredData = []

		self.user_data = get_user()

		self.setWindowTitle(f"Connect to Network")
		self.setWindowIcon(QIcon(NETWORK_ICON))

		# Server information
		self.connType = QLabel("")
		self.netType = QLabel("")

		ntLayout = QHBoxLayout()
		ntLayout.addStretch()
		ntLayout.addWidget(self.netType)
		ntLayout.addStretch()

		ctLayout = QHBoxLayout()
		ctLayout.addStretch()
		ctLayout.addWidget(self.connType)
		ctLayout.addStretch()

		# self.servers = QComboBox(self)
		self.servers = HTMLComboBox(self)
		self.servers.activated.connect(self.setServer)

		script = open(IRC_NETWORK_LIST,"r")
		for line in script:
			x = line.split(":")
			if len(x) != 4: continue
			x[0].strip()
			x[1].strip()
			x[2].strip()
			x[3].strip()
			if "ssl" in x[3]:
				if not self.can_do_ssl: continue

			if x[2] == UNKNOWN_NETWORK: x[2] = "Unknown"

			#print(self.can_do_ssl)
			self.StoredData.append(x)
			# self.servers.addItem(x[2] + "\t\t" + x[0])
			self.servers.addItem("<b>" + x[2] + "</b> - <i>" + x[0] + "</i> ")

		self.StoredServer = self.servers.currentIndex()

		self.netType.setText("<b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b>")
		if "ssl" in self.StoredData[self.StoredServer][3]:
			self.connType.setText(f"Connect via SSL to port {self.StoredData[self.StoredServer][1]}")
		else:
			self.connType.setText(f"Connect via TCP/IP to port {self.StoredData[self.StoredServer][1]}")

		self.recon = QCheckBox("Reconnect on disconnection",self)
		self.recon.stateChanged.connect(self.clickRecon)

		fstoreLayout = QVBoxLayout()
		fstoreLayout.addWidget(self.servers)
		#fstoreLayout.addStretch()
		fstoreLayout.addLayout(ntLayout)
		fstoreLayout.addLayout(ctLayout)
		fstoreLayout.addWidget(QLabel(" "))
		fstoreLayout.addWidget(self.recon)

		servBox = QGroupBox("IRC Network")
		servBox.setLayout(fstoreLayout)
		
		# User information
		nickLayout = QHBoxLayout()
		self.nickLabel = QLabel("Nickname")
		self.nick = QLineEdit(self.user_data['nick'])
		nickLayout.addWidget(self.nickLabel)
		nickLayout.addStretch()
		nickLayout.addWidget(self.nick)

		alternateLayout = QHBoxLayout()
		self.altLabel = QLabel("Alternate")
		self.alternative = QLineEdit(self.user_data["alternate"])
		alternateLayout.addWidget(self.altLabel)
		alternateLayout.addStretch()
		alternateLayout.addWidget(self.alternative)

		userLayout = QHBoxLayout()
		self.userLabel = QLabel("Username")
		self.username = QLineEdit(self.user_data['username'])
		userLayout.addWidget(self.userLabel)
		userLayout.addStretch()
		userLayout.addWidget(self.username)

		realLayout = QHBoxLayout()
		self.realLabel = QLabel("Real Name")
		self.realname = QLineEdit(self.user_data['realname'])
		realLayout.addWidget(self.realLabel)
		realLayout.addStretch()
		realLayout.addWidget(self.realname)

		nurLayout = QVBoxLayout()
		nurLayout.addLayout(nickLayout)
		nurLayout.addLayout(alternateLayout)
		nurLayout.addLayout(userLayout)
		nurLayout.addLayout(realLayout)

		nickBox = QGroupBox("User Information")
		nickBox.setLayout(nurLayout)

		#############################
		# autojoin channels

		inithost = self.StoredData[self.StoredServer][0]

		self.autoChannels = QListWidget(self)
		self.autoChannels.setMaximumWidth(175)
		#self.parent.autoChannels.addItem(f"{channel}")
		for c in get_autojoins(inithost):
			p = c.split('/')
			if len(p)==2:
				item = QListWidgetItem(c)
				item.setIcon(QIcon(LOCKED_ICON))
				self.autoChannels.addItem(item)
			else:
				item = QListWidgetItem(c)
				item.setIcon(QIcon(CHANNEL_WINDOW_ICON))
				self.autoChannels.addItem(item)

		self.addChannelButton = QPushButton("+")
		self.addChannelButton.clicked.connect(self.doAddChannel)

		self.removeChannelButton = QPushButton("-")
		self.removeChannelButton.clicked.connect(self.doRemoveChannel)

		buttonLayout = QHBoxLayout()
		buttonLayout.addStretch()
		buttonLayout.addWidget(self.addChannelButton)
		buttonLayout.addWidget(self.removeChannelButton)

		autoJoinLayout = QVBoxLayout()
		autoJoinLayout.addWidget(self.autoChannels)
		autoJoinLayout.addLayout(buttonLayout)
		

		chanBox = QGroupBox("Auto-Join Channels")
		chanBox.setLayout(autoJoinLayout)

		#############################

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)


		vLayout = QVBoxLayout()
		vLayout.addWidget(nickBox)
		vLayout.addWidget(servBox)

		hLayout = QHBoxLayout()
		hLayout.addLayout(vLayout)
		hLayout.addWidget(chanBox)


		finalLayout = QVBoxLayout()
		finalLayout.addLayout(hLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)




