#
#  Erk IRC Client
#  Copyright (C) 2019  Daniel Hetrick
#               _   _       _                         
#              | | (_)     | |                        
#   _ __  _   _| |_ _  ___ | |__                      
#  | '_ \| | | | __| |/ _ \| '_ \                     
#  | | | | |_| | |_| | (_) | |_) |                    
#  |_| |_|\__,_|\__| |\___/|_.__/ _                   
#  | |     | |    _/ |           | |                  
#  | | __ _| |__ |__/_  _ __ __ _| |_ ___  _ __ _   _ 
#  | |/ _` | '_ \ / _ \| '__/ _` | __/ _ \| '__| | | |
#  | | (_| | |_) | (_) | | | (_| | || (_) | |  | |_| |
#  |_|\__,_|_.__/ \___/|_|  \__,_|\__\___/|_|   \__, |
#                                                __/ |
#                                               |___/ 
#  https://github.com/nutjob-laboratories
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from ..resources import *

TEXT_SEPARATOR = f'''
<table width="100%" border="0" cellspacing="2" cellpadding="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
			<td><center><small>!TEXT!</small></center></td>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

LIGHT_TEXT_SEPARATOR = f'''
<table width="100%" border="0" cellspacing="2" cellpadding="0">
	<tbody>
		<tr>
			<td style="background-image: url({LIGHT_HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
			<td><center><small>!TEXT!</small></center></td>
			<td style="background-image: url({LIGHT_HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

E_SEPARATOR = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

LIGHT_E_SEPARATOR = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({LIGHT_HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

PLAIN_TEXT = f'''
<table width="100%" border="0" cellspacing="1" cellpadding="1">
	<tbody>
		<tr>
			<td>&nbsp;&nbsp;!TEXT!&nbsp;&nbsp;</td>
		</tr>
	</tbody>
</table>'''

def textSeparatorLabel(self,text):

	if self.is_light_colored:
		gsep = TEXT_SEPARATOR
	else:
		gsep = LIGHT_TEXT_SEPARATOR

	return QLabel( gsep.replace("!TEXT!",text.upper()) )

def plainTextAction(self,text):
		
	# tsLabel = QLabel( TEXT_SEPARATOR.replace("!TEXT!",text) )
	tsLabel = QLabel( PLAIN_TEXT.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction

def insertNoTextSeparator(self,menu):

	if self.is_light_colored:
		gsep = E_SEPARATOR
	else:
		gsep = LIGHT_E_SEPARATOR
		
	# tsLabel = QLabel( TEXT_SEPARATOR.replace("!TEXT!",text) )
	tsLabel = QLabel( gsep )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	menu.addAction(tsAction)

	return tsAction

def textSeparator(self,text):

	if self.is_light_colored:
		gsep = TEXT_SEPARATOR
	else:
		gsep = LIGHT_TEXT_SEPARATOR

	text = text.upper()
		
	# tsLabel = QLabel( TEXT_SEPARATOR.replace("!TEXT!",text) )
	tsLabel = QLabel( gsep.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction

class MenuLabel(QLabel):
	clicked=pyqtSignal()

	def __init__(self, parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

	def mousePressEvent(self, ev):
		self.clicked.emit()

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			col = self.palette().highlight().color().name()
			highlight = QColor(col).name()

			col = self.palette().highlightedText().color().name()
			highlight_text = QColor(col).name()
			
			self.setStyleSheet(f"background-color: {highlight}; color: {highlight_text};")
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet('')
			return True
		return False

def MenuAction(self,icon,title,description,icon_size,func):

	erkmenuLabel = MenuLabel( menuHtml(icon,title,description,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)
	erkmenuLabel.clicked.connect(func)

	return erkmenuAction

def MenuNoActionRaw(self,icon,title,description,icon_size):

	erkmenuLabel = QLabel( menuHtmlSpaced(icon,title,description,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	return erkmenuAction

def MenuNoAction(self,icon,title,description,icon_size):

	erkmenuLabel = MenuLabel( menuHtml(icon,title,description,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	return erkmenuAction

def Menu3Action(self,icon,title,description,description2,icon_size):

	erkmenuLabel = MenuLabel( menu3Html(icon,title,description,description2,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	return erkmenuAction


def Menu4Action(self,icon,title,description,description2,description3,icon_size):

	erkmenuLabel = MenuLabel( menu4Html(icon,title,description,description2,description3,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	erkmenuLabel.setOpenExternalLinks(True)

	return erkmenuAction

def Menu5Action(self,icon,title,description,description2,description3,description4,icon_size):

	erkmenuLabel = MenuLabel( menu5Html(icon,title,description,description2,description3,description4,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	erkmenuLabel.setOpenExternalLinks(True)

	return erkmenuAction

def menuHtmlSpaced(icon,text,description,icon_size):
	return f'''
<table style="width: 100%" border="0" cellspacing="2" cellpadding="2">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;">&nbsp;<img src="{icon}" width="{icon_size}" height="{icon_size}"></td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: italic; font-weight: normal;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''

def menuHtml(icon,text,description,icon_size):
	return f'''
<table style="width: 100%" border="0" cellspacing="2" cellpadding="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;">&nbsp;<img src="{icon}" width="{icon_size}" height="{icon_size}">&nbsp;</td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: italic; font-weight: normal;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''

def menu3Html(icon,text,description,description2,icon_size):
	return f'''
<table style="width: 100%" border="0" cellspacing="0" cellpadding="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;"><img src="{icon}" width="{icon_size}" height="{icon_size}">&nbsp;</td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-weight: bold;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
				<tr>
				  <td style="font-weight: bold;"><small>{description2}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''

def menu4Html(icon,text,description,description2,description3,icon_size):
	return f'''
<table style="width: 100%" border="0" cellspacing="0" cellpadding="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;"><img src="{icon}" width="{icon_size}" height="{icon_size}">&nbsp;</td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: italic; font-weight: normal;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
				<tr>
				  <td style="font-weight: bold;"><small>{description2}&nbsp;&nbsp;</small></td>
				</tr>
				<tr>
				  <td style="font-weight: bold;"><small>{description3}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''

def menu5Html(icon,text,description,description2,description3,description4,icon_size):
	return f'''
<table style="width: 100%" border="0" cellspacing="0" cellpadding="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;"><img src="{icon}" width="{icon_size}" height="{icon_size}">&nbsp;</td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: italic; font-weight: normal;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
				<tr>
				  <td style="font-weight: normal;"><small>{description2}&nbsp;&nbsp;</small></td>
				</tr>
				<tr>
				  <td style="font-weight: bold;"><small>{description3}<&nbsp;&nbsp;</small> <small>{description4}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''
