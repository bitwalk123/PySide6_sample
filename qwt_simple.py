# Reference:
# https://pypi.org/project/PythonQwt/
import sys

from qtpy import QtWidgets as QW
import qwt
import numpy as np


class Example(qwt.QwtPlot):
    def __init__(self):
        super().__init__()
        self.setTitle("Trigonometric functions")
        self.insertLegend(qwt.QwtLegend(), qwt.QwtPlot.BottomLegend)
        x = np.linspace(-10, 10, 500)
        qwt.QwtPlotCurve.make(x, np.cos(x), "Cosinus", self, linecolor="red", antialiased=True)
        qwt.QwtPlotCurve.make(x, np.sin(x), "Sinus", self, linecolor="blue", antialiased=True)
        self.resize(600, 300)


def main():
    app = QW.QApplication([])
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
