#!/usr/bin/env python
# coding: utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import seaborn as sns
import warnings

warnings.simplefilter('ignore', FutureWarning)

class MyFacetGrid(FigureCanvas):
    def __init__(self):
        sns.set(font_scale=0.8)
        tips = sns.load_dataset('tips')
        g = sns.FacetGrid(tips, col='time', height=4, aspect=0.8)
        g.map_dataframe(sns.scatterplot, x='total_bill', y='tip', hue='sex')
        g.refline(y=tips['tip'].mean())
        #g.set(xlabel=None)
        g.set(xticklabels=[])
        g.add_legend()
        g.figure.suptitle('TEST', y=1)
        super().__init__(g.figure)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FacetGrid example')
        self.init_ui()

    def init_ui(self):
        # chart
        canvas: FigureCanvas = MyFacetGrid()
        self.setCentralWidget(canvas)
        # navigation for plot
        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.BottomToolBarArea, navtoolbar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
