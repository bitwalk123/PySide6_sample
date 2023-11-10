# Reference:
# https://www.pythonguis.com/tutorials/pyside6-qtableview-modelviews-numpy-pandas/
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
            return self._data[index.row()][index.column()]

        if role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]

            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self._data[0])


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = [
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9],
        ]

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
