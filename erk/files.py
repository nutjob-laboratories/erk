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

import sys
import os
import json
import re
from collections import defaultdict
import string
import random
from datetime import datetime
import zipfile

from .strings import *
from .objects import *

# File extensions
SCRIPT_FILE_EXTENSION = "erk"
STYLE_FILE_EXTENSION = "style"
PACKAGE_FILE_EXTENSION = "erkp"

# Application directories
INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
DATA_DIRECTORY = os.path.join(ERK_MODULE_DIRECTORY, "data")
AUTOCOMPLETE_DIRECTORY = os.path.join(DATA_DIRECTORY, "autocomplete")

# Configuration directories
SETTINGS_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "settings")
if not os.path.isdir(SETTINGS_DIRECTORY): os.mkdir(SETTINGS_DIRECTORY)

# Script directories
SCRIPTS_DIRECTORY = os.path.join(SETTINGS_DIRECTORY, "scripts")
if not os.path.isdir(SCRIPTS_DIRECTORY): os.mkdir(SCRIPTS_DIRECTORY)

# Script directories
STYLES_DIRECTORY = os.path.join(SETTINGS_DIRECTORY, "styles")
if not os.path.isdir(STYLES_DIRECTORY): os.mkdir(STYLES_DIRECTORY)

# Log directory
LOG_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "logs")
if not os.path.isdir(LOG_DIRECTORY): os.mkdir(LOG_DIRECTORY)

# Configuration files
USER_FILE = os.path.join(SETTINGS_DIRECTORY, "user.json")
STYLE_FILE = os.path.join(SETTINGS_DIRECTORY, "text."+STYLE_FILE_EXTENSION)
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "settings.json")

NETWORK_FILE = os.path.join(DATA_DIRECTORY, "servers.txt")
BACKUP_STYLE_FILE = os.path.join(DATA_DIRECTORY, "text."+STYLE_FILE_EXTENSION)

PROFANITY_LIST = os.path.join(DATA_DIRECTORY, "profanity.txt")
EMOJI_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji2.txt")
EMOJI_ALIAS_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji1.txt")


MACRO_SAVE_FILE = os.path.join(SETTINGS_DIRECTORY, "macros.json")


def get_list_of_installed_scripts(scriptdir):
	scripts = []
	for root, subdirs, files in os.walk(scriptdir):
		for filename in files:
			ext = os.path.splitext(filename)[-1].lower()
			if ext=='.erk':
				file_path = os.path.join(root, filename)
				f = os.path.splitext(filename)[0]
				scripts.append( [file_path,f] )

	return scripts


def save_macros(macros,filename=MACRO_SAVE_FILE):
	if filename==None: filename=MACRO_SAVE_FILE

	state = []
	for e in macros:
		entry = [e.name,e.argcount,e.command,e.args,e.help]
		state.append(entry)

	with open(filename, "w") as write_data:
		json.dump(state, write_data, indent=4, sort_keys=True)

def get_macros(filename=MACRO_SAVE_FILE):
	#if filename==None: filename=USER_FILE
	if os.path.isfile(filename):
		with open(filename, "r") as read_user:
			data = json.load(read_user)

			macros = []
			for e in data:
				m = Macro(e[0],e[1],e[2],e[3],e[4])
				macros.append(m)

			return macros
	return []

# Plugin template for the editor
PLUGIN_TEMPLATE_FILE = os.path.join(DATA_DIRECTORY, "plugin_template.txt")
PLUGIN_TEMPLATE = ''
f = open(PLUGIN_TEMPLATE_FILE,"r")
PLUGIN_TEMPLATE = f.read()
f.close()

# Load in the profanity data file
f = open(PROFANITY_LIST,"r")
cursewords = f.read()
f.close()

PROFANITY = cursewords.split("\n")
PROFANITY_SYMBOLS = ["#","!","@","&","%","$","?","+","*"]

PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")

# Opens up a zip file containing plugins, and reads the
# package.txt from each included plugin, and returns an
# array containing the plugin(s) info
def get_plugin_info(file):
	plugins = []
	arc = zipfile.ZipFile(file)
	for f in arc.namelist():
		if os.path.basename(f)=="package.txt":
			if not os.path.isdir(f):
				pn = arc.read(f)
				plugins.append(pn.decode())
		if os.path.basename(f)==f:
			fn,ext = os.path.splitext(f)
			if ext.lower()==".py":
				plugins.append(f)
	return plugins

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

AUTO_SCRIPT_CACHE = {}

def delete_custom_style(network,name,styledir=STYLES_DIRECTORY):
	f = encodeStyleName(network,name)
	styleFileName = os.path.join(styledir,f)

	if os.path.isfile(styleFileName):
		os.remove(styleFileName)

