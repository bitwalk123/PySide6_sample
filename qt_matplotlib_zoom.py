import sys
from math import sin

import matplotlib.pyplot as plt
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from PySide6.QtWidgets import QMainWindow, QApplication


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.fig_width = self.fig.get_figwidth()
        self.fig_height = self.fig.get_figheight()
        self.fig.canvas.mpl_connect('resize_event', self.on_resize)
        self.ax = self.fig.add_subplot(111)
        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()
        self.ax.callbacks.connect('xlim_changed', self.lim_change)
        self.ax.callbacks.connect('ylim_changed', self.lim_change)

        super().__init__(self.fig)

        self.fig_factor = None
        self.path = None
        self.point_sizes = None

    def clearAxes(self):
        self.ax.cla()

    def lim_change(self, ax):
        lx = ax.get_xlim()
        ly = ax.get_ylim()

        factor = min(
            (self.xlim[1] - self.xlim[0]) / (lx[1] - lx[0]),
            (self.ylim[1] - self.ylim[0]) / (ly[1] - ly[0])
        )

        try:
            self.path.set_sizes([s * factor * self.fig_factor for s in self.point_sizes])
        except KeyError:
            pass

    def on_resize(self, event):
        w = self.fig.get_figwidth()
        h = self.fig.get_figheight()
        self.fig_factor = min(w / self.fig_width, h / self.fig_height)
        self.lim_change(self.ax)

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()

    def set_path(self, p):
        self.path = p
        self.point_sizes = p.get_sizes()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        chart = MyChart()
        list_x = list()
        list_y = list()
        for i in range(100):
            x = i / 10.
            y = sin(x)
            list_x.append(x)
            list_y.append(y)
        p = chart.ax.scatter(list_x, list_y, s=20, c='blue')
        chart.ax.grid()
        chart.set_path(p)
        self.setCentralWidget(chart)

        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
