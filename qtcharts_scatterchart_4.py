#!/usr/bin/env python
# coding: utf-8
from PySide6.QtCharts import QChartView
from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QApplication


class ChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value_pos = QPoint()
        self.setMouseTracking(True)

    def drawForeground(self, painter, rect):
        super().drawForeground(painter, rect)
        if self.chart() is None or self._value_pos.isNull():
            return

        pen = QPen(QColor("salmon"))
        pen.setWidth(8)
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

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.chart() is None:
            return
        sp = self.mapToScene(event.pos())
        if self.chart().plotArea().contains(sp):
            self._value_pos = self.chart().mapToValue(sp)
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.unsetCursor()
        self.update()



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow(start = 0)
    w.show()
    sys.exit(app.exec_())