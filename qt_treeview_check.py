#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication,
    QFileSystemModel,
    QMainWindow,
    QTreeView,
)


class Example(QMainWindow):
    pref = {
        '北海道': '札幌市', '青森県': '青森市', '岩手県': '盛岡市', '宮城県': '仙台市', '秋田県': '秋田市',
        '山形県': '山形市', '福島県': '福島市', '茨城県': '水戸市', '栃木県': '宇都宮市', '群馬県': '前橋市',
        '埼玉県': 'さいたま市', '千葉県': '千葉市', '東京都': '新宿区', '神奈川県': '横浜市', '新潟県': '新潟市',
        '富山県': '富山市', '石川県': '金沢市', '福井県': '福井市', '山梨県': '甲府市', '長野県': '長野市',
        '岐阜県': '岐阜市', '静岡県': '静岡市', '愛知県': '名古屋市', '三重県': '津市', '滋賀県': '大津市',
        '京都府': '京都市', '大阪府': '大阪市', '兵庫県': '神戸市', '奈良県': '奈良市', '和歌山県': '和歌山市',
        '鳥取県': '鳥取市', '島根県': '松江市', '岡山県': '岡山市', '広島県': '広島市', '山口県': '山口市',
        '徳島県': '徳島市', '香川県': '高松市', '愛媛県': '松山市', '高知県': '高知市', '福岡県': '福岡市',
        '佐賀県': '佐賀市', '長崎県': '長崎市', '熊本県': '熊本市', '大分県': '大分市', '宮崎県': '宮崎市',
        '鹿児島県': '鹿児島市', '沖縄県': '那覇市',
    }

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('TreeView with check')

    def init_ui(self):
        tree = QTreeView()
        self.setCentralWidget(tree)

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['都道府県', '庁所在地'])
        for name_pref in self.pref.keys():
            item_pref = QStandardItem(name_pref)
            item_pref.setCheckable(True)
            item_pref.setEditable(False)

            item_capital = QStandardItem(self.pref[name_pref])
            item_capital.setCheckable(True)
            item_capital.setEditable(False)

            model.appendRow([item_pref, item_capital])

        tree.setModel(model)
        model.itemChanged.connect(self.on_check_item)

    def on_check_item(self, item: QStandardItem):
        row = item.row()
        name = item.text()

        if item.checkState() == Qt.CheckState.Checked:
            msg = 'checked'
            is_checked = True
        else:
            msg = 'unchecked'
            is_checked = False

        print(row, name, msg)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
