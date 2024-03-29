import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QScrollArea,
)


class Example(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setWindowTitle('QScrollArea')

        pixmap = QPixmap("sample_picture.jpg")
        lab = QLabel()
        lab.setPixmap(pixmap)
        self.setWidget(lab)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
