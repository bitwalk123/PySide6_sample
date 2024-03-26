import sys
from typing import Union

import pandas as pd
from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from pandas import Index, DatetimeIndex
from scipy.interpolate import BSpline, make_interp_spline


class MyCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def clearAxes(self):
        self.axes.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Trend test')

        canvas = MyCanvas()
        self.setCentralWidget(canvas)

        dock = QDockWidget()
        dock.setTitleBarWidget(QWidget(None))
        dock.setWidget(NavigationToolbar(canvas))
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dock)

        csvfile = 'temperature.csv'
        df = pd.read_csv(csvfile, index_col=0, parse_dates=True)
        self.draw_plot(df)

    def draw_plot(self, df: pd.DataFrame):
        canvas: Union[QObject, MyCanvas] = self.centralWidget()
        fig = canvas.fig
        ax = canvas.axes

        ax.plot(
            df,
            linewidth=1,
            color='blue',
            marker='o',
            markersize=6,
            markeredgecolor='darkblue',
            markeredgewidth=1,
            markerfacecolor='cyan',
            label='original data'
        )

        ts: Index = df.index.map(pd.Timestamp.timestamp)
        bspl: BSpline = make_interp_spline(ts, df['気温'], k=2)
        dbspl = bspl.derivative(nu=1)

        x1: DatetimeIndex = pd.date_range(min(df.index), max(df.index), freq='1min')
        ts1: Index = x1.map(pd.Timestamp.timestamp)
        y1 = bspl(ts1)
        dy1 = dbspl(ts1)

        ax.plot(
            x1, y1,
            linewidth=1,
            color='red',
            label='spline curve'
        )

        ax2 = ax.twinx()
        ax2.plot(
            x1, dy1,
            linewidth=1,
            linestyle='dashed',
            color='violet',
            label='derivative'
        )

        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

        ax.set_ylabel('Temperature')
        ax.grid()
        ax2.set_ylabel('Derivative')

        fig.legend(loc='outside lower center')
        fig.subplots_adjust(top=0.99, left=0.1, bottom=0.3, right=0.8)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
