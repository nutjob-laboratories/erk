
from datetime import datetime

from erk.resources import *
from erk.files import *
from erk.widgets import *
from erk.objects import *
from erk.strings import *
from erk.common import *
import erk.config
import erk.format

CHANNELS = []
CONNECTIONS = []
CONSOLES = []
PRIVATES = []

UNSEEN = []

def starterWrite(client,msg):

	ts = datetime.timestamp(datetime.now())
	pretty_timestamp = datetime.fromtimestamp(ts).strftime('%H:%M')

	STARTER_MESSAGE = f'''
	<table style="width: 100%" border="0">
      <tbody>
        <tr>
          <td style="text-align: center; vertical-align: middle;">&nbsp;<b>{client.server+":"+str(client.port)} [{pretty_timestamp}]&nbsp;</b>
          </td>
          <td style="text-align: left; vertical-align: middle;">{msg}
          </td>
        </tr>
      </tbody>
    </table>
	'''

	client.gui.starter.append(STARTER_MESSAGE)
	client.gui.starter.moveCursor(QTextCursor.End)

def quit_all():
	for c in CONNECTIONS:
		c.quit()

def clear_unseen(window):
	global UNSEEN
	clean = []
	for w in UNSEEN:
		if w.client.id==window.client.id:
			if w.name==window.name:
				continue
		clean.append(w)
	UNSEEN = clean

def window_has_unseen(window):
	for w in UNSEEN:
		if w.client.id==window.client.id:
			if w.name==window.name: return True
	return False

def build_connection_display(gui,new_server=None):

	# Make a list of expanded server nodes, and make sure they
	# are still expanded when we rewrite the display
	expanded = []

	if new_server: expanded.append(new_server.id)

	iterator = QTreeWidgetItemIterator(gui.connection_display)
	while True:
		item = iterator.value()
		if item is not None:
			if hasattr(item,"isExpanded"):
				if item.isExpanded():
					if hasattr(item,"erk_client"):
						expanded.append(item.erk_client.id)
			iterator += 1
		else:
			break

	clearQTreeWidget(gui.connection_display)

	servers = []

	for c in CONNECTIONS:
		channels = []
		for window in CHANNELS:
			if window.widget.client.id == c.id:
				channels.append(window.widget)

		for window in PRIVATES:
			if window.widget.client.id == c.id:
				channels.append(window.widget)

		if c.hostname:
			servers.append( [c.hostname,c,channels] )
		else:
			servers.append( ["Connecting...",c,channels] )

	root = gui.connection_display.invisibleRootItem()

	# BEGIN STARTER DISPLAY

	if len(CONSOLES)>0 or len(CHANNELS)>0 or len(PRIVATES)>0:

		gui.connection_dock.show()

		parent = QTreeWidgetItem(root)
		parent.setText(0,MASTER_LOG_NAME)
		parent.setIcon(0,QIcon(LOG_ICON))
		parent.erk_client = None
		parent.erk_channel = False
		parent.erk_widget = gui.starter
		parent.erk_name = MASTER_LOG_NAME
		parent.erk_server = False
		parent.erk_console = False

		if gui.current_page:
			if hasattr(gui.current_page,"name"):
				if gui.current_page.name==MASTER_LOG_NAME:
					f = parent.font(0)
					f.setItalic(False)
					f.setBold(True)
					parent.setFont(0,f)

	else:
		gui.connection_dock.hide()

	# END STARTER DISPLAY

	for s in servers:

		parent = QTreeWidgetItem(root)
		parent.setText(0,s[0])
		parent.setIcon(0,QIcon(SERVER_ICON))
		parent.erk_client = s[1]
		parent.erk_channel = False
		parent.erk_widget = None
		parent.erk_name = None
		parent.erk_server = True
		parent.erk_console = False

		if erk.config.DISPLAY_CONNECTION_UPTIME:
			child = QTreeWidgetItem(parent)
			if s[1].id in gui.uptimers:
				child.setText(0,prettyUptime(gui.uptimers[s[1].id]))
			else:
				child.setText(0,"00:00:00")
			child.setIcon(0,QIcon(UPTIME_ICON))
			child.erk_uptime = True
			child.erk_client = s[1]
			child.erk_console = False

		if s[1].id in expanded:
			parent.setExpanded(True)

		# Add console "window"
		for c in CONSOLES:
			if c.widget.client.id == s[1].id:
				if s[0]!="Connecting...":

					parent.erk_widget = c.widget

					if c.widget.client.network:
						parent.erk_name = c.widget.client.network
						parent.setText(0,c.widget.client.network)
						parent.setIcon(0,QIcon(NETWORK_ICON))
					else:
						parent.erk_name = s[0]

					parent.erk_console = True

					if window_has_unseen(c.widget):
						f = parent.font(0)
						f.setItalic(True)
						parent.setFont(0,f)
					
					if gui.current_page:
						if hasattr(gui.current_page,"name"):
							if gui.current_page.name==SERVER_CONSOLE_NAME:
								if gui.current_page.client.id==s[1].id:
									f = parent.font(0)
									f.setItalic(False)
									f.setBold(True)
									parent.setFont(0,f)

		for channel in s[2]:
			child = QTreeWidgetItem(parent)
			child.setText(0,channel.name)
			if channel.type==erk.config.CHANNEL_WINDOW:
				child.erk_channel = True
				child.setIcon(0,QIcon(CHANNEL_ICON))
			elif channel.type==erk.config.PRIVATE_WINDOW:
				child.setIcon(0,QIcon(NICK_ICON))
				child.erk_channel = False
			child.erk_client = s[1]
			child.erk_widget = channel
			child.erk_name = channel.name
			child.erk_console = False

			if window_has_unseen(channel):
				f = child.font(0)
				f.setItalic(True)
				child.setFont(0,f)

			if gui.current_page:
				if hasattr(gui.current_page,"name"):
					if gui.current_page.name==channel.name:
						if gui.current_page.client.id==s[1].id:
							f = child.font(0)
							f.setBold(True)
							child.setFont(0,f)

							continue

