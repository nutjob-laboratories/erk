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
import argparse
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = QApplication(sys.argv)

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from erk import *
from erk.common import *

parser = argparse.ArgumentParser(
	prog=f"python {PROGRAM_FILENAME}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f'''
 ___      _   
|__ \ _ _| |__	|===============
/ _  | '_| / /	| {APPLICATION_NAME} {APPLICATION_VERSION}
\___/|_| |_\_\\	|===============

An open source IRC client
''',
	epilog='''https://github.com/nutjob-laboratories/erk'''
)

parser.add_argument( "-v", "--version", help=f"Display version", action="store_true")
parser.add_argument( "-l", "--licence", help=f"Display software license", action="store_true")

parser.add_argument( "--ontop", help=f"Display window on top of all other windows", action="store_true")
parser.add_argument( "--fullscreen", help=f"Fill screen with application window", action="store_true")
parser.add_argument( "--maximize", help=f"Display window maximized", action="store_true")

parser.add_argument("--beat", type=int,help=f"\"Keep alive\" heartbeat interval ({str(DEFAULT_KEEPALIVE_INTERVAL)})", metavar="SECONDS")

parser.add_argument("--config", type=str,help="Configuration file",default=SETTINGS_FILE, metavar="FILE")
parser.add_argument("--style", type=str,help="Text style file",default=TEXT_SETTINGS_FILE, metavar="FILE")

args = parser.parse_args()

if args.licence:
	print(GPL_NOTIFICATION,end='')
	sys.exit(0)

if args.version:
	print(APPLICATION_VERSION,end='')
	sys.exit(0)

if __name__ == '__main__':
	app = QApplication([])
	# app.setStyle("Windows")

	custom_style = ErkStyle('Windows')
	app.setStyle(custom_style)

	GUI = Erk(app,args.config,args.style)

	if args.ontop:
		GUI.setWindowFlags(GUI.windowFlags() | Qt.WindowStaysOnTopHint)
		GUI.window_on_top = True
		GUI.actOnTop.setChecked(True)

	if args.beat:
		GUI.keep_alive_interval = args.beat

	if args.fullscreen:
		GUI.window_fullscreen = True
		GUI.actFullscreen.setChecked(True)
		GUI.showFullScreen()
	else:
		if args.maximize:
			GUI.showMaximized()
		else:
			GUI.show()

	reactor.run()
