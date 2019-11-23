
import argparse
import urllib.parse
import posixpath

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = QApplication([])

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from erk.main import Erk
from erk.irc import connect,connectSSL,reconnect,reconnectSSL
from erk.strings import *

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
	#add_help=False,
)

parser.add_argument("server", type=str,help="Server to connect to", metavar="SERVER", nargs='?')
parser.add_argument("port", type=int,help="Server port to connect to (6667)", default=6667, nargs='?', metavar="PORT")

parser.add_argument("-u","--url", type=str,help="Use an IRC URL for server information", metavar="URL", default='')
parser.add_argument("-c","--channel", type=str,help="Join channel on connection", metavar="CHANNEL[:KEY]", action='append')
parser.add_argument("-p","--password", type=str,help="Use server password to connect", metavar="PASSWORD", default='')
parser.add_argument( "--ssl", help=f"Use SSL to connect to IRC", action="store_true")
parser.add_argument( "--reconnect", help=f"Reconnect to servers on disconnection", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':
	app = QApplication([])

	GUI = Erk(app)

	if args.channel:
		p = []
		for e in args.channel:
			ep=e.split(':')
			if len(ep)==2:
				p.append([ep[0],ep[1]])
			else:
				p.append([e,''])
		args.channel = p
	else:
		args.channel = []

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


	if args.server:
		server = args.server
		port = args.port

		user_info = get_user()

		if not args.password:
			args.password = None

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
			nickname=user_info["nickname"],
			server=server,
			port=port,
			alternate=user_info["alternate"],
			password=args.password,
			username=user_info["username"],
			realname=user_info["realname"],
			ssl=args.ssl,
			gui=GUI,
			reconnect=args.reconnect,
			autojoin=args.channel,
			disconnected_on_purpose=False
		)

	GUI.show()

	reactor.run()