from PySide6.QtCore import QByteArray
from PySide6.QtSql import QSqlQuery


def get_content_from_filename(filename: str) -> bytes:
    byte_array = None
    content = None
    query = QSqlQuery()
    sql = """
        SELECT content FROM pdfrepo
        WHERE name_file = '%s';
    """ % filename
    flag = query.exec(sql)
    if query.next():
        byte_array = query.value(0)
    if not flag:
        print(query.lastError())
    if byte_array is not None:
        content = byte_array.data()
    return content


def get_list_file(list_file: list):
    query = QSqlQuery()
    sql = 'SELECT name_file FROM pdfrepo;'
    flag = query.exec(sql)
    while query.next():
        list_file.append(query.value(0))
    if not flag:
        print(query.lastError())


def insert_filename_content(filename: str, content: bytes):
    sql = 'INSERT INTO pdfrepo VALUES(?, ?);'
    query = QSqlQuery()
    query.prepare(sql)
    query.bindValue(0, filename)
    query.bindValue(1, QByteArray(content))
    if not query.exec():
        print(query.lastError())
