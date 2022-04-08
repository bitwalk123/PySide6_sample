#!/usr/bin/env python
# coding: utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
)
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import EllipseSelector, RectangleSelector
import seaborn as sns


def select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scatter')
        self.init_ui()

    def init_ui(self):
        # sample data
        df = pd.DataFrame(np.random.random(size=(100, 2)), columns=['X', 'Y'])

        # plot
        canvas: FigureCanvas = Scatter(df)
        self.setCentralWidget(canvas)

        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.BottomToolBarArea, navtoolbar)


class Scatter(FigureCanvas):
    fig = Figure()

    def __init__(self, df):
        super().__init__(self.fig)
        self.init_plot(df)

    def init_plot(self, df):
        # Seaborn Scatter
        ax = self.fig.add_subplot(111)
        ax = sns.scatterplot(data=df, x=df.columns[0], y=df.columns[1], ax=ax)
        ax.set(title='Scatter Sample')
        # GUI setting
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # Selector
        plt.RS = RectangleSelector(
            ax, select_callback, useblit=True,
            button=[1],  # disable middle & right buttons
            minspanx=5, minspany=5, spancoords='pixels', interactive=True,
            props=dict(facecolor='pink', edgecolor='red', alpha=0.2, fill=True)
        )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
