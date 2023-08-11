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
    def __init__(self):
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

        list_sample = ['Sample 1']
        for sample in list_sample:
            series = QScatterSeries()
            series.setName(sample)
            series.setMarkerShape(
                QScatterSeries.MarkerShape.MarkerShapeCircle
            )
            series.setMarkerSize(5)
            series.setPen(QPen(Qt.PenStyle.NoPen))

            for r in range(100):
                xy_pair = [random.random(), random.random()]
                series.append(*xy_pair)

            self.addSeries(series)
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)

        axis_x.setRange(0, 1)
        axis_y.setRange(0, 1)


class ChartView(QChartView):
    origin = None

    def __init__(self):
        super().__init__()

        chart = ScatterSample()
        self.setChart(chart)
        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.setRenderHint(QPainter.Antialiasing)

    def mousePressEvent(self, event):
        self.origin = event.position()
        self.rubberBand.setGeometry(
            QRect(self.origin.toPoint(), QSize())
        )
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.origin is None:
            return

        self.rubberBand.setGeometry(
            QRect(self.origin.toPoint(), event.position().toPoint()).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.rubberBand.hide()
        QRect(self.origin.toPoint(), event.position().toPoint())
        # determine selection, for example using QRect::intersects()
        # and QRect::contains().


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        scatter = ChartView()
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
