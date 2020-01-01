
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.resources import *
import erk.dialogs.find as Find

INSTALL_DIRECTORY = sys.path[0]
PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")

class Window(QMainWindow):

	def closeEvent(self, event):
		if self.changed:
			self.doExitSave(self.filename)

		self.close()

	def docModified(self):
		if self.changed: return
		self.changed = True
		self.title = "* "+self.title
		self.setWindowTitle(self.title)

	def doNewFile(self):
		if self.changed:
			self.doExitSave(self.filename)

		self.filename = ''
		self.editor.clear()
		self.title = "Editor"
		self.setWindowTitle(self.title)
		self.changed = False
		self.menuSave.setEnabled(False)
		if self.findWindow != None:
			self.findWindow.setWindowTitle("Find")

	def doFileSaveAs(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Plugin As...",PLUGIN_DIRECTORY,"Python File (*.py);;All Files (*)", options=options)
		if fileName:
			if '.py' in fileName:
				pass
			else:
				fileName = fileName + '.py'
			self.filename = fileName
			code = open(fileName,"w")
			code.write(self.editor.toPlainText())
			self.title = os.path.basename(fileName)
			self.setWindowTitle(self.title)
			self.changed = False
			self.menuSave.setEnabled(True)
			if self.findWindow != None:
				self.findWindow.setWindowTitle(self.title)

	def doFileSave(self):
		code = open(self.filename,"w")
		code.write(self.editor.toPlainText())
		self.setWindowTitle(self.title)
		self.changed = False
		if self.findWindow != None:
			self.findWindow.setWindowTitle(self.title)

	def doFileOpen(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Plugin", PLUGIN_DIRECTORY,"Python File (*.py);;All Files (*)", options=options)
		if fileName:
			script = open(fileName,"r")
			self.editor.setPlainText(script.read())
			self.filename = fileName
			self.menuSave.setEnabled(True)
			self.title = os.path.basename(fileName)
			self.setWindowTitle(self.title)
			self.changed = False
			if self.findWindow != None:
				self.findWindow.setWindowTitle(self.title)

	def doExitSave(self,default):
		if not default: default = PLUGIN_DIRECTORY
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Plugin As...",default,"Python File (*.py);;All Files (*)", options=options)
		if fileName:
			if '.py' in fileName:
				pass
			else:
				fileName = fileName + '.py'
			self.filename = fileName
			code = open(fileName,"w")
			code.write(self.editor.toPlainText())

	def hasUndo(self,avail):
		if avail:
			self.menuUndo.setEnabled(True)
		else:
			self.menuUndo.setEnabled(False)

	def hasRedo(self,avail):
		if avail:
			self.menuRedo.setEnabled(True)
		else:
			self.menuRedo.setEnabled(False)

	def hasCopy(self,avail):
		if avail:
			self.menuCopy.setEnabled(True)
			self.menuCut.setEnabled(True)
		else:
			self.menuCopy.setEnabled(False)
			self.menuCut.setEnabled(False)

	def doFind(self):

		if self.findWindow != None:
			self.findWindow.setWindowTitle(self.title)
			self.findWindow.showNormal()
			return

		self.findWindow = Find.Dialog(self)
		if self.filename:
			self.findWindow.setWindowTitle(self.title)
		self.findWindow.show()
		return

	def __init__(self,filename=None,obj=None,parent=None):
		super(Window, self).__init__(parent)

		self.filename = filename
		self.gui = obj

		self.changed = False
		self.findWindow = None

		if self.filename:
			self.title = os.path.basename(self.filename)
			self.setWindowTitle(self.title)
		else:
			self.setWindowTitle("Editor")
			self.title = "Editor"
		self.setWindowIcon(QIcon(EDITOR_ICON))

		# Use spaces for indent
		self.indentspace = True

		# Number of spaces for indent
		self.tabsize = 2

		self.editor = QCodeEditor(self)
		self.highlight = PythonHighlighter(self.editor.document())

		self.editor.textChanged.connect(self.docModified)
		self.editor.redoAvailable.connect(self.hasRedo)
		self.editor.undoAvailable.connect(self.hasUndo)
		self.editor.copyAvailable.connect(self.hasCopy)

		self.setCentralWidget(self.editor)

		if self.filename:
			if os.path.isfile(self.filename):
				x = open(self.filename,mode="r")
				source_code = str(x.read())
				x.close()
				self.editor.setPlainText(source_code)
				self.changed = False
				self.title = os.path.basename(self.filename)
				self.setWindowTitle(self.title)

		self.menubar = self.menuBar()

		fileMenu = self.menubar.addMenu("File")

		entry = QAction(QIcon(NEWFILE_ICON),"New",self)
		entry.triggered.connect(self.doNewFile)
		entry.setShortcut("Ctrl+N")
		fileMenu.addAction(entry)

		entry = QAction(QIcon(OPENFILE_ICON),"Open file",self)
		entry.triggered.connect(self.doFileOpen)
		entry.setShortcut("Ctrl+O")
		fileMenu.addAction(entry)

		self.menuSave = QAction(QIcon(SAVEFILE_ICON),"Save file",self)
		self.menuSave.triggered.connect(self.doFileSave)
		self.menuSave.setShortcut("Ctrl+S")
		fileMenu.addAction(self.menuSave)
		if not self.filename:
			self.menuSave.setEnabled(False)

		entry = QAction(QIcon(SAVEASFILE_ICON),"Save as...",self)
		entry.triggered.connect(self.doFileSaveAs)
		fileMenu.addAction(entry)

		fileMenu.addSeparator()

		entry = QAction(QIcon(QUIT_ICON),"Quit",self)
		entry.triggered.connect(self.close)
		fileMenu.addAction(entry)

		editMenu = self.menubar.addMenu("Edit")

		mefind = QAction(QIcon(WHOIS_ICON),"Find",self)
		mefind.triggered.connect(self.doFind)
		mefind.setShortcut("Ctrl+F")
		editMenu.addAction(mefind)

		editMenu.addSeparator()

		entry = QAction(QIcon(SELECTALL_ICON),"Select All",self)
		entry.triggered.connect(self.editor.selectAll)
		entry.setShortcut("Ctrl+A")
		editMenu.addAction(entry)

		editMenu.addSeparator()

		self.menuUndo = QAction(QIcon(UNDO_ICON),"Undo",self)
		self.menuUndo.triggered.connect(self.editor.undo)
		self.menuUndo.setShortcut("Ctrl+Z")
		editMenu.addAction(self.menuUndo)
		self.menuUndo.setEnabled(False)

		self.menuRedo = QAction(QIcon(REDO_ICON),"Redo",self)
		self.menuRedo.triggered.connect(self.editor.redo)
		self.menuRedo.setShortcut("Ctrl+Y")
		editMenu.addAction(self.menuRedo)
		self.menuRedo.setEnabled(False)

		editMenu.addSeparator()

		self.menuCut = QAction(QIcon(CUT_ICON),"Cut",self)
		self.menuCut.triggered.connect(self.editor.cut)
		self.menuCut.setShortcut("Ctrl+X")
		editMenu.addAction(self.menuCut)
		self.menuCut.setEnabled(False)

		self.menuCopy = QAction(QIcon(COPY_ICON),"Copy",self)
		self.menuCopy.triggered.connect(self.editor.copy)
		self.menuCopy.setShortcut("Ctrl+C")
		editMenu.addAction(self.menuCopy)
		self.menuCopy.setEnabled(False)

		entry = QAction(QIcon(CLIPBOARD_ICON),"Paste",self)
		entry.triggered.connect(self.editor.paste)
		entry.setShortcut("Ctrl+V")
		editMenu.addAction(entry)

		editMenu.addSeparator()

		entry = QAction(QIcon(PLUS_ICON),"Zoom in",self)
		entry.triggered.connect(self.editor.zoomIn)
		entry.setShortcut("Ctrl++")
		editMenu.addAction(entry)

		entry = QAction(QIcon(MINUS_ICON),"Zoom out",self)
		entry.triggered.connect(self.editor.zoomOut)
		entry.setShortcut("Ctrl+-")
		editMenu.addAction(entry)


# Editor widgets/etc

def format(color, style=''):
	"""Return a QTextCharFormat with the given attributes.
	"""
	_color = QColor()
	_color.setNamedColor(color)

	_format = QTextCharFormat()
	_format.setForeground(_color)
	if 'bold' in style:
		_format.setFontWeight(QFont.Bold)
	if 'italic' in style:
		_format.setFontItalic(True)

	return _format


# Syntax styles that can be shared by all languages
STYLES = {
	'keyword': format('blue'),
	'operator': format('red'),
	'brace': format('darkGray'),
	'defclass': format('black', 'bold'),
	'string': format('magenta'),
	'string2': format('darkMagenta'),
	'comment': format('darkGreen', 'italic'),
	'self': format('black', 'italic'),
	'numbers': format('brown'),
}


class PythonHighlighter (QSyntaxHighlighter):
	"""Syntax highlighter for the Python language.
	"""
	# Python keywords
	keywords = [
		'and', 'assert', 'break', 'class', 'continue', 'def',
		'del', 'elif', 'else', 'except', 'exec', 'finally',
		'for', 'from', 'global', 'if', 'import', 'in',
		'is', 'lambda', 'not', 'or', 'pass', 'print',
		'raise', 'return', 'try', 'while', 'yield',
		'None', 'True', 'False',
		# Erk specific stuff
		'self.print','self.console','self.write','self.log',
		'Plugin'
	]

	# Python operators
	operators = [
		'=',
		# Comparison
		'==', '!=', '<', '<=', '>', '>=',
		# Arithmetic
		'\+', '-', '\*', '/', '//', '\%', '\*\*',
		# In-place
		'\+=', '-=', '\*=', '/=', '\%=',
		# Bitwise
		'\^', '\|', '\&', '\~', '>>', '<<',
	]

	# Python braces
	braces = [
		'\{', '\}', '\(', '\)', '\[', '\]',
	]
	def __init__(self, document):
		QSyntaxHighlighter.__init__(self, document)

		# Multi-line strings (expression, flag, style)
		# FIXME: The triple-quotes in these two lines will mess up the
		# syntax highlighting from this point onward
		self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
		self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

		rules = []

		# Keyword, operator, and brace rules
		rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
			for w in PythonHighlighter.keywords]
		rules += [(r'%s' % o, 0, STYLES['operator'])
			for o in PythonHighlighter.operators]
		rules += [(r'%s' % b, 0, STYLES['brace'])
			for b in PythonHighlighter.braces]

		# All other rules
		rules += [
			# 'self'
			(r'\bself\b', 0, STYLES['self']),

			# Double-quoted string, possibly containing escape sequences
			(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
			# Single-quoted string, possibly containing escape sequences
			(r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

			# 'def' followed by an identifier
			(r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
			# 'class' followed by an identifier
			(r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

			# From '#' until a newline
			(r'#[^\n]*', 0, STYLES['comment']),

			# Numeric literals
			(r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
		]

		# Build a QRegExp for each pattern
		self.rules = [(QRegExp(pat), index, fmt)
			for (pat, index, fmt) in rules]


	def highlightBlock(self, text):
		"""Apply syntax highlighting to the given block of text.
		"""
		# Do other syntax formatting
		for expression, nth, format in self.rules:
			index = expression.indexIn(text, 0)

			while index >= 0:
				# We actually want the index of the nth match
				index = expression.pos(nth)
				# length = expression.cap(nth).length()
				length = len(expression.cap(nth))
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		# Do multi-line strings
		in_multiline = self.match_multiline(text, *self.tri_single)
		if not in_multiline:
			in_multiline = self.match_multiline(text, *self.tri_double)


	def match_multiline(self, text, delimiter, in_state, style):
		"""Do highlighting of multi-line strings. ``delimiter`` should be a
		``QRegExp`` for triple-single-quotes or triple-double-quotes, and
		``in_state`` should be a unique integer to represent the corresponding
		state changes when inside those strings. Returns True if we're still
		inside a multi-line string when this function is finished.
		"""
		# If inside triple-single quotes, start at 0
		if self.previousBlockState() == in_state:
			start = 0
			add = 0
		# Otherwise, look for the delimiter on this line
		else:
			start = delimiter.indexIn(text)
			# Move past this match
			add = delimiter.matchedLength()

		# As long as there's a delimiter match on this line...
		while start >= 0:
			# Look for the ending delimiter
			end = delimiter.indexIn(text, start + add)
			# Ending delimiter on this line?
			if end >= add:
				length = end - start + add + delimiter.matchedLength()
				self.setCurrentBlockState(0)
			# No; multi-line string
			else:
				self.setCurrentBlockState(in_state)
				# length = text.length() - start + add
				length = len(text) - start + add
			# Apply formatting
			self.setFormat(start, length, style)
			# Look for the next match
			start = delimiter.indexIn(text, start + length)

		# Return True if still inside a multi-line string, False otherwise
		if self.currentBlockState() == in_state:
			return True
		else:
			return False

class QLineNumberArea(QWidget):
	def __init__(self, editor):
		super().__init__(editor)
		self.codeEditor = editor

	def sizeHint(self):
		return QSize(self.editor.lineNumberAreaWidth(), 0)

	def paintEvent(self, event):
		self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.lineNumberArea = QLineNumberArea(self)
		self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
		self.updateRequest.connect(self.updateLineNumberArea)
		self.cursorPositionChanged.connect(self.highlightCurrentLine)
		self.updateLineNumberAreaWidth(0)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Tab:
			if self.parent.indentspace:
				t = " " * self.parent.tabsize
			else:
				t = "\t"
			self.insertPlainText(t)
			return
		
		super().keyPressEvent(event)

	def lineNumberAreaWidth(self):
		digits = 1
		max_value = max(1, self.blockCount())
		while max_value >= 10:
			max_value /= 10
			digits += 1
		space = 3 + self.fontMetrics().width('9') * digits
		return space

	def updateLineNumberAreaWidth(self, _):
		self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

	def updateLineNumberArea(self, rect, dy):
		if dy:
			self.lineNumberArea.scroll(0, dy)
		else:
			self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
		if rect.contains(self.viewport().rect()):
			self.updateLineNumberAreaWidth(0)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		cr = self.contentsRect()
		self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

	def highlightCurrentLine(self):
		extraSelections = []
		if not self.isReadOnly():
			selection = QTextEdit.ExtraSelection()
			lineColor = QColor(Qt.yellow).lighter(160)
			selection.format.setBackground(lineColor)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extraSelections.append(selection)
		self.setExtraSelections(extraSelections)

	def lineNumberAreaPaintEvent(self, event):
		painter = QPainter(self.lineNumberArea)

		painter.fillRect(event.rect(), Qt.lightGray)

		block = self.firstVisibleBlock()
		blockNumber = block.blockNumber()
		top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
		bottom = top + self.blockBoundingRect(block).height()

		# Just to make sure I use the right font
		height = self.fontMetrics().height()
		while block.isValid() and (top <= event.rect().bottom()):
			if block.isVisible() and (bottom >= event.rect().top()):
				number = str(blockNumber + 1)
				painter.setPen(Qt.black)
				painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

			block = block.next()
			top = bottom
			bottom = top + self.blockBoundingRect(block).height()
			blockNumber += 1

	