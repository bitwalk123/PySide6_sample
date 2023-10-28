#!/usr/bin/env python
# coding: utf-8
#
# Reference:
# https://stackoverflow.com/questions/75727004/how-do-i-add-widgets-to-the-top-left-of-pyside-qt-layout-instead-of-having-the-i

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QGridLayoout test')
        self.setFixedSize(200, 200)

    def init_ui(self):
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setLayout(layout)

        label = QLabel('Hello World!')
        layout.addWidget(label, 0, 0)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
