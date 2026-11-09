"""Verify deterministic workshop inputs and a minimal, isolated execution package."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import yaml

from python.synthetic import build_parameters, prepare_workspace

ROOT = Path(__file__).resolve().parents[1]


class SyntheticTests(unittest.TestCase):
    def setUp(self):
        self.scenario = yaml.safe_load((ROOT / 'scenarios/synthetic_demo.yaml').read_text())

    def test_only_pricing_inputs_are_generated(self):
        config, models = build_parameters(self.scenario)
        self.assertEqual(set(models), {'opt_table_params', 'wtp_parameters', 'visit_curve'})
        self.assertEqual(config['workflow'], 'pricing-workshop-v1')
        self.assertEqual(set(config), {'leadtime', 'capacity', 'people', 'price_interval',
                                      'mt_multiplier', 'input_source', 'scenario', 'workflow'})
        weights = models['visit_curve'].visit.to_numpy()
        self.assertAlmostEqual(weights.sum(), 1)
        self.assertEqual(len(weights), self.scenario['leadtime'] + 1)
        for multiplier in config['mt_multiplier']:
            probabilities = weights * config['people'] * multiplier
            self.assertTrue(((probabilities >= 0) & (probabilities <= 1)).all())
            self.assertAlmostEqual(probabilities.sum(), config['people'] * multiplier)

    def test_invalid_inputs_are_rejected(self):
        for change in ({'people': 1000}, {'mt_multiplier': [1.0, 1.0]},
                       {'mt_multiplier': [0.6]}, {'capacity': 0}, {'simulation_num': 100}):
            scenario = copy.deepcopy(self.scenario)
            scenario.update(change)
            with self.assertRaises(ValueError):
                build_parameters(scenario)

    def test_workspace_uses_only_allowed_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            root.mkdir()
            for name in ('requirements.txt', 'pyproject.toml', 'uv.lock', '.python-version'):
                (root / name).write_bytes((ROOT / name).read_bytes())
            for number in (2, 3):
                path = next(ROOT.glob(f'{number:02d}_*.ipynb'))
                (root / path.name).write_bytes(path.read_bytes())
            output = Path(directory) / 'workshop'
            prepare_workspace(ROOT / 'scenarios/synthetic_demo.yaml', output, root)
            for name in ('requirements.txt', 'pyproject.toml', 'uv.lock', '.python-version'):
                self.assertEqual((output / name).read_bytes(), (ROOT / name).read_bytes())
            self.assertFalse((output / 'data').exists())
            self.assertFalse((output / 'python').exists())
            self.assertEqual(len(list((output / 'model').glob('*.pickle'))), 3)
            self.assertEqual(len(list(output.glob('*.ipynb'))), 2)
            for path in output.glob('*.ipynb'):
                for cell in json.loads(path.read_text())['cells']:
                    if cell['cell_type'] == 'code':
                        self.assertEqual(cell['outputs'], [])
                        self.assertIsNone(cell['execution_count'])
            before = (output / 'config.yaml').read_bytes()
            with self.assertRaises(FileExistsError):
                prepare_workspace(ROOT / 'scenarios/synthetic_demo.yaml', output, root)
            self.assertEqual(before, (output / 'config.yaml').read_bytes())

    def test_execution_staging_excludes_adjacent_private_files(self):
        from scripts.execute_workshop import stage_sources, ENV_FILES, NOTEBOOK_FILES
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            output = Path(directory) / 'output'
            root.mkdir()
            output.mkdir()
            allowed = (*ENV_FILES, *NOTEBOOK_FILES,
                       'python/synthetic.py', 'scenarios/synthetic_demo.yaml')
            for name in allowed:
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((ROOT / name).read_bytes())
            for name in ('python/private.csv', 'scenarios/client.yaml', '99_private.ipynb'):
                (root / name).write_text('must not be copied')
            stage_sources(output, root)
            actual = {str(p.relative_to(output)) for p in output.rglob('*') if p.is_file()}
            self.assertEqual(actual, set(allowed))
            for name in NOTEBOOK_FILES:
                for cell in json.loads((output / name).read_text())['cells']:
                    if cell['cell_type'] == 'code':
                        self.assertEqual(cell['outputs'], [])
                        self.assertIsNone(cell['execution_count'])

    def test_workshop_notebooks_do_not_contain_removed_concepts(self):
        paths = sorted(ROOT.glob('*.ipynb'))
        self.assertEqual([p.name[:2] for p in paths], ['01', '02', '03'])
        for path in paths:
            source = '\n'.join(''.join(c['source']) for c in json.loads(path.read_text())['cells']).lower()
            for term in ('cancellation', 'refund', 'confusion', 'can_t', 'ref_t', 'pred_cancel'):
                self.assertNotIn(term, source, path.name)
