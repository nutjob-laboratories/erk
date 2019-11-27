
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from .menubar import generate_menu_toolbar,add_toolbar_menu,end_toolbar_menu
from erk.resources import *
from erk.common import *
from erk.config import *

DEFAULT_APPLICATION_STYLE = 'Windows'

MENU_ICON_SIZE = 26
MENU_ICON_SMALL_SIZE = 20
MENU_MODE_ICON_SIZE = 22


TEXT_RIGHT_SEPARATOR = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">!SPACE!
			</td>
			<td style="text-align: right; vertical-align: middle;"><small>!TEXT!</small></td>
		</tr>
	</tbody>
</table>'''

def textRightSeparator(self,text):

	html = TEXT_RIGHT_SEPARATOR.replace("!TEXT!",text+"&nbsp;")
	html = html.replace("!SPACE!", '&nbsp;'*1     )

	tsLabel = QLabel( html  )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction






TEXT_SEPARATOR = f'''
<table width="100%" border="0">
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

def textSeparator(self,text):

	tsLabel = QLabel( TEXT_SEPARATOR.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction

class QHLine(QFrame):
	def __init__(self):
		super(QHLine, self).__init__()
		self.setFrameShape(QFrame.HLine)
		self.setFrameShadow(QFrame.Sunken)

class LargerIconsMenuStyle(QProxyStyle):
	def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

		if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
			return MENU_ICON_SIZE
		else:
			return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)

class SmallerIconsMenuStyle(QProxyStyle):
	def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

		if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
			return MENU_ICON_SMALL_SIZE
		else:
			return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)

class MainMenuBarStyle(QProxyStyle):
	def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

		if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
			return 18
		else:
			return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


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
		return False

def fancyMenu(self,icon,title,description,func):

	erkmenuLabel = MenuLabel( menuHtml(icon,title,description) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)
	erkmenuLabel.clicked.connect(func)

	return erkmenuAction

def menuHtml(icon,text,description):
	return f'''
<table style="width: 100%" border="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;"><img src="{icon}" width="{MENU_ICON_SIZE}" height="{MENU_ICON_SIZE}">&nbsp;</td>
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

def clearQTreeWidget(tree):
	iterator = QTreeWidgetItemIterator(tree, QTreeWidgetItemIterator.All)
	while iterator.value():
		iterator.value().takeChildren()
		iterator +=1
	i = tree.topLevelItemCount()
	while i > -1:
		tree.takeTopLevelItem(i)
		i -= 1

def buildConnectionDisplay(self):

	fm = QFontMetrics(self.app.font())
	fheight = fm.height() + 4
	fwidth = fm.width('X') * 27

	class LogWidget(QTreeWidget):

		def __init__(self,parent=None):
			self.started = True
			super(LogWidget, self).__init__(parent)

		def sizeHint(self):
			if self.started:
				self.started = False
				return QSize(fwidth, self.height())
			return QSize(self.width(), self.height())

	self.connectionTree = LogWidget()
	self.connectionTree.headerItem().setText(0,"1")
	self.connectionTree.header().setVisible(False)

	self.connectionTree.setSelectionMode(QAbstractItemView.NoSelection)
	
	self.connectionTree.setIconSize(QSize(fheight,fheight))

	self.connectionTree.itemDoubleClicked.connect(self.connectionNodeDoubleClicked)

	self.connectionTree.setFocusPolicy(Qt.NoFocus)

	self.connectionTree.setStyleSheet(self.styles[BASE_STYLE_NAME])

	text_color = get_style_attribute(self.styles[BASE_STYLE_NAME],"color")
	if not text_color: text_color = "#000000"

	user_display_qss='''
		QTreeWidget::item {
			border: 0px;
			color: !TEXT_COLOR!;
		}
		QTreeWidget {
			show-decoration-selected: 0;
		}
	'''
	user_display_qss = user_display_qss.replace('!TEXT_COLOR!',text_color)
	user_display_qss = user_display_qss + self.styles[BASE_STYLE_NAME]

	self.connectionTree.setStyleSheet(user_display_qss)

	connectionDisplay = QDockWidget(self)
	connectionDisplay.setWidget(self.connectionTree)
	connectionDisplay.setFloating(False)

	connectionDisplay.setAllowedAreas(Qt.AllDockWidgetAreas)

	connectionDisplay.setFeatures( QDockWidget.NoDockWidgetFeatures )
	connectionDisplay.setTitleBarWidget(QWidget())

	return connectionDisplay

def menuIconLabel(self,icon,title):

	erkmenuLabel = QLabel( menuIconLabel_Html(icon,title) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	return erkmenuAction

def menuIconLabel_Html(icon,text):
	return f'''
<table style="width: 100%" border="0">
      <tbody>
        <tr>
          <td style="text-align: center; vertical-align: middle;"><img src="{icon}" width="{MENU_MODE_ICON_SIZE}" height="{MENU_MODE_ICON_SIZE}">&nbsp;</td>
          <td style="vertical-align: middle;">{text}&nbsp;&nbsp;</td>
        </tr>
      </tbody>
    </table>
    '''

def menuPlainLabel(self,title):

	erkmenuLabel = QLabel( menuPlainLabel_Html(title) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	return erkmenuAction

def menuPlainLabel_Html(text):
	return f'''
<table style="width: 100%" border="0">
      <tbody>
        <tr>
        <td>&nbsp;{text}&nbsp;</td>
        </tr>
      </tbody>
    </table>
        '''
