
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
from erk.config import *

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
