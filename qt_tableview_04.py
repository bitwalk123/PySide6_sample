#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://pc-technique.info/2020/03/228/

import sys
import dataclasses

from typing import Any, List
from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel
)

# For Sample
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTableView
)


# custom Data class
@dataclasses.dataclass
class CustomData:
    name: str
    age: int
    country: str

    def toList(self) -> list:
        return [self.name, self.age, self.country]

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return ["NAME", "AGE", "COUNTRY"]

    def validateAndSetName(self, name) -> bool:
        if str(name) != "":  # Non-empty string is OK.
            self.name = str(name)
            return True
        return False

    def validateAndSetAge(self, age) -> bool:
        try:
            val_int = int(age)
            if val_int >= 0:  # int, and greater than 0 or equal 0 is OK.
                self.age = val_int
                return True
        except ValueError:
            pass  # Non-integer value is invalid.
        return False

    def validateAndSetCountry(self, country) -> bool:
        if str(country) in ["USA", "Japan", "US", "Russia", "Canada"]:  # Only 5 countries
            self.country = str(country)
            return True
        return False


class SimpleTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_data: List[CustomData] = [
            CustomData(name="Taro", age=24, country="Japan"),
            CustomData(name="Jiro", age=20, country="Japan"),
            CustomData(name="David", age=32, country="USA"),
            CustomData(name="Wattson", age=15, country="US")
        ]  # prepare table's source data (TEST)

    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.DisplayRole:
            # The QTableView wants a cell text of 'index'
            # BE CAREFUL about IndexError (rowCount() and/or columnCount() are incorrect.)
            return self.custom_data[index.row()].toList()[index.column()]

    def rowCount(self, parent=QModelIndex()) -> int:
        # = data count
        return len(self.custom_data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(CustomData.toHeaderList())

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # The QTableView wants a header text

            if orientation == Qt.Horizontal:
                # BE CAREFUL about IndexError
                return CustomData.toHeaderList()[section]

            return ""  # There is no vertical header

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        # Returning true means the value was accepted.
        if index.isValid() and role == Qt.EditRole:
            if index.column() == 0:
                return self.custom_data[index.row()].validateAndSetName(value)
            elif index.column() == 1:
                return self.custom_data[index.row()].validateAndSetAge(value)
            elif index.column() == 2:
                return self.custom_data[index.row()].validateAndSetCountry(value)

        return False  # Not Accepted.

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.NoItemFlags


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setWindowTitle('Test of QTableView')
        self.show()

    def initUI(self):
        self.root_widget: QWidget = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout()
        self.table: QTableView = QTableView()
        self.layout.addWidget(self.table)
        self.root_widget.setLayout(self.layout)
        self.table.setModel(SimpleTableModel())  # create model and set
        self.setCentralWidget(self.root_widget)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
