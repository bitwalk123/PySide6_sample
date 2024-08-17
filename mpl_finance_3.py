#!/usr/bin/env python
# coding: utf-8
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import sys

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)

        n = 2
        grid = plt.GridSpec(n + 1, 1, wspace=0.0, hspace=0.0)
        self.ax = ax = dict()
        ax[0] = self.fig.add_subplot(grid[0:2, 0])
        ax[0].grid()
        ax[0].tick_params(labelbottom=False)

        for i in range(1, n):
            ax[i] = self.fig.add_subplot(grid[i + 1, 0], sharex=ax[0])
            ax[i].grid()
            if i < n - 1:
                ax[i].tick_params(labelbottom=False)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Multiple charts')

        self.chart = chart = MyChart()
        self.setCentralWidget(chart)

        self.addToolBar(
            QtCore.Qt.ToolBarArea.BottomToolBarArea,
            NavigationToolbar(chart, self)
        )

        self.draw()

    def draw(self):
        # sample dataset
        filename = 'candlestick_sample_data.csv'
        df = pd.read_csv(filename, index_col=0, parse_dates=True)

        param = dict(
            data=df,
            style='yahoo',
            type='candle',
            datetime_format='%m/%d',
            xrotation=0,
            ax=self.chart.ax[0],
        )
        param['volume'] = self.chart.ax[1]

        mpf.plot(**param)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
