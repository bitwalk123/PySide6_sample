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
        self.show()

    def initUI(self):
        btn = QPushButton('プッシュボタン')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.clicked.connect(self.buttonClicked)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(btn)

    def buttonClicked(self):
        obj = self.sender()
        print('「' + obj.text() + '」がクリックされました。')


def main():
    app: QApplication = QApplication(sys.argv)
    ex: Example = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
