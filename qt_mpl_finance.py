#!/usr/bin/env python
# coding: utf-8
# Reference
# https://stackoverflow.com/questions/60599812/how-can-i-customize-mplfinance-plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

import mplfinance as mpf
import pandas as pd
import sys
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
        self.show()

    def initUI(self):
        # sample dataset
        filename = 'candlestick_sample_data.csv'
        df = pd.read_csv(filename, index_col=0, parse_dates=True)

        sty = mpf.make_mpf_style(base_mpf_style='binance', rc={'font.size': 8})
        fig = mpf.figure(dpi=100, style=sty)
        grid = plt.GridSpec(3, 3, wspace=0.45, hspace=0.45)
        ax1 = fig.add_subplot(grid[0:2, 0:])
        ax2 = fig.add_subplot(grid[2, 0:], sharex=ax1)
        mpf.plot(
            df,
            type='candle',
            mav=(14, 28),
            show_nontrading=False,
            datetime_format='%m-%d',
            ax=ax1,
            volume=ax2
        )
        canvas = FigureCanvas(fig)

        self.setCentralWidget(canvas)
        self.addToolBar(
            QtCore.Qt.ToolBarArea.BottomToolBarArea,
            NavigationToolbar(canvas, self)
        )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
