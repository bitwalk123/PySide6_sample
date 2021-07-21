#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-logvalueaxis-example.html
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QLogValueAxis,
    QValueAxis,
)
from PySide6.QtCore import (
    QPointF,
    Qt
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class LogLineChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series = QLineSeries()
        series.setPointsVisible(True)
        series << QPointF(1.0, 1.0) << QPointF(2.0, 73.0) << QPointF(3.0, 268.0) \
        << QPointF(4.0, 17.0) << QPointF(5.0, 4325.0) << QPointF(6.0, 723.0)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.setTitle('Logarithmic axis example')

        axisX = QValueAxis()
        axisX.setTitleText('Data point')
        axisX.setLabelFormat('%i')
        axisX.setTickCount(series.count())
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QLogValueAxis()
        axisY.setTitleText('Values (Log10)')
        axisY.setLabelFormat('%.0E')
        axisY.setBase(10.0)
        axisY.setMinorTickCount(-1)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        linechart = LogLineChart()
        self.setCentralWidget(linechart)
        self.resize(500, 300)
        self.setWindowTitle('LogLineChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
