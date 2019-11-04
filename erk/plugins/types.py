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

class EVENT(object):
	def __init__(self,etype,data):
		self.type = etype
		self.data = data

	def __eq__(self,other):
		return self.type == other

	def __iter__(self):
		return self.data

	def __getitem__(self,key):
		return self.data[key]

	def __setitem__(self,key,value):
		pass

	def __delitem__(self,key):
		pass

	def __missing__(self,key):
		return None

	def __len__(self):
		return len(self.data)

	def __contains__(self,key):
		if key in self.data: return True
		return False

class PRIVMSG(object):
	def __init__(self,mtype,target,sender,message):
		self.type = mtype
		self.target = target
		self.sender = sender
		self.message = message

	def __eq__(self,other):
		return self.type == other

	def __repr__(self):
		return "PRIVMSG(type=Message."+self.type.name+",target=\""+self.target+"\",sender=\""+self.sender+"\",message=\""+self.message+"\")"

	def __str__(self):
		return self.message

class INPUT(object):
	def __init__(self,text,window,console):
		self.text = text
		self.window = window
		self.console = console

	def __repr__(self):
		return 'INPUT(text="'+self.text+'",window="'+self.window+'",console='+str(self.console)+')'

	def __str__(self):
		return self.text
