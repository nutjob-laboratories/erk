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

	def setArgcount(self):
		index = self.argcount.currentIndex()

		c = self.argcount.currentText()
		if c == 'Any': c = '*'

		self.args = c

	@staticmethod
	def get_macro_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = [self.name.text(),self.args,self.message.text(),self.help.text(),self.argsDesc.text()]

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.args = "0"

		self.setWindowTitle("New Macro")
		self.setWindowIcon(QIcon(CHANNEL_ICON))

		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDABCDEFGHIJ")

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("Name")
		self.name = QLineEdit()
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addWidget(self.name)
		nameLayout.addStretch()


		self.argcount = QComboBox(self)
		self.argcount.activated.connect(self.setArgcount)

		self.argcount.addItem("0")
		self.argcount.addItem("Any")
		self.argcount.addItem("1")
		self.argcount.addItem("2")
		self.argcount.addItem("3")
		self.argcount.addItem("4")
		self.argcount.addItem("5")
		self.argcount.addItem("6")
		self.argcount.addItem("7")
		self.argcount.addItem("8")
		self.argcount.addItem("9")
		self.argcount.addItem("10")

		# argsLayout = QHBoxLayout()
		# self.argsLabel = QLabel("# of arguments")
		# argsLayout.addWidget(self.argsLabel)
		# argsLayout.addStretch()
		# argsLayout.addWidget(self.argcount)

		self.argsLabel = QLabel("# of arguments")
		nameLayout.addWidget(self.argsLabel)
		nameLayout.addWidget(self.argcount)
		nameLayout.addStretch()


		messageLayout = QHBoxLayout()
		self.messageLabel = QLabel("Message")
		self.message = QLineEdit()
		#self.message.setPlaceholderText("Type your comment here")
		self.message.setMinimumWidth(wwidth)
		messageLayout.addWidget(self.messageLabel)
		messageLayout.addStretch()
		messageLayout.addWidget(self.message)

		helpLayout = QHBoxLayout()
		self.helpLabel = QLabel("Help text")
		self.help = QLineEdit()
		self.help.setPlaceholderText("Macro help text")
		self.help.setMinimumWidth(wwidth)
		helpLayout.addWidget(self.helpLabel)
		helpLayout.addStretch()
		helpLayout.addWidget(self.help)

		argdescLayout = QHBoxLayout()
		self.argsDescLabel = QLabel("Arguments")
		self.argsDesc = QLineEdit()
		self.argsDesc.setPlaceholderText("Macro argument description")
		self.argsDesc.setMinimumWidth(wwidth)
		argdescLayout.addWidget(self.argsDescLabel)
		argdescLayout.addStretch()
		argdescLayout.addWidget(self.argsDesc)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		#finalLayout.addLayout(argsLayout)
		finalLayout.addLayout(messageLayout)
		finalLayout.addLayout(helpLayout)
		finalLayout.addLayout(argdescLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
