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

import sys
import inspect
import os
import pkgutil
import imp
import json

from .objects import *
from .strings import *
from .events import *
from . import config
from .userinput import handle_input

from .files import get_user,save_user

INSTALL_DIRECTORY = sys.path[0]
PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")
if not os.path.isdir(PLUGIN_DIRECTORY): os.mkdir(PLUGIN_DIRECTORY)

DISABLED_PLUGINS = []
LOADED_PLUGINS = []

def get_disabled(config):
	udata = get_user(config)
	return udata["disabled_plugins"]

def save_disabled(config):
	udata = get_user(config)
	udata["disabled_plugins"] = DISABLED_PLUGINS
	save_user(udata,config)

DISABLED_PLUGINS = []

class PluginError():
	def __init__(self,package,classname,file,reason):
		self.package = package
		self.classname = classname
		self.file = file
		self.reason = reason

class ErkFunctions(object):

	def __init__(self):
		self._erk_client = None
		self._erk_window_name = None

	def uptime(self):
		if self._erk_client:
			return self._erk_client.uptime
		else:
			return 0

	def exec(self,data):
		if self._erk_client and self._erk_window_name:
			if self._erk_window_name==SERVER_CONSOLE_NAME:
				window = erk.events.fetch_console_window(self._erk_client)
			else:
				windows = erk.events.fetch_window_list(self._erk_client)
				for w in windows:
					if w.name==self._erk_window_name:
						window = w

		if not window: return False
		
		handle_input(window,self._erk_client,data)
		return True

	def info(self):
		return APPLICATION_NAME+" "+APPLICATION_VERSION

	def print(self,text):
		if self._erk_client and self._erk_window_name:
			if self._erk_window_name==SERVER_CONSOLE_NAME:
				self.console(text)
			else:
				self.write(self._erk_window_name,text)

	def console(self,text):
		if self._erk_client:
			window = erk.events.fetch_console_window(self._erk_client)
			if window:
				msg = Message(PLUGIN_MESSAGE,'',text)
				window.writeText(msg,True)

	def write(self,name,text):
		if self._erk_client:
			windows = erk.events.fetch_window_list(self._erk_client)
			for w in windows:
				if w.name==name:
					msg = Message(PLUGIN_MESSAGE,'',text)
					w.writeText(msg,True)

	def log(self,name,text):
		if self._erk_client:
			windows = erk.events.fetch_window_list(self._erk_client)
			for w in windows:
				if w.name==name:
					msg = Message(PLUGIN_MESSAGE,'',text)
					w.writeText(msg,True)




class Plugin(ErkFunctions):
	"""Base class that each plugin must inherit from. within this class
	you must define the methods that all of your plugins must implement
	"""
	name = None
	author = None
	version = None

	description = None

	website = None
	source = None

def check_for_attributes(p):
	errors = []

	if hasattr(p,"description"):
		if p.description==None:
			err = PluginError(p._package,p._class,p.__file__,"\"description\" attribute is not set")
			errors.append(err)
	else:
		err = PluginError(p._package,p._class,p.__file__,"Missing \"description\" attribute")
		errors.append(err)

	if hasattr(p,"name"):
		if p.name==None:
			err = PluginError(p._package,p._class,p.__file__,"\"name\" attribute is not set")
			errors.append(err)
	else:
		err = PluginError(p._package,p._class,p.__file__,"Missing \"name\" attribute")
		errors.append(err)

	return errors

def check_for_methods(p):
	if hasattr(p,"load") or hasattr(p,"unload") or hasattr(p,"input") or hasattr(p,"public") or hasattr(p,"private"):
		return True
	return False

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

