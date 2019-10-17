
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *

class Dialog(QDialog):

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("About "+APPLICATION_NAME)
		self.setWindowIcon(QIcon(ABOUT_ICON))

		boldfont = self.font()
		boldfont.setBold(True)
		boldfont.setPointSize(10)

		boldsmaller = self.font()
		boldsmaller.setBold(True)
		boldsmaller.setPointSize(8)

		logo = QLabel()
		pixmap = QPixmap(LOGO_IMAGE)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		qt_image = QLabel()
		pixmap = QPixmap(QT_ICON)
		qt_image.setPixmap(pixmap)
		qt_image.setAlignment(Qt.AlignCenter)

		python_image = QLabel()
		pixmap = QPixmap(PYTHON_ICON)
		python_image.setPixmap(pixmap)
		python_image.setAlignment(Qt.AlignCenter)

		twisted_image = QLabel()
		pixmap = QPixmap(TWISTED_ICON)
		twisted_image.setPixmap(pixmap)
		twisted_image.setAlignment(Qt.AlignCenter)

		icons8_image = QLabel()
		pixmap = QPixmap(ICONS8_ICON)
		icons8_image.setPixmap(pixmap)
		icons8_image.setAlignment(Qt.AlignCenter)

		pyBox = QVBoxLayout()
		pyBox.addWidget(python_image)
		pyLink = QLabel("<a href=\"https://www.python.org/\">Python</a>")
		pyLink.setAlignment(Qt.AlignCenter)
		pyBox.addWidget(pyLink)
		pyLink.setFont(boldsmaller)
		pyLink.setOpenExternalLinks(True)

		qtBox = QVBoxLayout()
		qtBox.addWidget(qt_image)
		qtLink = QLabel("<a href=\"https://www.qt.io/\">Qt</a>")
		qtLink.setAlignment(Qt.AlignCenter)
		qtBox.addWidget(qtLink)
		qtLink.setFont(boldsmaller)
		qtLink.setOpenExternalLinks(True)

		twistBox = QVBoxLayout()
		twistBox.addWidget(twisted_image)
		twistLink = QLabel("<a href=\"https://twistedmatrix.com\">Twisted</a>")
		twistLink.setAlignment(Qt.AlignCenter)
		twistBox.addWidget(twistLink)
		twistLink.setFont(boldsmaller)
		twistLink.setOpenExternalLinks(True)

		icons8Box = QVBoxLayout()
		icons8Box.addWidget(icons8_image)
		icons8Link = QLabel("<a href=\"https://icons8.com/\">Icons8</a>")
		icons8Link.setAlignment(Qt.AlignCenter)
		icons8Box.addWidget(icons8Link)
		icons8Link.setFont(boldsmaller)
		icons8Link.setOpenExternalLinks(True)

		technology = QHBoxLayout()
		technology.addLayout(pyBox)
		technology.addLayout(twistBox)
		technology.addLayout(qtBox)
		technology.addLayout(icons8Box)

		spellcheck_credit = QLabel(f"<a href=\"https://github.com/barrust/pyspellchecker\">pyspellchecker</a> by <a href=\"mailto:barrust@gmail.com\">Tyler Barrus</a>")
		spellcheck_credit.setAlignment(Qt.AlignCenter)
		spellcheck_credit.setFont(boldfont)
		spellcheck_credit.setOpenExternalLinks(True)

		emoji_credit = QLabel(f"<a href=\"https://github.com/carpedm20/emoji\">emoji</a> by <a href=\"http://carpedm20.github.io/about/\">Taehoon Kim</a> and <a href=\"http://twitter.com/geowurster/\">Kevin Wurster</a>")
		emoji_credit.setAlignment(Qt.AlignCenter)
		emoji_credit.setFont(boldfont)
		emoji_credit.setOpenExternalLinks(True)

		asciimoji_credit = QLabel(f"<a href=\"https://github.com/hpcodecraft/ASCIImoji\">ASCIImoji</a> by <a href=\"mailto:thesquidpeople@gmail.com\">Volker Wieban</a>")
		asciimoji_credit.setAlignment(Qt.AlignCenter)
		asciimoji_credit.setFont(boldfont)
		asciimoji_credit.setOpenExternalLinks(True)

		gnu_credit = QLabel(f"<a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><small>Gnu General Public License 3.0</small></a>")
		gnu_credit.setAlignment(Qt.AlignCenter)
		gnu_credit.setFont(boldfont)
		gnu_credit.setOpenExternalLinks(True)

		creditsBox = QGroupBox()
		creditsBox.setAlignment(Qt.AlignHCenter)

		creditsLayout = QVBoxLayout()
		creditsLayout.addLayout(technology)
		creditsLayout.addWidget(spellcheck_credit)
		creditsLayout.addWidget(emoji_credit)
		creditsLayout.addWidget(asciimoji_credit)
		creditsLayout.addWidget(gnu_credit)
		
		creditsBox.setLayout(creditsLayout)

		author_credit = QLabel(f"<small>© Dan Hetrick 2019</small><br><a href=\"{OFFICIAL_REPOSITORY}\"><small>Official Erk Repository</small></a>")
		author_credit.setAlignment(Qt.AlignCenter)
		author_credit.setFont(boldfont)
		author_credit.setOpenExternalLinks(True)

		version = QLabel(f"<big>Version {APPLICATION_VERSION}</big>")
		version.setAlignment(Qt.AlignCenter)
		version.setFont(boldfont)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(logo)
		finalLayout.addWidget(creditsBox)
		finalLayout.addWidget(version)
		finalLayout.addWidget(author_credit)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())