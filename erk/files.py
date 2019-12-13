
import sys
import os
import json
import re
from collections import defaultdict
import string
import random

from erk.strings import *

# Application directories
INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")
AUTOCOMPLETE_DIRECTORY = os.path.join(DATA_DIRECTORY, "autocomplete")

# Configuration directories
SETTINGS_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "settings")
if not os.path.isdir(SETTINGS_DIRECTORY): os.mkdir(SETTINGS_DIRECTORY)

# Configuration files
USER_FILE = os.path.join(SETTINGS_DIRECTORY, "user.json")
STYLE_FILE = os.path.join(SETTINGS_DIRECTORY, "text.css")
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "settings.json")

NETWORK_FILE = os.path.join(DATA_DIRECTORY, "servers.txt")
BACKUP_STYLE_FILE = os.path.join(DATA_DIRECTORY, "text.css")
ASCIIEMOJI_LIST = os.path.join(DATA_DIRECTORY, "asciiemoji.json")
PROFANITY_LIST = os.path.join(DATA_DIRECTORY, "profanity.txt")
ASCIIMOJI_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "asciimoji.txt")
EMOJI_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji2.txt")
EMOJI_ALIAS_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji1.txt")

# Read in the ascii emoji list
ASCIIEMOJIS = {}
with open(ASCIIEMOJI_LIST, "r",encoding="utf-8") as read_emojis:
	ASCIIEMOJIS = json.load(read_emojis)

# Load in the profanity data file
f = open(PROFANITY_LIST,"r")
cursewords = f.read()
f.close()

PROFANITY = cursewords.split("\n")
PROFANITY_SYMBOLS = ["#","!","@","&","%","$","?","+","*"]

def censorWord(word,punc=True):
	result = ''
	last = '+'
	for letter in word:
		if punc:
			random.shuffle(PROFANITY_SYMBOLS)		
			nl = random.choice(PROFANITY_SYMBOLS)
			while nl == last:
				nl = random.choice(PROFANITY_SYMBOLS)
			last = nl
			result = result + nl
		else:
			result = result + "*"
	return result

def filterProfanityFromText(text,punc=True):
	clean = []
	for word in text.split(' '):
		nopunc = word.translate(str.maketrans("","", string.punctuation))
		if nopunc in PROFANITY:
			word = censorWord(word,punc)
		clean.append(word)
	return ' '.join(clean)

def inject_asciiemojis(data):
	for key in ASCIIEMOJIS:
		for word in ASCIIEMOJIS[key]["words"]:
			data = data.replace("("+word+")",ASCIIEMOJIS[key]["ascii"])
	return data

def load_asciimoji_autocomplete():
	ASCIIMOJI_AUTOCOMPLETE = []
	with open(ASCIIMOJI_AUTOCOMPLETE_FILE) as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			ASCIIMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	return ASCIIMOJI_AUTOCOMPLETE

def load_emoji_autocomplete():
	EMOJI_AUTOCOMPLETE = []
	with open(EMOJI_ALIAS_AUTOCOMPLETE_FILE) as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			EMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	with open(EMOJI_AUTOCOMPLETE_FILE) as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			EMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	return EMOJI_AUTOCOMPLETE

ASCIIMOJI_AUTOCOMPLETE = load_asciimoji_autocomplete()
EMOJI_AUTOCOMPLETE = load_emoji_autocomplete()

def get_text_format_settings(filename=STYLE_FILE):
	if os.path.isfile(filename):
		data = read_style_file(filename)
		return data
	else:
		data = read_style_file(BACKUP_STYLE_FILE)
		return data

def get_network_list(filename=NETWORK_FILE):
	servlist = []
	with open(NETWORK_FILE) as fp:
		line = fp.readline()
		line=line.strip()
		while line:
			line=line.strip()
			p = line.split(':')
			servlist.append(p)
			line = fp.readline()
	return servlist

def get_user(filename=USER_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_user:
			data = json.load(read_user)
			return data
	else:
		si = {
			"nickname": DEFAULT_NICKNAME,
			"username": DEFAULT_USERNAME,
			"realname": DEFAULT_IRCNAME,
			"alternate": DEFAULT_ALTERNATIVE,
			"last_server": '',
			"last_port": "6667",
			"last_password": '',
			"channels": [],
			"ssl": False,
			"reconnect": False,
			"autojoin": False,
		}
		return si

def save_user(user,filename=USER_FILE):
	with open(filename, "w") as write_data:
		json.dump(user, write_data, indent=4, sort_keys=True)

def read_style_file(filename=STYLE_FILE):

	# Read in the file
	f=open(filename, "r")
	text = f.read()
	f.close()

	# Strip comments
	text = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,text)

	# Tokenize the file
	buff = ''
	name = ''
	tokens = []
	inblock = False
	for char in text:
		if char=='{':
			if inblock:
				raise SyntaxError("Nested styles are forbidden")
			inblock = True
			name = buff.strip()
			buff = ''
			continue

		if char=='}':
			inblock = False
			section = [ name,buff.strip() ]
			tokens.append(section)
			buff = ''
			continue

		buff = buff + char

	# Check for an unclosed brace
	if inblock:
		raise SyntaxError("Unclosed brace")

	# Build output dict of lists
	style = defaultdict(list)
	for section in tokens:
		name = section[0]
		entry = []
		for l in section[1].split(";"):
			l = l.strip()
			if len(l)>0:
				entry.append(l)

		if name in style:
			raise SyntaxError("Styles can only be defined once")
		else:
			if len(entry)!=0:
				comp = "; ".join(entry) + ";"
				style[name] = comp
			else:
				style[name] = ''

	# Return the dict
	return style