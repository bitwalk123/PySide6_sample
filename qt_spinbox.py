#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SpinBox')
        self.initUI()

    def initUI(self):
        sbox = QSpinBox()
        sbox.setRange(0, 100)
        sbox.setAlignment(Qt.AlignRight)
        sbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sbox.valueChanged.connect(self.show_value)

        vbox = QVBoxLayout()
        vbox.addWidget(sbox)
        self.setLayout(vbox)
        self.show()

    def show_value(self):
        spin: QSpinBox = self.sender()
        print(spin.value())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
