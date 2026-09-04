import sys

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGraphs import (
    QGraphsTheme,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyle,
)


class MyTrend(QQuickWidget):
    def __init__(self):
        super().__init__()
        self.setResizeMode(
            QQuickWidget.ResizeMode.SizeRootObjectToView
        )
        self.setFixedSize(600, 300)

        # --------------------------------
        # Theme
        # --------------------------------
        self.theme = theme = QGraphsTheme()
        grid = theme.grid()
        grid.setMainWidth(1.0)
        grid.setSubWidth(0.5)
        theme.setGrid(grid)

        # --------------------------------
        # Axes
        # --------------------------------
        self.axis_x = axis_x = QValueAxis()
        axis_x.setRange(0, 100)

        self.axis_y = axis_y = QValueAxis()
        axis_y.setRange(0, 1)
        axis_y.setTitleText("Value")

        # --------------------------------
        # Line series
        # --------------------------------
        self.series = series = QLineSeries()
        series.setAxisX(axis_x)
        series.setAxisY(axis_y)

        # 線の太さと色
        series.setWidth(1.0)
        series.setColor(Qt.GlobalColor.green)

        # GraphsView に渡すプロパティ
        self.setInitialProperties({
            "theme": theme,
            "axisX": axis_x,
            "axisY": axis_y,
            "seriesList": [series],
        })

        # QtGraphs の GraphsView をロード
        self.loadFromModule(
            "QtGraphs",
            "GraphsView",
        )

    def append_data(self, x: float, y: float):
        self.series.append(x, y)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMenuButton
        )
        self.setWindowIcon(icon)
        self.setWindowTitle("Trend Chart")

        # --------------------------------
        # QQuickWidget
        # --------------------------------
        trend = MyTrend()
        self.setCentralWidget(trend)

        arr_y = np.random.random(100)
        for i, y in enumerate(arr_y):
            trend.append_data(i, y)


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
