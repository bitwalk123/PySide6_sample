from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QLineEdit,
    QToolBar,
    QWidget,
)
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DockNavigator(QDockWidget):
    def __init__(self, canvas):
        super().__init__()
        self.setTitleBarWidget(QWidget(None))
        navtoolbar = NavigationToolbar(canvas, self)
        self.setWidget(navtoolbar)


class MyToolBar(QToolBar):
    tickerEntered = Signal(str)

    def __init__(self):
        super().__init__()
        ent_ticker = QLineEdit()
        ent_ticker.setFixedWidth(100)
        ent_ticker.returnPressed.connect(self.on_ticker_entered)
        self.addWidget(ent_ticker)

    def on_ticker_entered(self):
        entry: QLineEdit = self.sender()
        ticker = entry.text()
        self.tickerEntered.emit(ticker)


class StockChart(FigureCanvas):
    plt.rcParams['font.family'] = plt.rcParams['font.monospace'][0]
    plt.rcParams['font.size'] = 9

    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)

        grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.0)
        self.ax = self.fig.add_subplot(grid[0:2, 0])
        self.ax2 = self.fig.add_subplot(grid[2, 0], sharex=self.ax)

    def clearAxes(self):
        self.ax.cla()
        self.ax2.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()