def rerender_all():
	for c in CHANNELS:
		c.widget.rerender()
	for c in PRIVATES:
		c.widget.rerender()
	for c in CONSOLES:
		c.widget.rerender()

def toggle_nickspell():
	for c in CHANNELS:
		c.widget.input.addNicks(c.widget.nicks)
	for c in PRIVATES:
		c.widget.input.addNicks(c.widget.nicks)
	for c in CONSOLES:
		c.widget.input.addNicks(c.widget.nicks)

def newspell_all(lang):
	for c in CHANNELS:
		c.widget.changeSpellcheckLanguage(lang)
	for c in PRIVATES:
		c.widget.changeSpellcheckLanguage(lang)
	for c in CONSOLES:
		c.widget.changeSpellcheckLanguage(lang)

def resetinput_all():
	for c in CHANNELS:
		c.widget.reset_input()
	for c in PRIVATES:
		c.widget.reset_input()
	for c in CONSOLES:
		c.widget.reset_input()

def set_fonts_all(font):
	for c in CHANNELS:
		c.widget.chat.setFont(font)
		c.widget.topic.setFont(font)
		c.widget.userlist.setFont(font)
		c.widget.input.setFont(font)
		c.widget.name_display.setFont(font)
		c.widget.nick_display.setFont(font)
	for c in PRIVATES:
		c.widget.chat.setFont(font)
		c.widget.input.setFont(font)
		c.widget.name_display.setFont(font)
	for c in CONSOLES:
		c.widget.chat.setFont(font)
		c.widget.input.setFont(font)
		c.widget.name_display.setFont(font)

def close_channel_window(client,name,msg=None):
	global CHANNELS

	starterWrite(client,"Left "+name)

	clean = []
	windex = 0
	for c in CHANNELS:
		if c.widget.client.id == client.id:
			if c.widget.name==name:
				windex = client.gui.stack.indexOf(c.widget)
				c.widget.client.part(name,msg)
				c.widget.close()
				continue
		clean.append(c)
	CHANNELS = clean

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(SYSTEM_MESSAGE,'',"You left "+name) )

	if len(CHANNELS)>0:
		w = None
		for c in CHANNELS:
			if c.widget.client.id==client.id:
				w = c.widget
		if w:
			client.gui.stack.setCurrentWidget(w)
			build_connection_display(client.gui)
			return

	if len(PRIVATES)>0:
		w = None
		for c in PRIVATES:
			if c.widget.client.id==client.id:
				w = c.widget
		if w:
			client.gui.stack.setCurrentWidget(w)
			build_connection_display(client.gui)
			return

	if len(CONSOLES)>0:
		w = None
		for c in CONSOLES:
			if c.widget.client.id==client.id:
				w = c.widget
		if w:
			client.gui.stack.setCurrentWidget(w)
			build_connection_display(client.gui)
			return

	client.gui.stack.setCurrentWidget(client.gui.starter)
	build_connection_display(client.gui)

