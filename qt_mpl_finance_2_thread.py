import pandas as pd
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)

from qt_mpl_finance_2_func import get_trade_info


class ThreadWorkerSignal(QObject):
    finished = Signal(str, pd.DataFrame)


class ThreadWorker(QRunnable, ThreadWorkerSignal):
    def __init__(self, ticker: str):
        super().__init__()
        self.ticker = ticker

    def run(self):
        df = get_trade_info(self.ticker)
        self.finished.emit(self.ticker, df)
