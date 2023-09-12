import pandas as pd


def main():
    filename = 'utf_all.zip'
    df = pd.read_csv(filename, header=None, compression='zip')
    print(df)


if __name__ == "__main__":
    main()
