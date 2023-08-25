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
from PySide6.QtCore import (
    QPointF,
    QRect,
    Qt,
    Signal, QEvent,
)
from PySide6.QtGui import (
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QMainWindow,
    QPushButton,
    QRubberBand,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ScatterPlot(QChart):
    def __init__(self, list_data: list):
        super().__init__()

        self.setDropShadowEnabled(False)
        self.legend().hide()

        self.axis_x = QValueAxis()
        self.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)

        self.axis_y = QValueAxis()
        self.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)

        series = QScatterSeries()
        series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
        series.setMarkerSize(10)
        series.setPen(QPen(Qt.PenStyle.NoPen))

        for xy_pair in list_data:
            series.append(*xy_pair)

        self.addSeries(series)
        series.attachAxis(self.axis_x)
        series.attachAxis(self.axis_y)

        self.axis_x.setRange(0, 1)
        self.axis_y.setRange(0, 1)

        # for selected data
        self.series_selected = QScatterSeries()
        self.series_selected.setMarkerShape(
            QScatterSeries.MarkerShape.MarkerShapeCircle
        )
        self.series_selected.setBrush(Qt.GlobalColor.red)
        self.series_selected.setMarkerSize(10)
        self.series_selected.setPen(QPen(Qt.PenStyle.NoPen))

        self.addSeries(self.series_selected)
        self.series_selected.attachAxis(self.axis_x)
        self.series_selected.attachAxis(self.axis_y)

    def highlightSelectedPoints(self, list_selected):
        for xy_pair in list_selected:
            self.series_selected.append(*xy_pair)

    def clearSelected(self):
        self.series_selected.clear()


class ChartView(QChartView):
    def __init__(self, list_data: list):
        super().__init__()

        self.rect = None
        self.origin = None
        self.mouseReleased = False
        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)

        self.chart = ScatterPlot(list_data)
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMaximumSize(500, 500)

    def mousePressEvent(self, event):
        self.rubberBand.hide()
        self.origin = event.position()
        self.mouseReleased = False

    def mouseMoveEvent(self, event):
        if self.origin is None:
            return

        if self.mouseReleased:
            return

        self.rubberBand.show()
        self.rubberBand.setGeometry(
            QRect(
                self.origin.toPoint(),
                event.position().toPoint()
            ).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.mouseReleased = True
        self.rect = QRect(
            self.origin.toPoint(),
            event.position().toPoint()
        ).normalized()

    def clearSelected(self):
        self.chart.clearSelected()

    def getSelectedArea(self) -> list:
        if not self.mouseReleased:
            return list()

        p1 = self.chart.mapToValue(
            QPointF(
                self.rect.x(),
                self.rect.y()
            )
        )
        p2 = self.chart.mapToValue(
            QPointF(
                self.rect.x() + self.rect.width(),
                self.rect.y() + self.rect.height()
            )
        )
        return [p1.x(), p1.y(), p2.x(), p2.y()]

    def addSelectedPoins(self, list_selected):
        self.chart.highlightSelectedPoints(list_selected)
        self.rubberBand.hide()


class DockControl(QDockWidget):
    selected = Signal()
    clear = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        base = QWidget()
        self.setWidget(base)
        layout = QVBoxLayout()
        base.setLayout(layout)

        but_sel = QPushButton('Select')
        but_sel.clicked.connect(self.on_click_selected)
        layout.addWidget(but_sel)

        but_clr = QPushButton('Clear')
        but_clr.clicked.connect(self.on_click_clear)
        layout.addWidget(but_clr)

        vpad = QWidget()
        vpad.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding
        )
        layout.addWidget(vpad)

    def on_click_selected(self):
        self.selected.emit()

    def on_click_clear(self):
        self.clear.emit()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cview = None
        self.list_data = None
        self.init_ui()

        # self.resize(600, 500)
        self.setWindowTitle('Scatter Plot')

    def init_ui(self):
        # ChartView widget
        self.list_data = self.data_prep()
        self.cview = ChartView(self.list_data)
        self.setCentralWidget(self.cview)

        # right dock
        dockWidget = DockControl()
        dockWidget.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea
        )
        dockWidget.selected.connect(self.on_click_selected)
        dockWidget.clear.connect(self.on_click_clear)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dockWidget
        )

    @staticmethod
    def data_prep() -> list:
        list_data = list()
        for r in range(100):
            xy_pair = [random.random(), random.random()]
            list_data.append(xy_pair)
        return list_data

    def on_click_selected(self):
        area_selected = self.cview.getSelectedArea()
        if len(area_selected) > 0:
            self.points_in_area(area_selected)
        else:
            print('area not selected!')

    def points_in_area(self, area):
        x1, y1, x2, y2 = area
        list_selected = list()
        for x, y in self.list_data:
            if x1 <= x and x2 >= x and y1 >= y and y2 <= y:
                xypair = [x, y]
                list_selected.append(xypair)
        self.cview.addSelectedPoins(list_selected)

    def on_click_clear(self):
        self.cview.clearSelected()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
