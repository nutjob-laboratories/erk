
<p align="center">
	<img src="https://github.com/nutjob-laboratories/erk/raw/master/images/logo_200x200.png"><br>
	<a href="https://github.com/nutjob-laboratories/erk/releases/tag/0.810.081"><b>Download latest stable release</b></a><br>
	<a href="https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-latest.zip"><b>Download Ərk 0.822</b></a><br>
	<a href="https://github.com/nutjob-laboratories/erk/blob/master/documentation/Erk_Plugin_Guide.pdf"><b>View Ərk plugin documentation</b></a>
</p>

**Ərk** is a graphical open source [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **0.822.171**.

**Ərk** is fully functional for use. Most features are complete, but bugs are still being found and fixed, and features are still being added.

# Screenshots

<p align="center">
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
	<b>Ərk connected to Undernet on Debian Linux</b></td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
</p>

# Features

* **Ərk** does chat, and _only_ chat.
	* **No** [DCC file transfer](https://en.wikipedia.org/wiki/Direct_Client-to-Client) support
	* **No** [Bittorrent](https://en.wikipedia.org/wiki/BitTorrent) client
	* Just plain ol' fashioned IRC
* Runs on Windows and Linux
* Supports multiple connections (you can chat on more than one IRC server at a time)
* Open source ([GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html))
* An extensive set of configuration options
	* Almost every part of the interface can be customized
	* Most behaviors can be customized
* Built-in [spell checker](https://github.com/barrust/pyspellchecker)
	* Supports English, Spanish, French, and German
	* Right click on misspelled words for suggested spellings/words
* [Emoji](https://en.wikipedia.org/wiki/Emoji) support
	* Insert emojis into chat by using shortcodes (such as `:joy:` :joy:, `:yum:` :yum:, etc.)                                                                        |
* Command/nickname auto-completion
	* Type the first few letters of a command or nickname and hit the tab key
	* Auto-complete works for emoji shortcodes, too
* Optional profanity filter
* Support for IRC color codes (and the option to turn them off)
* A built-in list of over 80 IRC servers to connect to
* Automatic logging of channel and private chats
	* Logging can be switched on and off
	* Logs can be automatically loaded when resuming public or private chats
* Powerful macro engine
	* Users can create and edit macros directly in the client
	* Macros can send messages or execute commands
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

**Ərk** is being developed with Python 3.7 on Windows 10.

To run properly on Linux, the latest version of all required software is recommended.  If you are running Debian or Debian-variant (such as Mint, Ubuntu, Xubuntu, etc) **you must install PyQt5, Twisted, and qt5reactor from pip! If you install these from the standard repo Ərk will not function!**

# Install

First, make sure that all the requirements are installed. Next, [download **Ərk**](https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-latest.zip). Extract the zipfile to a directory of your choice using your favorite archive/zip program. Open a command prompt, navigate to the directory you extracted **Ərk** to, and type:

	python erk.py

Hit enter, and **Ərk** will start up! Click "Connect" on the **Ərk** menu to enter a server hostname/IP and port to connect to a specific IRC server, or click "Networks" to select a server from the built-in server list.

**Ərk** does not need to be "installed" to any specific directory to run; it will run from any directory it is extracted to.

To make things easier, Windows users can create a shortcut to **Ərk** so all you have to do is double click to start chatting. There are many tutorials on how to do this online; a good place to start is [right here](https://therenegadecoder.com/code/how-to-make-a-python-script-shortcut-with-arguments/).

# Frequently asked questions

## What does "erk" mean?

The previous name for this client was "Quirc", but after working on it for a while, I discovered that there was already an IRC client named [Quirc](https://quirc.org/). I was asking for some name suggestions in IRC, when one of the users in the channel suggested "Erk", because "that's how you pronouce IRC". And thus **Ərk** was born.

## Is **Ərk** completed?

No. I'm still adding features and tracking down and squashing bugs.

## Can I use **Ərk** to chat on IRC?

Yes! Most basic functionality is done, and it's ready for most IRC stuff.

## Does **Ərk** run on Windows? Does it run on Linux?

**Ərk** runs on both Windows and Linux! It's being developed on Windows 10, but it's been tested (and runs great) on Debian, Ubuntu, and Mint Linux. I can't think of a reason why **Ərk** wouldn't run on OSX, but I don't have access to an Apple computer to test this.

## Another IRC client? Why not use HexChat?

HexChat is, well, aging. The last I heard, there was nobody maintaining the source. I wanted a new IRC client written in a modern, accessible language; I wanted a client that was *not* written in C or C++. I wanted a pretty, attractive client that looks like it was written in the last decade. And, moreover, I wanted a client written for the desktop; I didn't want one that runs in a web browser, or on a smartphone, or in "the cloud". I wanted a client that was open source (both free as in beer and free as in speech).  I wanted a client that ran fast, consumed resources commensurate with the task of a text-only chat protocol.  I wanted a client that wasn't limited to just text;  a client that can send and display emojis.

Since I couldn't find that IRC client, I decided to write my own.

When I decided to write a new IRC client, I wanted it to feature a few things:

* It had to be open source (free as in speech and as in beer)
* The ability to connect to multiple servers at a time (something almost every open source client does)
* A full, modern GUI (HexChat is sort of modern, I guess, if was still 1999-2000)
* Easy to install, easy to run (if you're trying to compile HexChat for Windows, good luck, you'll need it)
* Focuses on the chat experience (not downloading/uploading files)

**Ərk** is being developed on Windows 10, but it uses no Windows-specific libraries or functionality. It's written in pure Python3 and PyQt5, and installing it as easy as cloning this repo, making sure you have Python3 and the other pre-requisites installed, and executing `python erk.py`. It does IRC, and nothing else, and it looks good doing it.

The other reason why I wrote **Ərk** is because I got tired of not understanding how the most popular clients did things. I wanted a client that you could configure to do _exactly_ what you wanted it to do, no more and no less. That's why **Ərk** has a ridiculous amount of configuration options. Do you want to run the client in full-screen mode, and remove the ability of users to change settings or connect to other servers (aka, "kiosk mode")? You can do that. Do you want to strip all the "pretty" off the client, and basically run it in "text only" mode? You can do that. Do you want **Ərk** to do nothing except what you tell it to do? You can do that. Almost everything in the client can be configured from within the GUI or with command-line flags.

## Is **Ərk** designed for multiple users?

Not directly, as all its configuration files are stored in **Ərk**'s installation directory. However, there are three command-line options you can use to manage settings for different users:

* `--config` : This tells **Ərk** to use a user-specified file for most configuration options.
* `--user` : This tells **Ərk** to use a user-specified user settings file. Stored in this file are nickname and username settings, server connection history, the disabled plugins list, and other user specific data.
* `--format` : This tells **Ərk** to use a user-specified text display settings file. This sets what colors and formatting is used to display text in the client.
* `--logs` : This tells **Ərk** to use a user-specified directory for log loading and storage.

This allows users to set specific configuration files for different users, and can be set in a shortcut or batch file. Configuration and user setting files are JSON, and the text format settings file is CSS. If the filename (or directory name) passed to **Ərk** is not found, **Ərk** will create the file and fill it with default settings, or create the directory to be used for logs.

More command-line settings can be viewed by executing **Ərk** with the `--help` command-line flag.

For an example of how to implement this for multiple users, let's assume we have two users, named Alice and Bob. They're both running **Ərk** on the same computer (which runs Windows), and want to keep their settings and logs separate. **Ərk**, in this example, is installed in "C:\Erk". First, we create a directory for Alice; we'll put it in the root directory of the "C" drive. We'll name Alice's directory "Alice_Erk":

	mkdir C:\Alice_Erk

Now, let's make a directory for Bob:

	mkdir C:\Bob_Erk

We'll use these directories to store settings and logs. Now, let's create batch files for both users, ones that start **Ərk** up with the right commandline flags. Assuming that Python is in Window's PATH, Alice's batch file looks like this:

	python C:\Erk\erk.py --config C:\Alice_Erk\settings.json --user C:\Alice_Erk\user.json --format C:\Alice_Erk\text.css --logs C:\Alice_Erk\logs

Similarly, Bob's batch file looks like this:

	python C:\Erk\erk.py --config C:\Bob_Erk\settings.json --user C:\Bob_Erk\user.json --format C:\Bob_Erk\text.css --logs C:\Bob_Erk\logs

Alice and Bob can now use **Ərk** with their own customized settings!
