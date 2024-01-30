import mplfinance as mpf
import pandas as pd
import yfinance as yf

from qt_mpl_finance_2_sub import StockChart


def draw_chart(chart:StockChart, ticker:str, df:pd.DataFrame):
    chart.clearAxes()
    chart.ax.set_title(ticker)
    mpf.plot(
        df,
        type='candle',
        datetime_format='%m/%d',
        mav=(5, 25),
        tight_layout=False,
        style='yahoo',
        ax=chart.ax,
        volume=chart.ax2
    )
    chart.ax.grid()
    chart.ax2.grid()
    chart.refreshDraw()


def get_trade_info(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, period='3mo')
    return df
