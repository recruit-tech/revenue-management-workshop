"""Create an isolated workshop directory from invented scenario parameters."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from python.synthetic import prepare_workspace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', type=Path, default=ROOT / 'scenarios/synthetic_demo.yaml')
    parser.add_argument('--output', type=Path, default=ROOT / 'workshop-run')
    args = parser.parse_args()
    output = prepare_workspace(args.scenario, args.output)
    print(f'Created {output}. Open its Notebooks 02–03 and run them in order.')


if __name__ == '__main__':
    main()
