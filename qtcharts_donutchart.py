#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-donutchart-example.html
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QPieSeries,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class DonutChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series = QPieSeries()
        series.setHoleSize(0.35)

        series.append("Protein 4.2%", 4.2)

        slice = series.append("Fat 15.6%", 15.6)
        slice.setExploded()
        slice.setLabelVisible()

        series.append("Other 23.8%", 23.8)
        series.append("Carbs 56.4%", 56.4)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Donut with a lemon glaze (100g)')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        donutchart = DonutChart()
        self.setCentralWidget(donutchart)
        self.resize(550, 300)
        self.setWindowTitle('DonutChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