class PluginCollection(object):
	"""Upon creation, this class will read the plugins package for modules
	that contain a class definition that is inheriting from the Plugin class
	"""

	def __init__(self, plugin_package):
		"""Constructor that initiates the reading of all available plugins
		when an instance of the PluginCollection object is created
		"""
		self.plugin_package = plugin_package
		self.reload_plugins()

	def private(self,client,user,text):
		if not config.PLUGINS_ENABLED: return
		p = user.split('!')
		if len(p)==2:
			name = p[0]
		else:
			name = user
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"private"):
				p._erk_client = client
				p._erk_window_name = name
				p.private(client,user,text)
				p._erk_client = None
				p._erk_window_name = None

	def public(self,client,channel,user,text):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"public"):
				p._erk_client = client
				p._erk_window_name = channel
				p.public(client,channel,user,text)
				p._erk_client = None
				p._erk_window_name = None

	def input(self,client,name,text):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"input"):
				p._erk_client = client
				p._erk_window_name = name
				if p.input(client,name,text):
					p._erk_client = None
					p._erk_window_name = None
					return True
				p._erk_client = None
				p._erk_window_name = None

	def forceload(self,name):
		for p in self.plugins:
			if name==p.name:
				if hasattr(p,"load"):
					p._erk_client = None
					p._erk_window_name = None
					p.load()
					if not p.name in LOADED_PLUGINS:
						LOADED_PLUGINS.append(p.name)

	def forceunload(self,name):
		for p in self.plugins:
			if name==p.name:
				if hasattr(p,"unload"):
					p._erk_client = None
					p._erk_window_name = None
					p.unload()
					if p.name in LOADED_PLUGINS:
						LOADED_PLUGINS.remove(p.name)

	def uninstall_forceunload(self,name):
		for p in self.plugins:
			if not p.name in LOADED_PLUGINS: continue
			if name==p.name:
				if hasattr(p,"unload"):
					p._erk_client = None
					p._erk_window_name = None
					p.unload()
					if p.name in LOADED_PLUGINS:
						LOADED_PLUGINS.remove(p.name)

	def load(self):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if p.name in LOADED_PLUGINS: continue
			if hasattr(p,"load"):
				p._erk_client = None
				p._erk_window_name = None
				p.load()
				LOADED_PLUGINS.append(p.name)

	def unload(self):
		for p in self.plugins:
			if not p.name in LOADED_PLUGINS: continue
			if hasattr(p,"unload"):
				p._erk_client = None
				p._erk_window_name = None
				p.unload()

	def tick(self,client):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"tick"):
				p._erk_client = client
				p._erk_window_name = None
				p.tick(client)
				p._erk_client = None
				p._erk_window_name = None

	def join(self,client,channel,user):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"join"):
				p._erk_client = client
				p._erk_window_name = channel
				p.join(client,channel,user)
				p._erk_client = None
				p._erk_window_name = None

	def part(self,client,channel,user):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"part"):
				p._erk_client = client
				p._erk_window_name = channel
				p.part(client,channel,user)
				p._erk_client = None
				p._erk_window_name = None

	def connect(self,client):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"connect"):
				p._erk_client = client
				p._erk_window_name = None
				p.connect(client)
				p._erk_client = None
				p._erk_window_name = None



	def notice(self,client,target,user,text):
		if not config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"notice"):
				p._erk_client = client
				p._erk_window_name = target
				p.notice(client,target,user,text)
				p._erk_client = None
				p._erk_window_name = None



	def errors(self):
		return self.load_errors

	def reset_errors(self):
		self.load_errors = []

	def reload_plugins(self,do_reload=False):
		"""Reset the list of all plugins and initiate the walk over the main
		provided plugin package to load all available plugins
		"""
		self.plugins = []
		self.seen_paths = []
		self.load_errors = []
		self.failed_load = []
		self.walk_package(self.plugin_package,do_reload)

	def walk_package(self,package,do_reload=False):
		"""Recursively walk the supplied package to retrieve all plugins
		"""
		imported_package = __import__(package, fromlist=['blah'])

		for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
			if not ispkg:
				plugin_module = __import__(pluginname, fromlist=['blah'])

				# Reload the plugin if it's already been loaded
				if do_reload:
					plugin_module = imp.reload(plugin_module)

				# Find the directory the module is stored in
				m = plugin_module.__name__.split('.')
				# Remove plugin.
				m.pop(0)
				# Remove .classfile
				m.pop()
				mfile = PLUGIN_DIRECTORY
				for f in m:
					mfile = os.path.join(mfile, f)

				no_package_info = True
				pinfo = os.path.join(mfile, "package")
				if not os.path.isfile(pinfo):
					pinfo = pinfo + ".txt"
					if os.path.isfile(pinfo):
						no_package_info = False
				else:
					no_package_info = False

				if not no_package_info:
					x = open(pinfo,mode="r", encoding='latin-1')
					package_name = str(x.read())
					x.close()
					package_name = package_name.strip()
				else:
					package_name = None

				package_icon = os.path.join(mfile, "package.png")

				package_directory = mfile

				clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
				for (_, c) in clsmembers:

					if issubclass(c, Plugin) & (c is not Plugin):
						plugin = c()

						pm = c.__module__.split(".")
						pm.pop(0)
						plugin._icon = inspect.getfile(c).replace(".py",".png")
						plugin.__file__ = inspect.getfile(c).replace(".pyc",".py")

						plugin._packicon = package_icon

						plugin._packdir = package_directory

						if package_name:
							plugin._package = package_name
						else:
							plugin._package = ".".join(pm)

						# plugin._package = ".".join(pm)

						plugin._class = f"{c.__name__}"
						
						no_plugin_errors = True

						# Check for methods
						if not check_for_methods(plugin):
							# self.load_errors.append(plugin.__file__+": Missing valid entry points")
							err = PluginError(plugin._package,plugin._class,plugin.__file__,"Missing a valid entry point")
							self.load_errors.append(err)
							no_plugin_errors = False

						# Check for attributes
						e = check_for_attributes(plugin)
						if len(e)>0:
							self.load_errors = self.load_errors + e
							no_plugin_errors = False

						# Plugin name must be unique
						for p in self.plugins:
							if p.name == plugin.name:
								#self.load_errors.append(plugin.__file__+": A plugin named \""+plugin.name+"\" is already loaded")
								err = PluginError(plugin._package,plugin._class,plugin.__file__,"A plugin named "+plugin.name+" is already loaded")
								self.load_errors.append(err)
								no_plugin_errors = False

						# Check for a malicious input method
						if check_for_bad_input(plugin):
							#self.load_errors.append(plugin.__file__+": Malicious input method detected")
							err = PluginError(plugin._package,plugin._class,plugin.__file__,"Malicious input method detected")
							self.load_errors.append(err)
							no_plugin_errors = False

						if no_plugin_errors:
							self.plugins.append(plugin)
						else:
							self.failed_load.append(plugin.__file__)
							self.failed_load.append(plugin.name)

				self.load()

		# Now that we have looked at all the modules in the current package, start looking
		# recursively for additional modules in sub packages
		all_current_paths = []
		if isinstance(imported_package.__path__, str):
			all_current_paths.append(imported_package.__path__)
		else:
			all_current_paths.extend([x for x in imported_package.__path__])

		for pkg_path in all_current_paths:
			if pkg_path not in self.seen_paths:
				self.seen_paths.append(pkg_path)

				# Get all sub directory of the current package path directory
				child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

				# For each sub directory, apply the walk_package method recursively
				for child_pkg in child_pkgs:
					self.walk_package(package + '.' + child_pkg)
