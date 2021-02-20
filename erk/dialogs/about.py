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

import platform
import twisted

from ..resources import *
from ..strings import *

class Dialog(QDialog):

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("About "+APPLICATION_NAME)
		self.setWindowIcon(QIcon(ABOUT_ICON))

		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)

		self.tabs = QTabWidget()

		self.tabs.setFont(BOLD_FONT)

		self.tabs.setStyleSheet("""
			QTabWidget::tab-bar { alignment: center; font: bold; }
			""")

		self.about_tab = QWidget()
		self.tabs.addTab(self.about_tab, "About")

		self.credits_tab = QWidget()
		self.tabs.addTab(self.credits_tab, "Credits")

		logo = QLabel()
		pixmap = QPixmap(ERK_BIG_ICON)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		nutjob = QLabel()
		pixmap = QPixmap(NUTJOB_LOGO)
		nutjob.setPixmap(pixmap)
		nutjob.setAlignment(Qt.AlignCenter)

		line1 = QLabel("<big><b>"+APPLICATION_NAME+" Open Source IRC Client</b></big>")
		line1.setAlignment(Qt.AlignCenter)
		line2 = QLabel("<b>\"It's How You Say IRC\"</b>")
		line2.setAlignment(Qt.AlignCenter)
		line3 = QLabel("<b>Version "+APPLICATION_VERSION+"</b>")
		line3.setAlignment(Qt.AlignCenter)
		line4 = QLabel(f"<a href=\"{OFFICIAL_REPOSITORY}\"><small>Source Code Repository</small></a>")
		line4.setAlignment(Qt.AlignCenter)
		line4.setOpenExternalLinks(True)

		descriptionLayout = QVBoxLayout()
		descriptionLayout.addWidget(line1)
		descriptionLayout.addWidget(line2)
		descriptionLayout.addWidget(line3)
		descriptionLayout.addWidget(line4)

		titleLayout = QVBoxLayout()
		titleLayout.addWidget(logo)
		titleLayout.addLayout(descriptionLayout)


		tech_credit = QLabel(f"<small>Written with </small><a href=\"https://python.org\"><small>Python</small></a><small>, </small><a href=\"https://www.qt.io/\"><small>Qt</small></a><small>, and </small><a href=\"https://twistedmatrix.com/\"><small>Twisted</small></a>")
		tech_credit.setAlignment(Qt.AlignCenter)
		tech_credit.setOpenExternalLinks(True)


		icons_credit = QLabel(f"<small>Icons by </small><a href=\"https://icons8.com/\"><small>Icons8</small></a><small> and </small><a href=\"https://material.io/resources/icons/\"><small>Google</small></a>")
		icons_credit.setAlignment(Qt.AlignCenter)
		icons_credit.setOpenExternalLinks(True)


		spellcheck_credit = QLabel(f"<a href=\"https://github.com/barrust/pyspellchecker\"><small>pyspellchecker</small></a><small> by </small><a href=\"mailto:barrust@gmail.com\"><small>Tyler Barrus</small></a>")
		spellcheck_credit.setAlignment(Qt.AlignCenter)
		spellcheck_credit.setOpenExternalLinks(True)

		emoji_credit = QLabel(f"<a href=\"https://github.com/carpedm20/emoji\"><small>emoji</small></a><small> by </small><a href=\"http://carpedm20.github.io/about/\"><small>Taehoon Kim</small></a><small> and </small><a href=\"http://twitter.com/geowurster/\"><small>Kevin Wurster</small></a>")
		emoji_credit.setAlignment(Qt.AlignCenter)
		emoji_credit.setOpenExternalLinks(True)

		gnu_credit = QLabel(f"<a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><small>Gnu General Public License 3.0</small></a>")
		gnu_credit.setAlignment(Qt.AlignCenter)
		gnu_credit.setOpenExternalLinks(True)

		plug_credit = QLabel(f"<a href=\"https://www.guidodiepen.nl/2019/02/implementing-a-simple-plugin-framework-in-python/\"><small>Plugin framework</small></a><small> inspired by </small><small>Guido Diepen</small>")
		plug_credit.setAlignment(Qt.AlignCenter)
		plug_credit.setOpenExternalLinks(True)

		syn_credit = QLabel(f"<a href=\"https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting\"><small>Syntax highlighting from the Python Wiki</a></small>")
		syn_credit.setAlignment(Qt.AlignCenter)
		syn_credit.setOpenExternalLinks(True)

		ce_credit = QLabel(f"<a href=\"https://stackoverflow.com/questions/40386194/create-text-area-textedit-with-line-number-in-pyqt\"><small>Code editor line numbers</a></small>")
		ce_credit.setAlignment(Qt.AlignCenter)
		ce_credit.setOpenExternalLinks(True)

		qr_credit = QLabel(f"<a href=\"https://github.com/twisted/qt5reactor\"><small>qt5reactor</small></a> <small>by Twisted Matrix Labs</small>")
		qr_credit.setAlignment(Qt.AlignCenter)
		qr_credit.setOpenExternalLinks(True)

		platform_credit = QLabel(f"<small><i>Running on "+ platform.system().strip() + " " + platform.release().strip() +"</i></small>")
		platform_credit.setAlignment(Qt.AlignCenter)

		# QT_VERSION_STR

		qtv_credit = QLabel(f"<small><i>Qt5, version " + str(QT_VERSION_STR) +"</i></small>")
		qtv_credit.setAlignment(Qt.AlignCenter)

		tv = str(twisted.version)
		tv = tv.replace('[','',1)
		tv = tv.replace(']','',1)
		tv = tv.strip()

		twv_credit = QLabel(f"<small><i>" + tv +"</i></small>")
		twv_credit.setAlignment(Qt.AlignCenter)

		pyv_credit = QLabel(f"<small><i>Python, version " + platform.python_version().strip() +"</i></small>")
		pyv_credit.setAlignment(Qt.AlignCenter)

		me_credit = QLabel(f"<small>Created and written by <a href=\"https://github.com/danhetrick\">Dan Hetrick</a></small>")
		me_credit.setAlignment(Qt.AlignCenter)
		me_credit.setOpenExternalLinks(True)

		# https://bit.ly/erk-irc

		bitly_credit = QLabel(f"<big><b><a href=\"https://bit.ly/erk-irc\">https://bit.ly/erk-irc</a></b></big>")
		bitly_credit.setAlignment(Qt.AlignCenter)
		bitly_credit.setOpenExternalLinks(True)

		creditsBox = QGroupBox()
		creditsBox.setAlignment(Qt.AlignHCenter)

		creditsLayout = QVBoxLayout()
		creditsLayout.addWidget(icons_credit)
		creditsLayout.addWidget(spellcheck_credit)
		creditsLayout.addWidget(emoji_credit)
		creditsLayout.addWidget(qr_credit)
		creditsLayout.addWidget(plug_credit)
		creditsLayout.addWidget(syn_credit)
		creditsLayout.addWidget(ce_credit)
		creditsBox.setLayout(creditsLayout)

		okButton = QPushButton("Ok")
		okButton.clicked.connect(self.close)

		#self.about_tab = QWidget()
		#self.credits_tab = QWidget()

		aboutLayout = QVBoxLayout()
		aboutLayout.addLayout(titleLayout)
		aboutLayout.addWidget(tech_credit)
		aboutLayout.addWidget(gnu_credit)
		aboutLayout.addWidget(platform_credit)

		self.about_tab.setLayout(aboutLayout)

		credLayout = QVBoxLayout()
		credLayout.addWidget(nutjob)
		credLayout.addWidget(me_credit)
		credLayout.addWidget(bitly_credit)
		credLayout.addWidget(creditsBox)
		credLayout.addWidget(pyv_credit)
		credLayout.addWidget(qtv_credit)
		credLayout.addWidget(twv_credit)

		credLayout.addStretch()
		
		self.credits_tab.setLayout(credLayout)

		finalLayout = QVBoxLayout()
		# finalLayout.addLayout(titleLayout)
		# finalLayout.addWidget(tech_credit)
		# finalLayout.addWidget(gnu_credit)
		# finalLayout.addWidget(creditsBox)
		# finalLayout.addWidget(platform_credit)
		finalLayout.addWidget(self.tabs)
		finalLayout.addWidget(okButton)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
