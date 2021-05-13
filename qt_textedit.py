#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://pythonpyqt.com/pyqt-qtextedit/

import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.setWindowTitle("QTextEdit")
        self.resize(300, 270)
        self.show()

    def initUI(self):
        base = QWidget()
        self.setCentralWidget(base)

        tedit = QTextEdit()
        btn1 = QPushButton("Button 1")
        btn2 = QPushButton("Button 2")

        layout = QVBoxLayout()
        base.setLayout(layout)

        layout.addWidget(tedit)
        layout.addWidget(btn1)
        layout.addWidget(btn2)

        btn1.clicked.connect(lambda: self.btn1_Clicked(tedit))
        btn2.clicked.connect(lambda: self.btn2_Clicked(tedit))

    def btn1_Clicked(self, textEdit):
        textEdit.setPlainText("Hello PySide6!\nfrom pythonpyqt.com")

    def btn2_Clicked(self, textEdit):
        textEdit.setHtml("<font color='red' size='6'><red>Hello PySide6!\nHello</font>")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
