import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QLabel with QPixmap')

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        lab = QLabel()
        pixmap = QPixmap("sample_picture.jpg").scaledToWidth(400)
        lab.setPixmap(pixmap)
        vbox.addWidget(lab)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
