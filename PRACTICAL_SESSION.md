# Practical session: build and compare optimal hotel prices

[日本語](PRACTICAL_SESSION_JP.md)

Work through the steps in order. First run the default scenario, then change one
assumption and run it again. Compare the resulting price tables.

Keep this guide open in GitHub or a separate browser tab while using JupyterLab.
Detailed explanations stay in the notebooks and the [README](README.md).

## 1. Prepare your files and open JupyterLab

Download and extract the workshop source ZIP supplied by your instructor, or use
your authorised repository checkout. Open a terminal in the folder containing
`01_synthetic_scenario_setup.ipynb` and `pyproject.toml`.

If uv is not installed, follow [Install uv and the locked environment](SKILL.md#1-install-uv-and-the-locked-environment),
then return here. You do not need to run the automated notebook-execution steps
in SKILL.md for this practical session.

Run these commands from the source folder:

```bash
uv sync --locked
uv run --locked python -c "from pathlib import Path; from scripts.execute_workshop import stage_sources; p = Path('workshop-run-student'); p.mkdir(); stage_sources(p)"
uv run --locked jupyter lab --no-browser --ServerApp.ip=127.0.0.1 --ServerApp.port=8888 --ServerApp.port_retries=0 --ServerApp.root_dir="$PWD/workshop-run-student"
```

The second command creates a fresh teaching folder with only the required source
files. If `workshop-run-student` already exists, choose a new name in both commands;
do not remove a folder containing results you want to keep. These terminal commands
use macOS/Linux shell syntax; Windows users can run them in WSL.

Open the full localhost URL printed by Jupyter, including `?token=...`, in your
browser. Keep the terminal running. If port 8888 is in use, choose another unused
port in the last command. You should see three notebooks and the `scenarios/` folder.

For file roles, see [Repository structure and file roles](README.md#repository-structure-and-file-roles).

## 2. Create the baseline experiment with Notebook 01

1. Open `01_synthetic_scenario_setup.ipynb` in JupyterLab.
2. Keep `scenario_path = Path('scenarios/synthetic_demo.yaml')` unchanged.
3. In the final code cell, change the output folder to:

   ```python
   output_folder = Path('workshop-run-baseline')
   ```

4. Select **Run → Run All Cells**. Wait until the code cells finish.
5. Check the displayed scenario: capacity **10**, expected potential arrivals
   **18**, WTP mean **18,000**, WTP standard deviation **6,000**, and demand
   multipliers **0.6, 1.0, 1.2**.
6. Check that the final message names `workshop-run-baseline`.

If a cell fails, stop and resolve the error before continuing. If the output
folder already exists, choose a new output folder name and use that name in the
following steps. Each experiment needs a fresh folder.

For the meaning of each setting, see [Inputs](README.md#inputs).

## 3. Inspect the baseline distributions with Notebook 02

1. In JupyterLab's file browser, open **`workshop-run-baseline/`**.
2. Open `02_scenario_distributions.ipynb` **inside that folder**.
3. Select **Run → Run All Cells** and wait for completion.
4. Find the WTP density and purchase-probability plots.
5. Find the arrival-timing and daily arrival-probability plots. Confirm that the
   three demand levels appear.
6. Save the notebook with **File → Save Notebook**.

Use the notebook's explanations as needed. For the model assumptions, see
[Pricing workshop model](README.md#pricing-workshop-model).

## 4. Calculate and inspect the baseline prices with Notebook 03

1. In the same **`workshop-run-baseline/`** folder, open
   `03_estimate_optimized_price_table.ipynb`.
2. Select **Run → Run All Cells** and wait for completion.
3. Go to **Compare price tables on the same colour scale**.
4. Inspect the heatmaps, then the numerical tables below them. Table prices are
   rounded to whole currency units; `Closed` means no rooms remain.
5. In each demand table, find the row **30 days before check-in** and the column
   **5 remaining rooms**. Compare the prices at demand multipliers 0.6, 1.0 and 1.2.
6. Record the price for **Demand x 1** in the comparison table below.
7. Save the notebook. Keep this baseline notebook open for comparison.

Leave `remaining_rooms` unchanged. The later discussion and partner prompts are
optional reading, not tasks in this session. Continue directly to the next step.

For the calculation, see [Optimal pricing](README.md#optimal-pricing).
For the saved tables and figures, see [Outputs and interpretation](README.md#outputs-and-interpretation).

| Experiment | WTP mean | Demand multiplier | Days before check-in | Remaining rooms | Observed optimal price |
| --- | ---: | ---: | ---: | ---: | --- |
| Baseline | 18,000 | 1.0 | 30 | 5 | Fill in after Step 4 |
| Higher WTP | 21,000 | 1.0 | 30 | 5 | Fill in after Step 6 |
| Lower WTP (optional) | 15,000 | 1.0 | 30 | 5 | Fill in after Step 7 |

Record these values in your own notes; you do not need to edit this guide.
A discrete price grid means some cells may stay the same after an input changes.

## 5. Change one assumption and create a new experiment

1. Return to the top level of the JupyterLab file browser, then open
   **`scenarios/synthetic_demo.yaml`** in the text editor.
2. Change only the WTP mean from 18,000 to 21,000. This part should read:

   ```yaml
   wtp:
     mean: 21000
     std: 6000
   ```

3. Save the YAML file. Keep capacity, arrivals, price grid and all other settings
   unchanged so you can isolate the effect of WTP.
4. Return to **Notebook 01 at the top level**. Keep `scenario_path` unchanged and
   change its final code cell to:

   ```python
   output_folder = Path('workshop-run-high-wtp')
   ```

5. Select **Run → Run All Cells**. Check that the displayed mean is **21,000** and
   the final message names `workshop-run-high-wtp`.

Edit the source YAML in `scenarios/`, not the `scenario.yaml` snapshot inside
an existing experiment. Editing a snapshot or rerunning 03 alone does not
regenerate its inputs. See [Generated workspace versus saved results](README.md#generated-workspace-versus-saved-results).

## 6. Run the changed scenario and compare

1. Open **`workshop-run-high-wtp/02_scenario_distributions.ipynb`**.
2. Run all cells. Check how the WTP plots changed; the arrival settings are unchanged.
3. Open **`workshop-run-high-wtp/03_estimate_optimized_price_table.ipynb`**.
4. Run all cells and return to **Compare price tables on the same colour scale**.
5. Find **Demand x 1**, row **30**, column **5** and record its price alongside
   the baseline value.
6. Compare other cells in the two **Demand x 1** tables, keeping the same row and
   column when comparing. Look for cells where the price increased or stayed the same.
7. Save both notebooks. The baseline results are still in `workshop-run-baseline/`.

The same price grid is used in both experiments, so their heatmaps also share
the same colour limits. Use the numerical tables to check the exact prices.

## 7. Try a lower WTP mean (optional)

Repeat Steps 5–6 with only these substitutions:

- Set `wtp.mean` to **15000** in `scenarios/synthetic_demo.yaml` and save it.
- In Notebook 01, set `output_folder = Path('workshop-run-low-wtp')`.
- Run Notebook 01, then 02 and 03 **inside `workshop-run-low-wtp/`**.
- Record the price at the same demand multiplier, day and inventory, then compare
  all three experiments.

You now have separate, saved price tables for each experiment. To explore further,
change one setting at a time and repeat this same sequence with a new folder name.

## 8. Finish

Save your notebooks. Keep the experiment folders if you want to inspect the results
later. When finished, return to the terminal running JupyterLab, press **Ctrl-C**,
and confirm shutdown if asked.
