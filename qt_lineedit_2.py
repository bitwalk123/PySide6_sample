#!/usr/bin/env python
# coding: utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('LineEdit 2')

    def init_ui(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        lab = QLabel('Name')
        hbox.addWidget(lab)

        entry = QLineEdit()
        entry.setFixedWidth(200)
        entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        entry.returnPressed.connect(self.entered)
        hbox.addWidget(entry)

    def entered(self):
        entry: QLineEdit = self.sender()
        print('Your name: ' + entry.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
