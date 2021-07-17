#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('PushButton')

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        btn = QPushButton('プッシュボタン')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.clicked.connect(self.buttonClicked)
        vbox.addWidget(btn)

    def buttonClicked(self):
        obj = self.sender()
        print('「' + obj.text() + '」がクリックされました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
