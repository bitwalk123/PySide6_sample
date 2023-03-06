#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QPushButton,
    QSizePolicy,
    QStyle,
    QVBoxLayout,
    QWidget,
)


class ExampleDlg(QDialog):
    sbox: QDoubleSpinBox = None

    def __init__(self, value: float = 1):
        super().__init__()
        self.value = value
        self.setWindowTitle('Dialog')
        self.setWindowIcon(
            QIcon(
                self.style().standardIcon(
                    QStyle.StandardPixmap.SP_MessageBoxQuestion
                )
            )
        )

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.sbox = QDoubleSpinBox()
        self.sbox.setValue(self.value)
        self.sbox.setDecimals(3)
        self.sbox.setSingleStep(0.1)
        self.sbox.setAlignment(Qt.AlignRight)
        layout.addWidget(self.sbox)
        dlgbtn = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlgbtn)
        bbox.accepted.connect(self.accept)
        layout.addWidget(bbox)

    def getValue(self):
        return self.sbox.value()

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
        print(dlg.getValue())
        dlg.deleteLater()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
