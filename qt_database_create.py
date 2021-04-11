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
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QWidget,
)
from PySide6.QtCore import (
    QThread,
    Signal,
)


class Example(QMainWindow):
    file_csv = 'KEN_ALL_UTF8.csv'

    def __init__(self):
        super().__init__()

        self.initUI()
        self.setMinimumSize(QSize(600, 0))
        self.setWindowTitle("郵便番号データベース作成")
        self.show()

    def initUI(self):
        base = QWidget()
        self.setCentralWidget(base)

        grid = QGridLayout()
        base.setLayout(grid)

        r = 0
        lab0 = QLabel('データベースファイル')
        lab0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab0, r, 0)

        entry0 = QLineEdit()
        entry0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(entry0, r, 1)

        but0 = QPushButton('作成')
        but0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but0.clicked.connect(lambda: self.click_db_create(entry0, but0))
        grid.addWidget(but0, r, 2)

        status_label = QLabel('進捗')
        status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.progbar = QProgressBar()
        self.progbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        status_bar = QStatusBar()
        status_bar.addWidget(status_label, 1)
        status_bar.addWidget(self.progbar, 2)

        self.setStatusBar(status_bar)

    def click_db_create(self, entry, but):
        name_db = entry.text().strip()
        if len(name_db) == 0:
            return
        else:
            entry.setEnabled(False)
            but.setEnabled(False)
            self.task_start(name_db)

    def task_gen(self, name_db):
        self.task = TaskThread(name_db, self.file_csv)
        self.task.progressChanged.connect(self.progbar.setValue)

    def task_start(self, name_db):
        self.task_gen(name_db)
        self.task.start()
        self.task.progressCompleted.connect(self.task_end)

    def task_end(self):
        pass


class TaskThread(QThread):
    progressChanged = Signal(int)
    progressCompleted = Signal()

    name_db = None
    file_csv = None

    def __init__(self, name_db, file_csv):
        super().__init__()
        self.name_db = name_db
        self.file_csv = file_csv

    def run(self):
        if os.path.exists(self.name_db):
            os.remove(self.name_db)

        con = QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(self.name_db)

        if not con.open():
            self.show_error_message(con)
            self.progressChanged.emit(100)
            self.progressCompleted.emit()
            self.exit(0)
            return

        self.create_db_table()
        data = self.read_csv_file(self.file_csv)
        self.append_record(con, data)
        self.complete(con)

    def complete(self, con):
        con.close()
        self.progressCompleted.emit()
        self.exit(0)

    def create_db_table(self):
        query = QSqlQuery()
        query.exec_(
            '''
            CREATE TABLE postal (
                id INTEGER PRIMARY KEY,
                postal_code TEXT,
                address_1 TEXT,
                address_2 TEXT,
                address_3 TEXT
            )
            '''
        )

    def read_csv_file(self, filename):
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data

    def append_record(self, con, data):
        dbModel = QSqlTableModel()
        dbModel.setTable('postal')

        count = 0
        ndata = len(data)
        for line in data:
            count += 1
            progress = int(count / ndata * 100)
            self.progressChanged.emit(progress)

            record = dbModel.record()
            record.setValue(1, line[0])
            record.setValue(2, line[1])
            record.setValue(3, line[2])
            record.setValue(4, line[3])
            if not dbModel.insertRecord(-1, record):
                self.show_error_message(con)
                self.progressChanged.emit(100)
                break

    def show_error_message(self, con):
        QMessageBox.critical(
            None,
            'Error!',
            'Database Error: %s' % con.lastError().databaseText(),
        )



def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