def close_private_window(client,name):
	global PRIVATES

	starterWrite(client,"Closed private chat with "+name)

	clean = []
	windex = 0
	for c in PRIVATES:
		if c.widget.client.id == client.id:
			if c.widget.name==name:
				windex = client.gui.stack.indexOf(c.widget)
				c.widget.close()
				continue
		clean.append(c)
	PRIVATES = clean

	if len(CHANNELS)>0:
		w = None
		for c in CHANNELS:
			if c.widget.client.id==client.id:
				w = c.widget
		if w:
			client.gui.stack.setCurrentWidget(w)
			build_connection_display(client.gui)
			return

	if len(PRIVATES)>0:
		w = None
		for c in PRIVATES:
			if c.widget.client.id==client.id:
				w = c.widget
		if w:
			client.gui.stack.setCurrentWidget(w)
			build_connection_display(client.gui)
			return

	if len(CONSOLES)>0:
		w = None
		for c in CONSOLES:
			if c.widget.client.id==client.id:
				w = c.widget
		if w:
			client.gui.stack.setCurrentWidget(w)
			build_connection_display(client.gui)
			return

	client.gui.stack.setCurrentWidget(client.gui.starter)
	build_connection_display(client.gui)

def full_nick_list(client):
	nicks = []
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			nicks = nicks + window.widget.nicks
	for window in PRIVATES:
		if window.widget.client.id==client.id:
			if not window.widget.name in nicks:
				nicks.append(window.widget.name)
	return nicks


def fetch_channel_window(client,channel):
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			if window.widget.name==channel:
				return window.widget
	return None

def fetch_private_window(client,channel):
	for window in PRIVATES:
		if window.widget.client.id==client.id:
			if window.widget.name==channel:
				return window.widget
	return None

def fetch_console_window(client):
	for window in CONSOLES:
		if window.widget.client.id==client.id:
			return window.widget
	return None

def fetch_channel_list(client):
	channels = []
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			channels.append(window.widget.name)
	return channels

def fetch_private_list(client):
	channels = []
	for window in PRIVATES:
		if window.widget.client.id==client.id:
			channels.append(window.widget.name)
	return channels

def name_to_channel(client,channel):
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			if window.widget.name==channel:
				return window.widget
	return None

def name_to_private(client,channel):
	for window in PRIVATES:
		if window.widget.client.id==client.id:
			if window.widget.name==channel:
				return window.widget
	return None

def open_private_window(client,target):

	window = fetch_private_window(client,target)
	if window:
		gui.stack.setCurrentWidget(window)
		return
	else:
		starterWrite(client,"Started private chat with "+target)

		newchan = Chat(
			target,
			client,
			erk.config.PRIVATE_WINDOW,
			client.gui.app,
			client.gui
			)

		index = client.gui.stack.addWidget(newchan)
		if erk.config.SWITCH_TO_NEW_WINDOWS:
			client.gui.stack.setCurrentWidget(newchan)

		#client.gui.setWindowTitle(target)

		PRIVATES.append( Window(index,newchan) )

		# Update connection display
		build_connection_display(client.gui)

def where_is_user(client,nick):
	channels = []
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			if nick in window.widget.nicks:
				channels.append(window.widget.name)
			
	return channels

def channel_has_hostmask(gui,client,channel,user):

	window = fetch_channel_window(client,channel)
	if window:
		if user in window.hostmasks: return True
		return False

	# Window not found, so return true
	return True

def line_output(gui,client,line):
	pass

def line_input(gui,client,line):
	pass

