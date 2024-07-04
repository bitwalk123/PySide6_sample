import math
import numpy as np
import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure


class MyTrend(FigureCanvas):
    def __init__(self, count_max: int, legend_label: str):
        self.fig = Figure()
        super().__init__(self.fig)

        self.ax = ax = self.fig.add_subplot(111)
        self.ax.set(title='Sample')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_xlim(0, count_max)
        self.ax.set_ylim(-1, 1)
        self.ax.grid(True)

        self.line, = self.ax.plot([], [], label=legend_label)
        self.ax.legend(loc='best')

    def add_data(self, x: float, y: float):
        x_array = np.append(self.line.get_xdata(), [x])
        y_array = np.append(self.line.get_ydata(), [y])
        self.line.set_xdata(x_array)
        self.line.set_ydata(y_array)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Trend Sample')
        self.resize(600, 400)

        self.count = 0
        self.count_max = 500
        self.chart = chart = MyTrend(
            count_max=self.count_max,
            legend_label='TEST'
        )
        self.setCentralWidget(chart)

        toolbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, toolbar)

        self.timer = timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(10)

    def update_data(self):
        if self.count > self.count_max:
            self.timer.stop()
            print('Completed!')
            return

        x = float(self.count)
        y = math.sin(x * 0.1)

        self.chart.add_data(x, y)
        self.chart.fig.canvas.draw()
        self.count += 1


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
