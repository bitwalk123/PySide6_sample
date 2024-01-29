import sys

import mplfinance as mpf
import pandas as pd

from PySide6.QtCore import (
    QThreadPool,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)

from qt_mpl_finance_2_sub import (
    DockNavigator,
    MyToolBar,
    StockChart,
)
from qt_mpl_finance_2_yfinance import GetTradeInfoWorker


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.init_ui()
        self.setWindowTitle('Candlestick chart')
        self.resize(800, 600)

    def init_ui(self):
        toolbar = MyToolBar()
        toolbar.tickerEntered.connect(self.on_ticker_entered)
        self.addToolBar(toolbar)

        chart = StockChart()
        self.setCentralWidget(chart)

        dock_bottom = DockNavigator(chart)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            dock_bottom
        )

    def on_ticker_entered(self, ticker: str):
        worker = GetTradeInfoWorker(ticker)
        worker.signals.finished.connect(self.draw_chart)
        self.threadpool.start(worker)

    def draw_chart(self, ticker: str, df: pd.DataFrame):
        chart: QWidget | StockChart = self.centralWidget()
        chart.clearAxes()
        chart.ax.set_title(ticker)
        mpf.plot(
            df,
            type='candle',
            datetime_format='%m/%d',
            mav=(5, 25),
            tight_layout=False,
            style='yahoo',
            ax=chart.ax,
            volume=chart.ax2
        )
        chart.ax.grid()
        chart.ax2.grid()
        chart.refreshDraw()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
