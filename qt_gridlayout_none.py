#!/usr/bin/env python
# coding: utf-8
#
# Reference:
# https://stackoverflow.com/questions/75727004/how-do-i-add-widgets-to-the-top-left-of-pyside-qt-layout-instead-of-having-the-i

import sys

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
        self.setLayout(layout)

        label1 = QLabel('Hello World!')
        layout.addWidget(label1, 0, 0)

        label2 = QLabel('Thanks a lot.')
        layout.addWidget(label2, 1, 0)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
