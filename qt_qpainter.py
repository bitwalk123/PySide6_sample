# Reference:
# https://www.pythonguis.com/tutorials/pyside6-bitmap-graphics/
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def draw_something(self):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen()
        pen.setWidth(100)
        pen.setColor(QtGui.QColor('lightblue'))
        painter.setPen(pen)
        painter.drawPoint(100, 100)
        painter.end()
        self.label.setPixmap(canvas)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
