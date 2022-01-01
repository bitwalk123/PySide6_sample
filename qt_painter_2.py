#!/usr/bin/python
import sys

from PySide6.QtGui import QPainter, QPixmap, QPen, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.setWindowTitle('Line')

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.draw_something(painter)
        painter.end()

    def draw_something(self, painter):
        pen = QPen()
        painter.setPen(pen)
        painter.drawLine(10, 10, 300, 200)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec()


if __name__ == '__main__':
    main()