def save_custom_style(network,name,style,styledir=STYLES_DIRECTORY):
	f = encodeStyleName(network,name)
	styleFileName = os.path.join(styledir,f)

	write_style_file(style,styleFileName)

def load_custom_style(network,name,styledir=STYLES_DIRECTORY):
	f = encodeStyleName(network,name)
	styleFileName = os.path.join(styledir,f)

	if os.path.isfile(styleFileName):
		return read_style_file(styleFileName)
	else:
		return None

def get_complete_style_name(network,name,styledir=STYLES_DIRECTORY):
	f = encodeStyleName(network,name)
	return os.path.join(styledir,f)

def encodeStyleName(network,name=None):
	network = network.replace(":","-")
	network = network.lower()
	if name==None:
		return f"{network}.style"
	else:
		return f"{network}-{name}.style"

def find_cat_file(script,scriptdir):
	if os.path.isfile(script):
		return script

	e_script = script+".txt"
	if os.path.isfile(e_script):
		return e_script

	d_script = os.path.join(scriptdir, script)
	if os.path.isfile(d_script):
		return d_script

	d_script = os.path.join(scriptdir, script+".txt")
	if os.path.isfile(d_script):
		return d_script

	return None

def find_style_file(script,styledir):
	if os.path.isfile(script):
		return script

	e_script = script+"."+STYLE_FILE_EXTENSION
	if os.path.isfile(e_script):
		return e_script

	d_script = os.path.join(styledir, script)
	if os.path.isfile(d_script):
		return d_script

	d_script = os.path.join(styledir, script+"."+STYLE_FILE_EXTENSION)
	if os.path.isfile(d_script):
		return d_script

	return None

def find_script_file(script,scriptdir):
	if os.path.isfile(script):
		return script

	e_script = script+"."+SCRIPT_FILE_EXTENSION
	if os.path.isfile(e_script):
		return e_script

	d_script = os.path.join(scriptdir, script)
	if os.path.isfile(d_script):
		return d_script

	d_script = os.path.join(scriptdir, script+"."+SCRIPT_FILE_EXTENSION)
	if os.path.isfile(d_script):
		return d_script

	return None

def clear_auto_script_cache():
	global AUTO_SCRIPT_CACHE
	AUTO_SCRIPT_CACHE = {}

def get_auto_script_name(ip,port,scriptdir):
	fname = ip.strip()+"_"+str(port).strip()+"."+SCRIPT_FILE_EXTENSION
	scriptname = os.path.join(scriptdir, fname)

	return scriptname

def save_auto_script(ip,port,script,scriptdir):
	fname = ip.strip()+"_"+str(port).strip()+"."+SCRIPT_FILE_EXTENSION
	scriptname = os.path.join(scriptdir, fname)

	global AUTO_SCRIPT_CACHE
	if scriptname in AUTO_SCRIPT_CACHE: AUTO_SCRIPT_CACHE[scriptname] = script

	f=open(scriptname, "w")
	f.write(script)
	f.close()

def load_auto_script(ip,port,scriptdir):
	fname = ip.strip()+"_"+str(port).strip()+"."+SCRIPT_FILE_EXTENSION
	scriptname = os.path.join(scriptdir, fname)
	if scriptname in AUTO_SCRIPT_CACHE: return AUTO_SCRIPT_CACHE[scriptname]
	if os.path.isfile(scriptname):
		f=open(scriptname, "r")
		code = f.read()
		f.close()

		if len(code)>0:
			if code[-1]!="\n": code = code + "\n"

		AUTO_SCRIPT_CACHE[scriptname] = code
		return code
	else:
		return None


def load_emoji_autocomplete():
	EMOJI_AUTOCOMPLETE = []
	with open(EMOJI_ALIAS_AUTOCOMPLETE_FILE,mode="r",encoding="latin-1") as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			EMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	with open(EMOJI_AUTOCOMPLETE_FILE,mode="r",encoding="latin-1") as fp:
		line = fp.readline()
		while line:
			e = line.strip()
			EMOJI_AUTOCOMPLETE.append(e)
			line = fp.readline()
	return EMOJI_AUTOCOMPLETE

EMOJI_AUTOCOMPLETE = load_emoji_autocomplete()

def get_text_format_settings(filename=STYLE_FILE):
	if filename==None: filename=STYLE_FILE
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

def patch_user(data):
	if not 'failreconnect' in data:
		data['failreconnect'] = True
	if not 'auto_script' in data:
		data['auto_script'] = False
	if not 'save_script' in data:
		data['save_script'] = False
	return data

def get_user(filename=USER_FILE):
	#if filename==None: filename=USER_FILE
	if os.path.isfile(filename):
		with open(filename, "r") as read_user:
			data = json.load(read_user)
			data = patch_user(data)
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
			"reconnect": True,
			"autojoin": False,
			"history": [],
			"save_history": True,
			"ignore": [],
			'failreconnect': True,
			'auto_script': True,
			'save_script': False,
		}
		return si

