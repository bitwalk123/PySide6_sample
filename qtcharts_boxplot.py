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
#   https://doc.qt.io/qt-5/qtcharts-boxplotchart-example.html
class BoxPlot(QChartView):
    def __init__(self):
        super().__init__()
        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)

    def init_ui(self):
        # acmeSeries = QBoxPlotSeries()
        # acmeSeries.setName('Acme Ltd')
        acmeSeries = self.box_reader('acme_data.txt', 'Acme Ltd')

        # boxWhiskSeries = QBoxPlotSeries()
        # boxWhiskSeries.setName('BoxWhisk Inc')
        boxWhiskSeries = self.box_reader('boxwhisk_data.txt', 'BoxWhisk Inc')

        chart = QChart()
        chart.addSeries(acmeSeries)
        chart.addSeries(boxWhiskSeries)
        chart.setTitle('Acme Ltd and BoxWhisk Inc share deviation in 2012')
        # chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()
        chart.axes(Qt.Vertical)[0].setMin(15.0)
        chart.axes(Qt.Horizontal)[0].setMax(34.0)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart

    def box_reader(self, name_file: str, name_series: str):
        series = QBoxPlotSeries()
        series.setName(name_series)

        f = open(name_file, 'r')
        datalist = f.readlines()
        f.close()

        for data in datalist:
            list_element = data.strip().split()
            if len(list_element) == 0:
                continue
            if list_element[0] == '#':
                continue

            boxset = QBoxSet(list_element[0])
            for i in range(1, len(list_element)):
                boxset.append(float(list_element[i]))

            series.append(boxset)

        return series


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        boxplot = BoxPlot()
        self.setCentralWidget(boxplot)
        self.resize(700, 400)
        self.setWindowTitle('BoxPlot')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
