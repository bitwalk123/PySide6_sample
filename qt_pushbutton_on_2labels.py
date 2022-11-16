#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget, QPushButton, QSizePolicy,
)


class ButtonOn2Labels(QPushButton):
    def __init__(self, titles: list):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        layout_inner = QVBoxLayout()
        self.setLayout(layout_inner)
        lab_upper = QLabel(titles[0])
        lab_lower = QLabel(titles[1])
        layout_inner.addWidget(lab_upper)
        layout_inner.addWidget(lab_lower)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('2 Labels on button')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        but = ButtonOn2Labels(['ABC', 'DEF'])
        layout.addWidget(but)


def main():
    app = QApplication(sys.argv)
    hello = Example()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
