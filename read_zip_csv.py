import os
from sys import stdout

import pandas as pd
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

"""
Reference:
https://www.post.japanpost.jp/zipcode/dl/readme.html

01. 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
02. （旧）郵便番号（5桁）………………………………………　半角数字
03. 郵便番号（7桁）………………………………………　半角数字
04. 都道府県名　…………　半角カタカナ（コード順に掲載）
05. 市区町村名　…………　半角カタカナ（コード順に掲載）
06. 町域名　………………　半角カタカナ（五十音順に掲載）
07. 都道府県名　…………　漢字（コード順に掲載）
08. 市区町村名　…………　漢字（コード順に掲載）
09. 町域名　………………　漢字（五十音順に掲載）
10. 一町域が二以上の郵便番号で表される場合の表示（「1」は該当、「0」は該当せず）
11. 小字毎に番地が起番されている町域の表示（「1」は該当、「0」は該当せず）
12. 丁目を有する町域の場合の表示　（「1」は該当、「0」は該当せず）
13. 一つの郵便番号で二以上の町域を表す場合の表示（「1」は該当、「0」は該当せず）
14. 更新の表示（「0」は変更なし、「1」は変更あり、「2」廃止（廃止データのみ使用））
15. 変更理由　（「0」は変更なし、「1」市政・区政・町政・分区・政令指定都市施行、「2」住居表示の実施、「3」区画整理、「4」郵便区調整等、「5」訂正、「6」廃止（廃止データのみ使用））
"""
sql_create = '''
    CREATE TABLE postal (
        id INTEGER PRIMARY KEY,
        全国地方公共団体コード INTEGER,
        （旧）郵便番号 INTEGER,
        郵便番号 INTEGER,
        都道府県（カナ） STRING,
        市区町村（カナ） STRING,
        町域（カナ） STRING,
        都道府県（漢字） STRING,
        市区町村（漢字） STRING,
        町域（漢字） STRING,
        一町域が二以上の郵便番号 INTEGER,
        小字毎に番地が起番 INTEGER,
        丁目を有する町域 INTEGER,
        一つの郵便番号で二以上の町域 INTEGER,
        更新の表示 INTEGER,
        変更理由 INTEGER
    )
'''
# https://www.post.japanpost.jp/zipcode/download.html
filename = 'utf_all.zip'

name_db = '郵便番号.sqlite3'


def main():
    df = pd.read_csv(filename, header=None, compression='zip')

    if os.path.isfile(name_db):
        os.remove(name_db)

    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(name_db)

    if not con.open():
        exit(0)

    query = QSqlQuery()
    query.exec(sql_create)

    model_db = QSqlTableModel()
    model_db.setTable('postal')

    rows = len(df)
    for r in range(rows):
        record = model_db.record()
        for c in range(len(df.columns)):
            value = df.iloc[r:r + 1, c:c + 1].values[0][0]
            if type(value) is not str:
                value = int(value)
            record.setValue(c + 1, value)
        model_db.insertRecord(-1, record)

        comp = 100 * (r + 1) / rows
        stdout.write('\r%d%% completed' % comp)
        stdout.flush()

    stdout.write('\n')
    con.close()


if __name__ == "__main__":
    main()
