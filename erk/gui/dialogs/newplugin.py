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
	def get_plugin_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_strings()
		return None

	def return_strings(self):

		classname = str(self.classname.text())
		name = str(self.pluginname.text())
		version = str(self.version.text())
		description = str(self.description.text())



		retval = [classname,name,version,description,self.silent,self.nowindows,self.noirc]
		return retval

	def doSilent(self):
		if self.silent:
			self.silent = False
		else:
			self.silent = True

	def doWindows(self):
		if self.nowindows:
			self.nowindows = False
		else:
			self.nowindows = True

	def doIrc(self):
		if self.nowindows:
			self.noirc = False
		else:
			self.noirc = True

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.silent = False
		self.nowindows = False
		self.noirc = False

		self.setWindowTitle(f"New Plugin")
		self.setWindowIcon(QIcon(PLUGIN_ICON))


		# User information
		classLayout = QHBoxLayout()
		self.classLabel = QLabel("Class Name")
		self.classname = QLineEdit()
		classLayout.addWidget(self.classLabel)
		classLayout.addStretch()
		classLayout.addWidget(self.classname)

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("Name")
		self.pluginname = QLineEdit()
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addStretch()
		nameLayout.addWidget(self.pluginname)

		versionLayout = QHBoxLayout()
		self.versionLabel = QLabel("Version")
		self.version = QLineEdit("1.0")
		versionLayout.addWidget(self.versionLabel)
		versionLayout.addStretch()
		versionLayout.addWidget(self.version)

		descriptionLayout = QHBoxLayout()
		self.descLabel = QLabel("Description")
		self.description = QLineEdit()
		descriptionLayout.addWidget(self.descLabel)
		descriptionLayout.addStretch()
		descriptionLayout.addWidget(self.description)

		self.isSilent = QCheckBox("Don't display outgoing messages",self)
		self.isSilent.stateChanged.connect(self.doSilent)

		self.isNowindows = QCheckBox("Don't open new windows",self)
		self.isNowindows.stateChanged.connect(self.doWindows)

		self.isNoIrc = QCheckBox("Disable all IRC commands",self)
		self.isNoIrc.stateChanged.connect(self.doIrc)

		nurLayout = QVBoxLayout()
		nurLayout.addLayout(classLayout)
		nurLayout.addLayout(nameLayout)
		nurLayout.addLayout(versionLayout)
		nurLayout.addLayout(descriptionLayout)
		nurLayout.addWidget(self.isSilent)
		nurLayout.addWidget(self.isNowindows)
		nurLayout.addWidget(self.isNoIrc)

		nickBox = QGroupBox("Plugin Information")
		nickBox.setLayout(nurLayout)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(nickBox)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
