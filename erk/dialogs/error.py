
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
# import erk.plugins

# INSTALL_DIRECTORY = sys.path[0]
# PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")

class Dialog(QDialog):


	def __init__(self,errlist,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Plugin load errors")
		self.setWindowIcon(QIcon(ERROR_ICON))

		errTree = QTreeWidget()
		errTree.headerItem().setText(0,"1")
		errTree.header().setVisible(False)

		root = errTree.invisibleRootItem()

		dlable = QLabel( str(len(errlist)) + " plugin(s) not loaded"   )

		for pack in errlist:
			parent = QTreeWidgetItem(root)
			parent.setText(0,"Package \""+pack+"\"")
			parent.setIcon(0,QIcon(PACKAGE_ICON))

			parent.setExpanded(True)

			cl = {}
			for e in errlist[pack]:
				if e[0] in cl:
					cl[e[0]].append(e[1])
				else:
					cl[e[0]] = []
					cl[e[0]].append(e[1])

			for c in cl:
				uncle = QTreeWidgetItem(parent)
				uncle.setText(0,c+" class - "+str(len(cl[c]))+" error(s)")
				uncle.setExpanded(True)
				uncle.setIcon(0,QIcon(PLUGIN_ICON))
				for e in cl[c]:
					child = QTreeWidgetItem(uncle)
					child.setText(0,e)
					child.setIcon(0,QIcon(ERROR_ICON))


		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)

		buttons.button(QDialogButtonBox.Ok).setText("Ok")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(dlable)
		finalLayout.addWidget(errTree)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
