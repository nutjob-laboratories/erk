


import emoji

import erk.events
from erk.config import *
from erk.format import *
from erk.strings import *

def channel_window_input(gui,client,window,text):

	if len(text.strip())==0: return

	tokens = text.split()

	# /quit
	if len(tokens)>0:
		if tokens[0].lower()==QUIT_COMMAND and len(tokens)==1:
			client.quit()
			return
		if tokens[0].lower()==QUIT_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.quit(msg)
			return

	# /part
	if len(tokens)>0:
		if tokens[0].lower()==PART_COMMAND and len(tokens)==1:
			erk.events.erk_close_channel(gui,client,window.name)
			return
		if tokens[0].lower()==PART_COMMAND and len(tokens)>=2:
			if len(tokens[1])>0:
				if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
					# no channel passed as argument
					tokens.pop(0)	# Remove command
					msg = ' '.join(tokens)
					if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
					if gui.use_asciimojis: msg = inject_asciiemojis(msg)
					erk.events.erk_close_channel(gui,client,window.name,msg)
					return
				else:
					# channel passed as argument
					tokens.pop(0)	# Remove command
					channel = tokens.pop(0)
					if len(tokens)>0:
						msg = ' '.join(tokens)
						if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
						if gui.use_asciimojis: msg = inject_asciiemojis(msg)
						erk.events.erk_close_channel(gui,client,channel,msg)
						return
					else:
						erk.events.erk_close_channel(gui,client,channel)
						return

	# /join
	if len(tokens)>0:
		if tokens[0].lower()==JOIN_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			key = tokens.pop(0)
			client.join(target,key)
			return
		if tokens[0].lower()==JOIN_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			client.join(target)
			return
		if tokens[0].lower()==JOIN_COMMAND and (len(tokens)<2 or len(tokens)>3):
			window.writeLog(SYSTEM_MESSAGE,'',JOIN_COMMAND_HELP)
			return

	# /msg
	if len(tokens)>0:
		if tokens[0].lower()==MSG_COMMAND and len(tokens)>=3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.msg(target,msg)
			erk.events.outgoing_message(gui,client,target,msg)
			return
		if tokens[0].lower()==MSG_COMMAND and len(tokens)<3:
			window.writeLog(SYSTEM_MESSAGE,'',MSG_COMMAND_HELP)
			return

	# /nick
	if len(tokens)>0:
		if tokens[0].lower()==NICK_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			client.setNick(tokens.pop(0))
			return
		if tokens[0].lower()==NICK_COMMAND and len(tokens)!=2:
			window.writeLog(SYSTEM_MESSAGE,'',NICK_COMMAND_HELP)
			return

	# /me
	if len(tokens)>0:
		if tokens[0].lower()==ME_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.describe(window.name,msg)
			erk.events.outgoing_action_message(gui,client,window.name,msg)
			return
		if tokens[0].lower()==ME_COMMAND and len(tokens)<2:
			window.writeLog(SYSTEM_MESSAGE,'',ME_COMMAND_HELP)
			return

	if gui.use_emojis: text = emoji.emojize(text,use_aliases=True)
	if gui.use_asciimojis: text = inject_asciiemojis(text)

	client.msg(window.name,text)

	erk.events.outgoing_message(gui,client,window.name,text)

