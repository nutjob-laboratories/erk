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

class Dialog(QDialog):

	def doAdd(self):
		channel = self.name.text()
		key = self.key.text()

		if len(channel)==0:
			self.error_dialog = QErrorMessage()
			self.error_dialog.showMessage("No channel entered!")
			self.close()
			return

		#print(channel,key)
		if key == "":
			item = QListWidgetItem(f"{channel}")
			item.setIcon(QIcon(CHANNEL_WINDOW_ICON))
			self.parent.autoChannels.addItem(item)
			self.parent.AUTOJOINS.append(f"{channel}")

		else:
			item = QListWidgetItem(f"{channel}")
			item.setIcon(QIcon(LOCKED_ICON))
			self.parent.autoChannels.addItem(item)
			self.parent.AUTOJOINS.append(f"{channel}{AUTOJOIN_DELIMITER}{key}")

		self.close()

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle(f"Autojoin channel")
		self.setWindowIcon(QIcon(CHANNEL_WINDOW_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("Channel")
		self.name = QLineEdit()
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addStretch()
		nameLayout.addWidget(self.name)

		keyLayout = QHBoxLayout()
		self.keyLabel = QLabel("Key")
		self.key = QLineEdit()
		self.key.setEchoMode(QLineEdit.Password)
		keyLayout.addWidget(self.keyLabel)
		keyLayout.addStretch()
		keyLayout.addWidget(self.key)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.doAdd)
		buttons.rejected.connect(self.close)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		finalLayout.addLayout(keyLayout)
		finalLayout.addStretch()
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
