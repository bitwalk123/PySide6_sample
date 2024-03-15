import sys

from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QGridLayout')

        layout = QGridLayout()
        self.setLayout(layout)

        y_max = 4
        x_max = 3
        for y in range(y_max):
            for x in range(x_max):
                num = y * x_max + x + 1
                but = QPushButton(str(num))
                layout.addWidget(but, y, x)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
