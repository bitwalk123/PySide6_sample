#!/usr/bin/env python
# coding: utf-8
import platform
import sys
import PySide6
from PySide6 import QtCore
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget, QStyleFactory,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Hello World!')

        print('> Platform', platform.platform())
        print('> Python', sys.version)
        print('> PySide', PySide6.__version__)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel('こんにちは、世界！')
        font = QFont()
        font.setPointSize(24)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


def main():
    app = QApplication(sys.argv)
    print(QStyleFactory.keys())
    app.setStyle('Fusion')
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()