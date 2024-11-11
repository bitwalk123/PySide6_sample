import pandas as pd

csvname = 'https://raw.githubusercontent.com/bitwalk123/PySide6_sample/refs/heads/main/iris.csv'
df = pd.read_csv(csvname, index_col=0)
print(df)