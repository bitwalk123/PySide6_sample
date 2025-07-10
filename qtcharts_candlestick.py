import sys

import pandas as pd
import yfinance as yf
from PySide6.QtCharts import (
    QCandlestickSeries,
    QCandlestickSet,
    QChart,
    QChartView,
    QDateTimeAxis,
    QValueAxis,
)
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Candlestick Chart sample")
        self.setFixedSize(1200, 400)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart.legend().setVisible(False)

        self.series = QCandlestickSeries()
        self.series.setName("Price")
        self.series.setIncreasingColor(QColor(Qt.GlobalColor.white))
        self.series.setDecreasingColor(QColor(Qt.GlobalColor.black))
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(1)
        self.series.setPen(pen)
        self.chart.addSeries(self.series)

        self.axisX = QDateTimeAxis()
        self.axisX.setFormat("MM/dd")
        # self.axisX.setTitleText("Date")
        self.chart.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axisX)

        self.axisY = QValueAxis()
        self.axisY.setTitleText("Price")
        self.axisY.setLabelFormat("%.0f")
        self.chart.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axisY)

        self.load_stock_data()

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(chart_view)

    def load_stock_data(self):
        symbol = "^N225"

        try:
            obj = yf.Ticker(symbol)
            data: pd.DataFrame = obj.history(period="6mo", interval="1d")

            if data.empty:
                print(f"株価データを取得できませんでした。データが空です。({symbol})")
                self.axisX.setMin(QDateTime.currentDateTime())
                self.axisX.setMax(QDateTime.currentDateTime().addDays(1))
                self.axisY.setMin(0)
                self.axisY.setMax(1)
                return

            self.chart.setTitle(f"{obj.info['longName']} ({symbol})")

            min_price = float('inf')
            max_price = float('-inf')

            self.series.clear()

            for index, row in data.iterrows():
                index: pd.Timestamp
                ts_msec = int(index.timestamp() * 1000)

                price_open = row["Open"].item()
                price_high = row["High"].item()
                price_low = row["Low"].item()
                price_close = row["Close"].item()

                candle_set = QCandlestickSet(
                    price_open,
                    price_high,
                    price_low,
                    price_close,
                    ts_msec
                )
                self.series.append(candle_set)

                min_price = min(min_price, price_low)
                max_price = max(max_price, price_high)

            if not data.empty:
                ts_min: pd.Timestamp = data.index.min()
                ts_max: pd.Timestamp = data.index.max()
                self.axisX.setMin(
                    QDateTime.fromSecsSinceEpoch(int(ts_min.timestamp()))
                )
                self.axisX.setMax(
                    QDateTime.fromSecsSinceEpoch(int(ts_max.timestamp()))
                )

            if min_price != float('inf') and max_price != float('-inf'):
                padding = (max_price - min_price) * 0.05
                self.axisY.setMin(min_price - padding)
                self.axisY.setMax(max_price + padding)
            else:
                self.axisY.setMin(0)
                self.axisY.setMax(1)

        except Exception as e:
            print(f"データの取得または処理中にエラーが発生しました: {e}")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
