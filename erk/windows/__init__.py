
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from .channel import Window as Channel
from .private import Window as Private
from .server import Window as Server

def ChannelWindow(channel,MDI,client,parent=None):

		newSubwindow = QMdiSubWindow()
		# newWindow = Channel.Window(channel,WINDOW_WIDGET_MARGIN,newSubwindow,client,parent)
		newWindow = Channel(channel,1,newSubwindow,client,parent)
		newSubwindow.setWidget(newWindow)
		newSubwindow.window = newWindow
		MDI.addSubWindow(newSubwindow)

		#newSubwindow.resize(DEFAULT_WINDOW_WIDTH,DEFAULT_WINDOW_HEIGHT)
		#newSubwindow.resize(600,450)
		newSubwindow.resize(parent.initial_window_width,parent.initial_window_height)

		newSubwindow.show()

		return newWindow

def PrivateWindow(channel,MDI,client,parent=None):

		newSubwindow = QMdiSubWindow()
		# newWindow = Channel.Window(channel,WINDOW_WIDGET_MARGIN,newSubwindow,client,parent)
		newWindow = Private(channel,1,newSubwindow,client,parent)
		newSubwindow.setWidget(newWindow)
		newSubwindow.window = newWindow
		MDI.addSubWindow(newSubwindow)

		#newSubwindow.resize(DEFAULT_WINDOW_WIDTH,DEFAULT_WINDOW_HEIGHT)
		#newSubwindow.resize(600,450)
		newSubwindow.resize(parent.initial_window_width,parent.initial_window_height)

		newSubwindow.show()

		return newWindow

def ServerWindow(channel,MDI,client,parent=None):

		newSubwindow = QMdiSubWindow()
		# newWindow = Channel.Window(channel,WINDOW_WIDGET_MARGIN,newSubwindow,client,parent)
		newWindow = Server(channel,1,newSubwindow,client,parent)
		newSubwindow.setWidget(newWindow)
		newSubwindow.window = newWindow
		MDI.addSubWindow(newSubwindow)

		#newSubwindow.resize(DEFAULT_WINDOW_WIDTH,DEFAULT_WINDOW_HEIGHT)
		#newSubwindow.resize(600,450)
		newSubwindow.resize(parent.initial_window_width,parent.initial_window_height)

		newSubwindow.show()

		return newWindow
