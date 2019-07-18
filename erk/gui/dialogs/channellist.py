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

class Dialog(QMainWindow):

	def addChannel(self,channel,usercount,topic):
		rowPosition = self.channelList.rowCount()
		self.channelList.insertRow(rowPosition)

		self.channelList.setItem(rowPosition,0,QTableWidgetItem(channel))
		self.channelList.setItem(rowPosition,1,QTableWidgetItem(usercount))
		self.channelList.setItem(rowPosition,2,QTableWidgetItem(topic))

	def resizeEvent(self, event):
		self.channelList.resizeColumnsToContents()
		return super(Dialog, self).resizeEvent(event)

	def gotClick(self):
		for i in self.channelList.selectionModel().selectedIndexes():
			row = i.row()
			column = i.column()

		channel = self.channelList.item(row, 0).text()
		self.parent.channelListClickJoin(self.serverid,channel)


	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.serverid = ""

		self.setWindowIcon(QIcon(SERVER_ICON))

		self.channelList = QTableWidget(self)
		self.channelList.setColumnCount(3)

		self.channelList.setHorizontalHeaderLabels(["Channel","Users","Topic"])

		self.channelList.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.channelList.doubleClicked.connect(self.gotClick)

		self.setCentralWidget(self.channelList)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)
