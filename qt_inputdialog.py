#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget, QStyle,
)




class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Dialog Example')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton('Input Dialog')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.clicked.connect(self.button_clicked)
        layout.addWidget(btn)

    def button_clicked(self):
        dlg = QInputDialog()
        dlg.setWindowIcon(
            QIcon(
                self.style().standardIcon(
                    QStyle.StandardPixmap.SP_MessageBoxQuestion
                )
            )
        )
        value, ok = dlg.getDouble(dlg, 'Input value', 'value')
        if ok:
            print(value)
def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
