#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://pc-technique.info/2020/02/207/

import sys
from typing import Any
from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QHeaderView,
)


class SimpleTableModel(QAbstractTableModel):
    def __init__(self, source: list, headers: list):
        QAbstractTableModel.__init__(self)
        self.source = source
        self.headers = headers

    # QVariant QAbstractItemModel::data(const QModelIndex &midx, int role = Qt::DisplayRole) const
    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.DisplayRole:
            return self.source[index.row()][index.column()]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.source)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]
        else:
            return "{}".format(section + 1)


class Example(QMainWindow):
    prefdata = [
        ['茨城県', '310-8555 水戸市笠原町 978-6'],
        ['栃木県', '320-8501 宇都宮市塙田 1-1-20'],
        ['群馬県', '371-8570 前橋市大手町 1-1-1'],
        ['埼玉県', '330-9301 さいたま市浦和区高砂 3-15-1'],
        ['千葉県', '260-8667 千葉市中央区市場町 1-1'],
        ['東京都', '163-8001 新宿区西新宿 2-8-1'],
        ['神奈川県', '231-8588 横浜市中区日本大通 1'],
    ]
    header = ['都道府県', '県庁所在地']

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('TableView')

    def initUI(self):
        table: QTableView = QTableView()
        table.setWordWrap(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # set table model
        table.setModel(SimpleTableModel(self.prefdata, self.header))

        self.setCentralWidget(table)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
