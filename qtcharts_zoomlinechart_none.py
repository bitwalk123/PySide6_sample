#!/usr/bin/env python
# coding: utf-8
# Reference
#   https://doc.qt.io/qt-6/qtcharts-zoomlinechart-example.html
#   https://stackoverflow.com/questions/48164065/implement-selection-on-qchartview
import math
import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries, QValueAxis,
)
from PySide6.QtCore import (
    QPoint,
    QPointF,
    QRandomGenerator,
    QRect,
    Qt, QRectF
)
from PySide6.QtGui import (
    QMouseEvent,
    QPainter,
    QResizeEvent,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QRubberBand,
)


class ZoomLineChart(QChartView):

    def __init__(self):
        super().__init__()
        self.m_drawRubberBand = None
        self.m_rubberBand = QRubberBand(QRubberBand.Shape.Rectangle)
        self.m_rubberBandOrigin = None
        self.m_chartRectF = QRectF()

        chart = self.init_ui()
        self.setChart(chart)
        self.setRubberBand(QChartView.RubberBand.RectangleRubberBand)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMouseTracking(True)
        self.setInteractive(True)
        self.setRubberBand(QChartView.RubberBand.RectangleRubberBand)

    def init_ui(self):
        series = QLineSeries()
        for i in range(500):
            p = QPointF(i, math.sin(math.pi / 50 * i) * 100 + QRandomGenerator.global_().bounded(50))
            series << p

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle('Zoom in/out example')

        return chart

    def point_to_chart(self, pnt: QPoint):
        scene_point: QPointF = self.chart().mapToScene(pnt)
        chart_point: QPointF = self.chart().mapToValue(scene_point)

        return chart_point

    def chart_to_view_point(self, char_coord: QPointF):
        scene_point: QPointF = self.chart().mapToPosition(char_coord)
        view_point: QPoint = self.chart().mapFromScene(scene_point)

        return view_point

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.m_rubberBand.isVisible():
            self.update_rubber_band(event)
            self.m_drawRubberBand = False
            self.save_current_rubber_band()

    def resizeEvent(self, event: QResizeEvent):
        # self.resizeEvent(event)
        super().resizeEvent(event)

        if self.m_rubberBand.isVisible():
            self.restore_rubber_band()

        self.apply_nice_numbers()

    def update_rubber_band(self, event: QMouseEvent):
        rect: QRect = self.chart().plotArea().toRect()
        width: int = event.pos().x() - self.m_rubberBandOrigin.x()
        height: int = event.pos().y() - self.m_rubberBandOrigin.y()
        print(height, width)

        if not self.rubberBand().testFlag(Qt.VerticalRubberBand):
            self.m_rubberBandOrigin.setY(rect.top())
            height = rect.height()

        if not self.rubberBand().testFlag(Qt.HorizontalRubberBand):
            self.m_rubberBandOrigin.setX(rect.left())
            width = rect.width()

        self.m_rubberBand.setGeometry(
            QRect(
                self.m_rubberBandOrigin.x(),
                self.m_rubberBandOrigin.y(),
                width,
                height
            ).normalized()
        )

    def save_current_rubber_band(self):
        rect: QRect = self.m_rubberBand.geometry()

        chart_top_left: QPointF = self.point_to_chart(rect.topLeft());
        self.m_chartRectF.setTopLeft(chart_top_left);

        chart_bottom_right: QPointF = self.point_to_chart(rect.bottomRight());
        self.m_chartRectF.setBottomRight(chart_bottom_right);

    def restore_rubber_band(self):
        view_top_left: QPoint = self.chart_to_view_point(self.m_chartRectF.topLeft())
        view_bottom_right: QPoint = self.chart_to_view_point(self.m_chartRectF.bottomRight())

        self.m_rubberBandOrigin = view_top_left
        self.m_rubberBand.setGeometry(QRect(view_top_left, view_bottom_right))

    def apply_nice_numbers(self):
        axes_list = self.chart().axes()
        for abstract_axis in axes_list:
            value_axis: QValueAxis = abstract_axis
            if value_axis:
                value_axis.applyNiceNumbers()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        linechart = ZoomLineChart()
        self.setCentralWidget(linechart)
        self.resize(500, 300)
        self.setWindowTitle('ZoomLineChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
