import pandas as pd
import yfinance as yf
from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
)


def get_trade_info(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, period='3mo')
    return df


class GetTradeInfoWorkerSignals(QObject):
    finished = Signal(str, pd.DataFrame)


class GetTradeInfoWorker(QRunnable):
    def __init__(self, ticker: str):
        super().__init__()
        self.signals = GetTradeInfoWorkerSignals()
        self.ticker = ticker

    def run(self):
        df = get_trade_info(self.ticker)
        self.signals.finished.emit(self.ticker, df)
