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

import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from ..resources import *

INSTALL_DIRECTORY = sys.path[0]
PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")

def get_package_name(pack):
	pname = os.path.join(pack, "package.txt")
	if os.path.isfile(pname):
		f=open(pname, "r")
		package_name = f.read()
		f.close()
		return package_name
	return None

def get_package_icon(pack):
	pname = os.path.join(pack, "package.png")
	if os.path.isfile(pname):
		return pname
	return None


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

		item = self.packlist.currentItem()
		if item:
			retval = item.file
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("No plugin package selected")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Export plugin")
		self.setWindowIcon(QIcon(ARCHIVE_ICON))

		self.title = QLabel("<center><b>Select a plugin to export</b></center>")

		self.packlist = QListWidget(self)
		self.packlist.setMaximumHeight(100)

		for x in os.listdir(PLUGIN_DIRECTORY):
			if x.lower()=="__pycache__": continue
			pack = os.path.join(PLUGIN_DIRECTORY, x)
			if os.path.isdir(pack):

				pack_name = get_package_name(pack)
				if pack_name==None: pack_name = x

				pack_icon = get_package_icon(pack)
				if pack_icon==None: pack_icon = PACKAGE_ICON

				has_parent_gui = False
				if hasattr(self.parent,"gui"):
					if hasattr(self.parent.gui,"plugins"):
						has_parent_gui= True

				if has_parent_gui:
					if x in self.parent.gui.plugins.failed_load:
						item = QListWidgetItem(pack_name+" (Error loading)")
						item.setIcon(QIcon(ERROR_ICON))
					else:
						item = QListWidgetItem(pack_name)
						item.setIcon(QIcon(pack_icon))
					item.file = pack
					self.packlist.addItem(item)
				else:
					item = QListWidgetItem(pack_name)
					item.file = pack
					item.setIcon(QIcon(pack_icon))
					self.packlist.addItem(item)

			elif os.path.isfile(pack):
				if has_parent_gui:
					if x in self.parent.gui.plugins.failed_load:
						item = QListWidgetItem(pack_name+" (Error loading)")
						item.setIcon(QIcon(ERROR_ICON))
					else:
						item = QListWidgetItem(x)
						item.setIcon(QIcon(PLUGIN_ICON))
					item.file = pack
					self.packlist.addItem(item)
				else:
					item = QListWidgetItem(x)
					item.file = pack
					item.setIcon(QIcon(PLUGIN_ICON))
					self.packlist.addItem(item)


		self.packlist.setCurrentRow(0)


		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Export")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.title)
		finalLayout.addWidget(self.packlist)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
