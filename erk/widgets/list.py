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

from erk.files import *

class Window(QMainWindow):

	def empty_list(self):
		self.list = []

	def clear_list(self):

		self.channelListDisplay.clearContents()

		self.channelListDisplay.model().removeRows(0,self.channelListDisplay.rowCount())

	def rerender(self):

		self.clear_list()

		l = []
		for e in self.list:
			if int(e[1])==1:
				if not self.show_only_one:
					continue

			if e[2].strip()=='':
				if not self.show_no_topic:
					continue

			l.append(e)

		#print(l)

		for e in l:
			currentRowCount = self.channelListDisplay.rowCount()

			self.channelListDisplay.insertRow(currentRowCount)
			self.channelListDisplay.setItem(currentRowCount,0,QTableWidgetItem(e[0]))
			self.channelListDisplay.setItem(currentRowCount,1,QTableWidgetItem(e[1]))
			self.channelListDisplay.setItem(currentRowCount,2,QTableWidgetItem(e[2]))



	def add_channel(self,channel,usercount,topic):

		currentRowCount = self.channelListDisplay.rowCount()

		self.channelListDisplay.insertRow(currentRowCount)
		self.channelListDisplay.setItem(currentRowCount,0,QTableWidgetItem(channel))
		self.channelListDisplay.setItem(currentRowCount,1,QTableWidgetItem(usercount))
		self.channelListDisplay.setItem(currentRowCount,2,QTableWidgetItem(topic))

		self.list.append( [channel,usercount,topic]  )

	def refresh(self):
		self.client.sendLine("LIST")

	def click(self,row,column):
		channel = self.channelListDisplay.item(row,0)
		
		self.client.join(channel.text())

	def menuMoreOne(self):
		if self.show_only_one:
			self.show_only_one = False
		else:
			self.show_only_one = True
		self.rerender()

	def menuHasTopic(self):
		if self.show_no_topic:
			self.show_no_topic = False
		else:
			self.show_no_topic = True
		self.rerender()

	def __init__(self,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = "Channel list"
		self.client = client
		self.gui = parent

		self.channel_count = 0

		self.show_only_one = True
		self.show_no_topic = True

		self.list = []

		STYLES = get_text_format_settings(self.gui.stylefile)

		# self.channelListDisplay = QListWidget(self)
		self.channelListDisplay = QTableWidget(self)
		self.channelListDisplay.setObjectName("channelListDisplay")

		self.channelListDisplay.setColumnCount(3)
		self.channelListDisplay.setHorizontalHeaderLabels(['Channel', 'Users', 'Topic'])

		fm = QFontMetrics(self.font())
		countwidth = (fm.width("0")*4)+15
		chanwidth = (fm.width("X")*20)

		self.channelListDisplay.setColumnWidth(0,chanwidth)	# channel
		self.channelListDisplay.setColumnWidth(1,countwidth)	# User count
		self.channelListDisplay.horizontalHeader().setStretchLastSection(True)

		self.channelListDisplay.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.channelListDisplay.cellDoubleClicked.connect(self.click)

		self.channelListDisplay.setStyleSheet(STYLES["all"])

		self.setCentralWidget(self.channelListDisplay)

		self.menubar = self.menuBar()

		self.actRefresh = QAction("Refresh",self)
		self.actRefresh.triggered.connect(self.refresh)
		self.menubar.addAction(self.actRefresh)

		filterMenu = self.menubar.addMenu("Filter")

		self.actMoreOne = QAction("Show channels with only one user",self,checkable=True)
		self.actMoreOne.setChecked(self.show_only_one)
		self.actMoreOne.triggered.connect(self.menuMoreOne)
		filterMenu.addAction(self.actMoreOne)

		self.actHasTopic = QAction("Show channels without topics",self,checkable=True)
		self.actHasTopic.setChecked(self.show_no_topic)
		self.actHasTopic.triggered.connect(self.menuHasTopic)
		filterMenu.addAction(self.actHasTopic)

		