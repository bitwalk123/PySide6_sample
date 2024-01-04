import sys

from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QApplication

from qt_db_postgres_dialog import DBInfoDlg
from qt_db_sqlite_pdf_2 import SQLitePDF


class PostgresPDF(SQLitePDF):
    app_title = 'PostgreSQL & PDF test'

    def __init__(self):
        super().__init__()

    @staticmethod
    def create_table():
        query = QSqlQuery()
        sql = """
            CREATE TABLE IF NOT EXISTS pdfrepo (
                name_file character varying(255) UNIQUE,
                content bytea
            );
        """
        if not query.exec(sql):
            print(query.lastError())

    @staticmethod
    def get_connection() -> QSqlDatabase:
        con = QSqlDatabase.addDatabase('QPSQL')
        dict_info = dict()
        dlg = DBInfoDlg(dict_info)
        if dlg.exec():
            con.setHostName(dict_info['host'])
            con.setDatabaseName(dict_info['database'])
            con.setUserName(dict_info['user'])
            con.setPassword(dict_info['password'])
        return con


def main():
    app = QApplication()
    ex = PostgresPDF()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
