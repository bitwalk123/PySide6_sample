# Reference:
# https://stackoverflow.com/questions/62414356/add-a-checkbox-to-text-in-a-qtableview-cell-using-delegate
import sys

from PySide6.QtCore import (
    QAbstractTableModel,
    QPersistentModelIndex,
    Qt,
)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QStyledItemDelegate,
    QTableView,
)


class CustomDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        value = index.data(Qt.CheckStateRole)
        if value is None:
            model = index.model()
            model.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        super().initStyleOption(option, index)
        option.direction = Qt.RightToLeft
        option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter


class MyModel(QAbstractTableModel):
    def __init__(self, materials=[[]], parent=None):
        super().__init__()
        self.materials = materials

        self.check_states = dict()

    def rowCount(self, parent):
        return len(self.materials)

    def columnCount(self, parent):
        return len(self.materials[0])

    def data(self, index, role):

        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.materials[row][column]
            return value

        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            value = self.materials[row][column]
            return value

        if role == Qt.FontRole:
            if index.column() == 0:
                boldfont = QFont()
                boldfont.setBold(True)
                return boldfont

        if role == Qt.CheckStateRole:
            value = self.check_states.get(QPersistentModelIndex(index))
            if value is not None:
                return value

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.materials[row][column] = value
            self.dataChanged.emit(index, index, (role,))
            return True
        if role == Qt.CheckStateRole:
            self.check_states[QPersistentModelIndex(index)] = value
            self.dataChanged.emit(index, index, (role,))
            return True
        return False

    def flags(self, index):
        return (
                Qt.ItemIsEditable
                | Qt.ItemIsEnabled
                | Qt.ItemIsSelectable
                | Qt.ItemIsUserCheckable
        )


class Example(QMainWindow):
    list = ["item_1", "item_2", "item_3"]
    data = [
        [1, "Blocks γ=500 GOST 31359-2007", list[0], 0.18, 0.22],
        [2, "Blocks γ=600 GOST 31359-2008", list[0], 0.25, 0.27],
        [3, "Insulation", list[0], 0.041, 0.042],
        [3, "Insulation", list[0], 0.041, 0.042],
    ]
    model: MyModel = None

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(640, 480)

    def init_ui(self):
        table = QTableView()
        self.setCentralWidget(table)
        self.model = MyModel(self.data)
        table.setModel(self.model)
        table.setSelectionBehavior(table.SelectRows)
        table.setSelectionMode(table.SingleSelection)
        for row in range(len(self.model.materials)):
            index = table.model().index(row, 2)
            table.setIndexWidget(index, self.setting_combobox(index))
        delegate = CustomDelegate(table)
        table.setItemDelegateForColumn(4, delegate)

    def setting_combobox(self, index):
        widget = QComboBox()
        list = self.list
        widget.addItems(list)
        widget.setCurrentIndex(0)
        widget.currentTextChanged.connect(
            lambda value: self.model.setData(index, value)
        )
        return widget


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
