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

from erk.dialogs import ComboDialogBanner
from erk.main import Erk
from erk.files import *
from erk.objects import *
from erk.strings import *
import erk.config
from erk.common import *

from erk.dialogs.settings import Dialog as Settings
from erk.dialogs.scriptedit import Window as ErkScriptEditor
from erk.dialogs.export_log import Dialog as ExportLog

from erk.dialogs.format import Dialog as FormatText

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
congroup.add_argument("-a","--autoscript", help=f"Execute server script on connection (if one exists)", action="store_true")
congroup.add_argument("-s","--script", type=str,help="Execute a custom server script on connection", metavar="FILENAME", action='append')

displaygroup = parser.add_argument_group('Display')

displaygroup.add_argument("-f","--fullscreen", help="Open in fullscreen mode", action="store_true")
displaygroup.add_argument("-o","--ontop", help="Application window is always on top", action="store_true")
displaygroup.add_argument("-W","--width", type=int,help="Set initial window width", default=None, metavar="WIDTH")
displaygroup.add_argument("-H","--height", type=int,help="Set initial window height", default=None, metavar="HEIGHT")

miscgroup = parser.add_argument_group('Configuration')

miscgroup.add_argument("-C","--config", type=str,help="Use an alternate configuration file", metavar="FILE", default=SETTINGS_FILE)
miscgroup.add_argument("-U","--user", type=str,help="Use an alternate user file", metavar="FILE", default=USER_FILE)
miscgroup.add_argument("-Y","--style", type=str,help="Use an alternate text style file", metavar="FILE", default=STYLE_FILE)
miscgroup.add_argument("-L","--logs", type=str,help="Use an alternate log storage location", metavar="DIRECTORY", default=LOG_DIRECTORY)
miscgroup.add_argument("-S","--scripts", type=str,help="Use an alternate script storage location", metavar="DIRECTORY", default=SCRIPTS_DIRECTORY)
miscgroup.add_argument("-T","--styles", type=str,help="Use an alternate style storage location", metavar="DIRECTORY", default=STYLES_DIRECTORY)
miscgroup.add_argument("-M","--macros", type=str,help="Use an alternate macro save file", metavar="FILE", default=MACRO_SAVE_FILE)

devgroup = parser.add_argument_group('Tools')

devgroup.add_argument("--scripter", help="Open the script editor", action="store_true")
devgroup.add_argument("--scripter-edit", dest="scripted",type=str,help="Open a file in the script editor", metavar="FILE", default='')
devgroup.add_argument("--styler", dest="styler", help="Open the style editor", action="store_true")
devgroup.add_argument("--settings", help="Open the preferences dialog", action="store_true")
devgroup.add_argument("--export", dest="xlog", help="Open the log export dialog", action="store_true")

disgroup = parser.add_argument_group('Disable functionality')

disgroup.add_argument( "--noask", help=f"Don't ask for a server to connect to on start", action="store_true")
disgroup.add_argument( "--nosettings", help=f"Disable \"Settings & Tools\" menu", action="store_true")
disgroup.add_argument( "--nomenus", help=f"Disable all menus", action="store_true")
disgroup.add_argument( "--noconnect", help=f"Disable connection commands", action="store_true")
disgroup.add_argument( "--noscripts", help=f"Disable scripting", action="store_true")
disgroup.add_argument( "--nodisplay", help=f"Disable connection display", action="store_true")
disgroup.add_argument( "--nostyles", help=f"Disables style loading and editing", action="store_true")
disgroup.add_argument( "--noedit", help=f"Disables the script editor", action="store_true")
disgroup.add_argument( "--qt5menu", help=f"Disable menu toolbar, and use normal menus", action="store_true")

args = parser.parse_args()

loaded_config_file = False

