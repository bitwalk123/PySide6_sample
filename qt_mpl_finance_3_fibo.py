import mplfinance as mpf
import numpy as np
import pandas as pd
import sys
import yfinance as yf

from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QMainWindow,
    QToolBar,
)


class CandleChartSignal(QObject):
    rectangleSelected = Signal(list)


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.signal = CandleChartSignal()
        self.fig.subplots_adjust(
            left=0.12,
            right=0.87,
            top=0.9,
            bottom=0.05,
        )
        self.ax = dict()

    def clearAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.cla()

    def clearRectangle(self):
        self.rs.clear()

    def initAxes(self, ax, n: int):
        if n > 1:
            gs = self.fig.add_gridspec(
                n, 1,
                wspace=0.0, hspace=0.0,
                height_ratios=[3 if i == 0 else 1 for i in range(n)]
            )
            for i, axis in enumerate(gs.subplots(sharex='col')):
                ax[i] = axis
                ax[i].grid()
        else:
            ax[0] = self.fig.add_subplot()
            ax[0].grid()

        # Selector
        self.init_rectangle_selector(ax[0])

    def initChart(self, n: int):
        self.removeAxes()
        self.initAxes(self.ax, n)

    def init_rectangle_selector(self, ax):
        self.rs = RectangleSelector(
            ax,
            self.selection,
            useblit=True,
            button=MouseButton.LEFT,  # disable middle & right buttons
            minspanx=5,
            minspany=5,
            spancoords='pixels',
            interactive=True,
            props=dict(
                facecolor='#eef',
                edgecolor='blue',
                alpha=0.2,
                fill=True,
            )
        )

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()
        self.ax = dict()

    def selection(self, eclick: MouseEvent, erelease: MouseEvent):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.signal.rectangleSelected.emit([x1, y1, x2, y2])

    def setTitle(self, title: str):
        self.ax[0].set_title(title)


def fibonacci_retracement(
        chart: MyChart,
        df: pd.DataFrame,
        positions: list
):
    x_1, y_1, x_2, y_2 = positions
    idx_max = len(df)

    idx_1 = round(x_1)
    idx_2 = int(np.ceil(x_2))
    if idx_1 < 0:
        idx_1 = 0
    if idx_max < x_2:
        idx_2 = idx_max

    df_part = df.iloc[idx_1:idx_2]
    if len(df_part) < 2:
        return
    # print(df_part)

    list_ts = list()
    y_low = min(df_part['Low'])
    df_low = df_part[df_part['Low'] == y_low]
    for ts in df_low.index:
        list_ts.append(ts)

    y_high = max(df_part['High'])
    df_high = df_part[df_part['High'] == y_high]
    for ts in df_high.index:
        list_ts.append(ts)

    y_delta = y_high - y_low

    ts_left = min(list_ts)
    idx_left = list(df.index).index(ts_left)
    if df.iloc[idx_left]['Low'] == y_low:
        lev_start = y_high
        lev1 = lev_start - 0.236 * y_delta
        lev2 = lev_start - 0.382 * y_delta
        lev3 = lev_start - 0.618 * y_delta
        lev_end = y_low
    elif df.iloc[idx_left]['High'] == y_high:
        lev_start = y_low
        lev1 = lev_start + 0.236 * y_delta
        lev2 = lev_start + 0.382 * y_delta
        lev3 = lev_start + 0.618 * y_delta
        lev_end = y_high
    else:
        print('Unknown error!')
        return

    x_left, x_right = chart.ax[0].get_xbound()
    x_start = (idx_left - x_left) / (x_right - x_left)

    fibo_level = [lev_start, lev1, lev2, lev3, lev_end]
    fibo_ratio = [0.0, 0.236, 0.382, 0.618, 1.0]
    right_xdelta = 8
    y_gap = y_delta * 0.002
    fibo_color = '#00a'

    for y, v in zip(fibo_level, fibo_ratio):
        chart.ax[0].axhline(
            y,
            xmin=x_start,
            linestyle='dashed',
            linewidth=0.75,
            color=fibo_color,
        )
        chart.ax[0].text(
            idx_left,
            y + y_gap,
            '%3.1f%%' % (v * 100),
            color=fibo_color,
            fontsize=9,
        )
        chart.ax[0].text(
            x_right - right_xdelta,
            y + y_gap,
            '%.1f' % y,
            color=fibo_color,
            fontsize=9,
        )

    chart.refreshDraw()


class MyToolBar(QToolBar):
    volumeCheckChanged = Signal()

    def __init__(self):
        super().__init__()
        self.chk_volume = chk_volume = QCheckBox('Volume')
        chk_volume.checkStateChanged.connect(self.volume_check_changed)
        self.addWidget(chk_volume)

        self.chk_fibo = chk_fibo = QCheckBox('Fibonacci retracement')
        self.addWidget(chk_fibo)

    def isFibonacciSelected(self) -> bool:
        return self.chk_fibo.isChecked()

    def isVolumeSelected(self) -> bool:
        return self.chk_volume.isChecked()

    def volume_check_changed(self):
        self.volumeCheckChanged.emit()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dynamic charts')

        self.toolbar = toolbar = MyToolBar()
        toolbar.volumeCheckChanged.connect(self.draw)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.chart = chart = MyChart()
        chart.signal.rectangleSelected.connect(
            self.rectangle_selected
        )
        self.setCentralWidget(chart)

        self.navigation = navigation = NavigationToolbar(chart)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navigation)

        self.symbol = symbol = '^N225'
        ticker = yf.Ticker(symbol)
        self.df = ticker.history(period='3mo')
        self.draw()

    def draw(self):
        if self.toolbar.isVolumeSelected():
            n = 2
        else:
            n = 1

        self.chart.initChart(n)
        param = dict(
            data=self.df,
            style='yahoo',
            type='candle',
            datetime_format='%m/%d',
            xrotation=0,
            ax=self.chart.ax[0],
        )
        y_low = min(self.df['Low']) * 0.99
        y_high = max(self.df['High']) * 1.01
        param['ylim'] = (y_low, y_high)

        if self.toolbar.isVolumeSelected():
            param['volume'] = self.chart.ax[1]

        mpf.plot(**param)
        self.chart.setTitle(self.symbol)
        self.chart.refreshDraw()
        self.navigation.update()

    def rectangle_selected(self, positions: list):
        if self.toolbar.isFibonacciSelected():
            fibonacci_retracement(self.chart, self.df, positions)
        self.chart.clearRectangle()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
