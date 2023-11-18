import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
)


class WorkSheet(QTableWidget):
    def __init__(self, row_max=256, col_max=100):
        super().__init__(row_max, col_max)
        self.setStyleSheet("""
            QTableWidget {
                font-family: monospace;
            }
            QTableCornerButton::section {
                background: #fff;
            }
            QHeaderView {
                font-family: monospace;
                background: #eee;
                color: #666;
            }
        """)
        self.itemChanged.connect(self.cell_updated)

        header_horiz = QHeaderView(Qt.Orientation.Horizontal, parent=self)
        header_horiz.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setHorizontalHeader(header_horiz)

        header_vert = QHeaderView(Qt.Orientation.Vertical, parent=self)
        header_vert.setDefaultAlignment(Qt.AlignmentFlag.AlignRight)
        header_vert.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setVerticalHeader(header_vert)

    def cell_updated(self, item: QTableWidgetItem):
        value = item.text()
        if self.is_num(value):
            item.setText(str(float(value)))
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)

    @staticmethod
    def is_num(str_float: str) -> bool:
        try:
            float(str_float)
        except ValueError:
            return False
        else:
            return True


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WorkSheet test')
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        sheet = WorkSheet()
        self.setCentralWidget(sheet)


def main():
    """Main event loop
    """
    app = QApplication(sys.argv)
    obj = Example()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
