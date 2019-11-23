
from erk.resources import *
from erk.strings import *
from erk.widgets import *
from erk.config import *
from erk.common import *
from erk.windows import *
from erk.format import *

CONNECTIONS = []
CHANNEL_WINDOWS = []
PRIVATE_WINDOWS = []
SERVER_WINDOWS = []

# |---------------------------------------------------------|
# | HELPER FUNCTIONS AND EVENTS TRIGGERED BY THE ERK CLIENT |
# |---------------------------------------------------------|

def set_channel_hostmask(gui,client,nickname,hostmask):
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if nickname in window.nicks:
				window.join(nickname,hostmask)

def channel_has_hostmask(gui,client,channel,nickname):
	
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name == channel:
				if nickname in window.hostmasks: return True
	return False

def channelTurnOnNickClick():
	for w in CHANNEL_WINDOWS:
		w.onNickClick()

def channelTurnOffNickClick():
	for w in CHANNEL_WINDOWS:
		w.offNickClick()

def channelShowNicks():
	for w in CHANNEL_WINDOWS:
		w.nick.show()

def channelHideNicks():
	for w in CHANNEL_WINDOWS:
		w.nick.hide()

def refreshDisplayConnection(gui):
	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

def uptime(gui,client,uptime):
	gui.got_uptime(client,uptime)
	for w in SERVER_WINDOWS:
		if w.client.id==client.id: w.set_uptime(uptime)
	for w in CHANNEL_WINDOWS:
		if w.client.id==client.id: w.set_uptime(uptime)
	for w in PRIVATE_WINDOWS:
		if w.client.id==client.id: w.set_uptime(uptime)

def getConnections():
	return CONNECTIONS

def getWindows():
	return [CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS]

def setNewSpellCheckLanguage(lang):
	for w in SERVER_WINDOWS:
		w.userTextInput.changeLanguage(lang)
	for w in CHANNEL_WINDOWS:
		w.userTextInput.changeLanguage(lang)
	for w in PRIVATE_WINDOWS:
		w.userTextInput.changeLanguage(lang)

def toggleSpellcheck():
	for w in SERVER_WINDOWS:
		t = w.userTextInput.toPlainText()
		w.userTextInput.setPlainText(t)
		w.userTextInput.moveCursor(QTextCursor.End)
	for w in CHANNEL_WINDOWS:
		t = w.userTextInput.toPlainText()
		w.userTextInput.setPlainText(t)
		w.userTextInput.moveCursor(QTextCursor.End)
	for w in PRIVATE_WINDOWS:
		t = w.userTextInput.toPlainText()
		w.userTextInput.setPlainText(t)
		w.userTextInput.moveCursor(QTextCursor.End)

def togglePlainUserLists():
	for w in CHANNEL_WINDOWS:
		if w.plain_user_lists:
			w.plain_user_lists = False
		else:
			w.plain_user_lists = True
		w.refreshUserlist()

def rerenderAllText():
	for w in SERVER_WINDOWS:
		w.rerenderText()
	for w in CHANNEL_WINDOWS:
		w.rerenderText()
	for w in PRIVATE_WINDOWS:
		w.rerenderText()

def rerenderAllText_New_Font(gui):
	gui.app.setFont(gui.font)
	gui.connectionTree.setFont(gui.font)
	for w in SERVER_WINDOWS:
		w.setFont(gui.font)
		w.channelChatDisplay.setFont(gui.font)
		w.userTextInput.setFont(gui.font)
		w.rerenderText()
	for w in CHANNEL_WINDOWS:
		w.setFont(gui.font)
		w.channelChatDisplay.setFont(gui.font)
		w.userTextInput.setFont(gui.font)
		b = gui.font
		b.setBold(True)
		w.channelUserDisplay.setFont(b)

		fm = QFontMetrics(w.channelChatDisplay.font())
		fheight = fm.height() + 2
		w.channelUserDisplay.setIconSize(QSize(fheight,fheight))

		w.rerenderText()
	for w in PRIVATE_WINDOWS:
		w.setFont(gui.font)
		w.channelChatDisplay.setFont(gui.font)
		w.userTextInput.setFont(gui.font)
		w.rerenderText()

