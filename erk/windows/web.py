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

import pathlib

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import *

from erk.common import *

class Window(QMainWindow):

	def closeEvent(self, event):
		self.gui.browser_window = None
		self.gui.buildWindowMenu()
		self.subwindow.close()
		self.close()
		event.accept()

	def webTitleChanged(self,title):
		self.setWindowTitle(" "+title)
		self.title = title
		self.gui.buildWindowMenu()

	def webIconChanged(self,icon):
		self.setWindowIcon(icon)

	def enteredUrl(self):
		self.url = self.url_entry.text()
		self.web.load(QtCore.QUrl.fromUserInput(f"{self.url}"))
		self.gui.buildWindowMenu()

	def webUrlChanged(self,url):
		self.url_entry.setText(url.toString())
		self.url = url.toString()
		self.gui.buildWindowMenu()

	def navigate(self,url):
		self.web.load(QtCore.QUrl.fromUserInput(f"{url}"))
		self.url = url

	def __init__(self,url,subwindow,parent=None):
		super(Window, self).__init__()

		self.subwindow = subwindow
		self.gui = parent
		self.url = url
		self.title = url

		self.setWindowTitle(" "+url)

		self.web = QWebEngineView(self)

		self.toolbar = QToolBar(self)
		self.toolbar.setMovable(False)

		self.stopButton = QPushButton()
		self.stopButton.setIcon(QIcon(STOP_ICON))
		self.stopButton.clicked.connect(self.web.stop)

		self.backButton = QPushButton()
		self.backButton.setIcon(QIcon(BACK_ICON))
		self.backButton.clicked.connect(self.web.back)

		self.forwardButton = QPushButton()
		self.forwardButton.setIcon(QIcon(FORWARD_ICON))
		self.forwardButton.clicked.connect(self.web.forward)

		self.url_entry = QLineEdit()
		self.url_entry.setText(self.url)
		self.url_entry.returnPressed.connect(self.enteredUrl)

		toolLayout = QHBoxLayout()
		toolLayout.setContentsMargins(0,0,0,0)
		toolLayout.addWidget(self.stopButton)
		toolLayout.addWidget(self.backButton)
		toolLayout.addWidget(self.forwardButton)
		toolLayout.addWidget(self.url_entry)

		tools = QWidget()
		tools.setLayout(toolLayout)

		self.toolbar.addWidget(tools)

		finalLayout = QVBoxLayout()
		finalLayout.setContentsMargins(0,0,0,0)
		finalLayout.addWidget(self.toolbar)
		finalLayout.addWidget(self.web)

		window = QWidget()
		window.setLayout(finalLayout)

		self.setCentralWidget(window)

		self.web.load(QtCore.QUrl.fromUserInput(f"{self.url}"))

		self.web.titleChanged.connect(self.webTitleChanged)
		self.web.iconChanged.connect(self.webIconChanged)
		self.web.urlChanged.connect(self.webUrlChanged)

		self.setWindowIcon(QIcon(WEB_ICON))

		self.gui.buildWindowMenu()
		