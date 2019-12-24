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
from erk.files import *
from erk.objects import *
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
parser.add_argument( "-l","--last", help=f"Automatically connect to the last server connected to", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':

	app = QApplication([])

	if args.noconnect:
		GUI = Erk(app)
		GUI.show()
	elif args.last:
		u = get_user()
		if u["last_password"] == '':
			pword = None
		else:
			pword = u["last_password"]
		if u["autojoin"]:
			c = u["channels"]
		else:
			c = []
		i = ConnectInfo(
				u["last_server"],
				int(u["last_port"]),
				pword,
				u["ssl"],
				u["nickname"],
				u["alternate"],
				u["username"],
				u["realname"],
				u["reconnect"],
				c
			)
		GUI = Erk(app,i)
		GUI.show()
	else:
		info = ComboDialog()
		if info!=None:
			GUI = Erk(app,info)
			GUI.show()
		else:
			app.quit()


	reactor.run()
