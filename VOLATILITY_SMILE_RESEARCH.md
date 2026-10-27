# Experiment 2: Synthetic Volatility Smile

**Research question:** How does a strike-dependent volatility smile change European call prices relative to constant-volatility Black–Scholes pricing?

Run from repo root:

```bash
pip install -r requirements.txt
python volatility_smile_experiment.py
python -m unittest test_volatility_smile.py
```

Figures and CSV tables are generated in `plots/volatility_smile/`.

## Design

- Stock price S = 100; maturity T = 30/365 years; continuously compounded risk-free rate r = 4%.
- Strike prices K = 70 through 130, 61 equally spaced values.
- Constant-volatility baseline sigma0 = 25%.
- Synthetic symmetric smile: sigma(K,a) = 0.25 + a*((K-100)/100)^2.
- Strength a takes 0, 0.5, 1, 1.5 and 2.
- Synthetic market price = BSM(S,K,T,r,sigma(K,a)); comparison price = BSM(S,K,T,r,0.25).
- Signed error = comparison price minus synthetic price; MAE and RMSE average across the 61 strikes.
- Vega approximation = Vega at baseline sigma times (sigma(K,a)-sigma0). Compare with exact synthetic minus baseline price.

Outputs include five plots (smile, price comparison, absolute error, RMSE vs strength, and Vega comparison), per-strength CSVs, and an aggregate CSV.

**Interpretation:** This is a controlled synthetic exercise, not validation against observed market options. Both price sets use the same Black–Scholes formula. The symmetric smile is a hypothetical input, not guaranteed to be arbitrage-free at every setting. Vega is a first-order local approximation and may differ from the exact change for larger volatility shifts. An asymmetric skew and real market-data validation are possible future extensions.
