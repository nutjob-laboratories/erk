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

import shlex

from erk.common import *
import emoji

def escape_single_quotes(text):
	return text.replace("'","\\'")

def unescape_single_quotes(tlist):
	u = []
	for e in tlist:
		u.append(e.replace("\\'","'"))
	return u

def is_int(data):
	try:
		x = int(data)
	except:
		return False
	return True

def is_valid_color(data):
	if int(data)>=0:
		if int(data)<=15:
			return True
	return False

# New commands should be added to INPUT_COMMANDS in erk.common
# This enables their use with autocomplete

def handle_chat_input(obj,text,is_user=False):
	#print(text)

	if not len(text)>0: return

	etext = escape_single_quotes(text)
	tokens = shlex.split(etext)
	tokens = unescape_single_quotes(tokens)

	colored_text = False
	error = []
	color_command = False
	color_command_tokens = len(tokens)

	if len(tokens)>=3:
		if tokens[0].lower()=="/color":
			color_command = True
			tokens.pop(0)	# remove command
			fore = tokens.pop(0)
			back = tokens.pop(0)
			if is_int(fore):
				if is_valid_color(fore):
					if color_command_tokens>3:
						# background?
						if is_int(back):
							if is_valid_color(back):
								colored_text = True
								text = chr(3)+fore+","+back+' '.join(tokens)+chr(3)
							else:
								colored_text = True
								text = chr(3)+fore+back+' '.join(tokens)+chr(3)
						else:
							colored_text = True
							text = chr(3)+fore+back+' '.join(tokens)+chr(3)
					else:
						colored_text = True
						text = chr(3)+fore+back+chr(3)
				else:
					error.append("\""+fore+"\" is not a valid color")
			else:
				error.append("\""+fore+"\" is not a number")

	if len(error)>0:
		for e in error:
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],e)
			obj.gui.writeToChannel(obj.client,obj.name,msg)
		msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /color FOREGROUND [BACKGROUND] MESSAGE" )
		obj.gui.writeToChannel(obj.client,obj.name,msg)
		return

	if not colored_text:
		if color_command:
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /color FOREGROUND [BACKGROUND] MESSAGE" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if colored_text:
		# Inject emojis
		if obj.gui.use_emojis:
			text = emoji.emojize(text,use_aliases=True)

		# Inject ASCIImojis
		if obj.gui.use_asciimojis:
			text = inject_asciiemojis(text)

		obj.client.msg(obj.name,text)

		msg = render_message(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SELF_STYLE_NAME],obj.client.nickname,obj.gui.styles[MESSAGE_STYLE_NAME],text )
		obj.gui.writeToChannel(obj.client,obj.name,msg)
		obj.gui.writeToChannelLog(obj.client,obj.name,GLYPH_SELF+obj.client.nickname,text)
		return

	if len(tokens)==1:
		if tokens[0].lower()=="/color":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /color FOREGROUND [BACKGROUND] MESSAGE" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if len(tokens)==1:
		if tokens[0].lower()=="/list":
			obj.client.sendLine(f"LIST")
			return

	if len(tokens)>1:
		if tokens[0].lower()=="/list":
			tokens.pop(0)	# remove command
			for c in tokens:
				if c[:1]!='#':
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],f"\"{c}\" is not a valid channel name")
					obj.gui.writeToChannel(obj.client,obj.name,msg)
					return
			obj.client.sendLine(f"LIST "+",".join(tokens))
			return

	if len(tokens)>=2:
		if tokens[0].lower()=="/away":
			tokens.pop(0)	# remove command
			msg = ' '.join(tokens)
			obj.client.away(msg)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/away":
			obj.client.away("I'm busy")
			return

	if len(tokens)>=1:
		if tokens[0].lower()=="/back":
			obj.client.back()
			return

	if len(tokens)>=2:
		if tokens[0].lower()=="/quit":
			tokens.pop(0)	# remove command
			msg = ' '.join(tokens)
			obj.gui.disconnectFromIRC(obj.client,msg)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/quit":
			obj.gui.disconnectFromIRC(obj.client)
			return

	if is_user:
		if len(tokens)>=3:
			if tokens[0].lower()=="/invite":
				tokens.pop(0)	# remove command
				channel = tokens.pop(0)
				users = tokens
				if channel[:1]=='#':
					for u in users:
						obj.client.sendLine(f"INVITE {u} {channel}")
					return
				else:
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],"\""+channel+"\" is not a valid channel name" )
					obj.gui.writeToChannel(obj.client,obj.name,msg)
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"invite: /invite CHANNEL USER [USER ...]" )
					obj.gui.writeToChannel(obj.client,obj.name,msg)
					return
		if len(tokens)<3:
			if tokens[0].lower()=="/invite":
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /invite CHANNEL USER [USER ...]" )
				obj.gui.writeToChannel(obj.client,obj.name,msg)
				return
	else:
		if len(tokens)>2:
			if tokens[0].lower()=="/invite":
				tokens.pop(0)	# remove command
				channel = tokens.pop(0)
				users = tokens
				if channel[:1]=='#':
					for u in users:
						obj.client.sendLine(f"INVITE {u} {channel}")
					return
				else:
					obj.client.sendLine(f"INVITE {channel} {obj.name}")
					for u in users:
						obj.client.sendLine(f"INVITE {u} {obj.name}")
					return
		if len(tokens)==2:
			if tokens[0].lower()=="/invite":
				tokens.pop(0)	# remove command
				target = tokens.pop(0)
				if target[:1]=='#':
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],"\""+target+"\" is not a valid user name" )
					obj.gui.writeToChannel(obj.client,obj.name,msg)
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"invite: /invite [CHANNEL] USER [USER ...]" )
					obj.gui.writeToChannel(obj.client,obj.name,msg)
					return
				else:
					obj.client.sendLine(f"INVITE {target} {obj.name}")
					return
		if len(tokens)==1:
			if tokens[0].lower()=="/invite":
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /invite [CHANNEL] USER [USER ...]" )
				obj.gui.writeToChannel(obj.client,obj.name,msg)
				return


	if len(tokens)==3:
		if tokens[0].lower()=="/oper":
			tokens.pop(0)	# remove command
			username = tokens.pop(0)
			password = tokens.pop(0)
			obj.client.sendLine(f"OPER {username} {password}")
			return
	if len(tokens)!=3:
		if tokens[0].lower()=="/oper":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /oper USERNAME PASSWORD" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if is_user:
		if len(tokens)>2:
			if tokens[0].lower()=="/topic":
				tokens.pop(0)	# remove command
				target = tokens.pop(0)
				topic = ' '.join(tokens)
				if target[:1]=='#':
					obj.client.topic(target,topic)
					return
				else:
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],"\""+target+"\" is not a valid channel name" )
					obj.gui.writeToChannel(obj.client,obj.name,msg)
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /topic CHANNEL NEW_TOPIC" )
					obj.gui.writeToChannel(obj.client,obj.name,msg)
					return
		if len(tokens)<=2:
			if tokens[0].lower()=="/topic":
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /topic CHANNEL NEW_TOPIC" )
				obj.gui.writeToChannel(obj.client,obj.name,msg)
				return
	else:
		if len(tokens)>=2:
			if tokens[0].lower()=="/topic":
				tokens.pop(0)	# remove command
				target = tokens.pop(0)
				topic = ' '.join(tokens)
				if target[:1]=='#':
					obj.client.topic(target,topic)
					return
				else:
					obj.client.topic(obj.name,target+' '+topic)
					return
		if len(tokens)==1:
			if tokens[0].lower()=="/topic":
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /topic [CHANNEL] NEW_TOPIC" )
				obj.gui.writeToChannel(obj.client,obj.name,msg)
				return

	if len(tokens)==2:
		if tokens[0].lower()=="/whois":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.sendLine(f"WHOIS {target}")
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/whois":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /whois NICKNAME" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if len(tokens)==2:
		if tokens[0].lower()=="/nick":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.setNick(target)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/nick":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /nick NICKNAME" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/part":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			pmsg = ' '.join(tokens)
			obj.client.part(target,pmsg)
			obj.gui.irc_parting(obj.client,target)
			return
	if len(tokens)==2:
		if tokens[0].lower()=="/part":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.part(target)
			obj.gui.irc_parting(obj.client,target)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/part":
			if is_user:
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /part CHANNEL [MESSAGE]" )
				obj.gui.writeToChannel(obj.client,obj.name,msg)
				return
			obj.client.part(obj.name)
			obj.gui.irc_parting(obj.client,obj.name)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/join":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			key = ' '.join(tokens)
			obj.client.join(target,key)
			return
	if len(tokens)==2:
		if tokens[0].lower()=="/join":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.join(target)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/join":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /join CHANNEL [KEY]" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/notice":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if obj.gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if obj.gui.use_asciimojis: msg = inject_asciiemojis(msg)
			obj.client.notice(target,msg)

			if len(target)>0:
				if target[:1]=='#':
					# channel
					obj.gui.writeChannelMessage(obj.client,target,msg,True)
					return
				else:
					# user
					obj.gui.writePrivateMessage(obj.client,target,msg,True)
					return
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/notice":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /notice TARGET MESSAGE" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/msg":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if obj.gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if obj.gui.use_asciimojis: msg = inject_asciiemojis(msg)
			obj.client.msg(target,msg)

			if len(target)>0:
				if target[:1]=='#':
					# channel
					obj.gui.writeChannelMessage(obj.client,target,msg)
					return
				else:
					# user
					obj.gui.writePrivateMessage(obj.client,target,msg)
					return
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/msg":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /msg TARGET MESSAGE" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if len(tokens)>=2:
		if tokens[0].lower()=="/me":
			tokens.pop(0)	# remove command
			msg = ' '.join(tokens)
			if obj.gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if obj.gui.use_asciimojis: msg = inject_asciiemojis(msg)
			obj.client.describe(obj.name,msg)
			pmsg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ACTION_STYLE_NAME],obj.client.nickname+" "+msg )
			obj.gui.writeToChannel(obj.client,obj.name,pmsg)
			obj.gui.writeToChannelLog(obj.client,obj.name,GLYPH_ACTION+obj.client.nickname,msg)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/me":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /me MESSAGE" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	# Inject emojis
	if obj.gui.use_emojis:
		text = emoji.emojize(text,use_aliases=True)

	# Inject ASCIImojis
	if obj.gui.use_asciimojis:
		text = inject_asciiemojis(text)

	obj.client.msg(obj.name,text)

	msg = render_message(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SELF_STYLE_NAME],obj.client.nickname,obj.gui.styles[MESSAGE_STYLE_NAME],text )
	obj.gui.writeToChannel(obj.client,obj.name,msg)
	obj.gui.writeToChannelLog(obj.client,obj.name,GLYPH_SELF+obj.client.nickname,text)

