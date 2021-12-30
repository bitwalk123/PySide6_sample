#!/usr/bin/python
# Reference:
# https://zetcode.com/gui/pysidetutorial/drawing/
"""
ZetCode PySide tutorial

In the example, we draw randomly 1000 red points
on the window.

author: Jan Bodnar
website: zetcode.com
"""

import sys, random

from PySide6.QtGui import (
    QPainter,
    QPen,
    QColor,
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
)


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.resize(300, 300)
        self.setWindowTitle('Points')

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawPoints(painter)
        painter.end()

    def drawPoints(self, painter):
        pen = QPen()
        pen.setWidth(5)
        pen.setColor(QColor('red'))
        painter.setPen(pen)
        size = self.size()

        for i in range(1000):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            painter.drawPoint(x, y)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
