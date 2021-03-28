#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6 import QtCore
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


class Hello(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Hello World!')
        self.show()

    def initUI(self):
        label: QLabel = QLabel('こんにちは、世界！')
        font: QFont = QFont()
        font.setPointSize(24)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


def main():
    app: QApplication = QApplication(sys.argv)
    ex: Hello = Hello()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
