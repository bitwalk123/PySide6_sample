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
from PySide6.QtCore import (
    QPoint,
    QPointF,
    QRect,
    QRectF,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QMouseEvent,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class ScatterView(QChartView):
    def __init__(self, list_data):
        super().__init__()
        self.list_data = list_data
        self.init_ui()
        self.setRenderHint(QPainter.Antialiasing)
        self._value_pos = QPoint()
        self.setMouseTracking(True)

    def generate_scatter_series(self):
        series = QScatterSeries()
        series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
        series.setMarkerSize(10)
        series.setPen(QPen(Qt.PenStyle.NoPen))
        for xy in self.list_data:
            series.append(*xy)
        return series

    def generate_value_axis(self):
        axis = QValueAxis()
        axis.setRange(0, 1)
        return axis

    def init_ui(self):
        chrt = QChart()
        self.setChart(chrt)
        chrt.setTitle('Scatter Plot example')
        chrt.setDropShadowEnabled(False)
        chrt.legend().hide()

        # Series
        series = self.generate_scatter_series()
        chrt.addSeries(series)

        # X axis
        axis_x = self.generate_value_axis()
        chrt.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        # Y axis
        axis_y = self.generate_value_axis()
        chrt.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # Override methods
    def drawForeground(self, painter: QPainter, rect: QRectF):
        super().drawForeground(painter, rect)
        if self.chart() is None or self._value_pos.isNull():
            return

        pen = QPen(QColor('red'))
        pen.setWidth(1)
        painter.setPen(pen)

        area: QRect = self.chart().plotArea()
        point: QPointF = self.chart().mapToPosition(self._value_pos)
        horiz_left = QPointF(area.left() + pen.width() / 2, point.y())
        horiz_right = QPointF(area.right() - pen.width() / 2, point.y())
        vert_top = QPointF(point.x(), area.top() + pen.width() / 2)
        vert_bottom = QPointF(point.x(), area.bottom() - pen.width() / 2)

        if area.left() <= point.x() <= area.right():
            painter.drawLine(vert_top, vert_bottom)
        if area.top() < point.y() < area.bottom():
            painter.drawLine(horiz_left, horiz_right)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if self.chart() is None:
            return

        point_item: QPoint = event.position().toPoint()
        point_scene: QPointF = self.mapToScene(point_item)
        #print(point_scene.x(), point_scene.y())
        if self.chart().plotArea().contains(point_scene):
            self._value_pos = self.chart().mapToValue(point_scene)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()

        self.update()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        # Data prep.
        list_xy_pair = [[random.random(), random.random()] for i in range(100)]

        scatter = ScatterView(list_xy_pair)
        self.setCentralWidget(scatter)
        self.resize(500, 500)
        self.setWindowTitle('ScatterView')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
