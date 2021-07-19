import sys
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBoxPlotSeries,
    QBoxSet,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


# Reference
#   https://doc.qt.io/qt-5/qtcharts-linechart-example.html
class Boxplot(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        series = QBoxPlotSeries()
        series.setName('Test')

        set01 = QBoxSet('Sample')
        set01 << 27.74 << 27.28 << 27.86 << 28.05 << 28.64 << 27.47 << 28.30 << 28.22 << 28.72 << 26.50 << 26.62 << 26.50 << 26.15 << 26.47 << 26.41 << 25.78 << 24.82 << 24.89 << 24.88 << 24.60 << 23.85

        series.append(set01)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Acme Ltd and BoxWhisk Inc share deviation in 2012')
        # chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()
        chart.axes(Qt.Vertical)[0].setMin(15.0)
        chart.axes(Qt.Horizontal)[0].setMax(34.0)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        boxplot = Boxplot()
        self.setCentralWidget(boxplot)
        self.resize(500, 300)
        self.setWindowTitle('LineChart')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
