from dataclasses import dataclass, fields
from typing import List

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtWidgets import QApplication, QTableView, QMainWindow


@dataclass
class Item:
    name: str
    value: float
    is_checked: bool


class Model(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.items = []

    def setItems(self, items: List[Item]):
        self.items = items
        self.layoutChanged.emit()

    def setAllItemsSelected(self, selected: bool = True):
        for r in self.items:
            r.is_checked = selected
        self.layoutChanged.emit()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(fields(Item)) - 1

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                value = self.items[index.row()].name
            elif index.column() == 1:
                value = self.items[index.row()].value
            else:
                value = ""
            return value
        elif role == Qt.CheckStateRole and index.column() == 0:
            return Qt.Checked if self.items[index.row()].is_checked else Qt.Unchecked
        else:
            # return QVariant()
            print('not recognised')

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                value = "Name"
            elif section == 1:
                value = "Value"
            else:
                value = ""
            return value
        elif role == Qt.DisplayRole and orientation == Qt.Vertical:
            return section + 1

    def flags(self, index):
        fl = QAbstractTableModel.flags(self, index)
        if index.column() == 0:
            fl |= Qt.ItemIsEditable | Qt.ItemIsUserCheckable
        return fl


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        table = QTableView(self)
        model = Model()
        table.setModel(model)
        self.setCentralWidget(table)

        items = [
            Item("Item 1", 10.0, False),
            Item("Item 2", 20.0, False),
            Item("Item 3", 30.0, True),
            Item("Item 4", 40.0, True),
            Item("Item 5", 50.0, True),
        ]

        model.setItems(items)


if __name__ == "__main__":
    app = QApplication([])
    wnd = MainWindow()
    wnd.show()
    app.exec()