def received_error(gui,client,error):

	starterWrite(client,"Error: "+error)

	if gui.current_page:
		if hasattr(gui.current_page,"writeText"):
			gui.current_page.writeText( Message(ERROR_MESSAGE,'',error) )

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(ERROR_MESSAGE,'',error) )

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
		if mset:
			msg = Message(SYSTEM_MESSAGE,'',"Mode +"+modes+" set on "+channel)
			starterWrite(client,user+" set mode +"+modes)
		else:
			msg = Message(SYSTEM_MESSAGE,'',"Mode -"+modes+" set on "+channel)
			starterWrite(client,user+" set mode -"+modes)
		window = fetch_console_window(client)
		if window:
			window.writeText( msg )
		return

	reportadd = []
	reportremove = []
	window = fetch_channel_window(client,channel)
	if not window: return

	for m in modes:

		if m=="k":
			if len(args)>0:
				n = args.pop(0)
			else:
				n = None
			if mset:
				if n:
					window.setKey(n)
					if 'k' in window.modesoff:
						window.modesoff = window.modesoff.replace('k','')
					if not 'k' in window.modeson:
						window.modeson = window.modeson +'k'
					msg = Message(SYSTEM_MESSAGE,'',user+" set "+channel+"'s key to \""+n+"\"")
				else:
					msg = None
			else:
				window.setKey('')
				if 'k' in window.modeson:
					window.modeson = window.modeson.replace('k','')
				if not 'k' in window.modesoff:
					window.modesoff = window.modesoff +'k'
				msg = Message(SYSTEM_MESSAGE,'',user+" unset "+channel+"'s key")
			if msg:
				window.writeText( msg )

			# Update connection display
			build_connection_display(gui)

			continue

		if m=="o":
			if len(args)>0:
				n = args.pop(0)
			else:
				n = None
			if mset:
				if n:
					msg = Message(SYSTEM_MESSAGE,'',f"{user} granted {channel} operator status to {n}")
				else:
					msg = None
			else:
				if n:
					#msg = f"{user} took {channel} operator status from {n}"
					msg = Message(SYSTEM_MESSAGE,'',f"{user} took {channel} operator status from {n}")
				else:
					msg = None
			if msg:
				window.writeText( msg )
			continue

		if m=="v":
			if len(args)>0:
				n = args.pop(0)
			else:
				n = None
			if mset:
				if n:
					msg = Message(SYSTEM_MESSAGE,'',f"{user} granted {channel} voiced status to {n}")
				else:
					msg = None
			else:
				if n:
					#msg = f"{user} took {channel} operator status from {n}"
					msg = Message(SYSTEM_MESSAGE,'',f"{user} took {channel} voiced status from {n}")
				else:
					msg = None
			if msg:
				window.writeText( msg )
			continue

		if m=="c":
			if mset:
				if 'c' in window.modesoff:
					window.modesoff = window.modesoff.replace('c','')
				if not 'c' in window.modeson:
					window.modeson = window.modeson +'c'
				reportadd.append("c")
			else:
				if 'c' in window.modeson:
					window.modeson = window.modeson.replace('c','')
				if not 'c' in window.modesoff:
					window.modesoff = window.modesoff +'c'
				reportremove.append("c")
			continue

		if m=="C":
			if mset:
				if "C" in window.modesoff:
					window.modesoff = window.modesoff.replace("C",'')
				if not "C" in window.modeson:
					window.modeson = window.modeson +"C"
				reportadd.append("C")
			else:
				if "C" in window.modeson:
					window.modeson = window.modeson.replace("C",'')
				if not "C" in window.modesoff:
					window.modesoff = window.modesoff +"C"
				reportremove.append("C")
			continue

		if m=="m":
			if mset:
				if "m" in window.modesoff:
					window.modesoff = window.modesoff.replace("m",'')
				if not "m" in window.modeson:
					window.modeson = window.modeson +"m"
				reportadd.append("m")
			else:
				if "m" in window.modeson:
					window.modeson = window.modeson.replace("m",'')
				if not "m" in window.modesoff:
					window.modesoff = window.modesoff +"m"
				reportremove.append("m")
			continue

		if m=="n":
			if mset:
				if "n" in window.modesoff:
					window.modesoff = window.modesoff.replace("n",'')
				if not "n" in window.modeson:
					window.modeson = window.modeson +"n"
				reportadd.append("n")
			else:
				if "n" in window.modeson:
					window.modeson = window.modeson.replace("n",'')
				if not "n" in window.modesoff:
					window.modesoff = window.modesoff +"n"
				reportremove.append("n")
			continue

		if m=="p":
			if mset:
				if "p" in window.modesoff:
					window.modesoff = window.modesoff.replace("p",'')
				if not "p" in window.modeson:
					window.modeson = window.modeson +"p"
				reportadd.append("p")
			else:
				if "p" in window.modeson:
					window.modeson = window.modeson.replace("p",'')
				if not "p" in window.modesoff:
					window.modesoff = window.modesoff +"p"
				reportremove.append("p")
			continue

		if m=="s":
			if mset:
				if "s" in window.modesoff:
					window.modesoff = window.modesoff.replace("s",'')
				if not "s" in window.modeson:
					window.modeson = window.modeson +"s"
				reportadd.append("s")
			else:
				if "s" in window.modeson:
					window.modeson = window.modeson.replace("s",'')
				if not "s" in window.modesoff:
					window.modesoff = window.modesoff +"s"
				reportremove.append("s")
			continue

		if m=="t":
			if mset:
				if "t" in window.modesoff:
					window.modesoff = window.modesoff.replace("t",'')
				if not "t" in window.modeson:
					window.modeson = window.modeson +"t"
				reportadd.append("t")
			else:
				if "t" in window.modeson:
					window.modeson = window.modeson.replace("t",'')
				if not "t" in window.modesoff:
					window.modesoff = window.modesoff +"t"
				reportremove.append("t")
			continue

		if m=="i":
			if mset:
				if "i" in window.modesoff:
					window.modesoff = window.modesoff.replace("i",'')
				if not "i" in window.modeson:
					window.modeson = window.modeson +"i"
				reportadd.append("i")
			else:
				if "i" in window.modeson:
					window.modeson = window.modeson.replace("i",'')
				if not "i" in window.modesoff:
					window.modesoff = window.modesoff +"i"
				reportremove.append("i")
			continue

		if mset:
			reportadd.append(m)
		else:
			reportremove.append(m)

	if len(reportadd)>0 or len(reportremove)>0:
		if mset:

			for m in reportadd:
				if not m in window.modeson: window.modeson = window.modeson + m
				if m in window.modesoff: window.modesoff.replace(m,'')

			msg = Message(SYSTEM_MESSAGE,'',f"{user} set +{''.join(reportadd)} in {channel}")
			window.writeText( msg )
		else:

			for m in reportremove:
				if not m in window.modesoff: window.modesoff = window.modesoff + m
				if m in window.modeson: window.modeson.replace(m,'')

			msg = Message(SYSTEM_MESSAGE,'',f"{user} set -{''.join(reportremove)} in {channel}")
			window.writeText( msg )

	if erk.config.DISPLAY_CHANNEL_MODES:
		# Change the channel's name display
		if len(window.modeson)>0:
			window.name_display.setText("<b>"+window.name+"</b> <i>+"+window.modeson+"</i>")
		else:
			window.name_display.setText("<b>"+window.name+"</b>")

