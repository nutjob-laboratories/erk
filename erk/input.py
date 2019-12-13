
#import erk.events
import emoji

from erk.objects import *
from erk.files import *
import erk.config

COMMON_COMMANDS = {
	"/log": "/log",
	"/msg": "/msg ",
	"/switch": "/switch ",
	"/part": "/part ",
	"/join": "/join ",
	"/nick": "/nick ",
	"/connect": "/connect ",
	"/reconnect": "/reconnect ",
	"/ssl": "/ssl ",
	"/ressl": "/ressl ",
}

CHANNEL_COMMANDS = {
	"/me": "/me ",	
	"/part": "/part",
}

PRIVATE_COMMANDS = {
	"/me": "/me ",	
}

def handle_channel_input(window,client,text):

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()=='/me' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if erk.config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)
			if erk.config.USE_ASCIIMOJIS: msg = inject_asciiemojis(msg)
			client.describe(window.name,msg)
			out = Message(ACTION_MESSAGE,client.nickname,msg)
			window.writeText(out)
			return True
		if tokens[0].lower()=='/me':
			msg = Message(ERROR_MESSAGE,'',"Usage: /me [MESSAGE]")
			window.writeText(msg)
			return True

	# Handle channel-specific cases of the /part command
	if len(tokens)>0:
		if tokens[0].lower()=='/part' and len(tokens)==1:
			window.leaveChannel(window.name)
			return True
		if tokens[0].lower()=='/part' and len(tokens)>=2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# channel has not been passed as an argument
				tokens.pop(0)
				partmsg = ' '.join(tokens)
				window.leaveChannel(window.name,partmsg)
				return True

	if handle_common_input(window,client,text): return

	if erk.config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)
	if erk.config.USE_ASCIIMOJIS: text = inject_asciiemojis(text)
	
	client.msg(window.name,text)

	out = Message(SELF_MESSAGE,client.nickname,text)
	window.writeText(out)

def handle_private_input(window,client,text):

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()=='/me' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if erk.config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)
			if erk.config.USE_ASCIIMOJIS: msg = inject_asciiemojis(msg)
			client.describe(window.name,msg)
			out = Message(ACTION_MESSAGE,client.nickname,msg)
			window.writeText(out)
			return True
		if tokens[0].lower()=='/me':
			msg = Message(ERROR_MESSAGE,'',"Usage: /me [MESSAGE]")
			window.writeText(msg)
			return True

	if handle_common_input(window,client,text): return

	if erk.config.USE_EMOJIS: text = emoji.emojize(text,use_aliases=True)
	if erk.config.USE_ASCIIMOJIS: text = inject_asciiemojis(text)
	
	client.msg(window.name,text)

	out = Message(SELF_MESSAGE,client.nickname,text)
	window.writeText(out)

def handle_console_input(window,client,text):
	
	if handle_common_input(window,client,text): return

def handle_common_input(window,client,text):

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()=='/quit' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			window.parent.disconnect_current(msg)
			return True
		if tokens[0].lower()=='/quit' and len(tokens)==1:
			window.parent.disconnect_current()
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/msg' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)

			if erk.config.USE_EMOJIS: msg = emoji.emojize(msg,use_aliases=True)
			if erk.config.USE_ASCIIMOJIS: msg = inject_asciiemojis(msg)

			client.msg(target,msg)

			if target in window.channelList():
				swin = window.nameToChannel(target)
				msg = Message(SELF_MESSAGE,client.nickname,msg)
				swin.writeText(msg)
				return True

			if target in window.privateList():
				swin = window.nameToPrivate(target)
				msg = Message(SELF_MESSAGE,client.nickname,msg)
				swin.writeText(msg)
				return True

			if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
				# Target was not a channel
				if erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
					window.newPrivate(target)
					swin = window.nameToPrivate(target)
					msg = Message(SELF_MESSAGE,client.nickname,msg)
					swin.writeText(msg)
					return True

		if tokens[0].lower()=='/msg':
			msg = Message(ERROR_MESSAGE,'',"Usage: /msg TARGET MESSAGE")
			window.writeText(msg)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/part' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			if not channel in window.channelList():
				msg = Message(ERROR_MESSAGE,'',"You are not in "+channel)
				window.writeText(msg)
				return True
			window.leaveChannel(channel)
			return True
		if tokens[0].lower()=='/part' and len(tokens)>=2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# channel has not been passed as an argument
				msg = Message(ERROR_MESSAGE,'',"Usage: /part CHANNEL [MESSAGE]")
				window.writeText(msg)
				return True
			tokens.pop(0)
			channel = tokens.pop(0)
			if not channel in window.channelList():
				msg = Message(ERROR_MESSAGE,'',"You are not in "+channel)
				window.writeText(msg)
				return True
			partmsg = ' '.join(tokens)
			window.leaveChannel(channel,partmsg)
			return True
		if tokens[0].lower()=='/part':
			msg = Message(ERROR_MESSAGE,'',"Usage: /part CHANNEL [MESSAGE]")
			window.writeText(msg)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/join' and len(tokens)==3:
			tokens.pop(0)
			channel = tokens.pop(0)
			key = tokens.pop(0)
			client.join(channel,key)
			return True
		if tokens[0].lower()=='/join' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			client.join(channel)
			return True
		if tokens[0].lower()=='/join':
			window.doJoin(client)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/nick' and len(tokens)==2:
			tokens.pop(0)
			newnick = tokens.pop(0)
			client.setNick(newnick)
			return True
		if tokens[0].lower()=='/nick':
			window.doNick(client)
			return True

	return False

