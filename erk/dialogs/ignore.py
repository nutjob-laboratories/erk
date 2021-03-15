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

from ..resources import *
from .add_ignore import Dialog as AddIgnore
from .. import events
from ..files import *

class Dialog(QDialog):

	def closeEvent(self, event):

		newIgnores =  [str(self.ignorelist.item(i).text()) for i in range(self.ignorelist.count())]
		
		newIgnores.sort()
		self.parent.ignore.sort()

		if self.parent.ignore!=newIgnores:
			self.parent.ignore = list(newIgnores)

			u = get_user(self.parent.userfile)
			u["ignore"] = newIgnores
			save_user(u,self.parent.userfile)

			events.recheck_userlists()

		event.accept()
		self.close()

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		

		self.setWindowTitle("Ignore Manager")
		self.setWindowIcon(QIcon(HIDE_ICON))

		

		self.ignorelist = QListWidget(self)

		for x in self.parent.ignore:
			item = QListWidgetItem(x)
			self.ignorelist.addItem(item)

		self.addButton = QPushButton("Add Entry")
		self.addButton.clicked.connect(self.buttonAdd)
		
		self.removeButton = QPushButton("Remove Selected")
		self.removeButton.clicked.connect(self.buttonRemove)

		cLayout = QHBoxLayout()
		cLayout.addWidget(self.addButton)
		cLayout.addWidget(self.removeButton)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.close)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Save")


		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.ignorelist)
		finalLayout.addLayout(cLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def buttonAdd(self):
		x = AddIgnore(self)
		e = x.get_message_information(self)

		if not e: return

		self.ignorelist.addItem(e)

	def buttonRemove(self):
		i = self.ignorelist.currentRow()
		self.ignorelist.takeItem(i)


