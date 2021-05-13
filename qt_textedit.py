#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.btnPress1 = QPushButton("Button 1")
        self.btnPress2 = QPushButton("Button 2")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btnPress1)
        layout.addWidget(self.btnPress2)
        self.setLayout(layout)

        self.btnPress1.clicked.connect(self.btnPress1_Clicked)
        self.btnPress2.clicked.connect(self.btnPress2_Clicked)

        self.setWindowTitle("QTextEdit")
        self.resize(300, 270)
        self.show()


    def btnPress1_Clicked(self):
        self.textEdit.setPlainText("Hello PySide6!\nfrom pythonpyqt.com")

    def btnPress2_Clicked(self):
        self.textEdit.setHtml("<font color='red' size='6'><red>Hello PySide6!\nHello</font>")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
