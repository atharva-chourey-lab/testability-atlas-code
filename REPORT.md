# India Government Data — Patterns & Deviations: Pilot Report

**Date:** 2026-11-17 · **Status:** local pilot, nothing published · **Pre-registration:** `PREREGISTRATION.md`, committed (git `e7dfab9`) before any data was downloaded or analysed. Re-running `scripts/fetch_data.py` then `scripts/analysis.py` regenerates every number below.

## 0. Scope, sources, licences — and the novelty scrub

**Data that actually landed** (details + licences in `data/README.md`):

| Series | Source | Span | n |
|---|---|---|---|
| All-India + 4 homogeneous regions, JJAS rainfall (mm) | IMD Pune (operational series) | 1901–2026 in source; analysed 1901–2025 | 125 |
| All-India + 30 subdivisions, JJAS rainfall (mm) | IITM Pune homogeneous series (IMD observations) | 1871–2016 | 146 |
| IIP General index, monthly | MoSPI eSankhyiki API, base 2011-12 | Apr 2012–Mar 2026 | 168, 0 missing |

Failed routes are recorded in `data/README.md` (data.gov.in file fetch failed from this host; MoSPI CPI endpoint serves only a latest-year slice without undocumented filters; the `mospi-esankhyiki` package's metadata route failed via proxy — the same API was used directly).

### Prior work — read this before any headline

A novelty scrub against the live literature (2026-11-17) is unambiguous: **the headline candidates in this pilot are already in the public domain.**

- **Monsoon spectral analysis is done.** Kane (1990) ran Maximum Entropy Spectral Analysis on 29 Indian subdivisions (1871–1970/86) and reported a QBO (2–3 yr) signal everywhere, ~11 yr (sunspot) and ~22 yr (Hale) signals in some subdivisions, and a one-sided ENSO relationship. Schaefer & Domroes (1996) did all-India spectral analysis with ENSO/QBO/solar forcings.
- **Indian industrial-cycle spectral analysis is done.** Bose & Goyal (IGIDR Working Paper 2020-033) analysed disaggregated Indian industrial cycles spectrally, including spectral causality from policy parameters.
- **Political budget cycles in India are done** (by regression, not spectra): Khemani (J. Dev. Econ. 2004), 14 major states 1960–1996 — election-year effects on commodity taxes (down), investment spending (up), roads (large up), deficits (no effect); Khemani (2002/2007) — states aligned with the centre ran ~10% higher deficits. State convergence/divergence is likewise a crowded literature (sigma divergence; conditional-only beta convergence).

**Consequence for framing:** H1 and H2 below are **replication / benchmark runs** — the older series extended toward the present and re-tested under one uniform, pre-registered red-noise method. That is a useful check. It is **not** a discovery claim, and no novelty is claimed for either. The genuinely open ground, if any, is in §5 (scouting).

## 1. Methods (as registered)

- Spectrum: Hann-tapered periodogram of the demeaned, linear-detrended series, on an 8× zero-padded FFT grid (interpolation only — no added information — applied identically to real series and surrogates, so narrow bands always contain grid points).
- Null: 2,000 AR(1) surrogates per series (ρ and σ from the preprocessed series; seed 42), each detrended identically. Band statistic = **maximum** power inside the band; verdict **supported** iff empirical p < 0.05.
- Bands — H1: ENSO 2–7 yr, Solar 9.5–12.5 yr, Long 17–21 yr. H2: Kitchin 36–60 months, Juglar 84–132 months.
- R/S Hurst: classic rescaled range, secondary only. As a post-registered bias check (labelled exploratory), each H was also benchmarked against 200 same-ρ AR(1) surrogates, because classic R/S is upward-biased at these lengths.
- Sensitivity checks: Welch spectra (All-India IMD); IITM series as a second ruler for H1; All-India including the source's 2026 row.

## 2. H1 — Monsoon cycles: NOT SUPPORTED in any band, in any series (replication run)

Primary series — **IMD All-India JJAS, 1901–2025** (mean 888.0 mm, sd 86.5; driest 1972, 674.4 mm; wettest 1917, 1,099.8 mm; lag-1 autocorrelation of the detrended series ρ ≈ 0.03 — the series is close to serially uncorrelated):

| Band | Peak period | p | Verdict |
|---|---|---|---|
| ENSO 2–7 yr | 2.77 yr | 0.60 | not supported |
| Solar 9.5–12.5 yr | 12.20 yr | 0.34 | not supported |
| Long 17–21 yr | 17.24 yr | 0.27 | not supported |

The same test on the other four IMD regions, on IITM All-India (1871–2016), and on four contrasting IITM subdivisions (Coastal Karnataka, West Rajasthan, East Madhya Pradesh, Assam & Meghalaya) gives **30 of 30 band tests not supported** (full table: `data/results_band_tests.csv`). The closest calls anywhere are Central India solar (peak 11.9 yr, p = 0.12) and West Rajasthan long (peak 17.2 yr, p = 0.12) — neither approaches the registered threshold. Including the 2026 row, and the Welch sensitivity (p = 0.22 / 0.42 / 0.42), change no verdict.

**Reading, carefully:** under a uniform periodogram + AR(1)-null test, JJAS *seasonal totals* carry no significant periodic power at the claimed bands; the spectra are essentially flat. This does **not** refute Kane (1990) on his own terms — his claims rest on Maximum Entropy spectra (much sharper peak resolution), largely annual rather than JJAS-total data, and spans ending 1970/86. What the pilot establishes is narrower and still worth having on record: the claimed cycles do not survive a conservative, uniform, pre-registered test on the extended series, and any future claim of a monsoon cycle should have to state its method and clear a red-noise null. Correlation-with-ENSO indices (a regression question) is untouched by this test and is not claimed either way.

**Secondary checks:**
- **R/S Hurst:** IMD All-India H = 0.75; IITM All-India H = 0.67. Benchmarked against same-ρ surrogates (means 0.63 / 0.58), the IITM value is unremarkable (p = 0.11) but the IMD value sits above its surrogate 95th percentile (p = 0.025). Given classic R/S bias and that the two series are built differently (below), this is recorded as a **flagged discrepancy between two official series**, not as evidence of long memory in the monsoon itself.
- **Two rulers, one monsoon:** over the identical years 1901–2016, IMD's All-India JJAS mean is **887.3 mm** and IITM's is **843.6 mm** — a systematic ~44 mm (≈5%) level gap; year-to-year the two correlate at r = 0.95 with mean absolute difference 43.9 mm. The gap is construction (306-station homogeneous network vs IMD's operational subdivisional weighting), not an error by either — but any pattern claim about "the" Indian monsoon inherits whichever ruler produced it. (Figure: `figures/fig_monsoon_series.png`.)

Figures: `figures/fig_h1_allindia_imd.png`, `fig_h1_regions_imd.png`, `fig_h1_subdivisions_iitm.png`.

## 3. H2 — Macro cycles in IIP: NOT SUPPORTED in either band (replication run)

Series chosen under the registered rule: **IIP General index (base 2011-12), monthly, Apr 2012–Mar 2026, n = 168, no missing months**, from the MoSPI API (CPI was attempted first-class and failed on endpoint behaviour — see `data/README.md`; bank credit via RBI DBIE was not needed once IIP satisfied the rule). Analysed as log-growth, deseasonalised by calendar-month means, detrended (n = 167).

| Band | Peak period | p | Verdict |
|---|---|---|---|
| Kitchin 3–5 yr | 36.1 months | 0.93 | not supported |
| Juglar 7–11 yr | 89.1 months | 0.94 | not supported |

**Caveats, stated plainly:** (1) Power is low — 14 years contains ~3 Kitchin cycles and under 2 Juglar cycles; "not supported" here means *no detectable periodic power in this window*, not that Indian industry has no cycle dynamics (Bose & Goyal's disaggregated work, on longer/different constructions, is the standing literature). (2) The window contains the COVID collapse and rebound — Apr 2020 log-growth −77.5 points, May 2020 +51.3 — a single event that dominates the growth series' variance and flattens any spectrum. A full build should pre-register an outlier treatment before touching longer spliced series. Figure: `figures/fig_h2_iip.png`.

## 4. H3 — Political frequency: UNTESTABLE in this pilot (as registered)

The registration predicted this verdict and the scouting confirms it. Annual state-finance series of 30–40 points cannot resolve a 5-year spectral peak (too few cycles; detrending eats the target band). Scouting for the data that *would* be needed — a long monthly/quarterly fiscal series — found: CGA publishes monthly Union Government accounts and data.gov.in hosts recent monthly fiscal datasets, but **no openly downloadable multi-decade monthly/quarterly fiscal archive** was found; RBI's State Finances is annual. **No spectral verdict on H3 is forced.** Note also (§0) that the substance of Indian political budget cycles is already published by regression (Khemani) — a spectral version would be a methods variation, not an open question.

## 5. Scouting — where is the unaudited seam? (no analysis forced)

Ranked by seam quality: is the quantity load-bearing, does an independent comparator exist, and is the seam actually unaudited?

### (ii) Revision patterns — RECOMMENDED for the full build — rank 1
India publishes first-release GDP, IIP and CPI numbers that move budgets, markets and headlines, then revises them — and there is **no public vintage database** (no Indian ALFRED): first-release values survive only scattered across years of press-release PDFs. Nobody has systematised, across series, the direction and size of revisions by period/regime.
- *Obtainable?* Yes, with labour: MoSPI/NSO press notes (IIP/CPI monthly, GDP quarterly/annual) are public; the work is extraction, not access.
- *Comparator?* Built in — the final revised value is the comparator for every first release.
- *Unaudited?* The RBI and others have published occasional single-series revision studies, but no unified, public, cross-series revision dataset with regime splits exists. The deliverable is the dataset itself — the same move as this lab's famine panel.
- *Pilot evidence the seam is real:* §2's two monsoon rulers — a 5% level gap and a Hurst disagreement produced purely by series construction. Ruler-choice and revision are live properties of Indian official data, not hypotheticals.

### (i) "Two rulers" for the same quantity — rank 2
Unemployment is the flagship case: PLFS (official, open via MoSPI), EPFO payroll additions (official, monthly reports since 2018), CMIE (the third ruler — but proprietary, which blocks fully open replication). The gaps between rulers are widely *debated*, so the seam is not unaudited in commentary; what does not exist publicly is an aligned, like-for-like dataset with the definitional differences coded. Strong, but the CMIE paywall and the crowded debate lower it below (ii).

### (iii) Post-2014 digital-era series — rank 3
UPI volumes (NPCI, open, 2016–), GST collections (monthly PIB releases, 2017–), FASTag, electricity generation (CEA/POSOCO): genuinely un-cycle-testable before now and largely unsystematised. But spans are ~9–10 years of monthly data (~110 points): under two Juglar cycles, Kitchin barely — spectral work is weak tea today. Better framed, later, as seasonality/deviation studies (festival calendars, COVID shock, adoption curves) than as cycle tests.

**Recommendation: build (ii)** — an open Indian data-vintages archive (first release vs each revision vs final, for IIP, CPI and GDP), with revision direction/size by period as the first analysis. It is load-bearing, self-comparing, unaudited as a system, and it is a dataset other researchers would have to cite.

## 6. What a full build would need

1. The vintages archive (seam ii): press-release back-files, an extraction pipeline, and a pre-registration for revision statistics before analysis.
2. For H1 replication to be conclusive against Kane on his own terms: a registered MESA arm alongside the periodogram arm, on annual *and* JJAS totals.
3. For H2: a longer macro span (spliced IIP bases or RBI Handbook credit series) with a pre-registered COVID/outlier rule.
4. For H3: nothing until a multi-decade monthly/quarterly fiscal series exists openly — parked, by design.

## Files

- `PREREGISTRATION.md` — registered before the pull (git `e7dfab9`)
- `scripts/fetch_data.py`, `scripts/analysis.py` — re-runnable end to end
- `data/` — raw + tidy data, `results_band_tests.csv` (all 32 band tests), `results_extra.json`, `README.md` (provenance/licences/failures)
- `figures/` — `fig_h1_allindia_imd.png`, `fig_h1_regions_imd.png`, `fig_h1_subdivisions_iitm.png`, `fig_h2_iip.png`, `fig_monsoon_series.png`

*Language discipline, per registration: every statement above is about pattern in a sample under a stated method. Nothing here is a causal claim.*
