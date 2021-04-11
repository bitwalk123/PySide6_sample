#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import QSize
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setMinimumSize(QSize(400, 0))
        self.setWindowTitle("create SQLite database")
        self.show()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        r = 0
        lab0 = QLabel('DB file')
        lab0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid.addWidget(lab0, r, 0)

        entry0 = QLineEdit()
        entry0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid.addWidget(entry0, r, 1)

        but0 = QPushButton('Create')
        but0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        but0.clicked.connect(lambda: self.click_db_create(entry0, but0))
        grid.addWidget(but0, r, 2)

    def click_db_create(self, entry, but):
        name_db = entry.text().strip()
        if len(name_db) == 0:
            return
        con = QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(name_db)
        if not con.open():
            QMessageBox.critical(
                None,
                'Error!',
                'Database Error: %s' % con.lastError().databaseText(),
            )
            return
        else:
            entry.setEnabled(False)
            but.setEnabled(False)

            self.create_db_table()
            print(con.tables())
            con.close()

    def create_db_table(self):
        query = QSqlQuery()
        query.exec_(
            '''
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                job VARCHAR(50),
                email VARCHAR(40) NOT NULL
            )
            '''
        )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