def toggle_channel_mode_display():
	for window in CHANNELS:
		if erk.config.DISPLAY_CHANNEL_MODES:
			if len(window.widget.modeson)>0:
				window.widget.name_display.setText("<b>"+window.widget.name+"</b> <i>+"+window.widget.modeson+"</i>")
			else:
				window.widget.name_display.setText("<b>"+window.widget.name+"</b>")
		else:
			window.widget.name_display.setText("<b>"+window.widget.name+"</b>")

def received_hostmask_for_channel_user(gui,client,nick,hostmask):
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			if nick in window.widget.nicks:
				window.widget.hostmasks[nick] = hostmask

def received_whois(gui,client,whoisdata):
	pass

def topic(gui,client,setter,channel,topic):
	p = setter.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = setter

	if nick=='': nick = "The server"

	window = fetch_channel_window(client,channel)
	if window:
		window.setTopic(topic)
		window.writeText( Message(SYSTEM_MESSAGE,'',nick+" set the topic to \""+topic+"\"") )

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(SYSTEM_MESSAGE,'',nick+" set the topic in "+channel+" to \""+topic+"\"") )

def userlist(gui,client,channel,userlist):

	# Update connection display
	build_connection_display(gui)

	window = fetch_channel_window(client,channel)
	if window: window.writeUserlist(userlist)

def quit(gui,client,nick,message):

	for channel in where_is_user(client,nick):
		window = fetch_channel_window(client,channel)
		if window:
			if len(message)>0:
				window.writeText( Message(SYSTEM_MESSAGE,'',nick+" quit IRC ("+message+")") )
			else:
				window.writeText( Message(SYSTEM_MESSAGE,'',nick+" quit IRC") )

