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

from erk.resources import *
from erk.strings import *

class Dialog(QDialog):

	@staticmethod
	def get_name_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		if self.name.text().strip()=='':
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("Plugin name is required")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		if self.description.text().strip()=='':
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("Plugin description is required")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		retval = [self.name.text(),self.description.text()]

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Plugin information")
		self.setWindowIcon(QIcon(EDITOR_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("Name")
		self.name = QLineEdit()
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addStretch()
		nameLayout.addWidget(self.name)

		descriptionLayout = QHBoxLayout()
		self.descriptionLabel = QLabel("Description")
		self.description = QLineEdit()
		descriptionLayout.addWidget(self.descriptionLabel)
		descriptionLayout.addStretch()
		descriptionLayout.addWidget(self.description)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		finalLayout.addLayout(descriptionLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
