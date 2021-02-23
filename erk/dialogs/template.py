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
from ..strings import *

class Dialog(QDialog):

	@staticmethod
	def get_name_information(title="Insert",parent=None):
		dialog = Dialog(title,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		if self.name.text().strip()=='':
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("Plugin name is required")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		if self.description.text().strip()=='':
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("Plugin description is required")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		author = self.author.text()
		if len(author.strip())==0: author = None

		version = self.version.text()
		if len(version.strip())==0: version = None

		website = self.website.text()
		if len(website.strip())==0: website = None

		retval = [self.name.text(),self.description.text(),author,version,website]

		return retval

	def __init__(self,title,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.title = title

		if title=="Insert":
			self.setWindowTitle("Insert template")
		else:
			self.setWindowTitle("Create package")
		self.setWindowIcon(QIcon(EDITOR_ICON))

		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)

		self.name = QLineEdit()
		self.description = QLineEdit()

		self.name.setPlaceholderText("Required")
		self.description.setPlaceholderText("Required")

		self.name.setMinimumWidth(wwidth)

		self.author = QLineEdit()
		self.version = QLineEdit()
		self.website = QLineEdit()

		self.author.setPlaceholderText("Optional")
		self.version.setPlaceholderText("Optional")
		self.website.setPlaceholderText("http://optional.com")

		n1 = QLabel("Name")
		n1.setFont(BOLD_FONT)

		n2 = QLabel("Description")
		n2.setFont(BOLD_FONT)

		n3 = QLabel("Author")
		n3.setFont(BOLD_FONT)

		n4 = QLabel("Version")
		n4.setFont(BOLD_FONT)

		n5 = QLabel("Website")
		n5.setFont(BOLD_FONT)

		infoLayout = QFormLayout()
		infoLayout.addRow(n1, self.name)
		infoLayout.addRow(n2, self.description)
		infoLayout.addRow(n3, self.author)
		infoLayout.addRow(n4, self.version)
		infoLayout.addRow(n5, self.website)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText(self.title)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(infoLayout)
		#finalLayout.addLayout(descriptionLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
