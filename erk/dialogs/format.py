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

from erk.resources import *
from erk.files import *
import erk.format

def get_style_attribute(style,setting):

	for e in style.split(';'):
		e = e.strip()
		p = e.split(':')
		if len(p)==2:
			p[0] = p[0].strip()
			p[1] = p[1].strip()

			if p[0].lower()==setting.lower():
				return p[1]
	return None

class Dialog(QDialog):

	def resetStyles(self):
		self.styles = get_text_format_settings(BACKUP_STYLE_FILE)
		self.system.setStyleSheet(self.styles["system"])
		self.action.setStyleSheet(self.styles["action"])
		self.errormsg.setStyleSheet(self.styles["error"])
		self.hyperlink.setStyleSheet(self.styles["hyperlink"])
		self.backgroundcolor.setStyleSheet(self.styles["all"])
		self.selfuser.setStyleSheet(self.styles["self"])
		self.username.setStyleSheet(self.styles["username"])
		self.noticename.setStyleSheet(self.styles["notice"])

	def closeEvent(self,event):
		event.accept()

	def apply(self):
		erk.format.STYLES = self.styles

		self.parent.newStyle(self.styles["all"])

		self.parent.reload_all_text()
		self.close()
		

	def save(self):
		erk.format.STYLES = self.styles

		self.parent.newStyle(self.styles["all"])

		self.parent.reload_all_text()

		write_style_file(self.styles)

		self.close()

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Colors")
		self.setWindowIcon(QIcon(FORMAT_ICON))

		self.styles = get_text_format_settings()

		# System message settings

		c = get_style_attribute(self.styles["system"],"color")
		s = get_style_attribute(self.styles["system"],"font-style")
		w = get_style_attribute(self.styles["system"],"font-weight")
		b = get_style_attribute(self.styles["system"],"background-color")
		u = get_style_attribute(self.styles["system"],"text-decoration")

		self.system = QLabel("This is a system message")
		self.system.setStyleSheet(self.styles["system"])

		setColor = QPushButton("Color")
		setColor.clicked.connect(lambda state,u="system",t="system",o=self.system: self.get_color(u,t,o))

		setBold = QCheckBox("Bold",self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="system",t="system",o=self.system: self.toggle_bold(u,t,o))

		setItalic = QCheckBox("Italic",self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="system",t="system",o=self.system: self.toggle_italic(u,t,o))

		systemFormatLayout = QHBoxLayout()
		systemFormatLayout.addWidget(setColor)
		systemFormatLayout.addWidget(setBold)
		systemFormatLayout.addWidget(setItalic)

		sysSelector = QVBoxLayout()
		sysSelector.addWidget(self.system)
		sysSelector.addLayout(systemFormatLayout)

		systemBox = QGroupBox()
		systemBox.setAlignment(Qt.AlignHCenter)
		systemBox.setLayout(sysSelector)

		# Action message settings

		c = get_style_attribute(self.styles["action"],"color")
		s = get_style_attribute(self.styles["action"],"font-style")
		w = get_style_attribute(self.styles["action"],"font-weight")
		b = get_style_attribute(self.styles["action"],"background-color")
		u = get_style_attribute(self.styles["action"],"text-decoration")

		self.action = QLabel("This is a CTCP action message")
		self.action.setStyleSheet(self.styles["action"])

		setColor = QPushButton("Color")
		setColor.clicked.connect(lambda state,u="action",t="action",o=self.action: self.get_color(u,t,o))

		setBold = QCheckBox("Bold",self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="action",t="action",o=self.action: self.toggle_bold(u,t,o))

		setItalic = QCheckBox("Italic",self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="action",t="action",o=self.action: self.toggle_italic(u,t,o))	

		actionFormatLayout = QHBoxLayout()
		actionFormatLayout.addWidget(setColor)
		actionFormatLayout.addWidget(setBold)
		actionFormatLayout.addWidget(setItalic)

		actSelector = QVBoxLayout()
		actSelector.addWidget(self.action)
		actSelector.addLayout(actionFormatLayout)

		actionBox = QGroupBox()
		actionBox.setAlignment(Qt.AlignHCenter)
		actionBox.setLayout(actSelector)

		# Error message settings

		c = get_style_attribute(self.styles["error"],"color")
		s = get_style_attribute(self.styles["error"],"font-style")
		w = get_style_attribute(self.styles["error"],"font-weight")
		b = get_style_attribute(self.styles["error"],"background-color")

		self.errormsg = QLabel("This is an error message")
		self.errormsg.setStyleSheet(self.styles["error"])

		setColor = QPushButton("Color")
		setColor.clicked.connect(lambda state,u="error",t="error",o=self.errormsg: self.get_color(u,t,o))

		setBold = QCheckBox("Bold",self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="error",t="error",o=self.errormsg: self.toggle_bold(u,t,o))

		setItalic = QCheckBox("Italic",self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="error",t="error",o=self.errormsg: self.toggle_italic(u,t,o))		

		errorFormatLayout = QHBoxLayout()
		errorFormatLayout.addWidget(setColor)
		errorFormatLayout.addWidget(setBold)
		errorFormatLayout.addWidget(setItalic)

		errSelector = QVBoxLayout()
		errSelector.addWidget(self.errormsg)
		errSelector.addLayout(errorFormatLayout)

		errorBox = QGroupBox()
		errorBox.setAlignment(Qt.AlignHCenter)
		errorBox.setLayout(errSelector)

		# Hyperlink settings

		c = get_style_attribute(self.styles["hyperlink"],"color")
		s = get_style_attribute(self.styles["hyperlink"],"font-style")
		w = get_style_attribute(self.styles["hyperlink"],"font-weight")
		b = get_style_attribute(self.styles["hyperlink"],"background-color")

		self.hyperlink = QLabel("This is a hyperlink")
		self.hyperlink.setStyleSheet(self.styles["hyperlink"])

		setColor = QPushButton("Color")
		setColor.clicked.connect(lambda state,u="link",t="hyperlink",o=self.hyperlink: self.get_color(u,t,o))

		setBold = QCheckBox("Bold",self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="link",t="hyperlink",o=self.hyperlink: self.toggle_bold(u,t,o))

		setItalic = QCheckBox("Italic",self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="link",t="hyperlink",o=self.hyperlink: self.toggle_italic(u,t,o))	

		linkFormatLayout = QHBoxLayout()
		linkFormatLayout.addWidget(setColor)
		linkFormatLayout.addWidget(setBold)
		linkFormatLayout.addWidget(setItalic)

		urlSelector = QVBoxLayout()
		urlSelector.addWidget(self.hyperlink)
		urlSelector.addLayout(linkFormatLayout)

		hyperlinkBox = QGroupBox()
		hyperlinkBox.setAlignment(Qt.AlignHCenter)
		hyperlinkBox.setLayout(urlSelector)


		# Foreground/background settings

		c = get_style_attribute(self.styles["all"],"background-color")
		t = get_style_attribute(self.styles["all"],"color")
		self.backgroundcolor = QTextEdit()
		self.backgroundcolor.setReadOnly(True)
		self.backgroundcolor.append("Lorem ipsum dolor sit amet")
		self.backgroundcolor.setStyleSheet(self.styles["all"])

		fm = self.backgroundcolor.fontMetrics()
		h = fm.height() + 12
		self.backgroundcolor.setFixedHeight(h)

		setColor = QPushButton("Background color")
		setColor.clicked.connect(lambda state,u="all",t="all",o=self.backgroundcolor: self.get_bgcolor(u,t,o))

		fsetColor = QPushButton("Text color")
		fsetColor.clicked.connect(lambda state,u="all",t="all",o=self.backgroundcolor: self.get_color(u,t,o))

		backColorLayout = QHBoxLayout()
		backColorLayout.addWidget(self.backgroundcolor)
		backColorLayout.addWidget(setColor)
		backColorLayout.addWidget(fsetColor)

		backgroundBox = QGroupBox()
		backgroundBox.setAlignment(Qt.AlignHCenter)
		backgroundBox.setLayout(backColorLayout)

		# Self message settings

		t = get_style_attribute(self.styles["self"],"color")
		self.selfuser = QLabel("Your nickname")
		self.selfuser.setStyleSheet(self.styles["self"])
		fsetColor = QPushButton("Color")
		fsetColor.clicked.connect(lambda state,u="self",t="self",o=self.selfuser: self.get_color(u,t,o))

		selfColorLayout = QHBoxLayout()
		selfColorLayout.addWidget(self.selfuser)
		selfColorLayout.addWidget(fsetColor)

		selfBox = QGroupBox()
		selfBox.setAlignment(Qt.AlignHCenter)
		selfBox.setLayout(selfColorLayout)

		t = get_style_attribute(self.styles["username"],"color")
		self.username = QLabel("Other nicknames")
		self.username.setStyleSheet(self.styles["username"])
		fsetColor = QPushButton("Color")
		fsetColor.clicked.connect(lambda state,u="self",t="username",o=self.username: self.get_color(u,t,o))

		selfColorLayout = QHBoxLayout()
		selfColorLayout.addWidget(self.username)
		selfColorLayout.addWidget(fsetColor)

		otherBox = QGroupBox()
		otherBox.setAlignment(Qt.AlignHCenter)
		otherBox.setLayout(selfColorLayout)

		# Notice message settings

		t = get_style_attribute(self.styles["notice"],"color")
		self.noticename = QLabel("Notice nickname")
		self.noticename.setStyleSheet(self.styles["notice"])
		fsetColor = QPushButton("Color")
		fsetColor.clicked.connect(lambda state,u="self",t="notice",o=self.noticename: self.get_color(u,t,o))

		selfColorLayout = QHBoxLayout()
		selfColorLayout.addWidget(self.noticename)
		selfColorLayout.addWidget(fsetColor)

		noticeBox = QGroupBox()
		noticeBox.setAlignment(Qt.AlignHCenter)
		noticeBox.setLayout(selfColorLayout)


		# FINAL LAYOUT

		applyButton = QPushButton("Apply")
		applyButton.clicked.connect(self.apply)

		saveButton = QPushButton(" Apply + Save ")
		saveButton.clicked.connect(self.save)

		defaultButton = QPushButton("Defaults")
		defaultButton.clicked.connect(self.resetStyles)

		cancelButton = QPushButton("Cancel")
		cancelButton.clicked.connect(self.close)

		leftLayout = QVBoxLayout()
		leftLayout.addWidget(systemBox)
		leftLayout.addWidget(actionBox)
		leftLayout.addWidget(errorBox)
		

		rightLayout = QVBoxLayout()
		#rightLayout.addWidget(backgroundBox)
		rightLayout.addWidget(selfBox)
		rightLayout.addWidget(otherBox)
		rightLayout.addWidget(noticeBox)
		rightLayout.addWidget(hyperlinkBox)
		rightLayout.addStretch()

		textLayout = QHBoxLayout()
		textLayout.addLayout(leftLayout)
		textLayout.addLayout(rightLayout)

		buttonLayout = QHBoxLayout()
		buttonLayout.addStretch()
		buttonLayout.addWidget(applyButton)
		buttonLayout.addWidget(saveButton)
		buttonLayout.addWidget(defaultButton)
		buttonLayout.addWidget(cancelButton)


		finalLayout = QVBoxLayout()
		finalLayout.addLayout(textLayout)
		finalLayout.addWidget(backgroundBox)
		# finalLayout.addWidget(applyButton)
		# finalLayout.addWidget(saveButton)
		# finalLayout.addWidget(defaultButton)
		finalLayout.addLayout(buttonLayout)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())


	# SUPPORT FUNCTIONS

	def get_bgcolor(self,style,stylename,obj):

		dc = get_style_attribute(self.styles[stylename],"background-color")
		if dc:
			color = QColorDialog.getColor(QColor(dc))
		else:
			color = QColorDialog.getColor()

		if color.isValid():
			ncolor = color.name()

			newstyle = ["background-color: "+ncolor+";"]

			fstyle = get_style_attribute(self.styles[stylename],"color")
			if fstyle: newstyle.append("color: "+fstyle+";")

			fstyle = get_style_attribute(self.styles[stylename],"font-style")
			if fstyle: newstyle.append("font-style: "+fstyle+";")

			fweight = get_style_attribute(self.styles[stylename],"font-weight")
			if fweight: newstyle.append("font-weight: "+fweight+";")

			fd = get_style_attribute(self.styles[stylename],"text-decoration")
			if fd: newstyle.append("text-decoration: "+fd+";")

			final = "\n".join(newstyle)

			self.styles[stylename] = final

			obj.setStyleSheet(final)

	def toggle_italic(self,style,stylename,obj):

		newstyle = []
		fweight = get_style_attribute(self.styles[stylename],"font-style")
		if fweight: 
			if fweight.lower()=="italic":
				fweight = "normal"
			else:
				fweight = "italic"
			newstyle.append("font-style: "+fweight+";")
		else:
			newstyle.append("font-style: italic;")

		fcolor = get_style_attribute(self.styles[stylename],"color")
		if fcolor: newstyle.append("color: "+fcolor+";")

		fstyle = get_style_attribute(self.styles[stylename],"font-weight")
		if fstyle: newstyle.append("font-weight: "+fstyle+";")

		fbg = get_style_attribute(self.styles[stylename],"background-color")
		if fbg: newstyle.append("background-color: "+fbg+";")

		fd = get_style_attribute(self.styles[stylename],"text-decoration")
		if fd: newstyle.append("text-decoration: "+fd+";")

		final = "\n".join(newstyle)
		self.styles[stylename] = final

		obj.setStyleSheet(final)

	def toggle_bold(self,style,stylename,obj):

		newstyle = []
		fweight = get_style_attribute(self.styles[stylename],"font-weight")
		if fweight: 
			if fweight.lower()=="bold":
				fweight = "normal"
			else:
				fweight = "bold"
			newstyle.append("font-weight: "+fweight+";")
		else:
			newstyle.append("font-weight: bold;")

		fcolor = get_style_attribute(self.styles[stylename],"color")
		if fcolor: newstyle.append("color: "+fcolor+";")

		fstyle = get_style_attribute(self.styles[stylename],"font-style")
		if fstyle: newstyle.append("font-style: "+fstyle+";")

		fbg = get_style_attribute(self.styles[stylename],"background-color")
		if fbg: newstyle.append("background-color: "+fbg+";")

		fd = get_style_attribute(self.styles[stylename],"text-decoration")
		if fd: newstyle.append("text-decoration: "+fd+";")

		final = "\n".join(newstyle)
		self.styles[stylename] = final

		obj.setStyleSheet(final)

	def get_color(self,style,stylename,obj):

		dc = get_style_attribute(self.styles[stylename],"color")
		if dc:
			color = QColorDialog.getColor(QColor(dc))
		else:
			color = QColorDialog.getColor()

		if color.isValid():
			ncolor = color.name()

			newstyle = ["color: "+ncolor+";"]

			fstyle = get_style_attribute(self.styles[stylename],"font-style")
			if fstyle: newstyle.append("font-style: "+fstyle+";")

			fweight = get_style_attribute(self.styles[stylename],"font-weight")
			if fweight: newstyle.append("font-weight: "+fweight+";")

			fbg = get_style_attribute(self.styles[stylename],"background-color")
			if fbg: newstyle.append("background-color: "+fbg+";")

			fd = get_style_attribute(self.styles[stylename],"text-decoration")
			if fd: newstyle.append("text-decoration: "+fd+";")

			final = "\n".join(newstyle)
			self.styles[stylename] = final

			obj.setStyleSheet(final)