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

# Adopted from https://www.guidodiepen.nl/2019/02/implementing-a-simple-plugin-framework-in-python/

import inspect
import os
import pkgutil
import random
import string

# For reloading plugins
import imp

import json

from erk.common import *

Shared = {}

class Plugin(object):
	"""Base class that each plugin must inherit from. within this class
	you must define the methods that all of your plugins must implement
	"""

	def __init__(self):
		self._irc = None
		self._gui = None

	def _setIrc(self,obj):
		self._irc = obj

	def _setGui(self,obj):
		self._gui = obj

	def client(self,serverid):
		if serverid in self._gui.connections:
			return self._gui.connections[serverid]
		return None

	def msg(self,target,text,serverid=None):

		try:
			x = self.silent
		except AttributeError:
			self.silent = False

		try:
			x = self.nowindows
		except AttributeError:
			self.nowindows = False

		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		clientnick = ''
		sid = None

		if serverid==None:
			if self._irc!=None:
				self._irc.msg(target,text)
				clientnick = self._irc.nickname
				sid = self._irc.id
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].msg(target,text)
				clientnick = self._gui.connections[serverid].nickname
				sid = self._gui.connections[serverid].id

		if clientnick=='': return
		if not sid: return

		if not self.silent:
			if target[0]!="#":
				if not self.nowindows: self._gui.createUserWindow(sid,target)
			d = chat_display(clientnick,text,self._gui.maxnicklen,True,self._gui.display['self'],self._gui.display['text'],self._gui.display['background'])
			self._gui.writeToChatWindow(sid,target,d)


	def notice(self,target,text,serverid=None):

		try:
			x = self.silent
		except AttributeError:
			self.silent = False

		try:
			x = self.nowindows
		except AttributeError:
			self.nowindows = False

		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		clientnick = ''
		sid = None

		if serverid==None:
			if self._irc!=None:
				self._irc.notice(target,text)
				sid = self._irc.id
				clientnick = self._irc.nickname
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].notice(target,text)
				sid = self._gui.connections[serverid].id
				clientnick = self._gui.connections[serverid].nickname

		if clientnick=='': return
		if not sid: return

		if not self.silent:
			if target[0]!="#":
				if not self.nowindows: self._gui.createUserWindow(sid,target)
			d = notice_display(clientnick,text,self._gui.maxnicklen,True,self._gui.display['self'],self._gui.display['text'],self._gui.display['background'])
			self._gui.writeToChatWindow(sid,target,d)

	def action(self,target,text,serverid=None):

		try:
			x = self.silent
		except AttributeError:
			self.silent = False

		try:
			x = self.nowindows
		except AttributeError:
			self.nowindows = False

		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		clientnick = ''
		sid = None

		if serverid==None:
			if self._irc!=None:
				self._irc.describe(target,text)
				sid = self._irc.id
				clientnick = self._irc.nickname
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].describe(target,text)
				sid = self._gui.connections[serverid].id
				clientnick = self._gui.connections[serverid].nickname

		if clientnick=='': return
		if not sid: return

		if not self.silent:
			if target[0]!="#":
				if not self.nowindows: self._gui.createUserWindow(sid,target)
			d = action_display(clientnick,text,True,self._gui.display['action'],self._gui.display['background'])
			self._gui.writeToChatWindow(sid,target,d)

	def join(self,channel,key=None,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		if serverid==None:
			if self._irc!=None:
				self._irc.join(channel,key)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].join(channel,key)

	def part(self,channel,msg=None,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		if serverid==None:
			if self._irc!=None:
				self._irc.part(channel,msg)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].part(channel,msg)

	def send(self,msg,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		if serverid==None:
			if self._irc!=None:
				self._irc.sendLine(msg)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].sendLine(msg)

	def kick(self,channel,user,reason=None,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		if serverid==None:
			if self._irc!=None:
				self._irc.kick(channel,user,reason)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].kick(channel,user,reason)

	def invite(self,user,channel,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		if serverid==None:
			if self._irc!=None:
				self._irc.invite(user,channel)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].invite(user,channel)

	def topic(self,channel,topic,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		if serverid==None:
			if self._irc!=None:
				self._irc.topic(channel,topic)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].topic(channel,topic)

	def mode(self,target,tset,modes,limit=None,user=None,mask=None,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return

		if serverid==None:
			if self._irc!=None:
				self._irc.mode(target,tset,modes,limit,user,mask)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].mode(target,tset,modes,limit,user,mask)


	def nick(self,newnick,serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return
		
		#if self._irc!= None: self._irc.setNick(newNick)

		if serverid==None:
			if self._irc!=None:
				self._irc.setNick(newNick)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].setNick(newNick)

	def quit(self,message='',serverid=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return
		
		#if self._irc!= None: self._irc.quit(message)

		if serverid==None:
			if self._irc!=None:
				self._irc.quit(message)
		else:
			if serverid in self._gui.connections:
				self._gui.connections[serverid].quit(message)

	def getNickname(self,serverid=None):
		#if self._irc!=None: return self._irc.nickname
		#return None

		if serverid==None:
			if self._irc!=None: return self._irc.nickname
			return None
		else:
			if serverid in self._gui.connections:
				return self._gui.connections[serverid].nickname
			return None

	def getHostname(self,serverid=None):
		#if self._irc!=None: return self._irc.hostname
		#return None

		if serverid==None:
			if self._irc!=None: return self._irc.hostname
			return None
		else:
			if serverid in self._gui.connections:
				return self._gui.connections[serverid].hostname
			return None

	def getServer(self,serverid=None):
		# if self._irc!=None: return self._irc.host
		# return None

		if serverid==None:
			if self._irc!=None: return self._irc.host
			return None
		else:
			if serverid in self._gui.connections:
				return self._gui.connections[serverid].host
			return None

	def getPort(self,serverid=None):
		#if self._irc!=None: return self._irc.port
		#return None

		if serverid==None:
			if self._irc!=None: return self._irc.port
			return None
		else:
			if serverid in self._gui.connections:
				return self._gui.connections[serverid].port
			return None

	def getConnections(self):
		c = []
		for cc in self._gui.connections:
			c.append(cc)
		return c

	def getUsers(self,channel,serverid=None):

		if serverid==None:
			if self._irc==None: return []
			serverid = self._irc.id
			if serverid in self._gui.connections:
				for w in self._gui.windows[serverid]:
					if w.window.is_channel:
						if w.window.name==channel:
							return w.window.rawusers
				return []
			else:
				return []
		else:
			if serverid in self._gui.connections:
				for w in self._gui.windows[serverid]:
					if w.window.is_channel:
						if w.window.name==channel:
							return w.window.rawusers
				return []
			else:
				return []

	# GUI methods

	def getWindows(self,serverid=None):
		if serverid==None:
			master = {}
			for w in self._gui.connections:
				windows = []
				for x in self._gui.windows[w]:
					windows.append(x.window.name)
				master[w] = windows
			return master
		else:
			master = {}
			for w in self._gui.connections:
				if self._gui.connections.id == serverid:
					windows = []
					for x in self._gui.windows[w]:
						windows.append(x.window.name)
					master[w] = windows
			return master

	def serverIDtoHost(self,serverid):
		if serverid in self._gui.connections:
			s =  self._gui.connections[serverid].host + ":" + str(self._gui.connections[serverid].port)
			return s
		return None


	def suppress(self,text):
		self._gui.addSuppress(text)

	def unsuppress(self,text):
		self._gui.removeSuppress(text)

	def print(self,text,window=None):

		try:
			x = self.silent
		except AttributeError:
			self.silent = False

		if self.silent: return

		if not window:
			self._gui.printToActiveWindow(text)
			return
		if window.lower() == "all":
			self._gui.writeToAllExisting(text)
			return
		if window.lower() == "log":
			self._gui.writeToLog(text)
			return

	def away(self,message=None):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return
		
		if self._irc!= None:
			self._irc.away(message)
			self._gui.setToAway(self._irc.id,message)

	def back(self):
		try:
			x = self.noirc
		except AttributeError:
			self.noirc = False

		if self.noirc: return
		
		if self._irc!= None:
			self._irc.back()
			self._gui.setToBack(self._irc.id)

	def color(self,text,fore,back=None):
		return plugin_color(text,fore,back)



def validatePlugin(p):

	errors = []

	# Check for .name
	try:
		x = p().name
	except AttributeError:
		errors.append("missing .name attribute")

	# Check for .version
	try:
		x = p().version
	except AttributeError:
		errors.append("missing .version attribute")

	# Check for .description
	try:
		x = p().description
	except AttributeError:
		errors.append("missing .description attribute")

	hastag = True
	# Check for ._tag
	try:
		x = p()._tag
	except AttributeError:
		hastag = False

	if hastag:
		errors.append("._tag can't be used as an attribute name")

	# Return any errors
	return errors

def generateTag(tlength=32):
	letters = string.ascii_letters + string.digits
	return ''.join(random.choice(letters) for i in range(tlength))

class PluginCollection(object):

	def __init__(self, plugin_package):
		self.plugin_package = plugin_package
		self.reload_plugins()


	def reload_plugins(self,do_reload=False):
		self.plugins = []
		self.seen_paths = []
		self.errors = []
		self.walk_package(self.plugin_package,do_reload)

	def walk_package(self,package,do_reload=False):
		imported_package = __import__(package, fromlist=['blah'])

		for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
			if not ispkg:
				plugin_module = __import__(pluginname, fromlist=['blah'])

				# Reload the plugin if it's already been loaded
				if do_reload:
					plugin_module = imp.reload(plugin_module)

				clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
				for (_, c) in clsmembers:
					if issubclass(c, Plugin) & (c is not Plugin):
						e = validatePlugin(c)
						if len(e)==0:

							plugin = c()

							pm = c.__module__.split(".")
							pm.pop(0)
							plugin.__file__ = inspect.getfile(c).replace(".pyc",".py")
							plugin._package = ".".join(pm)
							plugin._class = f"{c.__name__}"
							plugin.host = ""
							plugin.port = 0
							plugin._tag = generateTag()

							self.plugins.append(plugin)
						else:
							ee = [ inspect.getfile(c).replace(".pyc",".py"), f"{c.__module__}.{c.__name__}" ]
							for er in e:
								ee.append(er)
							self.errors.append(ee)

		all_current_paths = []
		if isinstance(imported_package.__path__, str):
			all_current_paths.append(imported_package.__path__)
		else:
			all_current_paths.extend([x for x in imported_package.__path__])

		for pkg_path in all_current_paths:
			if pkg_path not in self.seen_paths:
				self.seen_paths.append(pkg_path)

				child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

				for child_pkg in child_pkgs:
					self.walk_package(package + '.' + child_pkg)
