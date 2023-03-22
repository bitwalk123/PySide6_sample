#!/usr/bin/env python
# coding: utf-8
import random
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QScatterSeries,
    QValueAxis,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class ScatterChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        chart = QChart()
        chart.setTitle('Scatter Chart')
        chart.setDropShadowEnabled(False)
        chart.legend().hide()

        axis_x = QValueAxis()
        axis_x.setRange(0, 1)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        axis_y = QValueAxis()
        axis_y.setRange(0, 1)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        series = QScatterSeries()
        series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
        series.setMarkerSize(5)
        series.setPen(QPen(Qt.PenStyle.NoPen))
        series.clicked.connect(self.handle)

        # Data prep.
        list_xy_pair = [[random.random(), random.random()] for i in range(100)]

        for xy_pair in list_xy_pair:
            series.append(*xy_pair)

        chart.addSeries(series)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        return chart

    def handle(self, event):
        print(event)

    def mousePressEvent(self, event):
        print(event)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        scatter = ScatterChart()
        self.setCentralWidget(scatter)
        self.resize(500, 500)
        self.setWindowTitle('ScatterChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
