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

class QColorButton(QPushButton):

	colorChanged = pyqtSignal(list)

	def __init__(self,cname,parent=None):
		super(QColorButton,self).__init__(parent)

		self.parent = parent
		self.cname = cname
		self.color = self.parent.display[cname]
		self.setMaximumWidth(32)
		self.setStyleSheet(f"background-color: {self.color};")
		self.pressed.connect(self.picker)

	def picker(self):
		color = QColorDialog.getColor(QColor(self.color))

		if color.isValid():
			self.color = color.name()
			self.setStyleSheet(f"background-color: {self.color};")
			self.colorChanged.emit( [self.cname,self.color] )

class Dialog(QDialog):

	@staticmethod
	def get_color_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_dict()
		return None

	def return_dict(self):
		#retval = str(self.name.text())
		#return retval
		return self.display

	def applyColors(self,text,display):

		text = text.replace(SYSTEM_COLOR,display["system"])
		text = text.replace(SELF_COLOR,display["self"])
		text = text.replace(USER_COLOR,display["user"])
		text = text.replace(ACTION_COLOR,display["action"])
		text = text.replace(NOTICE_COLOR,display["notice"])
		text = text.replace(ERROR_COLOR,display["error"])
		text = text.replace(HIGHLIGHT_COLOR,display["highlight"])
		text = text.replace(LINK_COLOR,display["link"])

		return text

	def updateText(self):

		nlen = len("your_nickname") + 2
		sysmsg = systemTextDisplay("Example system message",0,SYSTEM_COLOR)
		selfmsg = chat_display("your_nickname","Example chat message.",nlen,False,SELF_COLOR)
		othermsg = chat_display("user","Example chat message",nlen,False,USER_COLOR)
		noticemsg = notice_display("notice_sender","Example notice message.",nlen,False,NOTICE_COLOR)
		actionmsg = action_display("user","sends an example CTCP action.",False,ACTION_COLOR,False,HIGHLIGHT_COLOR,"none")
		errormsg = systemTextDisplay("Example error message",0,ERROR_COLOR)
		highlightmsg = "<font color=\"" + HIGHLIGHT_COLOR + "\"><b>Highlighted text.</b></font>"
		linkmsg = "<font color=\"" + LINK_COLOR + "\"><u><b>https://www.google.com</b></u></font>"

		return [selfmsg,othermsg,noticemsg,actionmsg,sysmsg,errormsg,highlightmsg,linkmsg]

	def doDisplay(self):
		self.textDisplay.clear()

		#self.textDisplay.append("<h3>Example text</h3>")

		for e in self.updateText():
			t = self.applyColors(e,self.display)
			self.textDisplay.append(t)

	def doColorChange(self,data):
		self.display[data[0]] = data[1]
		self.doDisplay()

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.display = self.parent.display

		self.setWindowTitle(f"Set text colors")
		self.setWindowIcon(QIcon(COLOR_ICON))

		self.textDisplay = QTextEdit()
		self.textDisplay.setReadOnly(True)
		self.textDisplay.setMinimumWidth(300)
		self.textDisplay.setMinimumHeight(150)
		self.doDisplay()


		systemEntry = QHBoxLayout()
		systemLabel = QLabel("System Messages")
		systemButton = QColorButton("system",self)
		systemButton.colorChanged.connect(self.doColorChange)
		systemEntry.addWidget(systemLabel)
		systemEntry.addWidget(systemButton)

		selfEntry = QHBoxLayout()
		selfLabel = QLabel("Your nickname")
		selfButton = QColorButton("self",self)
		selfButton.colorChanged.connect(self.doColorChange)
		selfEntry.addWidget(selfLabel)
		selfEntry.addWidget(selfButton)

		userEntry = QHBoxLayout()
		userLabel = QLabel("Other nicknames")
		userButton = QColorButton("user",self)
		userButton.colorChanged.connect(self.doColorChange)
		userEntry.addWidget(userLabel)
		userEntry.addWidget(userButton)

		actionEntry = QHBoxLayout()
		actionLabel = QLabel("CTCP Actions")
		actionButton = QColorButton("action",self)
		actionButton.colorChanged.connect(self.doColorChange)
		actionEntry.addWidget(actionLabel)
		actionEntry.addWidget(actionButton)

		columnOne = QVBoxLayout()
		columnOne.addLayout(systemEntry)
		columnOne.addLayout(selfEntry)
		columnOne.addLayout(userEntry)
		columnOne.addLayout(actionEntry)

		noticeEntry = QHBoxLayout()
		noticeLabel = QLabel("Notices")
		noticeButton = QColorButton("notice",self)
		noticeButton.colorChanged.connect(self.doColorChange)
		noticeEntry.addWidget(noticeLabel)
		noticeEntry.addWidget(noticeButton)

		errorEntry = QHBoxLayout()
		errorLabel = QLabel("Errors")
		errorButton = QColorButton("error",self)
		errorButton.colorChanged.connect(self.doColorChange)
		errorEntry.addWidget(errorLabel)
		errorEntry.addWidget(errorButton)

		highlightEntry = QHBoxLayout()
		highlightLabel = QLabel("Highlights")
		highlightButton = QColorButton("highlight",self)
		highlightButton.colorChanged.connect(self.doColorChange)
		highlightEntry.addWidget(highlightLabel)
		highlightEntry.addWidget(highlightButton)

		linkEntry = QHBoxLayout()
		linkLabel = QLabel("Hyperlinks")
		linkButton = QColorButton("link",self)
		linkButton.colorChanged.connect(self.doColorChange)
		linkEntry.addWidget(linkLabel)
		linkEntry.addWidget(linkButton)

		columnTwo = QVBoxLayout()
		columnTwo.addLayout(noticeEntry)
		columnTwo.addLayout(errorEntry)
		columnTwo.addLayout(highlightEntry)
		columnTwo.addLayout(linkEntry)

		colorButtons = QHBoxLayout()
		colorButtons.addLayout(columnOne)
		colorButtons.addStretch()
		colorButtons.addLayout(columnTwo)

		colorBox = QGroupBox("Select Colors",self)
		colorBox.setLayout(colorButtons)

		topLayout = QHBoxLayout()
		topLayout.addWidget(self.textDisplay)

		textBox = QGroupBox(self)
		textBox.setLayout(topLayout)

		mainLayout = QVBoxLayout()
		#mainLayout.addWidget(self.textDisplay)
		mainLayout.addWidget(textBox)
		# mainLayout.addLayout(colorButtons)
		mainLayout.addWidget(colorBox)


		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()

		finalLayout.addLayout(mainLayout)
		#finalLayout.addWidget(QLabel(" "))
		finalLayout.addStretch()
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
