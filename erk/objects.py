
from datetime import datetime

class Window:
	def __init__(self,index,widget):
		self.index = index
		self.widget = widget

class ConnectInfo:
	def __init__(self,server,port,password,ssl,nick,alter,username,realname,reconnect,autojoin):
		self.server = server
		self.port = int(port)
		self.password = password
		self.ssl = ssl
		self.nickname = nick
		self.alternate = alter
		self.username = username
		self.realname = realname
		self.reconnect = reconnect
		self.autojoin = autojoin

SYSTEM_MESSAGE = 0
CHAT_MESSAGE = 1
SELF_MESSAGE = 2
ERROR_MESSAGE = 3
ACTION_MESSAGE = 4
NOTICE_MESSAGE = 5
PRIVATE_MESSAGE = 6
HORIZONTAL_RULE_MESSAGE = 7

class Message:
	def __init__(self,mtype,sender,contents,timestamp=None):
		if timestamp:
			self.timestamp = timestamp
		else:
			self.timestamp = datetime.timestamp(datetime.now())
		self.type = mtype
		self.sender = sender
		self.contents = contents

class WhoisData:
	def __init__(self):
		self.nickname = 'Unknown'
		self.username = 'Unknown'
		self.realname = 'Unknown'
		self.host = 'Unknown'
		self.signon = '0'
		self.idle = '0'
		self.server = 'Unknown'
		self.channels = 'Unknown'
		self.privs = 'is a normal user'