def handle_input(window,client,text):
	if len(text.strip())==0: return

	if handle_ui_input(window,client,text): return
	
	if window.type==erk.config.CHANNEL_WINDOW:
		handle_channel_input(window,client,text)
	elif window.type==erk.config.PRIVATE_WINDOW:
		handle_private_input(window,client,text)
	elif window.type==erk.config.SERVER_WINDOW:
		handle_console_input(window,client,text)

def handle_ui_input(window,client,text):

	tokens = text.split()

	if len(tokens)>0:
		if tokens[0].lower()=='/switch' and len(tokens)==2:
			tokens.pop(0)
			winname = tokens.pop(0)
			channels = window.channelList()
			privates = window.privateList()

			if winname.lower()=="list":
				dl = channels + privates
				msg = Message(SYSTEM_MESSAGE,'',"Available chats: "+', '.join(dl))
				window.writeText(msg)
				return True

			if not winname in channels:
				if not winname in privates:
					msg = Message(ERROR_MESSAGE,'',"No chat named \""+winname+"\" found")
					window.writeText(msg)
					return True
			if winname in channels:
				swin = window.nameToChannel(winname)
			elif winname in privates:
				swin = window.nameToPrivate(winname)
			else:
				msg = Message(ERROR_MESSAGE,'',"No chat named \""+winname+"\" found")
				window.writeText(msg)
				return True
			window.parent.stack.setCurrentWidget(swin)
			return True
		if tokens[0].lower()=='/switch':
			msg = Message(ERROR_MESSAGE,'',"Usage: /switch CHAT_NAME")
			window.writeText(msg)
			return True

	if len(tokens)>0:
		if tokens[0].lower()=='/log' and len(tokens)==1:
			window.parent.stack.setCurrentWidget(client.gui.starter)
			return True

	# /connect SERVER [PORT] [PASSWORD]
	# /reconnect SERVER [PORT] [PASSWORD]
	# /ssl ...
	# /ressl ...
	if len(tokens)>0:

		if tokens[0].lower()=='/connect' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/connect' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/connect' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

			# RECONNECT

		if tokens[0].lower()=='/reconnect' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/reconnect' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/reconnect' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,False,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

			#ssl

		if tokens[0].lower()=='/ssl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ssl' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ssl' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],False,[])
			window.doConnect(info)
			return True

			#ressl

		if tokens[0].lower()=='/ressl' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			port = 6667
			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ressl' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			user = get_user()

			info = ConnectInfo(server,port,None,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/ressl' and len(tokens)==4:
			tokens.pop(0)
			server = tokens.pop(0)
			port = tokens.pop(0)

			try:
				port = int(port)
			except:
				msg = Message(ERROR_MESSAGE,'',"\""+str(port)+"\" is not a valid port number")
				window.writeText(msg)
				return True

			password =tokens.pop(0)

			user = get_user()

			info = ConnectInfo(server,port,password,True,user["nickname"],user["alternate"],user["username"],user["realname"],True,[])
			window.doConnect(info)
			return True

		if tokens[0].lower()=='/connect' or tokens[0].lower()=='/reconnect' or tokens[0].lower()=='/ssl' or tokens[0].lower()=='/ressl':
			window.connectDialog()
			return True

	return False