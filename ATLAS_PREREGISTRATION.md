# Pre-registration — The Testability Atlas (Build A)

**Registered:** 2026-11-17 (America/Los_Angeles)
**Status at registration:** No new data has been pulled for this build. The only numbers in
hand are the pilot's (`REPORT.md`, git `171929d`): IMD/IITM monsoon series, MoSPI IIP
(base 2011-12), and the pilot's band-test results. Series metadata and literature effect
sizes cited below were verified against public sources on 2026-11-17 *for this
registration* (sources in §7); no series values beyond the pilot's have been inspected.
Any later change to the grid, machinery, anchors, or thresholds must be made in a new
dated commit labelled as a revision, never silently edited into this version.
**Scope:** Local only. Nothing is to be posted or published publicly under this registration.
**Governing spec:** `ASSESSMENT.md` §A and §F (the Atlas is Build A, ranked 1 there).

## 0. The claim and the language rule

The Atlas grades **rulers, not theories**. Every verdict is a statement of the form:
*"on the clean (single-base / single-method) span of this Indian official series, a test
of this theory could / could barely / could not detect an effect of the size the
literature treats as meaningful."* A verdict of UNTESTABLE is **not** evidence against
the theory; a verdict of TESTABLE is **not** evidence for it. This wording discipline
applies to every cell, table, and figure caption in `ATLAS.md`.

## 1. The grid (fixed)

**Rows — series (10):**

| # | Series | Ruler / source | Frequency used |
|---|---|---|---|
| S1 | Monsoon rainfall (JJAS, All-India) | IMD Pune operational **and** IITM homogeneous — two rulers, graded jointly, both reported | Annual |
| S2 | GDP & national accounts (incl. state GSDP) | NSO/MoSPI | Quarterly (national); annual (GSDP panel) |
| S3 | IIP General index | MoSPI eSankhyiki | Monthly |
| S4 | CPI Combined | NSO/MoSPI | Monthly (quarterly for regression cells) |
| S5 | WPI (all commodities) | Office of the Economic Adviser, DPIIT | Monthly (quarterly for regression cells) |
| S6 | Bank credit — SCB non-food credit outstanding | RBI (DBIE / Handbook) | Monthly |
| S7 | Merchandise trade — exports, values | DGCIS via RBI Handbook | Monthly |
| S8 | State finances (deficit & spending categories) | RBI *State Finances* / e-States database | Annual (state panel) |
| S9 | Unemployment rate — PLFS | NSO/MoSPI | Annual (usual status); quarterly urban CWS noted, not graded (rule R5) |
| S10 | Groundwater stage of extraction | CGWB GWRA assessments | Irregular waves |

**Columns — tests (8):**

| # | Test | Family |
|---|---|---|
| T1 | Kitchin cycle, band 3–5 yr | Spectral |
| T2 | Juglar cycle, band 7–11 yr | Spectral |
| T3 | Monsoon periodicities: ENSO 2–7 yr, solar 9.5–12.5 yr, long 17–21 yr (three sub-tests) | Spectral |
| T4 | Phillips curve slope (inflation on output gap) | Regression |
| T5 | Okun coefficient (Δ unemployment on output growth deviation) | Regression |
| T6 | Political budget cycle (election-year effect, Khemani design) | Regression (panel) |
| T7 | Beta convergence (primary) with sigma convergence (sub-grade) across states | Regression (cross-section / trend) |
| T8 | Taylor rule / natural rate r* (state-space, Laubach–Williams class) | Structural |

**Applicability (fixed in advance; NA cells carry the one-line reason registered here):**

- **T1/T2** graded for S2 (quarterly growth), S3, S4, S5, S6, S7 (monthly growth/inflation),
  and S9 (span rule only — no simulation needed if the span rule already decides).
  NA for: S1 (business-cycle bands are not monsoon claims; monsoon periodicities are T3),
  S8 (no business-cycle band claim is made for annual fiscal aggregates in the literature;
  the fiscal cycle claim is T6), S10 (irregular assessment waves are not a fixed-frequency
  series; no cycle claim applies).
