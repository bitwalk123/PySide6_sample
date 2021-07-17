#!/usr/bin/env python
# coding: utf-8

import sys
import PySide6
from PySide6 import QtCore
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class Hello(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Hello World!')

        print('PySide', PySide6.__version__)
        print('Qt', PySide6.QtCore.__version__)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel('こんにちは、世界！')
        font = QFont()
        font.setPointSize(24)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)


def main():
    app = QApplication(sys.argv)
    hello = Hello()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()