def user_double_click(gui,client,user):

	# See if a private message window already exists
	window_is_created = False
	private_chat_window = None
	for w in PRIVATE_WINDOWS:
		if w.client.id==client.id:
			if w.name==user:
				window_is_created = True
				private_chat_window = w
				break

	if not window_is_created:
		private_chat_window = PrivateWindow(user,gui.MDI,client,gui)
		PRIVATE_WINDOWS.append(private_chat_window)
	else:
		gui.restoreWindow(private_chat_window,private_chat_window.subwindow)

	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

def erk_parted_private(gui,client,user):
	global PRIVATE_WINDOWS
	clean = []
	for c in PRIVATE_WINDOWS:
		if c.client.id==client.id:
			if c.name==user: continue
		clean.append(c)
	PRIVATE_WINDOWS = clean

	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

def erk_close_channel(gui,client,channel,msg=None):
	for c in CHANNEL_WINDOWS:
		if c.client.id==client.id:
			if c.name==channel:
				if msg:
					c.part_message = msg
				c.close()

def erk_parted_channel(gui,client,channel):
	global CHANNEL_WINDOWS
	clean = []
	for c in CHANNEL_WINDOWS:
		if c.client.id==client.id:
			if c.name==channel: continue
		clean.append(c)
	CHANNEL_WINDOWS = clean

	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			message = "Left "+channel
			w.writeLog(SYSTEM_MESSAGE,'',message)

def erk_joined_channel(gui,client,channel):
	
	w = ChannelWindow(channel,gui.MDI,client,gui)
	CHANNEL_WINDOWS.append(w)

	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			message = "Joined "+channel
			w.writeLog(SYSTEM_MESSAGE,'',message)

	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name==channel:
				message = "Joined "+channel
				window.writeLog(SYSTEM_MESSAGE,'',message)

def outgoing_message(gui,client,target,message):
	
	for window in PRIVATE_WINDOWS:
		if window.client.id==client.id:
			if window.name==target:
				window.writeLog(SELF_MESSAGE,client.nickname,message)
				return

	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name==target:
				window.writeLog(SELF_MESSAGE,client.nickname,message)
				return

	if len(target)>0:
		if target[0]=='&' or target[0]=='#' or target[0]=='!':
			# message target is a channel
			# do *not* open a window
			pass
		else:
			# message target is a user
			# open a private message window
			private_chat_window = PrivateWindow(target,gui.MDI,client,gui)
			PRIVATE_WINDOWS.append(private_chat_window)
			gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

			private_chat_window.writeLog(CHAT_MESSAGE,target,message)

def outgoing_action_message(gui,client,channel,message):

	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name==channel:
				window.writeLog(ACTION_MESSAGE,client.nickname,client.nickname+" "+message)
				return

	for window in PRIVATE_WINDOWS:
		if window.client.id==client.id:
			if window.name==channel:
				window.writeLog(ACTION_MESSAGE,client.nickname,client.nickname+" "+message)

def erk_changed_nick(gui,client,newnick):

	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			client.sendLine("NAMES "+window.name)
			message = "You are now known as "+newnick
			window.writeLog(SYSTEM_MESSAGE,'',message)
			window.setNick(newnick)
	
	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			message = "You are now known as "+newnick
			w.writeLog(SYSTEM_MESSAGE,'',message)

def setChannelKey(gui,client,channel,key):
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name == channel: window.setKey(key)
	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

def setChannelModes(client,channel,modes):
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name == channel:
				for l in modes:
					if l in window.modesoff:
						window.modesoff = window.modesoff.replace(l,"")
					if l in window.modeson:
						pass
					else:
						window.modeson = window.modeson + l

def unsetChannelModes(client,channel,modes):
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name == channel:
				for l in modes:
					if l in window.modeson:
						window.modeson = window.modeson.replace(l,"")
					if l in window.modesoff:
						pass
					else:
						window.modesoff = window.modesoff + l

def writeSytemMsgChannel(client,channel,msg):
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name == channel: window.writeLog(SYSTEM_MESSAGE,'',msg)

def writeErrorMsgActiveWindow(gui,client,msg):

	if gui.active_window:
		channel = gui.active_window.name
		cid = gui.active_window.client.id

		for window in CHANNEL_WINDOWS:
			if window.client.id==cid:
				if window.name == channel: window.writeLog(ERROR_MESSAGE,'',msg)

		for window in PRIVATE_WINDOWS:
			if window.client.id==cid:
				if window.name == channel: window.writeLog(ERROR_MESSAGE,'',msg)

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			w.writeLog(ERROR_MESSAGE,'',msg)


