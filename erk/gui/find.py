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

from erk.common import *

class Viewer(QMainWindow):

	def clickCase(self):
		if self.findCase:
			self.findCase = False
		else:
			self.findCase = True

	def clickWord(self):
		if self.wholeWord:
			self.wholeWord = False
		else:
			self.wholeWord = True

	def doSearch(self):
		self.status.setText(" ")
		self.parent.editor.removeSelection()

		if self.findCase:
			if self.wholeWord:
				options = QTextDocument.FindWholeWords | QTextDocument.FindCaseSensitively
			else:
				options = QTextDocument.FindCaseSensitively
		else:
			options = None

		sterm = self.find.text()
		if options:
			if not self.parent.editor.find(sterm,options):
				self.status.setText(f"\"{sterm}\" not found.")
		else:
			if not self.parent.editor.find(sterm):
				self.status.setText(f"\"{sterm}\" not found.")

	def doSearchBack(self):
		self.status.setText(" ")
		self.parent.editor.removeSelection()
		
		if self.findCase:
			if self.wholeWord:
				options = QTextDocument.FindWholeWords | QTextDocument.FindCaseSensitively | QTextDocument.FindBackward
			else:
				options = QTextDocument.FindCaseSensitively | QTextDocument.FindBackward
		else:
			options = QTextDocument.FindBackward

		sterm = self.find.text()

		if not self.parent.editor.find(sterm,options):
			self.status.setText(f"\"{sterm}\" not found.")

	def doClose(self):
		pass

	def closeEvent(self, event):
		if self.parent.findWindow != None:
			self.parent.findWindow = None
		if self.standalone != None:
			self.close()
			return
		self.subWindow.close()
		self.close()

	def setSubwindow(self,obj):
		self.subWindow = obj

	def __init__(self,parent=None,standalone=None):
		super(Viewer,self).__init__(parent)

		self.parent = parent
		self.standalone = standalone

		self.setWindowTitle(f"{FIND_WINDOW_TITLE}")
		self.setWindowIcon(QIcon(WHOIS_ICON))

		self.subWindow = None

		self.findCase = False
		self.wholeWord = False

		self.find = QLineEdit()

		self.status = QLabel("")
		self.status.setAlignment(Qt.AlignCenter)

		self.caseSensitive = QCheckBox("Case sensitive",self)
		self.caseSensitive.stateChanged.connect(self.clickCase)

		self.wordWhole = QCheckBox("Whole words",self)
		self.wordWhole.stateChanged.connect(self.clickWord)

		settingsLayout = QHBoxLayout()
		settingsLayout.addWidget(self.caseSensitive)
		settingsLayout.addWidget(self.wordWhole)

		doFind = QPushButton("Find Next")
		doFind.clicked.connect(self.doSearch)

		doBack = QPushButton("Find Previous")
		doBack.clicked.connect(self.doSearchBack)

		doClose = QPushButton("Close")
		doClose.clicked.connect(self.close)

		buttonsLayout = QHBoxLayout()
		buttonsLayout.addWidget(doFind)
		buttonsLayout.addWidget(doBack)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.find)
		finalLayout.addWidget(self.status)
		finalLayout.addLayout(settingsLayout)
		finalLayout.addLayout(buttonsLayout)
		finalLayout.addWidget(doClose)

		x = QWidget()
		x.setLayout(finalLayout)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		#self.setLayout(finalLayout)
		self.setCentralWidget(x)

		self.setFixedSize(finalLayout.sizeHint())

