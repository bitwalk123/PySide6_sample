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
    QWidget, QMessageBox,
)


class ExampleMsgBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("警告")
        self.setText("警告")
        self.setInformativeText("データを保存しますか？")
        self.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
        self.setDefaultButton(QMessageBox.StandardButton.No)


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

    def button_clicked(self):
        msgbox = ExampleMsgBox()
        ret = msgbox.exec()

        if ret == QMessageBox.StandardButton.Yes:
            print('Yes ボタンがクリックされました。')
        elif ret == QMessageBox.StandardButton.No:
            print('No ボタンがクリックされました。')
        else:
            print('不明な状態です。')

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
