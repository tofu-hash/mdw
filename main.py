import markdown
import sys

from PyQt5 import QtGui
from syntax_highlighter import Highlighter
import config
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTextEdit, QVBoxLayout,
                             QHBoxLayout, QPushButton,
                             QFileDialog, QLabel, QSizePolicy,
                             QWidget, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap


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
        self.highlighter = Highlighter(self.preview.document())
        self.preview.setStyleSheet('padding: 20px;')
        self.preview.setStyleSheet('margin: 17px; padding: 10px;'
                                   'border: 1px solid rgb(100, 100, 200);')

        self.setFont(QtGui.QFont(config.FONT, config.FONT_SIZE))
        self.adjustSize()

        self.label = QLabel()
        self.label.setText(config.LABEL_TEXT)
        self.label.setStyleSheet(config.LABEL_STYLESHEET)
        self.label.setMaximumSize(135, 150)

        self.preview.hide()
        self.preview.setReadOnly(True)

        btn_stylesheet = ('padding: 0px; '
                          'margin-left: 15px; '
                          'margin-right: 5px; '
                          'max-width: 150px; '
                          'font-size: 14px; '
                          'font-weight: 900;')

        icon_size = 20

        self.add_bold = QPushButton()
        self.add_bold.setIcon(QIcon('icons/editor/bold.png'))
        self.add_bold.setIconSize(QSize(icon_size, icon_size))
        self.add_bold.setCursor(Qt.PointingHandCursor)
        self.add_bold.clicked.connect(lambda: self.paste_format('__ [ ] __'))

        self.add_italic = QPushButton()
        self.add_italic.setIcon(QIcon('icons/editor/italic.png'))
        self.add_italic.setIconSize(QSize(icon_size, icon_size))
        self.add_italic.setCursor(Qt.PointingHandCursor)
        self.add_italic.clicked.connect(lambda: self.paste_format('__ [ ] __'))

        self.add_h1 = QPushButton()
        self.add_h1.setIcon(QIcon('icons/editor/header.png'))
        self.add_h1.setIconSize(QSize(icon_size, icon_size))
        self.add_h1.setCursor(Qt.PointingHandCursor)
        self.add_h1.clicked.connect(lambda: self.paste_format('# [ ]'))

        self.add_h2 = QPushButton()
        self.add_h2.setIcon(QIcon('icons/editor/header2.png'))
        self.add_h2.setIconSize(QSize(icon_size, icon_size))
        self.add_h2.setCursor(Qt.PointingHandCursor)
        self.add_h2.clicked.connect(lambda: self.paste_format('## [ ]'))

        self.add_h3 = QPushButton()
        self.add_h3.setIcon(QIcon('icons/editor/header3.png'))
        self.add_h3.setIconSize(QSize(icon_size, icon_size))
        self.add_h3.setCursor(Qt.PointingHandCursor)
        self.add_h3.clicked.connect(lambda: self.paste_format('### [ ]'))

        self.add_code = QPushButton()
        self.add_code.setIcon(QIcon('icons/editor/code.png'))
        self.add_code.setIconSize(QSize(icon_size, icon_size))
        self.add_code.setCursor(Qt.PointingHandCursor)
        self.add_code.clicked.connect(lambda: self.paste_format('### [ ]'))

        self.add_image_button = QPushButton()
        self.add_image_button.setIcon(QIcon('icons/editor/image.png'))
        self.add_image_button.setIconSize(QSize(icon_size, icon_size))
        self.add_image_button.setCursor(Qt.PointingHandCursor)

        self.save_button = QPushButton()
        self.save_button.setIcon(QIcon('icons/save.png'))
        self.save_button.setIconSize(QSize(icon_size, icon_size))
        self.save_button.setCursor(Qt.PointingHandCursor)

        self.open_button = QPushButton()
        self.open_button.setIcon(QIcon('icons/open.png'))
        self.open_button.setIconSize(QSize(icon_size, icon_size))
        self.open_button.setCursor(Qt.PointingHandCursor)

        self.switch_button = QPushButton()
        self.switch_button.setIcon(QIcon(QPixmap("icons/markdown.png")))  # добавляем иконку
        self.switch_button.setIconSize(QSize(30, 30))  # устанавливаем размер иконки
        # self.switch_button.setStyleSheet("border-radius: 15; "
        #                                  "background-color: rgb(40, 40, 40); "
        #                                  "padding: 20px; "
        #                                  "border: 2px solid rgb(100, 100, 200); "
        #                                  "margin-left: 0px; ")  # устанавливаем закругление углов
        # self.switch_button.setMaximumSize(120, 100)  # устанавливаем максимальный размер кнопки
        self.switch_button.setCursor(Qt.PointingHandCursor)

        self.main_box = QVBoxLayout()
        self.header_box_top = QHBoxLayout()
        self.header_box_bottom = QHBoxLayout()

        self.header_box_top.addWidget(self.save_button)
        self.header_box_top.addWidget(self.open_button)

        # self.header_box_top.addWidget(self.switch_button, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.editor_box = QHBoxLayout()

        self.editor_box.addWidget(self.switch_button)
        self.editor_box.addWidget(self.add_bold)
        self.editor_box.addWidget(self.add_italic)
        self.editor_box.addWidget(self.add_h1)
        self.editor_box.addWidget(self.add_h2)
        self.editor_box.addWidget(self.add_h3)
        self.editor_box.addWidget(self.add_code)
        self.editor_box.addWidget(self.add_image_button)
        self.editor_box.addWidget(self.open_button)
        self.editor_box.addWidget(self.save_button)

        for _ in range(2):
            self.editor_box.addWidget(self.add_image_button)

        self.main_box.addWidget(self.label)
        self.main_box.addLayout(self.editor_box)
        self.main_box.addWidget(self.editor)
        self.main_box.addWidget(self.preview)

        self.main_box.addLayout(self.header_box_top)

        self.setLayout(self.main_box)

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
            self.switch_button.setIcon(QIcon('icons/edit.png'))
        else:
            self.preview.hide()
            self.editor.show()
            self.switch_button.setIcon(QIcon('icons/markdown.png'))

    def update_preview(self):
        markdown_text = self.editor.toPlainText()
        html = self.parse_html(markdown.markdown(markdown_text))
        print(html)
        self.preview.setHtml(html)

    def parse_html(self, text: str):
        style = "<style>* {" \
                "   font-size: %spx;" \
                "}</style> " % config.FONT_SIZE
        # text = text.replace('"', '<span style="color: %s;">' % config.MARK_COLOR + '"' + '</span>')
        text = style + text
        text = text.replace('<img ', '<img width="450" ')
        text = text.replace('<h1>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 2))
        text = text.replace('<h2>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 1.5))
        text = text.replace('<h3>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 1.3))
        text = text.replace('<h4>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 1.2))
        text = text.replace('<h5>', '<div style="font-size: %spx; font-weight: 900;">' % int(config.FONT_SIZE * 1.1))
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

    def paste_format(self, __format: str):
        self.editor.setText(self.editor.toPlainText() + __format)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec_())
