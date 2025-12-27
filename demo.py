#!/usr/bin/env python
# coding: utf-8
import platform
import sys
import PySide6
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Hello(QWidget):
    def __init__(self):
        super().__init__()

        print("> Platform", platform.platform())
        print("> Python", sys.version)
        print("> PySide", PySide6.__version__)

        self.setWindowTitle("demo")

        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton()
        btn.setIcon(QIcon("qt.png"))
        btn.setIconSize(QSize(100, 100))
        layout.addWidget(btn)



def main():
    app = QApplication(sys.argv)
    hello = Hello()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
