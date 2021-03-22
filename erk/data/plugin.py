from erk import *

class BlankPlugin(Plugin):

	name = "Blank Plugin"
	version = "1.0"
	description = "This is a blank plugin"

	def action(self,target,user,message):
		pass

	def ctcp(self,user,target,tag,message):
		pass

	def input(self,window,text):
		pass

	def join(self,channel,user):
		pass

	def joined(self,channel):
		pass

	def kick(self,channel,kickee,kicker,message):
		pass

	def kicked(self,channel,kicker,message):
		pass

	def line_in(self,line):
		pass

	def line_out(self,line):
		pass

	def mode(self,channel,user,mset,modes,args):
		pass

	def motd(self,motd_message):
		pass

	def notice(self,target,user,message):
		pass

	def part(self,channel,user):
		pass

	def parted(self,channel):
		pass

	def private(self,user,message):
		pass

	def public(self,channel,user,message):
		pass

	def quit(self,nickname,message):
		pass

	def registered(self):
		pass

	def tick(self,uptime):
		pass
