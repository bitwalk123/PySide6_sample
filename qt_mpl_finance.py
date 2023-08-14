#!/usr/bin/env python
# coding: utf-8
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


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(800, 600)
        self.setWindowTitle('Candlestick Chart on PySide6')

    def initUI(self):
        # sample dataset
        filename = 'candlestick_sample_data.csv'
        df = pd.read_csv(filename, index_col=0, parse_dates=True)

        fig = Figure()
        grid = plt.GridSpec(3, 1, wspace=0, hspace=0.0)

        ax1 = fig.add_subplot(grid[0:2, 0])
        ax2 = fig.add_subplot(grid[2, 0], sharex=ax1)
        mpf.plot(
            df,
            style='binance',
            type='candle',
            mav=(14, 28),
            show_nontrading=False,
            datetime_format='%m/%d',
            ax=ax1,
            volume=ax2
        )
        ax1.grid()
        ax2.grid()
        canvas = FigureCanvas(fig)

        self.setCentralWidget(canvas)
        self.addToolBar(
            QtCore.Qt.ToolBarArea.BottomToolBarArea,
            NavigationToolbar(canvas, self)
        )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
