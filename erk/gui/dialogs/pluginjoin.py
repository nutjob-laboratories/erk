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

	@staticmethod
	def get_cmd_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_list()
		return None

	def return_list(self):
		channel = str(self.channel.text())
		key = str(self.key.text())
		sid = str(self.sid.text())

		return [channel,key,sid]

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle(f"Plugin.join()")
		
		self.setWindowIcon(QIcon(EDIT_ICON))

		channelLayout = QHBoxLayout()
		self.channelLabel = QLabel("<b>Channel</b>")
		self.channel = QLineEdit()
		channelLayout.addWidget(self.channelLabel)
		channelLayout.addWidget(self.channel)

		keyLayout = QHBoxLayout()
		self.keyLabel = QLabel("<i>Key</i>")
		self.key = QLineEdit()
		keyLayout.addWidget(self.keyLabel)
		keyLayout.addWidget(self.key)

		sidLayout = QHBoxLayout()
		self.sidLabel = QLabel("<i>Server ID</i><")
		self.sid = QLineEdit()
		sidLayout.addWidget(self.sidLabel)
		sidLayout.addWidget(self.sid)

		self.optLabel = QLabel("Arguments in <i>italics</i> are optional")

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(channelLayout)
		finalLayout.addLayout(keyLayout)
		finalLayout.addLayout(sidLayout)
		finalLayout.addStretch()
		finalLayout.addWidget(self.optLabel)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
