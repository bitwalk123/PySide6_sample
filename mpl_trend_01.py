import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    csvfile = 'temperature.csv'
    df = pd.read_csv(csvfile, index_col=0, parse_dates=True)
    print(df)
    print(type(df.index))

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Trend test')

    line1 = plt.plot(
        df,
        linewidth=1,
        color='blue',
        marker='o',
        markersize=6,
        markeredgecolor='darkblue',
        markeredgewidth=1,
        markerfacecolor='cyan',
        label='original data'
    )

    plt.grid()
    plt.xticks(rotation=45)
    plt.ylabel('Temperature')
    fig.legend(loc='outside lower center')

    plt.subplots_adjust(top=0.99, left=0.1, bottom=0.25, right=0.95)
    plt.show()
