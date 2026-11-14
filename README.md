# Hotel revenue management workshop

[日本語](README_JP.md)

Explore how demand, remaining inventory and willingness to pay change the best
offered price. Every accepted sale permanently consumes one room. This workshop
ends with optimal price tables and comparisons, using invented inputs only.

## Three notebooks

| Notebook | Purpose |
| --- | --- |
| `01_synthetic_scenario_setup.ipynb` | Choose a scenario and create a fresh workspace |
| `02_scenario_distributions.ipynb` | Explore willingness to pay and arrival probabilities |
| `03_estimate_optimized_price_table.ipynb` | Calculate optimal prices and compare demand conditions |

Follow [SKILL.md](SKILL.md) for uv installation, the locked Python 3.14 environment,
full notebook execution, local JupyterLab, dependency auditing and upgrades.
After installing uv, create the environment:

```bash
uv sync --locked
```

Run Notebook 01 from the repository root. Open **02 and 03 inside the generated
`workshop-run/` directory**, using that directory as the working directory.
Alternatively, create the same workspace from the command line:

```bash
uv run --locked python scripts/prepare_synthetic.py
```

Use a new directory for each scenario; existing directories are never overwritten:

```bash
uv run --locked python scripts/prepare_synthetic.py --scenario scenarios/synthetic_demo.yaml --output workshop-run-second
```

The generated workspace contains just Notebooks 02–03, three input parameter files,
configuration and dependencies. It does not copy research data, legacy Python
modules, existing models or saved notebook outputs. The notebooks reject old
runtime configurations before reading any model files.

## Repository structure and file roles

```text
.
├── 01_synthetic_scenario_setup.ipynb
├── 02_scenario_distributions.ipynb
├── 03_estimate_optimized_price_table.ipynb
├── README.md / README_JP.md
├── PRACTICAL_SESSION.md / PRACTICAL_SESSION_JP.md
├── SKILL.md
├── pyproject.toml / uv.lock / .python-version
├── requirements.txt
├── scenarios/
│   └── synthetic_demo.yaml
├── python/
│   └── synthetic.py
├── scripts/
│   ├── prepare_synthetic.py
│   └── execute_workshop.py
├── tests/
│   ├── test_pricing.py
│   └── test_synthetic.py
└── runs/
    ├── pricing-workshop/
    │   ├── README.md
    │   ├── scenario.yaml / config.yaml / requirements.txt
    │   ├── execution-report.json / validation.json
    │   ├── model/
    │   ├── result/price_tables.csv
    │   └── fig/distributions/ and fig/pricing/
    └── uv-verification/
        └── README.md / validation.json
```

The root notebooks are the workshop source and also contain saved execution
outputs. Their individual roles are listed above. Other files have these roles:

| File or folder | Role |
| --- | --- |
| `README.md` / `README_JP.md` | English and Japanese entry guides with matching content |
| `PRACTICAL_SESSION.md` / `PRACTICAL_SESSION_JP.md` | Student walkthrough for running, changing assumptions and comparing price tables |
| `SKILL.md` | uv setup, execution, auditing and local Jupyter instructions |
| `pyproject.toml` / `uv.lock` / `.python-version` | Dependency definitions, locked versions with hashes and the Python version |
| `requirements.txt` | Distribution dependencies automatically exported from uv.lock |
| `scripts/execute_workshop.py` | Executes 01–03 in a fresh synthetic-only folder and saves outputs |
| `scenarios/synthetic_demo.yaml` | Editable, invented input assumptions: capacity, demand, WTP, arrival timing and price grid |
| `python/synthetic.py` | Validates the scenario, generates three parameter inputs and creates an isolated workspace |
| `scripts/prepare_synthetic.py` | Command-line alternative to Notebook 01 for creating that workspace |
| `tests/test_pricing.py` | Checks the pricing function defined in Notebook 03 against independent small problems |
| `tests/test_synthetic.py` | Checks scenario validation, generated inputs, workspace isolation and the notebook scope |
| `runs/pricing-workshop/README.md` | Entry point to the saved pricing results and figures |
| `runs/pricing-workshop/scenario.yaml` | Snapshot of the input assumptions used for the saved run |
| `runs/pricing-workshop/config.yaml` | Runtime configuration generated from those assumptions |
| `runs/pricing-workshop/requirements.txt` | Dependency snapshot for the saved run |
| `runs/pricing-workshop/execution-report.json` | Notebook names and measured execution durations for the saved run |
| `runs/pricing-workshop/validation.json` | Source commit and validation checks recorded for that run, not a live test report |
| `runs/pricing-workshop/model/` | Generated inputs and calculated price/value tables for the saved run |
| `runs/pricing-workshop/result/price_tables.csv` | Prices and expected revenues by demand level, lead time and remaining inventory |
| `runs/pricing-workshop/fig/distributions/` | Saved WTP and arrival-distribution figures |
| `runs/pricing-workshop/fig/pricing/` | Saved price heatmaps, curves and baseline differences |
| `runs/uv-verification/` | Record of the uv environment verification; not a live security audit |
| `.gitignore` | Excludes generated `workshop-run*` folders, local environments and caches from Git |

### Generated workspace versus saved results

`workshop-run/` is created when you run Notebook 01 or the preparation script; it
is not part of the tracked source tree. It contains copies of Notebooks 02–03 with
outputs cleared, `scenario.yaml`, `config.yaml`, `requirements.txt`,
`pyproject.toml`, `uv.lock`, `.python-version`, and the
`model/`, `result/` and `fig/` directories. Use a new workspace for new experiments.

