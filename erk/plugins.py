
# Adapted from https://www.guidodiepen.nl/2019/02/implementing-a-simple-plugin-framework-in-python/

import sys
import inspect
import os
import pkgutil
import imp

from erk.objects import *

INSTALL_DIRECTORY = sys.path[0]
PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")
if not os.path.isdir(PLUGIN_DIRECTORY): os.mkdir(PLUGIN_DIRECTORY)

class ErkFunctions(object):

	def __init__(self):
		self._window = None

	def write(self,text):
		if self._window:
			#self._window.pluginWriteText(text)

			msg = Message(PLUGIN_MESSAGE,'',text)
			self._window.writeText(msg,True)

	def log(self,text):
		if self._window:
			msg = Message(PLUGIN_MESSAGE,'',text)
			self._window.writeText(msg,False)

	def _set_window_widget(self,obj):
		
		self._window = obj

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
		for p in self.plugins:
			if hasattr(p,"private"):
				p.private(client,user,text)

	def public(self,client,channel,user,text):
		for p in self.plugins:
			if hasattr(p,"public"):
				p.public(client,channel,user,text)

	def input(self,client,name,text):
		for p in self.plugins:
			if hasattr(p,"input"):
				p.input(client,name,text)

	def load(self):
		for p in self.plugins:
			if hasattr(p,"load"):
				p.load()

	def unload(self):
		for p in self.plugins:
			if hasattr(p,"unload"):
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

				clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
				for (_, c) in clsmembers:

					if issubclass(c, Plugin) & (c is not Plugin):
						plugin = c()

						pm = c.__module__.split(".")
						pm.pop(0)
						plugin._icon = inspect.getfile(c).replace(".py",".png")
						plugin.__file__ = inspect.getfile(c).replace(".pyc",".py")
						plugin._package = ".".join(pm)
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

						if no_plugin_errors: self.plugins.append(plugin)

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
