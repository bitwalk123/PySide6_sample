# Reference
# https://www.geeksforgeeks.org/pyqtgraph-scatter-plot-graph/
import numpy as np
import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QGridLayout,
    QMainWindow,
    QWidget,
)
import pyqtgraph as pg


def generate_scatter_random(plot):
    # number of points
    n = 1000
    # creating a scatter plot item
    # of size = 10
    # using brush to enlarge the of white color with transparency is 50%
    scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(128, 128, 255, 120))
    # generating random position
    pos = np.random.normal(size=(2, n), scale=1e-5)
    print(pos)
    # creating spots using the random position
    spots = [{'pos': pos[:, i], 'data': 1} for i in range(n)] + [{'pos': [0, 0], 'data': 1}]
    print(spots)
    # adding points to the scatter plot
    scatter.addPoints(spots)
    # add item to plot window
    # adding scatter plot item to the plot window
    plot.addItem(scatter)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtGraph")
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()
        self.show()

    def init_ui(self):
        base = QWidget()
        self.setCentralWidget(base)

        layout = QGridLayout()
        base.setLayout(layout)

        label = QLabel("Geeksforgeeks Scatter Plot")
        label.setWordWrap(True)
        label.setMinimumWidth(130)
        layout.addWidget(label, 1, 0)

        plot = pg.plot()
        generate_scatter_random(plot)
        layout.addWidget(plot, 0, 1, 3, 1)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