# |------------------------------------|
# | EVENTS TRIGGERED BY THE IRC SERVER |
# |------------------------------------|

def received_error(gui,client,msg):
	writeErrorMsgActiveWindow(gui,client,msg)

def server_options(gui,client,options):

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			w.server_options(options)

def received_network_and_hostname(gui,client,network,hostname):

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			w.setWindowTitle(" "+hostname+" ("+network+")")

	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

def connection(gui,client):
	CONNECTIONS.append(client)

	if client.hostname:
		name = client.hostname
	else:
		name = client.server+":"+str(client.port)

	server_console_window = ServerWindow(name,gui.MDI,client,gui)
	SERVER_WINDOWS.append(server_console_window)

	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			message = "Connected to "+client.server+":"+str(client.port)
			w.writeLog(SYSTEM_MESSAGE,'',message)

def disconnection(gui,client):
	global CONNECTIONS
	global CHANNEL_WINDOWS
	global PRIVATE_WINDOWS
	global SERVER_WINDOWS

	gui.client_disconnected(client)

	clean = []
	for c in CONNECTIONS:
		if c.id==client.id: continue
		clean.append(c)
	CONNECTIONS = clean

	clean = []
	for c in CHANNEL_WINDOWS:
		if c.client.id==client.id:
			c.close()
			continue
		clean.append(c)
	CHANNEL_WINDOWS = clean

	clean = []
	for c in PRIVATE_WINDOWS:
		if c.client.id==client.id:
			c.close()
			continue
		clean.append(c)
	PRIVATE_WINDOWS = clean

	clean = []
	for c in SERVER_WINDOWS:
		if c.client.id==client.id:
			c.do_actual_close = True
			c.close()
			continue
		clean.append(c)
	SERVER_WINDOWS = clean

	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

	gui.updateActiveChild(gui.MDI.activeSubWindow())


def registered(gui,client):

	gui.client_connected(client)
	
	gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			message = "Registered with "+client.server+":"+str(client.port)
			w.writeLog(SYSTEM_MESSAGE,'',message)

	if gui.connect_expand_node:
		iterator = QTreeWidgetItemIterator(gui.connectionTree)
		while True:
			item = iterator.value()
			if item is not None:
				if hasattr(item,"erk_server"):
					if item.erk_server:
						if hasattr(item,"erk_client"):
							if item.erk_client.id==client.id:
								item.setExpanded(True)
				iterator += 1
			else:
				break

def motd(gui,client,motd):

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			m = "\n".join(motd)
			w.writeLog(MOTD_MESSAGE,'',m)
			# for line in motd:
			# 	w.writeLog(MOTD_MESSAGE,'',line)

def private_message(gui,client,user,message):

	userinfo = user.split('!')
	if len(userinfo)==2:
		nickname = userinfo[0]
	else:
		nickname = user

	private_chat_window = None

	# See if a private message window already exists
	window_is_created = False
	for w in PRIVATE_WINDOWS:
		if w.client.id==client.id:
			if w.name==nickname:
				window_is_created = True
				private_chat_window = w
				break

	if not window_is_created:
		if gui.auto_create_private:
			private_chat_window = PrivateWindow(nickname,gui.MDI,client,gui)
			PRIVATE_WINDOWS.append(private_chat_window)
			gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)
		else:
			for w in SERVER_WINDOWS:
				if w.client.id==client.id:
					w.writeLog(CHAT_MESSAGE,nickname,message)
			return


	private_chat_window.writeLog(CHAT_MESSAGE,nickname,message)

def public_message(gui,client,channel,user,message):

	userinfo = user.split('!')
	if len(userinfo)==2:
		nickname = userinfo[0]
	else:
		nickname = user
	
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name==channel:
				window.writeLog(CHAT_MESSAGE,nickname,message)

