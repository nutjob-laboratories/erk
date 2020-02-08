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

import sys,os

DEFAULT_NICKNAME = "erk_user"
DEFAULT_USERNAME = "erk_user"
DEFAULT_IRCNAME = "Erk IRC Client"
DEFAULT_ALTERNATIVE = "erk_user99"

APPLICATION_NAME = "Ərk"

MINOR_VERSION_FILE = os.path.join(os.path.join(os.path.join(sys.path[0], "erk"), "data"), "minor.txt")
f = open(MINOR_VERSION_FILE,"r")
MINOR_VERSION = f.read()
f.close()
if len(MINOR_VERSION)==1:
	MINOR_VERSION = '00'+MINOR_VERSION
elif len(MINOR_VERSION)==2:
	MINOR_VERSION = '0'+MINOR_VERSION


APPLICATION_MAJOR_VERSION = "0.810"
APPLICATION_VERSION = APPLICATION_MAJOR_VERSION+"."+MINOR_VERSION

OFFICIAL_REPOSITORY = "https://github.com/nutjob-laboratories/erk"
PROGRAM_FILENAME = "erk.py"
NORMAL_APPLICATION_NAME = "Erk"

SERVER_CONSOLE_NAME = "_Server"

MASTER_LOG_NAME = "Log"

UNKNOWN_NETWORK = "Unknown"
