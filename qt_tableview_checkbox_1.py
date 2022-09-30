# Reference:
# https://stackoverflow.com/questions/62414356/add-a-checkbox-to-text-in-a-qtableview-cell-using-delegate
import sys

import pandas as pd
from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
)
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QProxyStyle,
    QStyledItemDelegate,
    QTableView,
)


class ProxyStyleCheckBoxCenter(QProxyStyle):
    def subElementRect(self, element, opt, widget=None):
        if element == self.SE_ItemViewItemCheckIndicator:
            rect = super().subElementRect(element, opt, widget)
            rect.moveCenter(opt.rect.center())
            return rect
        return super().subElementRect(element, opt, widget)


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

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data.iloc[row, column]
            return value

        if role == Qt.CheckStateRole:
            value = self.check_states.get(QPersistentModelIndex(index))
            if value is not None:
                return value

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            self.check_states[QPersistentModelIndex(index)] = value
            self.dataChanged.emit(index, index, (role,))
            return True

        return False

    def flags(self, index):
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


class Example(QMainWindow):
    sample = pd.DataFrame({
        'NAME': ['TEST' + str(x + 1).zfill(5) for x in range(10000)],
        'check(1)': None,
        'check(2)': None,
        'check(3)': None,
        'check(4)': None,
        'check(5)': None,
        'check(6)': None,
        'check(7)': None,
        'check(8)': None,
        'check(9)': None,
    })

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle('TableView')
        self.resize(800, 400)

    def init_ui(self):
        table = QTableView()
        table.setStyle(ProxyStyleCheckBoxCenter())
        table.setWordWrap(False)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.setCentralWidget(table)
        # delegate custom
        delegate = CustomDelegate(table)
        for col in range(1, self.sample.shape[1]):
            table.setItemDelegateForColumn(col, delegate)
        # set table model
        model = MyTableModel(self.sample)
        table.setModel(model)
        # set default status
        for row in range(self.sample.shape[0]):
            for col in range(1, self.sample.shape[1]):
                index = model.index(row, col)
                model.setData(index, 2, role=Qt.CheckStateRole)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