def notice_message(gui,client,channel,user,message):

	userinfo = user.split('!')
	if len(userinfo)==2:
		nickname = userinfo[0]
	else:
		nickname = user
	
	if channel=='*' or user==client.hostname:
		if client.hostname:
			sender = client.hostname
		else:
			sender = client.server + ":" + str(client.port)

		for w in SERVER_WINDOWS:
			if w.client.id==client.id:
				w.writeLog(NOTICE_MESSAGE,sender,message)
		return

	if channel==client.nickname:
		for w in SERVER_WINDOWS:
			if w.client.id==client.id:
				w.writeLog(NOTICE_MESSAGE,nickname,message)
		return

	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name==channel:
				window.writeLog(NOTICE_MESSAGE,nickname,message)
				return

	for w in SERVER_WINDOWS:
		if w.client.id==client.id:
			w.writeLog(NOTICE_MESSAGE,nickname,message)

def action_message(gui,client,channel,user,message):
	
	userinfo = user.split('!')
	if len(userinfo)==2:
		nickname = userinfo[0]
	else:
		nickname = user
	
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name==channel:
				window.writeLog(ACTION_MESSAGE,nickname,nickname+" "+message)
				return

	private_chat_window = None

	# See if a private message window already exists
	window_is_created = False
	for w in PRIVATE_WINDOWS:
		if w.client.id==client.id:
			if w.name==nickname:
				window_is_created = True
				private_chat_window = w
				break

	if not window_is_created:
		private_chat_window = PrivateWindow(nickname,gui.MDI,client,gui)
		PRIVATE_WINDOWS.append(private_chat_window)
		gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

	private_chat_window.writeLog(ACTION_MESSAGE,nickname,nickname+" "+message)

def mode(gui,client,channel,user,mset,modes,args):
	
	if len(modes)<1: return

	args = list(args)
	cleaned = []
	for a in args:
		if a == None: continue
		cleaned.append(a)
	args = cleaned

	p = user.split('!')
	if len(p)==2:
		user = p[0]

	if channel==client.nickname:
		for w in SERVER_WINDOWS:
			if w.client.id==client.id:
				if mset:
					message = "Mode +"+modes+" set on "+channel
				else:
					message = "Mode -"+modes+" set on "+channel
				w.writeLog(SYSTEM_MESSAGE,'',message)
				return

	reportadd = []
	reportremove = []
	get_names = False

	for m in modes:

		if m=="k":
			if len(args)>0:
				n = args.pop(0)
			else:
				n = None
			if mset:
				if n:
					msg = f"{user} set {channel}'s channel key to \"{n}\""
					setChannelKey(gui,client,channel,n)
					setChannelModes(client,channel,"k")
				else:
					msg = ''
			else:
				msg = f"{user} unset {channel}'s channel key"
				setChannelKey(gui,client,channel,'')
				unsetChannelModes(client,channel,"k")
			if len(msg)>0:
				writeSytemMsgChannel(client,channel,msg)
			continue

		if m=="o":
			if len(args)>0:
				n = args.pop(0)
			else:
				n = None
			if mset:
				if n:
					msg = f"{user} granted {channel} operator status to {n}"
				else:
					msg = ''
			else:
				if n:
					msg = f"{user} took {channel} operator status from {n}"
				else:
					msg = ''
			if len(msg)>0:
				writeSytemMsgChannel(client,channel,msg)
			get_names = True
			continue

		if m=="v":
			if len(args)>0:
				n = args.pop(0)
			else:
				n = None
			if mset:
				if n:
					msg = f"{user} granted {channel} voiced status to {n}"
				else:
					msg = ''
			else:
				if n:
					msg = f"{user} took {channel} voiced status from {n}"
				else:
					msg = ''
			if len(msg)>0:
				writeSytemMsgChannel(client,channel,msg)
			get_names = True
			continue

		if m=="b":
			if mset:
				for u in args:
					msg = f"{user} banned {u} from {channel}"
					writeSytemMsgChannel(client,channel,msg)
			else:
				for u in args:
					msg = f"{user} unbanned {u} from {channel}"
					writeSytemMsgChannel(client,channel,msg)
			continue

		if m=="c":
			if mset:
				setChannelModes(client,channel,"c")
				reportadd.append("c")
			else:
				unsetChannelModes(client,channel,"c")
				reportremove.append("c")
			continue

		if m=="C":
			if mset:
				setChannelModes(client,channel,"C")
				reportadd.append("C")
			else:
				unsetChannelModes(client,channel,"C")
				reportremove.append("C")
			continue

		if m=="m":
			if mset:
				setChannelModes(client,channel,"m")
				reportadd.append("m")
			else:
				unsetChannelModes(client,channel,"m")
				reportremove.append("m")
			continue

		if m=="n":
			if mset:
				setChannelModes(client,channel,"n")
				reportadd.append("n")
			else:
				unsetChannelModes(client,channel,"n")
				reportremove.append("n")
			continue

		if m=="p":
			if mset:
				setChannelModes(client,channel,"p")
				reportadd.append("p")
			else:
				unsetChannelModes(client,channel,"p")
				reportremove.append("p")
			continue

		if m=="s":
			if mset:
				setChannelModes(client,channel,"s")
				reportadd.append("s")
			else:
				unsetChannelModes(client,channel,"s")
				reportremove.append("s")
			continue

		if m=="t":
			if mset:
				setChannelModes(client,channel,"t")
				reportadd.append("t")
			else:
				unsetChannelModes(client,channel,"t")
				reportremove.append("t")
			continue

		if mset:
			reportadd.append(m)
		else:
			reportremove.append(m)

	if len(reportadd)>0 or len(reportremove)>0:
		if mset:
			msg = f"{user} set +{''.join(reportadd)} in {channel}"
			writeSytemMsgChannel(client,channel,msg)
		else:
			msg = f"{user} set -{''.join(reportremove)} in {channel}"
			writeSytemMsgChannel(client,channel,msg)

	if get_names: client.sendLine(f"NAMES {channel}")


