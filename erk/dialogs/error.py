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

class Dialog(QDialog):


	def __init__(self,errlist,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Plugin load errors")
		self.setWindowIcon(QIcon(ERROR_ICON))

		errTree = QTreeWidget()
		errTree.headerItem().setText(0,"1")
		errTree.header().setVisible(False)

		root = errTree.invisibleRootItem()

		counter = 0
		for e in errlist:
			counter = counter + len(e.errors)

		if len(errlist)>1:
			p = "plugins"
		else:
			p = "plugin"

		dlable = QLabel( str(len(errlist)) + " "+ p +" not loaded ("+ str(counter) + " errors)"  )

		for pack in errlist:
			parent = QTreeWidgetItem(root)
			parent.setText(0,"Plugin \""+pack.class_name()+"\"")
			parent.setIcon(0,QIcon(PLUGIN_MENU_ICON))

			parent.setExpanded(True)

			for c in pack.errors:
				uncle = QTreeWidgetItem(parent)
				uncle.setText(0,c)
				uncle.setExpanded(True)
				uncle.setIcon(0,QIcon(ERROR_ICON))
				#uncle.setIcon(0,QIcon(PLUGIN_ICON))
				# for e in c:
				# 	child = QTreeWidgetItem(uncle)
				# 	child.setText(0,e)
				# 	child.setIcon(0,QIcon(ERROR_ICON))


		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)

		buttons.button(QDialogButtonBox.Ok).setText("Ok")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(dlable)
		finalLayout.addWidget(errTree)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
