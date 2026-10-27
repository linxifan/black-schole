"""Regression checks for Experiment 2."""
import unittest
import numpy as np
from volatility_smile_experiment import STRIKES, BASE_SIGMA, smile_volatility, run_experiment


class VolatilitySmileTests(unittest.TestCase):
    def test_zero_smile_matches_baseline(self):
        df, mae, rmse = run_experiment(0)
        self.assertTrue(np.allclose(df["smile_sigma"], BASE_SIGMA))
        self.assertAlmostEqual(mae, 0, places=12)
        self.assertAlmostEqual(rmse, 0, places=12)

    def test_smile_symmetric_and_atm_unchanged(self):
        sigma = smile_volatility(STRIKES, 1.0)
        self.assertTrue(np.allclose(sigma, sigma[::-1]))
        self.assertAlmostEqual(sigma[len(sigma)//2], BASE_SIGMA)

    def test_rmse_increases_with_strength(self):
        rmses = [run_experiment(a)[2] for a in (0, 0.5, 1, 1.5, 2)]
        self.assertTrue(all(x < y for x, y in zip(rmses, rmses[1:])))

    def test_vega_approx_direction(self):
        df, _, _ = run_experiment(1)
        self.assertTrue(np.all(df["vega_approx_change"] >= 0))
        self.assertTrue(np.all(df["actual_price_change"] >= -1e-10))


if __name__ == "__main__":
    unittest.main()
