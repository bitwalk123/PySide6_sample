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
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def init_ui(self):
        list_value = [1, 2, 2, 4, 6, 3, 2, 1]
        barset = QBarSet('Frequency')
        for value in list_value:
            barset << value

        series = QBarSeries()
        series.setBarWidth(1)
        series.append(barset)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Simple barchart example')
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        categories = ['1', '2', '3', '4', '5', '6']
        axis_x = QBarCategoryAxis()
        axis_x.setLabelsVisible(False)
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        #axis_y.setRange(0, 15)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        return chart


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
