from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
from erk.strings import *
from erk.config import *

import erk.events


class Window(QMainWindow):

	def closeEvent(self, event):

		#erk.events.erk_parted_channel(self.gui,self.client,self.name)
		if self.do_actual_close:
			erk.events.erk_close_io(self.gui,self.client)
			if self.gui.title_from_active:
				self.gui.setWindowTitle(APPLICATION_NAME)
			self.subwindow.close()
			self.close()
			event.accept()
			self.gui.set_window_not_active(self)
			return

		# self.subwindow.close()
		# event.accept()

		self.subwindow.hide()
		self.hide()
		event.ignore()

	def __init__(self,name,window_margin,subwindow,client,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.subwindow = subwindow
		self.client = client
		self.gui = parent

		self.do_actual_close = False

		self.setWindowTitle(" "+self.name)
		self.setWindowIcon(QIcon(IO_ICON))

		self.ircLineDisplay = QListWidget(self)
		self.ircLineDisplay.setObjectName("ircLineDisplay")
		self.ircLineDisplay.setStyleSheet(self.gui.styles[BASE_STYLE_NAME])

		#self.ircLineDisplay.setIconSize(QSize(15, 15))
		self.ircLineDisplay.setWordWrap(True)

		ufont = self.ircLineDisplay.font()
		ufont.setBold(True)
		self.ircLineDisplay.setFont(ufont)

		fm = QFontMetrics(self.ircLineDisplay.font())
		fheight = fm.height() + 2
		self.ircLineDisplay.setIconSize(QSize(fheight,fheight))

		self.setCentralWidget(self.ircLineDisplay)

		self.menubar = self.menuBar()

		ioClear = QAction("Clear",self)
		ioClear.triggered.connect(self.doClear)
		self.menubar.addAction(ioClear)

	def doClear(self):
		self.ircLineDisplay.clear()

	def writeLine(self,line,is_input=True):

		t = datetime.timestamp(datetime.now())
		pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')

		ui = QListWidgetItem()

		f = ui.font()
		f.setBold(False)
		
		if not is_input:
			ui.setBackground(QColor("#E7E7E7"))
			ui.setIcon(QIcon(OUTPUT_ICON))
		else:
			ui.setBackground(QColor("#FFFFFF"))
			ui.setFont(f)
			ui.setIcon(QIcon(INPUT_ICON))
			#prefix = pretty +' -> '

		# ui.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
		ui.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

		ui.setText("["+pretty+"] "+line)
		self.ircLineDisplay.addItem(ui)

		self.ircLineDisplay.scrollToBottom()

		if self.ircLineDisplay.count()>self.gui.max_lines_in_io_display:
			self.ircLineDisplay.takeItem(0)

