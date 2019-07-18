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

		self.setWindowTitle(f" Version {APPLICATION_VERSION}")
		self.setWindowIcon(QIcon(ERK_ICON))

		boldfont = self.font()
		boldfont.setBold(True)
		boldfont.setPointSize(10)

		boldsmaller = self.font()
		boldsmaller.setBold(True)
		boldsmaller.setPointSize(8)

		logo = QLabel()
		pixmap = QPixmap(ERK_BANNER_LOGO)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		qt_image = QLabel()
		pixmap = QPixmap(QT_IMAGE)
		qt_image.setPixmap(pixmap)
		qt_image.setAlignment(Qt.AlignCenter)

		python_image = QLabel()
		pixmap = QPixmap(PYTHON_IMAGE)
		python_image.setPixmap(pixmap)
		python_image.setAlignment(Qt.AlignCenter)

		twisted_image = QLabel()
		pixmap = QPixmap(TWISTED_IMAGE)
		twisted_image.setPixmap(pixmap)
		twisted_image.setAlignment(Qt.AlignCenter)

		icons8_image = QLabel()
		pixmap = QPixmap(ICONS8_IMAGE)
		icons8_image.setPixmap(pixmap)
		icons8_image.setAlignment(Qt.AlignCenter)

		pyBox = QVBoxLayout()
		pyBox.addWidget(python_image)
		pyLink = QLabel("<a href=\"https://www.python.org/\">Python</a>")
		pyLink.setAlignment(Qt.AlignCenter)
		pyBox.addWidget(pyLink)
		pyLink.setFont(boldsmaller)
		pyLink.setOpenExternalLinks(True)

		qtBox = QVBoxLayout()
		qtBox.addWidget(qt_image)
		qtLink = QLabel("<a href=\"https://www.qt.io/\">Qt</a>")
		qtLink.setAlignment(Qt.AlignCenter)
		qtBox.addWidget(qtLink)
		qtLink.setFont(boldsmaller)
		qtLink.setOpenExternalLinks(True)

		twistBox = QVBoxLayout()
		twistBox.addWidget(twisted_image)
		twistLink = QLabel("<a href=\"https://twistedmatrix.com\">Twisted</a>")
		twistLink.setAlignment(Qt.AlignCenter)
		twistBox.addWidget(twistLink)
		twistLink.setFont(boldsmaller)
		twistLink.setOpenExternalLinks(True)

		icons8Box = QVBoxLayout()
		icons8Box.addWidget(icons8_image)
		icons8Link = QLabel("<a href=\"https://icons8.com/\">Icons8</a>")
		icons8Link.setAlignment(Qt.AlignCenter)
		icons8Box.addWidget(icons8Link)
		icons8Link.setFont(boldsmaller)
		icons8Link.setOpenExternalLinks(True)

		technology = QHBoxLayout()
		technology.addLayout(pyBox)
		technology.addLayout(twistBox)
		technology.addLayout(qtBox)
		technology.addLayout(icons8Box)

		dinfo = QLabel(f"Open Source Internet Relay Chat Client")
		dinfo.setAlignment(Qt.AlignCenter)
		dinfo.setFont(boldfont)

		linfo = QLabel(f"<small>© Dan Hetrick 2019</small><br><a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><small>Gnu General Public License 3.0</small></a><br><a href=\"{OFFICIAL_REPOSITORY}\"><small>Official Erk Repository</small></a>")
		linfo.setAlignment(Qt.AlignCenter)
		linfo.setFont(boldfont)
		linfo.setOpenExternalLinks(True)

		scinfo = QLabel(f"<a href=\"https://github.com/barrust/pyspellchecker\">pyspellchecker</a> by <a href=\"mailto:barrust@gmail.com\">Tyler Barrus</a>")
		scinfo.setAlignment(Qt.AlignCenter)
		scinfo.setFont(boldfont)
		scinfo.setOpenExternalLinks(True)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(logo)
		finalLayout.addWidget(dinfo)
		finalLayout.addLayout(technology)
		finalLayout.addWidget(scinfo)
		finalLayout.addWidget(linfo)
		
		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
