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


def plot(graph, x, y, name_plot, color):
    pen = pg.mkPen(color=color)
    graph.plot(x, y, name=name_plot, pen=pen, symbol='+', symbolSize=30, symbolBrush=(color))


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('pyqtgraph')

    def init_ui(self):
        grp = pg.PlotWidget()
        self.setCentralWidget(grp)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature_1 = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        temperature_2 = [50, 35, 44, 22, 38, 32, 27, 38, 32, 44]

        # Add Background colour to white
        grp.setBackground('w')
        # Add Title
        grp.setTitle("Your Title Here", color="b", size="30pt")
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        grp.setLabel("left", "Temperature (°C)", **styles)
        grp.setLabel("bottom", "Hour (H)", **styles)
        # Add legend
        grp.addLegend()
        # Add grid
        grp.showGrid(x=True, y=True)
        # Set Range
        grp.setXRange(0, 10, padding=0.05)
        grp.setYRange(20, 55, padding=0.05)

        plot(grp, hour, temperature_1, "Sensor1", 'r')
        plot(grp, hour, temperature_2, "Sensor2", 'b')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
