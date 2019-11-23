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

from erk.config import *
from erk.resources import *
from erk.common import *
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
			"last_server": self.host.text(),
			"last_port": self.port.text(),
			"last_password": self.password.text(),
			"channels": self.autojoins,
			"ssl": self.DIALOG_CONNECT_VIA_SSL,
			"reconnect": self.RECONNECT,
			"autojoin": self.AUTOJOIN_CHANNELS,
			"visited": self.user_info["visited"],
			"history": self.user_info["history"],
		}

		if self.parent.save_history:

			if not is_in_network_list(self.host.text(),self.port.text()):

				if self.DIALOG_CONNECT_VIA_SSL:
					dossl = "ssl"
				else:
					dossl = "normal"

				# Check to make sure it's not already in history
				found = False
				for e in self.user_info["history"]:
					if e[0]==self.host.text():
						if e[1]==self.port.text():
							# It's already in history
							# Update any settings as necessary
							found = True
							# Update password
							if len(e)==5:
								if e[4]!='':
									if self.password.text()!='':
										e[4] = self.password.text()
							else:
								if self.password.text()!='':
									e.append(self.password.text())
							# Update SSL
							if self.DIALOG_CONNECT_VIA_SSL:
								if e[3]=="normal":
									e[3]="ssl"
							else:
								if e[3]=="ssl":
									e[3]="normal"

				if not found:
					hpass = self.password.text()
					if hpass=='':
						entry = [
							self.host.text(),
							self.port.text(),
							"Unknown",
							dossl
						]
					else:
						entry = [
							self.host.text(),
							self.port.text(),
							"Unknown",
							dossl,
							hpass
						]

					self.user_info["history"].append(entry)

		save_user(user)

		if self.AUTOJOIN_CHANNELS:
			channels = self.autojoins
		else:
			channels = []

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

		self.setWindowTitle(CONNECT_DIALOG_TITLE)
		self.setWindowIcon(QIcon(SERVER_ICON))

		self.user_info = get_user()

		self.tabs = QTabWidget()
		self.server_tab = QWidget()
		self.user_tab = QWidget()
		self.channels_tab = QWidget()

		self.tabs.addTab(self.server_tab,CONNECT_AND_NETWORK_DIALOG_SERVER_TAB_NAME)
		self.tabs.addTab(self.user_tab,CONNECT_AND_NETWORK_DIALOG_USER_TAB_NAME)
		self.tabs.addTab(self.channels_tab,CONNECT_AND_NETWORK_DIALOG_CHANNEL_TAB_NAME)

		# SERVER INFO BEGIN

		serverlabel = HOST_LABEL
		if len(serverlabel)<LABEL_LENGTH: serverlabel = serverlabel + (' '*(LABEL_LENGTH-len(serverlabel)))

		sportlabel = PORT_LABEL
		if len(sportlabel)<LABEL_LENGTH: sportlabel = sportlabel + (' '*(LABEL_LENGTH-len(sportlabel)))

		passwordlabel = PASSWORD_LABEL
		if len(passwordlabel)<LABEL_LENGTH: passwordlabel = passwordlabel + (' '*(LABEL_LENGTH-len(passwordlabel)))

		hostLayout = QHBoxLayout()
		hostLayout.addStretch()
		self.hostLabel = QLabel(serverlabel)
		self.host = QLineEdit(self.user_info["last_server"])
		hostLayout.addWidget(self.hostLabel)
		hostLayout.addWidget(self.host)
		hostLayout.addStretch()

		portLayout = QHBoxLayout()
		portLayout.addStretch()
		self.portLabel = QLabel(sportlabel)
		self.port = QLineEdit(self.user_info["last_port"])
		portLayout.addWidget(self.portLabel)
		portLayout.addWidget(self.port)
		portLayout.addStretch()

		passLayout = QHBoxLayout()
		passLayout.addStretch()
		self.passLabel = QLabel(passwordlabel)
		self.password = QLineEdit(self.user_info["last_password"])
		self.password.setEchoMode(QLineEdit.Password)
		passLayout.addWidget(self.passLabel)
		passLayout.addWidget(self.password)
		passLayout.addStretch()

		self.ssl = QCheckBox(CONNECT_DIALOG_SSL_NAME,self)
		self.ssl.stateChanged.connect(self.clickSSL)

		self.reconnect = QCheckBox(CONNECT_AND_NETWORK_DIALOG_RECONNECT_NAME,self)
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
		sslLayout.addStretch()

		servLayout = QVBoxLayout()
		servLayout.addStretch()
		servLayout.addLayout(hostLayout)
		servLayout.addLayout(portLayout)
		servLayout.addLayout(passLayout)
		servLayout.addStretch()
		servLayout.addLayout(sslLayout)
		servLayout.addStretch()

		self.server_tab.setLayout(servLayout)

		# SERVER INFO END

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

		self.nick.setMaximumWidth( self.calculate_text_entry_size(self.nick,20)  )

		alternateLayout = QHBoxLayout()
		alternateLayout.addStretch()
		self.altLabel = QLabel(alternatelabel)
		self.alternative = QLineEdit(self.user_info["alternate"])
		alternateLayout.addWidget(self.altLabel)
		alternateLayout.addWidget(self.alternative)
		alternateLayout.addStretch()

		self.alternative.setMaximumWidth( self.calculate_text_entry_size(self.alternative,20)  )

		userLayout = QHBoxLayout()
		userLayout.addStretch()
		self.userLabel = QLabel(usernamelabel)
		self.username = QLineEdit(self.user_info["username"])
		userLayout.addWidget(self.userLabel)
		userLayout.addWidget(self.username)
		userLayout.addStretch()

		self.username.setMaximumWidth( self.calculate_text_entry_size(self.username,20)  )

		realLayout = QHBoxLayout()
		realLayout.addStretch()
		self.realLabel = QLabel(realnamelabel)
		self.realname = QLineEdit(self.user_info["realname"])
		realLayout.addWidget(self.realLabel)
		realLayout.addWidget(self.realname)
		realLayout.addStretch()

		self.realname.setMaximumWidth( self.calculate_text_entry_size(self.realname,20)  )

		nurLayout = QVBoxLayout()
		nurLayout.addLayout(nickLayout)
		nurLayout.addLayout(alternateLayout)
		nurLayout.addLayout(userLayout)
		nurLayout.addLayout(realLayout)

		self.user_tab.setLayout(nurLayout)

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

		# USER INFO END

		vLayout = QVBoxLayout()
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

	def calculate_text_entry_size(self,widget,size=20):
		fm = widget.fontMetrics()
		m = widget.textMargins()
		c = widget.contentsMargins()
		w = size*fm.width('x')+m.left()+m.right()+c.left()+c.right()
		return w