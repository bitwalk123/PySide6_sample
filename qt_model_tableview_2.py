import numpy as np

import pandas as pd
import sys
from typing import Union, Any

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableView,
)


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

        if role == Qt.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]

            if isinstance(value, np.int64) or isinstance(value, np.float64):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return self._data.shape[0]

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                # return str(section + 1)
                return str(self._data.index[section])

        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Vertical:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = pd.DataFrame([
            [1, 9.1, 2],
            [1, 0.5, -1],
            [3, 5.1, 2],
            [3, 3.6, 2],
            [5, 8.7, 9],
            [3, 6.2, 2],
            [6, 2.3, 2],
            [3, 6.2, -3],
            [2, 2.4, 5],
            [9, 3.1, 8],
        ],
            columns=['A', 'B', 'C'],
            index=[
                'Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5',
                'Row 6', 'Row 7', 'Row 8', 'Row 9', 'Row 10',

            ]
        )

        self.model = TableModel(data)
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.setCentralWidget(self.table)


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
