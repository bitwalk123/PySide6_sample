# Reference:
# https://stackoverflow.com/questions/49107722/pyqtgraph-strings-in-xticks-overlapping-each-other
import pyqtgraph as pg
from PySide6 import QtWidgets, QtGui, QtCore
import numpy as np
import sys

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class HistogramWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        pg.PlotWidget.__init__(self, parent=parent)
        self.values = np.array([])
        self.bins = np.linspace(0, 1, 10)
        self.brush = (0, 0, 255, 255)
        self.curve = None
        self.names = []
        self.getPlotItem().buttonsHidden = True
        self.setStyleSheet("border: 1px solid gray")

    def set_bins(self, bins, names):
        self.bins = bins
        self.names = names
        self.xdict = dict(enumerate(names))
        self.getPlotItem().axes['bottom']['item'].setTicks([self.xdict.items()])

    def add_values(self, values):
        self.values = np.append(self.values, values)
        self.values = self.values.flatten()
        self.y, self.x = np.histogram(self.values, bins=self.bins)
        if self.curve is not None:
            self.removeItem(self.curve)
        self.curve = pg.PlotCurveItem(list(self.xdict.keys()), self.y, stepMode=True, fillLevel=0, brush=self.brush)
        self.addItem(self.curve)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = HistogramWidget()
    w.set_bins(np.linspace(-3, 8, 40), ['bin_' + str(i[0]) for i in enumerate(np.linspace(-3, 8, 40))])
    w.add_values(np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)]))
    w.show()
    sys.exit(app.exec())
