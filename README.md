<p align="center">
  <img src="https://github.com/nutjob-laboratories/erk/raw/master/images/logo_200x200.png"><br>
  <a href="https://github.com/nutjob-laboratories/erk/releases/tag/0.840.114"><b>Download last stable release</b></a><br>
  <a href="https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-latest.zip"><b>Download Ərk 0.850.002</b></a><br>
  <a href="https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Plugin_Guide.pdf"><b>View Ərk plugin documentation</b></a><br>
  <a href="https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Scripting_and_Commands.pdf"><b>View Ərk command and scripting documentation</b></a>
</p>

**Ərk** is a graphical open source [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **0.850.002**.

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
  * Almost every part of the interface can be customized
  * Most behaviors can be customized
  * Over 50 display and configuration options settable in the GUI
  * Scripting, plugins, menus, and more can be disabled from the command-line
* Text colors are customizeable
  * Any text, from nicknames to messages to hyperlinks, can use custom colors
  * Text rendering setting are stored in "style files", and can be shared
  * Every text-displaying window can be styled: channels, private chats, and server consoles
  * Chat styles are "remembered" and loaded automatically
  * Features a built-in style file editor
* Built-in [spell checker](https://github.com/barrust/pyspellchecker)
  * Supports English, Spanish, French, and German
  * Right click on misspelled words for suggested spellings/words
* [Emoji](https://en.wikipedia.org/wiki/Emoji) support
  * Insert emojis into chat by using shortcodes (such as `:joy:` :joy:, `:yum:` :yum:, etc.)
* Command/nickname auto-completion
  * Type the first few letters of a command or nickname and hit the tab key
  * Auto-complete works for emoji shortcodes, too
* Optional profanity filter
* Full IRC color support
  * Colors are rendered in the client (and rendering can be turned off)
  * Full support for using foreground and background colors in outgoing messages
* Automatic logging of channel and private chats
  * Logging can be switched on and off
  * Logs can be automatically loaded when resuming public or private chats
* Powerful scripting engine
  * Almost anything you can do in the client, you can do in a script
  * Scripts can be triggered to execute on server connection or manually
  * Scripts run in a separate thread, so running a script won't interrupt your chatting
  * Micro-script editor built into the connection dialog
  * A script editor is built into the client
    * Create, open, and edit scripts
    * Syntax highlighting
    * Run scripts on any connection the client is connected to
  * [Scripting and command documentation](https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Scripting_and_Commands.pdf) is included
* Plugins!
  * Plugins are written in Python 3, just like **Ərk**
  * **Ərk** features a complete plugin [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment), built into the client!
    * Text editor with syntax highlighting
    * Tools to create, package, and export plugin packages
    * Create a basic plugin with two mouse clicks!
  * [Plugin documentation](https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Plugin_Guide.pdf) is included...no trying to figure out how to write a plugin from endless forum posts!
  * Plugins can be found in the [official **Ərk** plugin repository](https://github.com/nutjob-laboratories/erk-plugins)
* An extensive set of command-line flags, allowing for _even more_ configuration options
  * Disable most features on startup
  * Connect to an IRC server from the command-line
  * Support for connecting via [IRC URLs](https://www.w3.org/Addressing/draft-mirashi-url-irc-01.txt)

# Requirements
**Ərk** requires Python 3, [PyQt5](https://pypi.org/project/PyQt5/), [Twisted](https://twistedmatrix.com/trac/), and [qt5reactor](https://github.com/sunu/qt5reactor). PyQt5, Twisted, and qt5reactor can be manually installed, or by using [**pip**](https://pypi.org/project/pip/):

    pip install pyqt5
    pip install Twisted
    pip install qt5reactor

To connect to IRC servers via SSL, two additional libraries are needed:

    pip install pyOpenSSL
    pip install service_identity

**Ərk** is being developed with Python 3.7 on Windows 10, and Python 3.8.5 on Linux Mint.

To run properly on Linux, the latest version of all required software is recommended.  __**If you are running Debian or a Debian-variant (such as Mint, Ubuntu, Xubuntu, etc) you must install PyQt5 and qt5reactor with pip! If you install PyQt5 and qt5reactor from the standard repo Ərk will not function!**__

# Install

First, make sure that all the requirements are installed. Next, [download **Ərk**](https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-latest.zip). Extract the zipfile to a directory of your choice using your favorite archive/zip program. Open a command prompt, navigate to the directory you extracted **Ərk** to, and type:

  python erk.py

Hit enter, and **Ərk** will start up! Enter the hostname or IP address of the server you'd like to connect to, or click the "Servers" tab and select a server from the built-in list.

**Ərk** does not need to be "installed" to any specific directory to run; it will run from any directory it is extracted to.

To make things easier, Windows users can create a shortcut to **Ərk** so all you have to do is double click to start chatting. There are many tutorials on how to do this online; a good place to start is [right here](https://therenegadecoder.com/code/how-to-make-a-python-script-shortcut-with-arguments/).

# Usage
```
usage: python erk.py [-h] [--ssl] [--reconnect] [-p PASSWORD] [-c CHANNEL[:KEY]] [-l]
                     [-u URL] [-a] [-s FILENAME] [-f] [-o] [-W WIDTH] [-H HEIGHT] [-C FILE]
                     [-U FILE] [-Y FILE] [-L DIRECTORY] [-S DIRECTORY] [-T DIRECTORY]
                     [-M FILE] [-X ZIP] [-A ZIP] [-I ZIP] [--generate NAME] [--new]
                     [--editor] [--edit FILE] [--install ZIP] [--noplugins] [--noask]
                     [--nosettings] [--nomenus] [--noconnect] [--noscripts] [--nodisplay]
                     [--nostyles] [--noedit] [--noextensions] [--noinstall] [--qt5menu]
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
  -a, --autoscript      Execute server script on connection (if one exists)
  -s FILENAME, --script FILENAME
                        Execute a custom server script on connection

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
  -X ZIP, --export-settings ZIP
                        Export settings to a zip file
  -A ZIP, --export-all ZIP
                        Export settings and logs to a zip file
  -I ZIP, --import-settings ZIP
                        Import settings (and logs) from a zip file

Plugin development:
  --generate NAME       Generate a "blank" plugin package in the current directory
  --new                 Generate a "blank" plugin package in the plugins directory
  --editor              Open the code editor
  --edit FILE           Open a file in the code editor
  --install ZIP         Install a plugin

Disable functionality:
  --noplugins           Disable plugins
  --noask               Don't ask for a server to connect to on start
  --nosettings          Disable settings menu(s)
  --nomenus             Disable all menus
  --noconnect           Disable connection commands
  --noscripts           Disable scripting
  --nodisplay           Disable connection display
  --nostyles            Disables style loading and editing
  --noedit              Disables the script editor
  --noextensions        Disables scripts and plugins
  --noinstall           Disables plugin installation
  --qt5menu             Disable menu toolbar, and use normal menus
```
# Frequently asked questions

## What does "erk" mean?

The previous name for this client was "Quirc", but after working on it for a while, I discovered that there was already an IRC client named [Quirc](https://quirc.org/). I was asking for some name suggestions in IRC, when one of the users in the channel suggested "Erk", because "that's how you pronouce IRC". And thus **Ərk** was born.

## Is **Ərk** completed?

No. I'm still adding features and tracking down and squashing bugs.

## Can I use **Ərk** to chat on IRC?

Yes! Most basic functionality is done, and it's ready for most IRC stuff.

## Does **Ərk** run on Windows? Does it run on Linux?

**Ərk** runs on both Windows and Linux! It's being developed on Windows 10, but it's been tested (and runs great) on Debian, Ubuntu, and Mint Linux. I can't think of a reason why **Ərk** wouldn't run on OSX, but I don't have access to an Apple computer to test this.

## How do I write an **Ərk** plugin?
**Ərk** plugins are written in Python 3, and consist of a class that inherits from the _Plugin_ class built into **Ərk**. Here's an example plugin that says greets anyone joining a channel the client is in:
```python
from erk import *

class Greeter(Plugin):

  def __init__(self):
    self.name = "Greeter"
    self.description = "A greeting plugin."
  
  def join(self,client,channel,user):
    nickname = user.split('!')[0]
    client.msg(f"Welcome to {channel}, {nickname}!")
```
This plugin will greet anyone who joins any channel the client is in. The greeting message will be sent to the channel (and server) where the join event happened, on all servers that **Ərk** is connected to.

To install this plugin, save it to a file and place it in the "plugins" directory in your **Ərk** installation directory. **Ərk** will load it automatically. Individual plugins can be disabled in the client; even if a package contains multiple plugins, you can disable any one plugin while still allowing the others to execute.

For more information, check out the [documentation](https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Plugin_Guide.pdf).

## How configurable is **Ərk**?
*Super* configurable. You can customize just about every aspect of **Ərk** to make it look and behave *exactly* how you want it. For example, if you wanted to run **Ərk** in such a way that it only displays a single chat window with no menus or settings or whatnot, with the window always on top of all others, disabling all extraneous stuff like plugins and scripts, and automatically connects to your favorite channel, "#erk", on EFnet? You could use:

  python erk.py -o --noextensions --nomenu --nodisplay --nostyles --channel "#erk" irc.efnet.org 6667

And that's only using the command-line options! **Ərk** has over 50 different settings available, as well as nearly 20 different command-line options.

When I started writing **Ərk**, one of my goals was to make it as configurable as possible. I wanted an IRC client that gave the user the tools to make the client look and behave *exactly* how the user wanted.

## Another IRC client? Why not use HexChat?

Honestly? I wanted an IRC client that I liked using, and I wanted an IRC client that I could use in both Windows and Linux. Other than some "connects to every kind of chat network" clients, I didn't have a lot of choices. Since the only kind of chat I regularly use is IRC, I didn't care if the client could connect to Jabber, Facebook, or whatever. That left me (in my opinion) with only one choice: HexChat.

HexChat is, well, aging. The last I heard, there was nobody maintaining the source. I wanted a new IRC client written in a modern, accessible language; I wanted a client that was *not* written in C or C++. I wanted a pretty, attractive client that looks like it was written in the last decade. And, moreover, I wanted a client written for the desktop; I didn't want one that runs in a web browser, or on a smartphone, or in "the cloud". I wanted a client that was open source (both free as in beer and free as in speech).  I wanted a client that ran fast, consumed resources commensurate with the task of a text-only chat protocol.  I wanted a client that wasn't limited to just text;  a client that can send and display emojis.

Since I couldn't find that IRC client, I decided to write my own.

When I decided to write a new IRC client, I wanted it to feature a few things:

* It had to be open source (free as in speech and as in beer)
* The ability to connect to multiple servers at a time (something almost every open source client does)
* A full, modern GUI (HexChat is sort of modern, I guess, if was still 1999-2000)
* Easy to install, easy to run (if you're trying to compile HexChat for Windows, good luck, you'll need it)
* Focuses on the chat experience (not downloading/uploading files)
* The ability to easily extend the client without resorting to Black Magic&trade; or spend hours and hours surfing endless forum posts or decipher less-than-helpful documentation

**Ərk** is being developed on Windows 10 and Linux Mint, but it uses no Windows-specific or Linux-specific libraries or functionality. It's written in pure Python3 and PyQt5, and installing it as easy as cloning this repository, making sure you have Python3 and the other pre-requisites installed, and executing `python erk.py`. It does IRC, and nothing else, and it looks good doing it.

The other reason why I wrote **Ərk** is because I got tired of not understanding how the most popular clients did things. I wanted a client that you could configure to do _exactly_ what you wanted it to do, no more and no less. That's why **Ərk** has a ridiculous amount of configuration options. Do you want to run the client in full-screen mode, and remove the ability of users to change settings or connect to other servers (aka, "kiosk mode")? You can do that. Do you want to strip all the "pretty" off the client, and basically run it in "text only" mode? You can do that. Do you want **Ərk** to do nothing except what you tell it to do? You can do that. Almost everything in the client can be configured from within the GUI or with command-line flags.

## Is **Ərk** designed for multiple users?

Not directly, as all its configuration files are stored in **Ərk**'s installation directory. However, there are six command-line options you can use to manage settings for different users:

* `-C`,`--config` : This tells **Ərk** to use a user-specified file for most configuration options.
* `-U`,`--user` : This tells **Ərk** to use a user-specified user settings file. Stored in this file are nickname and username settings, server connection history, the disabled plugins list, and other user specific data.
* `-Y`,`--style` : This tells **Ərk** to use a user-specified text style file. This sets what colors and formatting is used to display text in the client.
* `-L`,`--logs` : This tells **Ərk** to use a user-specified directory for log loading and storage.
* `-S`,`--scripts` : This tells **Ərk** to use a user-specified directory for script loading and storage.
* `-T`,`--styles` : This tells **Ərk** to use a user-specified directory for text style loading and storage.
* `-M`,`--macros` : This tells **Ərk** to use a user-specified file for macro loading and storage.

This allows users to set specific configuration files for different users, and can be set in a shortcut or batch file. Configuration and user setting files are JSON, and the text format settings file is CSS. If the filename (or directory name) passed to **Ərk** is not found, **Ərk** will create the file and fill it with default settings, or create the directory to be used for logs.

More command-line settings can be viewed by executing **Ərk** with the `--help` command-line flag.

For an example of how to implement this for multiple users, let's assume we have two users, named Alice and Bob. They're both running **Ərk** on the same computer (which runs Windows), and want to keep their settings and logs separate. **Ərk**, in this example, is installed in "C:\Erk". First, we create a directory for Alice; we'll put it in the root directory of the "C" drive. We'll name Alice's directory "Alice_Erk":

  mkdir C:\Alice_Erk

Now, let's make a directory for Bob:

  mkdir C:\Bob_Erk

We'll use these directories to store settings and logs. Now, let's create batch files for both users, ones that start **Ərk** up with the right commandline flags. Assuming that Python is in Window's PATH, Alice's batch file looks like this:

  python C:\Erk\erk.py -C C:\Alice_Erk\settings.json -U C:\Alice_Erk\user.json -Y C:\Alice_Erk\text.style -L C:\Alice_Erk\logs -S C:\Alice_Erk\scripts -T C:\Alice\styles -M C:\Alice\macros.json

Similarly, Bob's batch file looks like this:

  python C:\Erk\erk.py -C C:\Bob_Erk\settings.json -U C:\Bob_Erk\user.json -Y C:\Bob_Erk\text.style -L C:\Bob_Erk\logs -S C:\Bob_Erk\scripts -T C:\Bob\styles -M C:\Bob\macros.json

Alice and Bob can now use **Ərk** with their own customized settings!


Download last stable release
Download Ərk 0.850.002
View Ərk plugin documentation
View Ərk command and scripting documentation

Ərk is a graphical open source Internet relay chat client. The current development version is !FULL_VERSION!.

Ərk is fully functional and ready for your use on Windows or Linux. Bugs are being fixed all the time, and features are still being tweaked, but it’s ready.
Screenshots


Ərk connected to EFnet on Windows 10  
Ərk connected to EFnet on Linux Mint

Features

    Ərk does chat, and only chat.
        No DCC file transfer support
        No Bittorrent client
        Just plain ol’ fashioned IRC
    Runs on Windows and Linux
    Supports multiple connections (you can chat on more than one IRC server at a time)
    Open source (GPL 3)
    A built-in list of over 80 IRC servers to connect to
    An extensive set of configuration options
        Almost every part of the interface can be customized
        Most behaviors can be customized
        Over 50 display and configuration options settable in the GUI
        Scripting, plugins, menus, and more can be disabled from the command-line
    Text colors are customizeable
        Any text, from nicknames to messages to hyperlinks, can use custom colors
        Text rendering setting are stored in “style files”, and can be shared
        Every text-displaying window can be styled: channels, private chats, and server consoles
        Chat styles are “remembered” and loaded automatically
        Features a built-in style file editor
    Built-in spell checker
        Supports English, Spanish, French, and German
        Right click on misspelled words for suggested spellings/words
    Emoji support
        Insert emojis into chat by using shortcodes (such as :joy: 😂, :yum: 😋, etc.)
    Command/nickname auto-completion
        Type the first few letters of a command or nickname and hit the tab key
        Auto-complete works for emoji shortcodes, too
    Optional profanity filter
    Full IRC color support
        Colors are rendered in the client (and rendering can be turned off)
        Full support for using foreground and background colors in outgoing messages
    Automatic logging of channel and private chats
        Logging can be switched on and off
        Logs can be automatically loaded when resuming public or private chats
    Powerful scripting engine
        Almost anything you can do in the client, you can do in a script
        Scripts can be triggered to execute on server connection or manually
        Scripts run in a separate thread, so running a script won’t interrupt your chatting
        Micro-script editor built into the connection dialog
        A script editor is built into the client
            Create, open, and edit scripts
            Syntax highlighting
            Run scripts on any connection the client is connected to
        Scripting and command documentation is included
    Plugins!
        Plugins are written in Python 3, just like Ərk
        Ərk features a complete plugin IDE, built into the client!
            Text editor with syntax highlighting
            Tools to create, package, and export plugin packages
            Create a basic plugin with two mouse clicks!
        Plugin documentation is included…no trying to figure out how to write a plugin from endless forum posts!
        Plugins can be found in the official Ərk plugin repository
    An extensive set of command-line flags, allowing for even more configuration options
        Disable most features on startup
        Connect to an IRC server from the command-line
        Support for connecting via IRC URLs

Requirements

Ərk requires Python 3, PyQt5, Twisted, and qt5reactor. PyQt5, Twisted, and qt5reactor can be manually installed, or by using pip:

pip install pyqt5
pip install Twisted
pip install qt5reactor

To connect to IRC servers via SSL, two additional libraries are needed:

pip install pyOpenSSL
pip install service_identity

Ərk is being developed with Python 3.7 on Windows 10, and Python 3.8.5 on Linux Mint.

To run properly on Linux, the latest version of all required software is recommended. If you are running Debian or a Debian-variant (such as Mint, Ubuntu, Xubuntu, etc) you can install PyQt5 and qt5reactor with pip, or by downloading Ərk with included requirements and installing the .debs yourself! If you install PyQt5 and qt5reactor from the standard repo Ərk will not function!
Install

First, make sure that all the requirements are installed. Next, download Ərk. Extract the zipfile to a directory of your choice using your favorite archive/zip program. Open a command prompt, navigate to the directory you extracted Ərk to, and type:

python erk.py

Hit enter, and Ərk will start up! Enter the hostname or IP address of the server you’d like to connect to, or click the “Servers” tab and select a server from the built-in list.

Ərk does not need to be “installed” to any specific directory to run; it will run from any directory it is extracted to.

To make things easier, Windows users can create a shortcut to Ərk so all you have to do is double click to start chatting. There are many tutorials on how to do this online; a good place to start is right here.
Usage

usage: python erk.py [-h] [--ssl] [--reconnect] [-p PASSWORD] [-c CHANNEL[:KEY]] [-l]
                     [-u URL] [-a] [-s FILENAME] [-f] [-o] [-W WIDTH] [-H HEIGHT] [-C FILE]
                     [-U FILE] [-Y FILE] [-L DIRECTORY] [-S DIRECTORY] [-T DIRECTORY]
                     [-M FILE] [-X ZIP] [-A ZIP] [-I ZIP] [--generate NAME] [--new]
                     [--editor] [--edit FILE] [--install ZIP] [--noplugins] [--noask]
                     [--nosettings] [--nomenus] [--noconnect] [--noscripts] [--nodisplay]
                     [--nostyles] [--noedit] [--noextensions] [--noinstall] [--qt5menu]
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
  -a, --autoscript      Execute server script on connection (if one exists)
  -s FILENAME, --script FILENAME
                        Execute a custom server script on connection

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
  -X ZIP, --export-settings ZIP
                        Export settings to a zip file
  -A ZIP, --export-all ZIP
                        Export settings and logs to a zip file
  -I ZIP, --import-settings ZIP
                        Import settings (and logs) from a zip file

Plugin development:
  --generate NAME       Generate a "blank" plugin package in the current directory
  --new                 Generate a "blank" plugin package in the plugins directory
  --editor              Open the code editor
  --edit FILE           Open a file in the code editor
  --install ZIP         Install a plugin

Disable functionality:
  --noplugins           Disable plugins
  --noask               Don't ask for a server to connect to on start
  --nosettings          Disable settings menu(s)
  --nomenus             Disable all menus
  --noconnect           Disable connection commands
  --noscripts           Disable scripting
  --nodisplay           Disable connection display
  --nostyles            Disables style loading and editing
  --noedit              Disables the script editor
  --noextensions        Disables scripts and plugins
  --noinstall           Disables plugin installation
  --qt5menu             Disable menu toolbar, and use normal menus

Frequently asked questions
What does “erk” mean?

The previous name for this client was “Quirc”, but after working on it for a while, I discovered that there was already an IRC client named Quirc. I was asking for some name suggestions in IRC, when one of the users in the channel suggested “Erk”, because “that’s how you pronouce IRC”. And thus Ərk was born.
Is Ərk completed?

No. I’m still adding features and tracking down and squashing bugs.
Can I use Ərk to chat on IRC?

Yes! Most basic functionality is done, and it’s ready for most IRC stuff.
Does Ərk run on Windows? Does it run on Linux?

Ərk runs on both Windows and Linux! It’s being developed on Windows 10, but it’s been tested (and runs great) on Debian, Ubuntu, and Mint Linux. I can’t think of a reason why Ərk wouldn’t run on OSX, but I don’t have access to an Apple computer to test this.
How do I write an Ərk plugin?

Ərk plugins are written in Python 3, and consist of a class that inherits from the Plugin class built into Ərk. Here’s an example plugin that says greets anyone joining a channel the client is in:

from erk import *

class Greeter(Plugin):

  def __init__(self):
    self.name = "Greeter"
    self.description = "A greeting plugin."
  
  def join(self,client,channel,user):
    nickname = user.split('!')[0]
    client.msg(f"Welcome to {channel}, {nickname}!")

This plugin will greet anyone who joins any channel the client is in. The greeting message will be sent to the channel (and server) where the join event happened, on all servers that Ərk is connected to.

To install this plugin, save it to a file and place it in the “plugins” directory in your Ərk installation directory. Ərk will load it automatically. Individual plugins can be disabled in the client; even if a package contains multiple plugins, you can disable any one plugin while still allowing the others to execute.

For more information, check out the documentation.
How configurable is Ərk?

Super configurable. You can customize just about every aspect of Ərk to make it look and behave exactly how you want it. For example, if you wanted to run Ərk in such a way that it only displays a single chat window with no menus or settings or whatnot, with the window always on top of all others, disabling all extraneous stuff like plugins and scripts, and automatically connects to your favorite channel, “#erk”, on EFnet? You could use:

python erk.py -o --noextensions --nomenu --nodisplay --nostyles --channel “#erk” irc.efnet.org 6667

And that’s only using the command-line options! Ərk has over 50 different settings available, as well as nearly 20 different command-line options.

When I started writing Ərk, one of my goals was to make it as configurable as possible. I wanted an IRC client that gave the user the tools to make the client look and behave exactly how the user wanted.
Another IRC client? Why not use HexChat?

Honestly? I wanted an IRC client that I liked using, and I wanted an IRC client that I could use in both Windows and Linux. Other than some “connects to every kind of chat network” clients, I didn’t have a lot of choices. Since the only kind of chat I regularly use is IRC, I didn’t care if the client could connect to Jabber, Facebook, or whatever. That left me (in my opinion) with only one choice: HexChat.

HexChat is, well, aging. The last I heard, there was nobody maintaining the source. I wanted a new IRC client written in a modern, accessible language; I wanted a client that was not written in C or C++. I wanted a pretty, attractive client that looks like it was written in the last decade. And, moreover, I wanted a client written for the desktop; I didn’t want one that runs in a web browser, or on a smartphone, or in “the cloud”. I wanted a client that was open source (both free as in beer and free as in speech). I wanted a client that ran fast, consumed resources commensurate with the task of a text-only chat protocol. I wanted a client that wasn’t limited to just text; a client that can send and display emojis.

Since I couldn’t find that IRC client, I decided to write my own.

When I decided to write a new IRC client, I wanted it to feature a few things:

    It had to be open source (free as in speech and as in beer)
    The ability to connect to multiple servers at a time (something almost every open source client does)
    A full, modern GUI (HexChat is sort of modern, I guess, if was still 1999-2000)
    Easy to install, easy to run (if you’re trying to compile HexChat for Windows, good luck, you’ll need it)
    Focuses on the chat experience (not downloading/uploading files)
    The ability to easily extend the client without resorting to Black Magic™ or spend hours and hours surfing endless forum posts or decipher less-than-helpful documentation

Ərk is being developed on Windows 10 and Linux Mint, but it uses no Windows-specific or Linux-specific libraries or functionality. It’s written in pure Python3 and PyQt5, and installing it as easy as cloning this repository, making sure you have Python3 and the other pre-requisites installed, and executing python erk.py. It does IRC, and nothing else, and it looks good doing it.

The other reason why I wrote Ərk is because I got tired of not understanding how the most popular clients did things. I wanted a client that you could configure to do exactly what you wanted it to do, no more and no less. That’s why Ərk has a ridiculous amount of configuration options. Do you want to run the client in full-screen mode, and remove the ability of users to change settings or connect to other servers (aka, “kiosk mode”)? You can do that. Do you want to strip all the “pretty” off the client, and basically run it in “text only” mode? You can do that. Do you want Ərk to do nothing except what you tell it to do? You can do that. Almost everything in the client can be configured from within the GUI or with command-line flags.
Is Ərk designed for multiple users?

Not directly, as all its configuration files are stored in Ərk’s installation directory. However, there are six command-line options you can use to manage settings for different users:

    -C,--config : This tells Ərk to use a user-specified file for most configuration options.
    -U,--user : This tells Ərk to use a user-specified user settings file. Stored in this file are nickname and username settings, server connection history, the disabled plugins list, and other user specific data.
    -Y,--style : This tells Ərk to use a user-specified text style file. This sets what colors and formatting is used to display text in the client.
    -L,--logs : This tells Ərk to use a user-specified directory for log loading and storage.
    -S,--scripts : This tells Ərk to use a user-specified directory for script loading and storage.
    -T,--styles : This tells Ərk to use a user-specified directory for text style loading and storage.
    -M,--macros : This tells Ərk to use a user-specified file for macro loading and storage.

This allows users to set specific configuration files for different users, and can be set in a shortcut or batch file. Configuration and user setting files are JSON, and the text format settings file is CSS. If the filename (or directory name) passed to Ərk is not found, Ərk will create the file and fill it with default settings, or create the directory to be used for logs.

More command-line settings can be viewed by executing Ərk with the --help command-line flag.

For an example of how to implement this for multiple users, let’s assume we have two users, named Alice and Bob. They’re both running Ərk on the same computer (which runs Windows), and want to keep their settings and logs separate. Ərk, in this example, is installed in “C:\Erk”. First, we create a directory for Alice; we’ll put it in the root directory of the “C” drive. We’ll name Alice’s directory “Alice_Erk”:

mkdir C:\Alice_Erk

Now, let’s make a directory for Bob:

mkdir C:\Bob_Erk

We’ll use these directories to store settings and logs. Now, let’s create batch files for both users, ones that start Ərk up with the right commandline flags. Assuming that Python is in Window’s PATH, Alice’s batch file looks like this:

python C:\Erk\erk.py -C C:\Alice_Erk\settings.json -U C:\Alice_Erk\user.json -Y C:\Alice_Erk\text.style -L C:\Alice_Erk\logs -S C:\Alice_Erk\scripts -T C:\Alice\styles -M C:\Alice\macros.json

Similarly, Bob’s batch file looks like this:

python C:\Erk\erk.py -C C:\Bob_Erk\settings.json -U C:\Bob_Erk\user.json -Y C:\Bob_Erk\text.style -L C:\Bob_Erk\logs -S C:\Bob_Erk\scripts -T C:\Bob\styles -M C:\Bob\macros.json

Alice and Bob can now use Ərk with their own customized settings!
