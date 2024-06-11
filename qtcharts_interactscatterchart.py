#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-scatterinteractions-example.html
import math
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QScatterSeries,
)
from PySide6.QtCore import (
    QPointF,
    Qt,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class InteractScatterChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def init_ui(self):
        series_a = QScatterSeries()
        series_a.setName('scatter1')
        series_a.setColor('cyan')
        for i in range(8):
            x = 0.5 * (i + 1)
            for j in range(8):
                y = 0.5 * (j + 1)
                series_a << QPointF(x, y)

        series_b = QScatterSeries()
        series_b.setName('scatter2')
        series_b.setColor('magenta')

        series_a.clicked.connect(lambda point: self.handleClickedPoint(point, series_a, series_b))
        series_b.clicked.connect(lambda point: self.handleClickedPoint(point, series_b, series_a))

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series_a)
        chart.addSeries(series_b)

        chart.setTitle('Click to interact with scatter points')
        chart.createDefaultAxes()
        chart.axes(Qt.Orientation.Horizontal)[0].setRange(0, 4.5)
        chart.axes(Qt.Orientation.Vertical)[0].setRange(0, 4.5)

        return chart

    def handleClickedPoint(self, clickedPoint: QPointF, series_old: QScatterSeries, series_new: QScatterSeries):
        # Find the closest point from series 1
        INT_MAX = 100000
        closest = QPointF(INT_MAX, INT_MAX)
        distance = float(INT_MAX)
        points = series_old.points()
        for currentPoint in points:
            currentDistance = math.sqrt((currentPoint.x() - clickedPoint.x())
                                        * (currentPoint.x() - clickedPoint.x())
                                        + (currentPoint.y() - clickedPoint.y())
                                        * (currentPoint.y() - clickedPoint.y()))
            if currentDistance < distance:
                distance = currentDistance
                closest = currentPoint

        # Remove the closes point from series 1 and append it to series 2
        series_old.remove(closest)
        series_new.append(closest)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        scatter = InteractScatterChart()
        self.setCentralWidget(scatter)
        self.resize(500, 300)
        self.setWindowTitle('InteractScatterChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
