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
		if c == 'None': c = '0'
		if c == 'One': c = '1'
		if c == 'Two': c = '2'
		if c == 'Three': c = '3'
		if c == 'Four': c = '4'
		if c == 'Five': c = '5'
		if c == 'Six': c = '6'
		if c == 'Seven': c = '7'
		if c == 'Eight': c = '8'
		if c == 'Nine': c = '9'
		if c == 'Ten': c = '10'

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
		self.name.setMinimumWidth(wwidth)
		self.name.setPlaceholderText("Macro name, callable with /NAME")
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addStretch()
		nameLayout.addWidget(self.name)


		self.argcount = QComboBox(self)
		self.argcount.activated.connect(self.setArgcount)

		self.argcount.addItem("None")
		self.argcount.addItem("Any")
		self.argcount.addItem("One")
		self.argcount.addItem("Two")
		self.argcount.addItem("Three")
		self.argcount.addItem("Four")
		self.argcount.addItem("Five")
		self.argcount.addItem("Six")
		self.argcount.addItem("Seven")
		self.argcount.addItem("Eight")
		self.argcount.addItem("Nine")
		self.argcount.addItem("Ten")

		# argsLayout = QHBoxLayout()
		# self.argsLabel = QLabel("# of arguments")
		# argsLayout.addWidget(self.argsLabel)
		# argsLayout.addStretch()
		# argsLayout.addWidget(self.argcount)

		self.argsLabel = QLabel("Number of arguments ")

		argsLayout = QHBoxLayout()

		argsLayout.addWidget(self.argsLabel)
		#argsLayout.addStretch()
		argsLayout.addWidget(self.argcount)
		argsLayout.addStretch()


		messageLayout = QHBoxLayout()
		self.messageLabel = QLabel("Output")
		self.message = QLineEdit()
		self.message.setPlaceholderText("Macro output")
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
		self.argsDescLabel = QLabel("Argument description")
		self.argsDesc = QLineEdit()
		self.argsDesc.setPlaceholderText("Macro argument description")
		self.argsDesc.setMinimumWidth(wwidth)
		argdescLayout.addWidget(self.argsDescLabel)
		argdescLayout.addStretch()
		argdescLayout.addWidget(self.argsDesc)


		

		allArgs = QLabel("<small><b>&+</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;All arguments to macro</small>")
		
		nicks = QLabel("<small><b>$NICK</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Current nickname</small>") 
		username = QLabel("<small><b>$USERNAME</b>&nbsp;&nbsp;&nbsp;&nbsp;Current username</small>") 
		realname = QLabel("<small><b>$REALNAME</b>&nbsp;&nbsp;&nbsp;&nbsp;Current realname</small>")

		hostname = QLabel("<small><b>$HOSTNAME</b>&nbsp;&nbsp;&nbsp;&nbsp;Server's hostname</small>")

		columnOne = QVBoxLayout()
		columnOne.addWidget(allArgs)
		
		columnOne.addWidget(nicks)
		columnOne.addWidget(username)
		columnOne.addWidget(realname)
		columnOne.addWidget(hostname)


		mostArgs = QLabel("<small><b>&-</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;All arguments except the first</small>") 
		ip = QLabel("<small><b>$SERVER</b>&nbsp;&nbsp;Server's connection address</small>")
		port = QLabel("<small><b>$PORT</b>&nbsp;&nbsp;&nbsp;&nbsp;Server's connection port</small>")
		where = QLabel("<small><b>$WHERE</b>&nbsp;&nbsp;&nbsp;Calling channel/nickname</small>")


		columnTwo = QVBoxLayout()
		columnTwo.addWidget(mostArgs)
		columnTwo.addWidget(ip)
		columnTwo.addWidget(port)
		columnTwo.addWidget(where)
		columnTwo.addWidget(QLabel(' '))

		aliasLayout = QHBoxLayout()
		aliasLayout.addLayout(columnOne)
		aliasLayout.addLayout(columnTwo)


		infoBox = QGroupBox("Special Aliases",self)
		infoBox.setLayout(aliasLayout)

		infoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")





		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		finalLayout.addLayout(argsLayout)
		finalLayout.addLayout(messageLayout)
		finalLayout.addLayout(helpLayout)
		finalLayout.addLayout(argdescLayout)

		finalLayout.addWidget(infoBox)

		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
