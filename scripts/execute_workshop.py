"""Execute all three notebooks in a fresh, synthetic-only teaching directory."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpec

ROOT = Path(__file__).resolve().parents[1]
ENV_FILES = ('requirements.txt', 'pyproject.toml', 'uv.lock', '.python-version')

NOTEBOOK_FILES = (
    '01_synthetic_scenario_setup.ipynb',
    '02_scenario_distributions.ipynb',
    '03_estimate_optimized_price_table.ipynb',
)


def stage_sources(output, source_root=ROOT):
    """Copy only reviewed teaching sources; never sweep in adjacent files."""
    for name in (*ENV_FILES, 'python/synthetic.py', 'scenarios/synthetic_demo.yaml'):
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_root / name, destination)
    for name in NOTEBOOK_FILES:
        notebook = nbformat.read(source_root / name, as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        nbformat.write(notebook, output / name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'workshop-run-verified')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    stage_sources(output)
    report = []
    for number in (1, 2, 3):
        directory = output if number == 1 else output / 'workshop-run'
        path = next(directory.glob(f'{number:02d}_*.ipynb'))
        notebook = nbformat.read(path, as_version=4)
        # Use the exact uv interpreter, without changing the user's kernelspecs.
        manager = KernelManager(kernel_name='python3')
        manager._kernel_spec = KernelSpec(
            argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            display_name='Python 3', language='python')
        start = time.monotonic()
        try:
            NotebookClient(notebook, km=manager, timeout=300,
                           resources={'metadata': {'path': str(directory)}}).execute()
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
            manager.cleanup_resources()
        nbformat.write(notebook, path)
        report.append({'notebook': str(path.relative_to(output)),
                       'seconds': round(time.monotonic() - start, 2)})
    (output / 'execution-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'Executed all notebooks. Open {output}/workshop-run/03_estimate_optimized_price_table.ipynb')


if __name__ == '__main__':
    main()
