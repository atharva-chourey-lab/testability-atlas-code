# Testability Atlas — Code

**Code for the Testability Atlas: a question-level grading of Indian historical
statistics — of 23 gradeable questions, only 4 are testable with surviving
data, 11 are underpowered, and 8 are untestable.**

Manuscript: https://github.com/atharva-chourey-lab/testability-atlas

## What this code does

- `scripts/atlas.py` — the Atlas computation, exactly as registered in
  `ATLAS_PREREGISTRATION.md`: spectral minimum-detectable-effect-size (MDES)
  tests with AR(1) surrogates, regression MDES, and the structural span rule,
  applied question-by-question. Outputs `data/atlas_grid.csv` (the 23 graded
  questions), `data/atlas_summary.json` (the 4 / 11 / 8 split) and the Atlas
  figures.
- `scripts/analysis.py` — the supporting series analyses (band tests and
  audits in `data/results_*.csv`, `data/series_audit.csv`).
- `scripts/fetch_data.py` — fetches the public source series (IMD/IITM rainfall,
  IIP) whose snapshots are committed under `data/`.

The method follows Ioannidis, Stanley & Doucouliagos (2017); the claim is the
first question-level grading scoped to Indian historical statistics, not the
method itself. `ATLAS.md` is the full report; `REPORT.md` and `ASSESSMENT.md`
record the earlier feasibility work.

## How to run

```bash
python3 scripts/atlas.py    # needs numpy, pandas, matplotlib
```

The spectral MDES step is simulation-based (2,000 surrogates per registered
test, fixed seeds 42/43) and takes a few minutes.

## Data

All data under `data/` are public Indian government / IMD-IITM series or the
lab's own computed outputs, and are included. Large raw snapshots (the raw IIP
JSON pull) are not needed to reproduce the Atlas and are not committed.

## Status

Research code as run for the manuscript — a single registered analysis, not a
general power-analysis package.

## Authorship and licence

**Author:** Atharva Chourey, Atharva Chourey Lab (independent research lab)

The Atharva Chourey Lab is a human–AI collaboration: Atharva Chourey works with
Lapis (Muse), an AI research partner. All results are framed as the
collaboration's.

Code in this repository is released under the **MIT License** (see `LICENSE`).
The associated manuscripts are published separately under CC BY 4.0 — the code
licence and the paper licence are deliberately different.
