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
			retval = [item.file,self.delimiter,self.linedelim, self.do_json]
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("No log selected")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		return retval

	def clickJson(self,state):
		if state == Qt.Checked:
			self.do_json = True
			self.line.setEnabled(False)
			self.type.setEnabled(False)
			self.lineLabel.setEnabled(False)
			self.typeLabel.setEnabled(False)
		else:
			self.do_json = False
			self.line.setEnabled(True)
			self.type.setEnabled(True)
			self.lineLabel.setEnabled(True)
			self.typeLabel.setEnabled(True)


	def setLine(self):

		dtype = self.line.itemText(self.line.currentIndex())
		if dtype=='Newline': self.linedelim = "\n"
		if dtype=='CRLF': self.linedelim = "\r\n"
		if dtype=='Tab': self.linedelim = "\t"
		if dtype=='Comma': self.linedelim = ","
		if dtype=='Pipe': self.linedelim = "|"

	def setType(self):

		dtype = self.type.itemText(self.type.currentIndex())
		if dtype=='Space': self.delimiter = ' '
		if dtype=='Double Space': self.delimiter = '  '
		if dtype=='Tab': self.delimiter = "\t"
		if dtype=='Comma': self.delimiter = ','
		if dtype=='Colon': self.delimiter = ':'
		if dtype=='Double Colon': self.delimiter = '::'
		if dtype=='Pipe': self.delimiter = '|'
		if dtype=='Double Pipe': self.delimiter = '||'

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.delimiter = "\t"
		self.linedelim = "\n"

		self.do_json = False

		self.setWindowTitle("Export log")
		self.setWindowIcon(QIcon(LOG_ICON))

		self.title = QLabel("Select a log to export")

		self.packlist = QListWidget(self)
		self.packlist.setMaximumHeight(100)

		for x in os.listdir(LOG_DIRECTORY):
			if x.endswith(".json"):
				log = os.path.join(LOG_DIRECTORY, x)
				if os.path.isfile(log):
					p = os.path.basename(log).replace('.json','')
					p = p.split('-')
					if len(p)==2:
						netname = p[0]
						channel = p[1]

						item = QListWidgetItem(channel+" ("+netname+")")
						item.file = log
						self.packlist.addItem(item)

		delimLayout = QFormLayout()

		self.type = QComboBox(self)
		self.type.activated.connect(self.setType)
		self.type.addItem("Tab")
		self.type.addItem("Space")
		self.type.addItem("Double Space")
		self.type.addItem("Comma")
		self.type.addItem("Colon")
		self.type.addItem("Double Colon")
		self.type.addItem("Pipe")
		self.type.addItem("Double Pipe")

		self.typeLabel = QLabel("<b>Field Delimiter</b>")
		delimLayout.addRow(self.typeLabel, self.type)

		self.line = QComboBox(self)
		self.line.activated.connect(self.setLine)
		self.line.addItem("Newline")
		self.line.addItem("CRLF")
		self.line.addItem("Tab")
		self.line.addItem("Comma")
		self.line.addItem("Pipe")

		self.lineLabel = QLabel("<b>Entry Delimiter</b>")
		delimLayout.addRow(self.lineLabel, self.line)

		self.json = QCheckBox(self)
		self.json.stateChanged.connect(self.clickJson)

		delimLayout.addRow(QLabel("<b>Export as JSON</b>"), self.json)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Export")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.title)
		finalLayout.addWidget(self.packlist)
		finalLayout.addLayout(delimLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
