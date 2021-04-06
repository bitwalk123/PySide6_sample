#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QWidget,
)

class Example(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)

        self.initUI()
        self.setWindowTitle('左上寄せ')
        self.show()

    def initUI(self):
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)

        grid = QGridLayout()
        base.setLayout(grid)

        row = 0
        lab0 = QLabel('個人情報記入欄')
        grid.addWidget(lab0, row, 0, 1, 2)
        row += 1

        lab1 = QLabel('氏名')
        grid.addWidget(lab1, row, 0)
        ent1 = QLineEdit()
        grid.addWidget(ent1, row, 1)
        row += 1

        lab2 = QLabel('住所')
        grid.addWidget(lab2, row, 0)
        ent2 = QLineEdit()
        grid.addWidget(ent2, row, 1)
        row += 1

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
