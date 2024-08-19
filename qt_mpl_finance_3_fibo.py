import mplfinance as mpf
import sys
import yfinance as yf

from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector

from PySide6.QtCore import Qt, Signal
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

    def selection(self, eclick: MouseEvent, erelease: MouseEvent):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.signal.rectangleSelected.emit([x1, y1, x2, y2])

    def setTitle(self, title: str):
        self.ax[0].set_title(title)


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
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.chart = chart = MyChart()
        self.setCentralWidget(chart)

        self.navigation = navigation = NavigationToolbar(chart)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navigation)

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

        print(self.chart.ax[0].get_xticklabels())
        print(self.chart.ax[0].get_xticks())
        print(self.chart.ax[0].get_xlim())
        print(self.chart.ax[0].get_major_locator())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
