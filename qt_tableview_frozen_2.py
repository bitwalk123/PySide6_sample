#!/usr/bin/env python
# coding: utf-8

import sys
from typing import Any

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel, QSortFilterProxyModel, QModelIndex, QPersistentModelIndex,
)
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableView, QAbstractItemView, QProxyStyle, QStyledItemDelegate,
)

class MyContents:
    """
    This class defines only column header and contents of label columns.
    It is assumed that label columns are left side of columns and rest of columns are checkbox.
    """
    # CheckBox status used by QPersistentModelIndex
    check_states = dict()

    def __init__(self, list_labels: list, header_labels: list):
        self.list_labels = list_labels
        self.header_labels = header_labels

    def getCheckColStart(self):
        return len(self.list_labels)

    def getCols(self):
        return len(self.header_labels)

    def getColumnHeader(self, index: int):
        return self.header_labels[index]

    def getData(self, row: int, col: int):
        if col < self.getCheckColStart():
            return self.list_labels[col][row]
        else:
            return None

    def getRowIndex(self, index: int):
        return str(index + 1)

    def getRows(self):
        return len(self.list_labels[0])


class ProxyStyle4CheckBoxCenter(QProxyStyle):
    def subElementRect(self, element, opt, widget=None):
        if element == self.SE_ItemViewItemCheckIndicator:
            rect = super().subElementRect(element, opt, widget)
            rect.moveCenter(opt.rect.center())
            return rect
        return super().subElementRect(element, opt, widget)


class CheckBoxDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index: QModelIndex):
        value = index.data(Qt.CheckStateRole)
        if value is None:
            model = index.model()
            model.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        super().initStyleOption(option, index)


class MyTableModel0(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.colLabels = ['Col%02d' % i for i in range(1, 21)]
        self.dataCached = [['cell%04d,%04d' % (i, j) for i in range(1, 21)]
                           for j in range(1, 51)]

    def rowCount(self, parent):
        return len(self.dataCached)

    def columnCount(self, parent):
        return len(self.colLabels)

    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.dataCached[i][j]

    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.get_value(index)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return value
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return None

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self.dataCached[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.colLabels[section]
            return header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.column() > 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

class MyTableModel(QAbstractTableModel):
    def __init__(self, data: MyContents):
        super(MyTableModel, self).__init__()
        self._data = data
        # self.check_states = dict()

    def rowCount(self, index: QModelIndex = None):
        return self._data.getRows()

    def columnCount(self, index: QModelIndex = None):
        return self._data.getCols()

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data.getData(row, column)
            return value

        if role == Qt.CheckStateRole:
            value = self._data.check_states.get(QPersistentModelIndex(index))
            if value is not None:
                return value

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole = Qt.EditRole):
        if role == Qt.CheckStateRole:
            self._data.check_states[QPersistentModelIndex(index)] = value
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
                return self._data.getColumnHeader(section)
            elif orientation == Qt.Vertical:
                return self._data.getRowIndex(section)


class FrozenTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionModel(QAbstractItemView.selectionModel(parent))
        #
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().hide()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)


class FTableView(QTableView):
    def __init__(self, model, parent=None, *args):
        QTableView.__init__(self, parent, *args)

        # set the table model
        # tm = MyTableModel(self)
        self.setModel(model)

        self.setMinimumSize(800, 600)
        self.setEditTriggers(QAbstractItemView.SelectedClicked)
        self.setStyleSheet('font-family: monospace;')
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.frozenTableView = FrozenTableView(self)
        self.frozenTableView.setModel(model)
        self.frozenTableView.resizeColumnsToContents()
        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        # connect the headers and scrollbars of both tableviews together
        self.verticalScrollBar().valueChanged.connect(
            self.frozenTableView.verticalScrollBar().setValue
        )
        self.frozenTableView.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue
        )

    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()

    def scrollTo(self, index, hint):
        if index.column() > 1:
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(
                self.verticalHeader().width() + self.frameWidth(),
                self.frameWidth(),
                self.columnWidth(0) + self.columnWidth(1),
                self.viewport().height() + self.horizontalHeader().height()
            )
        else:
            self.frozenTableView.setGeometry(
                self.frameWidth(),
                self.frameWidth(),
                self.columnWidth(0) + self.columnWidth(1),
                self.viewport().height() + self.horizontalHeader().height()
            )

    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        x = self.visualRect(current).topLeft().x()
        frozen_width = self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1)
        if cursorAction == self.MoveLeft and current.column() > 1 and x < frozen_width:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
        return current


class Example(QMainWindow):
    #  Sample Data preparation
    num_data = 1000
    names = ['TEST' + str(x + 1).zfill(5) for x in range(num_data)]
    units = ['unit' + str(x + 1).zfill(5) for x in range(num_data)]
    list_label_names = [names, units]
    num_check = 20
    col_labels = ['NAME', 'UNIT'] + ['check(%d)' % (x + 1) for x in range(num_check)]

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('FrozenTableView')

    def init_ui(self):
        #model = MyTableModel(self)
        contents = MyContents(self.list_label_names, self.col_labels)
        model = MyTableModel(contents)
        table = FTableView(model)
        table.setStyle(ProxyStyle4CheckBoxCenter())
        self.setCentralWidget(table)
        # table.resizeColumnsToContents()

        head_horizontal = table.horizontalHeader()
        head_horizontal.setSectionResizeMode(QHeaderView.ResizeToContents)

        # set table model
        # table.setModel(SimpleTableModel(self.prefdata, self.header))
        # delegate custom
        delegate = CheckBoxDelegate(table)
        for col in range(len(self.list_label_names), len(self.col_labels)):
            table.setItemDelegateForColumn(col, delegate)



def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()