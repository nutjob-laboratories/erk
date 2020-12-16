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

class ColorPick(QWidget):

	def getColor(self):
		self.newcolor = QColorDialog.getColor(QColor(self.color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()

			self.color = self.ncolor
			self.exampleText.setStyleSheet(f'color: {self.color};')


	def goDefault(self):
		self.color = self.default
		self.exampleText.setStyleSheet(f'color: {self.default};')

	def __init__(self,name,text,color,default,parent=None):
		super(ColorPick,self).__init__(parent)

		self.name = name
		self.color = color
		self.default = default

		self.exampleText = QLabel(f"{text}")
		self.exampleText.setStyleSheet(f'color: {self.color};')

		self.setColor = QPushButton("Color")
		self.setColor.clicked.connect(self.getColor)

		self.exLayout = QHBoxLayout()
		self.exLayout.addWidget(self.exampleText)
		self.exLayout.addWidget(self.setColor)

		self.setLayout(self.exLayout)

class Dialog(QDialog):

	def getBg(self):
		color = QColorDialog.getColor(QColor(self.bgcolor))

		if color.isValid():
			self.ncolor = color.name()

			self.bgcolor = self.ncolor
			#self.setStyleSheet(f'color: #000000; background-color: {self.bgcolor};')

			c = tuple(int(self.bgcolor[i:i + 2], 16) / 255. for i in (1, 3, 5))
			luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
			luma = luma*100

			if luma>=40:
				self.setStyleSheet(f'color: #000000; background-color: {self.bgcolor};')
			else:
				self.setStyleSheet(f'color: #ffffff; background-color: {self.bgcolor};')

	def buildStyle(self):

		styles = self.parent.style

		styles['editor'] = f'''
			color: {self.plaintext.color};
			background-color: {self.bgcolor};

			{self.keyword.name}: {self.keyword.color};
			{self.operator.name}: {self.operator.color};
			{self.brace.name}: {self.brace.color};
			{self.defined.name}: {self.defined.color};
			{self.string.name}: {self.string.color};
			{self.mstrings.name}: {self.mstrings.color};
			{self.comment.name}: {self.comment.color};
			{self.mself.name}: {self.mself.color};
			{self.numbers.name}: {self.numbers.color};
			{self.erk.name}: {self.erk.color};
		'''

		styles['editor'] = styles['editor'].replace("\n","")
		styles['editor'] = styles['editor'].replace("\t","")
		styles['editor'] = styles['editor'].replace(";","; ")
		styles['editor'] = styles['editor'].strip()

		return styles

	def applyDefault(self):

		self.keyword.goDefault()
		self.operator.goDefault()
		self.brace.goDefault()
		self.defined.goDefault()
		self.string.goDefault()
		self.mstrings.goDefault()
		self.comment.goDefault()
		self.mself.goDefault()
		self.numbers.goDefault()
		self.erk.goDefault()
		self.plaintext.goDefault()

		self.bgcolor = '#ffffff'
		self.setStyleSheet(f'color: #000000; background-color: {self.bgcolor};')

	def apply(self):
		
		cstyle = self.buildStyle()

		self.parent.setStyle(cstyle)
		
		if self.parent.changed==False:
			self.parent.changed = False
			self.parent.title = self.parent.title.replace('* ','',1)
			self.parent.updateApplicationTitle()

	def applySave(self):

		cstyle = self.buildStyle()

		self.parent.setStyle(cstyle)

		write_style_file(cstyle,self.parent.stylefile)

		if self.parent.changed==False:
			self.parent.changed = False
			self.parent.title = self.parent.title.replace('* ','',1)
			self.parent.updateApplicationTitle()

		self.close()


	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		skey = 'blue'
		soper = 'red'
		sbrac = 'darkGray'
		sdef = 'black'
		sstring = 'magenta'
		smstring = 'darkMagenta'
		scom = 'darkGreen'
		smself = 'black'
		snum = 'brown'
		sserk = '#0212b6'
		regtext = 'black'
		self.bgcolor = '#ffffff'


		self.setWindowTitle("Highlight colors")
		self.setWindowIcon(QIcon(FORMAT_ICON))


		styles = self.parent.style
		for e in styles['editor'].split(";"):
			line = e.split(':')
			if len(line)==2:

				line[0] = line[0].strip()
				line[1] = line[1].strip()

				key = str(line[0])
				val = str(line[1])


				if key.lower()=='keyword':
					skey = val

				if key.lower()=='operator':
					soper = val

				if key.lower()=='brace':
					sbrac = val

				if key.lower()=='defined':
					sdef = val

				if key.lower()=='string':
					sstring = val

				if key.lower()=='multiline-strings':
					smstring = val

				if key.lower()=='comment':
					scom = val

				if key.lower()=='comment':
					smself = val

				if key.lower()=='numbers':
					snum = val

				if key.lower()=='erk':
					sserk = val

				if key.lower()=='color':
					regtext = val

				if key.lower()=='background-color':
					self.bgcolor = val


		self.keyword = ColorPick('keyword','Keywords',skey,'blue')
		self.operator = ColorPick('operator','Operators',soper,'red')
		self.brace = ColorPick('brace','Braces',sbrac,'darkGray')
		self.defined = ColorPick('defined','Defines',sdef,'black')
		self.string = ColorPick('string','Strings',sstring,'magenta')
		self.mstrings = ColorPick('multiline-strings','Multiline Strings',smstring,'darkMagenta')
		self.comment = ColorPick('comment','Comments',scom,'darkGreen')
		self.mself = ColorPick('self','Self',smself,'black')
		self.numbers = ColorPick('numbers','Numbers',snum,'brown')
		self.erk = ColorPick('erk','Erk Specific',sserk,'#0212b6')
		self.plaintext = ColorPick('color','Text',regtext,'black')

		self.bgColorButton = QPushButton("Set background color")
		self.bgColorButton.clicked.connect(self.getBg)

		self.leftLayout = QVBoxLayout()
		self.leftLayout.addWidget(self.plaintext)
		self.leftLayout.addWidget(self.keyword)
		self.leftLayout.addWidget(self.operator)
		self.leftLayout.addWidget(self.brace)
		self.leftLayout.addWidget(self.defined)
		self.leftLayout.addWidget(self.mself)

		self.rightColumn = QVBoxLayout()
		self.rightColumn.addWidget(self.string)
		self.rightColumn.addWidget(self.mstrings)
		self.rightColumn.addWidget(self.comment)
		self.rightColumn.addWidget(self.numbers)
		self.rightColumn.addWidget(self.erk)
		
		self.columns = QHBoxLayout()
		self.columns.addLayout(self.leftLayout)
		self.columns.addLayout(self.rightColumn)

		self.applyButton = QPushButton("Apply")
		self.applyButton.clicked.connect(self.apply)

		self.saveAndApplyButton = QPushButton("Apply + Save")
		self.saveAndApplyButton.clicked.connect(self.applySave)

		self.setDefaultButton = QPushButton("Defaults")
		self.setDefaultButton.clicked.connect(self.applyDefault)

		self.cancelButton = QPushButton("Cancel")
		self.cancelButton.clicked.connect(self.close)

		buttonsLayout = QHBoxLayout()
		buttonsLayout.addWidget(self.applyButton)
		buttonsLayout.addWidget(self.saveAndApplyButton)
		buttonsLayout.addWidget(self.setDefaultButton)
		buttonsLayout.addWidget(self.cancelButton)

		self.buttonsBox = QGroupBox()
		self.buttonsBox.setAlignment(Qt.AlignHCenter)
		self.buttonsBox.setLayout(buttonsLayout)

		self.finalLayout = QVBoxLayout()
		self.finalLayout.addLayout(self.columns)
		self.finalLayout.addWidget(self.bgColorButton)
		self.finalLayout.addWidget(self.buttonsBox)

		self.setStyleSheet(f'color: #000000; background-color: {self.bgcolor};')

		self.setLayout(self.finalLayout)
		
