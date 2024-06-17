import sys
from math import cos, pi, sin

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure


class MyCharts(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)

        self.ax1 = self.fig.add_subplot(2, 1, 1)
        self.ax2 = self.fig.add_subplot(2, 1, 2)
        self.ax2.sharex(self.ax1)

        self.ax1.grid()
        self.ax2.grid()


def draw_charts(charts: MyCharts):
    list_x = list()
    list_y1 = list()
    list_y2 = list()
    for t in range(1000):
        x = t * pi / 100
        list_x.append(x)
        list_y1.append(sin(x))
        list_y2.append(cos(x))
    charts.ax1.plot(list_x, list_y1, lw=1, c='C0')
    charts.ax2.plot(list_x, list_y2, lw=1, c='C1')


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        charts = MyCharts()
        self.setCentralWidget(charts)

        navbar = NavigationToolbar(charts, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        draw_charts(charts)


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
