import matplotlib.pyplot as plt
import pandas as pd
from pandas import DatetimeIndex, Index
from scipy.interpolate import make_interp_spline, BSpline

if __name__ == '__main__':
    csvfile = 'temperature.csv'
    df = pd.read_csv(csvfile, index_col=0, parse_dates=True)
    print(df.index)

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Trend test with spline curve')

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

    ts: Index = df.index.map(pd.Timestamp.timestamp)
    print(ts)
    bspl: BSpline = make_interp_spline(ts, df['気温'], k=2)
    # dbspl = bspl.derivative(nu=1)

    x1: DatetimeIndex = pd.date_range(min(df.index), max(df.index), freq='1min')
    ts1: Index = x1.map(pd.Timestamp.timestamp)
    y1 = bspl(ts1)
    # dy1 = dbspl(ts1)

    line2 = plt.plot(
        x1, y1,
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
