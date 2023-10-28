#!/usr/bin/env python
# coding: utf-8
#
# Reference:
# https://stackoverflow.com/questions/75727004/how-do-i-add-widgets-to-the-top-left-of-pyside-qt-layout-instead-of-having-the-i

import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QVBoxLayoout test')
        self.setFixedSize(200, 200)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel('Hello World!')
        layout.addWidget(label1)

        label2 = QLabel('Thanks a lot.')
        layout.addWidget(label2)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
