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

import inspect
import os
import pkgutil
import imp

from erk.plugins.enums import *
from erk.plugins.types import *
from erk.plugins.objects import SET_IRC_OBJECT,SET_GUI_OBJECT,ERK,IRC,HEAP

# PLUGIN_MESSAGE_METHOD = 'handle_message'
# PLUGIN_INPUT_METHOD = 'handle_input'


class Plugin(object):
	"""Base class that each plugin must inherit from. within this class
	you must define the methods that all of your plugins must implement
	"""
	name = "No name"
	author = "Unknown"
	version = "1.0"

	website = None
	source = None

	def __init__(self):
		self.description = 'UNKNOWN'

	def handle_message(self,message):
		pass

	def handle_input(self,text):
		pass

	def handle_event(self,event):
		pass

	def load(self):
		pass

	def unload(self):
		pass




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


	def reload_plugins(self,do_reload=False):
		"""Reset the list of all plugins and initiate the walk over the main
		provided plugin package to load all available plugins
		"""
		self.plugins = []
		self.seen_paths = []
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
					# Only add classes that are a sub class of Plugin, but NOT Plugin itself
					if issubclass(c, Plugin) & (c is not Plugin):
						plugin = c()

						pm = c.__module__.split(".")
						pm.pop(0)
						plugin._icon = inspect.getfile(c).replace(".py",".png")
						plugin.__file__ = inspect.getfile(c).replace(".pyc",".py")
						plugin._package = ".".join(pm)
						plugin._class = f"{c.__name__}"

						self.plugins.append(plugin)


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
