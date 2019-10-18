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
from erk.config import *
import emoji

def escape_single_quotes(text):
	return text.replace("'","\\'")

def unescape_single_quotes(tlist):
	u = []
	for e in tlist:
		u.append(e.replace("\\'","'"))
	return u

# New commands should be added to INPUT_COMMANDS in erk.common
# This enables their use with autocomplete

def handle_chat_input(obj,text,is_user=False):
	#print(text)

	if not len(text)>0: return

	etext = escape_single_quotes(text)
	tokens = shlex.split(etext)
	tokens = unescape_single_quotes(tokens)

	if len(tokens)==2:
		if tokens[0].lower()=="/whois":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.sendLine(f"WHOIS {target}")
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/whois":
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /whois NICKNAME" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /nick NICKNAME" )
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
				msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /part CHANNEL [MESSAGE]" )
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
			obj.gui.locked.append( [target,key]  )
			return
	if len(tokens)==2:
		if tokens[0].lower()=="/join":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.join(target)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/join":
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /join CHANNEL [KEY]" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /notice TARGET MESSAGE" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /msg TARGET MESSAGE" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	if len(tokens)>=2:
		if tokens[0].lower()=="/me":
			tokens.pop(0)	# remove command
			msg = ' '.join(tokens)
			if obj.gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if obj.gui.use_asciimojis: msg = inject_asciiemojis(msg)
			obj.client.describe(obj.name,msg)
			pmsg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["action"],obj.client.nickname+" "+msg )
			obj.gui.writeToChannel(obj.client,obj.name,pmsg)
			obj.gui.writeToChannelLog(obj.client,obj.name,GLYPH_ACTION+obj.client.nickname,msg)
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/me":
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /me MESSAGE" )
			obj.gui.writeToChannel(obj.client,obj.name,msg)
			return

	# Inject emojis
	if obj.gui.use_emojis:
		text = emoji.emojize(text,use_aliases=True)

	# Inject ASCIImojis
	if obj.gui.use_asciimojis:
		text = inject_asciiemojis(text)

	obj.client.msg(obj.name,text)

	msg = render_message(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["self"],obj.client.nickname,obj.gui.styles["message"],text )
	obj.gui.writeToChannel(obj.client,obj.name,msg)
	obj.gui.writeToChannelLog(obj.client,obj.name,GLYPH_SELF+obj.client.nickname,text)

def handle_console_input(obj,text):
	
	# Handle any commands here
	etext = escape_single_quotes(text)
	tokens = shlex.split(etext)
	tokens = unescape_single_quotes(tokens)

	if len(tokens)==2:
		if tokens[0].lower()=="/whois":
			tokens.pop(0)	# remove command
			target = tokens.pop(0)
			obj.client.sendLine(f"WHOIS {target}")
			return
	if len(tokens)==1:
		if tokens[0].lower()=="/whois":
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /whois NICKNAME" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /nick NICKNAME" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /part CHANNEL [MESSAGE]" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /join CHANNEL [KEY]" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /notice TARGET MESSAGE" )
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
			msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Usage: /msg TARGET MESSAGE" )
			obj.gui.writeToConsole(obj.client,msg)
			return

	# No valid command detected
	msg = render_system(obj.gui, obj.gui.styles["timestamp"],obj.gui.styles["system"],"Unrecognized command: \""+text+"\"" )
	obj.gui.writeToConsole(obj.client,msg)
	return
