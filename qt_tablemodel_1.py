# Reference
# https://forum.qt.io/topic/136125/qabstracttablemodel-checkbox-not-showing-checked/7
import pandas as pd

from PySide6.QtCore import Qt, QAbstractTableModel


class pandasModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super(pandasModel, self).__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def data(self, index, role):
        row = index.row()
        column = index.column()
        value = self._data.iloc[row, column]
        if role == Qt.DisplayRole:
            if value == True:
                return "Yes"
            elif value == False:
                return "No"
            else:
                return str(value)
        if role == Qt.CheckStateRole and column == 2:
            if value == True:
                return Qt.Checked
            else:
                return Qt.Unchecked

    def setData(self, index, value, role):
        row = index.row()
        column = index.column()
        if role == Qt.CheckStateRole and column == 2:
            if value == Qt.Checked:
                self._data.iloc[row, column] = True
                self.dataChanged.emit(index, index)
            elif value == Qt.Unchecked:
                self._data.iloc[row, column] = False
                self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 2:
            flags |= Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return flags

    def headerData(self, section, orientation, role):
        # section is the midx of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            elif orientation == Qt.Vertical:
                return str(self._data.index[section])
