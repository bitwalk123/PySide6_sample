import matplotlib.pyplot as plt
import pandas as pd
from pandas import DatetimeIndex, Index
from scipy.interpolate import make_interp_spline, BSpline

if __name__ == '__main__':
    csvfile = 'temperature.csv'
    df = pd.read_csv(csvfile, index_col=0, parse_dates=True)

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Trend test with spline curve & derivative')

    line1 = ax.plot(
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
    bspl: BSpline = make_interp_spline(ts, df['気温'], k=2)
    dbspl = bspl.derivative(nu=1)

    x1: DatetimeIndex = pd.date_range(min(df.index), max(df.index), freq='1min')
    ts1: Index = x1.map(pd.Timestamp.timestamp)
    y1 = bspl(ts1)
    dy1 = dbspl(ts1)

    line2 = ax.plot(
        x1, y1,
        linewidth=1,
        color='red',
        label='spline curve'
    )

    ax2 = ax.twinx()
    line3 = ax2.plot(
        x1, dy1,
        linewidth=1,
        linestyle='dashed',
        color='violet',
        label='derivative'
    )

    fig.legend(loc='outside lower center')

    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.set_ylabel('Temperature')
    ax.grid()

    ax2.set_ylabel('Derivative')

    plt.subplots_adjust(top=0.99, left=0.1, bottom=0.3, right=0.8)
    plt.show()