def private_window_input(gui,client,window,text):

	if len(text.strip())==0: return

	tokens = text.split()

	# /quit
	if len(tokens)>0:
		if tokens[0].lower()==QUIT_COMMAND and len(tokens)==1:
			client.quit()
			return
		if tokens[0].lower()==QUIT_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.quit(msg)
			return

	# /part
	if len(tokens)>0:
		if tokens[0].lower()==PART_COMMAND and len(tokens)==1:
			window.writeLog(SYSTEM_MESSAGE,'',PART_COMMAND_HELP)
			return
		if tokens[0].lower()==PART_COMMAND and len(tokens)>=2:
			if len(tokens[1])>0:
				if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
					# no channel passed as argument
					window.writeLog(SYSTEM_MESSAGE,'',PART_COMMAND_HELP)
					return
				else:
					# channel passed as argument
					tokens.pop(0)	# Remove command
					channel = tokens.pop(0)
					if len(tokens)>0:
						msg = ' '.join(tokens)
						if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
						if gui.use_asciimojis: msg = inject_asciiemojis(msg)
						erk.events.erk_close_channel(gui,client,channel,msg)
						return
					else:
						erk.events.erk_close_channel(gui,client,channel)
						return

	# /join
	if len(tokens)>0:
		if tokens[0].lower()==JOIN_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			key = tokens.pop(0)
			client.join(target,key)
			return
		if tokens[0].lower()==JOIN_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			client.join(target)
			return
		if tokens[0].lower()==JOIN_COMMAND and (len(tokens)<2 or len(tokens)>3):
			window.writeLog(SYSTEM_MESSAGE,'',JOIN_COMMAND_HELP)
			return

	# /msg
	if len(tokens)>0:
		if tokens[0].lower()==MSG_COMMAND and len(tokens)>=3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.msg(target,msg)
			erk.events.outgoing_message(gui,client,target,msg)
			return
		if tokens[0].lower()==MSG_COMMAND and len(tokens)<3:
			window.writeLog(SYSTEM_MESSAGE,'',MSG_COMMAND_HELP)
			return

	# /nick
	if len(tokens)>0:
		if tokens[0].lower()==NICK_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			client.setNick(tokens.pop(0))
			return
		if tokens[0].lower()==NICK_COMMAND and len(tokens)!=2:
			window.writeLog(SYSTEM_MESSAGE,'',NICK_COMMAND_HELP)
			return

	# /me
	if len(tokens)>0:
		if tokens[0].lower()==ME_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.describe(window.name,msg)
			erk.events.outgoing_action_message(gui,client,window.name,msg)
			return
		if tokens[0].lower()==ME_COMMAND and len(tokens)<2:
			window.writeLog(SYSTEM_MESSAGE,'',ME_COMMAND_HELP)
			return

	if gui.use_emojis: text = emoji.emojize(text,use_aliases=True)
	if gui.use_asciimojis: text = inject_asciiemojis(text)

	client.msg(window.name,text)

	erk.events.outgoing_message(gui,client,window.name,text)

def server_window_input(gui,client,window,text):

	if len(text.strip())==0: return

	tokens = text.split()

	# /quit
	if len(tokens)>0:
		if tokens[0].lower()==QUIT_COMMAND and len(tokens)==1:
			client.quit()
			return
		if tokens[0].lower()==QUIT_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.quit(msg)
			return

	# /part
	if len(tokens)>0:
		if tokens[0].lower()==PART_COMMAND and len(tokens)==1:
			window.writeLog(SYSTEM_MESSAGE,'',PART_COMMAND_HELP)
			return
		if tokens[0].lower()==PART_COMMAND and len(tokens)>=2:
			if len(tokens[1])>0:
				if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
					# no channel passed as argument
					window.writeLog(SYSTEM_MESSAGE,'',PART_COMMAND_HELP)
					return
				else:
					# channel passed as argument
					tokens.pop(0)	# Remove command
					channel = tokens.pop(0)
					if len(tokens)>0:
						msg = ' '.join(tokens)
						if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
						if gui.use_asciimojis: msg = inject_asciiemojis(msg)
						erk.events.erk_close_channel(gui,client,channel,msg)
						return
					else:
						erk.events.erk_close_channel(gui,client,channel)
						return

	# /join
	if len(tokens)>0:
		if tokens[0].lower()==JOIN_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			key = tokens.pop(0)
			client.join(target,key)
			return
		if tokens[0].lower()==JOIN_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			client.join(target)
			return
		if tokens[0].lower()==JOIN_COMMAND and (len(tokens)<2 or len(tokens)>3):
			window.writeLog(SYSTEM_MESSAGE,'',JOIN_COMMAND_HELP)
			return

	# /send
	if len(tokens)>0:
		if tokens[0].lower()==SEND_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			client.sendLine(msg)
			return
		if tokens[0].lower()==SEND_COMMAND and len(tokens)<2:
			window.writeLog(SYSTEM_MESSAGE,'',SEND_COMMAND_HELP)
			return

	# /msg
	if len(tokens)>0:
		if tokens[0].lower()==MSG_COMMAND and len(tokens)>=3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.msg(target,msg)
			erk.events.outgoing_message(gui,client,target,msg)
			return
		if tokens[0].lower()==MSG_COMMAND and len(tokens)<3:
			window.writeLog(SYSTEM_MESSAGE,'',MSG_COMMAND_HELP)
			return

	# /nick
	if len(tokens)>0:
		if tokens[0].lower()==NICK_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			client.setNick(tokens.pop(0))
			return
		if tokens[0].lower()==NICK_COMMAND and len(tokens)!=2:
			window.writeLog(SYSTEM_MESSAGE,'',NICK_COMMAND_HELP)
			return