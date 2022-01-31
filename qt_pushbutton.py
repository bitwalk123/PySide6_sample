#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('PushButton')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton('プッシュボタン')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.clicked.connect(self.button_clicked)
        layout.addWidget(btn)

    def button_clicked(self):
        obj = self.sender()
        print('「%s」がクリックされました。' % obj.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
