#!/usr/bin/env python
# coding: utf-8
#
# Reference
# https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm
import sys
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Combobox")

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        combo = QComboBox(self)
        combo.addItem("C")
        combo.addItem("C++")
        combo.addItems(["Java", "C#", "Python"])
        combo.currentIndexChanged.connect(self.selection_changed)

        layout.addWidget(combo)

    def selection_changed(self, i):
        sender = self.sender()

        print("Items in the list are :")
        for count in range(sender.count()):
            print(sender.itemText(count))

        print("Current index", i, "selection changed ", sender.currentText())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
