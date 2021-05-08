import sys
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import QtCharts


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(500, 300)
        self.show()

    def initUI(self):
        self.series = QtCharts.QLineSeries()
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 8)
        self.series.append(7, 4)
        self.series.append(10, 5)
        self.series.append(QPointF(11, 1))
        self.series.append(QPointF(13, 3))
        self.series.append(QPointF(17, 6))
        self.series.append(QPointF(18, 3))
        self.series.append(QPointF(20, 2))
        self.chart = QtCharts.QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Simple line chart example")
        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.chartView)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
