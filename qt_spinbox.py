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
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        sbox = QSpinBox()
        sbox.setRange(0, 100)
        sbox.setAlignment(Qt.AlignRight)
        sbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sbox.valueChanged.connect(self.show_value)
        vbox.addWidget(sbox)

    def show_value(self):
        spin: QSpinBox = self.sender()
        print(spin.value())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
