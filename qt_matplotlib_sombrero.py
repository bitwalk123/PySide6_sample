#!/usr/bin/env python
# coding: utf-8
import matplotlib as mpl
import numpy as np
import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow


class Sombrero(FigureCanvas):
    def __init__(self):
        fig = Figure()
        super().__init__(fig)

        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)

        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(
            X, Y, Z,
            rstride=1, cstride=1,
            cmap=mpl.colormaps['coolwarm'],
            linewidth=0, antialiased=False
        )


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sombrero example')

        canvas = Sombrero()
        self.setCentralWidget(canvas)

        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.BottomToolBarArea, navtoolbar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
