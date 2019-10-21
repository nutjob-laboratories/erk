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
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore

from erk.common import *

class Dialog(QDialog):

	@staticmethod
	def get_user_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

	def return_info(self):

		# Save user info
		user = {
			"nickname": self.nick.text(),
			"username": self.username.text(),
			"realname": self.realname.text(),
			"alternate": self.alternative.text(),
		}
		save_user(user)

		return True

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle(f"Edit user information")
		self.setWindowIcon(QIcon(USER_ICON))

		user_info = get_user()

		# USER INFO BEGIN

		nickLayout = QHBoxLayout()
		nickLayout.addStretch()
		self.nickLabel = QLabel("Nickname  ")
		self.nick = QLineEdit(user_info["nickname"])
		nickLayout.addWidget(self.nickLabel)
		#nickLayout.addStretch()
		nickLayout.addWidget(self.nick)
		nickLayout.addStretch()

		f = self.nick.font()
		f.setBold(True)
		self.nickLabel.setFont(f)

		self.nick.setMaximumWidth( self.calculate_text_entry_size(self.nick,20)  )

		alternateLayout = QHBoxLayout()
		alternateLayout.addStretch()
		self.altLabel = QLabel("Alternate ")
		self.alternative = QLineEdit(user_info["alternate"])
		alternateLayout.addWidget(self.altLabel)
		#alternateLayout.addStretch()
		alternateLayout.addWidget(self.alternative)
		alternateLayout.addStretch()

		self.altLabel.setFont(f)

		self.alternative.setMaximumWidth( self.calculate_text_entry_size(self.alternative,20)  )

		userLayout = QHBoxLayout()
		userLayout.addStretch()
		self.userLabel = QLabel("Username  ")
		self.username = QLineEdit(user_info["username"])
		userLayout.addWidget(self.userLabel)
		#userLayout.addStretch()
		userLayout.addWidget(self.username)
		userLayout.addStretch()

		self.userLabel.setFont(f)

		self.username.setMaximumWidth( self.calculate_text_entry_size(self.username,20)  )

		realLayout = QHBoxLayout()
		realLayout.addStretch()
		self.realLabel = QLabel("Real Name ")
		self.realname = QLineEdit(user_info["realname"])
		realLayout.addWidget(self.realLabel)
		#realLayout.addStretch()
		realLayout.addWidget(self.realname)
		realLayout.addStretch()

		self.realLabel.setFont(f)

		self.realname.setMaximumWidth( self.calculate_text_entry_size(self.realname,20)  )

		nurLayout = QVBoxLayout()
		nurLayout.addLayout(nickLayout)
		nurLayout.addLayout(alternateLayout)
		nurLayout.addLayout(userLayout)
		nurLayout.addLayout(realLayout)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Save")

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nurLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def calculate_text_entry_size(self,widget,size=20):
		fm = widget.fontMetrics()
		m = widget.textMargins()
		c = widget.contentsMargins()
		w = size*fm.width('x')+m.left()+m.right()+c.left()+c.right()
		return w