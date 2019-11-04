
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

from erk.common import *

# Build distribution zips

os.mkdir("./dist")
os.mkdir("./dist/settings")
os.mkdir("./dist/settings/user")
os.mkdir("./dist/logs")
os.mkdir("./dist/plugins")
os.mkdir("./dist/documentation")

os.system("compile_resources.bat")

shutil.copytree("./erk", "./dist/erk",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copytree("./spellchecker", "./dist/spellchecker",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))
shutil.copytree("./emoji", "./dist/emoji",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copytree("./pdfjs", "./dist/pdfjs",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copy("./erk.py", "./dist/erk.py")

shutil.copy("./LICENSE", "./dist/LICENSE")

shutil.copy("./documentation/Erk-Plugin-Guide.odt", "./dist/documentation/Erk-Plugin-Guide.odt")
shutil.copy("./documentation/Erk-Plugin-Guide.pdf", "./dist/documentation/Erk-Plugin-Guide.pdf")

os.system("powershell.exe -nologo -noprofile -command \"& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist', 'erk_dist.zip'); }\" ")

shutil.rmtree('./dist')

archive_name = f"{NORMAL_APPLICATION_NAME.lower()}-{APPLICATION_VERSION}.zip"

os.rename('erk_dist.zip', archive_name)

os.remove("./downloads/erk-latest.zip")

shutil.copy(archive_name, "./downloads/"+archive_name)
shutil.copy(archive_name, "./downloads/erk-latest.zip")

os.remove(archive_name)

# Build readme

x = open("README.txt",mode="r", encoding='latin-1')
t = str(x.read())
x.close()
t = t.replace("!_VERSION_!",APPLICATION_MAJOR_VERSION)
t = t.replace("!_FULL_VERSION_!",APPLICATION_VERSION)
os.remove("README.md")
f = open("README.md",mode="w", encoding='latin-1')
f.write(t)
f.close()
