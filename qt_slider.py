#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Slider')
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        slider = QSlider(orientation=Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setRange(0, 100)
        slider.setTickInterval(10)
        slider.valueChanged.connect(self.show_value)
        vbox.addWidget(slider)

        self.show()

    def show_value(self):
        sld: QSlider = self.sender()
        print(sld.value())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
