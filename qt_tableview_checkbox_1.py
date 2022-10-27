import sys
from typing import Any

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    QRect,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProxyStyle,
    QStyle,
    QStyledItemDelegate,
    QStyleOption,
    QStyleOptionViewItem,
    QTableView,
    QWidget,
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
    def subElementRect(self, element: QStyle.SubElement, opt: QStyleOption, widget: QWidget = None) -> QRect:
        if element == self.SubElement.SE_ItemViewItemCheckIndicator:
            rect = super().subElementRect(element, opt, widget)
            rect.moveCenter(opt.rect.center())
            return rect
        return super().subElementRect(element, opt, widget)


class CheckBoxDelegate(QStyledItemDelegate):
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
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

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
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

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.getColumnHeader(section)
            elif orientation == Qt.Vertical:
                return self._data.getRowIndex(section)


class Example(QMainWindow):
    #  Sample Data preparation
    num_data = 10000
    names = ['TEST' + str(x * x + 1) for x in range(num_data)]
    units = ['unit' + str(x + 1) for x in range(num_data)]
    list_label_names = [names, units]
    num_check = 10
    col_labels = ['NAME', 'UNIT'] + ['check(%d)' % (x + 1) for x in range(num_check)]

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('TableView')
        self.resize(800, 400)

    def init_ui(self):
        table = QTableView()
        # set table model
        contents = MyContents(self.list_label_names, self.col_labels)
        model = MyTableModel(contents)
        table.setModel(model)
        #
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.setStyleSheet('font-family:monospace; font-size:12pt;')
        table.setStyle(ProxyStyle4CheckBoxCenter())
        table.resizeColumnsToContents()
        table.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        # delegate custom
        delegate = CheckBoxDelegate(table)
        for col in range(len(self.list_label_names), len(self.col_labels)):
            table.setItemDelegateForColumn(col, delegate)
        self.setCentralWidget(table)
        table.setColumnWidth(0, table.sizeHintForColumn(0))
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # WRITE/READ TEST for CheckBox status
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # set default status
        for row in range(contents.getRows()):
            for col in range(contents.getCheckColStart(), contents.getCols()):
                index = model.index(row, col)
                model.setData(index, 2, role=Qt.CheckStateRole)
        # get check status
        for row in range(contents.getRows()):
            for col in range(contents.getCheckColStart(), contents.getCols()):
                index = model.index(row, col)
                value = model.data(index, role=Qt.CheckStateRole)
                # print(row, col, value)

        width = table.fontMetrics().averageCharWidth() * (12 + 2)
        table.horizontalHeader().resizeSection(0, width)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
