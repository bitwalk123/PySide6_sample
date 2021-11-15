#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-datetimeaxis-example.html
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import (
    QDate,
    QDateTime,
    QLocale,
    Qt,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
import numpy as np

def datetime_data_reader(name_file):
    series = QLineSeries()

    with open(name_file) as f:
        for line in f:
            values = line.strip().split()
            if len(values) == 0:
                continue
            if values[0].startswith('#'):
                continue
            if values[0].startswith(':'):
                continue

            moment_in_time = QDateTime()
            moment_in_time.setDate(QDate(int(values[0]), int(values[1]), 15))
            series.append(np.int64(moment_in_time.toMSecsSinceEpoch()), float(values[2]))

    return series


class LineChart(QChartView):
    def __init__(self):
        super().__init__()
        QLocale.setDefault(QLocale.c())
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series = datetime_data_reader('sun_spots.txt')

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.setTitle('Sunspots count (by Space Weather Prediction Center)')

        axisX = QDateTimeAxis()
        axisX.setTickCount(10)
        axisX.setFormat('MMM yyyy')
        axisX.setTitleText('Date')
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTickCount(10)
        axisY.setLabelFormat('%i')
        axisY.setTitleText('Sunspots count')
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        linechart = LineChart()
        self.setCentralWidget(linechart)
        self.resize(1000, 600)
        self.setWindowTitle('LineChart (DateTime)')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
