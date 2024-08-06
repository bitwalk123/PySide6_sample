import datetime as dt
import mplfinance as mpf
import pandas as pd
import sys
import yfinance as yf

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.fig.subplots_adjust(left=0.2, right=0.95, top=0.9, bottom=0.15)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def clearAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Exchange')
        self.setFixedSize(400, 400)

        self.ticker = yf.Ticker('USDJPY=X')
        self.chart = MyChart()
        self.setCentralWidget(self.chart)
        self.draw_chart()

        timer = QTimer(self)
        timer.timeout.connect(self.draw_chart)
        timer.start(60000)

    def draw_chart(self):
        df = self.get_exchange()
        if len(df) == 0:
            return

        self.chart.clearAxes()
        mpf.plot(df, type='candle', style='binance', ax=self.chart.ax, )

        df0 = df.tail(1)
        title = '%.3f JPY at %s' % (df0['Close'].iloc[0], str(df0.index[0].time()))
        self.chart.ax.set_title(title)
        self.chart.ax.set_ylabel('USD - JPY')
        self.chart.ax.grid()
        self.chart.refreshDraw()

    def get_exchange(self) -> pd.DataFrame:
        end = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
        delta = dt.timedelta(hours=3)
        start = end - delta
        df = self.ticker.history(start=start, end=end, interval='1m')
        if len(df) > 0:
            df.index = df.index.tz_convert('Asia/Tokyo')
        return df

    def on_update(self):
        self.draw_chart()


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
