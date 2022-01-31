#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget, QDialogButtonBox, QLabel,
)


class ExampleDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialog')
        dlgbut = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        message = QLabel('ダイアログボックスを表示しました。')
        self.layout.addWidget(message)

        bbox = QDialogButtonBox(dlgbut)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        self.layout.addWidget(bbox)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Dialog Example')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton('ダイアログ表示')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.clicked.connect(self.button_clicked)
        layout.addWidget(btn)

    @staticmethod
    def button_clicked():
        dlg = ExampleDlg()
        if dlg.exec():
            print('OK ボタンがクリックされました。')
        else:
            print('Cancel ボタンがクリックされました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
