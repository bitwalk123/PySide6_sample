# Reference:
# https://www.pythonguis.com/faq/abstract-table-model-question/
import sys

from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import QApplication, QTableView, QMainWindow


class TableModel(QAbstractTableModel):

    def __init__(self, data, checked):
        super(TableModel, self).__init__()
        self._data = data
        self._checked = checked

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)

        if role == Qt.CheckStateRole:
            checked = self._checked[index.row()][index.column()]
            return Qt.Checked if checked else Qt.Unchecked

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            checked = value == Qt.Checked
            self._checked[index.row()][index.column()] = checked
            return True

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = [
            [1, 9, 2],
            [1, 0, -1],
            [3, 5, 2],
            [3, 3, 2],
            [5, 8, 9],
        ]

        checked = [
            [True, True, True],
            [False, False, False],
            [True, False, False],
            [True, False, True],
            [False, True, True],
        ]

        self.model = TableModel(data, checked)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
