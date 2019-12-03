
import html

import emoji

import erk.events
from erk.config import *
from erk.format import *
from erk.strings import *

def channel_window_input(gui,client,window,text):

	if len(text.strip())==0: return

	tokens = text.split()

	KNOCK = gui.does_server_support_knock(client)

	# /knock
	if KNOCK:
		if len(tokens)>0:
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)<2:
				window.writeLog(ERROR_MESSAGE,'',KNOCK_COMMAND_HELP)
				return
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)==2:
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				client.sendLine("KNOCK "+channel)
				return
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)>=3:
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("KNOCK "+channel+" "+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==KNOCK_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("KNOCK"))
				return

	# /userhost
	if len(tokens)>0:
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',USERHOST_COMMAND_HELP)
			return
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)>6:
			window.writeLog(ERROR_MESSAGE,'',USERHOST_COMMAND_HELP)
			return
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)<=6:
			tokens.pop(0)	# Remove command
			client.sendLine("USERHOST "+' '.join(tokens))
			return

	# /time
	if len(tokens)>0:
		if tokens[0].lower()==TIME_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',TIME_COMMAND_HELP)
			return
		if tokens[0].lower()==TIME_COMMAND and len(tokens)==2:
			client.sendLine("TIME "+tokens[1])
			return
		if tokens[0].lower()==TIME_COMMAND and len(tokens)==1:
			client.sendLine("TIME")
			return

	CNOTICE = gui.does_server_support_cnotice(client)
	CPRIVMSG = gui.does_server_support_cprivmsg(client)

	if CPRIVMSG:
		if len(tokens)>0:
			if tokens[0].lower()==CPRIVMSG_COMMAND and len(tokens)<4:
				window.writeLog(ERROR_MESSAGE,'',CPRIVMSG_COMMAND_HELP)
				return
			if tokens[0].lower()==CPRIVMSG_COMMAND and len(tokens)>=4:
				tokens.pop(0)	# Remove command
				nickname = tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("CPRIVMSG "+nickname+" "+channel+" :"+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==CPRIVMSG_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("CPRIVMSG"))
				return

	if CNOTICE:
		if len(tokens)>0:
			if tokens[0].lower()==CNOTICE_COMMAND and len(tokens)<4:
				window.writeLog(ERROR_MESSAGE,'',CNOTICE_COMMAND_HELP)
				return
			if tokens[0].lower()==CNOTICE_COMMAND and len(tokens)>=4:
				tokens.pop(0)	# Remove command
				nickname = tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("CNOTICE "+nickname+" "+channel+" :"+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==CNOTICE_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("CNOTICE"))
				return

	# /unignore
	if len(tokens)>0:
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',UNIGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',UNIGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			gui.remove_ignore(client,user)
			return

	# /ignore
	if len(tokens)>0:
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',IGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',IGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			gui.add_ignore(client,user)
			return

	# /oper
	if len(tokens)>0:
		if tokens[0].lower()==OPER_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',OPER_COMMAND_HELP)
			return
		if tokens[0].lower()==OPER_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',OPER_COMMAND_HELP)
			return
		if tokens[0].lower()==OPER_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			password = tokens.pop(0)
			client.sendLine("OPER "+user+" "+password)
			return

	# /invite
	if len(tokens)>0:
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',INVITE_COMMAND_HELP)
			return
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',INVITE_COMMAND_HELP)
			return
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			channel = tokens.pop(0)
			client.invite(user,channel)
			return

	# /whois
	if len(tokens)>0:
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==1:
			window.writeLog(ERROR_MESSAGE,'',WHOIS_COMMAND_HELP)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',WHOIS_COMMAND_HELP)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			client.sendLine("WHOIS "+target)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			server = tokens.pop(0)
			client.sendLine("WHOIS "+target+" "+server)
			return

	# /away
	if len(tokens)>0:
		if tokens[0].lower()==AWAY_COMMAND and len(tokens)==1:
			client.away(AWAY_COMMAND_DEFAULT_MESSAGE)
			return
		if tokens[0].lower()==AWAY_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			client.away(msg)
			return

	# /back
	if len(tokens)>0:
		if tokens[0].lower()==BACK_COMMAND and len(tokens)==1:
			client.back()
			return
		if tokens[0].lower()==BACK_COMMAND and len(tokens)>1:
			window.writeLog(ERROR_MESSAGE,'',BACK_COMMAND_HELP)
			return

	# /topic
	if len(tokens)>0:
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)==1:
			window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_HELP)
			return
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)==2:
			client.topic(window.name,tokens[1])
			return
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)>2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# no channel argument
				tokens.pop(0)	# Remove command
				msg = ' '.join(tokens)
				client.topic(window.name,msg)
				return
			else:
				# channel argument
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.topic(channel,msg)
				return

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
			window.writeLog(ERROR_MESSAGE,'',JOIN_COMMAND_HELP)
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
			msg = html.escape(msg)
			erk.events.outgoing_message(gui,client,target,msg)
			return
		if tokens[0].lower()==MSG_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',MSG_COMMAND_HELP)
			return

	# /nick
	if len(tokens)>0:
		if tokens[0].lower()==NICK_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			client.setNick(tokens.pop(0))
			return
		if tokens[0].lower()==NICK_COMMAND and len(tokens)!=2:
			window.writeLog(ERROR_MESSAGE,'',NICK_COMMAND_HELP)
			return

	# /me
	if len(tokens)>0:
		if tokens[0].lower()==ME_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
			if gui.use_asciimojis: msg = inject_asciiemojis(msg)
			client.describe(window.name,msg)
			msg = html.escape(msg)
			erk.events.outgoing_action_message(gui,client,window.name,msg)
			return
		if tokens[0].lower()==ME_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',ME_COMMAND_HELP)
			return

	if gui.use_emojis: text = emoji.emojize(text,use_aliases=True)
	if gui.use_asciimojis: text = inject_asciiemojis(text)

	client.msg(window.name,text)

	text = html.escape(text)

	erk.events.outgoing_message(gui,client,window.name,text)