def action_message(gui,client,target,user,message):
	global UNSEEN
	p = user.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = user

	window = fetch_channel_window(client,target)
	if window:
		window.writeText( Message(ACTION_MESSAGE,user,message) )
	else:
		window = fetch_private_window(client,nick)
		if window:
			window.writeText( Message(ACTION_MESSAGE,user,message) )
		else:
			if erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
				newchan = Chat(
					nick,
					client,
					erk.config.PRIVATE_WINDOW,
					gui.app,
					gui
					)

				index = gui.stack.addWidget(newchan)
				if erk.config.SWITCH_TO_NEW_WINDOWS:
					gui.stack.setCurrentWidget(newchan)

				#gui.setWindowTitle(nick)

				PRIVATES.append( Window(index,newchan) )

				newchan.writeText( Message(ACTION_MESSAGE,user,message) )

				window = newchan

				# Update connection display
				build_connection_display(gui)
			else:
				# Write the private messages to the console window
				window = fetch_console_window(client)
				if window:
					window.writeText( Message(ACTION_MESSAGE,user,message) )

					posted_to_current = False
					if gui.current_page:
						if gui.current_page.name==SERVER_CONSOLE_NAME:
							if gui.current_page.client.id==client.id:
								posted_to_current = True

					if not posted_to_current:
						UNSEEN.append(window)

						# Update connection display
						build_connection_display(gui)
			return

	posted_to_current = False
	if gui.current_page:
		if gui.current_page.name==nick:
			if gui.current_page.client.id==client.id:
				posted_to_current = True

	if not posted_to_current:
		if not window_has_unseen(window):
			UNSEEN.append(window)

		# Update connection display
		build_connection_display(gui)

def nick(gui,client,oldnick,newnick):

	channels = where_is_user(client,oldnick)
	msg = Message(SYSTEM_MESSAGE,'',oldnick+" is now known as "+newnick)
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			if window.widget.name in channels:
				window.widget.writeText(msg)
	
	for window in PRIVATES:
		if window.widget.client.id==client.id:
			if window.widget.name==oldnick:
				window.widget.name = newnick
				window.widget.name_display.setText("<b>"+newnick+"</b>")

	window = fetch_console_window(client)
	if window:
		window.writeText(msg)

	# Update connection display
	build_connection_display(gui)


def erk_changed_nick(gui,client,newnick):
	starterWrite(client,"Nickname changed to "+newnick)

	if gui.current_page:
		if hasattr(gui.current_page,"writeText"):
			gui.current_page.writeText( Message(SYSTEM_MESSAGE,'',"You are now known as "+newnick) )

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(SYSTEM_MESSAGE,'',"You are now known as "+newnick) )

	# Update channel window nick displays
	for window in CHANNELS:
		if window.widget.client.id==client.id:
			window.widget.nickDisplay(newnick)

def erk_joined_channel(gui,client,channel):
	global CHANNELS

	starterWrite(client,"Joined "+channel)
	
	newchan = Chat(
		channel,
		client,
		erk.config.CHANNEL_WINDOW,
		gui.app,
		gui
		)

	index = gui.stack.addWidget(newchan)
	if erk.config.SWITCH_TO_NEW_WINDOWS:
		gui.stack.setCurrentWidget(newchan)

	#gui.setWindowTitle(channel)

	CHANNELS.append( Window(index,newchan) )

	newchan.writeText( Message(SYSTEM_MESSAGE,'',"Joined "+channel) )

	# Set focus to the input widget
	newchan.input.setFocus()

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(SYSTEM_MESSAGE,'',"Joined "+channel) )

	# Update connection display
	build_connection_display(gui)

def uptime(gui,client,uptime):
	
	gui.uptimers[client.id] = uptime

	if erk.config.DISPLAY_CONNECTION_UPTIME:
		iterator = QTreeWidgetItemIterator(gui.connection_display)
		while True:
			item = iterator.value()
			if item is not None:
				if hasattr(item,"erk_uptime"):
					if item.erk_uptime:
						if item.erk_client.id==client.id:
							item.setText(0,prettyUptime(uptime))
				iterator += 1
			else:
				break

