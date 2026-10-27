"""Synthetic volatility-smile experiment; run: python volatility_smile_experiment.py."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from black_scholes import european_call_price
from greeks import call_greeks

S, T, R, BASE_SIGMA = 100.0, 30 / 365, 0.04, 0.25
STRIKES = np.linspace(70, 130, 61)
STRENGTHS = (0, 0.5, 1.0, 1.5, 2.0)
OUTPUT_DIR = Path("plots/volatility_smile")


def smile_volatility(K, a):
    """Synthetic symmetric smile: sigma(K,a) = 0.25 + a*((K-S)/S)^2."""
    if a < 0:
        raise ValueError("Smile strength must be nonnegative")
    return BASE_SIGMA + a * ((np.asarray(K) - S) / S) ** 2


def run_experiment(a):
    fixed = np.asarray(european_call_price(S, STRIKES, T, R, BASE_SIGMA))
    sigma = smile_volatility(STRIKES, a)
    synthetic = np.asarray(european_call_price(S, STRIKES, T, R, sigma))
    error = fixed - synthetic
    vega = call_greeks(S, STRIKES, T, R, BASE_SIGMA)["vega"]
    df = pd.DataFrame({
        "strike": STRIKES, "fixed_sigma": BASE_SIGMA,
        "smile_sigma": sigma, "fixed_price": fixed,
        "synthetic_market_price": synthetic, "pricing_error": error,
        "absolute_error": np.abs(error), "baseline_vega": vega,
        "vega_approx_change": vega * (sigma - BASE_SIGMA),
        "actual_price_change": synthetic - fixed,
    })
    mae = float(np.mean(np.abs(error)))
    rmse = float(np.sqrt(np.mean(error ** 2)))
    return df, mae, rmse


def save_plot(filename, title, ylabel):
    plt.xlabel("Strike price (K)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=200)
    plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    runs = {}
    for a in STRENGTHS:
        df, mae, rmse = run_experiment(a)
        runs[a] = df
        summary.append({"smile_strength": a, "MAE": mae, "RMSE": rmse})
        df.to_csv(OUTPUT_DIR / f"results_a_{a:.1f}.csv", index=False)
        print(f"a={a:.1f}: MAE={mae:.6f}, RMSE={rmse:.6f}")
    pd.DataFrame(summary).to_csv(OUTPUT_DIR / "experiment_summary.csv", index=False)

    for a in STRENGTHS:
        plt.plot(STRIKES, smile_volatility(STRIKES, a) * 100, label=f"a={a}")
    save_plot("01_volatility_smile.png", "Synthetic volatility smiles", "Volatility (%)")

    # Side-by-side comparison: full price scale and magnified difference.
    df = runs[1.0]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(df["strike"], df["fixed_price"], label="Constant BSM")
    axes[0].plot(df["strike"], df["synthetic_market_price"], "--", label="Synthetic smile")
    axes[0].set_title("Full call price comparison (a=1)")
    axes[0].set_xlabel("Strike price (K)")
    axes[0].set_ylabel("Call price ($)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(
        df["strike"], df["synthetic_market_price"] - df["fixed_price"],
        label="Synthetic smile - Constant BSM", color="tab:orange"
    )
    axes[1].axhline(0, color="gray", linewidth=0.8)
    axes[1].set_title("Magnified price difference (a=1)")
    axes[1].set_xlabel("Strike price (K)")
    axes[1].set_ylabel("Price difference ($)")
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "02_price_comparison.png", dpi=200)
    plt.close(fig)

    for a in STRENGTHS:
        plt.plot(STRIKES, runs[a]["absolute_error"], label=f"a={a}")
    save_plot("03_pricing_error.png", "Absolute pricing errors", "Absolute error ($)")

    plt.plot([r["smile_strength"] for r in summary],
             [r["RMSE"] for r in summary], marker="o", label="RMSE")
    plt.xlabel("Smile strength (a)")
    plt.ylabel("RMSE ($)")
    plt.title("Smile strength vs pricing RMSE")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_rmse_sensitivity.png", dpi=200)
    plt.close()

    plt.plot(df["strike"], df["actual_price_change"], label="Actual synthetic change")
    plt.plot(df["strike"], df["vega_approx_change"], "--", label="Baseline Vega approximation")
    save_plot("05_vega_analysis.png", "Vega first-order approximation (a=1)", "Price change ($)")
    print(f"Output: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
