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
import urllib.parse
import posixpath

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = QApplication(sys.argv)

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from erk import *
from erk.common import *
from erk.irc import connect,connectSSL,reconnect,reconnectSSL

parser = argparse.ArgumentParser(
	prog=f"python {PROGRAM_FILENAME}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f''' ___      _   
|__ \ _ _| |__	|===============
/ _  | '_| / /	| {APPLICATION_NAME} {APPLICATION_VERSION}
\___/|_| |_\_\\	|===============

An open source IRC client
''',
	epilog=f'''Official {APPLICATION_NAME} source code repository
https://github.com/nutjob-laboratories/erk''',
	add_help=False,
)

user_info = get_user()

proggroup = parser.add_argument_group('Connect to IRC on startup')

proggroup.add_argument("server", type=str,help="Server to connect to", metavar="SERVER", nargs='?')
proggroup.add_argument("port", type=int,help="Server port to connect to (6667)", default=6667, nargs='?', metavar="PORT")
proggroup.add_argument("-p","--password", type=str,help="Use server password to connect", metavar="PASSWORD", default='')
proggroup.add_argument("-c","--channel", type=str,help="Join channel on connection", metavar="CHANNEL[:KEY]", action='append')
proggroup.add_argument( "--autojoin", help=f"Autojoin channels on connection", action="store_true")
proggroup.add_argument( "--ssl", help=f"Use SSL to connect to IRC", action="store_true")
proggroup.add_argument( "--reconnect", help=f"Reconnect to servers on disconnection", action="store_true")
proggroup.add_argument("-U","--url", type=str,help="Use an IRC URL for server information", metavar="URL", default='')

usergroup = parser.add_argument_group('User options')

usergroup.add_argument("-n","--nickname", type=str,help=f"Nickname to use ({user_info['nickname']})",default=user_info["nickname"], metavar="NICK")
usergroup.add_argument("-a","--alternate", type=str,help=f"Alternate nickname to use ({user_info['alternate']})",default=user_info["alternate"], metavar="NICK")
usergroup.add_argument("-u","--username", type=str,help=f"Username to use ({user_info['username']})",default=user_info["username"], metavar="USER")
usergroup.add_argument("-r","--realname", type=str,help=f"Realname to use ({user_info['realname']})",default=user_info["realname"], metavar="NAME")

infogroup = parser.add_argument_group('Application information')

infogroup.add_argument( "-v", "--version", help=f"Display version", action="store_true")
infogroup.add_argument( "-l", "--licence", help=f"Display software license", action="store_true")

configgroup = parser.add_argument_group('Configuration options')

configgroup.add_argument("--config", type=str,help="Load configuration file",default=SETTINGS_FILE, metavar="FILE")
configgroup.add_argument("--style", type=str,help="Load text style file",default=TEXT_SETTINGS_FILE, metavar="FILE")
configgroup.add_argument( "--forget", help=f"Delete connection history", action="store_true")
configgroup.add_argument( "--default", help=f"Reset configuration to default", action="store_true")

optgroup = parser.add_argument_group('Options')

optgroup.add_argument("-h", "--help", help=f"Displays help", action="help")
optgroup.add_argument( "--top", help=f"Display window on top of all other windows", action="store_true")
optgroup.add_argument( "--full", help=f"Fill screen with application window", action="store_true")
optgroup.add_argument( "--maximize", help=f"Display window maximized", action="store_true")
optgroup.add_argument( "--beat", type=int,help=f"Set \"keep alive\" heartbeat interval ({str(DEFAULT_KEEPALIVE_INTERVAL)})", metavar="SECONDS")
optgroup.add_argument( "--oldschool", help=f"Run in \"old school\" mode", action="store_true")
optgroup.add_argument( "--dump", help=f"Print all network traffic to the console", action="store_true")

disablegroup = parser.add_argument_group('Disable features')

disablegroup.add_argument( "--noignore", help=f"Disable user ignoring", action="store_true")

args = parser.parse_args()

# ====================
# | USER INFORMATION |
# ====================

edited_user_info = False
new_user = {
	"nickname": user_info['nickname'],
	"username": user_info['username'],
	"realname": user_info['realname'],
	"alternate": user_info['alternate'],
}

if args.nickname!=user_info['nickname']:
	new_user['nickname'] = args.nickname
	edited_user_info = True

if args.alternate!=user_info['alternate']:
	new_user['alternate'] = args.alternate
	edited_user_info = True

if args.username!=user_info['username']:
	new_user['username'] = args.username
	edited_user_info = True

if args.realname!=user_info['realname']:
	new_user['realname'] = args.realname
	edited_user_info = True

if edited_user_info: save_user(new_user)

# =======================
# | LICENSE AND VERSION |
# =======================

if args.licence:
	print(GPL_NOTIFICATION,end='')
	sys.exit(0)

if args.version:
	print(APPLICATION_VERSION,end='')
	sys.exit(0)

exit_on_delete = False

if args.forget:
	print("Deleting history...",end='')
	os.remove(HISTORY_FILE)
	os.remove(VISITED_FILE)
	print("done.",end='')
	exit_on_delete = True

if args.default:
	print("Deleting configuration files...",end='')
	os.remove(USER_FILE)
	os.remove(LAST_SERVER_INFORMATION_FILE)
	os.remove(CHANNELS_FILE)
	os.remove(IGNORE_FILE)
	os.remove(SETTINGS_FILE)
	print("done.",end='')
	exit_on_delete = True

if exit_on_delete: sys.exit(0)

if __name__ == '__main__':
	app = QApplication([])
	# app.setStyle("Windows")

	custom_style = ErkStyle('Windows')
	app.setStyle(custom_style)

	GUI = Erk(app,args.config,args.style)

	if args.dump: GUI.view_all_traffic = True

	if args.top:
		GUI.setWindowFlags(GUI.windowFlags() | Qt.WindowStaysOnTopHint)
		GUI.window_on_top = True
		GUI.actOnTop.setChecked(True)

	if args.beat:
		GUI.keep_alive_interval = args.beat

	if args.full:
		GUI.window_fullscreen = True
		GUI.actFullscreen.setChecked(True)
		GUI.showFullScreen()
	else:
		if args.maximize:
			GUI.showMaximized()
		else:
			GUI.show()

	if args.oldschool:
		GUI.oldschoolMode()

	if args.noignore:
		GUI.noIgnore()

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
									GUI.autojoins[args.server].append(channel)
							else:
								if c[1:]!='#': c = '#'+c
								GUI.autojoins[args.server].append([c,''])

	if args.server:
		server = args.server
		port = args.port

		if args.autojoin:
			for c in loadChannels():
				GUI.autojoins[server].append(c) 

		if args.channel:
			if server in GUI.autojoins:
				for c in args.channel:
					p = c.split(':')
					if len(p)==2:
						GUI.autojoins[server].append(p)
					else:
						GUI.autojoins[server].append([c,''])
			else:
				GUI.autojoins[server] = []
				for c in args.channel:
					p = c.split(':')
					if len(p)==2:
						GUI.autojoins[server].append(p)
					else:
						GUI.autojoins[server].append([c,''])


		if args.ssl:
			if args.reconnect:
				func = reconnectSSL
			else:
				func = connectSSL
		else:
			if args.reconnect:
				func = reconnect
			else:
				func = connect

		func(
			nickname=new_user['nickname'],
			server=server,
			port=port,
			alternate=new_user['alternate'],
			password=args.password,
			username=new_user['username'],
			realname=new_user['realname'],
			ssl=args.ssl,
			gui=GUI,
			reconnect=args.reconnect
		)

	reactor.run()