def part(gui,client,user,channel):
	p = user.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = user

	window = fetch_channel_window(client,channel)
	if window: window.writeText( Message(SYSTEM_MESSAGE,'',nick+" left the channel") )

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(SYSTEM_MESSAGE,'',nick+" left "+channel) )

def join(gui,client,user,channel):
	p = user.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = user

	window = fetch_channel_window(client,channel)
	if window: window.writeText( Message(SYSTEM_MESSAGE,'',nick+" joined the channel") )

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(SYSTEM_MESSAGE,'',nick+" joined "+channel) )

def motd(gui,client,motd):
	
	window = fetch_console_window(client)
	window.writeText( Message(SYSTEM_MESSAGE,'',"BEGIN MOTD") )
	if window:
		for line in motd:
			window.writeText( Message(SYSTEM_MESSAGE,'',line) )
	window.writeText( Message(SYSTEM_MESSAGE,'',"END MOTD") )

def notice_message(gui,client,target,user,message):

	if len(user.strip())==0:
		if client.hostname:
			user = client.hostname
		else:
			user = client.server+":"+str(client.port)

	window = fetch_channel_window(client,target)
	if window:
		window.writeText( Message(NOTICE_MESSAGE,user,message) )

		posted_to_current = False
		if gui.current_page:
			if gui.current_page.name==target:
				if gui.current_page.client.id==client.id:
					posted_to_current = True

		if not posted_to_current:
			if not window_has_unseen(window):
				UNSEEN.append(window)

			# Update connection display
			build_connection_display(gui)
		return

	p = user.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = user

	window = fetch_private_window(client,nick)
	if window:
		window.writeText( Message(NOTICE_MESSAGE,user,message) )

		posted_to_current = False
		if gui.current_page:
			if gui.current_page.name==nick:
				if gui.current_page.client.id==client.id:
					posted_to_current = True

		if not posted_to_current:
			if not window_has_unseen(window):
				UNSEEN.append(window)

			# Update connection display
			build_connection_display(gui)

		return

	window = fetch_console_window(client)
	if window:
		window.writeText( Message(NOTICE_MESSAGE,user,message) )

		posted_to_current = False
		if gui.current_page:
			if gui.current_page.name==SERVER_CONSOLE_NAME:
				if gui.current_page.client.id==client.id:
					posted_to_current = True

		if not posted_to_current:
			if not window_has_unseen(window):
				UNSEEN.append(window)

			# Update connection display
			build_connection_display(gui)

def private_message(gui,client,user,message):
	global UNSEEN
	p = user.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = user
	
	msg = Message(CHAT_MESSAGE,user,message)

	window = fetch_private_window(client,nick)
	if window:
		window.writeText(msg)
	else:
		if erk.config.OPEN_NEW_PRIVATE_MESSAGE_WINDOWS:
			newchan = Chat(
				nick,
				client,
				erk.config.PRIVATE_WINDOW,
				gui.app,
				gui
				)

			index = gui.stack.addWidget(newchan)
			if erk.config.SWITCH_TO_NEW_WINDOWS:
				gui.stack.setCurrentWidget(newchan)

			#gui.setWindowTitle(nick)

			PRIVATES.append( Window(index,newchan) )

			newchan.writeText(msg)

			window = newchan

			# Update connection display
			build_connection_display(gui)
		else:
			# Write the private messages to the console window
			window = fetch_console_window(client)
			if window:
				window.writeText(msg)

				posted_to_current = False
				if gui.current_page:
					if gui.current_page.name==SERVER_CONSOLE_NAME:
						if gui.current_page.client.id==client.id:
							posted_to_current = True

				if not posted_to_current:

					found = False
					for w in UNSEEN:
						if w.client.id==window.client.id:
							if w.name==window.name:
								found = True

					if not found: UNSEEN.append(window)

					# Update connection display
					build_connection_display(gui)
		return

	posted_to_current = False
	if gui.current_page:
		if gui.current_page.name==nick:
			if gui.current_page.client.id==client.id:
				posted_to_current = True

	if not posted_to_current:
		
		found = False
		for w in UNSEEN:
			if w.client.id==window.client.id:
				if w.name==window.name:
					found = True

		if not found: UNSEEN.append(window)

		# Update connection display
		build_connection_display(gui)