- **T3** graded for S1 only (both rulers). NA for all other rows: the bands are
  monsoon-specific claims (Kane 1990).
- **T4** graded at S4 (primary; partner = S2 output gap) and S5 (the pre-CPI literature
  ruler; partner = S2 output gap). NA elsewhere with pointer: S2, S3, S9 — "graded where
  the inflation ruler lives (S4/S5)".
- **T5** graded at S9 (partner = S2 growth). NA at S2 with pointer ("same pair graded at
  S9; the binding ruler is unemployment"); NA elsewhere (no output–unemployment pair).
- **T6** graded at S8 only. NA elsewhere (the Khemani design is a state-fiscal panel;
  no equivalent registered design exists for the other rows).
- **T7** graded at S2 (state per-capita GSDP panel, the national-accounts companion
  series; same base breaks as S2). NA elsewhere (no cross-unit income panel).
- **T8** graded at S4 (joint span of CPI + GDP + repo rate; the binding rulers are the
  price index and the accounts). NA elsewhere with pointer to S4.
- **S10 (CGWB)** is NA on every column, for the reasons above; its audit row exists
  because the series powers the future Shah build (ASSESSMENT §B), and an honest grid
  must show a load-bearing series that none of the registered theories can use.

Graded cells: S1×T3 (3 sub-tests), S2×{T1,T2,T7}, S3×{T1,T2}, S4×{T1,T2,T4,T8},
S5×{T1,T2,T4}, S6×{T1,T2}, S7×{T1,T2}, S8×{T6}, S9×{T1,T2,T5} = **23 graded cells**
(of 80 grid cells; 57 NA). No cell may be added, dropped, or re-graded after computation.

## 2. Break and ruler rules (fixed)

- **R1 — No silent splicing.** A series' *clean span* is its longest span on a single
  base / single method / single design. All n's, MDES values, and verdicts use the clean
  span only. Longer spliced spans may be mentioned in audit notes, labelled "spliced",
  and never graded.
- **R2 — Clean-span ends are stated with their cause** (base change, method change,
  design revamp, or data end) in the audit table.
- **R3 — Cross-ruler gaps** are measured only over identical periods, as (a) level or
  growth gap on the overlap and (b) correlation where both rulers are in hand. Gaps not
  measurable from data in hand or documented values are recorded as "documented-only"
  or "pending D", never estimated.
- **R4 — Revision facts are documented-only.** Only revision behaviour attested in an
  official release, release calendar, or cited study enters the audit. Anything that
  would require the vintages dataset is marked **"pending D"** (ASSESSMENT §D).
- **R5 — Like-for-like pairing.** A regression cell is graded on the pairing whose
  rulers measure the same population and concept as the literature design.
  Mismatched pairings (e.g. urban-only CWS unemployment against national GDP for
  Okun) are noted in the cell, not graded.
- **R6 — No observation dropping.** COVID-era observations inside a clean span stay
  in; their effect enters through the registered σ and ρ inputs, which are full-span
  values. No outlier rule is registered for this build, so none may be applied.

## 3. MDES machinery (fixed)

**Common settings:** α = 0.05; target power = 0.80. Regression multiplier
(z₀.₉₇₅ + z₀.₈₀) = 1.960 + 0.842 = **2.802**.

### 3a. Spectral family (T1–T3) — the pilot's rule, verbatim, plus injection

For each graded spectral cell, preprocessing and the test are exactly the pilot's
registered rule (`PREREGISTRATION.md` decision rules 1–5): demean + linear-detrend;
Hann-tapered periodogram on an 8× zero-padded grid; 2,000 AR(1) surrogates with the
series' ρ and variance (seed 42); band statistic = maximum power in band; a peak is
supported iff its band maximum exceeds the surrogates' 95th percentile.

The Atlas adds the registered **injection step** (this is the MDES computation, fixed
here before any Atlas data work): inject a pure sinusoid at the band's geometric-centre
period into AR(1) surrogates of the same length/ρ, at amplitudes
A ∈ {0.10, 0.15, …, 1.20} × (series sd), 200 trials per amplitude (seed 43); power(A) =
fraction of trials whose band maximum clears the §3a null threshold; **MDES amplitude**
= smallest A with power ≥ 0.80, linearly interpolated between grid points. MDES is
reported in sd units and as variance share A²/2 ÷ (1 + A²/2).

Inputs per cell: clean n at the series' frequency (from the audit, §5) and ρ —
*real* (estimated from data in hand: S1 IMD, S1 IITM, S3) or *assumed* (stated in the
audit with its source: S2, S4, S5, S6, S7). Assumed ρ may not be revised after seeing
any MDES output.

**Span rules (spectral), registered:**
- Clean span < 2 × (longest band period) → **UNTESTABLE**, no simulation needed
  (fewer than two full cycles cannot identify a cycle against trend).
- Clean span < 4 × (longest band period) → verdict **capped at UNDERPOWERED**
  (fewer than four cycles; ASSESSMENT §A anchor: a Juglar claim needs ≥35–55 clean
  years).

**Anchor amplitudes (literature-sized cycles), registered:**
- T3 monsoon bands: a sinusoid explaining **10% of variance** → A_lit = √(2·0.10/0.90)
  ≈ **0.47 sd**. Justification: Kane's (1990) reported periodicities were the dominant
  features of his MESA spectra; a claimed monsoon cycle weaker than a tenth of total
  variance is not the claim the literature makes.
- T1/T2 business-cycle bands: a sinusoid explaining **15% of variance** →
  A_lit = √(2·0.15/0.85) ≈ **0.59 sd**. Justification: band-pass business-cycle
  components in the Burns–Mitchell / Bose & Goyal (2020) tradition carry a
  double-digit share of growth variance; 15% is the conservative end.

**Spectral verdicts:** TESTABLE iff MDES ≤ A_lit **and** span ≥ 4 × longest period;
UNDERPOWERED iff MDES ≤ 2 × A_lit and span ≥ 2 × longest period (and not TESTABLE);
UNTESTABLE iff MDES > 2 × A_lit or span < 2 × longest period.

### 3b. Regression family (T4–T7) — standard power formulas

MDES(β) = 2.802 × σ_ε / ( sd(x) × √n_eff ), with each cell's design, inputs, and input
sources fixed in §4 **before** computation. Rules:

- **Minimum-n rules (registered):** a time-series regression cell with clean n < 20 is
  **UNTESTABLE** regardless of the formula value (a slope on fewer than 20 points is
  not a test of a literature claim; the formula MDES is still reported, labelled
  "for the record"). Cross-section cells require ≥ 20 units; panel cells require
  ≥ 200 unit-years and ≥ 15 clusters.
- **Panels:** n_eff = n / DEFF, DEFF = 1 + (m − 1) × ICC, with m = mean years per
  cluster and the ICC registered per cell in §4.
- **Regression verdicts:** TESTABLE iff MDES ≤ anchor; UNDERPOWERED iff
  anchor < MDES ≤ 2 × anchor; UNTESTABLE iff MDES > 2 × anchor, or a minimum-n /
  pairing rule (R5) decides.

### 3c. Structural family (T8)

r* estimation of the Laubach–Williams class is graded by a registered span rule, not
a formula: the literature's own practice uses ≥ 40 years of quarterly data on
consistent rulers (Laubach & Williams use US data from 1961). Clean joint span
(CPI base-2012 + GDP base-2011-12 + repo) < 100 quarters → **UNTESTABLE** under Atlas
rules; 100–159 quarters → UNDERPOWERED; ≥ 160 quarters → TESTABLE. Published RBI r*
estimates (1.4–1.9%, RBI Bulletin 2022/2026) rest on spliced series plus model
structure; they are recorded in the cell as existing estimates, and the verdict is
explicitly about data-only testability under R1.

## 4. Cell designs, inputs, and literature anchors (fixed)

All σ_ε / sd(x) / ρ inputs below are either (i) computed from data already in hand
(pilot), (ii) documented values cited in §7, or (iii) **assumptions**, labelled as
such, anchored to the cited published magnitudes. Assumptions are registered now
and may not be tuned after computation.

- **T4 Phillips at S4 (CPI):** quarterly; π_t (YoY CPI inflation) on output gap;
  joint clean span = CPI base-2012 (Jan 2011–Dec 2025) ∩ GDP base-2011-12
  (Q1 2011-12–Q2 2025-26) → **n = 58 quarters**. Inputs (assumptions anchored to
  RBI-published inflation volatility): σ_ε = 1.1 pp (residual sd of quarterly YoY
  inflation after lagged inflation; full-span value incl. COVID, per R6);
  sd(gap) = 1.4 pp (RBI output-gap estimates range roughly ±3 pp).
  **Anchor κ_lit = 0.25** pp inflation per 1 pp gap — the middle of published Indian
  estimates (sacrifice-ratio literature: RBI 2002 ≈ 2; Kapur & Patra 2003, 0.5–4.7;
  Dholakia 2014, 1.8–2.8; RBI WP 01/2026 ≈ 2.3–2.8; Patra et al., India Policy Forum
  2015-16, sacrifice ≈ 2.7 with slopes "imprecise" on post-1996 data).
- **T4 Phillips at S5 (WPI):** same design and joint span (**n = 58 quarters**);
  σ_ε = 1.5 pp (WPI inflation is the more volatile ruler — assumption anchored to
  RBI Handbook magnitudes); sd(gap) = 1.4 pp. Anchor κ_lit = 0.25 (the Kapur–Patra /
  RBI 2002 estimates were WPI-based).
- **T5 Okun at S9 (PLFS):** annual; ΔUR (usual status, all-India) on real GDP growth
  deviation; clean span = PLFS annual reports 2017-18–2023-24 → **n = 7** (the
  Jan-2025 design revamp and the move to calendar-year reporting break the span
  there; EUS rounds are a different ruler — "not comparable" per NSO — not a splice).
  Formula inputs, for the record: σ_ε = 0.45 pp, sd(growth deviation) = 3.0 pp
  (full-span incl. COVID, per R6). **Anchor β_lit = 0.30** pp ΔUR per 1 pp growth —
  Okun's rule-of-thumb for advanced economies (≈0.3; US gap-version ≈0.5).
  Published India estimates are smaller and scattered (−0.04 to −0.47, several
  insignificant; state-panel estimate −0.12 for 1993–2011) — which is precisely why
  the cell matters: distinguishing "India's coefficient is ≈0.1" from "≈0.3" needs
  MDES well under 0.3. The quarterly urban CWS pairing (2019Q1–2024Q4, n = 24) is
  **not graded** (rule R5: urban-only CWS ruler vs national output).
- **T6 Political budget cycle at S8:** Khemani design — state and year fixed effects,
  election-year dummy, primary outcome capital outlay (% of GSDP); deficit (% of
  GSDP) as the registered secondary outcome. Panel: 28 states × 1990-91–2023-24
  (RBI e-States span) → n = 952 state-years, m = 34, **ICC = 0.05** (assumption:
  residual ICC after state and year FE), n_eff = 952 / (1 + 33×0.05) ≈ 359.
  sd(election dummy) = √(0.21 × 0.79) ≈ 0.41 (five-year terms plus midterm polls).
  σ_ε: capital outlay 0.55 pp of GSDP; deficit 0.80 pp (assumptions anchored to RBI
  *State Finances* magnitudes: capital outlay ≈2–3% of GSDP, deficits ≈2–3%).
  **Anchors:** capital outlay **0.25 pp of GSDP**; deficit **0.50 pp of GSDP** —
  both set *below* the developing-country election-year deficit average (≈0.6–1.3%
  of GDP, Shi & Svensson as summarised in the PBC literature) because Khemani (2004,
  J. Dev. Econ. 73:125–154; 14 states, 1960–1996) found Indian fiscal effects
  deliberately *small* (commodity taxes down, investment spending up, deficits
  **no effect**, road construction large). Cell verdict is graded on the primary
  (capital outlay) outcome; the deficit MDES is reported alongside.
- **T7 Convergence at S2 (GSDP):** beta — long-difference cross-section over the
  clean span: mean annual growth of per-capita GSDP 2011-12–2023-24 on initial
  (2011-12) log per-capita GSDP, **n = 28 states** (major states with a consistent
  base-2011-12 GSDP series). Inputs: σ_ε = 1.1 pp/yr (assumption: residual sd of
  state mean growth); sd(log initial pc income) = 0.52 (documented cross-state
  dispersion, richest/poorest ratio ≈4–5×). Slope-to-speed map over T = 13 years:
  slope = −(1 − e^(−λT))/T. **Anchor λ_lit = 1.5%/yr** (Cashin & Sahay 1996, IMF
  Staff Papers: Indian states, 1961–1991, ≈1.5%/yr conditional; Barro's cross-country
  "iron law" ≈2%/yr is the less conservative alternative — the India-specific
  anchor governs). Sigma sub-grade: linear trend in the cross-state sd of log
  per-capita GSDP over the same 13 annual points; noise sd of the dispersion
  series = 0.015 (assumption); literature-sized sigma drift ≈ 0.001–0.003/yr.
- **T8 at S4:** joint clean span 58 quarters < 100 → graded by §3c rule.
- **Spectral inputs:** S1-IMD n = 125, ρ real (pilot: ≈0.03); S1-IITM n = 146, ρ real;
  S3 n = 167 (log-growth, deseasonalised; pilot), ρ real. Assumed ρ (registered):
  S2 quarterly real GDP growth ρ = 0.35; S4 monthly CPI inflation ρ = 0.50;
  S5 monthly WPI inflation ρ = 0.45; S6 monthly non-food credit growth ρ = 0.30;
  S7 monthly export growth ρ = 0.15. (Assumptions anchored to the persistence
  typical of these series in RBI/MoSPI published work; labelled assumptions in the
  audit, per §3a.)
- **S9 spectral (T1/T2):** graded by the span rule only, on the longest like-for-like
  PLFS span (quarterly urban CWS, 2019Q1–2024Q4, 6.0 years).

## 5. Series audit — what will be recorded (fixed schema)

`data/series_audit.csv`, one row per series (S1 gets two rows, one per ruler):
series, ruler/source, frequency, full span as published, clean span, clean-span end
cause, breaks list (each with year + nature + source), second ruler (if any),
cross-ruler gap over identical periods (measured / documented-only / pending D),
revision behaviour (documented-only or "pending D"), n at each graded frequency,
ρ and σ inputs used (real / assumed + source). Metadata (spans, base years, breaks)
verified against the sources in §7 — including: GDP bases 2004-05 → 2011-12 (Jan
2015) → 2022-23 (27 Feb 2026; back series pending, expected Dec 2026); CPI bases
2010 (Jan 2011) → 2012 → 2024 (12 Feb 2026; index values from Jan 2025, YoY
comparable only from Jan 2026); IIP bases 2004-05 → 2011-12 → 2022-23 (1 Jun 2026);
WPI bases … → 2011-12 → 2022-23 (15 Jun 2026); PLFS launch Apr 2017, design revamp
Jan 2025; CGWB method break GEC-97 → GEC-2015 at the 2017 assessment (waves 2009,
2013, 2017, 2020, 2022, 2023, 2024, 2025); SCB credit definition stable since Nov
1960 (RBI Handbook notes), coverage events (e.g. Jul 2023 merger) noted, sectoral
format revision Jan 2021; merchandise *values* carry no base year (only the DGCIS
unit-value/quantity *indices* were rebased, to FY2022-23, Feb 2026); RBI e-States
time series from 1990-91 (publication since 1950-51; Handbook major indicators from
1980-81); state set changes (bifurcations 2000/2014/2019; UTs with legislature
included from 2017-18).

## 6. Deliverables

- `data/series_audit.csv` — §5 schema.
- `data/atlas_grid.csv` — one row per graded cell (monsoon = 3 rows): series, test,
  applicable, verdict, MDES, anchor, clean n / span, one-line reason.
- `scripts/atlas.py` — re-runnable end to end; regenerates both CSVs' computed
  values and both figures.
- `figures/fig_atlas_heatmap.png` — grid heatmap (series × test, verdict colours,
  NA greyed) generated from `atlas_grid.csv`.
- `figures/fig_atlas_spans.png` — clean-span timeline per series.
- `ATLAS.md` — verdict grid as a readable table, per-series audit summaries,
  headline counts per verdict, the surprising cells, honest gaps. Every verdict
  sentence obeys §0.

## 7. Sources verified for this registration (2026-11-17)

MoSPI FAQ on the new GDP series (base 2022-23; release 27 Feb 2026 for 2022-23 to
2025-26; back series expected Dec 2026, spliced beyond the previous base) · PIB /
Lok Sabha reply (base revisions: GDP & IIP 2011-12 → 2022-23; CPI 2012 → 2024,
released 12 Feb 2026; IIP new series 1 Jun 2026; WPI 2011-12 → 2022-23 released
15 Jun 2026) · MoSPI CPI base-2024 press materials via MFIN technical note (old
2012 series stopped Dec 2025; new index values from Jan 2025; Jan 2026 inflation
2.75% provisional → 2.74% final; linking factor 0.5267) · NSO SAE press note,
28 Feb 2025 (2011-12 base: FY2023-24 growth 9.2% FRE; FY2024-25 6.5% SAE;
FY2022-23 7.6% final) — against MoSPI new-series FY2023-24 7.2% / FY2024-25 7.1%:
the documented two-ruler growth gap on identical years · Khemani (2004) abstract,
J. Dev. Econ. 73:125–154 / World Bank PRWP 2454 · RBI WP 01/2026 press summary
(sacrifice ratios: RBI 2002 ≈2; Kapur & Patra 0.5–4.7; Dholakia 1.8–2.8; time-varying
≈2.3–2.8) · Patra et al., *Understanding Inflation in India*, India Policy Forum
2015-16 (Phillips estimates imprecise; data since 1996) · Okun-India literature
(state-panel coefficient −0.12, 1993–2011; other estimates −0.04…−0.47, several
insignificant) · RBI *State Finances* explanatory notes & Communication Policy
2025 (e-States time series from 1990-91; publication since 1950-51; budget-based
figures may differ from CAG audited accounts) · Cashin & Sahay (1996) as surveyed
in the Indian convergence literature (≈1.5%/yr) · PLFS Annual Report 2025 press
note & Lok Sabha reply (annual reports Jul 2017–Jun 2024; revamped design from
Jan 2025; monthly CWS from Apr 2025; quarterly urban-only to Dec 2024; PLFS not
comparable with EUS) · RBI Handbook notes on tables (SCB credit definition since
Nov 1960; sectoral format revision Jan 2021; credit growth adjusted for reporting
errors) · DBIE banking table spans (monthly banking series from 1997–2001 by
table; CEIC/RBI sectoral credit outstanding from Mar 2003) · DGCIS / PIB (trade
indices rebased to FY2022-23, Feb 2026; values are levels) · CGWB GWRA waves and
the GEC-97 → GEC-2015 break: `ASSESSMENT.md` §B (verified there from CGWB state
reports) · Pilot `REPORT.md` §0–§5 and `PREREGISTRATION.md` (spectral rule;
Kane 1990; Bose & Goyal 2020; Khemani deficit-alignment ≈10%, 2002/2007; IMF
Article IV national-accounts grade "C", 2024/2025 — via ASSESSMENT §A).

*End of registration. The next commit touching this project must be the build
(scripts + audit + grid + figures + ATLAS.md), or a dated revision to this file
labelled as such.*
