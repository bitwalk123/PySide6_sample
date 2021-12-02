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
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import EllipseSelector, RectangleSelector
import seaborn as sns


class Example(QMainWindow):
    RS = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scatter')
        self.init_ui()

    def init_ui(self):
        # sample data
        df = pd.DataFrame(np.random.random(size=(100, 2)), columns=['X', 'Y'])

        canvas = self.chart(df)
        self.setCentralWidget(canvas)

        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(
            Qt.BottomToolBarArea,
            navtoolbar
        )

    def chart(self, df):
        fig, ax = plt.subplots()

        ax = sns.scatterplot(data=df, x=df.columns[0], y=df.columns[1])
        canvas = FigureCanvas(fig)

        self.RS = RectangleSelector(
            ax, self.select_callback, useblit=True,
            button=[1],  # disable middle & right buttons
            minspanx=5, minspany=5, spancoords='pixels', interactive=True,
            props=dict(
                facecolor='pink',
                edgecolor='red',
                alpha=0.2,
                fill=True
            )
        )
        return canvas

    def select_callback(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
