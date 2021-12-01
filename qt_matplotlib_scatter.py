#!/usr/bin/env python
# coding: utf-8
# Reference
# https://matplotlib.org/stable/gallery/widgets/rectangle_selector.html

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow
)
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import EllipseSelector, RectangleSelector
import seaborn as sns


def select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")


def toggle_selector(event):
    toggle_selector.RS.set_active(True)


def chart():
    fig, ax = plt.subplots()

    x = np.random.rand(100)
    y = np.random.rand(100)
    ax = sns.scatterplot(x=x, y=y)
    canvas = FigureCanvas(fig)

    toggle_selector.RS = RectangleSelector(
        ax, select_callback, useblit=True,
        button=[1],  # disable middle & right buttons
        minspanx=5, minspany=5, spancoords='pixels', interactive=True,
        props=dict(
            facecolor='pink',
            edgecolor='red',
            alpha=0.2,
            fill=True
        )
    )
    fig.canvas.mpl_connect('key_press_event', toggle_selector)

    return canvas


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scatter')
        self.init_ui()

    def init_ui(self):
        canvas = chart()
        self.setCentralWidget(canvas)

        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(
            Qt.BottomToolBarArea,
            navtoolbar
        )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
