import sys

import numpy as np
from PySide6.QtCore import QUrl
from PySide6.QtGraphs import (
    QGraphsTheme,
    QScatterSeries,
    QValueAxis,
)
from PySide6.QtQml import QQmlComponent, QQmlEngine
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyle,
)


class MyScatter(QQuickWidget):
    def __init__(self):
        super().__init__()
        self.setResizeMode(
            QQuickWidget.ResizeMode.SizeRootObjectToView
        )
        self.setFixedSize(600, 600)

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
        axis_x.setRange(0, 1)

        self.axis_y = axis_y = QValueAxis()
        axis_y.setRange(0, 1)

        # --------------------------------
        # Scatter series
        # --------------------------------
        self.series = series = QScatterSeries()
        series.setAxisX(axis_x)
        series.setAxisY(axis_y)

        # ----------------------
        # QMLで描画ポイントを修飾
        # ----------------------
        qml = """
        import QtQuick

        Rectangle {
            width: 5
            height: 5
            radius: width / 2
        }
        """
        self.engine = QQmlEngine()
        self.point_delegate = QQmlComponent(self.engine)
        self.point_delegate.setData(qml.encode(), QUrl())

        if self.point_delegate.isError():
            print(self.point_delegate.errors())
        else:
            series.setPointDelegate(self.point_delegate)

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
        self.setWindowTitle("Scatter Chart")

        # --------------------------------
        # QQuickWidget
        # --------------------------------
        scatter = MyScatter()
        self.setCentralWidget(scatter)

        arr_xy = np.random.random(size=(200, 2))
        for x, y in arr_xy:
            scatter.append_data(x, y)


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
