# Reference:
# https://stackoverflow.com/questions/48474699/marker-size-alpha-scaling-with-window-size-zoom-in-plot-scatter
import sys
from math import sin
from typing import Any

from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QMainWindow, QApplication


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.fig.canvas.mpl_connect('resize_event', self.onResize)
        super().__init__(self.fig)

        self.fig_w = self.fig.get_figwidth()
        self.fig_h = self.fig.get_figheight()

        self.ax = self.fig.add_subplot(111)
        self.ax.callbacks.connect('xlim_changed', self.onLimitChanged)
        self.ax.callbacks.connect('ylim_changed', self.onLimitChanged)

        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()

        self.fig_factor = None
        self.path = None
        self.sizes = None

    def getZoomFactor(self,
                      limx: tuple[float, float],
                      limy: tuple[float, float]) -> float:
        return min(
            (self.xlim[1] - self.xlim[0]) / (limx[1] - limx[0]),
            (self.ylim[1] - self.ylim[0]) / (limy[1] - limy[0])
        )

    def onLimitChanged(self, ax: Axes):
        lx = ax.get_xlim()
        ly = ax.get_ylim()
        zfactor = self.getZoomFactor(lx, ly)

        try:
            self.path.set_sizes(
                [s * zfactor * self.fig_factor for s in self.sizes]
            )
        except KeyError:
            pass

    def onResize(self, event: Any):
        w = self.fig.get_figwidth()
        h = self.fig.get_figheight()
        self.fig_factor = min(w / self.fig_w, h / self.fig_h)

    def setPath(self, path: PathCollection):
        self.path = path
        self.sizes = self.path.get_sizes()


def draw_chart(chart: MyChart):
    list_x = list()
    list_y = list()
    for i in range(100):
        x = i / 10.
        y = sin(x)
        list_x.append(x)
        list_y.append(y)
    path = chart.ax.scatter(list_x, list_y, s=20, c='blue')
    chart.setPath(path)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        chart = MyChart()
        chart.ax.grid()
        self.setCentralWidget(chart)

        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        draw_chart(chart)


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
