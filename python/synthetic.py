"""Generate invented demand and willingness-to-pay inputs for the pricing workshop."""

import json
from pathlib import Path
import pickle
import shutil

import numpy as np
import pandas as pd
from scipy.stats import lognorm
import yaml


def _number(value, name, lower=0, upper=np.inf, integer=False, positive=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not np.isfinite(value) or value < lower or value > upper
            or (positive and value <= 0) or (integer and not isinstance(value, int))):
        raise ValueError(f'Invalid {name}: {value!r}')
    return value


def build_parameters(scenario):
    """Return the runtime configuration and three deterministic pricing inputs."""
    s = scenario
    required = {'name', 'leadtime', 'capacity', 'people', 'price_interval',
                'mt_multiplier', 'wtp', 'price', 'arrival'}
    if set(s) != required:
        raise ValueError(f'Scenario fields must be exactly: {sorted(required)}')
    for key in ('leadtime', 'capacity', 'price_interval'):
        _number(s[key], key, integer=True, positive=True)
    _number(s['people'], 'people', positive=True)
    multipliers = s['mt_multiplier']
    if not isinstance(multipliers, list) or not multipliers:
        raise ValueError('mt_multiplier must be a non-empty list')
    for value in multipliers:
        _number(value, 'mt_multiplier', positive=True)
    if 1.0 not in multipliers or len(set(multipliers)) != len(multipliers):
        raise ValueError('mt_multiplier must be unique and include baseline 1.0')
    mu = _number(s['wtp']['mean'], 'wtp.mean', positive=True)
    sigma = _number(s['wtp']['std'], 'wtp.std', positive=True)
    low = _number(s['price']['min'], 'price.min', positive=True, integer=True)
    high = _number(s['price']['max'], 'price.max', positive=True, integer=True)
    if high <= low:
        raise ValueError('price.max must exceed price.min')
    log_mean = _number(s['arrival']['log_mean'], 'arrival.log_mean', lower=-100, upper=100)
    log_std = _number(s['arrival']['log_std'], 'arrival.log_std', positive=True)
    weights = np.diff(lognorm.cdf(np.arange(s['leadtime'] + 2),
                                  s=log_std, scale=np.exp(log_mean)))
    if not np.isfinite(weights.sum()) or weights.sum() <= 0:
        raise ValueError('Arrival distribution has no representable mass in the horizon')
    weights /= weights.sum()
    if weights.max() * s['people'] * max(multipliers) > 1:
        raise ValueError('Arrival probability exceeds 1; reduce people/multipliers or broaden the arrival curve')
    config = {key: s[key] for key in ('leadtime', 'capacity', 'people', 'price_interval', 'mt_multiplier')}
    config.update(input_source='synthetic', scenario=s['name'], workflow='pricing-workshop-v1')
    models = {
        'opt_table_params': [low, high, s['price_interval']],
        'wtp_parameters': [mu, sigma],
        'visit_curve': pd.DataFrame({'visit': weights}),
    }
    return config, models


def prepare_workspace(scenario_path, output, source_root=None):
    """Create a fresh workspace from an explicit source allowlist, without old outputs."""
    scenario = yaml.safe_load(Path(scenario_path).read_text(encoding='utf-8'))
    config, models = build_parameters(scenario)
    root = Path(source_root) if source_root else Path(__file__).resolve().parents[1]
    notebooks = [next(root.glob(f'{number:02d}_*.ipynb')) for number in (2, 3)]
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    for name in ('model', 'result', 'fig'):
        (output / name).mkdir()
    for name in ('requirements.txt', 'pyproject.toml', 'uv.lock', '.python-version'):
        shutil.copyfile(root / name, output / name)
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding='utf-8'))
        notebook['metadata'] = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}
        for cell in notebook['cells']:
            cell['metadata'] = {}
            if cell['cell_type'] == 'code':
                cell['outputs'] = []
                cell['execution_count'] = None
        (output / path.name).write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    (output / 'config.yaml').write_text(yaml.safe_dump(config), encoding='utf-8')
    (output / 'scenario.yaml').write_text(yaml.safe_dump(scenario), encoding='utf-8')
    for name, value in models.items():
        with (output / 'model' / f'{name}.pickle').open('wb') as handle:
            pickle.dump(value, handle)
    (output / 'README.md').write_text(
        '# Hotel pricing workshop\n\n'
        'Inputs are invented assumptions in `scenario.yaml`. Run `uv sync --locked`, '
        'then run Notebook 02 (distributions) and 03 (optimal prices), using this folder '
        'as the working directory. No observations or pre-existing models are required.\n'
        'Pricing is deterministic: every accepted sale permanently consumes one room.\n', encoding='utf-8')
    return output
