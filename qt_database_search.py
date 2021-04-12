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
        self.setMinimumSize(QSize(600, 400))
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
        lab0 = QLabel('データベースファイル')
        lab0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab0, r, 0)

        entry0 = QLabel()
        entry0.setStyleSheet("QLabel {background: #fff;}")
        entry0.setFrameShape(QFrame.Panel)
        entry0.setFrameShadow(QFrame.Sunken)
        entry0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(entry0, r, 1)

        but0 = QPushButton('選択')
        but0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but0.clicked.connect(lambda: self.click_db_create(entry0))
        grid.addWidget(but0, r, 2)

    def click_db_create(self, ent: QLineEdit):
        dialog = QFileDialog()
        filters: str = 'SQLite file (*.db *.sqlite *.sqlite3 *db3);; All (*.*)'
        dialog.setNameFilter(filters)

        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            ent.setText(filename)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
