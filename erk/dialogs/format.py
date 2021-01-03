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


def menuHtml(icon,text,description,icon_size):
	return f'''
<table style="width: 100%" border="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;"><img src="{icon}" width="{icon_size}" height="{icon_size}">&nbsp;</td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: italic; font-weight: normal;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''

def MenuAction(self,icon,title,description,icon_size,func):

	erkmenuLabel = MenuLabel( menuHtml(icon,title,description,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)
	erkmenuLabel.clicked.connect(func)

	return erkmenuAction

class MenuLabel(QLabel):
	clicked=pyqtSignal()

	def __init__(self, parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

	def mousePressEvent(self, ev):
		self.clicked.emit()

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			col = self.palette().highlight().color().name()
			highlight = QColor(col).name()

			col = self.palette().highlightedText().color().name()
			highlight_text = QColor(col).name()
			
			self.setStyleSheet(f"background-color: {highlight}; color: {highlight_text};")

			#self.setStyleSheet(f"background-color: #a9a9a9; color: white;")

			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet('')
		return False

class AllStyler(QWidget):

	def loadQss(self,style,default):
		self.qss = style
		self.default = default

		self.parseQss()
		self.generateQss()

		self.example.setStyleSheet(self.qss)


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

	def __init__(self,name,qss,default,funcs_to_update,parent=None):
		super(AllStyler,self).__init__(parent)
		self.name = name
		self.qss = qss 
		self.default = default

		self.color = None
		self.background_color = None

		self.parseQss()

		self.first_color = self.color
		self.first_background = self.background_color

		# self.example = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor<br>incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud")
		self.example = QLabel("This is an example of chat text, with the <br>background color of all text displays")
		self.example.setStyleSheet(self.qss)

		self.setColor = QPushButton("Text")
		self.setColor.clicked.connect(self.buttonColor)
		self.setColor.setIcon(QIcon(FORMAT_ICON))

		fm = QFontMetrics(self.font())
		br = fm.boundingRect('Text')
		#self.setDefault.setFixedWidth(br.width()+8)
		self.setColor.setFixedWidth(br.width()+35)

		self.setBg = QPushButton("Background")
		self.setBg.clicked.connect(self.buttonBg)
		self.setBg.setIcon(QIcon(FORMAT_ICON))

		br = fm.boundingRect('Background')
		self.setBg.setFixedWidth(br.width()+35)

		self.setDefault = QPushButton("Default")
		self.setDefault.clicked.connect(self.buttonDefault)

		br = fm.boundingRect('Default')
		self.setDefault.setFixedWidth(br.width()+10)

		self.setReset = QPushButton("Reset")
		self.setReset.clicked.connect(self.buttonReset)

		br = fm.boundingRect('Reset')
		self.setReset.setFixedWidth(br.width()+10)



		controlLayout = QHBoxLayout()
		controlLayout.addWidget(self.setColor)
		controlLayout.addWidget(self.setBg)
		controlLayout.addWidget(self.setDefault)
		controlLayout.addWidget(self.setReset)
		controlLayout.setAlignment(Qt.AlignRight)

		allTextLayout = QVBoxLayout()
		allTextLayout.addWidget(self.example)
		allTextLayout.addLayout(controlLayout)

		finalBox = QGroupBox()
		finalBox.setAlignment(Qt.AlignHCenter)
		finalBox.setLayout(allTextLayout)

		finalLayout = QHBoxLayout()
		finalLayout.addWidget(finalBox)

		DMARGIN = 0
		margins = finalLayout.contentsMargins()
		finalLayout.setContentsMargins(margins.left(),DMARGIN,margins.right(),DMARGIN)

		self.setLayout(finalLayout)


class TextStyler(QWidget):

	def loadQss(self,style,default):
		self.qss = style
		self.default = default

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

		gcode = gcode + f' background-color: {self.bgcolor}'
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
		self.bgcolor = None

		self.parseQss()

		self.first_color = self.color
		self.first_bold = self.bold
		self.first_italic = self.italic
		self.first_underline = self.underline

		if self.underline:
			self.example = QLabel(f"<u>{self.text}</u>")
		else:
			self.example = QLabel(f"{self.text}")

		#self.parseQss()
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
		self.styles['notice'] = self.noticewid.exportQss()
		self.styles['all'] = self.allText.exportQss()
		self.styles['server'] = self.motdwid.exportQss()
		self.styles['plugin'] = self.plugwid.exportQss()

		textformat.STYLES = self.styles

		self.parent.newStyle(self.styles["all"])

		self.parent.reload_all_text()

		self.close()

	def doSaveAs(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Style As...",self.parent.styledir,f"{APPLICATION_NAME} Style File (*.{STYLE_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:
			self.styles['system'] = self.syswid.exportQss()
			self.styles['action'] = self.actwid.exportQss()
			self.styles['error'] = self.errwid.exportQss()
			self.styles['hyperlink'] = self.linkwid.exportQss()
			self.styles['self'] = self.selfwid.exportQss()
			self.styles['username'] = self.userwid.exportQss()
			self.styles['notice'] = self.noticewid.exportQss()
			self.styles['all'] = self.allText.exportQss()
			self.styles['server'] = self.motdwid.exportQss()
			self.styles['plugin'] = self.plugwid.exportQss()
			exlen = len(STYLE_FILE_EXTENSION)+1
			if fileName[-exlen:].lower()!="."+STYLE_FILE_EXTENSION: fileName = fileName+"."+STYLE_FILE_EXTENSION
			write_style_file(self.styles,fileName)

			self.filename = fileName

	def doApplySave(self):
		
		self.styles['system'] = self.syswid.exportQss()
		self.styles['action'] = self.actwid.exportQss()
		self.styles['error'] = self.errwid.exportQss()
		self.styles['hyperlink'] = self.linkwid.exportQss()
		self.styles['self'] = self.selfwid.exportQss()
		self.styles['username'] = self.userwid.exportQss()
		self.styles['notice'] = self.noticewid.exportQss()
		self.styles['all'] = self.allText.exportQss()
		self.styles['server'] = self.motdwid.exportQss()
		self.styles['plugin'] = self.plugwid.exportQss()

		textformat.STYLES = self.styles

		self.parent.newStyle(self.styles["all"])

		self.parent.reload_all_text()

		write_style_file(self.styles,self.filename)

		self.close()

	def doDefaults(self):
		
		self.syswid.doDefault()
		self.actwid.doDefault()
		self.errwid.doDefault()
		self.linkwid.doDefault()
		self.selfwid.doDefault()
		self.userwid.doDefault()
		self.noticewid.doDefault()
		self.allText.doDefault()
		self.motdwid.doDefault()
		self.plugwid.doDefault()

	def loadStyle(self):

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Load Style File",self.parent.styledir,f"{APPLICATION_NAME} Style File (*.{STYLE_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:

			self.styles = get_text_format_settings(fileName)

			self.syswid.loadQss(self.styles["system"],self.default_styles["system"])
			self.actwid.loadQss(self.styles["action"],self.default_styles["action"])
			self.errwid.loadQss(self.styles["error"],self.default_styles["error"])
			self.linkwid.loadQss(self.styles["hyperlink"],self.default_styles["hyperlink"])
			self.selfwid.loadQss(self.styles["self"],self.default_styles["self"])
			self.userwid.loadQss(self.styles["username"],self.default_styles["username"])
			self.noticewid.loadQss(self.styles["notice"],self.default_styles["notice"])
			self.allText.loadQss(self.styles["all"],self.default_styles["all"])
			self.motdwid.loadQss(self.styles["server"],self.default_styles["server"])
			self.plugwid.loadQss(self.styles["plugin"],self.default_styles["plugin"])


	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Text colors & formatting")
		self.setWindowIcon(QIcon(FORMAT_ICON))

		self.filename = parent.stylefile

		# self.styles = get_text_format_settings()
		self.styles = get_text_format_settings(self.filename)
		self.default_styles = get_text_format_settings(BACKUP_STYLE_FILE)

		self.syswid = TextStyler('system','This is a system message',self.styles['system'],self.default_styles['system'],True,False,self)
		self.actwid = TextStyler('action','This is a CTCP action message',self.styles['action'],self.default_styles['action'],True,False,self)
		self.errwid = TextStyler('error','This is an error message',self.styles['error'],self.default_styles['error'],True,False,self)

		self.linkwid = TextStyler('hyperlink','This is an example hyperlink',self.styles['hyperlink'],self.default_styles['hyperlink'],True,True,self)

		self.selfwid = TextStyler('self','Your nickname',self.styles['self'],self.default_styles['self'],True,False,self)
		self.userwid = TextStyler('username','Other nicknames',self.styles['username'],self.default_styles['username'],True,False,self)
		self.noticewid = TextStyler('notice','Notice nicknames',self.styles['notice'],self.default_styles['notice'],True,False,self)

		self.motdwid = TextStyler('server','This is a server message',self.styles['server'],self.default_styles['server'],True,False,self)

		self.plugwid = TextStyler('plugin','This is a plugin-generated message',self.styles['plugin'],self.default_styles['plugin'],True,False,self)


		self.tabs = QTabWidget()
		self.user_tab = QWidget()
		self.chat_tab = QWidget()
		self.system_tab = QWidget()

		mbcolor = self.palette().color(QPalette.Window).name()
		self.tabs.setStyleSheet(f'background-color: {mbcolor}')

		self.tabs.addTab(self.user_tab,"Nicknames")
		self.tabs.addTab(self.chat_tab,"Chat")
		self.tabs.addTab(self.system_tab,"System")

		usersaLayout = QVBoxLayout()
		usersaLayout.addWidget(self.selfwid)
		usersaLayout.addWidget(self.userwid)
		usersaLayout.addWidget(self.noticewid)
		usersaLayout.addStretch()

		chatLayout = QVBoxLayout()
		chatLayout.addWidget(self.actwid)
		chatLayout.addWidget(self.linkwid)
		chatLayout.addWidget(self.motdwid)
		chatLayout.addStretch()

		systemLayout = QVBoxLayout()
		systemLayout.addWidget(self.syswid)
		systemLayout.addWidget(self.errwid)
		systemLayout.addWidget(self.plugwid)

		self.user_tab.setLayout(usersaLayout)
		self.chat_tab.setLayout(chatLayout)
		self.system_tab.setLayout(systemLayout)

		self.allText = AllStyler('all',self.styles['all'],self.default_styles['all'],self)

		self.buttonApply = QPushButton("Apply to unstyled chats")
		self.buttonApply.clicked.connect(self.doApply)

		self.buttonApplySave = QPushButton("Apply && Save")
		self.buttonApplySave.clicked.connect(self.doApplySave)
		

		# self.buttonSaveAs = QPushButton("Save style as...")
		# self.buttonSaveAs.clicked.connect(self.doSaveAs)

		self.buttonDefault = QPushButton("Load stock style settings")
		self.buttonDefault.clicked.connect(self.doDefaults)

		self.buttonCancel = QPushButton("Cancel")
		self.buttonCancel.clicked.connect(self.close)
		self.buttonCancel.setDefault(True)  

		# self.buttonLoad = QPushButton("Open style")
		# self.buttonLoad.clicked.connect(self.loadStyle)

		self.menubar = QMenuBar(self)
		fileMenu = self.menubar.addMenu ("File")

		entry = MenuAction(self,OPENFILE_ICON,"Open","Load a style file",25,self.loadStyle)
		fileMenu.addAction(entry)

		entry = MenuAction(self,SAVEASFILE_ICON,"Save as...","Save to a style file",25,self.doSaveAs)
		fileMenu.addAction(entry)

		# entry = MenuAction(self,DOCUMENT_ICON,"Restore","Load base style",25,self.doDefaults)
		# fileMenu.addAction(entry)

		# fileMenu.addSeparator()

		# entry = QAction(QIcon(EXIT_ICON),"Exit",self)
		# entry.triggered.connect(self.close)
		# fileMenu.addAction(entry)



		topButtons = QHBoxLayout()
		topButtons.addStretch()
		topButtons.addWidget(self.buttonApply)
		topButtons.addWidget(self.buttonApplySave)
		topButtons.addWidget(self.buttonCancel)

		midButtons = QHBoxLayout()
		# midButtons.addWidget(self.buttonLoad)
		# midButtons.addWidget(self.buttonSaveAs)
		midButtons.addWidget(self.buttonDefault)

		# buttons = QHBoxLayout()
		# buttons.addWidget(self.buttonApply)
		# buttons.addWidget(self.buttonApplySave)
		# buttons.addWidget(self.buttonSaveAs)
		# buttons.addWidget(self.buttonDefault)
		# buttons.addWidget(self.buttonCancel)

		controls = QVBoxLayout()
		controls.addLayout(midButtons)
		controls.addLayout(topButtons)
		#controls.addLayout(midButtons)
		#controls.addWidget(self.buttonCancel)
		

		setLayout = QVBoxLayout()
		setLayout.addWidget(self.menubar)
		setLayout.addWidget(self.allText)
		setLayout.addWidget(self.tabs)

		DMARGIN = 0
		margins = setLayout.contentsMargins()
		setLayout.setContentsMargins(margins.left(),DMARGIN,margins.right(),DMARGIN)

		finalLayout = QVBoxLayout()
		# finalLayout.addWidget(self.allText)
		# finalLayout.addWidget(self.tabs)
		finalLayout.addLayout(setLayout)
		finalLayout.addLayout(controls)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
