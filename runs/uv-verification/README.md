# uv environment verification

Verified on 2026-11-08 on macOS arm64. See [validation.json](validation.json)
for versions, notebook execution times and checks.

- All nine unit tests passed.
- All three notebooks executed successfully with the Python interpreter selected by uv.
- The default scenario produced 2,013 price/value rows and four figures.
- Every price/value table entry matches the historical pricing-workshop result
  within `rtol=1e-12`, `atol=1e-9`.
- pip-audit checked 120 installed packages, including the audit tools, and found
  no known vulnerabilities on the verification date. This is not a safety guarantee.
- The skill metadata validator passed.

Follow the repository-root [SKILL.md](../../SKILL.md) to reproduce this check.
Executed notebooks are saved in the ignored local `workshop-run-review/` directory:
Notebook 01 is at its root; executed Notebooks 02 and 03, CSV and figures are in
its `workshop-run/` child. The earlier committed `runs/pricing-workshop/` snapshot
and root notebook outputs remain historical records, not outputs of this run.
