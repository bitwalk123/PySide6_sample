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
    fig = Figure()

    def __init__(self, df: pd.Series):
        super().__init__(self.fig)
        self.init_chart(df)

    def init_chart(self, df: pd.Series):
        sns.set_style('whitegrid')
        ax = sns.histplot(data=df, kde=True, ax=self.fig.add_subplot(111))
        ax.set(title='Histogram Sample')


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Histogram example')
        self.init_ui()

    def init_ui(self):
        # sample data
        df = pd.Series(np.random.normal(50, 10, 1000), name='length [cm]')
        # chart
        canvas: FigureCanvas = Histogram(df)
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
