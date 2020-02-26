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
import erk.config

class Dialog(QDialog):

	@staticmethod
	def get_window_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = [ self.width.value(),self.height.value() ]

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Set initial window size")
		self.setWindowIcon(QIcon(RESIZE_ICON))

		widthLayout = QHBoxLayout()
		self.widthLabel = QLabel("Width")
		self.width = QSpinBox()
		self.width.setRange(100,2000)
		#self.width.setValue(erk.config.DEFAULT_APP_WIDTH)
		self.width.setValue(self.parent.width())
		widthLayout.addWidget(self.widthLabel)
		#widthLayout.addStretch()
		widthLayout.addWidget(self.width)
		widthLayout.addWidget(QLabel("pixels"))

		heightLayout = QHBoxLayout()
		self.heightLabel = QLabel("Height")
		self.height = QSpinBox()
		self.height.setRange(100,2000)
		# self.height.setValue(erk.config.DEFAULT_APP_HEIGHT)
		self.height.setValue(self.parent.height())
		heightLayout.addWidget(self.heightLabel)
		#heightLayout.addStretch()
		heightLayout.addWidget(self.height)
		heightLayout.addWidget(QLabel("pixels"))

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(widthLayout)
		finalLayout.addLayout(heightLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