def private_window_input(gui,client,window,text):

	if len(text.strip())==0: return

	tokens = text.split()

	KNOCK = gui.does_server_support_knock(client)

	# /knock
	if KNOCK:
		if len(tokens)>0:
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)<2:
				window.writeLog(ERROR_MESSAGE,'',KNOCK_COMMAND_HELP)
				return
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)==2:
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				client.sendLine("KNOCK "+channel)
				return
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)>=3:
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("KNOCK "+channel+" "+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==KNOCK_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("KNOCK"))
				return

	# /userhost
	if len(tokens)>0:
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',USERHOST_COMMAND_HELP)
			return
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)>6:
			window.writeLog(ERROR_MESSAGE,'',USERHOST_COMMAND_HELP)
			return
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)<=6:
			tokens.pop(0)	# Remove command
			client.sendLine("USERHOST "+' '.join(tokens))
			return

	# /time
	if len(tokens)>0:
		if tokens[0].lower()==TIME_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',TIME_COMMAND_HELP)
			return
		if tokens[0].lower()==TIME_COMMAND and len(tokens)==2:
			client.sendLine("TIME "+tokens[1])
			return
		if tokens[0].lower()==TIME_COMMAND and len(tokens)==1:
			client.sendLine("TIME")
			return

	CNOTICE = gui.does_server_support_cnotice(client)
	CPRIVMSG = gui.does_server_support_cprivmsg(client)

	if CPRIVMSG:
		if len(tokens)>0:
			if tokens[0].lower()==CPRIVMSG_COMMAND and len(tokens)<4:
				window.writeLog(ERROR_MESSAGE,'',CPRIVMSG_COMMAND_HELP)
				return
			if tokens[0].lower()==CPRIVMSG_COMMAND and len(tokens)>=4:
				tokens.pop(0)	# Remove command
				nickname = tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("CPRIVMSG "+nickname+" "+channel+" :"+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==CPRIVMSG_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("CPRIVMSG"))
				return

	if CNOTICE:
		if len(tokens)>0:
			if tokens[0].lower()==CNOTICE_COMMAND and len(tokens)<4:
				window.writeLog(ERROR_MESSAGE,'',CNOTICE_COMMAND_HELP)
				return
			if tokens[0].lower()==CNOTICE_COMMAND and len(tokens)>=4:
				tokens.pop(0)	# Remove command
				nickname = tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("CNOTICE "+nickname+" "+channel+" :"+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==CNOTICE_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("CNOTICE"))
				return

	# /unignore
	if len(tokens)>0:
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',UNIGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',UNIGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			gui.remove_ignore(client,user)
			return

	# /ignore
	if len(tokens)>0:
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',IGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',IGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			gui.add_ignore(client,user)
			return

	# /oper
	if len(tokens)>0:
		if tokens[0].lower()==OPER_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',OPER_COMMAND_HELP)
			return
		if tokens[0].lower()==OPER_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',OPER_COMMAND_HELP)
			return
		if tokens[0].lower()==OPER_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			password = tokens.pop(0)
			client.sendLine("OPER "+user+" "+password)
			return

	# /invite
	if len(tokens)>0:
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',INVITE_COMMAND_HELP)
			return
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',INVITE_COMMAND_HELP)
			return
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			channel = tokens.pop(0)
			client.invite(user,channel)
			return

	# /whois
	if len(tokens)>0:
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==1:
			window.writeLog(ERROR_MESSAGE,'',WHOIS_COMMAND_HELP)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',WHOIS_COMMAND_HELP)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			client.sendLine("WHOIS "+target)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			server = tokens.pop(0)
			client.sendLine("WHOIS "+target+" "+server)
			return

	# /away
	if len(tokens)>0:
		if tokens[0].lower()==AWAY_COMMAND and len(tokens)==1:
			client.away(AWAY_COMMAND_DEFAULT_MESSAGE)
			return
		if tokens[0].lower()==AWAY_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			client.away(msg)
			return

	# /back
	if len(tokens)>0:
		if tokens[0].lower()==BACK_COMMAND and len(tokens)==1:
			client.back()
			return
		if tokens[0].lower()==BACK_COMMAND and len(tokens)>1:
			window.writeLog(ERROR_MESSAGE,'',BACK_COMMAND_HELP)
			return

	# /topic
	if len(tokens)>0:
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)==1:
			window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_PRIVATE_HELP)
			return
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)==2:
			window.writeLog(ERROR_MESSAGE,'',PRIVATE_TOPIC_ERROR)
			window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_PRIVATE_HELP)
			return
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)>2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# no channel argument
				window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_NOT_CHANNEL_ERROR.format(tokens[1]))
				window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_PRIVATE_HELP)
				return
			else:
				# channel argument
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.topic(channel,msg)
				return

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
			window.writeLog(ERROR_MESSAGE,'',PART_COMMAND_HELP)
			return
		if tokens[0].lower()==PART_COMMAND and len(tokens)>=2:
			if len(tokens[1])>0:
				if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
					# no channel passed as argument
					window.writeLog(ERROR_MESSAGE,'',PART_COMMAND_HELP)
					return
				else:
					# channel passed as argument
					tokens.pop(0)	# Remove command
					channel = tokens.pop(0)
					if len(tokens)>0:
						msg = ' '.join(tokens)
						if gui.use_emojis: msg = emoji.emojize(msg,use_aliases=True)
						if gui.use_asciimojis: msg = inject_asciiemojis(msg)
						msg = html.escape(msg)
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
			window.writeLog(ERROR_MESSAGE,'',JOIN_COMMAND_HELP)
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
			msg = html.escape(msg)
			erk.events.outgoing_message(gui,client,target,msg)
			return
		if tokens[0].lower()==MSG_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',MSG_COMMAND_HELP)
			return

	# /nick
	if len(tokens)>0:
		if tokens[0].lower()==NICK_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			client.setNick(tokens.pop(0))
			return
		if tokens[0].lower()==NICK_COMMAND and len(tokens)!=2:
			window.writeLog(ERROR_MESSAGE,'',NICK_COMMAND_HELP)
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
			window.writeLog(ERROR_MESSAGE,'',ME_COMMAND_HELP)
			return

	if gui.use_emojis: text = emoji.emojize(text,use_aliases=True)
	if gui.use_asciimojis: text = inject_asciiemojis(text)

	client.msg(window.name,text)

	text = html.escape(text)

	erk.events.outgoing_message(gui,client,window.name,text)

