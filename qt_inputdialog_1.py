#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ExampleDlg(QDialog):
    def __init__(self, value: float = 1):
        super().__init__()
        self.setWindowTitle('Dialog')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.sbox = QDoubleSpinBox()
        self.sbox.setValue(value)
        self.sbox.setDecimals(3)
        self.sbox.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.sbox)

        dlgbtn = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlgbtn)
        bbox.accepted.connect(self.accept)
        self.layout.addWidget(bbox)


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
        dlg = ExampleDlg()
        dlg.exec()
        print(dlg.sbox.value())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
