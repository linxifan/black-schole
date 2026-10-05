# Black-Scholes Baseline: Call Price vs. Volatility

A small, readable Python project that prices a **European call option** with the standard Black-Scholes model and plots how that price changes when assumed volatility changes.

This is a research baseline only. It does **not** include Heston, stochastic volatility, a volatility smile/surface, or Monte Carlo simulation.

## What the Black-Scholes model does

Black-Scholes gives a closed-form price for a European option (exercisable only at expiration) under a simple market model: the stock follows geometric Brownian motion, volatility is constant, there are no dividends (in this implementation), and one can hedge continuously.

The European **call** price is:

```
C = S * N(d1) - K * exp(-r * T) * N(d2)

d1 = [ln(S/K) + (r + sigma^2 / 2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```

`N(.)` is the cumulative distribution function of the standard normal.

## The five parameters

| Symbol | Meaning |
|--------|---------|
| **S** | Current stock price (here: latest closing price) |
| **K** | Strike price (here: at-the-money, rounded to the nearest dollar) |
| **T** | Time to expiration in years (here: 30/365) |
| **r** | Risk-free interest rate (here: 0.04) |
| **sigma** | Volatility of the underlying (the variable we sweep) |

## What this experiment tests

**S, K, T, and r stay fixed.** Only **sigma** changes, from 0.10 to 0.80.

For each sigma, the script computes the Black-Scholes call price and plots:

- **X-axis:** Volatility (sigma)
- **Y-axis:** Black-Scholes Call Option Price

It also estimates **AAPL**’s historical annualized volatility from about one year of daily log returns:

```
daily_returns = log(S_t / S_{t-1})
annualized_volatility = std(daily_returns) * sqrt(252)
```

That realized volatility is printed and drawn as a **vertical dashed line** on the plot. The curve should be increasing: a higher assumed volatility makes the call more expensive.

The default ticker is **AAPL**. Change `TICKER` at the top of `main.py` to use another stock.

## Project layout

| File | Role |
|------|------|
| `black_scholes.py` | Black-Scholes European call formula |
| `data.py` | yfinance download + historical volatility |
| `main.py` | Fetch data, run the sigma sweep, save the plot |
| `requirements.txt` | Python dependencies |

Start with **`main.py`** to see how the pieces fit together, then read `black_scholes.py` for the pricing formula.

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

This prints S, K, T, r, historical volatility, a few sample prices, and writes:

```
black_scholes_call_vs_volatility.png
```

Internet access is required so yfinance can download prices from Yahoo Finance.