| Generated file | Created by | Contents |
| --- | --- | --- |
| `model/opt_table_params.pickle` | Setup | Price-grid bounds and step |
| `model/wtp_parameters.pickle` | Setup | Mean and standard deviation of WTP |
| `model/visit_curve.pickle` | Setup | Daily arrival-timing weights |
| `model/opt_price.pickle` | Notebook 03 | Optimal price tables for each demand multiplier |
| `model/opt_revenue.pickle` | Notebook 03 | Expected-revenue tables for each demand multiplier |
| `result/price_tables.csv` | Notebook 03 | Combined price/value table for inspection |
| `fig/distributions/*.png` | Notebook 02 | Input-distribution figures |
| `fig/pricing/*.png` | Notebook 03 | Optimal-price comparison figures |

`runs/pricing-workshop/` is a committed snapshot for viewing an earlier execution.
It is not read as input when a new workspace is generated. Edit the scenario and
create a new workspace rather than editing this snapshot to change an experiment.

## Practical session

Follow [PRACTICAL_SESSION.md](PRACTICAL_SESSION.md) ([日本語](PRACTICAL_SESSION_JP.md)) for the student walkthrough:
run the baseline, inspect the results, change the WTP mean, rerun, and compare
the optimal price tables.

## Outputs and interpretation

Notebook 02 saves two distribution figures. Notebook 03 saves a heatmap comparison
with a common colour scale, price curves and differences from baseline demand.
Zero-inventory states mean sales are closed and are excluded from the colour scale.
`result/price_tables.csv` contains all price/value states, and `model/` contains
optimal price and expected-revenue tables. Prices are chosen from a discrete grid.

There is no random simulation, prediction-accuracy experiment, repayment schedule
or repetition count in this workflow. Values are deterministic expected revenues.
See the pricing workshop model section below for the model and validation.

[Saved execution results](runs/pricing-workshop/README.md) contain the executed
scenario, tables and four figures. The root notebooks also include their outputs.

## Pricing workshop model

The workflow is Notebook 01 (scenario setup), 02 (distributions) and 03 (pricing).
It has no event prediction or booking-reversal model. An accepted sale is final.

### Inputs

Prices use arbitrary currency units. Arrivals are Bernoulli opportunities, at most one per day; invalid probabilities are rejected rather than clipped.

The scenario schema contains only `name`, `leadtime`, `capacity`, `wtp`, `price` and `arrival`. Unexpected top-level
fields are rejected so that obsolete configuration is not silently ignored.

- `wtp.mean` and `wtp.std` define normally distributed willingness to pay.
- `price.min`, `price.max` and `price.price_interval` define an integer price grid with
  an exclusive upper bound. The lowest price wins a tie.
- `arrival.log_mean` and `arrival.log_std` define a lognormal arrival-time variable.
  Daily mass integrates intervals $[t,t+1)$, then normalises over the horizon.
- `arrival.people` is the expected number of potential arrivals at demand multiplier 1.
- Daily arrival probability is $a_t = w_t N m$, and must be at
  most one. Here $w_t$ is the timing weight, $N$ is `arrival.people`, and $m$ is the demand multiplier. Multipliers must be unique, positive and include baseline 1.0.
- The three generated inputs are the price grid bounds, WTP parameters and
  arrival weights. There are no seed, repetition or accuracy settings.

The normal WTP model is not truncated; a negative WTP does not accept positive
prices. Arrival timing, WTP and price acceptance follow the stated exogenous
assumptions. Accepted bookings also depend on room availability.

Scenario demand multipliers are set in `arrival.mt_multiplier`. Generated `config.yaml` keeps its flat runtime format; regenerate your workspace after editing the scenario.

### Optimal pricing

Let $a_t$ be daily arrival probability, $d(p) = \Pr(\mathrm{WTP} \geq p)$ and $s(t,p) = a_t d(p)$.
Here $t$ is days before check-in, $c$ is remaining rooms, and $\mathcal{P}$ is the allowed price grid. $V(t,c)$ is optimal expected future revenue.
The only transitions are a sale (one fewer room) and no sale (same inventory):

$$
V(t,c) = \max_{p \in \mathcal{P}} \left(s(t,p)\left[p + V(t-1,c-1)\right] + \left[1-s(t,p)\right]V(t-1,c)\right).
$$

$$
V(t,0) = 0, \qquad V(-1,c) = 0.
$$

The implementation is visible in Notebook 03. It computes purchase probabilities
with the normal survival function once per price grid and stores full-precision
values during optimisation. This replaces repeated numerical integration with
direct evaluation of the same normal tail. No separate full-capacity branch is
needed. Prices for zero inventory are infinite to represent sales being closed.

This is a reduced state-transition model, not a disabled parameter in the previous
research model. The removed mechanisms have no inputs, state, branches or helper
imports in the three workshop notebooks or their generated package.

Expected revenues are computed directly, not estimated from sampled trajectories.
The workshop does not run the former simulation and evaluation notebooks.

### Execution and validation

Notebook 01 generates a fresh, isolated directory from an explicit allowlist;
only Notebooks 02 and 03 and their required inputs are copied. Those notebooks
require the `pricing-workshop-v1` runtime marker to avoid using legacy model files.

The pricing tests execute the function defined in Notebook 03. Independent checks
cover a single-period calculation and a small recursive decision tree, along with
zero demand, zero capacity, tie handling and invalid probabilities. Workshop input
checks ensure only three parameter files are produced and no legacy modules are
copied. Tests depend only on the current pricing workshop.

The three notebooks are executed from a clean source-only staging directory. The
saved results in `runs/pricing-workshop/` include the scenario, runtime config,
price/value tables, four figures and an execution report. The former simulation
code, tests, models, results and analysis reports have been removed.

## Tests

```bash
uv run --locked python -m unittest discover -s tests -v
```

Tests check the teaching notebook's pricing function against independent small
problems, input validation, workspace isolation and the three-notebook contract.
