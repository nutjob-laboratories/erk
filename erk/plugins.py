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

# Adapted from https://www.guidodiepen.nl/2019/02/implementing-a-simple-plugin-framework-in-python/

import os,random,string,inspect

from pike.manager import PikeManager

from .strings import *
from . import events
from . import config
from .files import *
from .objects import *

from .userinput import(
	handle_input,
	VARIABLE_TABLE,
	execute_script_line,
	execute_script_end,
	execute_script_error,
	execute_script_msgbox,
	execute_script_unalias,
	SCRIPT_THREADS,
)
from .irc import ScriptThreadWindow

from .dialogs.plugin_input import Dialog as GetInput

PLUGINS = []

class Plugin():

	irc = None
	__class_icon = None
	__class_file = None
	__plugin_icon = None
	__plugin_directory = None

	def ask(self,text):
		if self.irc:
			if self.__class_icon:
				icon = self.__class_icon
			else:
				if self.__plugin_icon:
					icon = self.__plugin_icon
				else:
					icon = None

			x = GetInput(self.NAME,text,icon,self.irc.gui)
			res = x.get_input_information(self.NAME,text,icon,self.irc.gui)

			return res

	def switch(self,window):
		if self.irc:

			chans = events.fetch_channel_list(self.irc)
			privs = events.fetch_private_list(self.irc)

			w = None

			if window in chans:
				w = events.name_to_channel(self.irc,window)
			elif window in privs:
				w = events.name_to_private(self.irc,window)

			if w:
				self.irc.gui.stack.setCurrentWidget(w)
				return True
		return False

	def uptime(self):
		if self.irc: return events.get_uptime(self.irc)
		return None

	def server(self):
		server = None
		if self.irc:
			server = self.irc.server
		return server

	def port(self):
		port = None
		if self.irc:
			port = self.irc.port
		return port

	def windows(self):
		retval = []
		if self.irc:
			windows = events.fetch_window_list(self.irc)
			for w in windows:
				retval.append(w.name)
		return retval

	def current(self):
		if self.irc:
			w = events.fetch_current_window(self.irc.gui)
			if w:
				return w.name

	def print(self,*args):
		if self.irc:
			w = events.fetch_current_window(self.irc.gui)
			if w:
				for m in args:
					msg = Message(PLUGIN_MESSAGE,'',m)
					w.writeText(msg,True)
		else:
			print(args)

	def write(self,name,text):
		if self.irc:
			windows = events.fetch_window_list(self.irc)
			for w in windows:
				if w.name==name:
					msg = Message(PLUGIN_MESSAGE,'',text)
					w.writeText(msg,True)
					return True
		return False

	def console(self,text):
		if self.irc:
			window = events.fetch_console_window(self.irc)
			if window:
				msg = Message(PLUGIN_MESSAGE,'',text)
				window.writeText(msg,True)

	def exec(self,data):
		if self.irc:
			window = events.fetch_current_window(self.irc.gui)
			if window:
				handle_input(window,self.irc,data)
				return True
		return False

	def script(self,file,arguments=[]):
		if self.irc:

			window = events.fetch_current_window(self.irc.gui)
			scriptname = find_script_file(file,self.irc.gui.scriptsdir)

			if scriptname!=None and window!=None:

				base_scriptname = os.path.basename(scriptname)

				# Read in the script
				s = open(scriptname,"r")
				script = s.read()
				s.close()

				# Generate a random script ID
				scriptID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

				# Create a thread for the script and run it
				scriptThread = ScriptThreadWindow(window,self.irc,script,scriptID,base_scriptname,dict(VARIABLE_TABLE),arguments)
				scriptThread.execLine.connect(execute_script_line)
				scriptThread.scriptEnd.connect(execute_script_end)
				scriptThread.scriptErr.connect(execute_script_error)
				scriptThread.msgBox.connect(execute_script_msgbox)
				scriptThread.unalias.connect(execute_script_unalias)
				scriptThread.start()

				# Store the thread so it doesn't get garbage collected
				entry = [scriptID,scriptThread]
				SCRIPT_THREADS.append(entry)

def is_plugin_disabled(entry):
	for e in config.DISABLED_PLUGINS:
		if e==entry.id():
			return True
	return False

def disable_plugin(entry):
	for e in config.DISABLED_PLUGINS:
		if e==entry.id(): return
	config.DISABLED_PLUGINS.append(entry.id())

def enable_all_plugins():
	for p in PLUGINS:
		try:
			config.DISABLED_PLUGINS.remove(p.id())
		except:
			pass

def disable_all_plugins():
	for p in PLUGINS:
		disable_plugin(p)

def enable_plugin(entry):
	clean = []
	for e in config.DISABLED_PLUGINS:
		if e==entry.id(): continue
		clean.append(e)
	config.DISABLED_PLUGINS = clean

