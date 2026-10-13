"""Offline, one-factor-at-a-time BSM sensitivity plots.

Run: python experiments.py
All parameters are illustrative; no live market data is required.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from black_scholes import european_call_price
from greeks import call_greeks

OUTPUT_DIR = Path("plots")
BASE = dict(S=100.0, K=100.0, T=30 / 365, r=0.04, sigma=0.25)

def make_plots(output_dir=OUTPUT_DIR):
    """Create four price curves and one Vega curve, returning their paths."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    sweeps = {
        "stock_price": ("Stock price (S)", np.linspace(60, 140, 100)),
        "strike_price": ("Strike price (K)", np.linspace(60, 140, 100)),
        "time_to_expiry": ("Time to expiry (years)", np.linspace(1 / 365, 2, 100)),
        "volatility": ("Annualized volatility (sigma)", np.linspace(0.05, 0.80, 100)),
    }
    paths = []
    for key, (label, values) in sweeps.items():
        params = {**BASE, {"stock_price":"S","strike_price":"K",
                           "time_to_expiry":"T","volatility":"sigma"}[key]: values}
        prices = european_call_price(**params)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(values, prices, linewidth=2)
        ax.set(xlabel=label, ylabel="European call price",
               title=f"Black-Scholes call price vs {label}")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        path = output_dir / f"call_vs_{key}.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        paths.append(path)

    sigmas = sweeps["volatility"][1]
    vegas = call_greeks(**{**BASE, "sigma": sigmas})["vega"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sigmas, vegas, linewidth=2)
    ax.set(xlabel="Annualized volatility (sigma)", ylabel="Vega (per 1.0 sigma)",
           title="BSM Vega vs volatility")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = output_dir / "vega_vs_volatility.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)
    return paths

if __name__ == "__main__":
    print("Illustrative inputs:", BASE)
    print("Greeks at baseline:", call_greeks(**BASE))
    for path in make_plots():
        print("Saved:", path)
