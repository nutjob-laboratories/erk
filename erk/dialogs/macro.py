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
from erk.objects import *
from erk.files import *
from erk.widgets import *
from erk.strings import *

import erk.macros

class Dialog(QDialog):

	def setType(self):

		index = self.type.currentIndex()
		self.output_type = self.type.itemText(index)

	def clickExecute(self,state):
		if state == Qt.Checked:
			self.do_execute = True
		else:
			self.do_execute = False

	def saveMacro(self):

		trigger = self.trigger.text()
		output = self.output.text()
		mtype = self.output_type
		argc = self.argc.value()
		exe = self.do_execute

		macro = {
			"trigger": trigger,
			"output": output,
			"type": mtype,
			"arguments": argc,
			"execute": exe
		}

		if self.filename:
			erk.macros.save_macro(macro,self.filename)
			self.parent.rebuildMacroMenu()
			self.close()
		else:
			fileName, _ = QFileDialog.getSaveFileName(self,"Save macro as...",erk.macros.MACRO_DIRECTORY,"JSON Files (*.json)")
			if fileName:
				erk.macros.save_macro(macro,fileName)
				self.parent.rebuildMacroMenu()
				self.close()


	def __init__(self,filename=None,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.filename = filename

		self.output_type = "privmsg"
		self.do_execute = False

		macroLayout = QFormLayout()

		self.trigger = QLineEdit()
		self.output = QLineEdit()

		self.argc = QSpinBox()
		self.argc.setRange(0,100)
		self.argc.setValue(0)

		self.type = QComboBox(self)
		self.type.activated.connect(self.setType)
		self.type.addItem("privmsg")
		self.type.addItem("action")
		self.type.addItem("notice")
		self.type.addItem("command")

		self.execute = QCheckBox(self)
		self.execute.stateChanged.connect(self.clickExecute)

		macroLayout.addRow(QLabel("<small>The word that will \"trigger\" the macro</small>"))

		macroLayout.addRow(QLabel("<b>Trigger</b>"), self.trigger)

		macroLayout.addRow(QLabel("<small>How many arguments the macro will accept</small>"))

		macroLayout.addRow(QLabel("<b>Number of arguments</b>"), self.argc)

		typeDesc = QLabel("<small>Set to <i><b>privmsg</b></i> to send the macro as a message; set to <i><b>action</b></i> to send the macro as a CTCP action message; set to <i><b>notice</b></i> to send the macro as a notice; set to <i><b>command</b></i> to interpret the macro as a command</small>")

		typeDesc.setWordWrap(True)
		macroLayout.addRow(typeDesc)

		macroLayout.addRow(QLabel("<b>Macro type</b>"), self.type)

		exeDesc = QLabel("<small>If set to execute immediately, the macro will be processed immediately; if not, the macro's output will be inserted into the window's text entry</small>")

		exeDesc.setWordWrap(True)
		macroLayout.addRow(exeDesc)

		macroLayout.addRow(QLabel("<b>Execute immediately</b>"), self.execute)

		outDesc = QLabel("<small>Macro arguments will be interpolated into the output. Use <i><b>$</b></i> to insert arguments; the first <i><b>$</b></i> will be replaced with the first macro argument, and so on. To insert an actual \"$\" symbol into the output, use \"$$\".</small>")
		outDesc.setWordWrap(True)
		macroLayout.addRow(outDesc)

		macroLayout.addRow(QLabel("<small><u><b>Special Variables</b></u></small>"),QLabel("<small><u><b>Description</b></u></small>"))

		chanDesc = QLabel("<small>The name of the channel window where the macro was triggered</small>")
		chanDesc.setWordWrap(True)

		servDesc = QLabel("<small>Address used to connect to the IRC server</small>")
		servDesc.setWordWrap(True)

		macroLayout.addRow(QLabel("<small><i><b>$channel</b></i></small>"), chanDesc)
		macroLayout.addRow(QLabel("<small><i><b>$server</b></i></small>"), servDesc)
		macroLayout.addRow(QLabel("<small><i><b>$port</b></i></small>"), QLabel("<small>Port connected to</small>"))
		macroLayout.addRow(QLabel("<small><i><b>$hostname</b></i></small>"), QLabel("<small>The server's hostname</small>"))
		macroLayout.addRow(QLabel("<small><i><b>$network</b></i></small>"), QLabel("<small>The server's network</small>"))
		macroLayout.addRow(QLabel("<small><i><b>$self</b></i></small>"), QLabel("<small>Your nickname</small>"))

		macroLayout.addRow(QLabel("<b>Output</b>"), self.output)

		if self.filename:
			m = erk.macros.get_macro(self.filename)

			if m:
				self.setWindowTitle("Edit "+m["trigger"])

				self.trigger.setText(m["trigger"])
				self.output.setText(m["output"])

				pi = self.type.findText("privmsg")
				ai = self.type.findText("action")
				ci = self.type.findText("command")
				ni = self.type.findText("notice")

				if m["type"]=="privmsg": self.type.setCurrentIndex(pi)
				if m["type"]=="action": self.type.setCurrentIndex(ai)
				if m["type"]=="command": self.type.setCurrentIndex(ci)
				if m["type"]=="notice": self.type.setCurrentIndex(ni)

				self.argc.setValue(int(m["arguments"]))

				if m["execute"]: self.execute.toggle()
		else:
			self.setWindowTitle("Create new macro")

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.saveMacro)
		buttons.rejected.connect(self.close)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(macroLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)


		
