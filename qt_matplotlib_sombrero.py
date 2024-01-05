#!/usr/bin/env python
# coding: utf-8
import matplotlib as mpl
import numpy as np
import sys

from PySide6.QtGui import QPixmap, QIcon
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure

from PySide6.QtCore import (
    QBuffer,
    QByteArray,
    QIODevice,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStyle,
    QToolBar,
    QToolButton,
    QWidget,
)


class ImageViewer(QWidget):
    def __init__(self, byte_array: QByteArray):
        super().__init__()
        self.setWindowTitle('Matplotlib image viewer')
        lab = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        lab.setPixmap(pixmap)
        self.setFixedSize(
            pixmap.size().width(),
            pixmap.size().height()
        )


class Sombrero(FigureCanvas):
    def __init__(self):
        self.fig = fig = Figure()
        super().__init__(fig)

        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)

        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(
            X, Y, Z,
            rstride=1, cstride=1,
            cmap=mpl.colormaps['coolwarm'],
            linewidth=0, antialiased=False
        )


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win = None
        self.init_ui()
        self.setWindowTitle('QBuffer test')

    def init_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        but_apply = QToolButton()
        ico_apply = self.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogApplyButton
        )
        but_apply.setIcon(QIcon(ico_apply))
        but_apply.clicked.connect(self.on_apply_button)
        toolbar.addWidget(but_apply)

        canvas = Sombrero()
        self.setCentralWidget(canvas)

        navtoolbar = NavigationToolbar(canvas, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navtoolbar)

    def on_apply_button(self):
        canvas: QWidget | Sombrero = self.centralWidget()
        fig = canvas.fig
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        fig.savefig(buffer)
        byte_array = buffer.data()

        self.win = ImageViewer(byte_array)
        self.win.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
