import sys
from PySide6.QtSql import QSqlDatabase, QSqlQuery

# Create the connection
con = QSqlDatabase.addDatabase('QSQLITE')
con.setDatabaseName('contacts.sqlite')

# Open the connection
if not con.open():
    print('Database Error: %s' % con.lastError().databaseText())
    sys.exit(1)

# Create a query and execute it right away using .exec()
createTableQuery = QSqlQuery()
createTableQuery.exec_(
    '''
    CREATE TABLE contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        name VARCHAR(40) NOT NULL,
        job VARCHAR(50),
        email VARCHAR(40) NOT NULL
    )
    '''
)

print(con.tables())

# Creating a query for later execution using .prepare()
insertDataQuery = QSqlQuery()
insertDataQuery.prepare(
    '''
    INSERT INTO contacts (
        name,
        job,
        email
    )
    VALUES (?, ?, ?)
    '''
)

# Sample data
data = [
    ('Joe', 'Senior Web Developer', 'joe@example.com'),
    ('Lara', 'Project Manager', 'lara@example.com'),
    ('David', 'Data Analyst', 'david@example.com'),
    ('Jane', 'Senior Python Developer', 'jane@example.com'),
]

# Use .addBindValue() to insert data
for name, job, email in data:
    insertDataQuery.addBindValue(name)
    insertDataQuery.addBindValue(job)
    insertDataQuery.addBindValue(email)
    insertDataQuery.exec_()
