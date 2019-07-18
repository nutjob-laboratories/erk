<p align="center">
	<img src="https://github.com/nutjob-laboratories/erk/raw/master/downloads/images/logo.png"><br>
	<img src="https://github.com/nutjob-laboratories/erk/raw/master/downloads/images/nutjob.png"><br>
	<a href="https://github.com/nutjob-laboratories/erk/raw/master/downloads/erk-0.410-unstable.zip">Download Erk 0.410</a><br>
</p>

**Erk** is a graphical open source [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **0.410**.

# Features

<p align="center">
	<a href="https://github.com/nutjob-laboratories/erk/raw/master/downloads/images/screenshot_full.png"><img src="https://github.com/nutjob-laboratories/erk/raw/master/downloads/images/screenshot.png"></a><br>
	<i>Erk's interface</i>
</p>

* Supports multiple connections (you can chat on more than one IRC server at a time)
* Uses a [multiple document interface](https://en.wikipedia.org/wiki/Multiple_document_interface) (similar to [mIRC](https://www.mirc.com/))
* Automatic channel and private message logging
* A powerful plugin architecture (plugins are written in Python3, just like Quirc)
* A built-in code editor
* Open source ([GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html))
* Extensive commandline configuration options
* Built-in spell checker
* Command/nick/channel auto-completion
* Powerful theme engine using QSS and JSON

# Requirements
**Erk** requires Python 3, Qt5, Twisted, and qt5reactor. Qt5 and Twisted can be installed by downloading and installing the software from their respected websites, or by using [**pip**](https://pypi.org/project/pip/):

    pip install pyqt5
    pip install Twisted
    pip install qt5reactor

To connect to IRC servers via SSL, two additional libraries are needed:

    pip install pyOpenSSL
    pip install service_identity

**Erk** is being developed with Python 3.7.