#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-scatterchart-example.html
import math
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLegend,
    QScatterSeries,
)
from PySide6.QtCore import (
    QPointF,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QImage,
    QPainter,
    QPainterPath,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class InteractScatterChart(QChartView):
    def __init__(self):
        super().__init__()
        self.series1 = QScatterSeries()
        self.series2 = QScatterSeries()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        self.series1.setName('scatter1')
        self.series1.setColor('cyan')
        for i in range(8):
            x = 0.5 * (i + 1)
            for j in range(8):
                y = 0.5 * (j + 1)
                self.series1 << QPointF(x, y)
        self.series1.clicked.connect(self.handleClickedPoint)

        self.series2.setName('scatter2')
        self.series2.setColor('magenta')

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(self.series1)
        chart.addSeries(self.series2)

        chart.setTitle('Click to interact with scatter points')
        chart.createDefaultAxes()
        chart.axes(Qt.Horizontal)[0].setRange(0, 4.5)
        chart.axes(Qt.Vertical)[0].setRange(0, 4.5)

        return chart

    def handleClickedPoint(self, clickedPoint: QPointF):
        # Find the closest point from series 1
        INT_MAX = 10000
        closest = QPointF(INT_MAX, INT_MAX)
        distance = float(INT_MAX)
        points = self.series1.points()
        for currentPoint in points:
            currentDistance = math.sqrt((currentPoint.x() - clickedPoint.x())
                                        * (currentPoint.x() - clickedPoint.x())
                                        + (currentPoint.y() - clickedPoint.y())
                                        * (currentPoint.y() - clickedPoint.y()))
            if currentDistance < distance:
                distance = currentDistance
                closest = currentPoint

        # Remove the closes point from series 1 and append it to series 2
        self.series1.remove(closest)
        self.series2.append(closest)


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
