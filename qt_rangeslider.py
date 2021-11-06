#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)
# https://pythonrepo.com/repo/tlambert03-QtRangeSlider-python-graphical-user-interface-applications
# pip install qtrangeslider
from qtrangeslider import QRangeSlider


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Slider')
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        slider = QRangeSlider(orientation=Qt.Horizontal)
        slider.setTickPosition(QRangeSlider.TicksBothSides)
        slider.setRange(0, 100)
        slider.setTickInterval(10)
        slider.valueChanged.connect(self.show_value)
        vbox.addWidget(slider)

    def show_value(self):
        sld: QRangeSlider = self.sender()
        print(sld.value())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
