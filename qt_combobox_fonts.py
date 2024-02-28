#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QVBoxLayout,
    QWidget, QLabel,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Font list')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.combo = combo = QComboBox(self)
        fdb = QFontDatabase()
        fonts = fdb.families(QFontDatabase.WritingSystem.Any)
        combo.addItems(fonts)
        combo.currentIndexChanged.connect(self.selection_changed)
        layout.addWidget(combo)

        self.label = label = QLabel()
        label.setText('ABCDEabcde12345?#$%&あいうえお')
        layout.addWidget(label)

        self.selection_changed()

    def selection_changed(self):
        self.label.setStyleSheet("""
            QLabel {
                font-family: %s;
                font-size: 36px;
            }
        """ % self.combo.currentText())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
