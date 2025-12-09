#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import QModelIndex, QItemSelectionModel
from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QApplication,
    QListView,
)


class Example(QListView):
    list_letters = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO']

    def __init__(self):
        super().__init__()
        self.clicked.connect(self.on_clicked)

        self.model = model = QStandardItemModel(self)
        self.setModel(model)

        for letters in self.list_letters:
            item = QStandardItem(letters)
            item.setCheckable(True)
            model.appendRow(item)

    def on_clicked(self, midx: QModelIndex):
        item: QStandardItem = self.model.itemFromIndex(midx)
        print(item.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
