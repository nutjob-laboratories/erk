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

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = QApplication(sys.argv)

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from erk.gui.main import ErkGUI
from erk.common import *

defaults = get_user()
themeList = getThemeList()
themeflat = ", ".join(themeList)
settings = loadSettings()

parser = argparse.ArgumentParser(
	prog=f"python {PROGRAM_FILENAME}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f"""
{APPLICATION_NAME} IRC Client
An open source IRC client written with Python, Qt5, and Twisted""",
	epilog=f"""SERVER can be a hostname or IP address, a hostname/port pair (SERVER:PORT), or an IRC URL.

Available themes: {themeflat}

Official Ərk repository: https://github.com/nutjob-laboratories/erk
Official Ərk plugin repository: https://github.com/nutjob-laboratories/erk-plugins

Erk Copyright (C) 2019  Dan Hetrick
""",
	add_help=False,
)

proggroup = parser.add_argument_group('Optional Arguments')

proggroup.add_argument('clserver', metavar='SERVER', type=str, nargs='?', help='Server to connect to on startup', default=None)
proggroup.add_argument('clport', metavar='PORT', type=int, nargs='?', help='Port (6667)', default=0)

netgroup = parser.add_argument_group('Server options')

netgroup.add_argument("-P","--password", type=str,help="Server password",default=None)
netgroup.add_argument("-S", "--ssl", help="Connect via SSL", action="store_true")
netgroup.add_argument("-C","--channel", type=str,help=f"Join CHANNEL on connect",default=None, metavar="CHANNEL[:KEY]")

infogroup = parser.add_argument_group('Application information')

infogroup.add_argument( "-v", "--version", help=f"Display version", action="store_true")
infogroup.add_argument( "-l", "--licence", help=f"Display software license", action="store_true")

optgroup = parser.add_argument_group('Options')

optgroup.add_argument("-h", "--help", help=f"Displays help", action="help")

optgroup.add_argument( "--interval", type=int,help="Keep-alive heartbeat interval (120 seconds)", default=120, metavar="SECONDS")
optgroup.add_argument( "--maximize", help=f"Display maximized", action="store_true")
optgroup.add_argument( "--fullscreen", help=f"Displays in full screen mode", action="store_true")
optgroup.add_argument( "--ontop", help=f"{APPLICATION_NAME}'s window is always on top", action="store_true")
optgroup.add_argument( "--noprofanity", help=f"Force profanity filter on", action="store_true")
optgroup.add_argument( "--nocolors", help=f"Force IRC color filter on", action="store_true")
optgroup.add_argument( "--throttle", type=int,help="Throttle notification sounds (60 seconds)", default=60, metavar="SECONDS")

themegroup = parser.add_argument_group('Themes')

themegroup.add_argument( "-t", "--theme", type=str,help=f"Loads a specific theme on startup ({settings['theme']})", metavar="THEME")
themegroup.add_argument("-T","--install-theme", type=str,help=f"Install theme(s) from zip file",default=None, metavar="ZIP_FILE")

configgroup = parser.add_argument_group('Configuration')

configgroup.add_argument("-c","--config", type=str,help=f"Use FILE for configuration",default=None, metavar="FILE")
configgroup.add_argument("-d","--display", type=str,help=f"Use FILE for display configuration",default=None, metavar="FILE")
configgroup.add_argument("--generate-config", type=str,help=f"Writes a default config file to FILE",default=None, metavar="FILE")
configgroup.add_argument("--generate-display", type=str,help=f"Writes a default display config file to FILE",default=None, metavar="FILE")

usergroup = parser.add_argument_group('Set user defaults')

usergroup.add_argument("-n","--nick", type=str,help=f"Set default nickname ({defaults['nick']})", metavar="NICKNAME")
usergroup.add_argument("-a","--alternate", type=str,help=f"Set default alternate nickname ({defaults['alternate']})", metavar="NICKNAME")
usergroup.add_argument("-u","--username", type=str,help=f"Set default username ({defaults['username']})", metavar="USERNAME")
usergroup.add_argument("-r","--realname", type=str,help=f"Set default realname ({defaults['realname']})", metavar="IRCNAME")

forbidGroup = parser.add_argument_group('Disable features')

forbidGroup.add_argument( "--nologs", help=f"Don't save chat logs on window close", action="store_true")
forbidGroup.add_argument( "--nosettings", help=f"Disable settings menu", action="store_true")
forbidGroup.add_argument( "--nossl", help=f"Disable SSL", action="store_true")
forbidGroup.add_argument( "--nowindows", help=f"Disable windows menu", action="store_true")
forbidGroup.add_argument( "--nothemes", help=f"Disable themes", action="store_true")
forbidGroup.add_argument( "--nosystray", help=f"Disable system tray icon", action="store_true")
forbidGroup.add_argument( "--nosound", help=f"Disable audio notifications", action="store_true")
forbidGroup.add_argument( "--nohistory", help=f"Disable loading and saving server history", action="store_true")

logGroup = parser.add_argument_group('Log exporting')

logGroup.add_argument("--exporttext", type=str,help=f"Exports all logs as text", metavar="ZIP")
logGroup.add_argument("--exporthtml", type=str,help=f"Exports all logs as HTML", metavar="ZIP")


args = parser.parse_args()


if args.licence:
	print(GPL_NOTIFICATION)
	sys.exit(0)

if args.version:
	print(APPLICATION_VERSION)
	sys.exit(0)

if args.generate_config:
	config = loadSettings('')
	with open(args.generate_config, "w") as write_data:
		json.dump(config, write_data, indent=4, sort_keys=True)
	if not args.generate_display:
		sys.exit(0)

if args.generate_display:
	config = loadDisplay('')
	with open(args.generate_display, "w") as write_data:
		json.dump(config, write_data, indent=4, sort_keys=True)
		sys.exit(0)

if __name__ == '__main__':

	if args.install_theme:
		if installThemeFromZip(args.install_theme):
			print(f"Installed theme(s) from {args.install_theme}")
			sys.exit(0)
		else:
			print(f"Error installing theme(s) from {args.install_theme}")
			sys.exit(1)

	if args.exporttext:
		lc = exportLogsAsText(args.exporttext)
		if lc>0:
			print(f"{str(lc)} log(s) zipped to {args.exporttext}")
			sys.exit(0)
		else:
			print(f"No logs found in {LOG_DIRECTORY}")
			sys.exit(1)

	if args.exporthtml:
		lc = exportLogsAsHTML(args.exporthtml)
		if lc>0:
			print(f"{str(lc)} log(s) zipped to {args.exporthtml}")
			sys.exit(0)
		else:
			print(f"No logs found in {LOG_DIRECTORY}")
			sys.exit(1)


	app = QApplication([])
	app.setStyle("Windows")

	if args.config:
		if args.display:
			erkClient = ErkGUI(app,args.config,args.display)
		else:
			erkClient = ErkGUI(app,args.config)
	else:
		if args.display:
			erkClient = ErkGUI(app,None,args.display)
		else:
			erkClient = ErkGUI(app)

	if args.noprofanity:
		erkClient.forceProfanityFilter()

	if args.nocolors:
		erkClient.forceNoIRCColors()

	if args.theme:
		if args.theme in themeList:
			erkClient.applyTheme(args.theme)
		else:
			print(f"Can't find theme: {args.theme}")
			sys.exit(1)

	if args.ontop:
		erkClient.setWindowFlags(erkClient.windowFlags() | Qt.WindowStaysOnTopHint)

	erkClient.heartbeatInterval = args.interval

	erkClient.mentionLimit = args.throttle

	if args.nossl:
		erkClient.can_use_ssl = False

	if args.fullscreen:
		erkClient.setWindowFlags(erkClient.windowFlags() | Qt.WindowCloseButtonHint)
		erkClient.setWindowFlags(erkClient.windowFlags() | Qt.WindowType_Mask)
		erkClient.showFullScreen()
	else:
		if args.maximize:
			erkClient.showMaximized()
		else:
			
			erkClient.show()

	if args.nologs:
		erkClient.turnOffLogging()

	if args.nosettings:
		erkClient.hideSettingsMenu()

	if args.nowindows:
		erkClient.disableWindowsMenu()

	if args.nothemes:
		erkClient.disableThemes()

	if args.nosystray:
		erkClient.disableSystray()

	if args.nosound:
		erkClient.disableSound()

	if args.nohistory:
		erkClient.disableSave()

	user = get_user()
	
	changed = False
	if args.nick:
		user["nick"] = args.nick
		changed = True
	if args.username:
		user["username"] = args.username
		changed = True
	if args.realname:
		user["realname"] = args.realname
		changed = True
	if args.alternate:
		user["alternate"] = args.alternate
		changed = True

	if changed: save_user(user)

	nickname = user["nick"]
	alternate = user["alternate"]
	username = user["username"]
	realname = user["realname"]

	if args.clserver!=None:

		channel = None
		chankey = None

		if "irc://" in args.clserver:
			# got an irc url
			t = args.clserver.replace("irc://","",1)
			tp = t.split('/')
			if len(tp)==2:
				server = tp.pop(0)
				channel = tp.pop(0)
			else:
				server = t
				server = server.replace('/',"")

			args.clserver = server

			# check to see if a channel key is provided
			p = channel.split(":")
			if len(p)==2:
				channel=p[0]
				chankey=p[1]

				# check to see if the channel starts with a #,
				# and if not, prepend it
				if len(channel)>0:
					if channel[:1]!="#":
						channel = "#" + channel

		p = args.clserver.split(":")
		if len(p)==2:
			server = p[0]
			port = p[1]
		else:
			server = args.clserver
			if args.clport==0:
				port = "6667"
			else:
				port = str(args.clport)

		if args.channel:
			p = args.channel.split(':')
			if len(p)==2:
				channel = p[0]
				key = p[1]
			else:
				channel = args.channel

			# check to see if the channel starts with a #,
			# and if not, prepend it
			if len(channel)>0:
				if channel[:1]!="#":
					channel = "#" + channel

		if channel!=None:
			erkClient.commandlineJoinChannel = channel

		if chankey!=None:
			erkClient.commandlineJoinChannelKey = chankey

		ci = [nickname,username,realname,alternate,server,port,args.password,args.ssl]
		erkClient.connectToIRC(ci)

	reactor.run()
