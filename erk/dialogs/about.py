
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
from erk.strings import *

class Dialog(QDialog):

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("About "+APPLICATION_NAME)
		self.setWindowIcon(QIcon(ABOUT_ICON))

		logo = QLabel()
		pixmap = QPixmap(ERK_BIG_ICON)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		line1 = QLabel("<big><b>"+APPLICATION_NAME+"</b></big>")
		line1.setAlignment(Qt.AlignCenter)
		line2 = QLabel("<b>Open Source IRC Client</b>")
		line2.setAlignment(Qt.AlignCenter)
		line3 = QLabel("<small>Version "+APPLICATION_VERSION+"</small>")
		line3.setAlignment(Qt.AlignCenter)
		line4 = QLabel(f"<a href=\"{OFFICIAL_REPOSITORY}\"><small>Source Code Repository</small></a>")
		line4.setAlignment(Qt.AlignCenter)
		line4.setOpenExternalLinks(True)

		descriptionLayout = QVBoxLayout()
		descriptionLayout.addWidget(line1)
		descriptionLayout.addWidget(line2)
		descriptionLayout.addWidget(line3)
		descriptionLayout.addWidget(line4)

		titleLayout = QHBoxLayout()
		titleLayout.addWidget(logo)
		titleLayout.addLayout(descriptionLayout)


		tech_credit = QLabel(f"<small>Written with </small><a href=\"https://python.org\"><small>Python</small></a><small>, </small><a href=\"https://www.qt.io/\"><small>Qt</small></a><small>, and </small><a href=\"https://twistedmatrix.com/\"><small>Twisted</small></a>")
		tech_credit.setAlignment(Qt.AlignCenter)
		tech_credit.setOpenExternalLinks(True)


		icons_credit = QLabel(f"<small>Icons by </small><a href=\"https://icons8.com/\"><small>Icons8</small></a><small> and </small><a href=\"https://material.io/resources/icons/\"><small>Google</small></a>")
		icons_credit.setAlignment(Qt.AlignCenter)
		icons_credit.setOpenExternalLinks(True)


		spellcheck_credit = QLabel(f"<a href=\"https://github.com/barrust/pyspellchecker\"><small>pyspellchecker</small></a><small> by </small><a href=\"mailto:barrust@gmail.com\"><small>Tyler Barrus</small></a>")
		spellcheck_credit.setAlignment(Qt.AlignCenter)
		spellcheck_credit.setOpenExternalLinks(True)

		emoji_credit = QLabel(f"<a href=\"https://github.com/carpedm20/emoji\"><small>emoji</small></a><small> by </small><a href=\"http://carpedm20.github.io/about/\"><small>Taehoon Kim</small></a><small> and </small><a href=\"http://twitter.com/geowurster/\"><small>Kevin Wurster</small></a>")
		emoji_credit.setAlignment(Qt.AlignCenter)
		emoji_credit.setOpenExternalLinks(True)

		asciimoji_credit = QLabel(f"<a href=\"https://github.com/hpcodecraft/ASCIImoji\"><small>ASCIImoji</small></a><small> by </small><a href=\"mailto:thesquidpeople@gmail.com\"><small>Volker Wieban</small></a>")
		asciimoji_credit.setAlignment(Qt.AlignCenter)
		asciimoji_credit.setOpenExternalLinks(True)

		gnu_credit = QLabel(f"<a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><small>Gnu General Public License 3.0</small></a>")
		gnu_credit.setAlignment(Qt.AlignCenter)
		gnu_credit.setOpenExternalLinks(True)

		creditsBox = QGroupBox()
		creditsBox.setAlignment(Qt.AlignHCenter)

		creditsLayout = QVBoxLayout()
		creditsLayout.addWidget(icons_credit)
		creditsLayout.addWidget(spellcheck_credit)
		creditsLayout.addWidget(emoji_credit)
		creditsLayout.addWidget(asciimoji_credit)
		creditsBox.setLayout(creditsLayout)

		okButton = QPushButton("Ok")
		okButton.clicked.connect(self.close)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(titleLayout)
		finalLayout.addWidget(tech_credit)
		finalLayout.addWidget(creditsBox)
		finalLayout.addWidget(gnu_credit)
		finalLayout.addWidget(okButton)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
