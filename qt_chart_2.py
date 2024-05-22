import sys
from PySide6.QtCore import (
    QPointF,
    Qt,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
)
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
)


#  Reference
#    https://stackoverflow.com/questions/58350723/qchart-add-axis-not-show-and-when-hovered-info-not-work-correct
class Example(QChartView):
    def __init__(self):
        super().__init__()
        self.chart = QChart()
        self.setChart(self.chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        axis_x = QValueAxis()
        axis_x.setTickCount(10)
        axis_x.setTitleText('x')
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        axis_y= QValueAxis()
        axis_y.setLinePenColor(Qt.GlobalColor.red)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        series = QLineSeries()
        series.setPointsVisible(True)
        series.hovered.connect(self.show_tool_tip)
        series << QPointF(1, 5) << QPointF(3.5, 18) << QPointF(4.8, 7.5) << QPointF(10, 2.5)

        self.chart.addSeries(series)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        self.value_label = QLabel(self)

    def show_tool_tip(self, pt, state):
        pos = self.chart.mapToPosition(pt)
        if state:
            self.value_label.move(int(pos.x()), int(pos.y()))
            self.value_label.setText(f'{pt}')
            self.value_label.show()
        else:
            self.value_label.hide()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
