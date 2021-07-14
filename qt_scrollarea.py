#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import (
    QSize,
)
from PySide6.QtGui import (
    QFont,
    QIcon,
    QPaintDevice,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QWidget,
)


class Example(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.initUI()
        self.setWindowTitle('QScrollArea')

    def initUI(self):
        # base widget to display on the QScrollArea
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)

        # Grid Layout
        grid = QGridLayout()
        base.setLayout(grid)

        # QLineEdit (Entry)
        label_0 = QLabel('Sample for different font/icon sizes')
        label_0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addWidget(label_0, 0, 0, 1, 2)

        # Font Size - Large
        font_size_1: int = 24
        # Font Pixel
        font_pixel_1: int = int(font_size_1 * QPaintDevice.physicalDpiY(self) / 72)
        # Font object
        font_1 = QFont()
        font_1.setPointSize(font_size_1)

        # QLineEdit (1)
        ledit_1 = QLineEdit()
        ledit_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ledit_1.setFont(font_1)
        grid.addWidget(ledit_1, 1, 0)

        # QPushButton (1)
        button_1 = QPushButton()
        button_1.setIcon(QIcon('pencil.png'))
        button_1.setIconSize(QSize(font_pixel_1, font_pixel_1))
        button_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(button_1, 1, 1)

        # Font Size - Small
        font_size_2: int = 9
        # Font Pixel
        font_pixel_2: int = int(font_size_2 * QPaintDevice.physicalDpiY(self) / 72)
        # Font object
        font_2 = QFont()
        font_2.setPointSize(font_size_2)

        # QLineEdit (2)
        ledit_2 = QLineEdit()
        ledit_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ledit_2.setFont(font_2)
        grid.addWidget(ledit_2, 2, 0)

        # QPushButton (2)
        button_2 = QPushButton()
        button_2.setIcon(QIcon('pencil.png'))
        button_2.setIconSize(QSize(font_pixel_1, font_pixel_2))
        button_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(button_2, 2, 1)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
