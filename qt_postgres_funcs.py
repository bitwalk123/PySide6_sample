from PySide6.QtSql import QSqlQuery


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
