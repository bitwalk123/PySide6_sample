import sys

from PySide6.QtWidgets import (
    QApplication,
    QTableWidget,
)


class Example(QTableWidget):
    def __init__(self):
        super().__init__(10, 5)
        self.setWindowTitle('QTableWidget')


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
