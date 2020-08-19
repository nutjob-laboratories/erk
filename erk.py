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
import string
import shutil
import sys
import os
from zipfile import ZipFile
import urllib.parse
import posixpath

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

app = QApplication([])

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from erk.dialogs import ComboDialog,EditorDialog
from erk.main import Erk
from erk.files import *
from erk.objects import *
from erk.strings import *
import erk.config
from erk.common import *
from erk.plugins import PLUGIN_DIRECTORY

# Handle commandline arguments

parser = argparse.ArgumentParser(
	prog=f"python {PROGRAM_FILENAME}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f''' ___      _   
|__ \ _ _| |__	|==============
/ _  | '_| / /	| {APPLICATION_NAME} {APPLICATION_VERSION}
\___/|_| |_\_\\	|==============

An open source, cross-platform IRC client
https://github.com/nutjob-laboratories/erk
''',
)

congroup = parser.add_argument_group('Connection')

congroup.add_argument("server", type=str,help="Server to connect to", metavar="SERVER", nargs='?')
congroup.add_argument("port", type=int,help="Server port to connect to (6667)", default=6667, nargs='?', metavar="PORT")
congroup.add_argument( "--ssl", help=f"Use SSL to connect to IRC", action="store_true")
congroup.add_argument( "--reconnect", help=f"Reconnect to servers on disconnection", action="store_true")
congroup.add_argument("-p","--password", type=str,help="Use server password to connect", metavar="PASSWORD", default='')
congroup.add_argument("-c","--channel", type=str,help="Join channel on connection", metavar="CHANNEL[:KEY]", action='append')
congroup.add_argument("-l","--last", help=f"Automatically connect to the last server connected to", action="store_true")
congroup.add_argument("-u","--url", type=str,help="Use an IRC URL to connect", metavar="URL", default='')

disgroup = parser.add_argument_group('Disable functionality')

disgroup.add_argument( "-P","--noplugins", help=f"Disable plugins", action="store_true")
disgroup.add_argument( "-M","--nomacros", help=f"Disable macros", action="store_true")
disgroup.add_argument( "-N","--noask", help=f"Don't ask for a server to connect to on start", action="store_true")

devgroup = parser.add_argument_group('Plugins')

devgroup.add_argument("--generate", type=str,help="Generate a \"blank\" plugin package in the current directory", metavar="NAME", default='')
devgroup.add_argument("--new", help="Generate a \"blank\" plugin package in the plugins directory", action="store_true")
devgroup.add_argument("--editor", help="Open the code editor", action="store_true")
devgroup.add_argument("--edit", type=str,help="Open a file in the code editor", metavar="FILE", default='')
devgroup.add_argument("--install", type=str,help="Install a plugin", metavar="ZIP", default='')

displaygroup = parser.add_argument_group('Display')

displaygroup.add_argument("-f","--fullscreen", help="Open in fullscreen mode", action="store_true")
displaygroup.add_argument("-W","--width", type=int,help="Set initial window width", default=None, metavar="WIDTH")
displaygroup.add_argument("-H","--height", type=int,help="Set initial window height", default=None, metavar="HEIGHT")

miscgroup = parser.add_argument_group('Configuration')

miscgroup.add_argument("-C","--config", type=str,help="Use an alternate configuration file", metavar="FILE", default=SETTINGS_FILE)
miscgroup.add_argument("-U","--user", type=str,help="Use an alternate user file", metavar="FILE", default=USER_FILE)
miscgroup.add_argument("-F","--format", type=str,help="Use an alternate text format file", metavar="FILE", default=STYLE_FILE)


args = parser.parse_args()

if __name__ == '__main__':

	app = QApplication([])

	# If the user has passed an alternate configuration file,
	# and the file doesn't exist, create a new config file
	# where the user indicated, with default values

	if args.config:
		if not os.path.isfile(args.config):
			erk.config.load_settings(args.config)
			print("\""+args.config+"\" created!")

	if args.format:
		if not os.path.isfile(args.format):
			f = get_text_format_settings(None)
			write_style_file(f,args.format)
			print("\""+args.format+"\" created!")

	if args.user:
		if not os.path.isfile(args.user):
			u = get_user(args.user)
			save_user(u,args.user)
			print("\""+args.user+"\" created!")

	# Handle installing plugins

	if args.install:
		file = args.install
		if not os.path.isfile(file):
			print("\""+file+"\" doesn't exist.")
			sys.exit(1)

		print("Installing plugin \""+file+"\"...")
		with ZipFile(file,'r') as zipObj:
			zipObj.extractall(PLUGIN_DIRECTORY)
		print("Done!")
		sys.exit(0)

	# Handle launching the editor

	elif args.editor:
		erk.config.load_settings(args.config)

		if erk.config.EDITOR_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.EDITOR_FONT)
			font = f

		app.setFont(font)

		EDITOR = EditorDialog(None,None,app,args.config)
		EDITOR.resize(int(erk.config.DEFAULT_APP_WIDTH),int(erk.config.DEFAULT_APP_HEIGHT))
		EDITOR.show()

	# Handle opening a file in the editor

	elif args.edit:

		file = args.edit
		if not os.path.isfile(file):
			print("\""+file+"\" doesn't exist. Please use --editor to create a new file.")
			sys.exit(1)

		erk.config.load_settings(args.config)

		if erk.config.EDITOR_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.EDITOR_FONT)
			font = f

		app.setFont(font)

		EDITOR = EditorDialog(None,file,app,args.config)
		EDITOR.resize(int(erk.config.DEFAULT_APP_WIDTH),int(erk.config.DEFAULT_APP_HEIGHT))
		EDITOR.show()

	# Handle creating a new plugin and opening it in the editor

	elif args.new:
		erk.config.load_settings(args.config)

		if erk.config.EDITOR_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.EDITOR_FONT)
			font = f

		app.setFont(font)

		EDITOR = EditorDialog(None,None,app,args.config)
		EDITOR.resize(int(erk.config.DEFAULT_APP_WIDTH),int(erk.config.DEFAULT_APP_HEIGHT))
		EDITOR.show()
		EDITOR.newPackage()

	# Handle creating a new package

	else:

		if args.generate!='':
			safe_name = args.generate
			for c in string.punctuation:
				safe_name=safe_name.replace(c,"")
			safe_name = safe_name.translate( {ord(c): None for c in string.whitespace}  )

			ERK_MODULE_DIRECTORY = os.path.join(sys.path[0], "erk")
			DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")
			PLUGIN_SKELETON = os.path.join(DATA_DIRECTORY, "plugin")

			print("Creating plugin package "+safe_name+"...")
			os.mkdir(safe_name)
			shutil.copy(os.path.join(PLUGIN_SKELETON, "package.png"), os.path.join(safe_name, "package.png"))
			shutil.copy(os.path.join(PLUGIN_SKELETON, "plugin.png"), os.path.join(safe_name, "plugin.png"))
			shutil.copy(os.path.join(PLUGIN_SKELETON, "plugin.py"), os.path.join(safe_name, "plugin.py"))
			shutil.copy(os.path.join(PLUGIN_SKELETON, "package.txt"), os.path.join(safe_name, "package.txt"))

			f = open(os.path.join(safe_name, "package.txt"),"r")
			ptxt = f.read()
			f.close()

			ptxt = ptxt.replace("!PLUGIN_FULL_NAME!",args.generate)

			f = open(os.path.join(safe_name, "package.txt"),"w")
			f.write(ptxt)
			f.close()

			f = open(os.path.join(safe_name, "plugin.py"),"r")
			ppy = f.read()
			f.close()

			ppy = ppy.replace("!PLUGIN_FULL_NAME!",args.generate)
			ppy = ppy.replace("!_PLUGIN_NAME!",safe_name)

			f = open(os.path.join(safe_name, "plugin.py"),"w")
			f.write(ppy)
			f.close()

			print("Done!")

			sys.exit(0)

		# Handle disabling connect commands

		if False: erk.config.DISABLE_CONNECT_COMMANDS = True

		# Handle IRC URLs

		if args.url!='':
			u = urllib.parse.urlparse(args.url)
			if u.scheme=='irc':
				if u.password:
					args.password = u.password
				if u.hostname:
					args.server = u.hostname
				if u.port:
					args.port = u.port
				if u.path!='':
					p = urllib.parse.unquote(u.path)
					p = posixpath.normpath(p)
					l = posixpath.split(p)
					if len(l)>0:
						if l[0]=='/':
							if l[1]!='':
								c = str(l[1])
								if ',' in c:
									channel = c.split(',')
									if len(channel)==2:
										if channel[0][:1]!='#': channel[0] = '#'+channel[0]
										if args.channel:
											args.channel.append([channel[0],channel[1]])
										else:
											args.channel = []
											args.channel.append([channel[0],channel[1]])
								else:
									if c[1:]!='#': c = '#'+c
									if args.channel:
										args.channel.append([c,''])
									else:
										args.channel = []
										args.channel.append([c,''])

		# Handle connecting to a server if one has been provided

		if args.server:
			if args.password=='':
				pword = None
			else:
				pword = args.password
			chans = []
			if args.channel:
				for c in args.channel:
					if type(c)==list:
						chans.append(c)
					else:
						p = c.split(':')
						if len(p)==2:
							chans.append(p)
						else:
							chans.append( [c,''] )
			u = get_user(args.user)
			i = ConnectInfo(
					args.server,
					args.port,
					pword,
					args.ssl,
					u["nickname"],
					u["alternate"],
					u["username"],
					u["realname"],
					args.reconnect,
					chans
				)
			GUI = Erk(app,i,args.noplugins,args.nomacros,False,False,args.config,args.format,args.user,args.fullscreen,args.width,args.height)
			GUI.show()
		else:

			# Handle launching without the connection dialog

			if args.noask:
				GUI = Erk(app,None,args.noplugins,args.nomacros,False,False,args.config,args.format,args.user,args.fullscreen,args.width,args.height)
				GUI.show()

			# Handle connecting to the last server

			elif args.last:
				u = get_user(args.user)
				if u["last_password"] == '':
					pword = None
				else:
					pword = u["last_password"]
				if u["autojoin"]:
					c = u["channels"]
				else:
					c = []
				if args.channel:
					for ch in args.channel:
						p = ch.split(':')
						if len(p)==2:
							c.append(p)
						else:
							c.append( [ch,''] )
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
				GUI = Erk(app,i,args.noplugins,args.nomacros,False,False,args.config,args.format,args.user,args.fullscreen,args.width,args.height)
				GUI.show()
			else:

				# Launch normally, showing the connection dialog first

				info = ComboDialog(args.user)
				if info!=None:
					GUI = Erk(app,info,args.noplugins,args.nomacros,False,False,args.config,args.format,args.user,args.fullscreen,args.width,args.height)
					GUI.show()
				else:
					app.quit()

	reactor.run()
