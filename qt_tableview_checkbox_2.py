# Reference:
# https://www.pythonguis.com/faq/abstract-table-model-question/

import sys

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel
from PySide6.QtGui import QColor, QPixmap, QPainter, QPen, QIcon
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox, QAbstractItemDelegate, QWidget, QTableView, QAbstractItemView, QVBoxLayout, QApplication


class AssetDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if isinstance(self.parent(), QAbstractItemView):
            self.parent().openPersistentEditor(index)
        QStyledItemDelegate.paint(self, painter, option, index)

    def createEditor(self, parent, option, index):
        combobox = QComboBox(parent)
        combobox.addItems(index.data(AssetModel.ItemsRole))
        combobox.currentIndexChanged.connect(self.onCurrentIndexChanged)
        return combobox

    def onCurrentIndexChanged(self, ix):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QAbstractItemDelegate.NoHint)

    def setEditorData(self, editor, index):
        ix = index.data(AssetModel.ActiveRole)
        editor.setCurrentIndex(ix)

    def setModelData(self, editor, model, index):
        ix = editor.currentIndex()
        model.setData(index, ix, AssetModel.ActiveRole)


class Asset(object):
    def __init__(self, name, items=[], active=0):
        self.active = active
        self.name = name
        self.items = items

    @property
    def status(self):
        return self.active == len(self.items) - 1


class AssetModel(QAbstractTableModel):
    attr = ["Name", "Options", "Extra"]
    ItemsRole = Qt.UserRole + 1
    ActiveRole = Qt.UserRole + 2

    def __init__(self, *args, **kwargs):
        QAbstractTableModel.__init__(self, *args, **kwargs)
        self._items = []

    def flags(self, index):
        fl = QAbstractTableModel.flags(self, index)
        if index.column() == 1:
            fl |= Qt.ItemIsEditable
        return fl

    def clear(self):
        self.beginResetModel()
        self._items = []
        self.endResetModel()

    def rowCount(self, index=QModelIndex()):
        return len(self._items)

    def columnCount(self, index=QModelIndex()):
        return len(self.attr)

    def addItem(self, sbsFileObject):
        self.beginInsertRows(QModelIndex(),
                             self.rowCount(), self.rowCount())
        self._items.append(sbsFileObject)
        self.endInsertRows()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return AssetModel.attr[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if 0 <= index.row() < self.rowCount():
            item = self._items[index.row()]
            col = index.column()
            if role == AssetModel.ItemsRole:
                return getattr(item, 'items')

            if role == AssetModel.ActiveRole:
                return getattr(item, 'active')

            if 0 <= col < self.columnCount():
                if role == Qt.DisplayRole:
                    if col == 0:
                        return getattr(item, 'name', '')
                    if col == 1:
                        return getattr(item, 'items')[getattr(item, 'active')]
                elif role == Qt.DecorationRole:
                    if col == 0:
                        status = getattr(item, 'status')
                        col = QColor(Qt.red) if status else QColor(Qt.green)
                        px = QPixmap(120, 120)
                        px.fill(Qt.transparent)
                        painter = QPainter(px)
                        painter.setRenderHint(QPainter.Antialiasing)
                        px_size = px.rect().adjusted(12, 12, -12, -12)
                        painter.setBrush(col)
                        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                        painter.drawEllipse(px_size)
                        painter.end()

                        return QIcon(px)

    def setData(self, index, value, role=Qt.EditRole):
        if 0 <= index.row() < self.rowCount():
            item = self._items[index.row()]
            if role == AssetModel.ActiveRole:
                setattr(item, 'active', value)
                return True
        return QAbstractTableModel.setData(self, index, value, role)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(400, 300)

        # controls
        asset_model = QSortFilterProxyModel()
        asset_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        asset_model.setSourceModel(AssetModel())

        self.ui_assets = QTableView()
        self.ui_assets.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui_assets.setModel(asset_model)
        self.ui_assets.verticalHeader().hide()
        self.ui_assets.setItemDelegateForColumn(1, AssetDelegate(self.ui_assets))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.ui_assets)
        self.setLayout(main_layout)

        self.unit_test()

    def unit_test(self):
        assets = [
            Asset('Dev1', ['v01', 'v02', 'v03'], 0),
            Asset('Dev2', ['v10', 'v11', 'v13'], 1),
            Asset('Dev3', ['v11', 'v22', 'v53'], 2),
            Asset('Dev4', ['v13', 'v21', 'v23'], 0)
        ]

        self.ui_assets.model().sourceModel().clear()
        for i, obj in enumerate(assets):
            self.ui_assets.model().sourceModel().addItem(obj)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
