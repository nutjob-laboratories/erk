
import sys
import os

DEFAULT_NICKNAME = "erk_user"
DEFAULT_USERNAME = "erk"
DEFAULT_IRCNAME = "Erk IRC Client"
DEFAULT_ALTERNATIVE = "erk_user_1"

CONSOLE_COMMANDS = {
	"/away":"/away ",
	"/back": "/back",
	"/join": "/join ",
	"/part": "/part ",
	"/msg": "/msg ",
	"/nick": "/nick ",
	"/send": "/send ",
	"/quit": "/quit",
	"/whois": "/whois ",
	"/invite": "/invite ",
	"/oper": "/oper ",
	"/ignore": "/ignore ",
	"/unignore": "/unignore ",
}

INPUT_COMMANDS = {
	"/away":"/away ",
	"/back": "/back",
	"/topic": "/topic ",
	"/join": "/join ",
	"/part": "/part ",
	"/msg": "/msg ",
	"/nick": "/nick ",
	"/me": "/me ",
	"/quit": "/quit",
	"/whois": "/whois ",
	"/invite": "/invite ",
	"/oper": "/oper ",
	"/ignore": "/ignore ",
	"/unignore": "/unignore ",
}


def get_style_attribute(style,setting):

	for e in style.split(';'):
		e = e.strip()
		p = e.split(':')
		if len(p)==2:
			p[0] = p[0].strip()
			p[1] = p[1].strip()

			if p[0].lower()==setting.lower():
				return p[1]
	return None

def restart_program():
	python = sys.executable
	os.execl(python, python, * sys.argv)

def convertSeconds(seconds):
	h = seconds//(60*60)
	m = (seconds-h*60*60)//60
	s = seconds-(h*60*60)-(m*60)
	return [h, m, s]

def prettyUptime(uptime):
	t = convertSeconds(uptime)
	hours = t[0]
	if len(str(hours))==1: hours = f"0{hours}"
	minutes = t[1]
	if len(str(minutes))==1: minutes = f"0{minutes}"
	seconds = t[2]
	if len(str(seconds))==1: seconds = f"0{seconds}"
	return f"{hours}:{minutes}:{seconds}"

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

# Written by Chase Seibert: https://chase-seibert.github.io/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html
# use negative offset to darken, positive offset to brighten
def color_variant(hex_color, brightness_offset=1):
	""" takes a color like #87c95f and produces a lighter or darker variant """
	if len(hex_color) != 7:
		raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
	rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
	new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
	new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
	# hex() produces "0x88", we want just "88"
	return "#" + "".join([hex(i)[2:] for i in new_rgb_int])