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

		self.log = []

		self.show_timestamp = True
		self.show_input = True
		self.show_output = True

		if not self.name:
			pass
		else:
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

		options = self.menubar.addMenu("Options")

		entry = QAction("Show timestamps",self,checkable=True)
		entry.setChecked(self.show_timestamp)
		entry.triggered.connect(lambda state,s="timestamp": self.change_setting(s))
		options.addAction(entry)

		entry = QAction("Show input",self,checkable=True)
		entry.setChecked(self.show_input)
		entry.triggered.connect(lambda state,s="input": self.change_setting(s))
		options.addAction(entry)

		entry = QAction("Show output",self,checkable=True)
		entry.setChecked(self.show_output)
		entry.triggered.connect(lambda state,s="output": self.change_setting(s))
		options.addAction(entry)

		options.addSeparator()

		ioClear = QAction(QIcon(CLEAR_ICON),"Clear",self)
		ioClear.triggered.connect(self.doClear)
		options.addAction(ioClear)

	def change_setting(self,s):
		if s=="output":
			if self.show_output:
				self.show_output = False
			else:
				self.show_output = True
		if s=="input":
			if self.show_input:
				self.show_input = False
			else:
				self.show_input = True
		if s=="timestamp":
			if self.show_timestamp:
				self.show_timestamp = False
			else:
				self.show_timestamp = True

		self.rerender()

	def doClear(self):
		self.ircLineDisplay.clear()

	def rerender(self):
		self.ircLineDisplay.clear()

		for e in self.log:
			timestamp = e[0]
			line = e[1]
			is_input = e[2]

			if not self.show_input and is_input: continue
			if not self.show_output and not is_input: continue

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

			if self.show_timestamp:
				pretty = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
				ui.setText("["+pretty+"] "+line)
			else:
				ui.setText(line)

			self.ircLineDisplay.addItem(ui)

		self.ircLineDisplay.scrollToBottom()



	def writeLine(self,line,is_input=True):

		t = datetime.timestamp(datetime.now())
		

		entry = [t,line,is_input]
		self.log.append(entry)

		if not self.show_input and is_input: return
		if not self.show_output and not is_input: return

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

		if self.show_timestamp:
			pretty = datetime.fromtimestamp(t).strftime('%H:%M:%S')
			ui.setText("["+pretty+"] "+line)
		else:
			ui.setText(line)

		
		self.ircLineDisplay.addItem(ui)

		self.ircLineDisplay.scrollToBottom()

		if self.ircLineDisplay.count()>self.gui.max_lines_in_io_display:
			self.ircLineDisplay.takeItem(0)
			self.log.pop(0)

