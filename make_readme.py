
import os
import sys

from erk.strings import *

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

x = open("README_DIST.txt",mode="r", encoding='latin-1')
t = str(x.read())
x.close()
t = t.replace("!_VERSION_!",APPLICATION_MAJOR_VERSION)
t = t.replace("!_FULL_VERSION_!",APPLICATION_VERSION)
os.remove("README_DIST.md")
f = open("README_DIST.md",mode="w", encoding='latin-1')
f.write(t)
f.close()