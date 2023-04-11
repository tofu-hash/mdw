import markdown
import sys

from PyQt5 import QtGui

import config
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTextEdit, QVBoxLayout,
                             QHBoxLayout, QPushButton,
                             QFileDialog, QLabel)
from PyQt5.QtGui import QIcon


class MarkdownEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('mdw')
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: rgb(50, 50, 50); color: rgb(250, 250, 250); border-radius: 10px;")

        self.editor = QTextEdit()
        self.editor.setStyleSheet('margin: 17px; padding: 10px;'
                                  'font-size: %spx; '
                                  'font-weight: %s; '
                                  'border: 1px solid rgb(100, 100, 200);' %
                                  (config.FONT_SIZE,
                                   config.FONT_WEIGHT))
        self.preview = QTextEdit()
        self.preview.setStyleSheet('padding: 20px;')

        self.setFont(QtGui.QFont(config.FONT, config.FONT_SIZE))
        self.adjustSize()

        self.label = QLabel()
        self.label.setText(config.LABEL_TEXT)
        self.label.setStyleSheet(config.LABEL_STYLESHEET)
        self.label.setMaximumSize(135, 150)

        self.preview.hide()
        self.preview.setReadOnly(True)

        btn_stylesheet = ('border: 1px solid rgb(100, 100, 200); '
                          'border-radius: 10px; '
                          'padding: 10px; '
                          'margin-left: 15px; '
                          'margin-right: 5px; '
                          'max-width: 150px; '
                          'font-size: 14px; '
                          'font-weight: 900;')

        self.switch_button = QPushButton(QIcon('icons/markdown.png'), 'Markdown')
        self.add_image_button = QPushButton(QIcon('icons/image.png'), 'Add Image')
        self.save_button = QPushButton(QIcon('icons/save.png'), 'Save')
        self.open_button = QPushButton(QIcon('icons/open.png'), 'Open')

        self.switch_button.setStyleSheet(btn_stylesheet)
        self.add_image_button.setStyleSheet(btn_stylesheet)
        self.save_button.setStyleSheet(btn_stylesheet)
        self.open_button.setStyleSheet(btn_stylesheet)

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.switch_button)
        self.hbox.addWidget(self.add_image_button)
        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.open_button)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.editor)
        self.vbox.addWidget(self.preview)

        self.setLayout(self.vbox)

        self.switch_button.clicked.connect(self.switch_windows)
        self.add_image_button.clicked.connect(self.paste_image)

        # self.editor.textChanged.connect(self.update_preview)
        self.save_button.clicked.connect(self.save_file)
        self.open_button.clicked.connect(self.open_file)

    def switch_windows(self):
        if self.editor.isVisible():
            self.update_preview()
            self.editor.hide()
            self.preview.show()
            self.switch_button.setText('Edit')
            self.switch_button.setIcon(QIcon('icons/edit.png'))
        else:
            self.preview.hide()
            self.editor.show()
            self.switch_button.setText('Markdown')
            self.switch_button.setIcon(QIcon('icons/markdown.png'))

    def update_preview(self):
        markdown_text = self.editor.toPlainText()
        html = self.parse_html(markdown.markdown(markdown_text))
        print(html)
        self.preview.setHtml(html)

    def parse_html(self, text: str):
        # text = text.replace('"', '<span style="color: %s;">' % config.MARK_COLOR + '"' + '</span>')
        text = text.replace('<code>',
                            '<code style="color: %s; font-weight: %s;">' %
                            (config.CODE_COLOR, config.CODE_FONT_WEIGHT))
        text = text.replace('<img ', '<img width="450" ')
        text = text.replace('<h1>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 3))
        text = text.replace('<h2>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 2.3))
        text = text.replace('<h3>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 2))
        text = text.replace('<h4>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 1.7))
        text = text.replace('<h5>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 1.5))
        for i in range(1, 6):
            text = text.replace('</h%s>' % i, '</div>')

        return text

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save file', '', '.md (*.txt, *.md)')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.editor.toPlainText())

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', '.md (*.txt, *.md)')
        if file_path:
            with open(file_path, 'r') as file:
                self.editor.setText(file.read())

    def paste_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Images (*.jpeg, *.png, *.jpg)')
        if file_path:
            img = '![Image](%s)' % file_path
            self.editor.setText(self.editor.toPlainText() + img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec_())
