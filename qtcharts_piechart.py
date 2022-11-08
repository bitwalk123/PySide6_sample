#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-piechart-example.html
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QPieSeries,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPainter,
    QPen
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class PieChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series = QPieSeries()
        series.append('Jane', 25)
        series.append('Joe', 16)
        series.append('Andy', 9)
        series.append('Barbara', 4)
        series.append('Axel', 1)

        slice1 = series.slices()[1]
        slice1.setExploded()
        slice1.setLabelVisible()
        slice1.setPen(QPen(Qt.darkGreen, 2))
        slice1.setBrush(Qt.green)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Simple piechart example')
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        piechart = PieChart()
        self.setCentralWidget(piechart)
        self.resize(500, 300)
        self.setWindowTitle('PieChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
