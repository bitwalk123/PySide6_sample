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
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableView,
)


class SimpleTableModel(QAbstractTableModel):
    def __init__(self, headers: list, source: list):
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

        a = source[0]
        type_col = (list(map(type, a)))
        if type_col[0] is str:
            print('This is string')
        else:
            print('This is not string')


        table.setModel(SimpleTableModel(headers, source))

        self.setCentralWidget(table)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
