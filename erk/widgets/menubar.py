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

toolbar_button_style = '''
	QPushButton {
		border: 0px;
		color: black;
	}
	QPushButton::menu-indicator{width:0px;}
	QPushButton::open{
		background-color: #a9a9a9;
		color: white;
		font: bold;
	}
'''

toolbar_button_style_hover = '''
	QPushButton {
		border: 0px;
		background-color: #a9a9a9;
		color: black;
		font: bold;
	}
	QPushButton::menu-indicator{width:0px;}
	QPushButton::open{
		background-color: #a9a9a9;
		color: white;
		font: bold;
	}
'''

toolbar_menu_style = '''
	QMenu {
		margin: 2px;
	}
	QMenu::item:selected {
		background-color: #a9a9a9;
		color: white;
	}
	QMenu::item {
		background-color: transparent;
		color: black;
	}
	QMenu::item:disabled {
		background-color: transparent;
		color: grey;
	}
'''

def generate_menu_toolbar(self):

	toolbar = QToolBar(self)
	toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
	# toolbar.setStyleSheet(''' QToolBar { spacing: 5px; } ''')
	toolbar.setStyleSheet(''' QToolBar { spacing: 8px; } ''')

	f = toolbar.font()
	fm = QFontMetrics(f)
	fheight = fm.height()
		
	toolbar.setFixedHeight(fheight+8)

	return toolbar

def add_toolbar_menu(toolbar,name,menu):

	f = toolbar.font()
	f.setBold(True)

	menu.setStyleSheet(toolbar_menu_style)

	toolMenuButton = MenuButton(
			toolbar_button_style,
			toolbar_button_style_hover,
			" "+name+" "
			)

	toolMenuButton.setStyleSheet(toolbar_button_style)
	menu.setFont(f)
	toolMenuButton.setMenu(menu)
	toolbar.addWidget(toolMenuButton)

def end_toolbar_menu(toolbar):
	toolbar.addWidget(QLabel(' '))

def add_toolbar_image(toolbar,icon):

	f = toolbar.font()
	f.setBold(True)

	toolMenuButton = QPushButton()
	toolMenuButton.setIcon(QIcon(icon))

	toolMenuButton.setStyleSheet("border: 0px;")

	toolbar.addWidget(toolMenuButton)

	return toolMenuButton

class MenuButton(QPushButton):

	def __init__(self,normal_style,hover_style,parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

		self.normal_style = normal_style
		self.hover_style = hover_style

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			self.setStyleSheet(self.hover_style)
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet(self.normal_style)
		return False