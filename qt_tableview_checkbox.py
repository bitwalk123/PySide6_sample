# Reference:
# https://stackoverflow.com/questions/17748546/pyqt-column-of-checkboxes-in-a-qtableview
import sys

from PySide6.QtCore import (
    Qt,
    QEvent,
    QModelIndex,
)
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import (
    QApplication,
    QItemDelegate,
    QMainWindow,
    QTableView,
)


class CheckBoxDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column to which it's applied.
    """

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        self.drawCheck(painter, option, option.rect, Qt.Unchecked if int(index.data()) == 0 else Qt.Checked)

    def editorEvent(self, event, model, option, index):
        """
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        """
        if not int(index.flags() & Qt.ItemIsEditable) > 0:
            return False

        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True

        return False

    def setModelData(self, editor, model, index):
        """
        The user wanted to change the old state in the opposite.
        """
        model.setData(index, 1 if int(index.data()) == 0 else 0, Qt.EditRole)


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle('TableView, CheckBoxDelegate')

    def init_ui(self):
        """
        initialize UI
        """
        tblview = QTableView()
        self.setCentralWidget(tblview)
        model = QStandardItemModel(4, 3)
        tblview.setModel(model)

        delegate = CheckBoxDelegate(None)
        tblview.setItemDelegateForColumn(1, delegate)
        for row in range(4):
            for column in range(3):
                index = model.index(row, column, QModelIndex())
                model.setData(index, 1)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
