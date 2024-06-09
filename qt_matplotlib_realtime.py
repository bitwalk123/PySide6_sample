import datetime
import math
import sys

import pandas as pd
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class RTChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)

        self.ax = ax = self.fig.add_subplot(111)
        ax.set(title='Sample')
        ax.set_ylabel('Y')
        ax.grid(True)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Real Time Sample')
        self.resize(600, 400)

        self.t0 = None
        self.y0 = None
        self.count = 0
        self.canvas = canvas = RTChart()
        self.setCentralWidget(canvas)

        toolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, toolbar)

        self.timer = timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(50)

    def update_data(self):
        if self.count > 1000:
            self.timer.stop()
            print('completed!')
            return

        t1 = datetime.datetime.now()
        y1 = math.sin(t1.timestamp())
        if self.t0 is not None:
            self.canvas.ax.plot(
                [self.t0, t1], [self.y0, y1], color='C1',
                linewidth=1, marker='o', markersize=2)
        self.canvas.fig.canvas.draw()
        self.t0 = t1
        self.y0 = y1
        self.count += 1


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
