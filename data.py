"""
Download stock prices with yfinance and estimate historical volatility.

Annualized volatility is computed from daily log returns:
    daily_returns = log(S_t / S_{t-1})
    annualized_volatility = std(daily_returns) * sqrt(252)
"""

import numpy as np
import yfinance as yf

# Default ticker for the baseline experiment. Change this in main.py.
DEFAULT_TICKER = "AAPL"
TRADING_DAYS_PER_YEAR = 252


def download_history(ticker=DEFAULT_TICKER, period="1y"):
    """
    Download recent daily price history for a ticker.

    Parameters
    ----------
    ticker : str
        Yahoo Finance ticker symbol (e.g. "AAPL").
    period : str
        Lookback window passed to yfinance (default: about one year).

    Returns
    -------
    pandas.DataFrame
        Daily OHLCV history. Raises ValueError if no data is returned.
    """
    history = yf.Ticker(ticker).history(period=period, auto_adjust=True)

    if history.empty:
        raise ValueError(
            f"No price data returned for ticker {ticker!r}. "
            "Check the symbol or your network connection."
        )

    return history


def latest_close(history):
    """Return the most recent closing price as S."""
    return float(history["Close"].iloc[-1])


def historical_volatility(history):
    """
    Annualized historical volatility from daily log returns.

    Uses Close prices over the downloaded window (about one year by default).
    """
    close = history["Close"].astype(float)
    daily_returns = np.log(close / close.shift(1)).dropna()

    if daily_returns.empty:
        raise ValueError("Not enough price observations to compute volatility.")

    return float(daily_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR))
