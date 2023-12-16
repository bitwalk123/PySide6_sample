import pandas as pd
import sys

from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyle,
    QToolBar,
    QToolButton,
    QTableView, QHeaderView,
)

from qt_model_dataframe import PandasModel
from qt_sql_postgres_dialog import DBInfoDlg


def db_get_col_info(info: dict, cols: list, query: QSqlQuery):
    sql = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '%s';
        """ % info['table']
    query.exec(sql)
    while query.next():
        cols.append(query.value(0))


def db_get_all_contents(info: dict, vals: dict, cols: list, query: QSqlQuery):
    for key in cols:
        vals[key] = list()
    sql = 'SELECT * FROM %s;' % info['table']
    query.exec(sql)
    while query.next():
        for i, key in enumerate(cols):
            vals[key].append(query.value(i))


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = None
        self.init_ui()
        self.setWindowTitle('DB Connection test')
        self.resize(800, 600)

    def init_ui(self):
        toolbar = QToolBar()
        self.add_button_to_toolbar(toolbar)
        self.addToolBar(toolbar)

        self.view = QTableView()
        self.view.setAlternatingRowColors(True)
        self.setCentralWidget(self.view)

        header = self.view.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

    def add_button_to_toolbar(self, toolbar: QToolBar):
        but_connect = QToolButton()
        but_connect.setText('Connect')
        but_connect.setToolTip('Connect with PostgreSQL')
        pixmap_connect = QStyle.StandardPixmap.SP_CommandLink
        icon_connect = self.style().standardIcon(pixmap_connect)
        but_connect.setIcon(icon_connect)
        but_connect.clicked.connect(self.button_clicked)
        toolbar.addWidget(but_connect)

    def button_clicked(self):
        obj: QToolButton = self.sender()
        if obj.text() == 'Connect':
            self.show_db_info_dlg()

    def show_db_info_dlg(self):
        dict_info = dict()
        dlg = DBInfoDlg(dict_info)
        if dlg.exec():
            self.db_connection(dict_info)

    def db_connection(self, dict_info: dict):
        con = QSqlDatabase.addDatabase('QPSQL')
        con.setHostName(dict_info['host'])
        con.setDatabaseName(dict_info['database'])
        con.setUserName(dict_info['user'])
        con.setPassword(dict_info['password'])
        if con.open():
            print('connected!')
            list_col = list()
            query = QSqlQuery()
            db_get_col_info(dict_info, list_col, query)
            dict_val = dict()
            db_get_all_contents(dict_info, dict_val, list_col, query)
            df = pd.DataFrame(dict_val)
            con.close()

            model = PandasModel(df)
            self.view.setModel(model)

        else:
            print('NOT connected!')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
