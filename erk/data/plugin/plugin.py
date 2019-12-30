from erk import *

class !_PLUGIN_NAME!(Plugin):

	def __init__(self):
		self.name = "!PLUGIN_FULL_NAME!"
		self.description = "UNKNOWN"
		
		self.author = "UNKNOWN"
		self.version = "1.0"

		self.website = None
		self.source = None

	def load(self):
		pass

	def unload(self):
		pass

	def input(self,client,name,text):
		pass

	def public(self,client,channel,user,message):
		pass

	def private(self,client,user,message):
		pass
