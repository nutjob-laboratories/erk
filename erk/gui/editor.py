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
import re
import string

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *
from erk.syntax import QCodeEditor, PythonHighlighter

import erk.gui.dialogs.newplugin as PluginDialog
import erk.gui.dialogs.newcommand as CommandDialog

import erk.gui.find as FindWindow

import erk.gui.dialogs.pluginmsg as CommandMsgDialog
import erk.gui.dialogs.pluginjoin as CommandJoinDialog
import erk.gui.dialogs.pluginpart as CommandPartDialog
import erk.gui.dialogs.pluginprint as CommandPrintDialog
import erk.gui.dialogs.plugincolor as CommandColorDialog
import erk.gui.dialogs.pluginaway as CommandAwayDialog
import erk.gui.dialogs.pluginmode as CommandModeDialog

from erk.plugins import PluginCollection

class Viewer(QMainWindow):

	def closeEvent(self, event):

		# Remove window from master window list
		clean = []
		for w in self.parent.editor_windows:
			if w==self: continue
			clean.append(w)
		self.parent.editor_windows = clean
		self.parent.rebuildWindowMenu()

		if self.findWindow != None:
			self.findWindow.close()

		if self.parent==None:
			self.close()
			return

		if self.changed:
			self.doExitSave(self.filename)

		if self.parent.windowcount==0:
			self.parent.setWindowTitle(DEFAULT_WINDOW_TITLE)
		
		self.subwindow.close()
		self.close()

	def doNewFile(self):
		if self.changed:
			self.doExitSave(self.filename)

		self.filename = ''
		self.editor.clear()
		self.title = EDITOR_NAME
		self.setWindowTitle(self.title)
		self.parent.updateActiveChild(self.parent.MDI.activeSubWindow())
		self.changed = False
		self.msav.setEnabled(False)
		self.parent.rebuildWindowMenu()


	def doFileOpen(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Plugin", PLUGIN_DIRECTORY,"Python File (*.py);;All Files (*)", options=options)
		if fileName:
			script = open(fileName,"r")
			self.editor.setPlainText(script.read())
			self.filename = fileName
			self.msav.setEnabled(True)
			self.title = f"{EDITOR_NAME} - " + os.path.basename(fileName)
			self.setWindowTitle(self.title)
			self.parent.updateActiveChild(self.parent.MDI.activeSubWindow())
			self.changed = False
			self.parent.rebuildWindowMenu()

	def doFileSave(self):
		code = open(self.filename,"w")
		code.write(self.editor.toPlainText())
		self.setWindowTitle(self.title)
		self.parent.updateActiveChild(self.parent.MDI.activeSubWindow())
		self.changed = False
		self.parent.rebuildWindowMenu()

	def doExitSave(self,default):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Plugin As...",default,"Python File (*.py);;All Files (*)", options=options)
		if fileName:
			if '.py' in fileName:
				pass
			else:
				fileName = fileName + '.py'
			self.filename = fileName
			code = open(fileName,"w")
			code.write(self.editor.toPlainText())

	def doFileSaveAs(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Plugin As...",PLUGIN_DIRECTORY,"Python File (*.py);;All Files (*)", options=options)
		if fileName:
			if '.py' in fileName:
				pass
			else:
				fileName = fileName + '.py'
			self.filename = fileName
			code = open(fileName,"w")
			code.write(self.editor.toPlainText())
			self.msav.setEnabled(True)
			self.title = f"{EDITOR_NAME} - " + os.path.basename(fileName)
			self.setWindowTitle(self.title)
			self.parent.updateActiveChild(self.parent.MDI.activeSubWindow())
			self.changed = False
			self.parent.rebuildWindowMenu()

			if self.findWindow!=None:
				f = os.path.basename(self.filename)
				self.findWindow.setWindowTitle(f"Find in {f}")

	def docModified(self):
		if self.count==0:
			self.count = 1
			self.changed = False
			return
		if self.changed: return
		self.setWindowTitle(f"{self.title} *")
		self.parent.updateActiveChild(self.parent.MDI.activeSubWindow())
		self.changed = True
		self.parent.rebuildWindowMenu()

	def injectPlugin(self,classname,name,version,description,issilent,isnowindows,isnoirc):

		# Escape any double quotes
		description = description.replace('"',r'\"')
		name = name.replace('"',r'\"')

		t = PLUGIN_SKELETON
		t = t.replace(PLUGIN_CLASS,classname)
		t = t.replace(PLUGIN_NAME,name)
		t = t.replace(PLUGIN_VERSION,version)
		t = t.replace(PLUGIN_DESCRIPTION,description)

		if issilent and isnowindows and isnoirc:
			po = "self.silent,self.nowindows,self.noirc = True,True,True"
		elif issilent and isnowindows:
			po = "self.silent,self.nowindows = True,True"
		elif issilent and isnoirc:
			po = "self.silent,self.noirc = True,True"
		elif isnowindows and isnoirc:
			po = "self.nowindows,self.noirc = True,True"
		elif isnoirc:
			po = "self.noirc = True"
		elif issilent:
			po = "self.silent = True"
		elif isnowindows:
			po = "self.nowindows = True"
		else:
			po = ""
		t = t.replace(PLUGIN_OPTIONS,po)

		# self.editor.appendPlainText(t)
		self.editor.insertPlainText(t)

	def doTemplate(self):
		x = PluginDialog.Dialog()
		pinfo = x.get_plugin_information(parent=self)

		if not pinfo: return

		classname = pinfo[0]
		name = pinfo[1]
		version = pinfo[2]
		description = pinfo[3]
		issilent = pinfo[4]
		isnowindows = pinfo[5]
		isnoirc = pinfo[6]

		# Strip forbidden characters from classname
		classname = classname.translate(str.maketrans('', '', string.punctuation))
		classname = classname.translate(str.maketrans('', '', string.whitespace))

		errs = []
		if len(classname)==0: errs.append("class name not entered")
		if len(name)==0: errs.append("name not entered")
		if len(version)==0: errs.append("version not entered")
		if len(description)==0: errs.append("description not entered")

		if classname.isspace(): errs.append("class name is blank")
		if name.isspace(): errs.append("name is blank")
		if version.isspace(): errs.append("version is blank")
		if description.isspace(): errs.append("description is blank")

		if len(errs)>0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(EDIT_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Missing or Invalid Input")
			es = ""
			for e in errs: es = es + f"<li>{e}</li>"
			msg.setInformativeText(f"<ul>{es}</ul>")
			msg.setWindowTitle("Can't inject plugin template")
			msg.exec_()
			return

		i = TEMPLATE_MODULE_LOAD
		if i in self.editor.toPlainText():
			pass
		else:
			self.addToBeginning(i)

		self.injectPlugin(classname,name,version,description,issilent,isnowindows,isnoirc)

	def doCommand(self):
		x = CommandDialog.Dialog()
		pinfo = x.get_plugin_information(parent=self)

		if not pinfo: return

		classname = pinfo[0]
		name = pinfo[1]
		version = pinfo[2]
		description = pinfo[3]
		trigger = pinfo[4]
		issilent = pinfo[5]
		isnowindows = pinfo[6]
		isnoirc = pinfo[7]

		argcount = pinfo[8]

		# Strip forbidden characters from classname
		classname = classname.translate(str.maketrans('', '', string.punctuation))
		classname = classname.translate(str.maketrans('', '', string.whitespace))

		errs = []
		if len(classname)==0: errs.append("class name not entered")
		if len(name)==0: errs.append("name not entered")
		if len(version)==0: errs.append("version not entered")
		if len(description)==0: errs.append("description not entered")
		if len(trigger)==0: errs.append("command name not entered")

		if classname.isspace(): errs.append("class name is blank")
		if name.isspace(): errs.append("name is blank")
		if version.isspace(): errs.append("version is blank")
		if description.isspace(): errs.append("description is blank")
		if trigger.isspace(): errs.append("command name is blank")

		if len(errs)>0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(EDIT_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Missing or Invalid Input")
			es = ""
			for e in errs: es = es + f"<li>{e}</li>"
			msg.setInformativeText(f"<ul>{es}</ul>")
			msg.setWindowTitle("Can't inject command template")
			msg.exec_()
			return

		i = TEMPLATE_MODULE_LOAD
		if i in self.editor.toPlainText():
			pass
		else:
			self.addToBeginning(i)

		i = "import shlex"
		if i in self.editor.toPlainText():
			pass
		else:
			self.addToBeginning(i)

		self.injectCommand(classname,name,version,description,trigger,issilent,isnowindows,isnoirc,argcount)


	def doPublicCommand(self):
		x = CommandDialog.Dialog()
		pinfo = x.get_plugin_information(parent=self)

		if not pinfo: return

		classname = pinfo[0]
		name = pinfo[1]
		version = pinfo[2]
		description = pinfo[3]
		trigger = pinfo[4]
		issilent = pinfo[5]
		isnowindows = pinfo[6]
		isnoirc = pinfo[7]

		argcount = pinfo[8]

		# Strip forbidden characters from classname
		classname = classname.translate(str.maketrans('', '', string.punctuation))
		classname = classname.translate(str.maketrans('', '', string.whitespace))

		errs = []
		if len(classname)==0: errs.append("class name not entered")
		if len(name)==0: errs.append("name not entered")
		if len(version)==0: errs.append("version not entered")
		if len(description)==0: errs.append("description not entered")
		if len(trigger)==0: errs.append("command name not entered")

		if classname.isspace(): errs.append("class name is blank")
		if name.isspace(): errs.append("name is blank")
		if version.isspace(): errs.append("version is blank")
		if description.isspace(): errs.append("description is blank")
		if trigger.isspace(): errs.append("command name is blank")

		if len(errs)>0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(EDIT_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Missing or Invalid Input")
			es = ""
			for e in errs: es = es + f"<li>{e}</li>"
			msg.setInformativeText(f"<ul>{es}</ul>")
			msg.setWindowTitle("Can't inject command template")
			msg.exec_()
			return

		i = TEMPLATE_MODULE_LOAD
		if i in self.editor.toPlainText():
			pass
		else:
			self.addToBeginning(i)

		i = "import shlex"
		if i in self.editor.toPlainText():
			pass
		else:
			self.addToBeginning(i)


		self.injectPublicCommand(classname,name,version,description,trigger,issilent,isnowindows,isnoirc,argcount)

	def addToBeginning(self,text):

		code = self.editor.toPlainText()
		self.editor.clear()
		# self.editor.setPlainText(code)
		self.editor.insertPlainText(text)
		self.editor.appendPlainText(code)
		

	def injectPublicCommand(self,classname,name,version,description,trigger,issilent,isnowindows,isnoirc,argcount):

		# Escape any double quotes
		description = description.replace('"',r'\"')
		name = name.replace('"',r'\"')

		t = PUBLIC_COMMAND_SKELETON
		t = t.replace(PLUGIN_CLASS,classname)
		t = t.replace(PLUGIN_NAME,name)
		t = t.replace(PLUGIN_VERSION,version)
		t = t.replace(PLUGIN_DESCRIPTION,description)
		t = t.replace(PLUGIN_TRIGGER,trigger)

		t = t.replace(PLUGIN_ARGCOUNT,str(argcount))

		if issilent and isnowindows and isnoirc:
			po = "self.silent,self.nowindows,self.noirc = True,True,True"
		elif issilent and isnowindows:
			po = "self.silent,self.nowindows = True,True"
		elif issilent and isnoirc:
			po = "self.silent,self.noirc = True,True"
		elif isnowindows and isnoirc:
			po = "self.nowindows,self.noirc = True,True"
		elif isnoirc:
			po = "self.noirc = True"
		elif issilent:
			po = "self.silent = True"
		elif isnowindows:
			po = "self.nowindows = True"
		else:
			po = ""
		t = t.replace(PLUGIN_OPTIONS,po)

		self.editor.insertPlainText(t)
		#self.editor.appendPlainText(t)



	def doPrivateCommand(self):
		x = CommandDialog.Dialog()
		pinfo = x.get_plugin_information(parent=self)

		if not pinfo: return

		classname = pinfo[0]
		name = pinfo[1]
		version = pinfo[2]
		description = pinfo[3]
		trigger = pinfo[4]
		issilent = pinfo[5]
		isnowindows = pinfo[6]
		isnoirc = pinfo[7]

		argcount = pinfo[8]

		# Strip forbidden characters from classname
		classname = classname.translate(str.maketrans('', '', string.punctuation))
		classname = classname.translate(str.maketrans('', '', string.whitespace))

		errs = []
		if len(classname)==0: errs.append("class name not entered")
		if len(name)==0: errs.append("name not entered")
		if len(version)==0: errs.append("version not entered")
		if len(description)==0: errs.append("description not entered")
		if len(trigger)==0: errs.append("command name not entered")

		if classname.isspace(): errs.append("class name is blank")
		if name.isspace(): errs.append("name is blank")
		if version.isspace(): errs.append("version is blank")
		if description.isspace(): errs.append("description is blank")
		if trigger.isspace(): errs.append("command name is blank")

		if len(errs)>0:
			msg = QMessageBox()
			msg.setWindowIcon(QIcon(EDIT_ICON))
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Missing or Invalid Input")
			es = ""
			for e in errs: es = es + f"<li>{e}</li>"
			msg.setInformativeText(f"<ul>{es}</ul>")
			msg.setWindowTitle("Can't inject command template")
			msg.exec_()
			return

		i = TEMPLATE_MODULE_LOAD
		if i in self.editor.toPlainText():
			pass
		else:
			self.editor.insertPlainText(f"{i}\n")

		i = "import shlex"
		if i in self.editor.toPlainText():
			pass
		else:
			self.editor.insertPlainText(f"{i}\n")

		self.injectPrivateCommand(classname,name,version,description,trigger,issilent,isnowindows,isnoirc,argcount)

	def injectPrivateCommand(self,classname,name,version,description,trigger,issilent,isnowindows,isnoirc,argcount):

		# Escape any double quotes
		description = description.replace('"',r'\"')
		name = name.replace('"',r'\"')

		t = PRIVATE_COMMAND_SKELETON
		t = t.replace(PLUGIN_CLASS,classname)
		t = t.replace(PLUGIN_NAME,name)
		t = t.replace(PLUGIN_VERSION,version)
		t = t.replace(PLUGIN_DESCRIPTION,description)
		t = t.replace(PLUGIN_TRIGGER,trigger)

		t = t.replace(PLUGIN_ARGCOUNT,str(argcount))

		if issilent and isnowindows and isnoirc:
			po = "self.silent,self.nowindows,self.noirc = True,True,True"
		elif issilent and isnowindows:
			po = "self.silent,self.nowindows = True,True"
		elif issilent and isnoirc:
			po = "self.silent,self.noirc = True,True"
		elif isnowindows and isnoirc:
			po = "self.nowindows,self.noirc = True,True"
		elif isnoirc:
			po = "self.noirc = True"
		elif issilent:
			po = "self.silent = True"
		elif isnowindows:
			po = "self.nowindows = True"
		else:
			po = ""
		t = t.replace(PLUGIN_OPTIONS,po)

		# self.editor.appendPlainText(t)
		self.editor.insertPlainText(t)





	def injectCommand(self,classname,name,version,description,trigger,issilent,isnowindows,isnoirc,argcount):

		# Escape any double quotes
		description = description.replace('"',r'\"')
		name = name.replace('"',r'\"')

		t = COMMAND_SKELETON
		t = t.replace(PLUGIN_CLASS,classname)
		t = t.replace(PLUGIN_NAME,name)
		t = t.replace(PLUGIN_VERSION,version)
		t = t.replace(PLUGIN_DESCRIPTION,description)
		t = t.replace(PLUGIN_TRIGGER,trigger)

		t = t.replace(PLUGIN_ARGCOUNT,str(argcount))

		if issilent and isnowindows and isnoirc:
			po = "self.silent,self.nowindows,self.noirc = True,True,True"
		elif issilent and isnowindows:
			po = "self.silent,self.nowindows = True,True"
		elif issilent and isnoirc:
			po = "self.silent,self.noirc = True,True"
		elif isnowindows and isnoirc:
			po = "self.nowindows,self.noirc = True,True"
		elif isnoirc:
			po = "self.noirc = True"
		elif issilent:
			po = "self.silent = True"
		elif isnowindows:
			po = "self.nowindows = True"
		else:
			po = ""
		t = t.replace(PLUGIN_OPTIONS,po)

		#self.editor.appendPlainText(t)
		self.editor.insertPlainText(t)

	def hasUndo(self,avail):
		if avail:
			self.meun.setEnabled(True)
		else:
			self.meun.setEnabled(False)

	def hasRedo(self,avail):
		if avail:
			self.mere.setEnabled(True)
		else:
			self.mere.setEnabled(False)

	def hasCopy(self,avail):
		if avail:
			self.mecopy.setEnabled(True)
			self.mecut.setEnabled(True)
		else:
			self.mecopy.setEnabled(False)
			self.mecut.setEnabled(False)

	def doFind(self):

		if self.findWindow != None:
			self.findWindow.showNormal()
			return

		if self.parent==None:
			self.findWindow = FindWindow.Viewer(self,True)
			self.findWindow.show()
			return

		x = self.parent.newFindWindow(self)

	def setFindWindow(self,obj):
		self.findWindow = obj

	def toggleFindtop(self):
		if self.findOnTop:
			self.findOnTop = False
			if self.findWindow != None:
				self.findWindow.setWindowFlags(self.findWindow.windowFlags() & ~Qt.WindowStaysOnTopHint)
		else:
			self.findOnTop = True
			if self.findWindow != None:
				self.findWindow.setWindowFlags(self.findWindow.windowFlags() | Qt.WindowStaysOnTopHint)
		self.settings[EDITOR_FIND_ON_TOP] = self.findOnTop
		save_editor_settings(self.settings)

	def toggleWrap(self):
		if self.wordwrap:
			self.wordwrap = False
			self.editor.setWordWrapMode(QTextOption.NoWrap)
			self.editor.update()
			self.update()
		else:
			self.wordwrap = True
			self.editor.setWordWrapMode(QTextOption.WordWrap)
			self.editor.update()
			self.update()

		self.settings[EDITOR_WORD_WRAP_SETTING] = self.wordwrap
		save_editor_settings(self.settings)

	def getFont(self):
		font, ok = QFontDialog.getFont()
		if ok:

			self.editor.setFont(font)

			self.settings[EDITOR_FONT_SETTING] = font.toString()
			save_editor_settings(self.settings)

	def contextMenu(self,location):
		#print(location)
		menu = self.editor.createStandardContextMenu()

		# Custom menu stuff here
		
		menu.addSeparator()

		#funcMenu = menu.addMenu(QIcon(CHANNEL_WINDOW_ICON),"IRC function calls")
		funcMenu = QMenu("IRC function calls")
		funcMenu.setIcon(QIcon(CHANNEL_WINDOW_ICON))
		menu.insertMenu(menu.actions()[0],funcMenu)

		plugCmdMsg = QAction(QIcon(PUBLIC_ICON),"msg()",self)
		plugCmdMsg.triggered.connect(lambda state,f="msg": self.generateMsgFunctionCall(f))
		funcMenu.addAction(plugCmdMsg)

		plugCmdNotice = QAction(QIcon(PUBLIC_ICON),"notice()",self)
		plugCmdNotice.triggered.connect(lambda state,f="notice": self.generateMsgFunctionCall(f))
		funcMenu.addAction(plugCmdNotice)

		plgCmdAction = QAction(QIcon(PUBLIC_ICON),"action()",self)
		plgCmdAction.triggered.connect(lambda state,f="action": self.generateMsgFunctionCall(f))
		funcMenu.addAction(plgCmdAction)

		plugCmdJoin = QAction(QIcon(CHANNEL_WINDOW_ICON),"join()",self)
		plugCmdJoin.triggered.connect(self.generateJoinFunctionCall)
		funcMenu.addAction(plugCmdJoin)

		plugCmdPart = QAction(QIcon(CHANNEL_WINDOW_ICON),"part()",self)
		plugCmdPart.triggered.connect(self.generatePartFunctionCall)
		funcMenu.addAction(plugCmdPart)

		plugCmdAway = QAction(QIcon(USER_ICON),"away()",self)
		plugCmdAway.triggered.connect(self.generateAwayFunctionCall)
		funcMenu.addAction(plugCmdAway)

		plgCmdBack = QAction(QIcon(USER_ICON),"back()",self)
		plgCmdBack.triggered.connect(lambda state: self.editor.insertPlainText("self.back()"))
		funcMenu.addAction(plgCmdBack)

		plugCmdColor = QAction(QIcon(FONT_ICON),"color()",self)
		plugCmdColor.triggered.connect(self.generateColorFunctionCall)
		funcMenu.addAction(plugCmdColor)

		plugCmdMode = QAction(QIcon(CHANNEL_WINDOW_ICON),"mode()",self)
		plugCmdMode.triggered.connect(self.generateModeFunctionCall)
		funcMenu.addAction(plugCmdMode)

		#erkMenu = menu.addMenu(QIcon(ERK_ICON),"Client function calls")
		erkMenu = QMenu("Client function calls")
		erkMenu.setIcon(QIcon(ERK_ICON))
		menu.insertMenu(menu.actions()[0],erkMenu)

		plugCmdPrint = QAction(QIcon(WINDOW_ICON),"print()",self)
		plugCmdPrint.triggered.connect(self.generatePrintFunctionCall)
		erkMenu.addAction(plugCmdPrint)

		menu.insertSeparator(menu.actions()[2])

		action = menu.exec_(self.editor.mapToGlobal(location))

	def __init__(self,filename=None,parent=None):
		super(Viewer, self).__init__(parent)

		self.parent = parent
		self.filename = ''
		self.title = EDITOR_NAME
		self.count = 0
		self.subwindow = None

		self.findWindow = None

		self.wordwrap = True

		self.findOnTop = True

		self.settings = get_editor_settings()
		self.wordwrap = self.settings[EDITOR_WORD_WRAP_SETTING]
		self.font = self.settings[EDITOR_FONT_SETTING]
		self.findOnTop = self.settings[EDITOR_FIND_ON_TOP]

		self.setWindowTitle(self.title)
		self.setWindowIcon(QIcon(EDIT_ICON))

		self.editor = QCodeEditor(self)
		self.highlight = PythonHighlighter(self.editor.document())

		self.editor.textChanged.connect(self.docModified)
		self.editor.redoAvailable.connect(self.hasRedo)
		self.editor.undoAvailable.connect(self.hasUndo)
		self.editor.copyAvailable.connect(self.hasCopy)

		self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
		self.editor.customContextMenuRequested.connect(self.contextMenu)

		f = QFont()
		f.fromString(self.font)
		self.editor.setFont(f)

		self.setCentralWidget(self.editor)

		if self.wordwrap:
			self.editor.setWordWrapMode(QTextOption.WordWrap)
		else:
			self.editor.setWordWrapMode(QTextOption.NoWrap)

		self.indentspace = self.settings[EDITOR_SPACES_TAB_SETTING]
		self.tabsize = self.settings[EDITOR_NUMBER_OF_SPACES]

		self.menubar = self.menuBar()
		self.changed = False

		fileMenu = self.menubar.addMenu("File")

		mnf = QAction(QIcon(NEWFILE_ICON),"New file",self)
		mnf.triggered.connect(self.doNewFile)
		mnf.setShortcut("Ctrl+N")
		fileMenu.addAction(mnf)

		mop = QAction(QIcon(OPEN_ICON),"Open file",self)
		mop.triggered.connect(self.doFileOpen)
		mop.setShortcut("Ctrl+O")
		fileMenu.addAction(mop)

		fileMenu.addSeparator()

		self.msav = QAction(QIcon(SAVE_ICON),"Save file",self)
		self.msav.triggered.connect(self.doFileSave)
		self.msav.setShortcut("Ctrl+S")
		fileMenu.addAction(self.msav)
		self.msav.setEnabled(False)

		msava = QAction(QIcon(SAVEAS_ICON),"Save as...",self)
		msava.triggered.connect(self.doFileSaveAs)
		fileMenu.addAction(msava)

		fileMenu.addSeparator()

		mex = QAction(QIcon(EXIT_ICON),"Exit",self)
		mex.triggered.connect(self.close)
		fileMenu.addAction(mex)

		editMenu = self.menubar.addMenu("Edit")

		mefind = QAction(QIcon(WHOIS_ICON),"Find",self)
		mefind.triggered.connect(self.doFind)
		mefind.setShortcut("Ctrl+F")
		editMenu.addAction(mefind)

		editMenu.addSeparator()

		mesela = QAction(QIcon(SELECTALL_ICON),"Select All",self)
		mesela.triggered.connect(self.editor.selectAll)
		mesela.setShortcut("Ctrl+A")
		editMenu.addAction(mesela)

		editMenu.addSeparator()

		self.meun = QAction(QIcon(UNDO_ICON),"Undo",self)
		self.meun.triggered.connect(self.editor.undo)
		self.meun.setShortcut("Ctrl+Z")
		editMenu.addAction(self.meun)
		self.meun.setEnabled(False)

		self.mere = QAction(QIcon(REDO_ICON),"Redo",self)
		self.mere.triggered.connect(self.editor.redo)
		self.mere.setShortcut("Ctrl+Y")
		editMenu.addAction(self.mere)
		self.mere.setEnabled(False)

		editMenu.addSeparator()

		self.mecut = QAction(QIcon(CUT_ICON),"Cut",self)
		self.mecut.triggered.connect(self.editor.cut)
		self.mecut.setShortcut("Ctrl+X")
		editMenu.addAction(self.mecut)
		self.mecut.setEnabled(False)

		self.mecopy = QAction(QIcon(COPY_ICON),"Copy",self)
		self.mecopy.triggered.connect(self.editor.copy)
		self.mecopy.setShortcut("Ctrl+C")
		editMenu.addAction(self.mecopy)
		self.mecopy.setEnabled(False)

		mepaste = QAction(QIcon(CLIPBOARD_ICON),"Paste",self)
		mepaste.triggered.connect(self.editor.paste)
		mepaste.setShortcut("Ctrl+V")
		editMenu.addAction(mepaste)

		editMenu.addSeparator()

		mezoomin = QAction(QIcon(PLUS_ICON),"Zoom in",self)
		mezoomin.triggered.connect(self.editor.zoomIn)
		mezoomin.setShortcut("Ctrl++")
		editMenu.addAction(mezoomin)

		mezoomout = QAction(QIcon(MINUS_ICON),"Zoom out",self)
		mezoomout.triggered.connect(self.editor.zoomOut)
		mezoomout.setShortcut("Ctrl+-")
		editMenu.addAction(mezoomout)

		pluginsMenu = self.menubar.addMenu("Templates")

		mist = QAction(QIcon(PLUGIN_ICON),"Insert plugin template",self)
		mist.triggered.connect(self.doTemplate)
		pluginsMenu.addAction(mist)

		miscc = QAction(QIcon(COMMAND_ICON), f"Insert {APPLICATION_NAME} command template",self)
		miscc.triggered.connect(self.doCommand)
		pluginsMenu.addAction(miscc)

		mispub = QAction(QIcon(PUBLIC_ICON),"Insert public command template",self)
		mispub.triggered.connect(self.doPublicCommand)
		pluginsMenu.addAction(mispub)

		mispriv = QAction(QIcon(PRIVATE_ICON),"Insert private command template",self)
		mispriv.triggered.connect(self.doPrivateCommand)
		pluginsMenu.addAction(mispriv)

		settingsMenu = self.menubar.addMenu("Settings")

		optFont = QAction(QIcon(FONT_ICON),"Set font",self)
		optFont.triggered.connect(self.getFont)
		settingsMenu.addAction(optFont)

		self.optWrap = QAction(QIcon(WRAP_ICON),"Word wrap",self,checkable=True)
		self.optWrap.setChecked(self.wordwrap)
		self.optWrap.triggered.connect(self.toggleWrap)
		settingsMenu.addAction(self.optWrap)

		numIndentMenu = settingsMenu.addMenu(QIcon(INDENT_ICON),"Indentation")

		self.tabs = QAction("Use tabs",self,checkable=True)
		self.tabs.triggered.connect(lambda state,f=0: self.setSpaceIndent(f))
		numIndentMenu.addAction(self.tabs)

		numIndentMenu.addSeparator()

		self.opt1 = QAction("Use 1 space",self,checkable=True)
		self.opt1.triggered.connect(lambda state,f=1: self.setSpaceIndent(f))
		numIndentMenu.addAction(self.opt1)

		self.opt2 = QAction("Use 2 spaces",self,checkable=True)
		self.opt2.triggered.connect(lambda state,f=2: self.setSpaceIndent(f))
		numIndentMenu.addAction(self.opt2)

		self.opt3 = QAction("Use 3 spaces",self,checkable=True)
		self.opt3.triggered.connect(lambda state,f=3: self.setSpaceIndent(f))
		numIndentMenu.addAction(self.opt3)

		self.opt4 = QAction("Use 4 spaces",self,checkable=True)
		self.opt4.triggered.connect(lambda state,f=4: self.setSpaceIndent(f))
		numIndentMenu.addAction(self.opt4)

		self.opt5 = QAction("Use 5 spaces",self,checkable=True)
		self.opt5.triggered.connect(lambda state,f=5: self.setSpaceIndent(f))
		numIndentMenu.addAction(self.opt5)

		if self.indentspace:
			if self.tabsize==1:
				self.opt1.setChecked(True)
			elif self.tabsize==2:
				self.opt2.setChecked(True)
			elif self.tabsize==3:
				self.opt3.setChecked(True)
			elif self.tabsize==4:
				self.opt4.setChecked(True)
			elif self.tabsize==5:
				self.opt5.setChecked(True)
		else:
			self.tabs.setChecked(True)

		settingsMenu.addSeparator()

		self.optFind = QAction("Find window always on top",self,checkable=True)
		self.optFind.setChecked(self.findOnTop)
		self.optFind.triggered.connect(self.toggleFindtop)
		settingsMenu.addAction(self.optFind)

		#settingsMenu.addSeparator()

		# preload = QAction(QIcon(LOAD_ICON),"Load new packages",self)
		# preload.triggered.connect(lambda state: self.parent.reloadPlugins())
		# settingsMenu.addAction(preload)

		# prestart = QAction(QIcon(RESTART_ICON),"Restart Erk",self)
		# prestart.triggered.connect(lambda state: restart_program())
		# settingsMenu.addAction(prestart)

		# Add window to master window list
		self.parent.editor_windows.append(self)

		if filename!=None:
			self.filename = filename
			script = open(filename,"r")
			self.editor.setPlainText(script.read())
			self.title = f"{EDITOR_NAME} - " + os.path.basename(filename)
			self.setWindowTitle(self.title)
			self.parent.updateActiveChild(self.parent.MDI.activeSubWindow())
			self.msav.setEnabled(True)

	def generateMsgFunctionCall(self,ctype):
		x = CommandMsgDialog.Dialog(ctype,self)
		data = x.get_cmd_information(ctype,self)

		# User cancled dialog
		if not data: return

		target = data[0]
		msg = data[1]
		sid = data[2]

		# Escape double quotes in msg
		msg = msg.replace('"',r"\"")

		if len(sid)>0:
			code = f"self.{ctype}(\"{target}\",\"{msg}\",\"{sid}\")"
		else:
			code = f"self.{ctype}(\"{target}\",\"{msg}\")"

		self.editor.insertPlainText(code)

	def generateJoinFunctionCall(self):
		x = CommandJoinDialog.Dialog(self)
		data = x.get_cmd_information(self)

		# User cancled dialog
		if not data: return

		channel = data[0]
		key = data[1]
		sid = data[2]

		# Escape double quotes in key
		key = key.replace('"',r"\"")

		if len(key)>0:
			if len(sid)>0:
				code = f"self.join(\"{channel}\",\"{key}\",\"{sid}\")"
			else:
				code = f"self.join(\"{channel}\",\"{key}\")"
		else:
			if len(sid)>0:
				code = f"self.join(\"{channel}\",None,\"{sid}\")"
			else:
				code = f"self.join(\"{channel}\")"

		self.editor.insertPlainText(code)

	def generatePartFunctionCall(self):
		x = CommandPartDialog.Dialog(self)
		data = x.get_cmd_information(self)

		# User cancled dialog
		if not data: return

		channel = data[0]
		msg = data[1]
		sid = data[2]

		# Escape double quotes in msg
		msg = msg.replace('"',r"\"")

		if len(msg)>0:
			if len(sid)>0:
				code = f"self.part(\"{channel}\",\"{msg}\",\"{sid}\")"
			else:
				code = f"self.part(\"{channel}\",\"{msg}\")"
		else:
			if len(sid)>0:
				code = f"self.part(\"{channel}\",None,\"{sid}\")"
			else:
				code = f"self.part(\"{channel}\")"

		self.editor.insertPlainText(code)
		

	# generatePrintFunctionCall
	def generatePrintFunctionCall(self):
		x = CommandPrintDialog.Dialog(self)
		data = x.get_cmd_information(self)

		# User cancled dialog
		if not data: return

		text = data[0]
		target = data[1]

		# Escape double quotes in text
		text = text.replace('"',r"\"")

		if target=="active":
			code = f"self.print(\"{text}\")"
		elif target=="all":
			code = f"self.print(\"{text}\",\"all\")"
		elif target=="log":
			code = f"self.print(\"{text}\",\"log\")"

		self.editor.insertPlainText(code)

	def generateColorFunctionCall(self):
		x = CommandColorDialog.Dialog(self)
		data = x.get_cmd_information(self)

		# User cancled dialog
		if not data: return

		text = data[0]
		fore = int(data[1])
		back = data[2]

		# Escape double quotes in text
		text = text.replace('"',r"\"")

		if back!="None":
			back = int(back)
			code = f"self.color(\"{text}\",{fore},{back})"
		else:
			code = f"self.color(\"{text}\",{fore})"

		self.editor.insertPlainText(code)

	def generateAwayFunctionCall(self):
		x = CommandAwayDialog.Dialog(self)
		data = x.get_cmd_information(self)

		# User cancled dialog
		if not data: return

		# Escape double quotes in text
		text = data.replace('"',r"\"")

		if text!="____blank____":
			code = f"self.away(\"{text}\")"
		else:
			code = f"self.away()"

		self.editor.insertPlainText(code)

	def generateModeFunctionCall(self):
		x = CommandModeDialog.Dialog(self)
		data = x.get_cmd_information(self)

		# User cancled dialog
		if not data: return

		setOrUnset = data[0]
		target = data[1]
		modes = data[2]
		limit = data[3]
		user = data[4]
		mask = data[5]
		serverid = data[6]

		if setOrUnset:
			setOrUnset = "True"
		else:
			setOrUnset = "False"

		if not len(limit)>0:
			limit = "None"
		else:
			limit = f"\"{limit}\""

		if not len(user)>0:
			user = "None"
		else:
			user = f"\"{user}\""

		if not len(mask)>0:
			mask = "None"
		else:
			mask = f"\"{mask}\""

		if not len(serverid)>0:
			serverid = "None"
		else:
			serverid = f"\"{serverid}\""

		code = f"self.mode(\"{target}\",{setOrUnset},\"{modes}\",{limit},{user},{mask},{serverid})"
		self.editor.insertPlainText(code)


		# # Escape double quotes in text
		# text = data.replace('"',r"\"")

		# if text!="____blank____":
		# 	code = f"self.away(\"{text}\")"
		# else:
		# 	code = f"self.away()"

		# self.editor.insertPlainText(code)

	def setSpaceIndent(self,num):
		if num>0:
			self.indentspace = True
			self.tabsize = num
			self.tabs.setChecked(False)
		else:
			self.indentspace = False
			self.tabs.setChecked(True)

		self.settings[EDITOR_SPACES_TAB_SETTING] = self.indentspace
		self.settings[EDITOR_NUMBER_OF_SPACES] = self.tabsize
		save_editor_settings(self.settings)

		self.opt2.setChecked(False)
		self.opt3.setChecked(False)
		self.opt4.setChecked(False)
		self.opt5.setChecked(False)

		if num==2:
			self.opt2.setChecked(True)
		elif num==3:
			self.opt3.setChecked(True)
		elif num==4:
			self.opt4.setChecked(True)
		elif num==5:
			self.opt5.setChecked(True)
