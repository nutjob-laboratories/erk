
<p align="center">
  <img src="https://github.com/nutjob-laboratories/erk/raw/master/images/logo_200x200.png"><br>
  <b>Ərk IRC Client</b><br>
  <a href="https://github.com/nutjob-laboratories/erk/releases/tag/0.875.077"><b>Download last stable release</b></a><br>
  <a href="https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-latest.zip"><b>Download Ərk 0.880.003</b></a><br>
  <a href="https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Scripting_and_Commands.pdf"><b>View Ərk command and scripting documentation</b></a><br>
  <a href="https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Plugin_Guide.pdf"><b>View Ərk plugin documentation</b></a>
</p>

**Ərk** is a graphical open source [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **0.880.003**.

**Ərk** is fully functional and ready for your use on Windows or Linux. Bugs are being fixed all the time, and features are still being tweaked, but it's ready.

# Screenshots
<center><p align="center">
<table style="width: 100%" border="0">
      <tbody>
        <tr>
          <td>
            <table style="width: 100%" border="0">
              <tbody>
                <tr>
                  <td style="text-align: center; vertical-align: middle;"><a href="https://github.com/nutjob-laboratories/erk/raw/master/images/screenshot_full.png"><img src="https://github.com/nutjob-laboratories/erk/raw/master/images/screenshot.png"></a><br>
  <b>Ərk connected to EFnet on Windows 10</b></td>
                  <td style="text-align: center; vertical-align: middle;"><a href="https://github.com/nutjob-laboratories/erk/raw/master/images/screenshot_linux_full.png"><img src="https://github.com/nutjob-laboratories/erk/raw/master/images/screenshot_linux.png"></a><br>
  <b>Ərk connected to EFnet on Linux Mint</b></td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
</p></center>

# Features

* **Ərk** does chat, and _only_ chat.
  * **No** [DCC file transfer](https://en.wikipedia.org/wiki/Direct_Client-to-Client) support
  * **No** [Bittorrent](https://en.wikipedia.org/wiki/BitTorrent) client
  * Just plain ol' fashioned IRC
* Runs on Windows and Linux
* Supports multiple connections (you can chat on more than one IRC server at a time)
* Open source ([GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html))
* A built-in list of over 80 IRC servers to connect to
* An extensive set of configuration options
  * Over 100 display and configuration options settable in the GUI
  * Over 30 different command line options
* Text colors are customize-able
* Built-in [spell checker](https://github.com/barrust/pyspellchecker) (supports English, Spanish, French, and German)
* [Emoji](https://en.wikipedia.org/wiki/Emoji) support
  * Insert emojis into chat by using shortcodes (such as `:joy:` :joy:, `:yum:` :yum:, etc.)
* Command/nickname auto-completion
  * Type the first few letters of a command or nickname and hit the tab key
  * Auto-complete works for emoji shortcodes, custom macros, and plugin-based commands, too!
* Optional profanity filter
* Full IRC color support
* Automatic logging of channel and private chats
* Powerful scripting engine
  * A script editor is built into the client
    * Create, open, and edit scripts
    * Syntax highlighting
  * [Scripting and command documentation](https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Scripting_and_Commands.pdf) is included
 * Powerful plugin engine
   * Plugins are written in Python 3, just like **Ərk**
   * Most IRC events can be caught
   * Obscure blog and forums posts aren't needed, [plugin documentation](https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Plugin_Guide.pdf) (with everything you need to know to write **Ərk** plugins) is included
   * [Check out the official plugin repository](https://github.com/nutjob-laboratories/erk-plugins)! If you've got a plugin that you've written and want to include in the repository, send a pull request!
* An extensive set of command line flags, allowing for _even more_ configuration options
  * Disable most features on startup
  * Connect to an IRC server from the command-line
  * Support for connecting via [IRC URLs](https://www.w3.org/Addressing/draft-mirashi-url-irc-01.txt)

# Requirements
**Ərk** requires Python 3, [PyQt5](https://pypi.org/project/PyQt5/), and [Twisted](https://twistedmatrix.com/trac/). PyQt5 and Twisted can be installed by using [**pip**](https://pypi.org/project/pip/):

    pip install pyqt5
    pip install Twisted

To connect to IRC servers via SSL, two additional libraries are needed:

    pip install pyOpenSSL
    pip install service_identity

**Ərk** is being developed with Python 3.7 on Windows 10, and Python 3.8.5 on Linux Mint.

If you're running Windows, and you're getting errors when trying to run **Ərk**, you may have to install another library, [pywin32](https://pypi.org/project/pywin32/). You can also install this with [**pip**](https://pypi.org/project/pip/):

    pip install pywin32

To run properly on Linux, the latest version of all required software is recommended.  There are four libraries that come bundled with **Ərk**:

 - [pike](https://github.com/pyarmory/pike)
 - [emoji](https://github.com/carpedm20/emoji)
 - [pyspellchecker](https://github.com/barrust/pyspellchecker)
 - [qt5reactor](https://github.com/twisted/qt5reactor)

# Install

First, make sure that all the requirements are installed. Next, [download **Ərk**](https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-latest.zip). Extract the zipfile to a directory of your choice using your favorite archive/zip program. Open a command prompt, navigate to the directory you extracted **Ərk** to, and type:

    python erk.py

Hit enter, and **Ərk** will start up! Enter the hostname or IP address of the server you'd like to connect to, or select a server from the built-in list. **Ərk** does not need to be "installed" to any specific directory to run; it will run from any directory it is extracted to.

To make things easier, Windows users can create a shortcut to **Ərk** so all you have to do is double click to start chatting. There are many tutorials on how to do this online; a good place to start is [right here](https://therenegadecoder.com/code/how-to-make-a-python-script-shortcut-with-arguments/).

# Usage
```
usage: python erk.py [-h] [--ssl] [--reconnect] [-p PASSWORD] [-c CHANNEL[:KEY]] [-l]
                     [-u URL] [-a] [-s FILE] [-f] [-o] [-W WIDTH] [-H HEIGHT] [-C FILE]
                     [-U FILE] [-Y FILE] [-L DIRECTORY] [-S DIRECTORY] [-T DIRECTORY]
                     [-M FILE] [-P DIRECTORY] [-e [FILE]] [--settings [FILE]]
                     [--generate [FILE]] [--edit-style] [--export] [--noask] [--nosettings]
                     [--nomenus] [--noconnect] [--noscripts] [--nodisplay] [--nostyles]
                     [--noedit] [--noplugins] [--nocommands] [--noextensions] [--nologs]
                     [--noload] [--nowrite] [--nosystray] [--qt5menu]
                     [SERVER] [PORT]

optional arguments:
  -h, --help            show this help message and exit

Connection:
  SERVER                Server to connect to
  PORT                  Server port to connect to (6667)
  --ssl                 Use SSL to connect to IRC
  --reconnect           Reconnect to servers on disconnection
  -p PASSWORD, --password PASSWORD
                        Use server password to connect
  -c CHANNEL[:KEY], --channel CHANNEL[:KEY]
                        Join channel on connection
  -l, --last            Automatically connect to the last server connected to
  -u URL, --url URL     Use an IRC URL to connect
  -a, --autoscript      Execute connection script (if one exists)
  -s FILE, --script FILE
                        Execute a custom script on connection

Display:
  -f, --fullscreen      Open in fullscreen mode
  -o, --ontop           Application window is always on top
  -W WIDTH, --width WIDTH
                        Set initial window width
  -H HEIGHT, --height HEIGHT
                        Set initial window height

Configuration:
  -C FILE, --config FILE
                        Use an alternate configuration file
  -U FILE, --user FILE  Use an alternate user file
  -Y FILE, --style FILE
                        Use an alternate text style file
  -L DIRECTORY, --logs DIRECTORY
                        Use an alternate log storage location
  -S DIRECTORY, --scripts DIRECTORY
                        Use an alternate script storage location
  -T DIRECTORY, --styles DIRECTORY
                        Use an alternate style storage location
  -M FILE, --macros FILE
                        Use an alternate macro save file
  -P DIRECTORY, --plugins DIRECTORY
                        Add a directory to load plugins from

Tools:
  -e [FILE], --edit [FILE]
                        Launch the script editor
  --settings [FILE], --preferences [FILE]
                        Launch the preferences editor
  --generate [FILE]     Create a "blank" plugin for editing
  --edit-style          Launch the style editor
  --export              Launch the log export tool

Disable functionality:
  --noask               Don't ask for a server to connect to on start
  --nosettings          Disable the "Settings" menu
  --nomenus             Disable all menus
  --noconnect           Disable connection commands
  --noscripts           Disable scripting
  --nodisplay           Disable connection display
  --nostyles            Disables style loading and editing
  --noedit              Disables the script editor
  --noplugins           Disables plugins
  --nocommands          Disables user input commands
  --noextensions        Disables plugins, scripts, and styles
  --nologs              Disables reading and writing logs
  --noload              Disables log loading
  --nowrite             Disables log writing
  --nosystray           Disables system tray icon
  --qt5menu             Disable menu toolbar, and use normal menus
```
# Frequently asked questions

## What does "erk" mean?

The previous name for this client was "Quirc", but after working on it for a while, I discovered that there was already an IRC client named [Quirc](https://quirc.org/). I was asking for some name suggestions in IRC, when Necrosand (one of the users in `#themaxx` on [EFnet](http://www.efnet.org/), and someone who insists on being called, and wanted to be credited as, "IRC Champion Necrosand") suggested "Erk", because "that's how you pronouce IRC". And thus **Ərk** was born.

## Can I use **Ərk** to chat on IRC?

Yes! All basic IRC functionality is in and working. **Ərk** is ready to go!

## Is **Ərk** completed?

No. The current version, 0.880.003, is still a pre-release. I'm still adding and tweaking features, and catching and fixing as many bugs as I can. The final version, **Ərk** 1.0, will come eventually, and we're more than half-way there!

## Does **Ərk** run on Windows? Does it run on Linux?

**Ərk** runs on both Windows and Linux! Now, it's being developed primarily on Linux, but when I first started development I was using Windows 10, and **Ərk** runs flawlessly (and identically) on both platforms. I can't think of a reason why **Ərk** wouldn't run on OSX, but I don't have access to an Apple computer to test this.
My current development "environment" is Python 3.8.5, Qt 5.15.2, and Twisted 18.9.0, and I use [Sublime Text 3](https://www.sublimetext.com/) for my code editor; I'm currently using [Linux Mint](https://linuxmint.com/) 20.1 as my operating system, with [Cinnamon](https://github.com/linuxmint/cinnamon) as my desktop environment.

## How configurable is **Ərk**?
*Super* configurable. You can customize just about every aspect of **Ərk** to make it look and behave *exactly* how you want it. For example, if you wanted to run **Ərk** in such a way that it only displays a single channel with no menus or settings or whatnot, with the window always on top of all others, disabling all extraneous stuff like scripts and plugins and styles, and automatically connects to your favorite channel, "#erk", on EFnet? You could use:

    python erk.py -o --noextensions --nomenu --nodisplay --channel "#erk" irc.efnet.org 6667

And that's only using the command-line options! **Ərk** has over 100 different configuration options available, as well as over 30 different command-line options.

When I started writing **Ərk**, one of my goals was to make it as configurable as possible. I wanted an IRC client that gave the user the tools to make the client look and behave *exactly* how the user wanted.

## Where does **Ərk** store configuration files and logs?

**Ərk** stores all configuration files and logs in your home directory, on all platforms, in a directory named `.erk`. This directory contains several subdirectories, each of which contains different types of files:

 - **`settings`** - Contains the main configuration files for **Ərk**.
   - `settings.json` - The main configuration file for the **Ərk** application.
   - `user.json` - User settings, including your connection history.
   - `macro.json` - If you've created any macros, here is where they are saved.
 - **`scripts`** - Contains connection scripts. Put your **Ərk** scripts in this directory so  that they're easily findable by the client. This is also the default location when you're saving scripts created with the script editor.
 - **`styles`** - Contains any text styles that you've created, as well as the default text style **Ərk** uses.
   - `default.style` - The default text style for **Ərk**. If this file is missing, **Ərk** will re-create it with default settings.
 - **`logs`** - This is where **Ərk** stores all chat logs. Logs are stored in JSON, and use a format specific to **Ərk**. If you want to export your logs, use the "Export Log" entry in the "Tools" menu, or launch **Ərk** with `python erk.py --export` to launch a GUI log export wizard. You can export them to plain text (with your choice of delimiters) or to JSON.
 - **`plugins`** - This is where **Ərk** stores and loads plugins from. Installing a plugin is as easy as placing it in this directory.

## How do you write plugins for Ərk?

It's easy! **Ərk** plugins are written in Python 3, the same language that **Ərk** is written in. At its core, a  plugin is just a Python 3 class that inherits from a parent class built into **Ərk**. Here's a basic example. All it does is print all incoming and outgoing IRC traffic to the console:
```python
from erk import *

class ExamplePlugin(Plugin):

  NAME = "Example Plugin"
  VERSION = "1.0"
  DESCRIPTION = "Displays all IRC network traffic"

  def line_in(self,data):
    print(self.irc.server+":"+str(self.irc.port)+" <- "+data)

  def line_out(self,data):
    print(self.irc.server+":"+str(self.irc.port)+" -> "+data)
```
Everything you need to write your own **Ərk** plugins is in the [**Ərk** Plugin Guide](https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Plugin_Guide.pdf), included with every download!

## Some of the options are weird...why is there a profanity filter?!
Both my parents were teachers, and all of my grandparents were teachers. Having the ability to configure **Ərk** to run in a classroom environment was (and is) one of my goals. That's part of the reason why I've included configuration options to "lock down" **Ərk** while it's running (like the ability to disable command input, remove GUI menus, disable most customization and features, and, yes, hide profanity).

## Who is writing Ərk?
Currently, it's just me. My name is Dan Hetrick. I'm 47 years old as of 2021, and I've been a software developer for many years, though no longer professionally. I began writing Quirc, the IRC client that eventually became **Ərk**, in order to learn Python 3, and to learn the ins and outs of the Qt library. Quirc died off, got re-written and/or refactored a few (dozen) times, got renamed once I found out there already was an IRC client named [Quirc](https://quirc.org/), and eventually became **Ərk**! I've been working on this client for a little over 2.5 years as my primary project, and I'm rather proud of it. I use **Ərk** as my primary IRC client, and have for almost 2 years.

## Another IRC client? Why not use HexChat?

Honestly? I wanted an IRC client that I liked using, and I wanted an IRC client that I could use in both Windows and Linux. Other than some "connects to every kind of chat network" clients, I didn't have a lot of choices. Since the only kind of chat I regularly use is IRC, I didn't care if the client could connect to Jabber, Facebook, or whatever. That left me (in my opinion) with only one choice: HexChat.

HexChat is, well, aging. The last I heard, there was nobody maintaining the source. I wanted a new IRC client written in a modern, accessible language; I wanted a client that was *not* written in C or C++. I wanted a pretty, attractive client that looks like it was written in the last decade. And, moreover, I wanted a client written for the desktop; I didn't want one that runs in a web browser, or on a smartphone, or in "the cloud". I wanted a client that was open source (both free as in beer and free as in speech).  I wanted a client that ran fast, consumed resources commensurate with the task of a text-only chat protocol.  I wanted a client that wasn't limited to just text;  a client that can send and display emojis.

Since I couldn't find that IRC client, I decided to write my own.

When I decided to write a new IRC client, I wanted it to feature a few things:

* It had to be open source (free as in speech _and_ as in beer)
* The ability to connect to multiple servers at a time (something almost every open source client does)
* A full, modern GUI (HexChat is sort of modern, I guess, if was still 1999-2000)
* Easy to install, easy to run (if you're trying to compile HexChat for Windows, good luck, you'll need it)
* Cross-platform compatibility; the ability to run on Windows, Linux, and OSX 
* The ability to extend the client _easily_, without having to track down a bunch of forum and blog posts
* Focuses on the chat experience (not downloading/uploading files)

**Ərk** is being developed on primarily on Linux (and occasionally on Windows 10), but it uses no Windows-specific or Linux-specific libraries or functionality. It's written in pure Python3 and PyQt5, and installing it as easy as cloning this repository, making sure you have Python3 and the other pre-requisites installed, and executing `python erk.py`. It does IRC, and nothing else, and it looks good doing it.

The other reason why I wrote **Ərk** is because I got tired of not understanding how the most popular clients did things. I wanted a client that you could configure to do _exactly_ what you wanted it to do, no more and no less. That's why **Ərk** has a ridiculous amount of configuration options. Do you want to run the client in full-screen mode, and remove the ability of users to change settings or connect to other servers (aka, "kiosk mode")? You can do that. Do you want to strip all the "pretty" off the client, and basically run it in "text only" mode? You can do that. Do you want **Ərk** to do nothing except what you tell it to do? You can do that. Almost everything in the client can be configured from within the GUI or with command-line flags.

## Is **Ərk** designed for multiple users?

Yes! **Ərk** stores configuration files in a user's "home" directory, on both Linux and Windows. However, if multiple users want to use **Ərk** on the same account, there are command-line options to store configuration files in specific, designated locations.

* `-C`,`--config` : This tells **Ərk** to use a user-specified file for most configuration options.
* `-U`,`--user` : This tells **Ərk** to use a user-specified user settings file. Stored in this file are nickname and username settings, server connection history, and other user specific data.
* `-Y`,`--style` : This tells **Ərk** to use a user-specified text style file. This sets what colors and formatting are used to display text in the client.
* `-L`,`--logs` : This tells **Ərk** to use a user-specified directory for log loading and storage.
* `-S`,`--scripts` : This tells **Ərk** to use a user-specified directory for script loading and storage.
* `-T`,`--styles` : This tells **Ərk** to use a user-specified directory for text style loading and storage.
* `-M`,`--macros` : This tells **Ərk** to use a user-specified file for macro loading and storage.
* `-P`,`--plugins` : This tells **Ərk** to load plugins from additional directories. This option can be called multiple times to load plugins from multiple directories.

This allows users to set specific configuration files for different users, and can be set in a shortcut or batch file. Configuration and user setting files are JSON, and the text format settings file is CSS. If the filename (or directory name) passed to **Ərk** is not found, **Ərk** will create the file and fill it with default settings, or create the directory to be used for logs.

More command-line settings can be viewed by executing **Ərk** with the `-h` or `--help` command-line flag.

For an example of how to implement this for multiple users, let's assume we have two users, named Alice and Bob. They're both running **Ərk** on the same computer (which runs Windows), and want to keep their settings and logs separate. **Ərk**, in this example, is installed in `C:\Erk`. First, we create a directory for Alice; we'll put it in the root directory of the "C" drive. We'll name Alice's directory "Alice_Erk":

    mkdir C:\Alice_Erk

Now, let's make a directory for Bob:

    mkdir C:\Bob_Erk

We'll use these directories to store settings and logs. Now, let's create batch files for both users, ones that start **Ərk** up with the right commandline flags. Assuming that Python is in Window's PATH, Alice's batch file looks like this:

    python C:\Erk\erk.py -C C:\Alice_Erk\settings.json -U C:\Alice_Erk\user.json -Y C:\Alice_Erk\text.style -L C:\Alice_Erk\logs -S C:\Alice_Erk\scripts -T C:\Alice\styles -M C:\Alice\macros.json

Similarly, Bob's batch file looks like this:

    python C:\Erk\erk.py -C C:\Bob_Erk\settings.json -U C:\Bob_Erk\user.json -Y C:\Bob_Erk\text.style -L C:\Bob_Erk\logs -S C:\Bob_Erk\scripts -T C:\Bob\styles -M C:\Bob\macros.json

Alice and Bob can now use **Ərk** with their own customized settings!
