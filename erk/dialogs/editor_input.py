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
from ..strings import *

class Dialog(QDialog):

	@staticmethod
	def get_string_information(title,prompt,twoinputs,twoprompt,parent=None):
		dialog = Dialog(title,prompt,twoinputs,twoprompt,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		if self.twoinputs:
			retval = [self.name.text(),self.two.text()]
		else:
			retval = self.name.text()

		return retval

	def __init__(self,title,prompt,twoinputs=False,twoprompt='',parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.twoinputs = twoinputs

		self.setWindowTitle(title)
		self.setWindowIcon(QIcon(ERK_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("<b>"+prompt+"</b>")
		self.name = QLineEdit()
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addStretch()
		nameLayout.addWidget(self.name)

		if twoinputs:
			twoLayout = QHBoxLayout()
			self.twoLabel = QLabel("<b>"+twoprompt+"</b>")
			self.two = QLineEdit()
			twoLayout.addWidget(self.twoLabel)
			twoLayout.addStretch()
			twoLayout.addWidget(self.two)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		if twoinputs:
			finalLayout.addLayout(twoLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
