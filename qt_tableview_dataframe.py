#!/usr/bin/env python
# coding: utf-8
# Reference
# https://doc.qt.io/qtforpython/examples/example_external__pandas.html
import pandas as pd

from PySide6.QtWidgets import QTableView, QApplication, QMainWindow
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
import sys


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        df = pd.read_csv('iris.csv')
        self.init_ui(df)
        self.setWindowTitle('QTableView')
        self.resize(800, 500)

    def init_ui(self, df:pd.DataFrame):
        view = QTableView()
        self.setCentralWidget(view)

        view.horizontalHeader().setStretchLastSection(True)
        view.setAlternatingRowColors(True)
        view.setSelectionBehavior(QTableView.SelectRows)

        model = PandasModel(df)
        view.setModel(model)


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()