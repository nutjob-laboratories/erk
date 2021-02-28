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

import os

from ..resources import *
from ..strings import *
from ..files import *

class Dialog(QDialog):

	@staticmethod
	def get_install_information(nick,parent=None):
		dialog = Dialog(nick,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		if self.is_plugin:
			return True
		else:
			return False

	def __init__(self,nick,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.file = nick
		self.is_plugin = True

		self.setWindowTitle("Install plugin")
		self.setWindowIcon(QIcon(INSTALL_ICON))

		file_name, file_extension = os.path.splitext(self.file)

		if file_extension.lower()==f".{PACKAGE_FILE_EXTENSION}":
			packs = get_plugin_info(self.file)

			if len(packs)>1:
				self.title = QLabel("The following plugins will be installed:")
				self.packlist = QListWidget(self)
				for x in packs:
					item = QListWidgetItem(x)
					self.packlist.addItem(item)
			elif len(packs)==1:
				self.title = QLabel(F"The plugin \"{packs.pop(0)}\" will be installed.")
				self.packlist = QLabel('')
			else:
				self.is_plugin = False
				self.title = QLabel("No plugins found.")
				self.packlist = QLabel('')

		elif file_extension.lower()==".py":
			self.is_plugin = True
			bfile = os.path.basename(self.file)
			self.title = QLabel(F"The plugin \"{bfile}\" will be installed.")
			self.packlist = QLabel('')

		else:
			self.is_plugin = False
			self.title = QLabel("No plugins found.")
			self.packlist = QLabel('')

		nameLayout = QVBoxLayout()
		nameLayout.addWidget(self.title)
		nameLayout.addWidget(self.packlist)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
