#!/usr/bin/env python
# coding: utf-8

import csv
import os
import sys
from PySide6.QtCore import QSize
from PySide6.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlTableModel,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QWidget,
)
from PySide6.QtCore import (
    QThread,
    Signal,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setMinimumSize(QSize(600, 0))
        self.setWindowTitle('郵便番号検索')
        self.show()

    def initUI(self):
        area = QScrollArea()
        area.setWidgetResizable(True)
        self.setCentralWidget(area)

        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        area.setWidget(base)

        grid = QGridLayout()
        base.setLayout(grid)

        r = 0
        lab0 = QLabel('DBファイル')
        lab0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab0, r, 0)

        entry0 = QLabel()
        entry0.setStyleSheet("QLabel {background: #fff;}")
        entry0.setFrameShape(QFrame.Panel)
        entry0.setFrameShadow(QFrame.Sunken)
        entry0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(entry0, r, 1, 1, 4)

        but0 = QPushButton('選択')
        but0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but0.clicked.connect(lambda: self.select_database(entry0))
        grid.addWidget(but0, r, 5)

        r += 1
        lab10 = QLabel('検索キー')
        lab10.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab10, r, 0, 2, 1)

        lab11 = QLabel('都道府県')
        lab11.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab11, r, 1)

        lab12 = QLabel('市区町村')
        lab12.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab12, r, 2)

        lab13 = QLabel('住　　所')
        lab13.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(lab13, r, 3)

        lab14 = QLabel('郵便番号')
        lab14.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(lab14, r, 4, 1, 2)

        r += 1
        self.combo1 = QComboBox()
        self.combo1.setMinimumWidth(80)
        self.combo1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.combo1.currentIndexChanged.connect(self.on_address_1_index_changed)
        grid.addWidget(self.combo1, r, 1)

        self.combo2 = QComboBox()
        self.combo2.setMinimumWidth(150)
        self.combo2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.combo2.currentIndexChanged.connect(self.on_address_2_index_changed)
        grid.addWidget(self.combo2, r, 2)

        self.combo3 = QComboBox()
        self.combo3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo3.currentIndexChanged.connect(self.on_address_3_index_changed)
        grid.addWidget(self.combo3, r, 3)

        self.zipcode = QLabel()
        self.zipcode.setStyleSheet("QLabel {background: #fff;}")
        self.zipcode.setFrameShape(QFrame.Panel)
        self.zipcode.setFrameShadow(QFrame.Sunken)
        self.zipcode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(self.zipcode, r, 4, 1, 2)

    def select_database(self, ent: QLineEdit):
        dialog = QFileDialog()
        filters: str = 'SQLite file (*.db *.sqlite *.sqlite3 *db3);; All (*.*)'
        dialog.setNameFilter(filters)

        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            ent.setText(filename)
            self.connect_database(filename)

    def connect_database(self, filename):
        con = QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(filename)
        if not con.open():
            self.show_error_message(con)
            return
        query = QSqlQuery()
        sql = 'SELECT DISTINCT address_1 FROM postal ORDER BY id;'
        if query.exec_(sql):
            self.combo1.clear()
            while query.next():
                self.combo1.addItem(query.value(0))
        # con.close()

    def show_error_message(self, con):
        QMessageBox.critical(
            None,
            'Error!',
            'Database Error: %s' % con.lastError().databaseText(),
        )

    def on_address_1_index_changed(self):
        idx = self.combo1.currentIndex()
        address_1 = self.combo1.itemText(idx)
        query = QSqlQuery()

        sql = 'SELECT DISTINCT address_2 FROM postal WHERE address_1 = ? ORDER BY id;'
        query.prepare(sql)
        query.addBindValue(address_1)
        if query.exec_():
            self.combo2.clear()
            while query.next():
                self.combo2.addItem(query.value(0))

    def on_address_2_index_changed(self):
        idx1 = self.combo1.currentIndex()
        address_1 = self.combo1.itemText(idx1)
        idx2 = self.combo2.currentIndex()
        address_2 = self.combo2.itemText(idx2)

        query = QSqlQuery()
        sql = 'SELECT address_3 FROM postal WHERE address_1 = ? AND address_2 = ? ORDER BY id;'
        query.prepare(sql)
        query.addBindValue(address_1)
        query.addBindValue(address_2)
        if query.exec_():
            self.combo3.clear()
            while query.next():
                self.combo3.addItem(query.value(0))

    def on_address_3_index_changed(self):
        idx1 = self.combo1.currentIndex()
        address_1 = self.combo1.itemText(idx1)
        idx2 = self.combo2.currentIndex()
        address_2 = self.combo2.itemText(idx2)
        idx3 = self.combo3.currentIndex()
        address_3 = self.combo3.itemText(idx3)

        query = QSqlQuery()
        sql = 'SELECT postal_code FROM postal WHERE address_1 = ? AND address_2 = ? AND address_3 = ?;'
        query.prepare(sql)
        query.addBindValue(address_1)
        query.addBindValue(address_2)
        query.addBindValue(address_3)
        if query.exec_():
            while query.next():
                self.zipcode.setText(query.value(0))



def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
