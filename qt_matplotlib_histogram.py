#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://stats.biopapyrus.jp/python/hist.html

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns


class Histogram(FigureCanvas):
    fig = Figure()

    def __init__(self, df: pd.Series):
        super().__init__(self.fig)
        self.init_chart(df)

    def init_chart(self, df: pd.Series):
        sns.set()
        sns.set_style('whitegrid')

        ax = self.fig.add_subplot(111)
        ax.hist(df)
        ax.set_xlabel('length [cm]')

        ax.set(title='Histogram Sample')


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Histogram example')
        self.init_ui()

    def init_ui(self):
        # sample data
        np.random.seed(2022)
        df = pd.Series(np.random.normal(50, 10, 1000))
        # plot
        canvas: FigureCanvas = Histogram(df)
        self.setCentralWidget(canvas)
        # navigation for plot
        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.BottomToolBarArea, navtoolbar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
