import sys

from PySide6.QtSql import QSqlDatabase, QSqlQuery


def main():
    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName('postal.sqlite')

    if not con.open():
        print('database cannot be opened!')
        sys.exit()

    #sql = 'SELECT * FROM postal WHERE id="%s"' % '124517'
    sql = 'SELECT * FROM postal WHERE id="%s"' % '1245178'
    query = QSqlQuery(sql)
    query.exec()
    if query.isActive():
        print(query.result())
    if query.next():
        print(query.value(0), query.value(1))
    else:
        print('no record found!')
    con.close()

if __name__ == "__main__":
    main()
