#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ExampleDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialog')

        layout = QVBoxLayout()
        self.setLayout(layout)

        message = QLabel('ダイアログボックスを表示しました。')
        layout.addWidget(message)

        dlgbtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        bbox = QDialogButtonBox(dlgbtn)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        layout.addWidget(bbox)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialog Example')

        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton('ダイアログ表示')
        btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
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
