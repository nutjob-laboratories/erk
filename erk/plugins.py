
# Adapted from https://www.guidodiepen.nl/2019/02/implementing-a-simple-plugin-framework-in-python/

import sys
import inspect
import os
import pkgutil
import imp
import json

from erk.objects import *
from erk.strings import *
from erk.events import *
import erk.config

INSTALL_DIRECTORY = sys.path[0]
PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")
if not os.path.isdir(PLUGIN_DIRECTORY): os.mkdir(PLUGIN_DIRECTORY)

SETTINGS_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "settings")
DISABLED_FILE = os.path.join(SETTINGS_DIRECTORY, "disabled.json")

DISABLED_PLUGINS = []
LOADED_PLUGINS = []

def get_disabled(filename=DISABLED_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_disabled:
			data = json.load(read_disabled)
			return data
	else:
		return []

def save_disabled(filename=DISABLED_FILE):
	with open(filename, "w") as write_data:
		json.dump(DISABLED_PLUGINS, write_data, indent=4, sort_keys=True)

DISABLED_PLUGINS = get_disabled()

class ErkFunctions(object):

	def __init__(self):
		self.client = None

	def info(self):
		return APPLICATION_NAME+" "+APPLICATION_VERSION

	def console(self,text):
		if self.client:
			window = erk.events.fetch_console_window(self.client)
			if window:
				msg = Message(PLUGIN_MESSAGE,'',text)
				window.writeText(msg,True)

	def write(self,name,text):
		if self.client:
			windows = erk.events.fetch_window_list(self.client)
			for w in windows:
				if w.name==name:
					msg = Message(PLUGIN_MESSAGE,'',text)
					w.writeText(msg,True)

	def log(self,text):
		if self.client:
			windows = erk.events.fetch_window_list(self.client)
			for w in windows:
				if w.name==name:
					msg = Message(PLUGIN_MESSAGE,'',text)
					w.writeText(msg,True)




class Plugin(ErkFunctions):
	"""Base class that each plugin must inherit from. within this class
	you must define the methods that all of your plugins must implement
	"""
	name = "No name"
	author = "Unknown"
	version = "1.0"

	description = 'UNKNOWN'

	website = None
	source = None

	def input(self,client,name,text):
		pass

	def public(self,client,channel,user,message):
		pass

	def private(self,client,user,message):
		pass

	def load(self):
		pass

	def unload(self):
		pass

def check_for_attributes(p):
	errors = []

	if hasattr(p,"description"):
		if p.description=='UNKNOWN':
			errors.append(p.__file__+": \"description\" attribute is set to the default")
	else:
		errors.append(p.__file__+': Missing \"description\" attribute')

	if hasattr(p,"name"):
		if p.name=='No name':
			errors.append(p.__file__+": \"name\" attribute is set to the default")
	else:
		errors.append(p.__file__+': Missing \"name\" attribute')

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
		if not erk.config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"private"):
				p.client = client
				p.private(client,user,text)
				p.client = None

	def public(self,client,channel,user,text):
		if not erk.config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"public"):
				p.client = client
				p.public(client,channel,user,text)
				p.client = None

	def input(self,client,name,text):
		if not erk.config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if hasattr(p,"input"):
				p.client = client
				if p.input(client,name,text):
					p.client = None
					return True
				p.client = None

	def load(self):
		if not erk.config.PLUGINS_ENABLED: return
		for p in self.plugins:
			if p.name in DISABLED_PLUGINS: continue
			if p.name in LOADED_PLUGINS: continue
			if hasattr(p,"load"):
				p.client = None
				p.load()
				LOADED_PLUGINS.append(p.name)

	def unload(self):
		for p in self.plugins:
			if not p.name in LOADED_PLUGINS: continue
			if hasattr(p,"unload"):
				p.client = None
				p.unload()

	def errors(self):
		return self.load_errors

	def reload_plugins(self,do_reload=False):
		"""Reset the list of all plugins and initiate the walk over the main
		provided plugin package to load all available plugins
		"""
		self.plugins = []
		self.seen_paths = []
		self.load_errors = []
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

				clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
				for (_, c) in clsmembers:

					if issubclass(c, Plugin) & (c is not Plugin):
						plugin = c()

						pm = c.__module__.split(".")
						pm.pop(0)
						plugin._icon = inspect.getfile(c).replace(".py",".png")
						plugin.__file__ = inspect.getfile(c).replace(".pyc",".py")

						plugin._packicon = package_icon

						if package_name:
							plugin._package = package_name
						else:
							plugin._package = ".".join(pm)

						# plugin._package = ".".join(pm)

						plugin._class = f"{c.__name__}"
						
						no_plugin_errors = True

						# Check for methods
						if not check_for_methods(plugin):
							self.load_errors.append(plugin.__file__+": Missing valid entry points")
							no_plugin_errors = False

						# Check for attributes
						e = check_for_attributes(plugin)
						if len(e)>0:
							self.load_errors = self.load_errors + e
							no_plugin_errors = False

						# Plugin name must be unique
						for p in self.plugins:
							if p.name == plugin.name:
								self.load_errors.append(plugin.__file__+": A plugin named \""+plugin.name+"\" is already loaded")
								no_plugin_errors = False

						# Check for a malicious input method
						if check_for_bad_input(plugin):
							self.load_errors.append(plugin.__file__+": Malicious input method detected")
							no_plugin_errors = False

						if no_plugin_errors: self.plugins.append(plugin)

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
