"""
Standard Black-Scholes pricing for a European call option.

Formula:
    C = S * N(d1) - K * exp(-r * T) * N(d2)

where
    d1 = [ln(S/K) + (r + sigma^2 / 2) * T] / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    N(.) is the standard normal CDF
"""

import numpy as np
from scipy.stats import norm


def _d1(S, K, T, r, sigma):
    """First term of the Black-Scholes formula."""
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def _d2(S, K, T, r, sigma):
    """Second term: d1 shifted by sigma * sqrt(T)."""
    return _d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def european_call_price(S, K, T, r, sigma):
    """
    Price a European call option with the Black-Scholes model.

    Parameters
    ----------
    S : float
        Current stock price.
    K : float
        Strike price.
    T : float
        Time to expiration in years.
    r : float
        Risk-free interest rate (annual, continuously compounded).
    sigma : float or array-like
        Volatility (annualized). Can be a single value or many values.

    Returns
    -------
    float or numpy.ndarray
        Call option price(s). A scalar if sigma is a scalar.
    """
    sigma = np.asarray(sigma, dtype=float)
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)

    # C = S * N(d1) - K * e^{-rT} * N(d2)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    if price.ndim == 0:
        return float(price)
    return price
