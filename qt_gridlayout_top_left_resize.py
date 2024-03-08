#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('QWidget {background-color: gray;}')
        self.setWindowTitle('QGridLayoout sample')

        layout = QGridLayout()
        layout.setSpacing(5)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.setLayout(layout)

        y_max = 3
        x_max = 3
        for y in range(y_max):
            for x in range(x_max):
                v = y * x_max + x + 1
                but = QPushButton(str(v))
                but.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        padding: 1em 2em;
                    }
                """)
                layout.addWidget(but, y, x)

        self.setFixedSize(self.sizeHint())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
