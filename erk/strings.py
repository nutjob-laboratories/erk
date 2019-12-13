
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


APPLICATION_MAJOR_VERSION = "0.700"
APPLICATION_VERSION = APPLICATION_MAJOR_VERSION+"."+MINOR_VERSION

OFFICIAL_REPOSITORY = "https://github.com/nutjob-laboratories/erk"
PROGRAM_FILENAME = "erk.py"
NORMAL_APPLICATION_NAME = "Erk"

SERVER_CONSOLE_NAME = "Server"

MASTER_LOG_NAME = "Log"