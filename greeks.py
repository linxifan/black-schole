"""Analytical Black-Scholes Greeks for European calls (no dividends)."""
import numpy as np
from scipy.stats import norm
from black_scholes import _d1, _d2

def call_greeks(S, K, T, r, sigma):
    """Return delta, gamma, vega, theta, rho; T is in years.

    Vega and rho are per 1.0 absolute change (not per 1%).
    Theta is per year. Supports scalar or broadcastable array inputs.
    Requires S, K, T, sigma > 0.
    """
    S, K, T, r, sigma = np.broadcast_arrays(
        *[np.asarray(x, dtype=float) for x in (S, K, T, r, sigma)]
    )
    if np.any(S <= 0) or np.any(K <= 0) or np.any(T <= 0) or np.any(sigma <= 0):
        raise ValueError("S, K, T and sigma must be positive")
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)
    pdf = norm.pdf(d1)
    result = {
        "delta": norm.cdf(d1),
        "gamma": pdf / (S * sigma * np.sqrt(T)),
        "vega": S * pdf * np.sqrt(T),
        "theta": -(S * pdf * sigma) / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2),
        "rho": K * T * np.exp(-r * T) * norm.cdf(d2),
    }
    return {name: float(value) if value.ndim == 0 else value
            for name, value in result.items()}
