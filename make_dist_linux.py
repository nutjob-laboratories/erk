
import os
import sys
import shutil

f = open("./erk/data/minor.txt","r")
mversion = f.read()
f.close()

mversion = int(mversion)+1
mversion = str(mversion)

f = open("./erk/data/minor.txt","w")
f.write(mversion)
f.close()

from erk.strings import *

# Build distribution zips

os.mkdir("./erk-irc-client")
os.mkdir("./erk-irc-client/settings")

os.mkdir("./erk-irc-client/plugins")
os.mkdir("./erk-irc-client/plugins/examples")

shutil.copy("./plugins/examples/hello.png", "./erk-irc-client/plugins/examples/hello.png")
shutil.copy("./plugins/examples/notes.png", "./erk-irc-client/plugins/examples/notes.png")
shutil.copy("./plugins/examples/hello.py", "./erk-irc-client/plugins/examples/hello.py")
shutil.copy("./plugins/examples/notes.py", "./erk-irc-client/plugins/examples/notes.py")
shutil.copy("./plugins/examples/package.png", "./erk-irc-client/plugins/examples/package.png")
shutil.copy("./plugins/examples/package.txt", "./erk-irc-client/plugins/examples/package.txt")

os.mkdir("./erk-irc-client/documentation")
shutil.copy("./documentation/Erk_Plugin_Guide.pdf", "./erk-irc-client/documentation/Erk_Plugin_Guide.pdf")
shutil.copy("./documentation/Erk_Scripting_and_Commands.pdf", "./erk-irc-client/documentation/Erk_Scripting_and_Commands.pdf")
shutil.copy("./documentation/rfc1459.pdf", "./erk-irc-client/documentation/rfc1459.pdf")
shutil.copy("./documentation/rfc2812.pdf", "./erk-irc-client/documentation/rfc2812.pdf")

os.system("sh compile_resources.sh")

shutil.copytree("./erk", "./erk-irc-client/erk",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copytree("./spellchecker", "./erk-irc-client/spellchecker",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))
shutil.copytree("./emoji", "./erk-irc-client/emoji",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copy("./erk.py", "./erk-irc-client/erk.py")

shutil.copy("./LICENSE", "./erk-irc-client/LICENSE")

#os.system("powershell.exe -nologo -noprofile -command \"& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist', 'erk_dist.zip'); }\" ")
os.system("cd erk-irc-client; zip -r ../erk_dist.zip . ; cd ..")

shutil.rmtree('./erk-irc-client')

archive_name = f"{NORMAL_APPLICATION_NAME.lower()}-{APPLICATION_MAJOR_VERSION}.zip"

os.rename('erk_dist.zip', archive_name)

os.remove(f"./downloads/{archive_name}")
os.remove("./downloads/erk-latest.zip")

shutil.copy(archive_name, "./downloads/"+archive_name)
shutil.copy(archive_name, "./downloads/erk-latest.zip")

os.remove(archive_name)
