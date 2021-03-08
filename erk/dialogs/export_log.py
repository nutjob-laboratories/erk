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
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from ..resources import *

class Dialog(QDialog):

	@staticmethod
	def get_name_information(logdir,parent=None,app=None):
		dialog = Dialog(logdir,parent,app)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		item = self.packlist.currentItem()
		if item:
			retval = [item.file,self.delimiter,self.linedelim, self.do_json, self.epoch]
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("No log selected")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		return retval


	def clickTime(self,state):
		if state == Qt.Checked:
			self.epoch = True
		else:
			self.epoch = False

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

	def closeEvent(self, event):

		if self.app != None:
			self.app.quit()

		event.accept()
		self.close()

	def __init__(self,logdir,parent=None,app=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.logdir = logdir
		self.app = None
		self.delimiter = "\t"
		self.linedelim = "\n"

		self.do_json = True
		self.epoch = False

		self.setWindowTitle("Export log")
		self.setWindowIcon(QIcon(LOG_ICON))

		self.title = QLabel("<b>Select a log to export</b>")

		self.packlist = QListWidget(self)

		for x in os.listdir(self.logdir):
			if x.endswith(".json"):
				log = os.path.join(self.logdir, x)
				if os.path.isfile(log):
					p = os.path.basename(log).replace('.json','')
					p = p.split('-')
					if len(p)==2:
						netname = p[0]
						channel = p[1]

						netname = netname.upper()

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

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Save")

		titleLayout = QHBoxLayout()
		titleLayout.addStretch()
		titleLayout.addWidget(self.title)
		titleLayout.addStretch()

		self.time = QCheckBox("Epoch format for date/time ",self)
		self.time.stateChanged.connect(self.clickTime)
		self.time.toggle()

		f = self.time.font()
		f.setBold(True)
		self.time.setFont(f)

		self.time.setLayoutDirection(Qt.RightToLeft)

		self.menubar = QMenuBar(self)
		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)
		self.menubar.setFont(BOLD_FONT)
		self.menubar.setStyleSheet(f"QMenuBar {{ background-color:transparent;  }}")


		fileMenu = self.menubar.addMenu ("Export As...")

		self.menuJson = QAction(QIcon(RCHECKED_ICON),"JSON",self)
		self.menuJson.triggered.connect(lambda state,s="json": self.toggleSetting(s))
		fileMenu.addAction(self.menuJson)

		self.menuText = QAction(QIcon(RUNCHECKED_ICON),"Text",self)
		self.menuText.triggered.connect(lambda state,s="text": self.toggleSetting(s))
		fileMenu.addAction(self.menuText)

		self.format = QLabel("JSON file")
		self.format.setFont(BOLD_FONT)

		self.type.setVisible(False)
		self.typeLabel.setVisible(False)
		self.line.setVisible(False)
		self.lineLabel.setVisible(False)

		formatLayout = QHBoxLayout()
		formatLayout.addWidget(self.menubar)
		formatLayout.addWidget(self.format)

		finalLayout = QVBoxLayout()
		
		finalLayout.addLayout(titleLayout)
		finalLayout.addWidget(self.packlist)
		finalLayout.addLayout(formatLayout)
		finalLayout.addLayout(delimLayout)
		finalLayout.addWidget(self.time)
		
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def toggleSetting(self,setting):

		if setting=='json':
			self.menuJson.setIcon(QIcon(RCHECKED_ICON))
			self.menuText.setIcon(QIcon(RUNCHECKED_ICON))
			self.do_json = True
			self.type.setVisible(False)
			self.typeLabel.setVisible(False)
			self.line.setVisible(False)
			self.lineLabel.setVisible(False)
			self.format.setText("JSON file")
			return

		if setting=='text':
			self.menuJson.setIcon(QIcon(RUNCHECKED_ICON))
			self.menuText.setIcon(QIcon(RCHECKED_ICON))
			self.do_json = False
			self.type.setVisible(True)
			self.typeLabel.setVisible(True)
			self.line.setVisible(True)
			self.lineLabel.setVisible(True)
			self.format.setText("ASCII text file")
			return