def join(gui,client,user,channel):

	userinfo = user.split('!')
	if len(userinfo)==2:
		nickname = userinfo[0]
	else:
		nickname = user
	
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name == channel:
				client.sendLine("NAMES "+window.name)
				message = nickname+" has joined "+channel
				window.writeLog(SYSTEM_MESSAGE,'',message)

	for window in SERVER_WINDOWS:
		if window.client.id==client.id:
			message = nickname+" has joined "+channel
			window.writeLog(SYSTEM_MESSAGE,'',message)

def part(gui,client,user,channel):
	
	userinfo = user.split('!')
	if len(userinfo)==2:
		nickname = userinfo[0]
	else:
		nickname = user
	
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name == channel:
				client.sendLine("NAMES "+window.name)
				message = nickname+" has left "+channel
				window.writeLog(SYSTEM_MESSAGE,'',message)
				window.part(nickname)

	for window in SERVER_WINDOWS:
		if window.client.id==client.id:
			message = nickname+" has left "+channel
			window.writeLog(SYSTEM_MESSAGE,'',message)

def nick(gui,client,oldnick,newnick):
	
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if oldnick in window.nicks:
				client.sendLine("NAMES "+window.name)
				message = oldnick+" is now known as "+newnick
				window.writeLog(SYSTEM_MESSAGE,'',message)

	for window in PRIVATE_WINDOWS:
		if window.client.id==client.id:
			if window.name==oldnick:
				window.name = newnick
				window.setWindowTitle(" "+newnick)
				message = oldnick+" is now known as "+newnick
				window.writeLog(SYSTEM_MESSAGE,'',message)
				gui.populateConnectionDisplay(CONNECTIONS,CHANNEL_WINDOWS,PRIVATE_WINDOWS,SERVER_WINDOWS)

	for window in SERVER_WINDOWS:
		if window.client.id==client.id:
			message = oldnick+" is now known as "+newnick
			window.writeLog(SYSTEM_MESSAGE,'',message)


def topic(gui,client,user,channel,topic):

	if user=='':
		nickname = client.hostname
	else:
		userinfo = user.split('!')
		if len(userinfo)==2:
			nickname = userinfo[0]
		else:
			nickname = user
	
	for window in CHANNEL_WINDOWS:
		if window.client.id==client.id:
			if window.name==channel:
				window.writeTopic(topic)
				if topic!='':
					message = nickname+" set the channel topic to \""+topic+"\""
					window.writeLog(SYSTEM_MESSAGE,'',message)
				else:
					message = nickname+" set the channel topic to nothing"
					window.writeLog(SYSTEM_MESSAGE,'',message)

def quit(gui,client,user,message):
	pass

def userlist(gui,client,channel,users):
	
	for win in CHANNEL_WINDOWS:
		# Make sure the event and the window are using
		# the same IRC connection
		if client.id==win.client.id:
			if win.name==channel:
				win.writeUserlist(users)