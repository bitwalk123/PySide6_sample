import sys
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries
)


class Example(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.resize(400, 300)
        self.setWindowTitle('LineChart')

    def init_ui(self):
        series = QLineSeries()
        series.setPointsVisible(True)
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)
        series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 2)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle('Simple line chart example')

        return chart


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
