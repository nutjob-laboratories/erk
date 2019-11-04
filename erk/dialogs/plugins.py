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

import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *

class Dialog(QDialog):

	def doOkay(self):

		save_disabled(self.disabled)
		self.do_load_unload()
		
		items = [] 
		for index in range(self.plugins.count()): 
			 items.append(self.plugins.item(index).text())

		self.parent.buildPluginMenu()

		self.close()

	def doCancel(self):
		self.close()

	def doInstallPlugin(self):
		options = QFileDialog.Options()
		#options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,APPLICATION_NAME+" Plugin", INSTALL_DIRECTORY,"Zip File (*.zip);;All Files (*)", options=options)
		if fileName:
			install_plugin_from_zip(fileName)
			self.doReload()

	def setSubwindow(self,sw):
		self.subwindow = sw

	def clickPlugin(self,item):
		plug = item.toolTip()
		#index = self.plugins.currentRow()
		if item.checkState() == Qt.Checked:
			if plug in self.disabled:
				self.disabled.remove(plug)
				self.do_load.append(plug)
			else:
				pass
		else:
			if plug in self.disabled:
				pass
			else:
				self.disabled.append(plug)
				self.do_unload.append(plug)

	def do_load_unload(self):
		self.do_load = list(dict.fromkeys(self.do_load))
		self.do_unload = list(dict.fromkeys(self.do_unload))

		for p in self.do_load:
			if p in self.loaded: continue
			self.parent.force_execute_plugin(p,PLUGIN_LOAD_METHOD, None )

		for p in self.do_unload:
			if not p in self.disabled: continue
			self.parent.force_execute_plugin(p,PLUGIN_UNLOAD_METHOD, None )

	def doReload(self):
		self.parent.pluginReload()

		self.pluginlist = self.parent.packages.plugins
		self.plugins.clear()

		toggle = 0
		for p in self.pluginlist:
			icon = p._icon
			if not os.path.isfile(icon): icon = PLUGIN_ICON
			item = QListWidgetItem(p.name+" "+p.version+"\n"+p._package+"."+p._class+"\n"+p.author)
			item.setToolTip(p._package+"."+p._class)
			item.setIcon(QIcon(icon))
			item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
			if (p._package+"."+p._class) in self.disabled:
				item.setCheckState(QtCore.Qt.Unchecked)
			else:
				item.setCheckState(QtCore.Qt.Checked)
				self.loaded.append(p._package+"."+p._class)
			if toggle == 0:
				item.setBackground(QColor("#FFFFFF"))
				toggle = 1
			else:
				item.setBackground(QColor("#E7E7E7"))
				toggle = 0
			self.plugins.addItem(item)

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.subwindow = None

		self.pluginlist = self.parent.packages.plugins
		self.disabled = get_disabled()
		self.loaded = []

		self.do_load = []
		self.do_unload = []

		self.setWindowTitle(f"Manage Plugins")
		self.setWindowIcon(QIcon(PLUGIN_ICON))

		self.plugins = QListWidget(self)
		self.plugins.itemChanged.connect(self.clickPlugin)
		#self.plugins.setMaximumWidth(175)

		toggle = 0
		for p in self.pluginlist:
			icon = p._icon
			if not os.path.isfile(icon): icon = PLUGIN_ICON
			# item = QListWidgetItem()
			# item.setText(p.name+" "+p.version)
			item = QListWidgetItem(p.name+" "+p.version+"\n"+p._package+"."+p._class+"\n"+p.author)
			item.setToolTip(p._package+"."+p._class)
			item.setIcon(QIcon(icon))
			item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
			if (p._package+"."+p._class) in self.disabled:
				item.setCheckState(QtCore.Qt.Unchecked)
			else:
				item.setCheckState(QtCore.Qt.Checked)
				self.loaded.append(p._package+"."+p._class)
			if toggle == 0:
				item.setBackground(QColor("#FFFFFF"))
				toggle = 1
			else:
				item.setBackground(QColor("#E7E7E7"))
				toggle = 0
			self.plugins.addItem(item)


		self.installPluginButton = QPushButton("Install plugin")
		self.installPluginButton.clicked.connect(self.doInstallPlugin)

		self.reloadPlugins = QPushButton("Reload plugins")
		self.reloadPlugins.clicked.connect(self.doReload)

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(self.installPluginButton)
		buttonLayout.addStretch()
		buttonLayout.addWidget(self.reloadPlugins)

		instructLayout = QHBoxLayout()
		instructLayout.addStretch()
		instructLayout.addWidget( QLabel("<small><i>Check plugins to <b>enable</b>, uncheck to <b>disable</b></i></small>") )

		installedPluginsLayout = QVBoxLayout()
		installedPluginsLayout.addWidget(self.plugins)
		installedPluginsLayout.addLayout(buttonLayout)
		

		pluginsBox = QGroupBox("Installed plugins")
		pluginsBox.setLayout(installedPluginsLayout)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.doOkay)
		buttons.rejected.connect(self.doCancel)

		buttons.button(QDialogButtonBox.Ok).setText("Save")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(pluginsBox)
		finalLayout.addLayout(instructLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)