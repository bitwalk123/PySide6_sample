#!/usr/bin/env python
# coding: utf-8
# Reference
#   hhttps://doc.qt.io/qt-6/qtcharts-zoomlinechart-example.html
import math
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
)
from PySide6.QtCore import (
    QEvent,
    QPointF,
    QRandomGenerator
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class ZoomLineChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMouseTracking(True)
        self.setInteractive(True)
        self.setRubberBand(QChartView.RectangleRubberBand)

    def init_ui(self):
        series = QLineSeries()
        for i in range(500):
            p = QPointF(i, math.sin(math.pi / 50 * i) * 100 + QRandomGenerator.global_().bounded(50))
            series << p

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle('Zoom in/out example')

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        zoomlinechart = ZoomLineChart()
        self.setCentralWidget(zoomlinechart)
        self.resize(500, 300)
        self.setWindowTitle('ZoomLineChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
