import sys

from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableView,
)


class Example(QMainWindow):
    pref_data: list = [
        ['茨城県', '310-8555 水戸市笠原町 978-6'],
        ['栃木県', '320-8501 宇都宮市塙田 1-1-20'],
        ['群馬県', '371-8570 前橋市大手町 1-1-1'],
        ['埼玉県', '330-9301 さいたま市浦和区高砂 3-15-1'],
        ['千葉県', '260-8667 千葉市中央区市場町 1-1'],
        ['東京都', '163-8001 新宿区西新宿 2-8-1'],
        ['神奈川県', '231-8588 横浜市中区日本大通 1'],
        ['新潟県', '950-8570 新潟県新潟市中央区新光町4-1'],
        ['富山県', '930-8501 富山県富山市新総曲輪1-7'],
        ['石川県', '920-8580 石川県金沢市鞍月1-1'],
    ]
    header: list = ['都道府県', '県庁所在地']

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('TableView')

    def init_ui(self):
        # table
        table = QTableView()
        self.setCentralWidget(table)
        table.setWordWrap(False)
        table.setCornerButtonEnabled(True)
        table.setStyleSheet(
            'QTableCornerButton::section {border:1px outset #ccc;}'
        )
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        table.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        # model for table
        model = QStandardItemModel()
        table.setModel(model)
        model.setHorizontalHeaderLabels(self.header)
        for info_pref in self.pref_data:
            list_row = [QStandardItem(info) for info in info_pref]
            model.appendRow(list_row)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
