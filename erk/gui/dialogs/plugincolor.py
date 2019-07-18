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
		text = str(self.text.text())
		

		return [text,self.forecolor,self.backcolor]

	def selectFore(self,i):
		self.forecolor = self.fore.itemText(i)

	def selectBack(self,i):
		self.backcolor = self.back.itemText(i)

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.forecolor = "00"
		self.backcolor = "None"

		self.setWindowTitle(f"Plugin.print()")
		
		self.setWindowIcon(QIcon(EDIT_ICON))

		textLayout = QHBoxLayout()
		self.textLabel = QLabel("<b>Text</b>")
		self.text = QLineEdit()

		self.text.setFixedWidth(200)

		textLayout.addWidget(self.textLabel)
		textLayout.addWidget(self.text)

		targLayout = QHBoxLayout()

		self.foreLabel = QLabel("<b>Foreground</b>")
		self.fore = QComboBox()
		self.fore.addItems([ "00", "01", "02", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"  ])
		self.fore.activated.connect(self.selectFore)

		targLayout.addWidget(self.foreLabel)
		targLayout.addWidget(self.fore)
		targLayout.addStretch()

		self.backLabel = QLabel("<b>Background</b>")
		self.back = QComboBox()
		self.back.addItems([ "None", "00", "01", "02", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"  ])
		self.back.activated.connect(self.selectBack)

		targLayout.addWidget(self.backLabel)
		targLayout.addWidget(self.back)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(textLayout)
		finalLayout.addLayout(targLayout)
		finalLayout.addStretch()
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
