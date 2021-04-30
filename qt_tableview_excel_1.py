#!/usr/bin/env python
# coding: utf-8

# Reference:
# https://pc-technique.info/2020/02/207/

import pandas as pd
import sys
from typing import Any, List
from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel
)
from PySide6.QtGui import (
    QPainter,
)
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
        elif type_cell is int or type_cell is float:
            option.displayAlignment = Qt.AlignRight
        else:
            option.displayAlignment = Qt.AlignCenter

        QItemDelegate.paint(self, painter, option, index)


class ExampleTableModel(QAbstractTableModel):
    def __init__(self, headers: List, source: List):
        super().__init__()
        self.headers = headers
        self.source = source

    # QVariant QAbstractItemModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const
    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.DisplayRole:
            return self.source[index.row()][index.column()]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.source)

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
        self.show()

    def initUI(self, df):
        table: QTableView = QTableView()
        table.setWordWrap(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # set table model
        headers = df.columns.values
        source = df.values.tolist()

        # table model
        table.setModel(ExampleTableModel(headers, source))

        # table item delegate
        table.setItemDelegate(ExampleDelegate())

        self.setCentralWidget(table)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
