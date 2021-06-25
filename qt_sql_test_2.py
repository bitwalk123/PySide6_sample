# Reference
# https://realpython.com/python-pyqt-database/
import sys

from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('QSqlQuery Example')
        self.resize(450, 250)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(4)
        self.view.setHorizontalHeaderLabels(['ID', 'Name', 'Job', 'Email'])
        query = QSqlQuery('SELECT id, name, job, email FROM contacts')
        while query.next():
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            self.view.setItem(rows, 2, QTableWidgetItem(query.value(2)))
            self.view.setItem(rows, 3, QTableWidgetItem(query.value(3)))
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)


# noinspection PyTypeChecker
def createConnection():
    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName('contacts.sqlite')
    if not con.open():
        QMessageBox.critical(
            None,
            'QTableView Example - Error!',
            'Database Error: %s' % con.lastError().databaseText(),
        )
        return False
    return True


def main():
    app = QApplication(sys.argv)
    if not createConnection():
        sys.exit(1)
    win = Example()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
