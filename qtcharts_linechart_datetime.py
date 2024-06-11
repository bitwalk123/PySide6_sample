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
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
import numpy as np


def datetime_data_reader(name_file) -> QLineSeries:
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
        pen = series.pen()
        pen.setWidth(1)
        pen.setColor('blue')
        series.setPen(pen)
        series.setPointsVisible(True)
        series.setMarkerSize(5.0)
        series.setColor(QColor('blue'))

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.setTitle('Sunspots count (by Space Weather Prediction Center)')

        axis_x = QDateTimeAxis()
        axis_x.setTickCount(10)
        axis_x.setFormat('MMM yyyy')
        axis_x.setTitleText('Date')
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTickCount(10)
        axis_y.setLabelFormat('%i')
        axis_y.setTitleText('Sunspots count')
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

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
