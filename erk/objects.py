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
WHOIS_MESSAGE = 8
PLUGIN_MESSAGE = 9

TYPE_MODE = 0
TYPE_TOPIC = 1
TYPE_QUIT = 2
TYPE_NICK = 3
TYPE_INVITE = 4
TYPE_PART = 5
TYPE_JOIN = 6

class Message:
	def __init__(self,mtype,sender,contents,timestamp=None,stype=None):
		if timestamp:
			self.timestamp = timestamp
		else:
			self.timestamp = datetime.timestamp(datetime.now())
		self.type = mtype
		self.sender = sender
		self.contents = contents
		self.stype = stype

class ChannelInfo:
	def __init__(self,name,count,topic):
		self.name = name
		self.count = count
		self.topic = topic

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

HELP_HTML_TEMPLATE='''<table style="width: 100%" border="0">
	<tbody>
        <tr>
          <td><center><b>Common Commands</b></center></td>
        </tr>
        <tr>
          <td>
            <table style="width: 100%" border="0">
              <tbody>
                %_LIST_%
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>'''

CHAT_HELP_HTML_TEMPLATE='''<table style="width: 100%" border="0">
	<tbody>
        <tr>
          <td><center><b>Chat Commands</b></center></td>
        </tr>
        <tr>
          <td>
            <table style="width: 100%" border="0">
              <tbody>
                %_LIST_%
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>'''

HELP_ENTRY='''<tr><td>%_USAGE_%&nbsp;</td><td><i>%_DESCRIPTION_%</i></td></tr>'''