def handle_console_input(obj,text):
	
	# Handle any commands here
	etext = escape_single_quotes(text)
	tokens = shlex.split(etext)
	tokens = unescape_single_quotes(tokens)

	if len(tokens)==1:
		if tokens[0].lower()=="/list":
			obj.client.sendLine(f"LIST")
			return

	if len(tokens)>1:
		if tokens[0].lower()=="/list":
			tokens.pop(0)	# remove command
			for c in tokens:
				if c[:1]!='#':
					msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],f"\"{c}\" is not a valid channel name")
					obj.gui.writeToConsole(obj.client,msg)
					return
			obj.client.sendLine(f"LIST "+",".join(tokens))
			return

	if len(tokens)>=2:
		if tokens[0].lower()=="/away":
			tokens.pop(0)	# remove command
			msg = ' '.join(tokens)
			obj.client.away(msg)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/away":
			obj.client.away("I'm busy")
			return

	if len(tokens)>=1:
		if tokens[0].lower()=="/back":
			obj.client.back()
			return

	if len(tokens)>=2:
		if tokens[0].lower()=="/send":
			if not obj.gui.enable_send_cmd:
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],"The \"send\" command is not enabled")
				obj.gui.writeToConsole(obj.client,msg)
				return
			tokens.pop(0)	# remove command
			msg = ' '.join(tokens)
			obj.client.sendLine(msg)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/send":
			if not obj.gui.enable_send_cmd:
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],"The \"send\" command is not enabled")
				obj.gui.writeToConsole(obj.client,msg)
				return
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /send COMMAND ..." )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)>=2:
		if tokens[0].lower()=="/quit":
			tokens.pop(0)	# remove command
			msg = ' '.join(tokens)
			obj.gui.disconnectFromIRC(obj.client,msg)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/quit":
			obj.gui.disconnectFromIRC(obj.client)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/invite":
			tokens.pop(0)	# remove command
			channel = tokens.pop(0)
			users = tokens
			if channel[:1]=='#':
				for u in users:
					obj.client.sendLine(f"INVITE {u} {channel}")
				return
			else:
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],"\""+channel+"\" is not a valid channel name" )
				obj.gui.writeToConsole(obj.client,msg)
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"invite: /invite CHANNEL USER [USER ...]" )
				obj.gui.writeToConsole(obj.client,msg)
				return
	if len(tokens)<3:
		if tokens[0].lower()=="/invite":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /invite CHANNEL USER [USER ...]" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)==3:
		if tokens[0].lower()=="/oper":
			tokens.pop(0)	# remove command
			username = tokens.pop(0)
			password = tokens.pop(0)
			obj.client.sendLine(f"OPER {username} {password}")
			return
	if len(tokens)!=3:
		if tokens[0].lower()=="/oper":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /oper USERNAME PASSWORD" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)>2:
		if tokens[0].lower()=="/topic":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			topic = ' '.join(tokens)
			if target[:1]=='#':
				obj.client.topic(target,topic)
				return
			else:
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[ERROR_STYLE_NAME],"\""+target+"\" is not a valid channel name" )
				obj.gui.writeToConsole(obj.client,msg)
				msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /topic CHANNEL NEW_TOPIC" )
				obj.gui.writeToConsole(obj.client,msg)
				return
	if len(tokens)<=2:
		if tokens[0].lower()=="/topic":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /topic CHANNEL NEW_TOPIC" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)==2:
		if tokens[0].lower()=="/whois":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.sendLine(f"WHOIS {target}")
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/whois":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /whois NICKNAME" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)==2:
		if tokens[0].lower()=="/nick":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.setNick(target)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/nick":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /nick NICKNAME" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/part":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			pmsg = ' '.join(tokens)
			obj.client.part(target,pmsg)
			obj.gui.irc_parting(obj.client,target)
			return
	if len(tokens)==2:
		if tokens[0].lower()=="/part":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.part(target)
			obj.gui.irc_parting(obj.client,target)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/part":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /part CHANNEL [MESSAGE]" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/join":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			key = ' '.join(tokens)
			obj.client.join(target,key)
			return
	if len(tokens)==2:
		if tokens[0].lower()=="/join":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.join(target)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/join":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /join CHANNEL [KEY]" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/notice":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if obj.gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if obj.gui.use_asciimojis: msg = inject_asciiemojis(msg)
			obj.client.notice(target,msg)

			if len(target)>0:
				if target[:1]=='#':
					# channel
					obj.gui.writeChannelMessage(obj.client,target,msg,True)
					return
				else:
					# user
					obj.gui.writePrivateMessage(obj.client,target,msg,True)
					return
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/notice":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /notice TARGET MESSAGE" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	if len(tokens)>=3:
		if tokens[0].lower()=="/msg":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if obj.gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if obj.gui.use_asciimojis: msg = inject_asciiemojis(msg)
			obj.client.msg(target,msg)

			if len(target)>0:
				if target[:1]=='#':
					# channel
					obj.gui.writeChannelMessage(obj.client,target,msg)
					return
				else:
					# user
					obj.gui.writePrivateMessage(obj.client,target,msg)
					return
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/msg":
			msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Usage: /msg TARGET MESSAGE" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	# No valid command detected
	msg = render_system(obj.gui, obj.gui.styles[TIMESTAMP_STYLE_NAME],obj.gui.styles[SYSTEM_STYLE_NAME],"Unrecognized command: \""+text+"\"" )
	obj.gui.writeToConsole(obj.client,msg)
	return
