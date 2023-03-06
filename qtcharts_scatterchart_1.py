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
    QScatterSeries, QValueAxis,
)
from PySide6.QtCore import (
    QPointF,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QImage,
    QPainter,
    QPainterPath, QPen,
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
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        list_sample = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

        for sample in list_sample:
            series = QScatterSeries()
            series.setName(sample)
            series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
            series.setMarkerSize(5)
            series.setPen(QPen(Qt.PenStyle.NoPen))

            df = pd.DataFrame(np.random.random(size=(100, 2)), columns=['X', 'Y'])
            for r in range(len(df)):
                xy_pair = df.iloc[r, :].to_list()
                series.append(*xy_pair)

            chart.addSeries(series)
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)

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
