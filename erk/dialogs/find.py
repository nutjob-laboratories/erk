#
#  Quirc IRC Client
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

from erk.resources import *

class Dialog(QMainWindow):

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
		#self.icount.setText(" ")

		sterm = self.find.text()
		if len(sterm.strip())==0: return

		if self.findCase:
			if self.wholeWord:
				options = QTextDocument.FindWholeWords | QTextDocument.FindCaseSensitively
			else:
				options = QTextDocument.FindCaseSensitively
		else:
			options = None

		
		if options:
			if not self.parent.editor.find(sterm,options):
				#self.status.setText(f"\"{sterm}\" not found.")
				pass
		else:
			if not self.parent.editor.find(sterm):
				#self.status.setText(f"\"{sterm}\" not found.")
				pass

		# self.icount
		f = self.parent.editor.toPlainText()
		c = f.count(sterm)
		if c>=1:
			self.icount.setText("<small>"+str(c)+" matches</small>")
			#self.icount.show()
		else:
			self.icount.setText("<small>No matches found</small>")
			#self.icount.show()

	def doSearchBack(self):
		#self.icount.setText(" ")

		sterm = self.find.text()
		if len(sterm.strip())==0: return
		
		if self.findCase:
			if self.wholeWord:
				options = QTextDocument.FindWholeWords | QTextDocument.FindCaseSensitively | QTextDocument.FindBackward
			else:
				options = QTextDocument.FindCaseSensitively | QTextDocument.FindBackward
		else:
			options = QTextDocument.FindBackward

		#sterm = self.find.text()

		if not self.parent.editor.find(sterm,options):
			#self.status.setText(f"\"{sterm}\" not found.")
			pass

		f = self.parent.editor.toPlainText()
		c = f.count(sterm)
		if c>=1:
			self.icount.setText("<small>"+str(c)+" matches</small>")
			#self.icount.show()
		else:
			self.icount.setText("<small>No matches found</small>")
			#self.icount.show()


	def doClose(self):
		pass

	def closeEvent(self, event):
		if self.parent.findWindow != None:
			del self.parent.findWindow
			self.parent.findWindow = None
		self.close()

	def setSubwindow(self,obj):
		self.subWindow = obj

	def doReplace(self):
		cursor = self.parent.editor.textCursor()
		cursor.select(QTextCursor.BlockUnderCursor)
		self.parent.editor.setTextCursor(cursor)
		if self.parent.editor.textCursor().hasSelection():
			text = self.parent.editor.textCursor().selectedText()
			cursor.beginEditBlock()
			reptext = text.replace(self.find.text(),self.replace.text())
			cursor.insertText(reptext)
			cursor.endEditBlock()
			self.doSearch()
		else:
			print("no select")

	def __init__(self,parent=None,replace=False):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Find")
		self.setWindowIcon(QIcon(WHOIS_ICON))

		self.subWindow = None

		self.findCase = False
		self.wholeWord = False

		self.find = QLineEdit()

		if replace:
			self.replace = QLineEdit()

		# self.status = QLabel("")
		# self.status.setAlignment(Qt.AlignCenter)

		self.icount = QLabel("<small>Ready</small>")
		self.icount.setAlignment(Qt.AlignCenter)
		#self.icount.hide()

		inputLayout = QVBoxLayout()
		inputLayout.addWidget(self.find)
		if replace:
			inputLayout.addWidget(self.replace)
		inputLayout.addWidget(self.icount)

		inputBox = QGroupBox()
		inputBox.setAlignment(Qt.AlignHCenter)
		inputBox.setLayout(inputLayout)

		self.caseSensitive = QCheckBox("Case sensitive",self)
		self.caseSensitive.stateChanged.connect(self.clickCase)

		self.wordWhole = QCheckBox("Whole words",self)
		self.wordWhole.stateChanged.connect(self.clickWord)

		settingsLayout = QHBoxLayout()
		settingsLayout.addWidget(self.caseSensitive)
		settingsLayout.addWidget(self.wordWhole)

		# settingsBox = QGroupBox()
		# settingsBox.setAlignment(Qt.AlignHCenter)
		# settingsBox.setLayout(settingsLayout)

		doFind = QPushButton("Find Next")
		doFind.clicked.connect(self.doSearch)

		doBack = QPushButton("Find Previous")
		doBack.clicked.connect(self.doSearchBack)

		if replace:
			doReplace = QPushButton("Replace")
			doReplace.clicked.connect(self.doReplace)

		doClose = QPushButton("Close")
		doClose.clicked.connect(self.close)

		buttonsLayout = QHBoxLayout()
		buttonsLayout.addWidget(doFind)
		buttonsLayout.addWidget(doBack)
		if replace:
			buttonsLayout.addWidget(doReplace)

		# buttonBox = QGroupBox()
		# buttonBox.setAlignment(Qt.AlignHCenter)
		# buttonBox.setLayout(buttonsLayout)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(inputBox)
		# finalLayout.addWidget(self.find)
		# if replace:
		# 	finalLayout.addWidget(self.replace)
		# finalLayout.addWidget(self.icount)
		finalLayout.addLayout(settingsLayout)
		#finalLayout.addWidget(settingsBox)
		finalLayout.addLayout(buttonsLayout)
		#finalLayout.addWidget(buttonBox)
		finalLayout.addWidget(doClose)

		x = QWidget()
		x.setLayout(finalLayout)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		#self.setLayout(finalLayout)
		self.setCentralWidget(x)

		self.setFixedSize(finalLayout.sizeHint())

