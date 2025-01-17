#!/usr/bin/env python
import csv
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import (
    QTime,
    Qt, QDateTime, QTimeZone,
)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


def csv_reader(csvname: str) -> tuple[QLineSeries, list]:
    series = QLineSeries()
    msec_delta = 9 * 60 * 60 * 1000

    with open(csvname) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
                continue

            tick_time = QTime.fromString(row[0], 'H:mm:ss')
            series.append(tick_time.msecsSinceStartOfDay() - msec_delta, float(row[1]))
            # series.append(tick_time.msecsSinceStartOfDay(), float(row[1]))

    return series, headers


class LineChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def init_ui(self):
        series, headers = csv_reader('tick.csv')

        pen = series.pen()
        pen.setColor('gray')
        pen.setWidthF(0.5)
        series.setPen(pen)
        series.setPointsVisible(True)
        series.setMarkerSize(1.5)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.setTitle('Stock Price trend')

        axis_x = QDateTimeAxis()
        axis_x.setTickCount(14)
        axis_x.setFormat('HH:mm')

        axis_x.setTitleText(headers[0])
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTickCount(10)
        axis_y.setLabelFormat('%i')
        axis_y.setTitleText(headers[1])
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        axis_x_min = axis_x.min()
        # axis_x_min.setTimeZone(QTimeZone.systemTimeZone(), QDateTime.TransitionResolution.Reject)
        axis_x_min.setTime(QTime.fromString('9:00:00', 'H:mm:ss'))
        axis_x_max = axis_x.max()
        # axis_x_max.setTimeZone(QTimeZone.systemTimeZone(), QDateTime.TransitionResolution.Reject)
        axis_x_max.setTime(QTime.fromString('15:30:00', 'H:mm:ss'))
        axis_x.setRange(axis_x_min, axis_x_max)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        linechart = LineChart()
        self.setCentralWidget(linechart)
        self.resize(1000, 600)
        self.setWindowTitle('LineChart (Time)')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
