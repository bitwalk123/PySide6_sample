#!/usr/bin/env python
# coding: utf-8

# Reference
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

import pyqtgraph as pg
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('pyqtgraph')

    def init_ui(self):
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temp = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        grp = pg.PlotWidget()
        self.setCentralWidget(grp)

        grp.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        grp.plot(hour, temp, pen=pen)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
