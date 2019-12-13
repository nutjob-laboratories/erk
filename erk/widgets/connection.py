
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.strings import *

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

	class LogWidget(QTreeWidget):

		def __init__(self,parent=None):
			self.started = True
			super(LogWidget, self).__init__(parent)

		def sizeHint(self):
			if self.started:
				self.started = False
				return QSize(fwidth, self.height())
			return QSize(self.width(), self.height())
			
	connectionTree = LogWidget()
	connectionTree.headerItem().setText(0,"1")
	connectionTree.header().setVisible(False)

	#connectionTree.setSelectionMode(QAbstractItemView.NoSelection)
	
	connectionTree.setIconSize(QSize(fheight,fheight))

	connectionTree.setFocusPolicy(Qt.NoFocus)

	connectionTree.itemDoubleClicked.connect(self.connectionNodeDoubleClicked)
	connectionTree.itemClicked.connect(self.connectionNodeSingleClicked)

	connectionDisplay = QDockWidget(self)
	connectionDisplay.setWidget(connectionTree)
	connectionDisplay.setFloating(False)

	connectionDisplay.setAllowedAreas(Qt.AllDockWidgetAreas)

	connectionDisplay.setWindowTitle("Connections")

	# connectionDisplay.setFeatures(
	# 	QDockWidget.DockWidgetMovable |
	# 	QDockWidget.DockWidgetFloatable
	# 	)

	# connectionDisplay.setFeatures( QDockWidget.NoDockWidgetFeatures )
	# connectionDisplay.setTitleBarWidget(QWidget())

	return [connectionTree,connectionDisplay]

	