import sys

from PySide6.QtSql import QSqlDatabase, QSqlQuery

dbname = 'test.sqlite'
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName(dbname)

ok = db.open()
if not ok:
    print('Database Error: %s' % db.lastError().databaseText())
    sys.exit(1)

query = QSqlQuery()
query.exec(
    '''
    CREATE TABLE IF NOT EXISTS test (
        id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        description TEXT    NULL
    );
    '''
)

print(db.tables())

db.close()

