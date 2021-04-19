#!/usr/bin/env python
# coding: utf-8
#
# Reference
# https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm
import sys
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QWidget
)


class Example(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Combobox")
        self.show()

    def initUI(self):
        cb = QComboBox(self)
        cb.addItem("C")
        cb.addItem("C++")
        cb.addItems(["Java", "C#", "Python"])
        cb.currentIndexChanged.connect(self.selectionchange)

    def selectionchange(self, i):
        sender = self.sender()

        print("Items in the list are :")
        for count in range(sender.count()):
            print(sender.itemText(count))

        print("Current index", i, "selection changed ", sender.currentText())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
