import pandas as pd

max_rows = pd.get_option('display.max_rows')
max_columns = pd.get_option('display.max_columns')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

csvname = 'https://raw.githubusercontent.com/bitwalk123/PySide6_sample/refs/heads/main/iris.csv'
df = pd.read_csv(csvname, index_col=0)
print(df)

pd.set_option('display.max_rows', max_rows)
pd.set_option('display.max_columns', max_columns)
