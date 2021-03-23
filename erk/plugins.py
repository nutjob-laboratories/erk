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

PLUGINS = []

class Plugin():

	irc = None

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

def public_message(client,channel,user,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"public"):
			obj.public(channel,user,message)
		obj.irc = None

def private_message(client,user,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"private"):
			obj.private(user,message)
		obj.irc = None

def action_message(client,target,user,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"action"):
			obj.action(target,user,message)
		obj.irc = None

def line_in(client,data):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"line_in"):
			obj.line_in(data)
		obj.irc = None

def line_out(client,data):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"line_out"):
			obj.line_out(data)
		obj.irc = None

def mode_message(client,channel,user,mset,modes,args):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"mode"):
			obj.mode(channel,user,mset,modes,args)
		obj.irc = None

def tick(client,uptime):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"tick"):
			obj.tick(uptime)
		obj.irc = None

def input(client,window,text):
	result = False
	if window.type==config.SERVER_WINDOW:
		name = None
	else:
		name = window.name
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"input"):
			result = obj.input(name,text)
		obj.irc = None
		if result: return result

def notice_message(client,target,user,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"notice"):
			obj.notice(target,user,message)
		obj.irc = None

def motd(client,smotd):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"motd"):
			obj.motd(smotd)
		obj.irc = None

def registered(client):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"registered"):
			obj.registered()
		obj.irc = None

def join(client,channel,user):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"join"):
			obj.join(channel,user)
		obj.irc = None

def part(client,channel,user):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"part"):
			obj.part(channel,user)
		obj.irc = None

def joined(client,channel):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"joined"):
			obj.joined(channel)
		obj.irc = None

def parted(client,channel):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"parted"):
			obj.parted(channel)
		obj.irc = None

def kick(client,channel,kickee,kicker,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"kick"):
			obj.kick(channel,kickee,kicker,message)
		obj.irc = None

def kicked(client,channel,kicker,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"kicked"):
			obj.kicked(channel,kicker,message)
		obj.irc = None

def quit(client,nick,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"quit"):
			obj.quit(nick,message)
		obj.irc = None

def ctcp(client,user,target,tag,message):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"ctcp"):
			obj.ctcp(user,target,tag,message)
		obj.irc = None

def connect(client):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"connect"):
			obj.connect(user)
		obj.irc = None

def topic(client,channel,user,topic):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"topic"):
			obj.connect(channel,user,topic)
		obj.irc = None

def nick(client,oldnick,newnick):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"nick"):
			obj.nick(oldnick,newnick)
		obj.irc = None

def invite(client,user,channel):
	for p in PLUGINS:
		obj = p.obj
		obj.irc = client
		if hasattr(obj,"invite"):
			obj.invite(user,channel)
		obj.irc = None

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

	def module_name(self):
		return self.pclass.__module__

	def class_name(self):
		return self.pclass.__name__

	def plugin_name(self):
		return self.obj.name

	def plugin_version(self):
		return self.obj.version

	def plugin_description(self):
		if hasattr(self.obj,"description"): return self.obj.description
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
		if not hasattr(obj,"name"):
			entry.errors.append("No name attribute")
			had_error = True
		else:
			n = obj.name.strip()
			if len(n)==0:
				entry.errors.append("Name entry is blank")
				had_error = True

		if not hasattr(obj,"version"):
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