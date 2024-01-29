#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtConcurrent import QtConcurrent, QFutureVoid
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


# UNDER CONSTRUCTION! #
def aFunction():
    print('プッシュボタンがクリックされました。')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Concurrent')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton('クリックして！')
        btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        btn.clicked.connect(self.button_clicked)
        layout.addWidget(btn)

    def button_clicked(self):
        # future = QtConcurrent.run(aFunction)
        future = QFutureVoid()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
