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

import fnmatch

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *

import erk.dialogs.search_term as SearchDialog

class Window(QMainWindow):

	def closeEvent(self, event):
		if not self.gui.quitting:
			self.subwindow.hide()
			event.ignore()
		else:
			self.subwindow.close()
			self.close()
			event.accept()

	def enable_refresh(self):
		self.actRefresh.setEnabled(True)

	def disable_refresh(self):
		self.actRefresh.setEnabled(False)

	def clear(self):
		self.channelListDisplay.clear()
		self.channel_count = 0
		self.list = []
		self.filter_more_than_one = False
		self.filter_has_topic = False
		self.actMoreOne.setChecked(False)
		self.actHasTopic.setChecked(False)

	def refresh(self):
		self.client.sendLine(f"LIST")

	def update_channel_count(self):
		if self.channel_count==0:
			self.setWindowTitle(" "+self.name)
		else:
			if self.channel_count==1:
				self.setWindowTitle(" "+self.name+" (1 channel)")
			else:
				self.setWindowTitle(" "+self.name+" ("+ str(self.channel_count) +" channels)")

	def mfilter(self):
		self.filter(True,True)

	def filter(self,more_than_one,has_topic=False,searchterms=None):
		clist = []
		if searchterms:
			for e in self.list:
				if fnmatch.fnmatch(e[0],searchterms): clist.append(e)
				if fnmatch.fnmatch(e[2],searchterms): clist.append(e)
		else:
			clist = self.list

		flist = []
		if has_topic:
			for e in clist:
				if len(e[2])>0: flist.append(e)
		else:
			flist = clist

		mlist = []
		if more_than_one:
			for e in flist:
				if int(e[1])>1: mlist.append(e)
		else:
			mlist = flist

		self.channelListDisplay.clear()
		self.channel_count = 0

		for e in mlist:
			if int(e[1])==1:
				suffix = ""
			else:
				suffix = "s"
			if e[2] != '':
				entry = e[0] + " (" + str(e[1]) + " user" + suffix + ") - " + e[2]
			else:
				entry = e[0] + " (" + str(e[1]) + " user" + suffix + ")"
			ui = QListWidgetItem()
			ui.setIcon(QIcon(CHANNEL_WINDOW))
			ui.setText(entry)
			self.channelListDisplay.addItem(ui)
			self.channel_count = self.channel_count + 1
			self.update_channel_count()



	def _handleDoubleClick(self,item):
		index = self.channelListDisplay.currentRow()
		text = item.text()

		item.setSelected(False)
		
		p = text.split()
		if len(p)>0:
			channel = p[0]
		else:
			channel = None

		if channel: self.client.sendLine(f"JOIN "+channel)

		# item.setSelected(False)
		# self.gui.double_click_user(self.client,item.text())

	def add_channel(self,channel,usercount,topic):
		try:
			self.list.append( [channel,usercount,topic]  )

			if int(usercount)==1:
				suffix = ""
			else:
				suffix = "s"
			if topic != '':
				entry = channel + " (" + str(usercount) + " user" + suffix + ") - " + topic
			else:
				entry = channel + " (" + str(usercount) + " user" + suffix + ")"

			ui = QListWidgetItem()
			ui.setIcon(QIcon(CHANNEL_WINDOW))
			ui.setText(entry)
			self.channelListDisplay.addItem(ui)
			self.channel_count = self.channel_count + 1
			self.update_channel_count()
		except Exception as err:
			pass

	def menuMoreOne(self):
		if self.filter_more_than_one:
			self.filter_more_than_one = False
		else:
			self.filter_more_than_one = True
		self.filter(self.filter_more_than_one,self.filter_has_topic)

	def menuHasTopic(self):
		if self.filter_has_topic:
			self.filter_has_topic = False
		else:
			self.filter_has_topic = True
		self.filter(self.filter_more_than_one,self.filter_has_topic)

	def menuSearch(self):
		x = SearchDialog.Dialog(self)
		e = x.get_search_information(self)

		if not e: return

		self.filter(self.filter_more_than_one,self.filter_has_topic,e)

	def __init__(self,name,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.server = name
		self.channel_count = 0

		self.list = []
		self.filter_more_than_one = False
		self.filter_has_topic = False

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(ERK_ICON))

		self.channelListDisplay = QListWidget(self)
		self.channelListDisplay.setObjectName("channelListDisplay")
		self.channelListDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		self.channelListDisplay.itemDoubleClicked.connect(self._handleDoubleClick)

		ufont = self.channelListDisplay.font()
		ufont.setBold(True)
		self.channelListDisplay.setFont(ufont)

		self.setCentralWidget(self.channelListDisplay)

		self.menubar = self.menuBar()

		filterMenu = self.menubar.addMenu("Filter")

		self.actSearch = QAction(QIcon(WHOIS_ICON),"Search",self)
		self.actSearch.triggered.connect(self.menuSearch)
		filterMenu.addAction(self.actSearch)

		self.actMoreOne = QAction("More than one user",self,checkable=True)
		self.actMoreOne.setChecked(self.filter_more_than_one)
		self.actMoreOne.triggered.connect(self.menuMoreOne)
		filterMenu.addAction(self.actMoreOne)

		self.actHasTopic = QAction("Has a topic",self,checkable=True)
		self.actHasTopic.setChecked(self.filter_has_topic)
		self.actHasTopic.triggered.connect(self.menuHasTopic)
		filterMenu.addAction(self.actHasTopic)

		self.actRefresh = QAction("Refresh",self)
		self.actRefresh.triggered.connect(self.refresh)
		self.menubar.addAction(self.actRefresh)

		