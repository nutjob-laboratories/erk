

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *

class MenuLabel(QLabel):
	clicked=pyqtSignal()

	def __init__(self, parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

	def mousePressEvent(self, ev):
		self.clicked.emit()

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			col = self.palette().highlight().color().name()
			highlight = QColor(col).name()

			col = self.palette().highlightedText().color().name()
			highlight_text = QColor(col).name()
			
			# self.setStyleSheet(f"background-color: {highlight}; color: {highlight_text};")

			self.setStyleSheet(f"background-color: #a9a9a9; color: white;")

			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet('')
		return False

def MenuAction(self,icon,title,description,icon_size,func):

	erkmenuLabel = MenuLabel( menuHtml(icon,title,description,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)
	erkmenuLabel.clicked.connect(func)

	return erkmenuAction

def menuHtml(icon,text,description,icon_size):
	return f'''
<table style="width: 100%" border="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;"><img src="{icon}" width="{icon_size}" height="{icon_size}">&nbsp;</td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: italic; font-weight: normal;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''
