
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
from erk.strings import *
from erk.config import *
from erk.format import *
from erk.common import *

class Dialog(QDialog):

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

	def save(self):

		self.parent.styles = self.styles
		self.parent.got_new_style()
		write_style_file(self.styles)
		self.close()

	def restart(self):
		self.parent.styles = self.styles
		self.parent.got_new_style()
		write_style_file(self.styles)
		restart_program()

	def resetStyles(self):
		self.styles = get_text_format_settings(DEFAULT_TEXT_FORMAT_FILE)
		self.system.setStyleSheet(self.styles[SYSTEM_STYLE_NAME])
		self.action.setStyleSheet(self.styles[ACTION_STYLE_NAME])
		self.errormsg.setStyleSheet(self.styles[ERROR_STYLE_NAME])
		self.hyperlink.setStyleSheet(self.styles[HYPERLINK_STYLE_NAME])
		self.motd.setStyleSheet(self.styles[MOTD_STYLE_NAME])
		self.backgroundcolor.setStyleSheet(self.styles[BASE_STYLE_NAME])
		self.selfuser.setStyleSheet(self.styles[SELF_STYLE_NAME])
		self.username.setStyleSheet(self.styles[USERNAME_STYLE_NAME])
		self.noticename.setStyleSheet(self.styles[NOTICE_STYLE_NAME])

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle(FORMAT_DIALOG_TITLE)
		self.setWindowIcon(QIcon(FANCY_COLOR))

		self.styles = get_text_format_settings()

		c = get_style_attribute(self.styles[SYSTEM_STYLE_NAME],"color")
		s = get_style_attribute(self.styles[SYSTEM_STYLE_NAME],"font-style")
		w = get_style_attribute(self.styles[SYSTEM_STYLE_NAME],"font-weight")
		b = get_style_attribute(self.styles[SYSTEM_STYLE_NAME],"background-color")
		u = get_style_attribute(self.styles[SYSTEM_STYLE_NAME],"text-decoration")

		self.system = QLabel(FORMAT_DIALOG_SYSTEM)
		self.system.setStyleSheet(self.styles[SYSTEM_STYLE_NAME])

		setColor = QPushButton(FORMAT_DIALOG_COLOR)
		setColor.clicked.connect(lambda state,u="system",t=SYSTEM_STYLE_NAME,o=self.system: self.get_color(u,t,o))

		setBold = QCheckBox(FORMAT_DIALOG_BOLD,self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="system",t=SYSTEM_STYLE_NAME,o=self.system: self.toggle_bold(u,t,o))

		setItalic = QCheckBox(FORMAT_DIALOG_ITALIC,self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="system",t=SYSTEM_STYLE_NAME,o=self.system: self.toggle_italic(u,t,o))	

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

		c = get_style_attribute(self.styles[ACTION_STYLE_NAME],"color")
		s = get_style_attribute(self.styles[ACTION_STYLE_NAME],"font-style")
		w = get_style_attribute(self.styles[ACTION_STYLE_NAME],"font-weight")
		b = get_style_attribute(self.styles[ACTION_STYLE_NAME],"background-color")
		u = get_style_attribute(self.styles[ACTION_STYLE_NAME],"text-decoration")

		self.action = QLabel(FORMAT_DIALOG_ACTION)
		self.action.setStyleSheet(self.styles[ACTION_STYLE_NAME])

		setColor = QPushButton(FORMAT_DIALOG_COLOR)
		setColor.clicked.connect(lambda state,u="action",t=ACTION_STYLE_NAME,o=self.action: self.get_color(u,t,o))

		setBold = QCheckBox(FORMAT_DIALOG_BOLD,self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="action",t=ACTION_STYLE_NAME,o=self.action: self.toggle_bold(u,t,o))

		setItalic = QCheckBox(FORMAT_DIALOG_ITALIC,self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="action",t=ACTION_STYLE_NAME,o=self.action: self.toggle_italic(u,t,o))	

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

		c = get_style_attribute(self.styles[ERROR_STYLE_NAME],"color")
		s = get_style_attribute(self.styles[ERROR_STYLE_NAME],"font-style")
		w = get_style_attribute(self.styles[ERROR_STYLE_NAME],"font-weight")
		b = get_style_attribute(self.styles[ERROR_STYLE_NAME],"background-color")

		self.errormsg = QLabel(FORMAT_DIALOG_ERROR)
		self.errormsg.setStyleSheet(self.styles[ERROR_STYLE_NAME])

		setColor = QPushButton(FORMAT_DIALOG_COLOR)
		setColor.clicked.connect(lambda state,u="error",t=ERROR_STYLE_NAME,o=self.errormsg: self.get_color(u,t,o))

		setBold = QCheckBox(FORMAT_DIALOG_BOLD,self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="error",t=ERROR_STYLE_NAME,o=self.errormsg: self.toggle_bold(u,t,o))

		setItalic = QCheckBox(FORMAT_DIALOG_ITALIC,self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="error",t=ERROR_STYLE_NAME,o=self.errormsg: self.toggle_italic(u,t,o))		

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

		c = get_style_attribute(self.styles[HYPERLINK_STYLE_NAME],"color")
		s = get_style_attribute(self.styles[HYPERLINK_STYLE_NAME],"font-style")
		w = get_style_attribute(self.styles[HYPERLINK_STYLE_NAME],"font-weight")
		b = get_style_attribute(self.styles[HYPERLINK_STYLE_NAME],"background-color")

		self.hyperlink = QLabel(FORMAT_DIALOG_HYPERLINK)
		self.hyperlink.setStyleSheet(self.styles[HYPERLINK_STYLE_NAME])

		setColor = QPushButton(FORMAT_DIALOG_COLOR)
		setColor.clicked.connect(lambda state,u="link",t=HYPERLINK_STYLE_NAME,o=self.hyperlink: self.get_color(u,t,o))

		setBold = QCheckBox(FORMAT_DIALOG_BOLD,self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="link",t=HYPERLINK_STYLE_NAME,o=self.hyperlink: self.toggle_bold(u,t,o))

		setItalic = QCheckBox(FORMAT_DIALOG_ITALIC,self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="link",t=HYPERLINK_STYLE_NAME,o=self.hyperlink: self.toggle_italic(u,t,o))	

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

		c = get_style_attribute(self.styles[MOTD_STYLE_NAME],"color")
		s = get_style_attribute(self.styles[MOTD_STYLE_NAME],"font-style")
		w = get_style_attribute(self.styles[MOTD_STYLE_NAME],"font-weight")
		b = get_style_attribute(self.styles[MOTD_STYLE_NAME],"background-color")

		self.motd = QLabel(FORMAT_DIALOG_MOTD)
		self.motd.setStyleSheet(self.styles[MOTD_STYLE_NAME])

		setColor = QPushButton(FORMAT_DIALOG_COLOR)
		setColor.clicked.connect(lambda state,u="motd",t=MOTD_STYLE_NAME,o=self.motd: self.get_color(u,t,o))

		setBold = QCheckBox(FORMAT_DIALOG_BOLD,self)
		if w:
			if w.lower()=="bold": setBold.toggle()
		setBold.stateChanged.connect(lambda state,u="motd",t=MOTD_STYLE_NAME,o=self.motd: self.toggle_bold(u,t,o))

		setItalic = QCheckBox(FORMAT_DIALOG_ITALIC,self)
		if s:
			if s.lower()=="italic": setItalic.toggle()
		setItalic.stateChanged.connect(lambda state,u="motd",t=MOTD_STYLE_NAME,o=self.motd: self.toggle_italic(u,t,o))	

		motdFormatLayout = QHBoxLayout()
		motdFormatLayout.addWidget(setColor)
		motdFormatLayout.addWidget(setBold)
		motdFormatLayout.addWidget(setItalic)

		motdSelector = QVBoxLayout()
		motdSelector.addWidget(self.motd)
		motdSelector.addLayout(motdFormatLayout)

		motdBox = QGroupBox()
		motdBox.setAlignment(Qt.AlignHCenter)
		motdBox.setLayout(motdSelector)

		c = get_style_attribute(self.styles[BASE_STYLE_NAME],"background-color")
		t = get_style_attribute(self.styles[BASE_STYLE_NAME],"color")
		self.backgroundcolor = QTextEdit()
		self.backgroundcolor.setReadOnly(True)
		self.backgroundcolor.append(FORMAT_DIALOG_EXAMPLE_TEXT)
		self.backgroundcolor.setStyleSheet(self.styles[BASE_STYLE_NAME])

		fm = self.backgroundcolor.fontMetrics()
		h = fm.height() + 12
		self.backgroundcolor.setFixedHeight(h)

		setColor = QPushButton(FORMAT_DIALOG_BG_COLOR)
		setColor.clicked.connect(lambda state,u="all",t=BASE_STYLE_NAME,o=self.backgroundcolor: self.get_bgcolor(u,t,o))

		fsetColor = QPushButton(FORMAT_DIALOG_TXT_COLOR)
		fsetColor.clicked.connect(lambda state,u="all",t=BASE_STYLE_NAME,o=self.backgroundcolor: self.get_color(u,t,o))

		backColorLayout = QHBoxLayout()
		backColorLayout.addWidget(self.backgroundcolor)
		backColorLayout.addWidget(setColor)
		backColorLayout.addWidget(fsetColor)

		backgroundBox = QGroupBox()
		backgroundBox.setAlignment(Qt.AlignHCenter)
		backgroundBox.setLayout(backColorLayout)

		t = get_style_attribute(self.styles[SELF_STYLE_NAME],"color")
		self.selfuser = QLabel(FORMAT_DIALOG_SELF)
		self.selfuser.setStyleSheet(self.styles[SELF_STYLE_NAME])
		fsetColor = QPushButton(FORMAT_DIALOG_COLOR)
		fsetColor.clicked.connect(lambda state,u="self",t=SELF_STYLE_NAME,o=self.selfuser: self.get_color(u,t,o))

		selfColorLayout = QHBoxLayout()
		selfColorLayout.addWidget(self.selfuser)
		selfColorLayout.addWidget(fsetColor)

		selfBox = QGroupBox()
		selfBox.setAlignment(Qt.AlignHCenter)
		selfBox.setLayout(selfColorLayout)

		t = get_style_attribute(self.styles[USERNAME_STYLE_NAME],"color")
		self.username = QLabel(FORMAT_DIALOG_OTHER)
		self.username.setStyleSheet(self.styles[USERNAME_STYLE_NAME])
		fsetColor = QPushButton(FORMAT_DIALOG_COLOR)
		fsetColor.clicked.connect(lambda state,u="self",t=USERNAME_STYLE_NAME,o=self.username: self.get_color(u,t,o))

		selfColorLayout = QHBoxLayout()
		selfColorLayout.addWidget(self.username)
		selfColorLayout.addWidget(fsetColor)

		otherBox = QGroupBox()
		otherBox.setAlignment(Qt.AlignHCenter)
		otherBox.setLayout(selfColorLayout)

		t = get_style_attribute(self.styles[NOTICE_STYLE_NAME],"color")
		self.noticename = QLabel(FORMAT_DIALOG_NOTICE)
		self.noticename.setStyleSheet(self.styles[NOTICE_STYLE_NAME])
		fsetColor = QPushButton(FORMAT_DIALOG_COLOR)
		fsetColor.clicked.connect(lambda state,u="self",t=NOTICE_STYLE_NAME,o=self.noticename: self.get_color(u,t,o))

		selfColorLayout = QHBoxLayout()
		selfColorLayout.addWidget(self.noticename)
		selfColorLayout.addWidget(fsetColor)

		noticeBox = QGroupBox()
		noticeBox.setAlignment(Qt.AlignHCenter)
		noticeBox.setLayout(selfColorLayout)

		leftLayout = QVBoxLayout()
		leftLayout.addWidget(systemBox)
		leftLayout.addWidget(actionBox)
		leftLayout.addWidget(errorBox)
		leftLayout.addWidget(hyperlinkBox)

		rightLayout = QVBoxLayout()
		rightLayout.addWidget(motdBox)
		rightLayout.addWidget(selfBox)
		rightLayout.addWidget(otherBox)
		rightLayout.addWidget(noticeBox)

		textColorsLayout = QHBoxLayout()
		textColorsLayout.addLayout(leftLayout)
		textColorsLayout.addLayout(rightLayout)

		okButton = QPushButton(FORMAT_DIALOG_OK_BUTTON)
		okButton.clicked.connect(self.save)

		restartButton = QPushButton(FORMAT_DIALOG_RESTART_BUTTON)
		restartButton.clicked.connect(self.restart)

		defaultsButton = QPushButton(FORMAT_DIALOG_DEFAULTS_BUTTON)
		defaultsButton.clicked.connect(self.resetStyles)

		cancelButton = QPushButton(FORMAT_DIALOG_CANCEL_BUTTON)
		cancelButton.clicked.connect(self.close)

		buttonsLayout = QHBoxLayout()
		buttonsLayout.addStretch()
		buttonsLayout.addWidget(okButton)
		buttonsLayout.addWidget(restartButton)
		buttonsLayout.addWidget(defaultsButton)
		buttonsLayout.addWidget(cancelButton)

		warning = QLabel(FORMAT_DIALOG_WARNING)
		warning.setAlignment(Qt.AlignHCenter)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(warning)
		finalLayout.addLayout(textColorsLayout)
		finalLayout.addWidget(backgroundBox)
		finalLayout.addLayout(buttonsLayout)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
