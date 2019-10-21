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

import erk.dialogs.add_ignore as AddIgnoreDialog

class Dialog(QDialog):

	def doOkay(self):
		
		items = [] 
		for index in range(self.ignoredUsers.count()): 
			 items.append(self.ignoredUsers.item(index).text())

		save_ignore(items)
		self.parent.ignore = items
		self.close()

	def doCancel(self):
		self.close()

	def doAddUser(self):
		self.x = AddIgnoreDialog.Dialog(self)
		self.x.show()

	def doRemoveUser(self):
		self.removeSel()

	def removeSel(self):
	    listItems=self.ignoredUsers.selectedItems()
	    if not listItems: return        
	    for item in listItems:
	       self.ignoredUsers.takeItem(self.ignoredUsers.row(item))

	def setSubwindow(self,sw):
		self.subwindow = sw


	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.subwindow = None

		self.ignored = get_ignore()

		self.setWindowTitle(f"Ignored Users")
		self.setWindowIcon(QIcon(IGNORE_ICON))

		self.ignoredUsers = QListWidget(self)
		self.ignoredUsers.setMaximumWidth(175)

		for c in self.ignored:
			item = QListWidgetItem(c)
			item.setIcon(QIcon(USER_ICON))
			self.ignoredUsers.addItem(item)


		self.addUserButton = QPushButton("+")
		self.addUserButton.clicked.connect(self.doAddUser)

		self.removeUserButton = QPushButton("-")
		self.removeUserButton.clicked.connect(self.doRemoveUser)

		buttonLayout = QHBoxLayout()
		buttonLayout.addStretch()
		buttonLayout.addWidget(self.addUserButton)
		buttonLayout.addWidget(self.removeUserButton)

		ignoredUserLayout = QVBoxLayout()
		ignoredUserLayout.addWidget(self.ignoredUsers)
		ignoredUserLayout.addLayout(buttonLayout)
		

		ignoreBox = QGroupBox("")
		ignoreBox.setLayout(ignoredUserLayout)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.doOkay)
		buttons.rejected.connect(self.doCancel)

		buttons.button(QDialogButtonBox.Ok).setText("Save")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(ignoreBox)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)