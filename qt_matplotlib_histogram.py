#!/usr/bin/env python
# coding: utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
import sys
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns


class Histogram(FigureCanvas):

    def __init__(self, ser: pd.Series):
        fig = Figure()
        super().__init__(fig)
        sns.set_style("whitegrid")
        ax = sns.histplot(data=ser, kde=True, ax=fig.add_subplot(111))
        ax.set(title="Histogram Sample")


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histogram example")
        self.init_ui()

    def init_ui(self):
        # sample data
        ser = pd.Series(np.random.normal(50, 10, 1000), name="X")
        # chart
        canvas: FigureCanvas = Histogram(ser)
        self.setCentralWidget(canvas)
        # navigation for plot
        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navtoolbar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
