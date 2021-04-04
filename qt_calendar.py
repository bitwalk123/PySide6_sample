#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Calendar')
        self.show()

    def initUI(self):
        calendar = QCalendarWidget()

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(calendar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
