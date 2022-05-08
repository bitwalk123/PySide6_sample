#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QApplication,
    QListView,
    QWidget,
    QVBoxLayout
)


class Example(QWidget):
    foods = [
        'Cookie dough',  # Must be store-bought
        'Hummus',  # Must be homemade
        'Spaghetti',  # Must be saucy
        'Dal makhani',  # Must be spicy
        'Chocolate whipped cream'  # Must be plentiful
    ]

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QListView')
        self.setMinimumSize(600, 400)
        self.show()

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        lv = QListView()
        lv.clicked.connect(self.on_clicked)
        vbox.addWidget(lv)

        model = QStandardItemModel(lv)
        lv.setModel(model)

        for food in self.foods:
            item = QStandardItem(food)
            item.setCheckable(True)
            model.appendRow(item)

    def on_clicked(self, index: QModelIndex):
        lv: QListView = self.sender()
        model = lv.model()
        print(model.itemData(index)[0])


def main():
    app: QApplication = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()