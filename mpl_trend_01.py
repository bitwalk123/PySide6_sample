import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate

if __name__ == '__main__':
    csvfile = 'temperature.csv'
    df = pd.read_csv(csvfile, index_col=0)
    df.index = pd.to_datetime(df.index)
    print(df)

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Spline test')

    line1 = plt.plot(
        df['気温'],
        linewidth=1,
        color='blue',
        marker='o',
        markersize=6,
        markeredgecolor='darkblue',
        markeredgewidth=1,
        markerfacecolor='cyan',
        label='original'
    )

    # for spline
    f = interpolate.interp1d(
        df.index.map(pd.Timestamp.timestamp),
        df['気温'],
        kind='quadratic'
    )
    x = pd.date_range(min(df.index), max(df.index), freq='1min')
    y = f(x.map(pd.Timestamp.timestamp))
    line2 = plt.plot(
        x, y,
        linewidth=1,
        color='red',
        label='spline curve'
    )

    plt.grid()
    plt.xticks(rotation=45)
    plt.ylabel('Temperature')
    fig.legend(loc='outside lower center')

    plt.subplots_adjust(top=0.99, left=0.1, bottom=0.25, right=0.95)
    plt.show()

