"""Check the actual teaching-notebook function against independent small problems."""
import ast
from functools import lru_cache
import json
import math
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
from scipy.stats import norm


class PricingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / '03_estimate_optimized_price_table.ipynb'
        notebook = json.loads(path.read_text())
        definitions = []
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                definitions.extend(node for node in ast.parse(''.join(cell['source'])).body
                                   if isinstance(node, ast.FunctionDef) and node.name == 'create_optimized_price_table')
        assert len(definitions) == 1
        namespace = {'np': np, 'pd': pd, 'norm': norm}
        exec(compile(ast.Module(body=definitions, type_ignores=[]), str(path), 'exec'), namespace)
        cls.calculate = staticmethod(namespace['create_optimized_price_table'])

    def test_single_period_matches_direct_expected_revenue(self):
        prices = np.array([5., 10., 15.])
        p, v = self.calculate([0.7], prices, 12, 4, 2)
        expected = [0.7 * 0.5 * math.erfc((price - 12) / (4 * math.sqrt(2))) * price for price in prices]
        self.assertEqual(p.loc[0, 1], prices[np.argmax(expected)])
        self.assertAlmostEqual(v.loc[0, 1], max(expected))
        self.assertAlmostEqual(v.loc[0, 2], max(expected))

    def test_small_problem_matches_recursive_decision_tree(self):
        arrivals, prices, mu, sigma = [0.2, 0.9, 0.6], [5., 10., 15.], 12, 4
        @lru_cache(None)
        def reference(t, rooms):
            if t < 0 or rooms == 0:
                return 0.0
            return max(
                arrivals[t] * 0.5 * math.erfc((price - mu) / (sigma * math.sqrt(2)))
                * (price + reference(t - 1, rooms - 1))
                + (1 - arrivals[t] * 0.5 * math.erfc((price - mu) / (sigma * math.sqrt(2))))
                * reference(t - 1, rooms)
                for price in prices)
        p, v = self.calculate(arrivals, prices, mu, sigma, 3)
        for t in range(3):
            for rooms in range(4):
                self.assertAlmostEqual(v.loc[t, rooms], reference(t, rooms))
        self.assertTrue(np.isinf(p[0]).all())

    def test_no_arrivals_zero_capacity_and_ties(self):
        p, v = self.calculate([0, 0], [5, 10], 12, 4, 2)
        self.assertTrue((v.to_numpy() == 0).all())
        self.assertTrue((p.iloc[:, 1:].to_numpy() == 5).all())
        p, v = self.calculate([0.5], [5, 10], 12, 4, 0)
        self.assertTrue(np.isinf(p.to_numpy()).all())
        self.assertEqual(v.loc[0, 0], 0)

    def test_invalid_probabilities_are_not_silently_clipped(self):
        for arrival in ([1.01], [-0.1], [np.nan], []):
            with self.assertRaises(ValueError):
                self.calculate(arrival, [5, 10], 12, 4, 2)

    def test_fixed_workshop_conditions_change_prices(self):
        from python.synthetic import build_parameters
        import yaml
        root = Path(__file__).resolve().parents[1]
        config, models = build_parameters(yaml.safe_load((root / 'scenarios/synthetic_demo.yaml').read_text()))
        low, high, step = models['opt_table_params']
        tables = {}
        for multiplier in config['mt_multiplier']:
            tables[multiplier], values = self.calculate(models['visit_curve'].visit * config['people'] * multiplier,
                                                         np.arange(low, high, step), *models['wtp_parameters'], config['capacity'])
            self.assertTrue((np.diff(values, axis=0) >= -1e-8).all())
            self.assertTrue((np.diff(values, axis=1) >= -1e-8).all())
        self.assertFalse(np.array_equal(tables[0.6], tables[1.2]))