if __name__ == '__main__':

	app = QApplication([])

	# If the user has passed an alternate configuration file,
	# and the file doesn't exist, create a new config file
	# where the user indicated, with default values

	if args.config:
		if not os.path.isfile(args.config):
			erk.config.load_settings(args.config)
			loaded_config_file = True
			print("\""+args.config+"\" created!")

	if args.style:
		if not os.path.isfile(args.style):
			f = get_text_format_settings(None)
			write_style_file(f,args.style)
			print("\""+args.style+"\" created!")

	if args.user:
		if not os.path.isfile(args.user):
			u = get_user(args.user)
			save_user(u,args.user)
			print("\""+args.user+"\" created!")

	if args.logs:
		if not os.path.isdir(args.logs):
			os.mkdir(args.logs)
			print("\""+args.logs+"\" directory created!")

	if args.scripts:
		if not os.path.isdir(args.scripts):
			os.mkdir(args.scripts)
			print("\""+args.scripts+"\" directory created!")

	if args.styles:
		if not os.path.isdir(args.styles):
			os.mkdir(args.styles)
			print("\""+args.styles+"\" directory created!")

	# Handle the log export dialog
	if args.xlog:

		erk.config.load_settings(args.config)

		if erk.config.DISPLAY_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.DISPLAY_FONT)
			font = f

		app.setFont(font)
		
		x = ExportLog(args.logs,None,app)
		info = x.get_name_information(args.logs,None,app)

		if info:
			
			elog = info[0]
			dlog = info[1]
			llog = info[2]
			do_json = info[3]
			do_epoch = info[4]
			if not do_json:
				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(None,"Save export As...",INSTALL_DIRECTORY,"Text File (*.txt);;All Files (*)", options=options)
				if fileName:
					# extension = os.path.splitext(fileName)[1]
					# if extension.lower()!='txt': fileName = fileName + ".txt"
					efl = len("txt")+1
					if fileName[-efl:].lower()!=f".txt": fileName = fileName+f".txt"
					dump = dumpLog(elog,dlog,llog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()
			else:
				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(None,"Save export As...",INSTALL_DIRECTORY,"JSON File (*.json);;All Files (*)", options=options)
				if fileName:
					# extension = os.path.splitext(fileName)[1]
					# if extension.lower()!='json': fileName = fileName + ".json"
					efl = len("json")+1
					if fileName[-efl:].lower()!=f".json": fileName = fileName+f".json"
					dump = dumpLogJson(elog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()

			app.exit()
		else:
			sys.exit(0)

	# Handle opening the style editor

	elif args.styler:

		erk.config.load_settings(args.config)

		if erk.config.DISPLAY_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.DISPLAY_FONT)
			font = f

		app.setFont(font)

		x = FormatText(None,None,None,args.style,app,args.styles)
		x.show()

	# Handle opening the settings dialog

	elif args.settings:

		erk.config.load_settings(args.config)

		if erk.config.DISPLAY_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.DISPLAY_FONT)
			font = f

		app.setFont(font)

		SETTINGS = Settings(args.config,None,app)
		SETTINGS.show()

	# Handle launching the script editor

	elif args.scripter:

		erk.config.load_settings(args.config)

		if erk.config.DISPLAY_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.DISPLAY_FONT)
			font = f

		app.setFont(font)

		EDITOR = ErkScriptEditor(None,None,args.config,args.scripts,app)
		EDITOR.resize(int(erk.config.DEFAULT_APP_WIDTH),int(erk.config.DEFAULT_APP_HEIGHT))
		EDITOR.show()

	elif args.scripted:

		file = args.scripted
		if not os.path.isfile(file):
			print("\""+file+"\" doesn't exist. Please use --scripter to create a new file.")
			sys.exit(1)

		erk.config.load_settings(args.config)

		if erk.config.DISPLAY_FONT=='':
			id = QFontDatabase.addApplicationFont(DEFAULT_FONT)
			_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
			font = QFont(_fontstr,9)
		else:
			f = QFont()
			f.fromString(erk.config.DISPLAY_FONT)
			font = f

		app.setFont(font)

		EDITOR = ErkScriptEditor(file,None,args.config,args.scripts,app)
		EDITOR.resize(int(erk.config.DEFAULT_APP_WIDTH),int(erk.config.DEFAULT_APP_HEIGHT))
		EDITOR.show()

	else:

		if not loaded_config_file:
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

		# Handle disabling connect commands

		if args.noconnect: erk.config.DISABLE_CONNECT_COMMANDS = True

		# Disable scripting, if it's disabled in the config file
		is_scripting_enabled = args.noscripts
		if not erk.config.ENABLE_SCRIPTS:
			is_scripting_enabled = True

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

			if args.noscripts:
				if args.autoscript:
					print("Server script cannot execute: scripting has been disabled")
					sys.exit(1)
				if args.script!=None:
					print("Server script cannot execute: scripting has been disabled")
					sys.exit(1)

			autoscript = None
			if args.autoscript:
				autoscript = load_auto_script(args.server,args.port,args.scripts)

			if args.script:
				for s in args.script:
					sfile = find_script_file(s,args.scripts)
					if sfile==None:
						print("Script not found: "+s)
						sys.exit(1)

					if os.path.isfile(sfile):
						f=open(sfile, "r")
						cscript = f.read()
						f.close()

						if len(cscript)>0:
							if cscript[-1]!="\n": cscript = cscript + "\n"

						if autoscript!=None:
							autoscript = autoscript + cscript
						else:
							autoscript = cscript

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
					chans,
					u["failreconnect"],
					False,
					autoscript,
				)
			GUI = Erk(
				app,
				i,
				args.nosettings,
				args.nomenus,
				args.config,
				args.style,
				args.user,
				args.fullscreen,
				args.width,
				args.height,
				args.logs,
				is_scripting_enabled,
				args.scripts,
				args.nodisplay,
				args.ontop,
				args.qt5menu,
				args.styles,
				args.nostyles,
				args.noedit,
				args.macros,
				)
			GUI.show()
		else:

			# Handle launching without the connection dialog

			if args.noask:
				GUI = Erk(
					app,
					None,
					args.nosettings,
					args.nomenus,
					args.config,
					args.style,
					args.user,
					args.fullscreen,
					args.width,
					args.height,
					args.logs,
					is_scripting_enabled,
					args.scripts,
					args.nodisplay,
					args.ontop,
					args.qt5menu,
					args.styles,
					args.nostyles,
					args.noedit,
					args.macros,
					)
				GUI.show()

			# Handle connecting to the last server

			elif args.last:

				u = get_user(args.user)

				if args.noscripts:
					if args.autoscript:
						print("Server script cannot execute: scripting has been disabled")
						sys.exit(1)
					if args.script!=None:
						print("Server script cannot execute: scripting has been disabled")
						sys.exit(1)

				autoscript = None
				if args.autoscript:
					autoscript = load_auto_script(u["last_server"],u["last_port"],args.scripts)

				if args.script:
					for s in args.script:
						sfile = find_script_file(s,args.scripts)
						if sfile==None:
							print("Script not found: "+s)
							sys.exit(1)

						if os.path.isfile(sfile):
							f=open(sfile, "r")
							cscript = f.read()
							f.close()

							if len(cscript)>0:
								if cscript[-1]!="\n": cscript = cscript + "\n"

							if autoscript!=None:
								autoscript = autoscript + cscript
							else:
								autoscript = cscript

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
						c,
						u["failreconnect"],
						False,
						autoscript,
					)
				GUI = Erk(
					app,
					i,
					args.nosettings,
					args.nomenus,
					args.config,
					args.style,
					args.user,
					args.fullscreen,
					args.width,
					args.height,
					args.logs,
					is_scripting_enabled,
					args.scripts,
					args.nodisplay,
					args.ontop,
					args.qt5menu,
					args.styles,
					args.nostyles,
					args.noedit,
					args.macros,
					)
				GUI.show()
			else:

				# Launch normally, showing the connection dialog first
				info = ComboDialogBanner(args.user,is_scripting_enabled,args.scripts,args.config)
				if info!=None:
					GUI = Erk(
						app,
						info,
						args.nosettings,
						args.nomenus,
						args.config,
						args.style,
						args.user,
						args.fullscreen,
						args.width,
						args.height,
						args.logs,
						is_scripting_enabled,
						args.scripts,
						args.nodisplay,
						args.ontop,
						args.qt5menu,
						args.styles,
						args.nostyles,
						args.noedit,
						args.macros,
						)
					GUI.show()
				else:
					app.quit()

	reactor.run()
