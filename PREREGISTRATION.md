# Pre-registration — India Government Data: Patterns & Deviations (Pilot)

**Registered:** 2026-11-17 (America/Los_Angeles)
**Status at registration:** No data for this project has been downloaded, inspected, or analysed yet. This file is committed to a local git repository before any data pull. Any later change to hypotheses, bands, or decision rules must be made in a new dated commit and labelled as a revision, never silently edited into this version.
**Scope:** Local pilot only. Nothing is to be posted or published publicly under this registration.

## Question

Modern Indian government statistics are long, public, and largely unexamined with the
frequency-domain toolkit. Do the headline series actually contain the cycles that
socioeconomic and political theories claim they contain — and where they deviate
from those claims, are the deviations systematic?

The toolkit is described on its own terms, as standard methods, with no attribution
of the method to any single author:

- **Spectral analysis** (periodogram / Welch estimates) of a series against an
  AR(1) red-noise null, in the Granger/Hatanaka tradition of spectral analysis of
  economic time series.
- **Cross-spectral coherence** between paired series, where a genuine pair exists.
- **R/S (rescaled-range) analysis** and the Hurst exponent, in the Mandelbrot
  tradition, as a secondary check for long memory.

## Guardrail (registered in advance)

Granger's "typical spectral shape" warning is the load-bearing discipline of this
project: most economic (and many climatic) series have spectra that simply decay
with frequency — red, with no peak. **A spectrum with no significant peak is a
result, not a failure.** No peak will be reported as a "cycle" unless it clears the
red-noise test below. Eyeballing a wavy line and naming a period is banned.

## Decision rules (fixed)

For each tested series:

1. Preprocessing, declared per hypothesis below, is applied identically to the
   real series and to every surrogate.
2. Fit an AR(1) model to the preprocessed series (lag-1 autocorrelation ρ).
3. Simulate 2,000 AR(1) surrogates of the same length with that ρ and the same
   variance (fixed RNG seed: 42). Compute the same spectral estimate for each.
4. For each pre-declared band, the test statistic is the **maximum** spectral power
   inside the band (using the band maximum, not a single frequency, controls for
   picking the luckiest frequency inside the band).
5. A band is **supported** iff the real band maximum exceeds the 95th percentile
   of the surrogate band maxima (one-sided p < 0.05). Otherwise it is
   **not supported**. Borderline results are reported with their exact p-value;
   there is no "trend toward significance" verdict.
6. R/S Hurst: classic rescaled-range slope over window sizes from 8 to n/2 on a
   log–log plot. Reported as a secondary descriptive check only; H materially
   above 0.5 is *consistent with* long memory, it is not by itself proof of any
   cycle or mechanism. Known small-sample upward bias of classic R/S is stated
   wherever H is reported.

## H1 — Monsoon cycles

- **Series:** All-India South-West monsoon (June–September) rainfall, annual,
  longest openly obtainable IMD series (target 1901–present; the actual span
  obtained is reported, and no span is claimed that the file does not cover).
  Plus at least 3 contrasting meteorological subdivisions/regions from the same
  source, chosen for climatic contrast (e.g. a wet west-coast, an arid north-west,
  and a central/eastern subdivision) — the same band tests run on each.
- **Preprocessing:** annual seasonal (JJAS) totals; demean and linear-detrend.
  Primary spectrum: periodogram with a Hann taper. Welch estimate as sensitivity
  only (segments are short at this n).
- **Bands (periods, years):**
  - ENSO band: 2.0–7.0 yr (note: 2 yr is the Nyquist limit of annual data; power
    at the lowest edge is interpreted with that caution).
  - Solar band: 9.5–12.5 yr (the "~11-year" claim).
  - Long band: 17–21 yr (the "~18–20-year" claim).
- **Verdict per band:** supported / not supported, per the decision rules above,
  separately for All-India and for each subdivision. A band supported in a
  subdivision but not All-India (or vice versa) is reported exactly that way.

## H2 — Macro cycles

- **Series:** ONE monthly Indian macro series, chosen after the pull by this
  fixed rule: among {Index of Industrial Production, scheduled commercial bank
  credit (non-food), CPI or food CPI} take the longest openly obtainable series
  with <5% missing months and no login/paywall; tie-break in the order listed.
  The choice and its reason are recorded in REPORT.md.
- **Preprocessing:** if the series is a positive level/index, work in log
  differences (monthly growth / inflation); remove calendar-month means
  (deseasonalise); demean and linear-detrend the result. If the obtainable series
  is already a growth rate, demean/detrend only.
- **Bands (periods):** Kitchin 3–5 yr (36–60 months); Juglar 7–11 yr
  (84–132 months). Same surrogate decision rules as H1, applied at monthly
  frequency.
- **Verdict per band:** supported / not supported. A supported band is a statement
  about periodic power in that series over that span — not evidence for any
  particular inventory/investment mechanism.

## H3 — Political frequency (SCOUT ONLY in this pilot)

- **Claim scouted:** a ~5-year election-frequency peak in fiscal series
  (spending / deficit pulses tied to the electoral cycle).
- **Resolution problem, declared upfront:** annual state-finance series of
  30–40 points cannot credibly resolve a 5-year spectral peak — too few cycles,
  too few frequency bins near the target, and detrending eats exactly that band.
  The expected verdict is **UNTESTABLE at annual frequency**.
- **Pilot task:** record what data *would* be needed (a long quarterly or monthly
  fiscal series, e.g. monthly state/centre fiscal accounts over several decades),
  check whether such a series is openly obtainable, and stop there.
  **No spectral verdict on H3 will be forced from annual data.**

## Cross-spectral (exploratory only)

If, in the course of the H1/H2 pulls, a genuine paired series is obtained
(e.g. monsoon rainfall paired with an agricultural output series over a common
span), coherence at the H1 bands may be computed and reported as **exploratory**,
clearly labelled, with no supported/not-supported verdict attached in this pilot.

## Claim discipline

- No "first ever" / "first digitisation" claim without an explicit literature check, which this pilot does not perform — so no such claim is made in this pilot.
- Every value carries its source and licence; a source that fails is recorded as failed, never replaced by an invented or remembered number.
- Every deviation/pattern is reported with its n, span, and method.
- Correlation ≠ causation, in language throughout: spectral power, coherence, and Hurst exponents are statements about pattern in a sample, never about mechanism.
- Deviations from a theory's prediction are reported with the same prominence as confirmations.

## Deliverables of the pilot

- `data/` — pulled files, each with provenance + licence noted (in REPORT.md and/or a data README).
- `scripts/` — re-runnable Python that regenerates the data tables, figures, and the numbers quoted in the report.
- `figures/` — PNG spectra (real series vs red-noise band envelope) for H1 and H2.
- `REPORT.md` — scope/sources/licences first, methods as registered here, per-hypothesis verdicts with actual numbers, honest gaps, and what a full build would need.
