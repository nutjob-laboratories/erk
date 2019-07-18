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

	def doSet(self,state):
		if self.firstLoad:
			self.firstLoad = False
			return

		if state==2:
			self.unsetmode.setChecked(False)
			self.isSetMode = False
		else:
			self.unsetmode.setChecked(True)
			self.isSetMode = True

	def doUnset(self,state):
		if self.firstLoad:
			self.firstLoad = False
			return

		if state==2:
			self.setmode.setChecked(False)
			self.isSetMode = False
		else:
			self.setmode.setChecked(True)
			self.isSetMode = True

	def return_list(self):
		target = str(self.name.text())
		modes = str(self.modes.text())
		sid = str(self.sid.text())

		limit = str(self.limit.text())
		user = str(self.user.text())
		mask = str(self.mask.text())

		return [self.isSetMode,target,modes,limit,user,mask,sid]


	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle(f"Plugin.mode()")
		
		self.setWindowIcon(QIcon(EDIT_ICON))

		self.firstLoad = True

		self.isSetMode = True



		self.setmode = QCheckBox("Set mode",self)
		self.setmode.stateChanged.connect(self.doSet)

		self.setmode.setChecked(True)

		self.unsetmode = QCheckBox("Unset mode",self)
		self.unsetmode.stateChanged.connect(self.doUnset)

		setLayout = QHBoxLayout()
		setLayout.addWidget(self.setmode)
		setLayout.addWidget(self.unsetmode)

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("<b>Target</b>")
		self.name = QLineEdit()
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addWidget(self.name)

		modesLayout = QHBoxLayout()
		self.modesLabel = QLabel("<b>Modes</b>")
		self.modes = QLineEdit()
		modesLayout.addWidget(self.modesLabel)
		modesLayout.addWidget(self.modes)


		limitLayout = QHBoxLayout()
		self.limitLabel = QLabel("<i>Limit</i>")
		self.limit = QLineEdit()
		limitLayout.addWidget(self.limitLabel)
		limitLayout.addWidget(self.limit)

		userLayout = QHBoxLayout()
		self.userLabel = QLabel("<i>User</i>")
		self.user = QLineEdit()
		userLayout.addWidget(self.userLabel)
		userLayout.addWidget(self.user)

		maskLayout = QHBoxLayout()
		self.maskLabel = QLabel("<i>Mask</i>")
		self.mask = QLineEdit()
		maskLayout.addWidget(self.maskLabel)
		maskLayout.addWidget(self.mask)



		sidLayout = QHBoxLayout()
		self.sidLabel = QLabel("<i>Server ID</i>")
		self.sid = QLineEdit()
		sidLayout.addWidget(self.sidLabel)
		sidLayout.addWidget(self.sid)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		self.optLabel = QLabel("Arguments in <i>italics</i> are optional")

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(setLayout)
		finalLayout.addLayout(nameLayout)
		finalLayout.addLayout(modesLayout)
		finalLayout.addLayout(limitLayout)
		finalLayout.addLayout(userLayout)
		finalLayout.addLayout(maskLayout)
		finalLayout.addLayout(sidLayout)
		finalLayout.addStretch()
		finalLayout.addWidget(self.optLabel)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
