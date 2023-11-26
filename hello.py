#!/usr/bin/env python
# coding: utf-8
import platform
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
        self.init_ui()
        self.setWindowTitle('Hello World!')

        print('Machine', platform.machine())
        print('System', platform.system())
        print('Python', sys.version)
        print('PySide', PySide6.__version__)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel('こんにちは、世界！')
        font = QFont()
        font.setPointSize(24)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


def main():
    app = QApplication(sys.argv)
    hello = Hello()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()