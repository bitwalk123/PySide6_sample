#!/usr/bin/env python
# coding: utf-8
import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setMinimumSize(QSize(400, 0))
        self.setWindowTitle("LineEdit")

    def initUI(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        lab = QLabel('Name:')
        lab.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox.addWidget(lab)

        self.line = QLineEdit()
        self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox.addWidget(self.line)

        but = QPushButton('OK')
        but.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but.clicked.connect(self.clickMethod)
        hbox.addWidget(but)

    def clickMethod(self):
        print('Your name: ' + self.line.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
