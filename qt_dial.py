#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QDial,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QDial')

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        dial = QDial()
        dial.setRange(0, 100)
        dial.setNotchesVisible(True)
        dial.valueChanged.connect(self.show_value)
        vbox.addWidget(dial)

    def show_value(self, value: int):
        print('%d になりました。' % value)


def main():
    app = QApplication(sys.argv)
    # print(QStyleFactory.keys())
    app.setStyle('Fusion')
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