def save_user(user,filename=USER_FILE):
	if filename==None: filename=USER_FILE
	with open(filename, "w") as write_data:
		json.dump(user, write_data, indent=4, sort_keys=True)

def write_style_file(style,filename=STYLE_FILE):
	if filename==None: filename=STYLE_FILE
	output = f'''/*
\t ___      _   
\t|__ \ _ _| |__
\t/ _  | '_| / /
\t\___/|_| |_\_\\

\t{OFFICIAL_REPOSITORY}

\tThis file uses a sub-set of CSS used by Qt called \"QSS\"
\thttps://doc.qt.io/qt-5/stylesheet-syntax.html

\tThis file is generated and maintained by the Erk IRC Client
\tPlease don't edit manually!

*/\n\n'''

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

def patch_style_file(filename,data):

	missing = []

	if not 'timestamp' in data: missing.append('timestamp')
	if not 'username' in data: missing.append('username')
	if not 'message' in data: missing.append('message')
	if not 'system' in data: missing.append('system')
	if not 'self' in data: missing.append('self')
	if not 'action' in data: missing.append('action')
	if not 'notice' in data: missing.append('notice')
	if not 'hyperlink' in data: missing.append('hyperlink')
	if not 'all' in data: missing.append('all')
	if not 'error' in data: missing.append('error')
	if not 'server' in data: missing.append('server')
	if not 'plugin' in data: missing.append('plugin')
	if not 'editor' in data: missing.append('editor')

	# If there's no missing styles, return unpatched data
	if len(missing)==0: return data

	# Load in the backup style file
	backup = read_style_file(BACKUP_STYLE_FILE)

	# Patch the input style with backup data
	for m in missing:
		data[m] = backup[m]

	# Save the patched style file
	write_style_file(data,filename)

	# Return the patched data
	return data


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

	# Check to make sure the style file is complete,
	# and patch it with any missing data
	style = patch_style_file(filename,style)

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
	network = network.lower()
	if name==None:
		return f"{network}.json"
	else:
		return f"{network}-{name}.json"

# Takes an array of Message() objects, converts it to
# an AoA, and appens the AoA to a file containing
# AoAs on disk
def saveLog(network,name,logs,logdir=LOG_DIRECTORY):
	f = encodeLogName(network,name)
	logfile = os.path.join(logdir,f)

	logs = log_to_array(logs)

	slog = loadLog(network,name,logdir)
	for e in logs:
		slog.append(e)

	with open(logfile, "w") as writelog:
		json.dump(slog, writelog, indent=4, sort_keys=True)

# Loads an AoA from disk and returns it
def loadLog(network,name,logdir=LOG_DIRECTORY):
	f = encodeLogName(network,name)
	logfile = os.path.join(logdir,f)

	if os.path.isfile(logfile):
		with open(logfile, "r") as logentries:
			data = json.load(logentries)
			return data
	else:
		return []

# Loads an AoA from disk, converts it to an arroy
# of Message() objects, and returns it
def readLog(network,name,logdir):
	logs = loadLog(network,name,logdir)
	logs = array_to_log(logs)
	return logs

# Loads an AoA from disk, converts it to a string
def dumpLog(filename,delimiter,linedelim="\n",epoch=True):
	if os.path.isfile(filename):
		with open(filename, "r") as logentries:
			logs = json.load(logentries)
	if logs:
		out = []
		for l in logs:
			l[2] = l[2].strip()
			l[3] = l[3].strip()
			if l[2]=='': l[2] = '***'

			if not epoch:
				pretty_timestamp = datetime.fromtimestamp(l[0]).strftime('%a, %d %b %Y %H:%M:%S')
				entry = pretty_timestamp+delimiter+l[2]+delimiter+l[3]
			else:
				entry = str(l[0])+delimiter+l[2]+delimiter+l[3]
			out.append(entry)
		return linedelim.join(out)
	else:
		return ''

# Loads an AoA from disk, converts it to a JSON string
def dumpLogJson(filename,epoch=True):
	if os.path.isfile(filename):
		with open(filename, "r") as logentries:
			logs = json.load(logentries)
	if logs:
		out = []
		for l in logs:
			l[2] = l[2].strip()
			l[3] = l[3].strip()
			if l[2]=='': l[2] = '*'
			if not epoch:
				l[0] = datetime.fromtimestamp(l[0]).strftime('%a, %d %b %Y %H:%M:%S')
			entry = [ l[0],l[2],l[3] ]
			out.append(entry)
		return json.dumps(out, indent=4, sort_keys=True)
	else:
		return ''