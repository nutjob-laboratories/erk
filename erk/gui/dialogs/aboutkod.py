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

from erk.common import *

class Dialog(QDialog):

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle(f" Version {EDITOR_VERSION}")
		self.setWindowIcon(QIcon(EDIT_ICON))

		boldfont = self.font()
		boldfont.setBold(True)
		boldfont.setPointSize(10)

		boldsmaller = self.font()
		boldsmaller.setBold(True)
		boldsmaller.setPointSize(8)

		logo = QLabel()
		pixmap = QPixmap(KOD_LOGO_IMAGE)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		dinfo = QLabel(f"{APPLICATION_NAME} Plugin Editor")
		dinfo.setAlignment(Qt.AlignCenter)
		dinfo.setFont(boldfont)

		linfo = QLabel(f"<small>© Dan Hetrick 2019</small><br><a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><small>Gnu General Public License 3.0</small></a><br><a href=\"{OFFICIAL_REPOSITORY}\"><small>Official Erk Repository</small></a>")
		linfo.setAlignment(Qt.AlignCenter)
		linfo.setFont(boldfont)
		linfo.setOpenExternalLinks(True)

		sinfo = QLabel(f"<small>{PYTHON_IMPLEMENTATION} {PYTHON_VERSION} - Qt {QT_VERSION_STR} - PyQt {PYQT_VERSION_STR}</small>")
		sinfo.setAlignment(Qt.AlignCenter)
		sinfo.setFont(boldfont)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(logo)
		finalLayout.addWidget(dinfo)
		finalLayout.addWidget(sinfo)
		finalLayout.addWidget(linfo)
		
		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
