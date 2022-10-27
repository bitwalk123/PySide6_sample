# Reference:
# https://stackoverflow.com/questions/57489001/adding-button-next-to-every-row-of-a-table
import sys
from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QPushButton,
    QTableWidget,
)


class ButtonHeaderView(QHeaderView):
    def __init__(self, parent):
        super().__init__(Qt.Vertical, parent)
        self.m_buttons = []
        self.sectionResized.connect(self.adjustPositions)
        self.sectionCountChanged.connect(self.onSectionCountChanged)
        self.parent().horizontalScrollBar().valueChanged.connect(self.adjustPositions)

    def onSectionCountChanged(self):
        while self.m_buttons:
            button = self.m_buttons.pop()
            button.deleteLater()
        for i in range(self.count()):
            button = QPushButton(self)
            button.setCursor(Qt.ArrowCursor)
            self.m_buttons.append(button)
            self.update_data()
            self.adjustPositions()

    def setModel(self, model):
        super().setModel(model)
        if self.model() is not None:
            self.model().headerDataChanged.connect(self.update_data)

    def update_data(self):
        for i, button in enumerate(self.m_buttons):
            text = self.model().headerData(i, self.orientation(), Qt.DisplayRole)
            button.setText(str(text))

    def updateGeometries(self):
        super().updateGeometries()
        self.adjustPositions()

    def adjustPositions(self):
        w = 0
        for index, button in enumerate(self.m_buttons):
            geom = QRect(
                0,
                self.sectionViewportPosition(index),
                button.height(),
                self.sectionSize(index),
            )
            w = max(w, button.height())
            geom.adjust(0, 2, 0, -2)
            button.setGeometry(geom)
        self.setFixedWidth(w)


class Example(QTableWidget):
    def __init__(self):
        super().__init__(3, 4)
        self.init_ui()
        self.resize(320, 240)
        self.setWindowTitle('Header with button')

    def init_ui(self):
        header = ButtonHeaderView(self)
        self.setVerticalHeader(header)
        self.setHorizontalHeaderLabels(
            ['Field 1', 'Field 2', 'Field 3', 'Field N']
        )
        header_buttons = []
        for i in range(self.columnCount()):
            header_button = '+'
            header_buttons.append(header_button)
        self.setVerticalHeaderLabels(header_buttons)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
