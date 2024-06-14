import sys
from math import sin
from typing import Any

from PySide6.QtCore import Qt
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure

from PySide6.QtWidgets import QMainWindow, QApplication


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.fig.canvas.mpl_connect('resize_event', self.onResize)
        super().__init__(self.fig)

        self.fig_w = self.fig.get_figwidth()
        self.fig_h = self.fig.get_figheight()

        self.ax = self.fig.add_subplot(111)
        self.ax.callbacks.connect('xlim_changed', self.limChanged)
        self.ax.callbacks.connect('ylim_changed', self.limChanged)

        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()

        self.fig_factor = None
        self.path = None
        self.psizes = None

    def getZoomFactor(self, lx: tuple[float, float], ly: tuple[float, float]) -> float:
        return min(
            (self.xlim[1] - self.xlim[0]) / (lx[1] - lx[0]),
            (self.ylim[1] - self.ylim[0]) / (ly[1] - ly[0])
        )

    def limChanged(self, ax: Axes):
        lx = ax.get_xlim()
        ly = ax.get_ylim()
        zfactor = self.getZoomFactor(lx, ly)

        try:
            self.path.set_sizes(
                [s * zfactor * self.fig_factor for s in self.psizes]
            )
        except KeyError:
            pass

    def onResize(self, event: Any):
        w = self.fig.get_figwidth()
        h = self.fig.get_figheight()
        self.fig_factor = min(w / self.fig_w, h / self.fig_h)

    def setPath(self, path: PathCollection):
        self.path = path
        self.psizes = path.get_sizes()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        chart = MyChart()
        chart.ax.grid()
        self.setCentralWidget(chart)

        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        self.draw_chart(chart)

    def draw_chart(self, chart: MyChart):
        list_x = list()
        list_y = list()
        for i in range(100):
            x = i / 10.
            y = sin(x)
            list_x.append(x)
            list_y.append(y)
        path = chart.ax.scatter(list_x, list_y, s=20, c='blue')
        chart.setPath(path)


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
