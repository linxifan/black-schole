"""Offline regression checks: python -m unittest -v."""
import unittest
import numpy as np
from black_scholes import european_call_price
from greeks import call_greeks
from experiments import BASE

class BlackScholesResearchTests(unittest.TestCase):
    def test_reference_price(self):
        self.assertAlmostEqual(european_call_price(100, 100, 1, 0.05, 0.2),
                               10.450583572185565, places=8)

    def test_call_monotonicity(self):
        p = BASE
        for name, xs, sign in (
            ("S", np.linspace(80, 120, 15), 1),
            ("K", np.linspace(80, 120, 15), -1),
            ("T", np.linspace(0.02, 2, 15), 1),
            ("sigma", np.linspace(0.08, 0.7, 15), 1),
        ):
            prices = european_call_price(**{**p, name: xs})
            self.assertTrue(np.all(sign * np.diff(prices) > 0), name)

    def test_greeks_finite_difference(self):
        p = BASE
        g = call_greeks(**p)
        price = lambda **updates: european_call_price(**{**p, **updates})
        h = 1e-3
        delta = (price(S=p["S"] + h) - price(S=p["S"] - h)) / (2*h)
        gamma = (price(S=p["S"] + h)-2*price()+price(S=p["S"]-h))/h**2
        vega = (price(sigma=p["sigma"] + h)-price(sigma=p["sigma"] - h))/(2*h)
        rho = (price(r=p["r"] + h)-price(r=p["r"] - h))/(2*h)
        theta = -(price(T=p["T"] + 1e-5)-price(T=p["T"] - 1e-5))/(2e-5)
        for name, numerical in (("delta",delta),("gamma",gamma),
                                ("vega",vega),("rho",rho),("theta",theta)):
            self.assertAlmostEqual(g[name], numerical, delta=1e-3, msg=name)

    def test_invalid_greek_inputs(self):
        with self.assertRaises(ValueError):
            call_greeks(100, 100, 0, 0.04, 0.2)

if __name__ == "__main__":
    unittest.main()
