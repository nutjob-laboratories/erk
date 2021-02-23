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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

import sys,os

from ..resources import *
from ..strings import *

INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")
PLUGIN_SKELETON = os.path.join(DATA_DIRECTORY, "plugin")

class Dialog(QDialog):

	@staticmethod
	def get_name_information(title="Insert",parent=None):
		dialog = Dialog(title,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		if self.name.text().strip()=='':
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("Plugin name is required")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		if self.description.text().strip()=='':
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("Plugin description is required")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		author = self.author.text()
		if len(author.strip())==0: author = None

		version = self.version.text()
		if len(version.strip())==0: version = None

		website = self.website.text()
		if len(website.strip())==0: website = None

		retval = [self.name.text(),self.description.text(),author,version,website]

		if self.title!="Insert":
			# Creating a plugin

			retval.append(self.selectedPackageIcon)
			retval.append(self.selectedPluginIcon)

		return retval

	def __init__(self,title,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.title = title

		self.selectedPackageIcon = None
		self.selectedPluginIcon = None

		if title=="Insert":
			self.setWindowTitle("Insert template")
		else:
			self.setWindowTitle("Create package")
		self.setWindowIcon(QIcon(EDITOR_ICON))

		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)

		self.name = QLineEdit()
		self.description = QLineEdit()

		self.name.setPlaceholderText("Required")
		self.description.setPlaceholderText("Required")

		self.name.setMinimumWidth(wwidth)

		self.author = QLineEdit()
		self.version = QLineEdit()
		self.website = QLineEdit()

		self.author.setPlaceholderText("Optional")
		self.version.setPlaceholderText("Optional")
		self.website.setPlaceholderText("http://optional.com")

		n1 = QLabel("Name")
		n1.setFont(BOLD_FONT)

		n2 = QLabel("Description")
		n2.setFont(BOLD_FONT)

		n3 = QLabel("Author")
		n3.setFont(BOLD_FONT)

		n4 = QLabel("Version")
		n4.setFont(BOLD_FONT)

		n5 = QLabel("Website")
		n5.setFont(BOLD_FONT)

		self.info1 = QLabel("<small><center><i>You must supply a name and description for your plugin. The class name for the plugin will be derived from the name you supply (all whitespace and punctuation will be removed).</i></center></small>")
		self.info1.setWordWrap(True)
		self.info1.setAlignment(Qt.AlignJustify)

		self.info2 = QLabel("<small><center><i>Author, version, and website are all optional. They will be used for the menu entry in "+APPLICATION_NAME+", in the \"Plugins\" menu. Website should be set to a valid URL.</i></center></small>")
		self.info2.setWordWrap(True)
		self.info2.setAlignment(Qt.AlignJustify)

		infoLayout = QFormLayout()
		infoLayout.addRow(self.info1)
		infoLayout.addRow(n1, self.name)
		infoLayout.addRow(n2, self.description)
		infoLayout.addRow(self.info2)
		infoLayout.addRow(n3, self.author)
		infoLayout.addRow(n4, self.version)
		infoLayout.addRow(n5, self.website)

		if title!="Insert":
			# Since we're creating a package, add in the icon selection stuff

			self.info1.setText("<small><center><i>You must supply a name and description for your package. The class name for the plugin will be derived from the name you supply (all whitespace and punctuation will be removed).</i></center></small>")

			self.package_icon = QLabel()
			pixmap = QPixmap(os.path.join(PLUGIN_SKELETON, "package.png"))
			self.package_icon.setPixmap(pixmap)
			self.package_icon.setAlignment(Qt.AlignCenter)

			pack_width = pixmap.width()
			pack_height = pixmap.height()

			self.plugin_icon = QLabel()
			pixmap = QPixmap(os.path.join(PLUGIN_SKELETON, "plugin.png"))
			self.plugin_icon.setPixmap(pixmap)
			self.plugin_icon.setAlignment(Qt.AlignCenter)

			plug_width = pixmap.width()
			plug_height = pixmap.height()

			entry = QPushButton("Select package icon")
			entry.clicked.connect(self.selectPack)

			self.pack_desc = QLabel("<center><small>"+str(pack_width)+"x"+str(pack_height)+" PNG image</center></small>")

			piLayout = QVBoxLayout()
			piLayout.addWidget(self.package_icon)
			piLayout.addWidget(self.pack_desc)
			piLayout.addWidget(entry)

			entry = QPushButton("Select plugin icon")
			entry.clicked.connect(self.selectPlug)

			self.plug_desc = QLabel("<center><small>"+str(plug_width)+"x"+str(plug_height)+" PNG image</center></small>")

			pi2Layout = QVBoxLayout()
			pi2Layout.addWidget(self.plugin_icon)
			pi2Layout.addWidget(self.plug_desc)
			pi2Layout.addWidget(entry)

			fpLayout = QHBoxLayout()
			fpLayout.addLayout(piLayout)
			fpLayout.addLayout(pi2Layout)

			self.info3 = QLabel("<small><center><i>You can optionally select a package and plugin icon. If one or the other is <b>not</b> customized, the default image will be used. The package icon should be a 48x48 pixel PNG image, and the plugin icon should be a 25x25 pixel PNG image.</i></center></small>")
			self.info3.setWordWrap(True)
			self.info3.setAlignment(Qt.AlignJustify)

			infoLayout.addRow(self.info3)
			infoLayout.addRow(fpLayout)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText(self.title)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(infoLayout)
		#finalLayout.addLayout(descriptionLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def selectPlug(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Image", INSTALL_DIRECTORY,"PNG File (*.png)", options=options)
		if fileName:

			self.selectedPluginIcon = fileName
			pixmap = QPixmap(fileName)
			self.plugin_icon.setPixmap(pixmap)

			plug_width = pixmap.width()
			plug_height = pixmap.height()

			self.plug_desc.setText("<center><small>"+str(plug_width)+"x"+str(plug_height)+" PNG image</center></small>")

	def selectPack(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Image", INSTALL_DIRECTORY,"PNG File (*.png)", options=options)
		if fileName:

			self.selectedPackageIcon = fileName
			pixmap = QPixmap(fileName)
			self.package_icon.setPixmap(pixmap)

			pack_width = pixmap.width()
			pack_height = pixmap.height()

			self.pack_desc.setText("<center><small>"+str(pack_width)+"x"+str(pack_height)+" PNG image</center></small>")
