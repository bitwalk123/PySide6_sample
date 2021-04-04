#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Label')
        self.show()

    def initUI(self):
        lab = QLabel('ラベルは文字を表示します。')
        lab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(lab)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
