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

import os
import sys
import glob
import json
import re
from .strings import *

INSTALL_DIRECTORY = sys.path[0]
MACRO_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "macros")
if not os.path.isdir(MACRO_DIRECTORY): os.mkdir(MACRO_DIRECTORY)

MACROS = []
MACRO_COMMANDS = {}

def macro_variables(window,client,text):

	location_name = re.compile(re.escape('$channel'), re.IGNORECASE)
	text = location_name.sub(window.name,text)

	location_name = re.compile(re.escape('$name'), re.IGNORECASE)
	text = location_name.sub(window.name,text)

	server_ip = re.compile(re.escape('$server'), re.IGNORECASE)
	text = server_ip.sub(client.server,text)

	server_port = re.compile(re.escape('$port'), re.IGNORECASE)
	text = server_port.sub(str(client.port),text)

	server_host = re.compile(re.escape('$hostname'), re.IGNORECASE)
	if client.hostname:
		text = server_host.sub(client.hostname,text)
	else:
		text = server_host.sub("Unknown hostname",text)

	server_network = re.compile(re.escape('$network'), re.IGNORECASE)
	if client.network:
		text = server_network.sub(client.network,text)
	else:
		text = server_network.sub("Unknown network",text)

	user_nick = re.compile(re.escape('$self'), re.IGNORECASE)
	text = user_nick.sub(client.nickname,text)

	erk_name = re.compile(re.escape('$erk'), re.IGNORECASE)
	text = erk_name.sub(APPLICATION_NAME,text)

	erk_version = re.compile(re.escape('$version'), re.IGNORECASE)
	text = erk_version.sub(APPLICATION_VERSION,text)

	return text

def get_macro(filename):
	for m in MACROS:
		if m["filename"]==filename:
			return m
	return None

def save_macro(user,filename):

	filename = os.path.join(MACRO_DIRECTORY, filename)

	with open(filename, "w") as write_data:
		json.dump(user, write_data, indent=4, sort_keys=True)

	load_macros()

def load_macros():
	global MACROS
	global MACRO_COMMANDS

	# Load in macros
	MACROS = []
	MACRO_COMMANDS = {}
	target = os.path.join(MACRO_DIRECTORY, "*.json")
	for file in glob.glob(target):
		with open(file, "r") as macrofile:
			data = json.load(macrofile)
			data["filename"] = file
			MACROS.append(data)

			# Added macro data to autocomplete command list
			if data["arguments"]==0:
				MACRO_COMMANDS[data["trigger"]] = data["trigger"]
			else:
				MACRO_COMMANDS[data["trigger"]] = data["trigger"] + " "

load_macros()
