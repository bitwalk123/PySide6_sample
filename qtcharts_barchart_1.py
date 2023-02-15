#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-barchart-example.html
import sys
from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSet,
    QBarSeries,
    QChart,
    QChartView,
    QValueAxis,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class BarChart(QChartView):
    def __init__(self):
        super().__init__()

        series = QBarSeries()
        list_value = [1, 2, 2, 4, 6, 3, 2, 1]
        for v in list_value:
            barset = QBarSet('')
            barset.setColor(QColor('blue'))
            barset << v
            series.append(barset)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()

        categories = ['']
        axis_x = QBarCategoryAxis()
        axis_x.setCategories(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 15)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        barchart = BarChart()
        self.setCentralWidget(barchart)
        self.resize(500, 300)
        self.setWindowTitle('BarChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
