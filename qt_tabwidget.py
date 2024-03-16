import sys

from PySide6.QtWidgets import (
    QApplication,
    QTabWidget,
    QWidget,
)


class Example(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QTabWidget')

        self.addTab(QWidget(), 'タブ１')
        self.addTab(QWidget(), 'タブ２')


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
