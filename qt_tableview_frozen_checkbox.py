#!/usr/bin/env python
# coding: utf-8

import sys
from typing import Any

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHeaderView,
    QMainWindow,
    QProxyStyle,
    QStyledItemDelegate,
    QTableView,
)


class MyContents:
    """
    This class defines only column header and contents of label columns.
    It is assumed that label columns are left side of columns and rest of columns are checkbox.
    """
    # The CheckBox status is used by QPersistentModelIndex
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

    def getCheckColStart(self):
        return self._data.getCheckColStart()

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.column() >= self.getCheckColStart():
            # return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            return (
                    Qt.ItemIsEnabled
                    | Qt.ItemIsSelectable
                    | Qt.ItemIsUserCheckable
            )

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        # section is the midx of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.getColumnHeader(section)
            elif orientation == Qt.Vertical:
                return self._data.getRowIndex(section)


class FrozenTableView(QTableView):
    def __init__(self, parent: QTableView = None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().hide()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)


class MyTableView(QTableView):
    def __init__(self, model, parent=None, *args):
        QTableView.__init__(self, parent, *args)
        self.setModel(model)
        self.setMinimumSize(800, 600)
        self.setEditTriggers(QAbstractItemView.SelectedClicked)
        self.setStyleSheet('font-family: monospace;')
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # FrozenTableView
        self.frozenTableView = FrozenTableView(self)
        self.frozenTableView.setModel(model)
        self.frozenTableView.setSelectionModel(QAbstractItemView.selectionModel(self))
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
    names_a = ['A' + str(x + 1).zfill(5) for x in range(num_data)]
    names_b = ['B' + str(x + 1).zfill(5) for x in range(num_data)]
    list_label_names = [names_a, names_b]
    num_check = 20
    col_labels = ['NAME_A', 'NAME_B'] + ['check(%d)' % (x + 1) for x in range(num_check)]

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('FrozenTableView')

    def init_ui(self):
        contents = MyContents(self.list_label_names, self.col_labels)
        model = MyTableModel(contents)
        table = MyTableView(model)
        table.setStyleSheet('font-family: monospace;')
        table.setStyle(ProxyStyle4CheckBoxCenter())
        self.setCentralWidget(table)

        head_horizontal = table.horizontalHeader()
        head_horizontal.setSectionResizeMode(QHeaderView.ResizeToContents)

        # delegate custom
        delegate = CheckBoxDelegate(table)
        for col in range(len(self.list_label_names), len(self.col_labels)):
            table.setItemDelegateForColumn(col, delegate)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # WRITE/READ TEST for CheckBox status
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # set default status
        for row in range(contents.getRows()):
            for col in range(contents.getCheckColStart(), contents.getCols()):
                index = model.index(row, col)
                model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)
        # get check status
        for row in range(contents.getRows()):
            for col in range(contents.getCheckColStart(), contents.getCols()):
                index = model.index(row, col)
                value = model.data(index, role=Qt.CheckStateRole)
                print(row, col, int(value))


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
