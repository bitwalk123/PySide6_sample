#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://pythonpyqt.com/pyqt-qtextedit/

import sys
from PySide6.QtGui import (
    QFont,
    QIcon,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QToolBar,
    QToolButton,
)


class MNote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.setWindowTitle("MNote")
        self.show()

    def initUI(self):
        # Create pyqt toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add buttons to toolbar
        but_open = QToolButton()
        but_open.setIcon(QIcon.fromTheme('document-open'))
        toolbar.addWidget(but_open)

        tedit = QTextEdit()
        font = self.config_font()
        tedit.setFont(font)
        self.setCentralWidget(tedit)

    def config_font(self):
        font = QFont()
        font.setPointSize(24)
        font.setFixedPitch(True)
        return font


def main():
    app = QApplication(sys.argv)
    mnote = MNote()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
