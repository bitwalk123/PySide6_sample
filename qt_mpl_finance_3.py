import matplotlib.pyplot as plt
import mplfinance as mpf
import sys
import yfinance as yf

from PySide6.QtCore import Signal
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QMainWindow,
    QToolBar,
)


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.fig.subplots_adjust(
            left=0.12,
            right=0.87,
            top=0.9,
            bottom=0.05,
        )
        self.ax = dict()

    def initAxes(self, ax, n: int):
        grid = plt.GridSpec(n + 2, 1, wspace=0.0, hspace=0.0)
        # Main
        ax[0] = self.fig.add_subplot(grid[0:3, 0])
        ax[0].grid()
        if n > 1:
            ax[0].tick_params(labelbottom=False)
        # Sub
        for i in range(1, n):
            ax[i] = self.fig.add_subplot(grid[i + 2, 0], sharex=ax[0])
            ax[i].grid()
            if i < n - 1:
                ax[i].tick_params(labelbottom=False)

    def initChart(self, n: int):
        self.removeAxes()
        self.initAxes(self.ax, n)

    def clearAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()
        self.ax = dict()

    def setTitle(self, title: str):
        self.ax[0].set_title(title)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)


class MyToolBar(QToolBar):
    volumeCheckChanged = Signal()

    def __init__(self):
        super().__init__()
        self.chk_volume = chk_volume = QCheckBox('Volume')
        chk_volume.checkStateChanged.connect(self.volume_check_changed)
        self.addWidget(chk_volume)

    def isVolumeChecked(self) -> bool:
        return self.chk_volume.isChecked()

    def volume_check_changed(self):
        self.volumeCheckChanged.emit()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dynamic charts')

        self.toolbar = toolbar = MyToolBar()
        toolbar.volumeCheckChanged.connect(self.draw)
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.chart = chart = MyChart()
        self.setCentralWidget(chart)

        self.navigation = navigation = ChartNavigation(chart)
        self.addToolBar(QtCore.Qt.ToolBarArea.BottomToolBarArea, navigation)

        self.symbol = symbol = '^N225'
        ticker = yf.Ticker(symbol)
        self.df = ticker.history(period='3mo')
        self.draw()

    def draw(self):
        if self.toolbar.isVolumeChecked():
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
        if self.toolbar.isVolumeChecked():
            param['volume'] = self.chart.ax[1]

        mpf.plot(**param)
        self.chart.setTitle(self.symbol)
        self.chart.refreshDraw()
        self.navigation.update()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
