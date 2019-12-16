
import sys
import os
import json
import re
from collections import defaultdict
import string
import random

from erk.strings import *
from erk.objects import *

# Application directories
INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")
AUTOCOMPLETE_DIRECTORY = os.path.join(DATA_DIRECTORY, "autocomplete")

# Configuration directories
SETTINGS_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "settings")
if not os.path.isdir(SETTINGS_DIRECTORY): os.mkdir(SETTINGS_DIRECTORY)

# Log directory
LOG_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "logs")
if not os.path.isdir(LOG_DIRECTORY): os.mkdir(LOG_DIRECTORY)

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
			"history": [],
			"save_history": False,
		}
		return si

def save_user(user,filename=USER_FILE):
	with open(filename, "w") as write_data:
		json.dump(user, write_data, indent=4, sort_keys=True)

def write_style_file(style,filename=STYLE_FILE):
	output = "/*\n\tThis file uses a sub-set of CSS used by Qt called \"QSS\"\n\thttps://doc.qt.io/qt-5/stylesheet-syntax.html\n*/\n\n"

	for key in style:
		output = output + key + " {\n"
		for s in style[key].split(';'):
			s = s.strip()
			if len(s)==0: continue
			output = output + "\t" + s + ";\n"
		output = output + "}\n\n"

	f=open(filename, "w")
	f.write(output)
	f.close()

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

# Converts an array of Message() objects to an array of arrays
def log_to_array(log):
	out = []
	for l in log:
		entry = [ l.timestamp,l.type,l.sender,l.contents ]
		out.append(entry)
	return out

# Converts an array of arrays to an array of Message Objects
def array_to_log(log):
	out = []
	for l in log:
		m = Message(l[1],l[2],l[3],l[0])
		out.append(m)
	return out

def trimLog(ilog,maxsize):
	count = 0
	shortlog = []
	for line in reversed(ilog):
		count = count + 1
		shortlog.append(line)
		if count >= maxsize:
			break
	return list(reversed(shortlog))

def encodeLogName(network,name=None):
	network = network.replace(":","-")
	if name==None:
		return f"{network}.json"
	else:
		return f"{network}-{name}.json"

# Takes an array of Message() objects, converts it to
# an AoA, and appens the AoA to a file containing
# AoAs on disk
def saveLog(network,name,logs):
	f = encodeLogName(network,name)
	logfile = os.path.join(LOG_DIRECTORY,f)

	logs = log_to_array(logs)

	slog = loadLog(network,name)
	for e in logs:
		slog.append(e)

	with open(logfile, "w") as writelog:
		json.dump(slog, writelog, indent=4, sort_keys=True)

# Loads an AoA from disk and returns it
def loadLog(network,name):
	f = encodeLogName(network,name)
	logfile = os.path.join(LOG_DIRECTORY,f)

	if os.path.isfile(logfile):
		with open(logfile, "r") as logentries:
			data = json.load(logentries)
			return data
	else:
		return []

# Loads an AoA from disk, converts it to an arroy
# of Message() objects, and returns it
def readLog(network,name):
	logs = loadLog(network,name)
	logs = array_to_log(logs)
	return logs