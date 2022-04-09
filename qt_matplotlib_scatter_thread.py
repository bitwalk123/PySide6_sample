#!/usr/bin/env python
# coding: utf-8
from PySide6.QtCore import (
    QObject,
    QThread,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProgressDialog,
    QToolBar,
)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import EllipseSelector, RectangleSelector
import seaborn as sns
import sys
import time


class Scatter(FigureCanvas):
    fig = Figure()

    def __init__(self, df):
        super().__init__(self.fig)
        self.init_plot(df)

    def init_plot(self, df):
        # Seaborn Scatter
        ax = sns.scatterplot(data=df, x=df.columns[0], y=df.columns[1], ax=self.fig.add_subplot(111))
        ax.set(title='Scatter Sample')
        # Selector
        plt.RS = RectangleSelector(
            ax, self.select_callback, useblit=True,
            button=[1],  # disable middle & right buttons
            minspanx=5, minspany=5, spancoords='pixels', interactive=True,
            props=dict(facecolor='pink', edgecolor='red', alpha=0.2, fill=True)
        )

    @staticmethod
    def select_callback(eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print(f"({x1: 3.2f}, {y1: 3.2f}) --> ({x2: 3.2f}, {y2: 3.2f})")


class Example(QMainWindow):
    navtoolbar = None

    # for QThread
    progress = None
    thread = None
    worker = None

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setWindowTitle('Scatter + QThread')
        self.init_ui()

    def init_ui(self):
        toolbar = QToolBar()
        toolbar.addAction('plot', self.prep_start)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  DATA PREPARATION
    def prep_start(self):
        # remove widget from central
        self.takeCentralWidget()
        if self.navtoolbar is not None:
            self.removeToolBar(self.navtoolbar)

        # progress bar
        self.progress = QProgressDialog(labelText='Working...', parent=self)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setCancelButton(None)
        self.progress.setRange(0, 0)
        self.progress.setWindowTitle('progress')
        self.progress.show()

        # threading
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # signal handling
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.prepCompleted.connect(self.prep_end)

        # start threading
        self.thread.start()

    def prep_end(self, df):
        # stop QProgressDialog
        self.progress.cancel()

        # plotting chart
        canvas: FigureCanvas = Scatter(df)
        self.setCentralWidget(canvas)

        # navigation toolbar
        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(
            Qt.BottomToolBarArea,
            navtoolbar
        )
        self.navtoolbar = navtoolbar


class Worker(QObject):
    """
    DATA PREPARATION WORKER
    """
    prepCompleted = Signal(pd.DataFrame)
    finished = Signal()

    def __init__(self):
        super().__init__()

    def run(self):
        df = pd.DataFrame(np.random.random(size=(1000, 2)), columns=['X', 'Y'])
        # dummy!! dummy!! dummy!!
        time.sleep(2)

        self.prepCompleted.emit(df)
        self.finished.emit()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
