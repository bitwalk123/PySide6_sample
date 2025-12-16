#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import QModelIndex, Signal
from PySide6.QtGui import (
    QAction,
    QMouseEvent,
    QStandardItem,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QApplication,
    QListView,
    QMainWindow,
    QStyle,
    QStyleOptionViewItem,
    QToolBar,
)


class ListView(QListView):
    clickedOutsideCheckBox = Signal(QModelIndex)

    def mousePressEvent(self, event: QMouseEvent):
        mindex = self.indexAt(event.position().toPoint())
        if not mindex.isValid():
            return super().mousePressEvent(event)

        rect = self.visualRect(mindex)
        option = QStyleOptionViewItem()
        option.initFrom(self)
        option.rect = rect
        option.state = QStyle.StateFlag.State_Enabled
        option.features = QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator

        # チェックボックスの矩形を取得
        style = self.style()
        check_rect = style.subElementRect(
            QStyle.SubElement.SE_ItemViewItemCheckIndicator,
            option,
            self
        )

        # チェックボックスがクリックされたか判定
        if check_rect.contains(event.position().toPoint()):
            return super().mousePressEvent(event)
        else:
            self.clickedOutsideCheckBox.emit(mindex)
            return super().mousePressEvent(event)


class Example(QMainWindow):
    list_letters = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO']

    def __init__(self):
        super().__init__()

        toolbar = QToolBar()
        action_test = QAction(toolbar, text="TEST")
        action_test.triggered.connect(self.on_current_item)
        toolbar.addAction(action_test)

        self.addToolBar(toolbar)

        self.lv = lv = ListView()
        lv.clickedOutsideCheckBox.connect(self.on_clicked)
        self.setCentralWidget(lv)

        self.model = model = QStandardItemModel(lv)
        lv.setModel(model)

        for letters in self.list_letters:
            item = QStandardItem(letters)
            item.setCheckable(True)
            model.appendRow(item)

    def on_clicked(self, midx: QModelIndex):
        item: QStandardItem = self.model.itemFromIndex(midx)
        print(item.text())

    def on_current_item(self):
        idx = self.lv.currentIndex().row()
        print("現在のインデックス", idx)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
