---
name: hotel-pricing-workshop
description: Set up this hotel revenue management workshop with uv, execute all three synthetic pricing notebooks, inspect saved results in local JupyterLab, and update and audit the locked dependencies. Use when preparing, running, or verifying this repository's workshop.
---

# Run the hotel pricing workshop

Run commands from the repository root. Use only the invented scenario in
`scenarios/synthetic_demo.yaml`. No client CSV files are needed.

## 1. Install uv and the locked environment

Use [Astral's official installer](https://docs.astral.sh/uv/getting-started/installation/).
On macOS/Linux, download and inspect the versioned installer before executing it:

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://astral.sh/uv/0.13.7/install.sh -o /tmp/workshop-uv-install.sh
less /tmp/workshop-uv-install.sh
UV_INSTALL_DIR="$PWD/.tools/uv" UV_NO_MODIFY_PATH=1 sh /tmp/workshop-uv-install.sh
export PATH="$PWD/.tools/uv:$PATH"
uv --version
uv python install
uv sync --locked --group audit
```

The installer does not modify shell profiles. `.tools/` and `.venv/` are ignored.
Python is pinned in `.python-version` (3.14.10); `uv.lock` fixes direct and
transitive versions and distribution hashes. The initial verified stack includes
NumPy 2.5.4, pandas 3.1.1, SciPy 1.18.1, Matplotlib 3.11.2 and JupyterLab 4.6.6.
Do not bypass TLS verification if installation fails: repair the certificate trust
configuration or use an approved network. See [uv projects](https://docs.astral.sh/uv/guides/projects/).

## 2. Verify and execute all notebooks

```bash
uv run --locked --group audit python -m unittest discover -s tests -v
uv run --locked --group audit pip-audit --local
uv run --locked python scripts/execute_workshop.py --output workshop-run-verified
```

The runner refuses to overwrite an existing directory. Choose a new
`workshop-run-*` name on subsequent runs and use it in the commands below.
It copies an allowlist of synthetic teaching inputs, runs Notebook 01 there,
then runs 02 and 03 inside the generated `workshop-run/` child directory.
Each kernel uses the same Python interpreter as uv. Execution stops on any error;
outputs are saved to the notebooks, with durations in `execution-report.json`.
The original source notebooks and historical `runs/pricing-workshop/` snapshot
are not modified. Expected results in the child directory:

- `result/price_tables.csv`: 2,013 rows for the default scenario.
- `fig/distributions/`: two distribution figures.
- `fig/pricing/`: two price comparison figures.
- `model/`: three generated input files and two calculated price/value files.

Notebook 01 creates a new child directory: rerunning it requires a new output
folder. For manual setup instead, run `uv run --locked python scripts/prepare_synthetic.py
--output workshop-run-manual` on one line; open 02 and 03 inside that directory.
Generated workspaces include `pyproject.toml`, `uv.lock`, `.python-version` and
exported `requirements.txt`, so recipients can run `uv sync --locked` there.

## 3. Leave JupyterLab running for inspection

```bash
uv run --locked jupyter lab --no-browser --ServerApp.ip=127.0.0.1 --ServerApp.port=8888 --ServerApp.port_retries=0 --ServerApp.root_dir="$PWD/workshop-run-verified"
```

Keep this terminal/process running. Open the token-bearing localhost URL printed
by Jupyter in your browser, then open `01_synthetic_scenario_setup.ipynb` for the
setup output and **`workshop-run/02_scenario_distributions.ipynb`** and
**`workshop-run/03_estimate_optimized_price_table.ipynb`** for the executed analyses.
The root copies of 02/03 are templates; their executed copies are in the child.
If port 8888 is occupied, choose another unused port explicitly. To stop later,
press Ctrl-C in the server terminal and confirm shutdown.

Keep default token authentication enabled and bind only to `127.0.0.1`.
Do not serve the repository root: its Git history still contains private research data. Never commit server tokens, runtime files or logs; `.jupyter-local/`
is ignored if local process records are needed. A localhost server is for the
operator's computer, not classroom network sharing. See [Jupyter security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html).
Only execute reviewed notebook code and load pickle inputs generated locally by
this workflow; pickle loading can execute code. Share the generated synthetic
workspace rather than the repository or an authenticated server URL.

## 4. Maintain current dependencies

Use the lock for normal runs; update intentionally on a new branch before an
event, rather than silently upgrading during a session:

```bash
uv lock --upgrade
uv sync --locked --group audit
uv export --locked --no-dev --format requirements-txt --output-file requirements.txt
uv run --locked --group audit python -m unittest discover -s tests -v
uv run --locked --group audit pip-audit --local
uv run --locked python scripts/execute_workshop.py --output workshop-run-upgrade
```

Review changes to `pyproject.toml`, `uv.lock` and the generated requirements together.
For a Python patch update, install and pin the new patch explicitly and repeat
these checks. For a new Python minor, also update `requires-python` after checking
scientific package compatibility. Update the versioned uv installer above when
adopting a newer uv release. Do not hand-edit `requirements.txt`.
[pip-audit](https://pypi.org/project/pip-audit/) checks published advisories for the
installed environment; a clean result is not a guarantee of safety. Investigate
findings and upgrade affected dependencies before distribution; do not hide
failures with blanket exclusions. Record the audit date, versions, execution
results and any remaining findings in the PR.
