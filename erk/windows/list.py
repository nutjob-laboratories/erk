
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *

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

	def add_channel(self,channel):
		try:
			ui = QListWidgetItem()
			ui.setIcon(QIcon(CHANNEL_WINDOW))
			ui.setText(channel)
			self.channelListDisplay.addItem(ui)
			self.channel_count = self.channel_count + 1
			self.update_channel_count()
		except Exception as err:
			pass

	def __init__(self,name,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.server = name
		self.channel_count = 0

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

		self.actRefresh = QAction("Refresh",self)
		self.actRefresh.triggered.connect(self.refresh)
		self.menubar.addAction(self.actRefresh)