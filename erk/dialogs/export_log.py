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

from erk.resources import *

INSTALL_DIRECTORY = sys.path[0]
LOG_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "logs")

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
			msg.setInformativeText("No log selected")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Export log")
		self.setWindowIcon(QIcon(LOG_ICON))

		self.title = QLabel("Select a log to export")

		self.packlist = QListWidget(self)
		self.packlist.setMaximumHeight(100)

		for x in os.listdir(LOG_DIRECTORY):
			log = os.path.join(LOG_DIRECTORY, x)
			if os.path.isfile(log):
				p = os.path.basename(log).replace('.json','')
				p = p.split('-')
				netname = p[0]
				channel = p[1]

				item = QListWidgetItem(channel+" ("+netname+")")
				item.file = log
				#item.setIcon(QIcon(LOG_ICON))
				self.packlist.addItem(item)

		# for x in os.listdir(PLUGIN_DIRECTORY):
			# if x.lower()=="__pycache__": continue
			# pack = os.path.join(PLUGIN_DIRECTORY, x)
			# if os.path.isdir(pack):

		# 		has_parent_gui = False
		# 		if hasattr(self.parent,"gui"):
		# 			if hasattr(self.parent.gui,"plugins"):
		# 				has_parent_gui= True

		# 		if has_parent_gui:
		# 			if x in self.parent.gui.plugins.failed_load:
		# 				item = QListWidgetItem(x+" (Error loading)")
		# 				item.setIcon(QIcon(ERROR_ICON))
		# 			else:
		# 				item = QListWidgetItem(x)
		# 				item.setIcon(QIcon(PACKAGE_ICON))
		# 			item.file = pack
		# 			self.packlist.addItem(item)
		# 		else:
		# 			item = QListWidgetItem(x)
		# 			item.file = pack
		# 			item.setIcon(QIcon(PACKAGE_ICON))
		# 			self.packlist.addItem(item)


		# self.packlist.setCurrentRow(0)


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
