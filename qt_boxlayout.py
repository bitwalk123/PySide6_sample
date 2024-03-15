import sys

from PySide6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QPushButton,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QBoxLayout')

        layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.setLayout(layout)

        but_1 = QPushButton('松')
        layout.addWidget(but_1)

        but_2 = QPushButton('竹')
        layout.addWidget(but_2)

        but_3 = QPushButton('梅')
        layout.addWidget(but_3)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
