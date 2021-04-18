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

from ..strings import *
from ..files import *
from .. import config

from ..resources import *

def clearQTreeWidget(tree):
	iterator = QTreeWidgetItemIterator(tree, QTreeWidgetItemIterator.All)
	while iterator.value():
		iterator.value().takeChildren()
		iterator +=1
	i = tree.topLevelItemCount()
	while i > -1:
		tree.takeTopLevelItem(i)
		i -= 1

def buildConnectionDisplayWidget(self):

	fm = QFontMetrics(self.app.font())
	# fheight = fm.height() + 4
	fheight = fm.height() + 8
	fwidth = fm.width('X') * 25

	if config.CONNECTION_DISPLAY_WIDTH:
		fwidth = config.CONNECTION_DISPLAY_WIDTH

	class LogWidget(QTreeWidget):

		def __init__(self,parent=None):
			self.started = True
			self.parent = parent
			super(LogWidget, self).__init__(parent)

		def resizeEvent(self, newSize):
			s = newSize.size()
			config.CONNECTION_DISPLAY_WIDTH = s.width()

			self.parent.connectionDisplayResized()

		def sizeHint(self):
			if self.started:
				self.started = False
				return QSize(fwidth, self.height())
			return QSize(self.width(), self.height())
			
	connectionTree = LogWidget(self)
	connectionTree.headerItem().setText(0,"1")
	connectionTree.header().setVisible(False)
	
	connectionTree.setIconSize(QSize(fheight,fheight))

	connectionTree.setSelectionMode(QAbstractItemView.NoSelection)

	connectionTree.setFocusPolicy(Qt.NoFocus)


	connectionTree.itemDoubleClicked.connect(self.connectionNodeDoubleClicked)
	connectionTree.itemClicked.connect(self.connectionNodeSingleClicked)

	connectionDisplay = QDockWidget(self)
	connectionDisplay.setWidget(connectionTree)
	connectionDisplay.setFloating(False)

	connectionDisplay.setAllowedAreas(Qt.AllDockWidgetAreas)

	connectionDisplay.setWindowTitle("Connections")

	mbcolor = QColor(config.CONNECTION_DISPLAY_BG_COLOR).name()
	c = tuple(int(mbcolor[i:i + 2], 16) / 255. for i in (1, 3, 5))
	luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
	luma = luma*100

	if luma>=40:
		is_light_colored = True
	else:
		is_light_colored = False

	CONNECTION_DISPLAY_SS = f"""
		QTreeWidget {{
		    background-color: {config.CONNECTION_DISPLAY_BG_COLOR};
		    color: {config.CONNECTION_DISPLAY_TEXT_COLOR};
		}}

		QTreeWidget::branch:has-children:!has-siblings:closed,
		QTreeWidget::branch:closed:has-children:has-siblings {{
		        border-image: none;
		        image: url({CONNECTION_CLOSED});
		}}

		QTreeWidget::branch:open:has-children:!has-siblings,
		QTreeWidget::branch:open:has-children:has-siblings  {{
		        border-image: none;
		        image: url({CONNECTION_OPEN});
		}}"""

	LIGHT_CONNECTION_DISPLAY_SS = f"""
		QTreeWidget {{
		    background-color: {config.CONNECTION_DISPLAY_BG_COLOR};
		    color: {config.CONNECTION_DISPLAY_TEXT_COLOR};
		}}

		QTreeWidget::branch:has-children:!has-siblings:closed,
		QTreeWidget::branch:closed:has-children:has-siblings {{
		        border-image: none;
		        image: url({LIGHT_CONNECTION_CLOSED});
		}}

		QTreeWidget::branch:open:has-children:!has-siblings,
		QTreeWidget::branch:open:has-children:has-siblings  {{
		        border-image: none;
		        image: url({LIGHT_CONNECTION_OPEN});
		}}"""

	if is_light_colored:
		connectionTree.setStyleSheet(CONNECTION_DISPLAY_SS)
	else:
		connectionTree.setStyleSheet(LIGHT_CONNECTION_DISPLAY_SS)

	return [connectionTree,connectionDisplay]

	