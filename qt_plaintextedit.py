#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QPlainTextEdit')

    def init_ui(self):
        ptedit = QPlainTextEdit()
        self.setCentralWidget(ptedit)


def main():
    app = QApplication(sys.argv)
    hello = Example()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
