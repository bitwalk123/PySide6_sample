#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel, QSortFilterProxyModel,
)
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableView, QAbstractItemView,
)


class MyTableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.colLabels = ['Col%02d' % i for i in range(1, 21)]
        self.dataCached = [['cell%02d,%02d' % (i, j) for i in range(1, 21)]
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


class FrozenTableView(QTableView):
    def __init__(self, parent=None, *args):
        QTableView.__init__(self, parent, *args)

        self.setMinimumSize(800, 600)

        # set the table model
        tm = MyTableModel(self)

        # set the proxy model
        pm = QSortFilterProxyModel(self)
        pm.setSourceModel(tm)

        self.setModel(pm)

        self.frozenTableView = QTableView(self)
        self.frozenTableView.setModel(pm)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.setStyleSheet('''border: none; background-color: #CCC''')
        self.frozenTableView.setSelectionModel(QAbstractItemView.selectionModel(self))
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.viewport().stackUnder(self.frozenTableView)

        self.setEditTriggers(QAbstractItemView.SelectedClicked)

        # hide grid
        self.setShowGrid(False)

        self.setStyleSheet('font: 10pt "Courier New"')

        hh = self.horizontalHeader()
        hh.setDefaultAlignment(Qt.AlignCenter)
        hh.setStretchLastSection(True)

        ncol = tm.columnCount(self)
        for col in range(ncol):
            if col == 0:
                self.horizontalHeader().resizeSection(col, 60)
                self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
            elif col == 1:
                self.horizontalHeader().resizeSection(col, 150)
                self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
            else:
                self.horizontalHeader().resizeSection(col, 100)
                self.frozenTableView.setColumnHidden(col, True)

        self.frozenTableView.setSortingEnabled(True)
        self.frozenTableView.sortByColumn(0, Qt.AscendingOrder)

        self.setAlternatingRowColors(True)

        vh = self.verticalHeader()
        vh.setDefaultSectionSize(25)
        vh.setDefaultAlignment(Qt.AlignCenter)
        vh.setVisible(True)
        self.frozenTableView.verticalHeader().setDefaultSectionSize(vh.defaultSectionSize())

        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # connect the headers and scrollbars of both tableviews together
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex == 0 or logicalIndex == 1:
            self.frozenTableView.setColumnWidth(logicalIndex, newSize)
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()

    def scrollTo(self, index, hint):
        if index.column() > 1:
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(), self.columnWidth(0) + self.columnWidth(1),
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                                             self.frameWidth(), self.columnWidth(0) + self.columnWidth(1),
                                             self.viewport().height() + self.horizontalHeader().height())

    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        x = self.visualRect(current).topLeft().x()
        frozen_width = self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1)
        if cursorAction == self.MoveLeft and current.column() > 1 and x < frozen_width:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
        return current


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('FrozenTableView')

    def init_ui(self):
        table = FrozenTableView()
        head_horizontal = table.horizontalHeader()
        head_horizontal.setSectionResizeMode(QHeaderView.ResizeToContents)

        # set table model
        # table.setModel(SimpleTableModel(self.prefdata, self.header))

        self.setCentralWidget(table)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