def inject_plugin(obj,p,client):
	obj.irc = client
	obj._Plugin__class_icon = p.class_icon
	obj._Plugin__class_file = p.filename
	obj._Plugin__plugin_icon = p.icon
	obj._Plugin__plugin_directory = p.directory

def cleanup_plugin(obj):
	obj.irc = None
	obj._Plugin__class_icon = None
	obj._Plugin__class_file = None
	obj._Plugin__plugin_icon = None
	obj._Plugin__plugin_directory = None


def public_message(client,channel,user,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"public"):
			obj.public(channel,user,message)
		cleanup_plugin(obj)

def private_message(client,user,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"private"):
			obj.private(user,message)
		cleanup_plugin(obj)

def action_message(client,target,user,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"action"):
			obj.action(target,user,message)
		cleanup_plugin(obj)

def line_in(client,data):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"line_in"):
			obj.line_in(data)
		cleanup_plugin(obj)

def line_out(client,data):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"line_out"):
			obj.line_out(data)
		cleanup_plugin(obj)

def mode_message(client,channel,user,mset,modes,args):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"mode"):
			obj.mode(channel,user,mset,modes,args)
		cleanup_plugin(obj)

def tick(client,uptime):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"tick"):
			obj.tick(uptime)
		cleanup_plugin(obj)

def input(client,window,text):
	result = False
	if window.type==config.SERVER_WINDOW:
		name = None
	else:
		name = window.name
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"input"):
			result = obj.input(name,text)
		cleanup_plugin(obj)
		if result: return result

def notice_message(client,target,user,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"notice"):
			obj.notice(target,user,message)
		cleanup_plugin(obj)

def motd(client,smotd):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"motd"):
			obj.motd(smotd)
		cleanup_plugin(obj)

def registered(client):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"registered"):
			obj.registered()
		cleanup_plugin(obj)

def join(client,channel,user):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"join"):
			obj.join(channel,user)
		cleanup_plugin(obj)

def part(client,channel,user):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"part"):
			obj.part(channel,user)
		cleanup_plugin(obj)

def joined(client,channel):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"joined"):
			obj.joined(channel)
		cleanup_plugin(obj)

def parted(client,channel):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"parted"):
			obj.parted(channel)
		cleanup_plugin(obj)

def kick(client,channel,kickee,kicker,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"kick"):
			obj.kick(channel,kickee,kicker,message)
		cleanup_plugin(obj)

def kicked(client,channel,kicker,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"kicked"):
			obj.kicked(channel,kicker,message)
		cleanup_plugin(obj)

def quit(client,nick,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"quit"):
			obj.quit(nick,message)
		cleanup_plugin(obj)

def ctcp(client,user,target,tag,message):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"ctcp"):
			obj.ctcp(user,target,tag,message)
		cleanup_plugin(obj)

def connect(client):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"connect"):
			obj.connect()
		cleanup_plugin(obj)

def topic(client,channel,user,topic):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"topic"):
			obj.connect(channel,user,topic)
		cleanup_plugin(obj)

def nick(client,oldnick,newnick):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"nick"):
			obj.nick(oldnick,newnick)
		cleanup_plugin(obj)

def invite(client,user,channel):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"invite"):
			obj.invite(user,channel)
		cleanup_plugin(obj)

def oper(client):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"oper"):
			obj.oper()
		cleanup_plugin(obj)

def op(client,user,channel):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"op"):
			obj.op(user,channel)
		cleanup_plugin(obj)

def deop(client,user,channel):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"deop"):
			obj.deop(user,channel)
		cleanup_plugin(obj)

def voice(client,user,channel):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"voice"):
			obj.voice(user,channel)
		cleanup_plugin(obj)

def devoice(client,user,channel):
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"devoice"):
			obj.devoice(user,channel)
		cleanup_plugin(obj)

EVENTS = [
	"public",
	"private",
	"action",
	"input",
	"mode",
	"tick",
	"notice",
	"motd",
	"registered",
	"join",
	"part",
	"joined",
	"parted",
	"kick",
	"kicked",
	"quit",
	"ctcp",
	"line_in",
	"line_out",
	"connect",
	"topic",
	"nick",
	"invite",
	"oper",
	"op",
	"deop",
	"voice",
	"devoice",
]

def check_for_bad_input(p):
	if not hasattr(p,"input"): return False

	s = inspect.getsourcelines(p.input)

	c = []
	for l in s[0]:
		l = l.strip()
		if len(l)>0:
			# Strip comments
			if l[0]=='#': continue
			# Strip print commands
			if l[:5]=="print": continue

			c.append(l)

	if len(c)>=2:
		# source is greater or equal to two lines
		if len(c)<3:
			# source is less than three lines
			if 'return True' in c:
				# probably malicious
				return True

	return False

