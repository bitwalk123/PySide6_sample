#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-lineandbar-example.html
import sys
from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSet,
    QBarSeries,
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import (
    QPoint,
    Qt,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class LineBarChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        set0 = QBarSet('Jane')
        set1 = QBarSet('John')
        set2 = QBarSet('Axel')
        set3 = QBarSet('Mary')
        set4 = QBarSet('Samantha')

        set0 << 1 << 2 << 3 << 4 << 5 << 6
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2

        barseries = QBarSeries()
        barseries.append(set0)
        barseries.append(set1)
        barseries.append(set2)
        barseries.append(set3)
        barseries.append(set4)

        lineseries = QLineSeries()
        lineseries.setName('trend')
        lineseries.append(QPoint(0, 4))
        lineseries.append(QPoint(1, 15))
        lineseries.append(QPoint(2, 20))
        lineseries.append(QPoint(3, 4))
        lineseries.append(QPoint(4, 12))
        lineseries.append(QPoint(5, 17))

        chart = QChart()
        chart.addSeries(barseries)
        chart.addSeries(lineseries)
        chart.setTitle('Line and barchart example')
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        lineseries.attachAxis(axisX)
        barseries.attachAxis(axisX)
        axisX.setRange('Jan', 'Jun')

        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        lineseries.attachAxis(axisY)
        barseries.attachAxis(axisY)
        axisY.setRange(0, 20)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        linebarchart = LineBarChart()
        self.setCentralWidget(linebarchart)
        self.resize(500, 300)
        self.setWindowTitle('LineBarChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