def public_message(gui,client,channel,user,message):
	#print(target+" "+user+": "+message)

	msg = Message(CHAT_MESSAGE,user,message)

	window = fetch_channel_window(client,channel)
	if window: window.writeText(msg)

	posted_to_current = False
	if gui.current_page:
		if gui.current_page.name==channel:
			if gui.current_page.client.id==client.id:
				posted_to_current = True

	if not posted_to_current:
		if window:
			global UNSEEN
			found = False
			for w in UNSEEN:
				if w.client.id==window.client.id:
					if w.name==window.name:
						found = True

			if not found: UNSEEN.append(window)

			# Update connection display
			build_connection_display(gui)

def registered(gui,client):

	starterWrite(client,"Registered with server")

	gui.registered(client)

	window = fetch_console_window(client)
	window.writeText( Message(SYSTEM_MESSAGE,'',"Registered with "+client.server+":"+str(client.port)+"!") )
	
	# Update connection display
	build_connection_display(gui)

def disconnect_from_server(client):

	starterWrite(client,"Sent QUIT command to server")

	client.gui.quitting.append(client.server+str(client.port))

	client.quit()

def disconnection(gui,client):

	starterWrite(client,"Disconnected from server")

	global CONNECTIONS
	clean = []
	for c in CONNECTIONS:
		if c.id == client.id: continue
		clean.append(c)
	CONNECTIONS = clean

	global PRIVATES
	clean = []
	for c in PRIVATES:
		if c.widget.client.id == client.id:
			c.widget.close()
			continue
		clean.append(c)
	PRIVATES = clean

	global CHANNELS
	clean = []
	for c in CHANNELS:
		if c.widget.client.id == client.id:
			c.widget.close()
			continue
		clean.append(c)
	CHANNELS = clean

	global CONSOLES
	clean = []
	for window in CONSOLES:
		if window.widget.client.id==client.id:
			window.widget.close()
			continue
		clean.append(window)
	CONSOLES = clean

	if len(CHANNELS)>0:
		w = None
		for c in CHANNELS:
			w = c.widget
		client.gui.stack.setCurrentWidget(w)
	elif len(PRIVATES)>0:
		w = None
		for c in PRIVATES:
			w = c.widget
		client.gui.stack.setCurrentWidget(w)
	elif len(CONSOLES)>0:
		w = None
		for c in CONSOLES:
			w = c.widget
		client.gui.stack.setCurrentWidget(w)
	else:
		client.gui.stack.setCurrentWidget(client.gui.starter)

	# Update connection display
	build_connection_display(gui)

def connection(gui,client):
	global CONNECTIONS
	CONNECTIONS.append(client)

	starterWrite(client,"Connected to server")

	window = fetch_console_window(client)
	window.writeText( Message(SYSTEM_MESSAGE,'',"Connected to "+client.server+":"+str(client.port)+"!") )

	# Update connection display
	build_connection_display(gui,client)

def server_options(gui,client,options):
	
	window = fetch_console_window(client)

	window.writeText( Message(SYSTEM_MESSAGE,'', ", ".join(options)    ) )

	if client.network:
		user_info = get_user()
		newhistory = []
		change = False
		for s in user_info["history"]:
			if s[0]==client.server:
				if s[1]==str(client.port):
					if s[2]==UNKNOWN_NETWORK:
						s[2] = client.network
						change = True
			newhistory.append(s)

		if change:
			user_info["history"] = newhistory
			save_user(user_info)

	# Update connection display
	build_connection_display(gui)

def banlist(gui,client,channel,banlist):
	pass

def startup(gui,client):
	global CONSOLES

	starterWrite(client,"Connecting to server...")

	newconsole = Chat(
		SERVER_CONSOLE_NAME,
		client,
		erk.config.SERVER_WINDOW,
		gui.app,
		gui
		)

	index = gui.stack.addWidget(newconsole)

	if erk.config.SWITCH_TO_NEW_WINDOWS:
		gui.stack.setCurrentWidget(newconsole)

	if client.hostname:
		gui.setWindowTitle(client.hostname)
	else:
		gui.setWindowTitle(client.server+":"+str(client.port))

	CONSOLES.append( Window(index,newconsole) )

	newconsole.writeText( Message(SYSTEM_MESSAGE,'',"Connecting to "+client.server+":"+str(client.port)+"...") )

	# Set focus to the input widget
	newconsole.input.setFocus()
	
	# Update connection display
	build_connection_display(gui)