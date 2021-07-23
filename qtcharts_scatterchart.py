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


class ScatterChart(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series0 = QScatterSeries()
        series0.setName('scatter1')
        series0.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        series0.setMarkerSize(15.0)

        series1 = QScatterSeries()
        series1.setName('scatter2')
        series1.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
        series1.setMarkerSize(20.0)

        series2 = QScatterSeries()
        series2.setName('scatter3')
        series2.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
        series2.setMarkerSize(30.0)

        series0.append(0, 6)
        series0.append(2, 4)
        series0.append(3, 8)
        series0.append(7, 4)
        series0.append(10, 5)

        series1 << QPointF(1, 1) << QPointF(3, 3) << QPointF(7, 6) << QPointF(8, 3) << QPointF(10, 2)
        series2 << QPointF(1, 5) << QPointF(4, 6) << QPointF(6, 3) << QPointF(9, 5)

        starPath = QPainterPath()
        starPath.moveTo(28, 15)
        for i in range(1, 6):
            starPath.lineTo(14 + 14 * math.cos(0.8 * i * math.pi),
                            15 + 14 * math.sin(0.8 * i * math.pi))
        starPath.closeSubpath()

        star = QImage(30, 30, QImage.Format_ARGB32)
        star.fill(Qt.transparent)

        painter = QPainter(star)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(246, 166, 37))
        painter.setBrush(painter.pen().color())
        painter.drawPath(starPath)
        painter.end()

        series2.setBrush(star)
        series2.setPen(QColor(Qt.transparent))

        chart = QChart()
        chart.addSeries(series0)
        chart.addSeries(series1)
        chart.addSeries(series2)

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
        self.resize(500, 300)
        self.setWindowTitle('ScatterChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
