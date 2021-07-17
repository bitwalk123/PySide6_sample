#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://pc-technique.info/2020/02/207/

import pandas as pd
import sys
from typing import Any
from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QItemDelegate,
    QMainWindow,
    QStyleOptionViewItem,
    QTableView,
)


class ExampleDelegate(QItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        type_cell = type(index.data())
        if type_cell is str:
            option.displayAlignment = Qt.AlignLeft
        elif type_cell is int:
            option.displayAlignment = Qt.AlignRight
        elif type_cell is float:
            option.displayAlignment = Qt.AlignRight
        else:
            option.displayAlignment = Qt.AlignCenter

        QItemDelegate.paint(self, painter, option, index)


class ExampleTableModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.headers = df.columns.values
        self.values = df.values.tolist()

    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.DisplayRole:
            return self.values[index.row()][index.column()]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.values)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]
        else:
            return "{}".format(section + 1)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        # sample data
        filename = 'sample.xlsx'
        df = pd.read_excel(
            filename,
            engine='openpyxl',
        )

        self.initUI(df)
        self.setWindowTitle('TableView')
        self.resize(400, 300)

    def initUI(self, df: pd.DataFrame):
        table = QTableView()
        table.setStyleSheet('QHeaderView::section {color:#004; background-color:#ddf}')
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.setWordWrap(False)

        # table model
        table.setModel(ExampleTableModel(df))

        # table item delegate
        table.setItemDelegate(ExampleDelegate())

        self.setCentralWidget(table)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
