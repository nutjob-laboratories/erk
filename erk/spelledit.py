
import re
import fnmatch

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from erk.common import *

from spellchecker import SpellChecker

class SpellTextEdit(QPlainTextEdit):

	returnPressed = pyqtSignal()
	keyUp = pyqtSignal()
	keyDown = pyqtSignal()

	def __init__(self, *args):
		QPlainTextEdit.__init__(self, *args)

		self.parent = args[0]

		# Default dictionary based on the current locale.
		#self.dict = enchant.Dict("en_US")
		self.dict = SpellChecker(language=self.parent.gui.spellCheckLanguage,distance=1)

		self.highlighter = Highlighter(self.document())

		self.highlighter.setDict(self.dict)
		self.highlighter.setParent(self.parent)

	def keyPressEvent(self,event):

		#print(self.parent.parent.displayTimestamp)

		if event.key() == Qt.Key_Return:
			self.returnPressed.emit()
		elif event.key() == Qt.Key_Up:
			self.keyUp.emit()
		elif event.key() == Qt.Key_Down:
			self.keyDown.emit()
		elif event.key() == Qt.Key_Tab:
			cursor = self.textCursor()

			if self.parent.gui.autocomplete_commands:

				# Auto-complete commands
				cursor.select(QTextCursor.BlockUnderCursor)
				self.setTextCursor(cursor)
				if self.textCursor().hasSelection():
					text = self.textCursor().selectedText()

				if self.parent.is_console:
					COMMAND_LIST = CONSOLE_COMMANDS
				else:
					COMMAND_LIST = INPUT_COMMANDS

				for c in COMMAND_LIST:
					cmd = c
					rep = COMMAND_LIST[c]

					#if text in cmd:
					if fnmatch.fnmatch(cmd,f"{text}*"):
						cursor.beginEditBlock()
						cursor.insertText(rep)
						cursor.endEditBlock()
						return

			if self.parent.gui.autocomplete_nicks:

				# Auto-complete nicks/channels
				cursor.select(QTextCursor.WordUnderCursor)
				self.setTextCursor(cursor)
				if self.textCursor().hasSelection():
					text = self.textCursor().selectedText()

				# Nicks
				chan_nicks = self.parent.getUserNicks()
				channels = self.parent.gui.getChannelList(self.parent.client)
				for nick in chan_nicks:
					if fnmatch.fnmatch(nick,f"{text}*"):
						# If the nick matches a channel name, skip it for now
						mchan = False
						for chan in channels:
							if fnmatch.fnmatch(chan,f"#{text}*"):
								mchan = True
						if mchan: continue
						cursor.beginEditBlock()
						cursor.insertText(f"{nick} ")
						cursor.endEditBlock()
						return

				# Channels
				oldpos = cursor.position()
				cursor.select(QTextCursor.WordUnderCursor)
				newpos = cursor.selectionStart() - 1
				cursor.setPosition(newpos,QTextCursor.MoveAnchor)
				cursor.setPosition(oldpos,QTextCursor.KeepAnchor)
				self.setTextCursor(cursor)
				text = cursor.selectedText()

				if len(text)>0:
					for chan in channels:
						if fnmatch.fnmatch(chan,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(f"{chan} ")
							cursor.endEditBlock()
							return
					# Now that channels have been autocompleted, autocomplete nicks
					text = text[1:]
					for nick in chan_nicks:
						if fnmatch.fnmatch(nick,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(f" {nick} ")
							cursor.endEditBlock()
							return


			cursor.movePosition(QTextCursor.End)
			self.setTextCursor(cursor)

		else:
			return super().keyPressEvent(event)

	def text(self):
		return self.toPlainText()

	def setText(self,text):
		self.setPlainText(text)

	def changeLanguage(self,lang):
		self.dict = SpellChecker(language=lang,distance=1)
		self.highlighter.setDict(self.dict)


	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			# Rewrite the mouse event to a left button event so the cursor is
			# moved to the location of the pointer.
			event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
				Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
		QPlainTextEdit.mousePressEvent(self, event)

	def contextMenuEvent(self, event):

		# if not self.parent.parent.spellCheck:
		# 	return super().contextMenuEvent(event)

		if not self.parent.gui.spellCheck:
			return super().contextMenuEvent(event)

		popup_menu = self.createStandardContextMenu()

		# Select the word under the cursor.
		cursor = self.textCursor()
		cursor.select(QTextCursor.WordUnderCursor)
		self.setTextCursor(cursor)

		# Check if the selected word is misspelled and offer spelling
		# suggestions if it is.
		if self.textCursor().hasSelection():
			text = self.textCursor().selectedText()

			misspelled = self.dict.unknown([text])
			if len(misspelled)>0:
				counter = 0
				for word in self.dict.candidates(text):
					action = SpellAction(word, popup_menu)
					action.correct.connect(self.correctWord)
					popup_menu.insertAction(popup_menu.actions()[0],action)
					counter = counter + 1
				if counter != 0:
					popup_menu.insertSeparator(popup_menu.actions()[counter])

		popup_menu.exec_(event.globalPos())

	def correctWord(self, word):
		'''
		Replaces the selected text with word.
		'''
		cursor = self.textCursor()
		cursor.beginEditBlock()

		cursor.removeSelectedText()
		cursor.insertText(word)

		cursor.endEditBlock()


class Highlighter(QSyntaxHighlighter):

	WORDS = u'(?iu)[\w\']+'

	def __init__(self, *args):
		QSyntaxHighlighter.__init__(self, *args)

		self.dict = None
		self.ulist = []

	def setParent(self,parent):
		self.parent = parent

	def setDict(self, dict):
		self.dict = dict

	def highlightBlock(self, text):
		if not self.dict:
			return

		# if not self.parent.parent.spellCheck:
		# 	return
		if not self.parent.gui.spellCheck:
			return

		format = QTextCharFormat()
		format.setUnderlineColor(Qt.red)
		format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

		for word_object in re.finditer(self.WORDS, text):

			misspelled = self.dict.unknown([word_object.group()])
			if len(misspelled)>0:
				self.setFormat(word_object.start(), word_object.end() - word_object.start(), format)

class SpellAction(QAction):
	correct = pyqtSignal(str)

	def __init__(self, *args):
		QAction.__init__(self, *args)

		self.triggered.connect(lambda x: self.correct.emit(
			self.text()))