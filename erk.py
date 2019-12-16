
import argparse

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

app = QApplication([])

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from erk.dialogs import ComboDialog
from erk.main import Erk
from erk.strings import *

parser = argparse.ArgumentParser(
	prog=f"python {PROGRAM_FILENAME}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f''' ___      _   
|__ \ _ _| |__	|==============
/ _  | '_| / /	| {APPLICATION_NAME} {APPLICATION_VERSION}
\___/|_| |_\_\\	|==============

An open source IRC client
''',
	epilog=f'''Official {APPLICATION_NAME} source code repository
https://github.com/nutjob-laboratories/erk''',
	#add_help=False,
)

parser.add_argument( "-n","--noconnect", help=f"Don't ask for a server to connect to on start", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':

	app = QApplication([])

	if args.noconnect:
		GUI = Erk(app)
		GUI.show()
	else:
		info = ComboDialog()
		if info!=None:
			GUI = Erk(app,info)
			GUI.show()
		else:
			app.quit()


	reactor.run()
