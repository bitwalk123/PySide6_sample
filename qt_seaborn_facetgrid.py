#!/usr/bin/env python
# coding: utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import seaborn as sns
import warnings

warnings.simplefilter('ignore', FutureWarning)


class MyFacetGrid(FigureCanvas):
    def __init__(self):
        tips = sns.load_dataset('tips')

        g = sns.FacetGrid(tips, col='time')
        g.map_dataframe(sns.scatterplot, x='total_bill', y='tip', hue='sex')
        g.refline(y=tips['tip'].mean())
        g.add_legend()
        super().__init__(g.fig)


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
