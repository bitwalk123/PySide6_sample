#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-scatterchart-example.html
import math
import sys
import numpy as np
import pandas as pd
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


class ScatterChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series1 = QScatterSeries()
        series1.setName('sample')
        series1.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        series1.setMarkerSize(10.0)

        df = pd.DataFrame(np.random.random(size=(1000, 2)), columns=['X', 'Y'])
        series1.append(0, 6)
        series1.append(2, 4)
        series1.append(3, 8)
        series1.append(7, 4)
        series1.append(10, 5)

        chart = QChart()
        chart.addSeries(series1)

        chart.setTitle('Simple scatterchart example')
        chart.createDefaultAxes()
        chart.setDropShadowEnabled(False)

        chart.legend().setMarkerShape(QLegend.MarkerShapeFromSeries)

        return chart


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
