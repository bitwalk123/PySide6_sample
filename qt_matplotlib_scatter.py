#!/usr/bin/env python
# coding: utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import EllipseSelector, RectangleSelector
import seaborn as sns


class Scatter(FigureCanvas):
    df: pd.DataFrame = None
    fig = Figure()

    def __init__(self, df: pd.DataFrame):
        super().__init__(self.fig)
        self.df = df
        ax = self.init_chart()

        # Selector
        plt.RS = RectangleSelector(
            ax, self.selection, useblit=True,
            button=[1],  # disable middle & right buttons
            minspanx=5, minspany=5, spancoords='pixels', interactive=True,
            props=dict(facecolor='pink', edgecolor='red', alpha=0.2, fill=True)
        )

    def init_chart(self):
        # Seaborn Scatter
        ax = sns.scatterplot(
            data=self.df, x=self.df.columns[0], y=self.df.columns[1],
            ax=self.fig.add_subplot(111)
        )
        return ax

    @staticmethod
    def selection(eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print(f"({x1: 3.2f}, {y1: 3.2f}) --> ({x2: 3.2f}, {y2: 3.2f})")


class ScatterTest(Scatter):
    title: str = None

    def __init__(self, df: pd.DataFrame):
        self.title = 'Scatter Sample'
        super().__init__(df)

    def init_chart(self):
        # Seaborn Scatter
        ax = sns.scatterplot(
            data=self.df, x=self.df.columns[0], y=self.df.columns[1],
            ax=self.fig.add_subplot(111)
        )
        ax.set(title=self.title)
        return ax


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scatter example')
        self.init_ui()

    def init_ui(self):
        # sample data
        df = pd.DataFrame(np.random.random(size=(100, 2)), columns=['X', 'Y'])
        # chart
        canvas: FigureCanvas = ScatterTest(df)
        self.setCentralWidget(canvas)
        # navigation for plot
        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navtoolbar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
