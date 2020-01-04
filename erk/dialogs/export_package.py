
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *

INSTALL_DIRECTORY = sys.path[0]
PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")

class Dialog(QDialog):

	@staticmethod
	def get_name_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		item = self.packlist.currentItem()
		if item:
			retval = item.file
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("No plugin package selected")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Export package")
		self.setWindowIcon(QIcon(ARCHIVE_ICON))

		self.title = QLabel("Select a package to export")

		self.packlist = QListWidget(self)
		self.packlist.setMaximumHeight(100)

		for x in os.listdir(PLUGIN_DIRECTORY):
			if x.lower()=="__pycache__": continue
			pack = os.path.join(PLUGIN_DIRECTORY, x)
			if os.path.isdir(pack):
				item = QListWidgetItem(x)
				item.file = pack
				self.packlist.addItem(item)

		self.packlist.setCurrentRow(0)


		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.title)
		finalLayout.addWidget(self.packlist)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
