#!/usr/bin/env python
# coding: utf-8

# Reference:
# https://stackoverflow.com/questions/64446378/how-to-add-a-crosshair-to-a-pyqt5-graph
import random
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QScatterSeries,
    QValueAxis,
)
from PySide6.QtCore import Qt, QPointF, QPoint
from PySide6.QtGui import (
    QMouseEvent,
    QPainter,
    QPen, QColor,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class ScatterChart(QChartView):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setRenderHint(QPainter.Antialiasing)
        self._value_pos = QPoint()
        self.setMouseTracking(True)

    def init_ui(self):
        chart = QChart()
        self.setChart(chart)
        chart.setTitle('Scatter Chart')
        chart.setDropShadowEnabled(False)
        chart.legend().hide()

        axis_x = QValueAxis()
        axis_x.setRange(0, 1)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        axis_y = QValueAxis()
        axis_y.setRange(0, 1)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        series = QScatterSeries()
        series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
        series.setMarkerSize(5)
        series.setPen(QPen(Qt.PenStyle.NoPen))

        # Data prep.
        list_xy_pair = [[random.random(), random.random()] for i in range(100)]

        for xy_pair in list_xy_pair:
            series.append(*xy_pair)

        chart.addSeries(series)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    def drawForeground(self, painter, rect):
        super().drawForeground(painter, rect)
        if self.chart() is None or self._value_pos.isNull():
            return

        pen = QPen(QColor('salmon'))
        pen.setWidth(1)
        painter.setPen(pen)

        area = self.chart().plotArea()
        sp = self.chart().mapToPosition(self._value_pos)
        x1 = QPointF(area.left() + pen.width() / 2, sp.y())
        x2 = QPointF(area.right() - pen.width() / 2, sp.y())
        y1 = QPointF(sp.x(), area.top() + pen.width() / 2)
        y2 = QPointF(sp.x(), area.bottom() - pen.width() / 2)

        if area.left() <= sp.x() <= area.right():
            painter.drawLine(y1, y2)
        if area.top() < sp.y() < area.bottom():
            painter.drawLine(x1, x2)

    def mousePressEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if self.chart() is None:
            return
        sp = self.mapToScene(event.pos())
        if self.chart().plotArea().contains(sp):
            self._value_pos = self.chart().mapToValue(sp)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        self.update()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        scatter = ScatterChart()
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
