from typing import Union, Any

import pandas as pd
import sys

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
)


class TableModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self._data = df

    def columnCount(self, index: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return self._data.shape[1]

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        # section is the midx of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def rowCount(self, index: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return self._data.shape[0]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        table = QTableView()
        self.setCentralWidget(table)

        data = pd.DataFrame([
            [1, 9, 2],
            [1, 0, -1],
            [3, 5, 2],
            [3, 3, 2],
            [5, 8, 9],
        ], columns=['A', 'B', 'C'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

        model = TableModel(data)
        table.setModel(model)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
