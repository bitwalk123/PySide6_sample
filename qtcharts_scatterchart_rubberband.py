#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QRubberBand.html
import random
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QScatterSeries,
    QValueAxis,
)
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import (
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow, QRubberBand,
)


class ScatterSample(QChart):
    def __init__(self, list_data: list):
        super().__init__()

        self.setTitle('Scatter Chart')
        self.setDropShadowEnabled(False)
        self.legend().hide()

        axis_x = QValueAxis()
        self.addAxis(
            axis_x,
            Qt.AlignmentFlag.AlignBottom
        )

        axis_y = QValueAxis()
        self.addAxis(
            axis_y,
            Qt.AlignmentFlag.AlignLeft
        )

        series = QScatterSeries()
        series.setMarkerShape(
            QScatterSeries.MarkerShape.MarkerShapeCircle
        )
        series.setMarkerSize(10)
        series.setPen(QPen(Qt.PenStyle.NoPen))

        for xy_pair in list_data:
            series.append(*xy_pair)

        self.addSeries(series)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        axis_x.setRange(0, 1)
        axis_y.setRange(0, 1)


class ChartView(QChartView):
    def __init__(self, list_data: list):
        super().__init__()
        self.origin = None
        self.mouseReleased = False
        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.rubberBand.show()

        chart = ScatterSample(list_data)
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def mousePressEvent(self, event):
        self.origin = event.position()
        self.mouseReleased = False

    def mouseMoveEvent(self, event):
        if self.origin is None:
            return

        if self.mouseReleased:
            return

        self.rubberBand.setGeometry(
            QRect(
                self.origin.toPoint(),
                event.position().toPoint()
            ).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.mouseReleased = True


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.resize(500, 500)
        self.setWindowTitle('ScatterChart')

    def init_ui(self):
        # Plot data
        list_data = list()
        for r in range(100):
            xy_pair = [random.random(), random.random()]
            list_data.append(xy_pair)

        # ChartView widget
        cview = ChartView(list_data)
        self.setCentralWidget(cview)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
