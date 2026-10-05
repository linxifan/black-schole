"""
Run a simple Black-Scholes volatility sensitivity experiment.

Keeps S, K, T, and r fixed, then prices a European call across a range
of assumed volatilities (sigma). Also marks the stock's realized
historical volatility on the resulting plot.
"""

import matplotlib

matplotlib.use("Agg")  # headless-friendly; still saves a PNG

import matplotlib.pyplot as plt
import numpy as np

from black_scholes import european_call_price
from data import DEFAULT_TICKER, download_history, historical_volatility, latest_close

# --- experiment settings (easy to change) -----------------------------------
TICKER = DEFAULT_TICKER  # e.g. "AAPL", "MSFT", "GOOGL"
T = 30 / 365  # 30 days to expiration, in years
R = 0.04  # risk-free interest rate
SIGMA_MIN = 0.10
SIGMA_MAX = 0.80
N_SIGMA = 50  # number of volatility points on the curve
OUTPUT_PLOT = "black_scholes_call_vs_volatility.png"


def main():
    print(f"Downloading ~1 year of daily prices for {TICKER}...")
    history = download_history(TICKER, period="1y")

    S = latest_close(history)
    K = round(S)  # at-the-money: strike near the current price
    hist_vol = historical_volatility(history)

    print(f"  latest close (S): {S:.2f}")
    print(f"  strike (K):       {K:.2f}  (at-the-money)")
    print(f"  time to expiry T: {T:.6f} years  (30/365)")
    print(f"  risk-free rate r: {R:.2%}")
    print(f"  historical annualized volatility: {hist_vol:.2%}")

    # Volatility sweep with S, K, T, r held fixed
    sigmas = np.linspace(SIGMA_MIN, SIGMA_MAX, N_SIGMA)
    prices = european_call_price(S, K, T, R, sigmas)

    print("\nSample Black-Scholes call prices:")
    for sigma, price in zip(sigmas[::10], prices[::10]):
        print(f"  sigma = {sigma:.2f}  ->  C = {price:.2f}")

    plot_price_vs_volatility(sigmas, prices, hist_vol, S, K)
    print(f"\nSaved plot to {OUTPUT_PLOT}")


def plot_price_vs_volatility(sigmas, prices, hist_vol, S, K):
    """Plot call price against assumed volatility, with realized vol marked."""
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(sigmas, prices, color="steelblue", linewidth=2, label="Black-Scholes call")
    ax.axvline(
        hist_vol,
        color="firebrick",
        linestyle="--",
        linewidth=1.5,
        label=f"Historical vol ({hist_vol:.1%})",
    )

    ax.set_xlabel("Volatility (sigma)")
    ax.set_ylabel("Black-Scholes Call Option Price")
    ax.set_title("Black-Scholes Call Price vs. Volatility")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Caption in the upper-right so it does not cross the historical-vol line
    ax.text(
        0.98,
        0.98,
        f"{TICKER}  S={S:.2f}  K={K:.2f}  T=30/365  r={R:.0%}",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=8,
        color="dimgray",
    )

    fig.tight_layout()
    fig.savefig(OUTPUT_PLOT, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
