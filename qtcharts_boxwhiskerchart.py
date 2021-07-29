#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-boxplotchart-example.html

import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBoxPlotSeries,
    QBoxSet,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


def box_data_reader(name_file: str, name_series: str):
    series = QBoxPlotSeries()
    series.setName(name_series)

    with open(name_file) as f:
        for line in f:
            values = line.strip().split()
            if len(values) == 0:
                continue
            if values[0] == '#':
                continue

            boxset = QBoxSet(values[0])
            for i in range(1, len(values)):
                boxset.append(float(values[i]))

            series.append(boxset)

    return series


class BoxWhiskerChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series_acme = box_data_reader('acme_data.txt', 'Acme Ltd')
        series_boxwhisk = box_data_reader('boxwhisk_data.txt', 'BoxWhisk Inc')

        chart = QChart()
        chart.addSeries(series_acme)
        chart.addSeries(series_boxwhisk)
        chart.setTitle('Acme Ltd and BoxWhisk Inc share deviation in 2012')
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()
        chart.axes(Qt.Vertical)[0].setMin(15.0)
        chart.axes(Qt.Horizontal)[0].setMax(34.0)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        boxplot = BoxWhiskerChart()
        self.setCentralWidget(boxplot)
        self.resize(700, 400)
        self.setWindowTitle('Box & Whisker Chart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
