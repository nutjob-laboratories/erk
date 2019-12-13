
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

class QHLine(QFrame):
	def __init__(self):
		super(QHLine, self).__init__()
		self.setFrameShape(QFrame.HLine)
		self.setFrameShadow(QFrame.Sunken)