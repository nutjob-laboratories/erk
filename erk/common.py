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

import sys
import os

INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")
MINOR_VERSION_FILE = os.path.join(DATA_DIRECTORY, "minor.txt")

mvf=open(MINOR_VERSION_FILE, "r")
MINOR_VERSION = mvf.read()
mvf.close()

if len(MINOR_VERSION)==1:
	MINOR_VERSION = "00"+MINOR_VERSION
elif len(MINOR_VERSION)==2:
	MINOR_VERSION = "0"+MINOR_VERSION

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore

SSL_AVAILABLE = True
try:
	import ssl
except ImportError:
	SSL_AVAILABLE = False

APPLICATION_NAME = "Ərk"
APPLICATION_MAJOR_VERSION = "0.500"
APPLICATION_VERSION = APPLICATION_MAJOR_VERSION+"."+MINOR_VERSION
OFFICIAL_REPOSITORY = "https://github.com/nutjob-laboratories/erk"
PROGRAM_FILENAME = "erk.py"
NORMAL_APPLICATION_NAME = "Erk"

GPL_NOTIFICATION = """Ərk IRC Client
Copyright (C) 2019  Dan Hetrick

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

DEFAULT_WINDOW_TITLE = APPLICATION_NAME

MENU_ICON_SIZE = 22

class ErkStyle(QProxyStyle):
	# pass
	def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

		if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
			return MENU_ICON_SIZE
		else:
			return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)

# =============
# | RESOURCES |
# =============

# Load in resource file
globals()["erk.data.resources"] = __import__("erk.data.resources")

# List of commands for autocomplete
INPUT_COMMANDS = {
	"/msg": "/msg ",
	"/me": "/me ",
	"/nick": "/nick ",
	"/notice": "/notice ",
	"/join": "/join ",
	"/part": "/part ",
}
CONSOLE_COMMANDS = {
	"/msg": "/msg ",
	"/nick": "/nick ",
	"/notice": "/notice ",
	"/join": "/join ",
	"/part": "/part ",
}

GLYPH_SELF = '@'
GLYPH_ACTION = "+"
GLYPH_NOTICE = '&'
GLYPH_RESUME = '~'
GLYPH_ERROR = '%'

# exitButton.setShortcut('Ctrl+Q')
# exitButton.setStatusTip('Exit application')

EXIT_SHORTCUT = 'Ctrl+Q'
CONNECT_SERVER_SHORTCUT = 'Ctrl+S'
CONNECT_NETWORK_SHORTCUT = 'Ctrl+N'

# ------------
# | GRAPHICS |
# ------------

MDI_BACKGROUND = ":/gui-background.png"
USER_WINDOW = ":/gui-user.png"
CHANNEL_WINDOW = ":/gui-channel.png"
CONSOLE_WINDOW = ":/gui-console.png"
LOCKED_CHANNEL = ":/gui-locked.png"

USER_OPERATOR = ":/gui-chanoperator.png"
USER_VOICED = ":/gui-chanvoiced.png"
USER_NORMAL = ":/gui-chanuser.png"

LOGO_IMAGE = ":/gui-logo.png"

ICONS8_ICON = ":/gui-icons8.png"
PYTHON_ICON = ":/gui-python.png"
QT_ICON = ":/gui-qt.png"
TWISTED_ICON = ":/gui-twisted.png"

OPEN_SOURCE_ICON = ":/gui-opensource.png"
PYTHON_SMALL_ICON = ":/gui-pyicon.png"
QT_SMALL_ICON = ":/gui-qticon.png"
PYQT_ICON = ":/gui-pyqt.png"

# ---------
# | ICONS |
# ---------

ERK_ICON = ":/erk.png"
SERVER_ICON = ":/server.png"
NETWORK_ICON = ":/network.png"
EXIT_ICON = ":/exit.png"
RESTART_ICON = ":/restart.png"
CASCADE_ICON = ":/cascade.png"
TILE_ICON = ":/tile.png"
FONT_ICON = ":/font.png"
CHAT_ICON = ":/chat.png"
LOG_ICON = ":/log.png"
TIMESTAMP_ICON = ":/timestamp.png"
SPELL_ICON = ":/spell.png"
AUTOCOMPLETE_ICON = ":/autocomplete.png"
USER_ICON = ":/user.png"
HOST_ICON = ":/host.png"
DISCONNECT_ICON = ":/disconnect.png"
ABOUT_ICON = ":/about.png"
LINK_ICON = ":/link.png"
BAN_ICON = ":/ban.png"
MODERATED_ICON = ":/moderated.png"
PLUS_ICON = ":/plus.png"
MINUS_ICON = ":/minus.png"
WINDOW_ICON = ":/window.png"
CLIPBOARD_ICON = ":/clipboard.png"
LIST_ICON = ":/list.png"
KICK_ICON = ":/kick.png"
IGNORE_ICON = ":/ignore.png"
UNIGNORE_ICON = ":/unignore.png"
WHOIS_ICON = ":/whois.png"

# =====================
# | WINDOW MANAGEMENT |
# =====================

import erk.windows.channel as Channel
import erk.windows.user as User
import erk.windows.console as Console

WINDOW_WIDGET_MARGIN = 2

DEFAULT_WINDOW_WIDTH = 500
DEFAULT_WINDOW_HEIGHT = 275

def ChannelWindow(channel,MDI,client,parent=None):

		newSubwindow = QMdiSubWindow()
		newWindow = Channel.Window(channel,WINDOW_WIDGET_MARGIN,newSubwindow,client,parent)
		newSubwindow.setWidget(newWindow)
		newSubwindow.window = newWindow
		MDI.addSubWindow(newSubwindow)

		#newSubwindow.resize(DEFAULT_WINDOW_WIDTH,DEFAULT_WINDOW_HEIGHT)
		newSubwindow.resize(parent.default_window_width,parent.default_window_height)

		newSubwindow.show()

		return newWindow

def UserWindow(channel,MDI,client,parent=None):

		newSubwindow = QMdiSubWindow()
		newWindow = User.Window(channel,WINDOW_WIDGET_MARGIN,newSubwindow,client,parent)
		newSubwindow.setWidget(newWindow)
		newSubwindow.window = newWindow
		MDI.addSubWindow(newSubwindow)

		newSubwindow.resize(parent.default_window_width,parent.default_window_height)

		newSubwindow.show()

		return newWindow

def ConsoleWindow(channel,MDI,client,parent=None):

		newSubwindow = QMdiSubWindow()
		newWindow = Console.Window(channel,WINDOW_WIDGET_MARGIN,newSubwindow,client,parent)
		newSubwindow.setWidget(newWindow)
		newSubwindow.window = newWindow
		MDI.addSubWindow(newSubwindow)

		#newSubwindow.resize(DEFAULT_WINDOW_WIDTH,DEFAULT_WINDOW_HEIGHT)
		newSubwindow.resize(parent.default_window_width,parent.default_window_height)

		newSubwindow.show()

		return newWindow

# =====================
# | DIALOG MANAGEMENT |
# =====================

def ErrorDialog(message,title="Error",icon=ERK_ICON):
	msg = QMessageBox()
	msg.setWindowIcon(QIcon(icon))
	msg.setIcon(QMessageBox.Critical)
	msg.setText(message)
	msg.setWindowTitle(title)
	msg.exec_()

import erk.dialogs.connect as Connect

def ConnectDialog():
	x = Connect.Dialog(SSL_AVAILABLE)
	info = x.get_connect_information(SSL_AVAILABLE)

	if not info: return None
	return info

import erk.dialogs.network as Network

def NetworkDialog():
	x = Network.Dialog(SSL_AVAILABLE)
	info = x.get_connect_information(SSL_AVAILABLE)

	if not info: return None
	return info

# =====================
# | SUPPORT FUNCTIONS |
# =====================

def restart_program():
	python = sys.executable
	os.execl(python, python, * sys.argv)


