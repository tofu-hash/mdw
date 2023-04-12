from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QSyntaxHighlighter, QColor


class Highlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        self.highlighting_rules = []

        # Создание правил подсветки
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QBrush(QtGui.QColor(100, 100, 200)))
        keyword_format.setFontWeight(QtGui.QFont.Bold)
        keywords = ['if', 'else', 'while', 'for', 'return']
        for word in keywords:
            pattern = QtCore.QRegExp("\\b" + word + "\\b")
            rule = (pattern, keyword_format)
            self.highlighting_rules.append(rule)

        # Создание правил для строк и комментариев
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QColor(200, 100, 100))
        rule = (QtCore.QRegExp("\".*\""), string_format)
        self.highlighting_rules.append(rule)

        code_format = QtGui.QTextCharFormat()
        code_format.setForeground(QColor(100, 100, 200))
        rule = (QtCore.QRegExp("<code>.*</code>"), string_format)
        self.highlighting_rules.append(rule)

        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtCore.Qt.darkGray)
        rule = (QtCore.QRegExp("#[^\n]*"), comment_format)
        self.highlighting_rules.append(rule)

    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            pattern = rule[0]
            format = rule[1]
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, format)
                index = pattern.indexIn(text, index + length)
