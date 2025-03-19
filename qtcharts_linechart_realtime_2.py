#!/usr/bin/env python
import csv
import sys
from math import sin, pi

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis, QDateTimeAxis,
)
from PySide6.QtCore import QTimer, Qt, QTime
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow


def csv_reader(csvname: str) -> tuple[QLineSeries, list]:
    series = QLineSeries()
    msec_delta = 9 * 60 * 60 * 1000

    with open(csvname) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
                continue

            x = QTime.fromString(row[0], 'H:mm:ss').msecsSinceStartOfDay() - msec_delta
            y = float(row[1])
            series.append(x, y)

    return series, headers


def get_pen() -> QPen:
    pen = QPen(Qt.GlobalColor.gray)
    pen.setWidthF(0.5)
    return pen


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data, headers = csv_reader('tick.csv')

        self.idx = 0

        self.series = series = QLineSeries()
        series.setPen(get_pen())
        series.setPointsVisible(True)
        series.setMarkerSize(0.75)

        self.axis_x = axis_x = QDateTimeAxis()
        axis_x.setTitleText(headers[0])
        axis_x.setTickCount(14)
        axis_x.setFormat('HH:mm')

        axis_x_min = axis_x.min()
        axis_x_min.setTime(QTime.fromString('9:00:00', 'H:mm:ss'))
        axis_x_max = axis_x.max()
        axis_x_max.setTime(QTime.fromString('15:30:00', 'H:mm:ss'))
        axis_x.setRange(axis_x_min, axis_x_max)

        self.axis_y = axis_y = QValueAxis()
        axis_y.setRange(0, 1)
        axis_y.setTitleText(headers[1])

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        # chart.setTitle("Sample")

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(view)
        self.resize(1000, 600)

        self.timer = timer = QTimer()
        timer.timeout.connect(self.update_data)
        timer.setInterval(5)
        timer.start()

    def adjust_yrange(self, y):
        if self.idx == 0:
            self.axis_y.setRange(y - 5, y + 5)
        else:
            y_min = self.axis_y.min()
            y_max = self.axis_y.max()
            if y < y_min:
                y_min = y
                self.axis_y.setRange(y_min, y_max)
            if y_max < y:
                y_max = y
                self.axis_y.setRange(y_min, y_max)

    def append_point(self):
        point = self.data.at(self.idx)
        x = point.x()
        y = point.y()
        self.series.append(x, y)
        self.adjust_yrange(y)

        self.idx += 1

    def update_data(self):
        if self.idx >= self.data.count() - 1:
            self.timer.stop()

        self.append_point()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
