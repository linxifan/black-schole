# BSM research notes — general baseline

## Goal
Extend the original call-price-versus-volatility experiment with one-factor-at-a-time
sensitivity plots and analytical Greeks, before selecting a research expansion.

## Experiments
Run `python experiments.py` to generate price vs S, K, T and sigma and Vega vs sigma.
The fixed illustrative baseline is S=K=100, T=30/365 years, r=4%, sigma=25%.
Each curve changes **only one** parameter at a time.

Expected results for a no-dividend European call:
- Higher stock price S increases call price; higher strike K decreases it.
- Longer expiry T increases call price when r >= 0 (as in this experiment).
- Higher assumed volatility sigma increases call price.
- Vega is the first derivative of the call price with respect to sigma;
  its shape is not generally constant or linear.

## Greeks and conventions
- Delta = dC/dS; Gamma = d²C/dS².
- Vega = dC/dsigma. Unit: option-price change for +1.0 in sigma;
  divide by 100 for the approximate effect of +1 volatility percentage point.
- Theta = -dC/dT (calendar time decay, per year, with T as time remaining).
- Rho = dC/dr, per +1.0 in continuously compounded annual rate.

`test_models.py` compares analytical Greeks against central finite differences.
The original `main.py` still uses downloaded AAPL prices to estimate
**historical/realized** volatility, not option-implied volatility.

## Important limits
BSM here assumes constant sigma and r, no dividends, continuous hedging,
lognormal stock-price dynamics and European exercise. Fixed baseline inputs
are synthetic, not current option quotes. No market option prices are fetched,
so this does not estimate **implied volatility** or validate actual market prices.

## Next questions
1. How do empirical call option prices differ from BSM predictions?
2. Can quoted calls at different strikes/expiries reveal a volatility smile?
3. What happens to hedging error when Delta adjustments are discrete?
