import sys

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)
from PySide6.QtWidgets import QApplication, QTableView, QMainWindow


class TableModel(QAbstractTableModel):
    def __init__(self, mlist=None, checkableColumns=None):
        super(TableModel, self).__init__()
        self._items = [] if mlist == None else mlist
        self._header = ['aaaa', 'bbb', 'ccc']

        if checkableColumns is None:
            checkableColumns = []
        elif isinstance(checkableColumns, int):
            checkableColumns = [checkableColumns]

        self.checkableColumns = set(checkableColumns)

    def setColumnCheckable(self, column, checkable=True):
        if checkable:
            self.checkableColumns.add(column)
        else:
            self.checkableColumns.discard(column)
        self.dataChanged.emit(
            self.index(0, column), self.index(self.rowCount() - 1, column))

    def rowCount(self, parent=QModelIndex):
        return len(self._items)

    def columnCount(self, parent=QModelIndex):
        return len(self._header)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if (role == Qt.CheckStateRole and
                index.column() in self.checkableColumns):
            value = self._items[index.row()][index.column()]
            return Qt.Checked if value else Qt.Unchecked
        elif (index.column() not in self.checkableColumns and
              role in (Qt.DisplayRole, Qt.EditRole)):
            return self._items[index.row()][index.column()]
        else:
            return None

    def setData(self, index, value, role=Qt.EditRole):
        if (role == Qt.CheckStateRole and index.column() in self.checkableColumns):
            self._items[index.row()][index.column()] = bool(value)
            self.dataChanged.emit(index, index, (role,))
            return True

        if value is not None and role == Qt.EditRole:
            self._items[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, (role,))
            return True

        return False

    def flags(self, index):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() in self.checkableColumns:
            # only this flag is required
            flags |= Qt.ItemIsUserCheckable
        return flags


class Example(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle('TableView')

    def init_ui(self):
        table = QTableView()
        self.setCentralWidget(table)
        table.setWordWrap(False)
        table.setAlternatingRowColors(True)
        # set table model
        model = TableModel(mlist=[['A', False, 'C']], checkableColumns=[1])
        table.setModel(model)
        # delegate custom
        # delegate = CustomDelegate(table)
        # for col in range(2, 4):
        #    table.setItemDelegateForColumn(col, delegate)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
