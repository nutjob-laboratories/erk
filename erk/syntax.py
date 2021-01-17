
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from . import config

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
	if 'bi' in style:
		_format.setFontWeight(QFont.Bold)
		_format.setFontItalic(True)

	return _format

# STYLES = {
# 	'comments': format('darkMagenta','bold'),
# 	'erk': format('darkBlue','bold'),
# 	'channel': format('darkRed','bold'),
# 	'alias': format('darkGreen','bold'),
# }

STYLES = {
	'comments': format(config.SCRIPT_SYNTAX_COMMENTS,'bold'),
	'erk': format(config.SCRIPT_SYNTAX_COMMANDS,'bold'),
	'channel': format(config.SCRIPT_SYNTAX_TARGETS,'bold'),
	'alias': format(config.SCRIPT_SYNTAX_ALIAS,'bold'),
}

class ErkScriptHighlighter (QSyntaxHighlighter):

	erk = [
		config.INPUT_COMMAND_SYMBOL+'away',
		config.INPUT_COMMAND_SYMBOL+'back',
		config.INPUT_COMMAND_SYMBOL+'invite',
		config.INPUT_COMMAND_SYMBOL+'join',
		config.INPUT_COMMAND_SYMBOL+'list',
		config.INPUT_COMMAND_SYMBOL+'me',
		config.INPUT_COMMAND_SYMBOL+'msg',
		config.INPUT_COMMAND_SYMBOL+'nick',
		config.INPUT_COMMAND_SYMBOL+'notice',
		config.INPUT_COMMAND_SYMBOL+'oper',
		config.INPUT_COMMAND_SYMBOL+'part',
		config.INPUT_COMMAND_SYMBOL+'quit',
		config.INPUT_COMMAND_SYMBOL+'send',
		config.INPUT_COMMAND_SYMBOL+'time',
		config.INPUT_COMMAND_SYMBOL+'topic',
		config.INPUT_COMMAND_SYMBOL+'version',
		config.INPUT_COMMAND_SYMBOL+'who',
		config.INPUT_COMMAND_SYMBOL+'whois',
		config.INPUT_COMMAND_SYMBOL+'whowas',
		config.INPUT_COMMAND_SYMBOL+'alias',
		config.INPUT_COMMAND_SYMBOL+'argcount',
		config.INPUT_COMMAND_SYMBOL+'connect',
		config.INPUT_COMMAND_SYMBOL+'connectscript',
		config.INPUT_COMMAND_SYMBOL+'exit',
		config.INPUT_COMMAND_SYMBOL+'help',
		config.INPUT_COMMAND_SYMBOL+'print',
		config.INPUT_COMMAND_SYMBOL+'reconnect',
		config.INPUT_COMMAND_SYMBOL+'refresh',
		config.INPUT_COMMAND_SYMBOL+'ressl',
		config.INPUT_COMMAND_SYMBOL+'script',
		config.INPUT_COMMAND_SYMBOL+'settings',
		config.INPUT_COMMAND_SYMBOL+'ssl',
		config.INPUT_COMMAND_SYMBOL+'style',
		config.INPUT_COMMAND_SYMBOL+'switch',
		config.INPUT_COMMAND_SYMBOL+'wait',
		config.INPUT_COMMAND_SYMBOL+'_alias',
		config.INPUT_COMMAND_SYMBOL+'macro',
		config.INPUT_COMMAND_SYMBOL+'macrohelp',
		config.INPUT_COMMAND_SYMBOL+'unmacro',
		config.INPUT_COMMAND_SYMBOL+'edit',
		config.INPUT_COMMAND_SYMBOL+'clear',
		config.INPUT_COMMAND_SYMBOL+'msgbox',
		config.INPUT_COMMAND_SYMBOL+'macrousage',
	]


	def __init__(self, document):
		QSyntaxHighlighter.__init__(self, document)

		# Comments
		self.script_comments = (QRegExp("(\\/\\*|\\*\\/|\n)"), 1, STYLES['comments'])

		rules = []

		# Commands
		rules += [(r'%s' % o, 0, STYLES['erk'])
			for o in ErkScriptHighlighter.erk]

		# Make sure to escape any special characters in the
		# interpolation symbol; this also allows for interpolation
		# symbols that are more than one character
		special = ['\\','^','$','.','|','?','*','+','(',')','{']
		interp = ''
		for c in config.SCRIPT_INTERPOLATE_SYMBOL:
			if c in special:
				c = '\\'+c
			interp = interp + c

		# Channel names
		rules += [
			(r'(#\w+)', 0, STYLES['channel']),
			(r'(\&\w+)', 0, STYLES['channel']),
			(r'(\!\w+)', 0, STYLES['channel']),
			(r'(\+\w+)', 0, STYLES['channel']),
			(rf'({interp}\w+)', 0, STYLES['alias']),
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
				index = expression.pos(nth)
				length = len(expression.cap(nth))
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		# Do multi-line comments
		in_multiline = self.match_multiline(text, *self.script_comments)

	def match_multiline(self, text, delimiter, in_state, style):
		if self.previousBlockState() == in_state:
			start = 0
			add = 0
		else:
			start = delimiter.indexIn(text)
			add = delimiter.matchedLength()

		while start >= 0:
			end = delimiter.indexIn(text, start + add)
			if end >= add:
				length = end - start + add + delimiter.matchedLength()
				self.setCurrentBlockState(0)
			else:
				self.setCurrentBlockState(in_state)
				length = len(text) - start + add
			self.setFormat(start, length, style)
			start = delimiter.indexIn(text, start + length)

		if self.currentBlockState() == in_state:
			return True
		else:
			return False
