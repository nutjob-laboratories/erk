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

from erk.config import *
from erk.resources import *
from erk.common import *
from erk.widgets import *
from erk.strings import *

from erk.dialogs import AddChannelDialog

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

		if self.parent.save_history:
			if is_in_network_list(host,str(port)):
				self.user_info["visited"].append(host+":"+str(port))
				self.user_info["visited"] = list(dict.fromkeys(self.user_info["visited"]))

		if len(h)==5:
			if h[4]=='':
				password = ''
			else:
				password = h[4]
		else:
			password = ''

		# Save user info
		user = {
			"nickname": self.nick.text(),
			"username": self.username.text(),
			"realname": self.realname.text(),
			"alternate": self.alternative.text(),
			"last_server": host,
			"last_port": str(port),
			"last_password": password,
			"channels": self.autojoins,
			"ssl": use_ssl,
			"reconnect": self.RECONNECT,
			"autojoin": self.AUTOJOIN_CHANNELS,
			"visited": self.user_info["visited"],
			"history": self.user_info["history"],
		}
		save_user(user)

		if password=='': password=None

		if self.AUTOJOIN_CHANNELS:
			channels = self.autojoins
		else:
			channels = []

		retval = ConnectInfo(host,port,password,use_ssl,self.nick.text(),self.alternative.text(),self.username.text(),self.realname.text(),self.RECONNECT,channels)

		return retval

	def setServer(self):
		self.StoredServer = self.servers.currentIndex()

		self.netType.setText("<big><b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b></big>")
		if "ssl" in self.StoredData[self.StoredServer][3]:
			d = NETWORK_DIALOG_CONNECTION_VIA_SSL_TEXT.format(self.StoredData[self.StoredServer][1])
			self.connType.setText("<small>"+d+"</small>")
		else:
			d = NETWORK_DIALOG_CONNECTION_VIA_TCP_TEXT.format(self.StoredData[self.StoredServer][1])
			self.connType.setText("<small>"+d+"</small>")

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

		self.user_info = get_user()

		self.setWindowTitle(NETWORK_DIALOG_TITLE)
		self.setWindowIcon(QIcon(FANCY_NETWORK))

		self.tabs = QTabWidget()
		self.server_tab = QWidget()
		self.user_tab = QWidget()
		self.channels_tab = QWidget()

		self.tabs.addTab(self.server_tab,CONNECT_AND_NETWORK_DIALOG_SERVER_TAB_NAME)
		self.tabs.addTab(self.user_tab,CONNECT_AND_NETWORK_DIALOG_USER_TAB_NAME)
		self.tabs.addTab(self.channels_tab,CONNECT_AND_NETWORK_DIALOG_CHANNEL_TAB_NAME)

		# Server information
		self.entryType = QLabel("")
		self.connType = QLabel("")
		self.netType = QLabel("")
		self.description = QLabel("<big>"+NETWORK_DIALOG_SELECT_TITLE+"</big>")
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

		servlist = get_network_list()

		visitedlist = self.user_info["visited"].copy()

		visited = []
		not_visited = []
		for entry in servlist:
			if len(entry) > 5: continue

			if "ssl" in entry[3]:
				if not self.can_do_ssl: continue

			s = entry[0]+":"+entry[1]
			if s in visitedlist:
				visited.append(entry)
			else:
				not_visited.append(entry)

		for e in self.user_info["history"]:
			visitedlist.append(e[0]+":"+e[1])

		servlist = visited + not_visited

		servlist = self.user_info["history"] + servlist

		for entry in servlist:

			if len(entry) > 5: continue

			if "ssl" in entry[3]:
				if not self.can_do_ssl: continue

			self.StoredData.append(entry)

			s = entry[0]+":"+entry[1]
			if s in visitedlist:
				icon = VISITED_ICON
			else:
				icon = BOOKMARK_ICON

			self.servers.addItem(QIcon(icon),entry[2] + " - " + entry[0])

		self.StoredServer = self.servers.currentIndex()

		self.netType.setText("<big><b>"+self.StoredData[self.StoredServer][2]+" IRC Network</b></big>")
		if "ssl" in self.StoredData[self.StoredServer][3]:
			d = NETWORK_DIALOG_CONNECTION_VIA_SSL_TEXT.format(self.StoredData[self.StoredServer][1])
			self.connType.setText("<small>"+d+"</small>")
		else:
			d = NETWORK_DIALOG_CONNECTION_VIA_TCP_TEXT.format(self.StoredData[self.StoredServer][1])
			self.connType.setText("<small>"+d+"</small>")

		self.reconnect = QCheckBox(CONNECT_AND_NETWORK_DIALOG_RECONNECT_NAME,self)
		self.reconnect.stateChanged.connect(self.clickReconnect)

		if self.user_info["reconnect"]:
			self.reconnect.toggle()

		fstoreLayout = QVBoxLayout()
		#fstoreLayout.addStretch()
		fstoreLayout.addWidget(QLabel(' '))
		fstoreLayout.addWidget(self.description)
		fstoreLayout.addStretch()
		fstoreLayout.addWidget(self.servers)
		fstoreLayout.addStretch()
		#fstoreLayout.addWidget(QHLine())
		fstoreLayout.addWidget(QLabel(' '))
		fstoreLayout.addStretch()
		fstoreLayout.addLayout(ntLayout)
		fstoreLayout.addLayout(ctLayout)
		fstoreLayout.addLayout(etLayout)
		fstoreLayout.addStretch()

		self.server_tab.setLayout(fstoreLayout)

		# USER INFO BEGIN

		nicklabel = NICK_LABEL
		if len(nicklabel)<LABEL_LENGTH: nicklabel = nicklabel + (' '*(LABEL_LENGTH-len(nicklabel)))

		alternatelabel = ALTERNATE_LABEL
		if len(alternatelabel)<LABEL_LENGTH: alternatelabel = alternatelabel + (' '*(LABEL_LENGTH-len(alternatelabel)))

		usernamelabel = USERNAME_LABEL
		if len(usernamelabel)<LABEL_LENGTH: usernamelabel = usernamelabel + (' '*(LABEL_LENGTH-len(usernamelabel)))

		realnamelabel = REALNAME_LABEL
		if len(realnamelabel)<LABEL_LENGTH: realnamelabel = realnamelabel + (' '*(LABEL_LENGTH-len(realnamelabel)))

		nickLayout = QHBoxLayout()
		nickLayout.addStretch()
		self.nickLabel = QLabel(nicklabel)
		self.nick = QLineEdit(self.user_info["nickname"])
		nickLayout.addWidget(self.nickLabel)
		nickLayout.addWidget(self.nick)
		nickLayout.addStretch()

		self.nick.setMaximumWidth( self.calculate_text_entry_size(self.nick) )


		alternateLayout = QHBoxLayout()
		alternateLayout.addStretch()
		self.altLabel = QLabel(alternatelabel)
		self.alternative = QLineEdit(self.user_info["alternate"])
		alternateLayout.addWidget(self.altLabel)
		alternateLayout.addWidget(self.alternative)
		alternateLayout.addStretch()

		self.alternative.setMaximumWidth(self.calculate_text_entry_size(self.alternative))

		userLayout = QHBoxLayout()
		userLayout.addStretch()
		self.userLabel = QLabel(usernamelabel)
		self.username = QLineEdit(self.user_info["username"])
		userLayout.addWidget(self.userLabel)
		userLayout.addWidget(self.username)
		userLayout.addStretch()

		self.username.setMaximumWidth(self.calculate_text_entry_size(self.username))

		realLayout = QHBoxLayout()
		realLayout.addStretch()
		self.realLabel = QLabel(realnamelabel)
		self.realname = QLineEdit(self.user_info["realname"])
		realLayout.addWidget(self.realLabel)
		realLayout.addWidget(self.realname)
		realLayout.addStretch()

		self.realname.setMaximumWidth(self.calculate_text_entry_size(self.realname))

		nurLayout = QVBoxLayout()
		nurLayout.addLayout(nickLayout)
		nurLayout.addLayout(alternateLayout)
		nurLayout.addLayout(userLayout)
		nurLayout.addLayout(realLayout)

		self.user_tab.setLayout(nurLayout)

		# USER INFO END

		# CHANNELS TAB

		self.do_autojoin = QCheckBox(CONNECT_AND_NETWORK_DIALOG_AUTOJOIN_NAME,self)
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
		buttonLayout.addWidget(self.addChannelButton)
		buttonLayout.addWidget(self.removeChannelButton)

		autoJoinLayout = QVBoxLayout()
		autoJoinLayout.addWidget(self.autoChannels)
		autoJoinLayout.addLayout(buttonLayout)

		self.channels_tab.setLayout(autoJoinLayout)

		for c in self.user_info["channels"]:
			channel = c[0]
			key = c[1]
			if key == "":
				item = QListWidgetItem(f"{channel}")
				item.setIcon(QIcon(CHANNEL_WINDOW_ICON))
				self.autoChannels.addItem(item)

			else:
				item = QListWidgetItem(f"{channel}")
				item.setIcon(QIcon(LOCKED_CHANNEL_ICON))
				self.autoChannels.addItem(item)

			e = [channel,key]
			self.autojoins.append(e)

		# CHANNELS TAB

		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		vLayout = QVBoxLayout()
		vLayout.addWidget(self.tabs)
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

		if key == "":
			item = QListWidgetItem(f"{channel}")
			item.setIcon(QIcon(CHANNEL_WINDOW_ICON))
			self.autoChannels.addItem(item)

		else:
			item = QListWidgetItem(f"{channel}")
			item.setIcon(QIcon(LOCKED_CHANNEL_ICON))
			self.autoChannels.addItem(item)

		e = [channel,key]
		self.autojoins.append(e)

	def buttonRemove(self):
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

