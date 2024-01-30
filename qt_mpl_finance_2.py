import pandas as pd
import sys

from PySide6.QtCore import (
    QThreadPool,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)

from qt_mpl_finance_2_func import draw_chart
from qt_mpl_finance_2_sub import (
    DockNavigator,
    MyToolBar,
    StockChart,
)
from qt_mpl_finance_2_thread import ThreadWorker


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
        worker = ThreadWorker(ticker)
        worker.finished.connect(self.on_draw_chart)
        self.threadpool.start(worker)

    def on_draw_chart(self, ticker: str, df: pd.DataFrame):
        chart: QWidget | StockChart = self.centralWidget()
        draw_chart(chart, ticker, df)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