class PluginEntry():
	def __init__(self,pclass,pobj):
		self.pclass = pclass
		self.obj = pobj
		self.errors = []

		self.filename = inspect.getfile(pclass)
		self.directory = os.path.dirname(self.filename)
		self.basename = os.path.basename(self.filename)

		fname, extension = os.path.splitext(self.filename)

		icon_name = fname+".png"
		if os.path.isfile(icon_name):
			self.icon = icon_name
		else:
			self.icon = None

		self.number_of_events = 0

		module = inspect.getmodule(self.obj)
		if hasattr(module,"_ERK_PLUGIN_"):
			self.package = module._ERK_PLUGIN_
		else:
			self.package = None

		self.events = 0
		self.event_list = []
		for e in EVENTS:
			if hasattr(self.obj,e):
				self.events = self.events + 1
				self.event_list.append(e)

		self.size = get_size(self.obj)

		classicon = os.path.join(os.path.dirname(self.filename), self.pclass.__name__+".png")
		if os.path.isfile(classicon):
			self.class_icon = classicon
		else:
			self.class_icon = None

		if PLUGIN_DIRECTORY in self.filename:
			# This checks to see if the plugin is just a directory
			# in the user's HOME plugin directory
			self.relative_path = os.path.relpath(self.directory,PLUGIN_DIRECTORY)
			self.is_home_plugin = True
		else:
			self.relative_path = None
			self.is_home_plugin = False

	def module_name(self):
		return self.pclass.__module__

	def class_name(self):
		return self.pclass.__name__

	def id(self):
		return self.pclass.__module__+"."+self.pclass.__name__

	def plugin_name(self):
		return self.obj.NAME

	def plugin_version(self):
		return self.obj.VERSION

	def plugin_description(self):
		if hasattr(self.obj,"DESCRIPTION"): return self.obj.DESCRIPTION
		return None

def load_plugins(are_plugins_blocked,additional_locations):
	global PLUGINS

	PLUGINS = []
	ERRORS = []
	DIRECTORIES = []

	if not config.ENABLE_PLUGINS: return []
	if are_plugins_blocked: return []

	DIRECTORIES.append(PLUGIN_DIRECTORY)
	if len(additional_locations)>0:
		for loc in additional_locations:
			DIRECTORIES.append(loc)

	with PikeManager(DIRECTORIES) as mgr:
		classes = mgr.get_classes()

	for c in classes:
		# Ignore the base plugin class
		if c.__name__=="Plugin": continue

		# Create an instance of the plugin class
		obj = c()

		# Create the plugin entry for the registry (and errors)
		entry = PluginEntry(c,obj)

		# Make sure the class has any required attributes
		had_error = False
		if not hasattr(obj,"NAME"):
			entry.errors.append("No name attribute")
			had_error = True
		else:
			n = obj.NAME.strip()
			if len(n)==0:
				entry.errors.append("Name entry is blank")
				had_error = True

		if not hasattr(obj,"VERSION"):
			entry.errors.append("No version attribute")
			had_error = True

		# Make sure the plugin inherits from the "Plugin" class
		if not issubclass(type(obj), Plugin):
			entry.errors.append("Plugin doesn't inherit from \"Plugin\"")
			had_error = True

		# Make sure that the input() event method is valid, if the
		# plugin has one
		if check_for_bad_input(obj):
			entry.errors.append("Malicious input() event method detected")
			had_error = True

		# Make sure that the plugin has at least *one* event method
		counter = 0
		for e in EVENTS:
			if hasattr(obj,e): counter = counter+1
		if counter==0:
			entry.errors.append("Plugin doesn't have any "+APPLICATION_NAME+" event methods")
			had_error = True

		entry.number_of_events = counter

		# If we had an error, don't add the plugin to the registry
		if had_error:
			ERRORS.append(entry)
			continue

		# Add the plugin to the registry
		PLUGINS.append(entry)

	# Return any errors
	return ERRORS

def get_size(obj, seen=None):
	"""Recursively finds size of objects"""
	size = sys.getsizeof(obj)
	if seen is None:
		seen = set()
	obj_id = id(obj)
	if obj_id in seen:
		return 0
	# Important mark as seen *before* entering recursion to gracefully handle
	# self-referential objects
	seen.add(obj_id)
	if isinstance(obj, dict):
		size += sum([get_size(v, seen) for v in obj.values()])
		size += sum([get_size(k, seen) for k in obj.keys()])
	elif hasattr(obj, '__dict__'):
		size += get_size(obj.__dict__, seen)
	elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
		size += sum([get_size(i, seen) for i in obj])
	return size