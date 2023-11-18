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

        self.entry = QLineEdit()
        self.init_ui()
        self.setWindowTitle("LineEdit")

    def init_ui(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        lab = QLabel('Name:')
        lab.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox.addWidget(lab)

        self.entry.setFixedWidth(200)
        self.entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox.addWidget(self.entry)

        but = QPushButton('OK')
        but.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but.clicked.connect(self.button_clicked)
        hbox.addWidget(but)

    def button_clicked(self):
        print('Your name: ' + self.entry.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
