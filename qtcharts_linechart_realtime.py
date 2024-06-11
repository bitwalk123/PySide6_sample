#!/usr/bin/env python
import sys
from math import sin, pi

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow


def get_red_pen() -> QPen:
    pen = QPen(Qt.GlobalColor.red)
    pen.setWidth(1)
    return pen


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x = 0

        self.series = QLineSeries()
        self.series.setPen(get_red_pen())
        self.series.setPointsVisible(True)
        self.series.setMarkerSize(2.0)
        self.series.append(self.x, 0)

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText('X')
        self.axis_x.setTickCount(5)
        self.axis_x.setRange(0, 0)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText('Y')
        self.axis_y.setRange(-1, 1)

        chart = QChart()
        chart.setTitle("Sample")
        chart.addSeries(self.series)
        chart.legend().hide()

        chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axis_x)

        chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_y)

        view = QChartView(chart)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(view)
        self.resize(600, 400)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.setInterval(50)
        self.timer.start()

    def update_data(self):
        self.x += 0.02 * pi
        self.series.append(self.x, sin(self.x))
        x_max = round(self.x + 0.5)
        if self.axis_x.max() < x_max:
            self.axis_x.setRange(0, self.axis_x.max() + 4)
        if self.x > 10 * pi:
            self.timer.stop()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
