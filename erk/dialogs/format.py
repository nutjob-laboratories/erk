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

from ..resources import *
from ..files import *
from .. import textformat

class AllStyler(QWidget):

	def doDefault(self):
		self.qss = self.default
		self.parseQss()
		self.generateQss()
		self.example.setStyleSheet(self.qss)

	def buttonDefault(self):
		self.qss = self.default
		self.parseQss()
		self.generateQss()
		self.example.setStyleSheet(self.qss)

	def buttonColor(self):
		self.newcolor = QColorDialog.getColor(QColor(self.color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()
			self.color = self.ncolor
			self.generateQss()
			self.example.setStyleSheet(self.qss)

	def buttonBg(self):
		self.newcolor = QColorDialog.getColor(QColor(self.background_color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()
			self.background_color = self.ncolor
			self.generateQss()
			self.example.setStyleSheet(self.qss)

	def buttonReset(self):
		self.color = self.first_color
		self.background_color = self.first_background

		self.generateQss()
		self.example.setStyleSheet(self.qss)


	def generateQss(self):
		gcode = f'color: {self.color};'
		gcode = gcode + f' background-color: {self.background_color};'
		self.qss = gcode

	def exportQss(self):
		gcode = f'color: {self.color};'
		gcode = gcode + f' background-color: {self.background_color};'
		return gcode

	def parseQss(self):
		for line in self.qss.split(";"):
			e = line.split(':')
			if len(e)==2:
				key = e[0].strip()
				value = e[1].strip()

				if key.lower()=='color':
					self.color = value

				if key.lower()=='background-color':
					self.background_color = value


	def __init__(self,name,qss,default,parent=None):
		super(AllStyler,self).__init__(parent)
		self.name = name
		self.qss = qss 
		self.default = default

		self.color = None
		self.background_color = None

		self.parseQss()

		self.first_color = self.color
		self.first_background = self.background_color

		self.example = QLabel("Lorem ipsum dolor sit amet")
		self.example.setStyleSheet(self.qss)

		self.setColor = QPushButton("Set text color")
		self.setColor.clicked.connect(self.buttonColor)

		self.setBg = QPushButton("Set background color")
		self.setBg.clicked.connect(self.buttonBg)

		self.setDefault = QPushButton("Default")
		self.setDefault.clicked.connect(self.buttonDefault)

		self.setReset = QPushButton("Reset")
		self.setReset.clicked.connect(self.buttonReset)

		finalLayout = QHBoxLayout()
		finalLayout.addWidget(self.example)
		finalLayout.addWidget(self.setColor)
		finalLayout.addWidget(self.setBg)
		finalLayout.addWidget(self.setDefault)
		finalLayout.addWidget(self.setReset)

		self.setLayout(finalLayout)


class TextStyler(QWidget):

	def exportQss(self):
		gcode = f'color: {self.color};'
		if self.bold: gcode = gcode + ' font-weight: bold;'
		if self.italic: gcode = gcode + ' font-style: italic;'
		if self.underline: gcode = gcode + ' text-decoration: underline;'

		return gcode

	def generateQss(self):
		gcode = f'color: {self.color};'
		if self.bold: gcode = gcode + ' font-weight: bold;'
		if self.italic:
			gcode = gcode + ' font-style: italic;'
		else:
			gcode = gcode + ' font-style: normal;'
		#if self.underline: gcode = gcode + ' text-decoration: underline;'

		self.qss = gcode

	def doReset(self):

		self.color = self.first_color
		self.bold = self.first_bold
		self.italic = self.first_italic
		self.underline = self.first_underline

		self.generateQss()
		self.parseQss()

		self.example.setStyleSheet(self.qss)
		self.setColor.setStyleSheet(f'background-color: {self.color};')

		if self.show_styles:

			if self.bold:
				self.setBold.setCheckState(Qt.Checked)
			else:
				self.setBold.setCheckState(Qt.Unchecked)

			if self.italic:
				self.setItalic.setCheckState(Qt.Checked)
			else:
				self.setItalic.setCheckState(Qt.Unchecked)

	def doDefault(self):
		self.qss = self.default

		self.parseQss()

		self.example.setStyleSheet(self.qss)
		self.setColor.setStyleSheet(f'background-color: {self.color};')

		if self.show_styles:

			if self.bold:
				self.setBold.setCheckState(Qt.Checked)
			else:
				self.setBold.setCheckState(Qt.Unchecked)

			if self.italic:
				self.setItalic.setCheckState(Qt.Checked)
			else:
				self.setItalic.setCheckState(Qt.Unchecked)


	def buttonColor(self):

		self.newcolor = QColorDialog.getColor(QColor(self.color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()
			self.color = self.ncolor
			self.generateQss()
			self.example.setStyleSheet(self.qss)
			self.setColor.setStyleSheet(f'background-color: {self.color};')

	def checkBold(self,state):
		if state==Qt.Checked:
			self.bold = True
			self.setBold.setCheckState(Qt.Checked)
		else:
			self.bold = False
			self.setBold.setCheckState(Qt.Unchecked)
		self.generateQss()
		self.example.setStyleSheet(self.qss)

	def checkItalic(self,state):
		if state==Qt.Checked:
			self.italic = True
			self.setItalic.setCheckState(Qt.Checked)
		else:
			self.italic = False
			self.setItalic.setCheckState(Qt.Unchecked)
		self.generateQss()
		self.example.setStyleSheet(self.qss)

	def parseQss(self):
		for line in self.qss.split(";"):
			e = line.split(':')
			if len(e)==2:
				key = e[0].strip()
				value = e[1].strip()

				if key.lower()=='color':
					self.color = value

				if key.lower()=='font-style':
					if value.lower()=='italic':
						self.italic = True

				if key.lower()=='font-weight':
					if value.lower()=='bold':
						self.bold = True

	def __init__(self,name,text,qss,default,show_styles=True,underline=False,parent=None):
		super(TextStyler,self).__init__(parent)
		self.name = name
		self.text = text
		self.parent = parent
		self.qss = qss
		self.default = default
		self.show_styles = show_styles

		self.color = None
		self.bold = False
		self.italic = False
		self.underline = underline

		self.parseQss()

		self.first_color = self.color
		self.first_bold = self.bold
		self.first_italic = self.italic
		self.first_underline = self.underline

		if self.underline:
			self.example = QLabel(f"<u>{self.text}</u>")
		else:
			self.example = QLabel(f"{self.text}")
		self.example.setStyleSheet(self.qss)

		self.setColor = QPushButton("")
		self.setColor.clicked.connect(self.buttonColor)
		self.setColor.setStyleSheet(f'background-color: {self.color};')

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setColor.setFixedSize(fheight +10,fheight + 10)
		self.setColor.setIcon(QIcon(FORMAT_ICON))

		self.setDefault = QPushButton("Default")
		self.setDefault.clicked.connect(self.doDefault)

		br = fm.boundingRect('Default')
		#self.setDefault.setFixedWidth(br.width()+8)
		self.setDefault.setFixedHeight(br.height())

		self.setReset = QPushButton("Reset")
		self.setReset.clicked.connect(self.doReset)

		br = fm.boundingRect('Reset')
		#self.setReset.setFixedWidth(br.width()+8)
		self.setReset.setFixedHeight(br.height())

		if self.show_styles:

			self.setBold = QCheckBox("Bold",self)
			self.setBold.stateChanged.connect(self.checkBold)
			if self.bold:
				self.setBold.setCheckState(Qt.Checked)
			else:
				self.setBold.setCheckState(Qt.Unchecked)

			self.setItalic = QCheckBox("Italic",self)
			self.setItalic.stateChanged.connect(self.checkItalic)
			if self.italic:
				self.setItalic.setCheckState(Qt.Checked)
			else:
				self.setItalic.setCheckState(Qt.Unchecked)

			controlsLayout = QHBoxLayout()
			controlsLayout.addWidget(self.setColor)
			controlsLayout.addWidget(self.setBold)
			controlsLayout.addWidget(self.setItalic)
			controlsLayout.addWidget(self.setDefault)
			controlsLayout.addWidget(self.setReset)
			controlsLayout.setAlignment(Qt.AlignLeft)

		else:

			controlsLayout = QHBoxLayout()
			controlsLayout.addWidget(self.setColor)
			controlsLayout.addWidget(self.setDefault)
			controlsLayout.addWidget(self.setReset)
			controlsLayout.setAlignment(Qt.AlignLeft)
		

		finalBox = QGroupBox()
		finalBox.setAlignment(Qt.AlignHCenter)
		finalBox.setLayout(controlsLayout)

		finale = QVBoxLayout()
		finale.addWidget(self.example)
		finale.addWidget(finalBox)

		self.setLayout(finale)


class Dialog(QDialog):

	def closeEvent(self,event):
		event.accept()

	def doApply(self):
		
		self.styles['system'] = self.syswid.exportQss()
		self.styles['action'] = self.actwid.exportQss()
		self.styles['error'] = self.errwid.exportQss()
		self.styles['hyperlink'] = self.linkwid.exportQss()
		self.styles['self'] = self.selfwid.exportQss()
		self.styles['username'] = self.userwid.exportQss()
		self.styles['notice'] = self.userwid.exportQss()
		self.styles['all'] = self.allText.exportQss()

		textformat.STYLES = self.styles

		self.parent.newStyle(self.styles["all"])

		self.parent.reload_all_text()

		self.close()

	def doApplySave(self):
		
		self.styles['system'] = self.syswid.exportQss()
		self.styles['action'] = self.actwid.exportQss()
		self.styles['error'] = self.errwid.exportQss()
		self.styles['hyperlink'] = self.linkwid.exportQss()
		self.styles['self'] = self.selfwid.exportQss()
		self.styles['username'] = self.userwid.exportQss()
		self.styles['notice'] = self.userwid.exportQss()
		self.styles['all'] = self.allText.exportQss()

		textformat.STYLES = self.styles

		self.parent.newStyle(self.styles["all"])

		self.parent.reload_all_text()

		write_style_file(self.styles,self.parent.stylefile)

		self.close()

	def doDefaults(self):
		
		self.syswid.doDefault()
		self.actwid.doDefault()
		self.errwid.doDefault()
		self.linkwid.doDefault()
		self.selfwid.doDefault()
		self.userwid.doDefault()
		self.userwid.doDefault()
		self.allText.doDefault()

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Text colors & formatting")
		self.setWindowIcon(QIcon(FORMAT_ICON))

		# self.styles = get_text_format_settings()
		self.styles = get_text_format_settings(parent.stylefile)
		self.default_styles = get_text_format_settings(BACKUP_STYLE_FILE)

		self.syswid = TextStyler('system','This is a system message',self.styles['system'],self.default_styles['system'],True,False,self)
		self.actwid = TextStyler('action','This is a TCTP action message',self.styles['action'],self.default_styles['action'],True,False,self)
		self.errwid = TextStyler('error','This is an error message',self.styles['error'],self.default_styles['error'],True,False,self)

		self.linkwid = TextStyler('hyperlink','This is an example hyperlink',self.styles['hyperlink'],self.default_styles['hyperlink'],True,True,self)

		self.selfwid = TextStyler('self','Your nickname',self.styles['self'],self.default_styles['self'],False,False,self)
		self.userwid = TextStyler('username','Other nicknames',self.styles['username'],self.default_styles['username'],False,False,self)
		self.noticewid = TextStyler('notice','Notice nicknames',self.styles['notice'],self.default_styles['notice'],False,False,self)


		row_1 = QHBoxLayout()
		row_1.addWidget(self.syswid)
		row_1.addWidget(self.actwid)

		row_2 = QHBoxLayout()
		row_2.addWidget(self.errwid)
		row_2.addWidget(self.linkwid)

		row_3 = QHBoxLayout()
		row_3.addWidget(self.selfwid)
		row_3.addWidget(self.userwid)
		row_3.addWidget(self.noticewid)

		self.allText = AllStyler('all',self.styles['all'],self.default_styles['all'],self)

		bothColumns = QVBoxLayout()
		bothColumns.addLayout(row_1)
		bothColumns.addLayout(row_2)
		bothColumns.addLayout(row_3)

		self.buttonApply = QPushButton("Apply")
		self.buttonApply.clicked.connect(self.doApply)

		self.buttonApplySave = QPushButton("Apply + Save")
		self.buttonApplySave.clicked.connect(self.doApplySave)

		self.buttonDefault = QPushButton("Set Defaults")
		self.buttonDefault.clicked.connect(self.doDefaults)

		self.buttonCancel = QPushButton("Cancel")
		self.buttonCancel.clicked.connect(self.close)

		buttons = QHBoxLayout()
		buttons.addWidget(self.buttonApply)
		buttons.addWidget(self.buttonApplySave)
		buttons.addWidget(self.buttonDefault)
		buttons.addWidget(self.buttonCancel)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(bothColumns)
		finalLayout.addWidget(self.allText)
		finalLayout.addLayout(buttons)


		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
