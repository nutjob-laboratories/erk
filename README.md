
<p align="center">
	<img src="https://github.com/nutjob-laboratories/erk/raw/master/downloads/images/erk_keyboard_logo.png"><br>
	<a href="https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-latest.zip"><b>Download Erk 0.413</b></a><br>
	<a href="https://github.com/nutjob-laboratories/erk-theme">Theme Compiler Repository</a><br>
</p>

**Erk** is a graphical open source [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **0.413.16**.

**Erk** is fully functional for use. Features are still being added/completed and bugs are being fixed, but it is ready for daily use.

# Features

<p align="center">
	<a href="https://github.com/nutjob-laboratories/erk/raw/master/downloads/images/screenshot_full.png"><img src="https://github.com/nutjob-laboratories/erk/raw/master/downloads/images/screenshot.png"></a>
</p>

* Supports multiple connections (you can chat on more than one IRC server at a time)
* Uses a [multiple document interface](https://en.wikipedia.org/wiki/Multiple_document_interface) (similar to [mIRC](https://www.mirc.com/))
* Open source ([GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html))
* Extensive commandline configuration options
	* More than 30 commandline options
	* Options include:
		* `--fullscreen` to launch **Erk** in full screen mode
		* `--ontop` to display the **Erk** client "on top" of all other windows
		* `--nologs` to prevent chat logging
		* ...and many more!
* Built-in [spell checker](https://github.com/barrust/pyspellchecker)
	* Supports English, Spanish, French, and German
	* Right click on misspelled words for suggested spellings/words
* A theme engine using [QSS](https://doc.qt.io/qt-5/stylesheet-syntax.html) and [JSON](https://www.json.org/)
	* Nearly every aspect of the client, from widgets to icons, can be customized
* All configuration files use JSON
	* Setting files can be exported to a zip archive
	* Setting files can be imported from a zip archive
* Command/nick/channel auto-completion
	* Type the first few letters of a command, nickname, or channel, and hit the tab key
* [Emoji](https://en.wikipedia.org/wiki/Emoji) and [ASCIImoji](https://github.com/hpcodecraft/ASCIImoji) support
	* Insert emojis into chat by using shortcodes (such as `:joy:` :joy:, `:yum:` :yum:, etc.)
	* Insert ASCIImois into chat by using shortcodes (such as `(bear)` ʕ·͡ᴥ·ʔ or `(hug)` (づ｡◕‿‿◕｡)づ)
* Optional audio notifications
	* Notify if unread chat messages are received
	* Notify if your nickname is mentioned in public chat
* Server connection history
	* **Erk** will remember every server it connects to
* Optional profanity filter
* An extremely customizable interface
* Automatic channel and private message logging


# Requirements
**Erk** requires Python 3, [PyQt5](https://pypi.org/project/PyQt5/), [Twisted](https://twistedmatrix.com/trac/), and [qt5reactor](https://github.com/sunu/qt5reactor). PyQt5, Twisted, and qt5reactor can be manually installed, or by using [**pip**](https://pypi.org/project/pip/):

    pip install pyqt5
    pip install Twisted
    pip install qt5reactor

To connect to IRC servers via SSL, two additional libraries are needed:

    pip install pyOpenSSL
    pip install service_identity

**Erk** is being developed with Python 3.7.

# Frequently asked questions

## What does "erk" mean?

The previous name for this client was "Quirc", but after working on it for a while, I discovered that there was already an IRC client named [Quirc](https://quirc.org/). I was asking for some name suggestions in IRC, when one of the users in the channel suggested "Erk", because "that's how you pronouce IRC". And thus **Erk** was born.

## Another IRC client? Why not use HexChat?

Mostly because I don't like HexChat's interface.  I started using IRC in the mid to late 90's, and the first client I used regularly was mIRC.  I liked the simplicity of that client in the early days of IRC, and I felt like most modern IRC clients were either u/linux-centric, focused on everything **but** chat, or weird command-line-style interfaces grafted onto a half-thought out GUI.  I wanted to use an IRC client I actually enjoyed using, and since I haven't found one yet, the only thing left to do was create one.

When I decided to write a new IRC client, I wanted it to feature a few things:

* It had to be open source (free as in speech and as in beer)
* The ability to connect to multiple servers at a time (something almost every open source client does)
* A full, modern GUI (HexChat is sort of modern, I guess)
* A [multiple document interface](https://en.wikipedia.org/wiki/Multiple_document_interface) (I've heard that KVIrc does this)
* Easy to install, easy to run (if you're trying to compile HexChat for Windows, good luck, you'll need it)
* Focuses on the chat experience (not downloading/uploading files)
* Cross-platform without having to jump through hoops

**Erk** is being developed on Windows 10, but it uses no Windows-specific libraries or functionality. It's written in pure Python3 and PyQt5, and installing it as easy as cloning this repo, making sure you have Python3 and the other pre-requisites installed, and executing `python erk.py`. It does IRC, and nothing else, and it looks good doing it.