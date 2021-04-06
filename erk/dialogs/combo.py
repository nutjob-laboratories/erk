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

import os,sys

from ..resources import *
from ..objects import *
from ..files import *
from ..widgets import *
from ..strings import *
from ..common import *
from .. import syntax
from .. import config
from ..widgets.action import textSeparator
from ..dialogs import AddChannelDialog
from .send_pm import Dialog as SendPM
from .pause import Dialog as PauseTime
from .comment import Dialog as Comment
from .print import Dialog as PrintMsg
from .alias import Dialog as InsertAlias
from .new_macro import Dialog as NewMacro

INSTALL_DIRECTORY = sys.path[0]
DOCUMENTATION_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "documentation")
DOCUMENTATION = os.path.join(DOCUMENTATION_DIRECTORY, "Erk_Scripting_and_Commands.pdf")

class Dialog(QDialog):

	@staticmethod
	def get_connect_information(can_do_ssl,userfile,do_ssl=None,do_reconnect=None,block_scripts=False,scriptsdir='',show_banner=False,parent=None):
		dialog = Dialog(can_do_ssl,userfile,do_ssl,do_reconnect,block_scripts,scriptsdir,show_banner,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

	def return_info(self):

		if len(self.host.text())==0:
			self.errorDialog("Please select a server to connect to")
			return []

		try:
			port = int(self.port.text())
		except:
			self.errorDialog("Port must be a number")
			return []

		if len(self.password.text())>0:
			password = self.password.text()
		else:
			password = None

		user_history = self.user_info["history"]
		if self.SAVE_HISTORY: # For saving history

			# make sure server isn't in the built-in list
			inlist = False

			# make sure server isn't in history
			inhistory = False
			for s in user_history:
				if s[0]==self.host.text():
					if s[1]==self.port.text():
						inhistory = True

			if inlist==False and inhistory==False:

				if self.CONNECT_VIA_SSL:
					ussl = "ssl"
				else:
					ussl = "normal"


				entry = [ self.host.text(),self.port.text(),UNKNOWN_NETWORK,ussl,self.password.text() ]
				user_history.append(entry)

		# Save user ignores
		ignored = self.user_info["ignore"]

		# Save user info
		user = {
			"nickname": self.nick.text(),
			"username": self.username.text(),
			"realname": self.realname.text(),
			"alternate": self.alternative.text(),
			"last_server": self.host.text(),
			"last_port": self.port.text(),
			"last_password": self.password.text(),
			"ssl": self.CONNECT_VIA_SSL,
			"reconnect": self.RECONNECT_OPTION,
			"autojoin": True,
			"history": user_history,
			"save_history": self.SAVE_HISTORY,
			"ignore": ignored,
			"failreconnect": self.RETRY_FAILED_OPTION,
			"auto_script": self.EXECUTE_AUTOSCRIPT_OPTION,
			"save_script": self.SAVE_AUTOSCRIPT,
		}
		save_user(user,self.userfile)

		# Don't autojoin channels
		channels = []

		if not self.block_scripts:

			script = None

			if self.EXECUTE_AUTOSCRIPT_OPTION:
				# Autoscript
				script = self.scriptedit.toPlainText()
				if len(script)==0: script = None

				if self.SAVE_AUTOSCRIPT:
					if script!=None:
						save_auto_script(self.host.text(),str(port),script,self.scriptsdir)
					else:
						# If the script editor is empty, and the connect script exists,
						# AND saving is turned on, then remove the script
						sfile = get_auto_script_name(self.host.text(),str(port),self.scriptsdir)
						if os.path.isfile(sfile):
							os.remove(sfile)

		else:
			script = None

		retval = ConnectInfo(self.host.text(),port,password,self.CONNECT_VIA_SSL,self.nick.text(),self.alternative.text(),self.username.text(),self.realname.text(),self.RECONNECT_OPTION,channels,self.RETRY_FAILED_OPTION,True,script)

		return retval

	# BEGIN HELPER METHODS

	def clickDoScript(self,state):
		if state == Qt.Checked:
			self.EXECUTE_AUTOSCRIPT_OPTION = True
			self.tabs.addTab(self.script_tab, QIcon(SCRIPT_ICON), "Script")
		else:
			self.EXECUTE_AUTOSCRIPT_OPTION = False
			self.tabs.removeTab(1)

	def clickSSL(self,state):
		if state == Qt.Checked:
			self.CONNECT_VIA_SSL = True
		else:
			self.CONNECT_VIA_SSL = False

	def setServer(self):

		if not len(self.user_info["last_server"])>0:
			if self.placeholder:
				self.servers.removeItem(0)
				self.StoredData.pop(0)
				self.placeholder = False

		self.StoredServer = self.servers.currentIndex()

		# Fill in the server info
		h = self.StoredData[self.StoredServer]
		if "ssl" in h[3]:
			use_ssl = True
		else:
			use_ssl = False
		host = h[0]
		port = int(h[1])

		self.host.setText(host)
		self.port.setText(h[1])

		if len(h)==5:
			if h[4]=='':
				password = None
				self.password.setText('')
			else:
				password = h[4]
				self.password.setText(h[4])
		else:
			password = None
			self.password.setText('')

		if use_ssl:
			self.ssl.setCheckState(Qt.Checked)
		else:
			self.ssl.setCheckState(Qt.Unchecked)

	def serverEntered(self):
		serv = self.host.text()
		port = self.port.text()

		code = load_auto_script(serv,port,self.scriptsdir)
		if code!=None:
			self.scriptedit.setPlainText(code)
		else:
			self.scriptedit.clear()

		self.scriptedit.moveCursor(QTextCursor.End)

		if len(serv)>0:
			self.scriptDesignateServer.setText("<center><big><b>"+serv+":"+str(port)+"</b></big></center>")
			self.saveScript.setEnabled(True)
		else:
			self.saveScript.setEnabled(False)
			self.scriptDesignateServer.setText("<center><big><b>IRC Server</b></big></center>")

	# END HELPER METHODS

	def __init__(self,can_do_ssl,userfile=USER_FILE,do_ssl=None,do_reconnect=None,block_scripts=False,scriptsdir='',config_file=SETTINGS_FILE,show_banner=False,parent=None):
		super(Dialog,self).__init__(parent)

		config.load_settings(config_file)

		self.can_do_ssl = can_do_ssl
		self.parent = parent
		self.userfile = userfile

		self.block_scripts = block_scripts
		self.scriptsdir = scriptsdir
		self.config_file = config_file

		# do_ssl
		# Set to "not none" to check off "ssl"

		# do_reconnect
		# Set to "not None" to see if a command is trying to activate
		# the "set reconnect as checked"

		self.CONNECT_VIA_SSL = False

		self.RECONNECT_OPTION = False
		self.RETRY_FAILED_OPTION = False
		self.SAVE_HISTORY = False
		self.EXECUTE_AUTOSCRIPT_OPTION = False
		self.SAVE_AUTOSCRIPT = False

		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)

		# Determine if window color is dark or light
		mbcolor = self.palette().color(QPalette.Window).name()
		c = tuple(int(mbcolor[i:i + 2], 16) / 255. for i in (1, 3, 5))
		luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
		luma = luma*100

		if luma>=40:
			self.is_light_colored = True
		else:
			self.is_light_colored = False

		self.scriptEditor = None

		self.StoredData = []
		self.StoredServer = 0
		self.prevVisit = []

		self.placeholder = False

		self.setWindowTitle(APPLICATION_NAME+" "+APPLICATION_VERSION)
		self.setWindowIcon(QIcon(CONNECT_MENU_ICON))

		self.user_info = get_user(self.userfile)

		self.EXECUTE_AUTOSCRIPT_OPTION = self.user_info["auto_script"]

		# User information widget

		self.nick = QLineEdit(self.user_info["nickname"])
		self.alternative = QLineEdit(self.user_info["alternate"])
		self.username = QLineEdit(self.user_info["username"])
		self.realname = QLineEdit(self.user_info["realname"])

		nickl = QLabel("Nickname")
		nickl.setFont(BOLD_FONT)

		altl = QLabel("Alternate")
		altl.setFont(BOLD_FONT)

		usrl = QLabel("Username")
		usrl.setFont(BOLD_FONT)

		reall = QLabel("Real name")
		reall.setFont(BOLD_FONT)

		self.userbar = QMenuBar(self)
		self.userbar.setFont(BOLD_FONT)

		userMenu = self.userbar.addMenu ("Options")

		entry = QAction(QIcon(REDO_ICON),"Reset",self)
		entry.triggered.connect(self.resetUser)
		userMenu.addAction(entry)

		entry = QAction(QIcon(RESTART_ICON),"Set to defaults",self)
		entry.triggered.connect(self.restoreDefaults)
		userMenu.addAction(entry)

		entry = QAction(QIcon(EXPORT_ICON),"Save user settings",self)
		entry.triggered.connect(self.saveSettings)
		userMenu.addAction(entry)

		userLayout = QFormLayout()
		userLayout.addRow(nickl, self.nick)
		userLayout.addRow(altl, self.alternative)
		userLayout.addRow(usrl, self.username)
		userLayout.addRow(reall, self.realname)

		finUserLayout = QVBoxLayout()
		finUserLayout.addWidget(self.userbar)
		finUserLayout.addLayout(userLayout)

		userInfoBox = QGroupBox("User Information",self)
		userInfoBox.setLayout(finUserLayout)

		userInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		# Server selector

		self.servers = QComboBox(self)
		self.servers.activated.connect(self.setServer)
		self.servers.setFont(BOLD_FONT)

		self.buildServerSelector()

		# Menu bar

		self.menubar = QMenuBar(self)
		self.menubar.setFont(BOLD_FONT)

		optionsMenu = self.menubar.addMenu ("Options")

		entry = QAction(QIcon(BAN_ICON),"Clear connection history",self)
		entry.triggered.connect(self.clearHistory)
		optionsMenu.addAction(entry)

		entry = QAction(QIcon(BAN_ICON),"Clear last connection",self)
		entry.triggered.connect(self.clearLast)
		optionsMenu.addAction(entry)

		entry = QAction(QIcon(EXPORT_ICON),"Save user settings",self)
		entry.triggered.connect(self.saveSettings)
		optionsMenu.addAction(entry)

		optionsMenu.addSeparator()

		self.RECONNECT_OPTION = self.user_info["reconnect"]

		self.reconnect_Option = QAction(QIcon(UNCHECKED_ICON),"Reconnect on disconnection",self)
		self.reconnect_Option.triggered.connect(lambda state,s="reconnect": self.toggleSetting(s))
		optionsMenu.addAction(self.reconnect_Option)

		if self.RECONNECT_OPTION: self.reconnect_Option.setIcon(QIcon(CHECKED_ICON))

		if do_reconnect!=None:
			if not self.RECONNECT_OPTION:
				self.RECONNECT_OPTION = True
				self.reconnect_Option.setIcon(QIcon(CHECKED_ICON))

		# self.RETRY_FAILED_OPTION

		self.RETRY_FAILED_OPTION = self.user_info["failreconnect"]

		self.retryfailed_Option = QAction(QIcon(UNCHECKED_ICON),"Retry failed connections",self)
		self.retryfailed_Option.triggered.connect(lambda state,s="retry": self.toggleSetting(s))
		optionsMenu.addAction(self.retryfailed_Option)

		if self.RETRY_FAILED_OPTION: self.retryfailed_Option.setIcon(QIcon(CHECKED_ICON))

		if not self.RECONNECT_OPTION: self.retryfailed_Option.setEnabled(False)

		# self.SAVE_HISTORY

		self.SAVE_HISTORY = self.user_info["save_history"]

		self.savehistory_Option = QAction(QIcon(UNCHECKED_ICON),"Save connection history",self)
		self.savehistory_Option.triggered.connect(lambda state,s="save_history": self.toggleSetting(s))
		optionsMenu.addAction(self.savehistory_Option)

		if self.SAVE_HISTORY: self.savehistory_Option.setIcon(QIcon(CHECKED_ICON))

		# Server information box

		self.host = QLineEdit(self.user_info["last_server"])
		self.port = QLineEdit(self.user_info["last_port"])
		self.password = QLineEdit(self.user_info["last_password"])
		self.password.setEchoMode(QLineEdit.Password)

		self.host.textChanged.connect(self.serverEntered)
		self.port.textChanged.connect(self.serverEntered)

		serverLayout = QFormLayout()

		hostl = QLabel("Host")
		hostl.setFont(BOLD_FONT)
		serverLayout.addRow(hostl, self.host)

		portl = QLabel("Port")
		portl.setFont(BOLD_FONT)
		serverLayout.addRow(portl, self.port)

		passl = QLabel("Password")
		passl.setFont(BOLD_FONT)
		serverLayout.addRow(passl, self.password)

		self.ssl = QCheckBox("Connect via SSL/TLS",self)
		self.ssl.stateChanged.connect(self.clickSSL)

		self.doScript = QCheckBox("Execute script on connect",self)
		self.doScript.stateChanged.connect(self.clickDoScript)

		if self.block_scripts:
			self.doScript.setVisible(False)

		self.ssl.setFont(BOLD_FONT)
		self.doScript.setFont(BOLD_FONT)

		if self.user_info["ssl"]:
			self.ssl.toggle()

		if do_ssl!=None:
			if not self.user_info["ssl"]:
				self.ssl.toggle()

		sfBox = QVBoxLayout()
		sfBox.addWidget(self.menubar)
		sfBox.addWidget(self.servers)
		sfBox.addLayout(serverLayout)
		sfBox.addWidget(self.ssl)
		sfBox.addWidget(self.doScript)
		
		serverInfoBox = QGroupBox("IRC Server",self)
		serverInfoBox.setLayout(sfBox)

		serverInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		# Scripting

		self.scriptedit = QPlainTextEdit(self)
		self.highlight = syntax.ErkScriptHighlighter(self.scriptedit.document(),self.config_file)
		self.scriptedit.setPlaceholderText("Enter your connection script here.")

		self.scripttabinfo = QLabel("<small><center><i>Most commands usable in the client can be used. Insert comments between \"</i><b>/*</b><i>\" and \"</i><b>*/</b><i>\". To pause the script, call the \"</i><b>/wait</b><i>\" command with the number of seconds to pause as the only argument.</i></center></small>")
		self.scripttabinfo.setWordWrap(True)
		self.scripttabinfo.setAlignment(Qt.AlignJustify)

		self.scriptDesignate = QLabel("<center><small>Execute on connection to</small></center>")
		if len(self.user_info["last_server"])==0:
			self.scriptDesignateServer = QLabel("<center><big><b>IRC Server</b></big></center>")
		else:
			self.scriptDesignateServer = QLabel("<center><big><b>"+self.user_info["last_server"]+"</b></big></center>")

		# Load in script if there's one for the last entered server
		if len(self.user_info["last_server"])>0 and len(self.user_info["last_port"])>0:
			code = load_auto_script(self.user_info["last_server"],self.user_info["last_port"],self.scriptsdir)
			if code!=None:
				self.scriptedit.setPlainText(code)

		self.scriptedit.moveCursor(QTextCursor.End)

		# Tabs

		self.tabs = QTabWidget()

		self.tabs.setFont(BOLD_FONT)

		self.tabs.setStyleSheet("""
			QTabWidget::tab-bar { alignment: center; font: bold; }
			""")
		
		self.connection_information_tab = QWidget()
		self.tabs.addTab(self.connection_information_tab, QIcon(CONNECT_MENU_ICON), "Connect to IRC")

		connectTabLayout = QVBoxLayout()
		connectTabLayout.addWidget(userInfoBox)
		connectTabLayout.addWidget(serverInfoBox)

		self.connection_information_tab.setLayout(connectTabLayout)

		self.script_tab = QWidget()
		self.tabs.addTab(self.script_tab, QIcon(SCRIPT_ICON), "Script")

		self.scriptbar = QMenuBar(self)
		self.scriptbar.setFont(BOLD_FONT)

		fileMenu = self.scriptbar.addMenu ("File")

		self.saveScript = QAction(QIcon(EXPORT_ICON),"Save connection script",self)
		self.saveScript.triggered.connect(self.scriptSave)
		fileMenu.addAction(self.saveScript)

		if len(self.user_info["last_server"])==0: self.saveScript.setEnabled(False)

		entry = QAction(QIcon(NEWFILE_ICON),"Clear",self)
		entry.triggered.connect(self.scriptClear)
		fileMenu.addAction(entry)

		fileMenu.addSeparator()

		# self.SAVE_AUTOSCRIPT

		self.SAVE_AUTOSCRIPT = self.user_info["save_script"]

		self.savescript_Option = QAction(QIcon(UNCHECKED_ICON),"Save script on connection",self)
		self.savescript_Option.triggered.connect(lambda state,s="save_script": self.toggleSetting(s))
		fileMenu.addAction(self.savescript_Option)

		if self.SAVE_AUTOSCRIPT: self.savescript_Option.setIcon(QIcon(CHECKED_ICON))

		if not self.EXECUTE_AUTOSCRIPT_OPTION: self.savescript_Option.setEnabled(False)

		insertMenu = self.scriptbar.addMenu ("Insert command")

		insertMenu.addAction(textSeparator(self,"IRC"))

		entry = QAction(QIcon(MESSAGE_ICON),"Private message",self)
		entry.triggered.connect(self.scriptPM)
		insertMenu.addAction(entry)

		entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
		entry.triggered.connect(self.scriptJoin)
		insertMenu.addAction(entry)

		insertMenu.addAction(textSeparator(self,APPLICATION_NAME))

		entry = QAction(QIcon(TIMESTAMP_ICON),"Pause",self)
		entry.triggered.connect(self.scriptTime)
		insertMenu.addAction(entry)

		entry = QAction(QIcon(EDIT_ICON),"Print",self)
		entry.triggered.connect(self.scriptPrint)
		insertMenu.addAction(entry)

		entry = QAction(QIcon(MISC_ICON),"Alias",self)
		entry.triggered.connect(self.scriptAlias)
		insertMenu.addAction(entry)

		entry = QAction(QIcon(MISC_ICON),"Local alias",self)
		entry.triggered.connect(self.scriptLocal)
		insertMenu.addAction(entry)

		entry = QAction(QIcon(MISC_ICON),"Macro",self)
		entry.triggered.connect(self.scriptMacro)
		insertMenu.addAction(entry)

		insertMenu.addAction(textSeparator(self,"Miscellaneous"))

		entry = QAction(QIcon(EDIT_ICON),"Comment",self)
		entry.triggered.connect(self.scriptComment)
		insertMenu.addAction(entry)

		entry = QAction(QIcon(EDIT_ICON),"Multi-line comment",self)
		entry.triggered.connect(self.scriptMLComment)
		insertMenu.addAction(entry)

		self.docLink = QLabel("<center><small><b><a href=\""+DOCUMENTATION+"\">Command documentation</a></b></small></center>")
		self.docLink.setOpenExternalLinks(True)

		scriptTabLayout = QVBoxLayout()
		scriptTabLayout.addWidget(self.scriptDesignate)
		scriptTabLayout.addWidget(self.scriptDesignateServer)
		scriptTabLayout.addWidget(self.scriptbar)
		scriptTabLayout.addWidget(self.scriptedit)
		scriptTabLayout.addWidget(self.docLink)
		scriptTabLayout.addWidget(self.scripttabinfo)

		self.script_tab.setLayout(scriptTabLayout)

		if self.EXECUTE_AUTOSCRIPT_OPTION:
			self.doScript.toggle()
		else:
			self.tabs.removeTab(1)

		if self.block_scripts:
			self.tabs.removeTab(1)

		# Built final layout

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Connect")

		if show_banner:
			banner = QLabel()
			pixmap = QPixmap(BANNER_IMAGE)
			banner.setPixmap(pixmap)
			banner.setAlignment(Qt.AlignCenter)

		self.menubar.setStyleSheet(f"QMenuBar {{ background-color:transparent;  }}")
		self.scriptbar.setStyleSheet(f"QMenuBar {{ background-color:transparent;  }}")
		self.userbar.setStyleSheet(f"QMenuBar {{ background-color:transparent;  }}")

		finalLayout = QVBoxLayout()
		if show_banner: finalLayout.addWidget(banner)
		finalLayout.addWidget(self.tabs)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def errorDialog(self,text):
		msg = QMessageBox(self)
		msg.setIcon(QMessageBox.Critical)
		msg.setText(text)
		msg.setWindowTitle("Error!")
		msg.exec_()

	def scriptMacro(self):
		x = NewMacro(self)
		e = x.get_macro_information(self)

		if not e: return

		macro_name = e[0].strip()
		macro_args = e[1]
		macro = e[2].strip()
		macro_help = e[3].strip()
		macro_helpargs = e[4].strip()

		self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+f"macro {macro_name} {macro_args} {macro}\n")
		if macro_help!='':
			self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+f"macrohelp {macro_name} {macro_help}\n")
		if macro_helpargs!='':
			self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+f"macrousage {macro_name} {macro_helpargs}\n")

	def scriptLocal(self):
		x = InsertAlias(self)
		e = x.get_alias_information(self)

		if not e: return

		name = e[0]
		value = e[1]

		self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+"_alias "+name+" "+value+"\n")

	def scriptAlias(self):
		x = InsertAlias(self)
		e = x.get_alias_information(self)

		if not e: return

		name = e[0]
		value = e[1]

		self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+"alias "+name+" "+value+"\n")

	def scriptSave(self):

		try:
			port = int(self.port.text())
		except:
			self.errorDialog("Port must be a number")
			return

		script = self.scriptedit.toPlainText()

		# If the script is blank, and the file exists,
		# then just delete the file
		if len(script.strip())==0:
			sfile = get_auto_script_name(self.host.text(),str(port),self.scriptsdir)
			if os.path.isfile(sfile):
				os.remove(sfile)
				return

		save_auto_script(self.host.text(),str(port),script,self.scriptsdir)

	def scriptClear(self):
		self.scriptedit.clear()

	def scriptTime(self):
		x = PauseTime()
		e = x.get_time_information()

		if not e: return

		self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+"wait "+str(e)+"\n")

	def scriptPM(self):
		x = SendPM()
		e = x.get_message_information()

		if not e: return

		target = e[0]
		msg = e[1]
		
		if len(target)>0 and len(msg)>0:
			self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+"msg "+target+" "+msg+"\n")

	def scriptComment(self):
		x = Comment()
		e = x.get_message_information()

		if not e: return

		if len(e)>0:
			self.scriptedit.insertPlainText("/* "+e+" */\n")

	def scriptMLComment(self):
		x = Comment(False)
		e = x.get_message_information(False)

		if not e: return

		if len(e)>0:
			self.scriptedit.insertPlainText("/*\n"+e+"\n*/\n")

	def scriptPrint(self):
		x = PrintMsg()
		e = x.get_message_information()

		if not e: return

		if len(e)>0:
			self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+"print "+e+"\n")

	def scriptJoin(self):
		x = AddChannelDialog()
		e = x.get_channel_information()

		if not e: return

		channel = e[0]
		key = e[1]

		if len(key)==0:
			self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+"join "+channel+"\n")
		else:
			self.scriptedit.insertPlainText(config.INPUT_COMMAND_SYMBOL+"join "+channel+" "+key+"\n")

	def toggleSetting(self,setting):

		if setting=="save_script":
			if self.SAVE_AUTOSCRIPT:
				self.SAVE_AUTOSCRIPT = False
				self.savescript_Option.setIcon(QIcon(UNCHECKED_ICON))
			else:
				self.SAVE_AUTOSCRIPT = True
				self.savescript_Option.setIcon(QIcon(CHECKED_ICON))

		if setting=="save_history":
			if self.SAVE_HISTORY:
				self.SAVE_HISTORY = False
				self.savehistory_Option.setIcon(QIcon(UNCHECKED_ICON))
			else:
				self.SAVE_HISTORY = True
				self.savehistory_Option.setIcon(QIcon(CHECKED_ICON))

		if setting=="retry":
			if self.RETRY_FAILED_OPTION:
				self.RETRY_FAILED_OPTION = False
				self.retryfailed_Option.setIcon(QIcon(UNCHECKED_ICON))
			else:
				self.RETRY_FAILED_OPTION = True
				self.retryfailed_Option.setIcon(QIcon(CHECKED_ICON))

		if setting=="reconnect":
			if self.RECONNECT_OPTION:
				self.RECONNECT_OPTION = False
				self.retryfailed_Option.setEnabled(False)
				self.reconnect_Option.setIcon(QIcon(UNCHECKED_ICON))
			else:
				self.RECONNECT_OPTION = True
				self.retryfailed_Option.setEnabled(True)
				self.reconnect_Option.setIcon(QIcon(CHECKED_ICON))

	def saveSettings(self):

		# Save user info
		user = {
			"nickname": self.nick.text(),
			"username": self.username.text(),
			"realname": self.realname.text(),
			"alternate": self.alternative.text(),
			"last_server": self.host.text(),
			"last_port": self.port.text(),
			"last_password": self.password.text(),
			"ssl": self.CONNECT_VIA_SSL,
			"reconnect": self.RECONNECT_OPTION,
			"autojoin": True,
			"history": self.user_info["history"],
			"save_history": self.SAVE_HISTORY,
			"disabled_plugins": self.user_info["disabled_plugins"],
			"ignore": self.user_info["ignore"],
			"failreconnect": self.RETRY_FAILED_OPTION,
			"auto_script": self.EXECUTE_AUTOSCRIPT_OPTION,
			"save_script": self.SAVE_AUTOSCRIPT,
		}
		save_user(user,self.userfile)

	def resetUser(self):
		self.nick.setText(self.user_info["nickname"])
		self.alternative.setText(self.user_info["alternate"])
		self.username.setText(self.user_info["username"])
		self.realname.setText(self.user_info["realname"])

	def clearHistory(self):
		self.user_info["history"] = []
		self.buildServerSelector()

	def clearLast(self):
		self.user_info["last_server"] = ''
		self.user_info["last_port"] = '6667'
		self.user_info["last_password"] = ''

		self.host.setText('')
		self.port.setText('6667')
		self.password.setText('')

		self.buildServerSelector()

	def restoreDefaults(self):
		self.nick.setText(DEFAULT_NICKNAME)
		self.username.setText(DEFAULT_USERNAME)
		self.realname.setText(DEFAULT_IRCNAME)
		self.alternative.setText(DEFAULT_ALTERNATIVE)

	def buildServerSelector(self):
		self.StoredData = []
		self.StoredServer = 0
		self.prevVisit = []

		self.placeholder = False

		self.servers.clear()

		if self.user_info["ssl"]:
			dussl = "ssl"
			icon = QIcon(VISITED_SSL_ICON)
		else:
			dussl = "normal"
			icon = QIcon(VISITED_ICON)

		if len(self.user_info["last_server"])>0:
			self.StoredData.append( [ self.user_info["last_server"],self.user_info["last_port"],"Last server",dussl,self.user_info["last_password"] ]    )
			self.servers.addItem(icon,"Last server connection")
		else:
			self.StoredData.append( ['',"6667",'','normal','' ]    )
			self.servers.addItem("Select a server")

		# Load in stuff from disk
		self.built_in_server_list = get_network_list()

		organized_list = []

		if len(self.user_info["history"])>0:
			# servers are in history
			for s in self.user_info["history"]:

				builtin = False
				for entry in self.built_in_server_list:
					if entry[0]==s[0]:
						if entry[1]==s[1]:
							builtin = True

				if not builtin:
					self.built_in_server_list.insert(0,s)

		counter = -1
		for entry in self.built_in_server_list:
			counter = counter + 1
			if len(entry) < 4: continue

			if "ssl" in entry[3]:
				if not self.can_do_ssl: continue

			visited = False
			if len(self.user_info["history"])>0:
				for s in self.user_info["history"]:
					if s[0]==entry[0]:
						if s[1]==entry[1]:
							visited = True

			if visited:
				organized_list.append([True,entry])
			else:
				organized_list.append([False,entry])

		vserver = []
		nserver = []
		for x in organized_list:
			if x[0]:
				vserver.append(x)
			else:
				nserver.append(x)
		finallist = vserver + nserver
		
		for s in finallist:
			if s[0]:
				self.prevVisit.append(s[1])
				if s[1][3].lower()=='ssl':
					self.servers.addItem(QIcon(VISITED_SSL_ICON),s[1][2]+" - "+s[1][0])
				else:
					self.servers.addItem(QIcon(VISITED_ICON),s[1][2]+" - "+s[1][0])
			else:
				if s[1][3].lower()=='ssl':
					self.servers.addItem(QIcon(UNVISITED_SSL_ICON),s[1][2]+" - "+s[1][0])
				else:
					self.servers.addItem(QIcon(UNVISITED_ICON),s[1][2]+" - "+s[1][0])

			self.StoredData.append(s[1])

		self.StoredServer = self.servers.currentIndex()
