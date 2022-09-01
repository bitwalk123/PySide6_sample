#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel, Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView, QHeaderView,
)


class Example(QMainWindow):
    list_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('TableView with CheckBox')

    def init_ui(self):
        """
        initialize UI
        """
        tblview = QTableView()
        tblview.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        model = QStandardItemModel()
        model.itemChanged.connect(self.on_check_item)
        tblview.setModel(model)
        self.setCentralWidget(tblview)

        for row in range(len(self.list_label)):
            list_row = list()
            for column in range(10):
                item = QStandardItem()
                if column == 0:
                    item.setText(self.list_label[row])
                else:
                    item.setCheckable(True)
                    item.setCheckState(Qt.CheckState.Checked)
                    item.setEditable(False)
                list_row.append(item)
            model.appendRow(list_row)

    def on_check_item(self, item: QStandardItem):
        """
        on_check_item
        examine check status
        """
        if item.isCheckable():
            row = item.row()
            col = item.column()
            if item.checkState() == Qt.CheckState.Checked:
                msg = 'checked'
            else:
                msg = 'unchecked'
            print('(%d, %d) -> %s' % (row, col, msg))


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
