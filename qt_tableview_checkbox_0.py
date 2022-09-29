# Reference:
# https://stackoverflow.com/questions/62414356/add-a-checkbox-to-text-in-a-qtableview-cell-using-delegate
import sys

import pandas as pd
from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QPersistentModelIndex, QModelIndex,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyledItemDelegate,
    QTableView, QProxyStyle, QHeaderView,
)


class CustomDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index: QModelIndex):
        value = index.data(Qt.CheckStateRole)
        if value is None:
            model = index.model()
            model.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        super().initStyleOption(option, index)


class MyTableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super(MyTableModel, self).__init__()
        self._data = data
        self.check_states = dict()

    def rowCount(self, index: QModelIndex):
        return self._data.shape[0]

    def columnCount(self, index: QModelIndex):
        return self._data.shape[1]

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data.iloc[row, column]
            return value

        if role == Qt.CheckStateRole:
            value = self.check_states.get(QPersistentModelIndex(index))
            if value is not None:
                return value

    def setData(self, index: QModelIndex, value, role: Qt.ItemDataRole = Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self._data.iloc[row, column] = value
            self.dataChanged.emit(index, index, (role,))
            return True

        if role == Qt.CheckStateRole:
            self.check_states[QPersistentModelIndex(index)] = value
            self.dataChanged.emit(index, index, (role,))
            return True

        return False

    def flags(self, index: QModelIndex):
        return (
                Qt.ItemIsEnabled
                | Qt.ItemIsSelectable
                | Qt.ItemIsUserCheckable
        )

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            elif orientation == Qt.Vertical:
                return str(self._data.index[section] + 1)


class ProxyStyleCheckBoxCenter(QProxyStyle):
    def subElementRect(self, element, opt, widget=None):
        if element == self.SE_ItemViewItemCheckIndicator:
            rect = super().subElementRect(element, opt, widget)
            rect.moveCenter(opt.rect.center())
            return rect
        return super().subElementRect(element, opt, widget)


class Example(QMainWindow):
    sample = pd.DataFrame({
        'name': ['A', 'B', 'C', 'D'],
        'check(1)': None,
        'check(2)': None,
        'check(3)': None
    })

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle('TableView')

    def init_ui(self):
        table = QTableView()
        self.setCentralWidget(table)
        table.setStyle(ProxyStyleCheckBoxCenter())
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        # delegate custom
        delegate = CustomDelegate(table)
        for col in range(1, self.sample.shape[1]):
            table.setItemDelegateForColumn(col, delegate)
        # set table model
        model = MyTableModel(self.sample)
        table.setModel(model)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