def server_window_input(gui,client,window,text):

	if len(text.strip())==0: return

	tokens = text.split()

	KNOCK = gui.does_server_support_knock(client)

	# /knock
	if KNOCK:
		if len(tokens)>0:
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)<2:
				window.writeLog(ERROR_MESSAGE,'',KNOCK_COMMAND_HELP)
				return
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)==2:
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				client.sendLine("KNOCK "+channel)
				return
			if tokens[0].lower()==KNOCK_COMMAND and len(tokens)>=3:
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("KNOCK "+channel+" "+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==KNOCK_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("KNOCK"))
				return

	# /userhost
	if len(tokens)>0:
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',USERHOST_COMMAND_HELP)
			return
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)>6:
			window.writeLog(ERROR_MESSAGE,'',USERHOST_COMMAND_HELP)
			return
		if tokens[0].lower()==USERHOST_COMMAND and len(tokens)<=6:
			tokens.pop(0)	# Remove command
			client.sendLine("USERHOST "+' '.join(tokens))
			return

	# /time
	if len(tokens)>0:
		if tokens[0].lower()==TIME_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',TIME_COMMAND_HELP)
			return
		if tokens[0].lower()==TIME_COMMAND and len(tokens)==2:
			client.sendLine("TIME "+tokens[1])
			return
		if tokens[0].lower()==TIME_COMMAND and len(tokens)==1:
			client.sendLine("TIME")
			return

	CNOTICE = gui.does_server_support_cnotice(client)
	CPRIVMSG = gui.does_server_support_cprivmsg(client)

	if CPRIVMSG:
		if len(tokens)>0:
			if tokens[0].lower()==CPRIVMSG_COMMAND and len(tokens)<4:
				window.writeLog(ERROR_MESSAGE,'',CPRIVMSG_COMMAND_HELP)
				return
			if tokens[0].lower()==CPRIVMSG_COMMAND and len(tokens)>=4:
				tokens.pop(0)	# Remove command
				nickname = tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("CPRIVMSG "+nickname+" "+channel+" :"+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==CPRIVMSG_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("CPRIVMSG"))
				return

	if CNOTICE:
		if len(tokens)>0:
			if tokens[0].lower()==CNOTICE_COMMAND and len(tokens)<4:
				window.writeLog(ERROR_MESSAGE,'',CNOTICE_COMMAND_HELP)
				return
			if tokens[0].lower()==CNOTICE_COMMAND and len(tokens)>=4:
				tokens.pop(0)	# Remove command
				nickname = tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.sendLine("CNOTICE "+nickname+" "+channel+" :"+msg)
				return
	else:
		if len(tokens)>0:
			if tokens[0].lower()==CNOTICE_COMMAND:
				window.writeLog(ERROR_MESSAGE,'',CPRIV_CNOTICE_NOT_SUPPORTED.format("CNOTICE"))
				return

	# /unignore
	if len(tokens)>0:
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',UNIGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',UNIGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==UNIGNORE_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			gui.remove_ignore(client,user)
			return

	# /ignore
	if len(tokens)>0:
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',IGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)>2:
			window.writeLog(ERROR_MESSAGE,'',IGNORE_COMMAND_HELP)
			return
		if tokens[0].lower()==IGNORE_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			gui.add_ignore(client,user)
			return

	# /oper
	if len(tokens)>0:
		if tokens[0].lower()==OPER_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',OPER_COMMAND_HELP)
			return
		if tokens[0].lower()==OPER_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',OPER_COMMAND_HELP)
			return
		if tokens[0].lower()==OPER_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			password = tokens.pop(0)
			client.sendLine("OPER "+user+" "+password)
			return

	# /invite
	if len(tokens)>0:
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',INVITE_COMMAND_HELP)
			return
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',INVITE_COMMAND_HELP)
			return
		if tokens[0].lower()==INVITE_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			user = tokens.pop(0)
			channel = tokens.pop(0)
			client.invite(user,channel)
			return

	# /whois
	if len(tokens)>0:
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==1:
			window.writeLog(ERROR_MESSAGE,'',WHOIS_COMMAND_HELP)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)>3:
			window.writeLog(ERROR_MESSAGE,'',WHOIS_COMMAND_HELP)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			client.sendLine("WHOIS "+target)
			return
		if tokens[0].lower()==WHOIS_COMMAND and len(tokens)==3:
			tokens.pop(0)	# Remove command
			target = tokens.pop(0)
			server = tokens.pop(0)
			client.sendLine("WHOIS "+target+" "+server)
			return

	# /away
	if len(tokens)>0:
		if tokens[0].lower()==AWAY_COMMAND and len(tokens)==1:
			client.away(AWAY_COMMAND_DEFAULT_MESSAGE)
			return
		if tokens[0].lower()==AWAY_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			client.away(msg)
			return

	# /back
	if len(tokens)>0:
		if tokens[0].lower()==BACK_COMMAND and len(tokens)==1:
			client.back()
			return
		if tokens[0].lower()==BACK_COMMAND and len(tokens)>1:
			window.writeLog(ERROR_MESSAGE,'',BACK_COMMAND_HELP)
			return

	# /topic
	if len(tokens)>0:
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)==1:
			window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_PRIVATE_HELP)
			return
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)==2:
			window.writeLog(ERROR_MESSAGE,'',CONSOLE_TOPIC_ERROR)
			window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_PRIVATE_HELP)
			return
		if tokens[0].lower()==TOPIC_COMMAND and len(tokens)>2:
			if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
				# no channel argument
				window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_NOT_CHANNEL_ERROR.format(tokens[1]))
				window.writeLog(ERROR_MESSAGE,'',TOPIC_COMMAND_PRIVATE_HELP)
				return
			else:
				# channel argument
				tokens.pop(0)	# Remove command
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				client.topic(channel,msg)
				return

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
			window.writeLog(ERROR_MESSAGE,'',PART_COMMAND_HELP)
			return
		if tokens[0].lower()==PART_COMMAND and len(tokens)>=2:
			if len(tokens[1])>0:
				if tokens[1][:1]!='#' and tokens[1][:1]!='&' and tokens[1][:1]!='!' and tokens[1][:1]!='+':
					# no channel passed as argument
					window.writeLog(ERROR_MESSAGE,'',PART_COMMAND_HELP)
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
			window.writeLog(ERROR_MESSAGE,'',JOIN_COMMAND_HELP)
			return

	# /send
	if len(tokens)>0:
		if tokens[0].lower()==SEND_COMMAND and len(tokens)>=2:
			tokens.pop(0)	# Remove command
			msg = ' '.join(tokens)
			client.sendLine(msg)
			return
		if tokens[0].lower()==SEND_COMMAND and len(tokens)<2:
			window.writeLog(ERROR_MESSAGE,'',SEND_COMMAND_HELP)
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
			msg = html.escape(msg)
			erk.events.outgoing_message(gui,client,target,msg)
			return
		if tokens[0].lower()==MSG_COMMAND and len(tokens)<3:
			window.writeLog(ERROR_MESSAGE,'',MSG_COMMAND_HELP)
			return

	# /nick
	if len(tokens)>0:
		if tokens[0].lower()==NICK_COMMAND and len(tokens)==2:
			tokens.pop(0)	# Remove command
			client.setNick(tokens.pop(0))
			return
		if tokens[0].lower()==NICK_COMMAND and len(tokens)!=2:
			window.writeLog(ERROR_MESSAGE,'',NICK_COMMAND_HELP)
			return