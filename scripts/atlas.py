#!/usr/bin/env python3
"""Testability Atlas computation, exactly as registered in ATLAS_PREREGISTRATION.md.

- Spectral MDES (sec 3a): pilot's registered test verbatim (demean+detrend, Hann
  periodogram on 8x zero-padded grid, 2,000 AR(1) surrogates seed 42, band-max vs
  95th percentile) + the registered injection step (sinusoid at band geometric
  centre, amplitudes 0.10..1.20 sd, 200 trials each, seed 43, random phase;
  MDES = smallest amplitude with power >= 0.80, linearly interpolated).
  Surrogates are generated at unit variance, so amplitudes are in noise-sd units;
  variance share = A^2/2 / (1 + A^2/2), per the registration.
- Regression MDES (sec 3b): MDES = 2.802 * sigma_eps / (sd_x * sqrt(n_eff)),
  inputs exactly as registered in sec 4 of ATLAS_PREREGISTRATION.md.
- Structural T8 (sec 3c): span rule only.
Outputs: data/series_audit.csv, data/atlas_grid.csv, data/atlas_summary.json,
figures/fig_atlas_heatmap.png, figures/fig_atlas_spans.png.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA, FIG = ROOT / "data", ROOT / "figures"
FIG.mkdir(exist_ok=True)
Z = 2.802  # z_{.975} + z_{.80}

# ---------------------------------------------------------------- spectral core
def detrend_rows(M):
    M = np.asarray(M, float)
    n = M.shape[1]
    t = np.arange(n, dtype=float)
    tc = t - t.mean()
    b = (M @ tc) / (tc @ tc)
    a = M.mean(axis=1) - b * t.mean()
    return M - (a[:, None] + b[:, None] * t[None, :])


def spectra(M):
    """Hann periodogram, spectrum scaling, 8x zero-padded grid (pilot's rule)."""
    n = M.shape[1]
    w = np.hanning(n)
    F = np.fft.rfft(M * w[None, :], n=8 * n, axis=1)
    P = (np.abs(F) ** 2) / (w.sum() ** 2)
    P[:, 1:-1] *= 2.0  # one-sided convention, as in scipy scaling='spectrum'
    f = np.fft.rfftfreq(8 * n, d=1.0)
    return f, P


def ar1_matrix(n, rho, nsim, rng, burn=200):
    innov = rng.normal(0.0, np.sqrt(max(1 - rho ** 2, 1e-6)), (nsim, n + burn))
    S = np.zeros((nsim, n + burn))
    for t in range(1, n + burn):
        S[:, t] = rho * S[:, t - 1] + innov[:, t]
    return S[:, burn:]


def band_mask(f, plo, phi):
    return (f >= 1.0 / phi) & (f <= 1.0 / plo) & (f > 0)


def spectral_mdes(n, rho, bands, span_years):
    """bands: {name: (plo, phi, anchor_A, longest_period_years)} periods in
    sampling units (years/months/quarters as appropriate); span_years and
    longest_period_years in years for the span rules.
    Returns {band: dict(mdes_A, mdes_varshare, verdict, span_note)}."""
    rng = np.random.default_rng(42)
    null = ar1_matrix(n, rho, 2000, rng)
    f, P = spectra(detrend_rows(null))
    thr = {}
    for name, (plo, phi, *_rest) in bands.items():
        m = band_mask(f, plo, phi)
        thr[name] = float(np.percentile(P[:, m].max(axis=1), 95))
    amps = np.round(np.arange(0.10, 1.201, 0.05), 2)
    out = {}
    for name, (plo, phi, anchor, longest_yr) in bands.items():
        m = band_mask(f, plo, phi)
        centre = np.sqrt(plo * phi)
        rngi = np.random.default_rng(43)
        t = np.arange(n, dtype=float)
        powers = []
        for A in amps:
            trials = ar1_matrix(n, rho, 200, rngi)
            phase = rngi.uniform(0, 2 * np.pi, (200, 1))
            trials = trials + A * np.sin(2 * np.pi * t[None, :] / centre + phase)
            _, Pt = spectra(detrend_rows(trials))
            powers.append(float((Pt[:, m].max(axis=1) > thr[name]).mean()))
        powers = np.array(powers)
        if powers[-1] < 0.80:
            mdes = np.inf
        elif powers[0] >= 0.80:
            mdes = float(amps[0])
        else:
            i = int(np.argmax(powers >= 0.80))
            mdes = float(amps[i - 1] + (0.80 - powers[i - 1]) *
                         (amps[i] - amps[i - 1]) / (powers[i] - powers[i - 1]))
        # verdict per registration sec 3a
        if span_years < 2 * longest_yr:
            verdict, note = "UNTESTABLE", f"span {span_years:.1f}yr < 2x longest period {longest_yr}yr (span rule)"
        elif np.isinf(mdes) or mdes > 2 * anchor:
            verdict, note = "UNTESTABLE", f"MDES > 2x anchor ({2*anchor:.2f} sd)"
        elif mdes <= anchor and span_years >= 4 * longest_yr:
            verdict, note = "TESTABLE", "MDES <= anchor and span >= 4x longest period"
        else:
            cap = "; verdict capped at UNDERPOWERED (span < 4x longest period)" if span_years < 4 * longest_yr else ""
            verdict, note = "UNDERPOWERED", f"anchor < MDES <= 2x anchor{cap}" if mdes > anchor else f"MDES <= anchor{cap}"
        out[name] = {"mdes_A": None if np.isinf(mdes) else round(mdes, 3),
                     "mdes_varshare": None if np.isinf(mdes) else round((mdes ** 2 / 2) / (1 + mdes ** 2 / 2), 3),
                     "power_at_max_amp": round(float(powers[-1]), 3),
                     "verdict": verdict, "span_note": note}
    return out


# anchors (registration sec 3a)
A_MONSOON = float(np.sqrt(2 * 0.10 / 0.90))   # 0.471 sd, 10% variance
A_BIZ = float(np.sqrt(2 * 0.15 / 0.85))       # 0.594 sd, 15% variance

SPEC_RESULTS = {}
def run_spec(key, n, rho, bands, span_years):
    SPEC_RESULTS[key] = spectral_mdes(n, rho, bands, span_years)
    for b, r in SPEC_RESULTS[key].items():
        print(f"{key} {b}: MDES={r['mdes_A']} varshare={r['mdes_varshare']} -> {r['verdict']} ({r['span_note']})")

# monsoon bands in years; business bands converted per frequency below
T3 = {"ENSO 2-7yr": (2.0, 7.0, A_MONSOON, 7.0),
      "Solar 9.5-12.5yr": (9.5, 12.5, A_MONSOON, 12.5),
      "Long 17-21yr": (17.0, 21.0, A_MONSOON, 21.0)}
run_spec("S1-IMD", 125, 0.031, T3, 125.0)
run_spec("S1-IITM", 146, -0.100, T3, 146.0)
run_spec("S3-IIP", 167, -0.097,
         {"Kitchin 36-60mo": (36.0, 60.0, A_BIZ, 5.0),
          "Juglar 84-132mo": (84.0, 132.0, A_BIZ, 11.0)}, 167 / 12)
run_spec("S2-GDP-K", 58, 0.35,
         {"Kitchin 12-20q": (12.0, 20.0, A_BIZ, 5.0)}, 58 / 4)
run_spec("S4-CPI-K", 180, 0.50,
         {"Kitchin 36-60mo": (36.0, 60.0, A_BIZ, 5.0)}, 180 / 12)
run_spec("S5-WPI-K", 169, 0.45,
         {"Kitchin 36-60mo": (36.0, 60.0, A_BIZ, 5.0)}, 169 / 12)
run_spec("S6-Credit", 272, 0.30,
         {"Kitchin 36-60mo": (36.0, 60.0, A_BIZ, 5.0),
          "Juglar 84-132mo": (84.0, 132.0, A_BIZ, 11.0)}, 272 / 12)
run_spec("S7-Trade", 312, 0.15,
         {"Kitchin 36-60mo": (36.0, 60.0, A_BIZ, 5.0),
          "Juglar 84-132mo": (84.0, 132.0, A_BIZ, 11.0)}, 312 / 12)

# ---------------------------------------------------------------- regression MDES
def reg_mdes(sigma_eps, sd_x, n_eff):
    return Z * sigma_eps / (sd_x * np.sqrt(n_eff))

def reg_verdict(mdes, anchor):
    if mdes <= anchor:
        return "TESTABLE"
    if mdes <= 2 * anchor:
        return "UNDERPOWERED"
    return "UNTESTABLE"

REG = {}
# T4 Phillips (registration sec 4): n=58 quarters joint clean span
REG["S4-T4"] = {"mdes": reg_mdes(1.1, 1.4, 58), "anchor": 0.25}
REG["S5-T4"] = {"mdes": reg_mdes(1.5, 1.4, 58), "anchor": 0.25}
for k, v in REG.items():
    v["verdict"] = reg_verdict(v["mdes"], v["anchor"])
# T5 Okun: formula for the record; verdict by the registered n<20 rule
REG["S9-T5"] = {"mdes": reg_mdes(0.45, 3.0, 7), "anchor": 0.30,
                "verdict": "UNTESTABLE"}
# T6 PBC: panel, DEFF with ICC=0.05, m=34
n_eff_pbc = 952 / (1 + 33 * 0.05)
REG["S8-T6-primary"] = {"mdes": reg_mdes(0.55, 0.407, n_eff_pbc), "anchor": 0.25}
REG["S8-T6-deficit"] = {"mdes": reg_mdes(0.80, 0.407, n_eff_pbc), "anchor": 0.50}
for k in ("S8-T6-primary", "S8-T6-deficit"):
    REG[k]["verdict"] = reg_verdict(REG[k]["mdes"], REG[k]["anchor"])
    REG[k]["n_eff"] = n_eff_pbc
# T7 convergence beta: slope MDES -> implied convergence speed over T=13
se_beta = 0.011 / (0.52 * np.sqrt(28))
mdes_slope = Z * se_beta
lam_mdes = -np.log(1 - mdes_slope * 13) / 13
anchor_slope = (1 - np.exp(-0.015 * 13)) / 13
REG["S2-T7-beta"] = {"mdes_slope": mdes_slope, "anchor_slope": anchor_slope,
                     "mdes_lambda_pct": 100 * lam_mdes, "anchor_lambda_pct": 1.5,
                     "verdict": reg_verdict(mdes_slope, anchor_slope)}
# T7 sigma sub-grade: trend in cross-state dispersion, 13 annual points
sd_t = np.std(np.arange(1, 14), ddof=1)
mdes_sigma = Z * 0.015 / (sd_t * np.sqrt(13))
REG["S2-T7-sigma"] = {"mdes_per_yr": mdes_sigma,
                      "verdict": "UNDERPOWERED" if mdes_sigma <= 0.003 else "UNTESTABLE"}
for k, v in REG.items():
    print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})

# ---------------------------------------------------------------- audit table
AUDIT = [
 dict(series_id="S1-IMD", series="Monsoon rainfall (JJAS, All-India)", ruler_source="IMD Pune operational series (pilot pull)",
      frequency="annual", full_span_published="1901-2026 (source file)", clean_span="1901-2025", clean_span_years=125,
      clean_end_cause="data end (2026 row is a partial/current year; pilot analysed to 2025)",
      breaks="none on this ruler; construction differs from IITM ruler (operational subdivisional weighting vs 306-station homogeneous network)",
      second_ruler="IITM homogeneous series", cross_ruler_gap="MEASURED (pilot, identical years 1901-2016): IMD mean 887.3 mm vs IITM 843.6 mm (+43.7 mm, +5.2%); r=0.947; mean abs diff 43.9 mm",
      cross_ruler_gap_type="measured", revision_behaviour="pending D (IMD updates datasets; no documented revision-magnitude study used)",
      n_annual=125, n_quarterly="", n_monthly="", rho_input="0.031 (real, pilot)", sigma_inputs="sd 86.5 mm (pilot)",
      sources="Pilot REPORT.md sec 2; data/README.md"),
 dict(series_id="S1-IITM", series="Monsoon rainfall (JJAS, All-India)", ruler_source="IITM Pune homogeneous series (IMD observations)",
      frequency="annual", full_span_published="1871-2016", clean_span="1871-2016", clean_span_years=146,
      clean_end_cause="series end (data end, not a break)",
      breaks="input construction note: 306-station network to 2014; IMD subdivisional data for 2015-16",
      second_ruler="IMD operational series", cross_ruler_gap="MEASURED (pilot, identical years 1901-2016): see S1-IMD row; Hurst also disagrees (IMD H=0.75 vs IITM H=0.67, pilot sec 2)",
      cross_ruler_gap_type="measured", revision_behaviour="pending D",
      n_annual=146, n_quarterly="", n_monthly="", rho_input="-0.100 (real, pilot)", sigma_inputs="from pilot data",
      sources="Pilot REPORT.md sec 2; data/README.md"),
 dict(series_id="S2", series="GDP & national accounts (incl. state GSDP)", ruler_source="NSO / MoSPI",
      frequency="quarterly (national); annual (GSDP)", full_span_published="annual 1950-51- (spliced across bases); quarterly 1996-97- (spliced)",
      clean_span="quarterly, base 2011-12: Q1 2011-12 to Q2 2025-26; GSDP panel, base 2011-12: 2011-12 to 2023-24, 28 states",
      clean_span_years=14.5, clean_end_cause="base change to 2022-23 (released 27 Feb 2026); new-base series covers only 2022-23 to 2025-26 and its back series is pending (expected Dec 2026)",
      breaks="base 2004-05 -> 2011-12 (Jan 2015; MCA-21 corporate data + SNA-2008 methods); base 2011-12 -> 2022-23 (Feb 2026; new data sources, double deflation); 2018 back-series dispute (documented controversy over the spliced back series)",
      second_ruler="the other base over the overlap 2022-23 to 2025-26",
      cross_ruler_gap="DOCUMENTED (identical years, two bases): FY2023-24 real growth 9.2% (2011-12 base, NSO First Revised Estimates, Feb 2025) vs 7.2% (2022-23 base, Feb 2026) = -2.0 pp; FY2024-25 6.5% vs 7.1% = +0.6 pp; GDP level revised -2.9% (FY2022-23) and -3.8% (FY2023-24, FY2024-25)",
      cross_ruler_gap_type="documented-only",
      revision_behaviour="DOCUMENTED: multi-year revision ladder (advance -> provisional -> first/second revised -> final, ~3 years); IMF Article IV data-adequacy grade 'C' for national accounts (2024/2025, via ASSESSMENT sec A); systematic revision magnitudes pending D",
      n_annual="13 (GSDP panel years) x 28 states", n_quarterly=58, n_monthly="", rho_input="0.35 (assumed, quarterly real GDP growth)",
      sigma_inputs="convergence cell: sigma_eps 1.1 pp/yr, sd(log initial pc income) 0.52 (registration sec 4)",
      sources="MoSPI FAQ on new GDP series (Feb 2026); NSO SAE press note 28 Feb 2025 (PIB); PIB/Lok Sabha base-revision reply (2026); ASSESSMENT sec A"),
 dict(series_id="S3", series="IIP General index", ruler_source="MoSPI eSankhyiki API (pilot pull)",
      frequency="monthly", full_span_published="monthly on successive bases (2004-05, 2011-12, 2022-23)",
      clean_span="base 2011-12: Apr 2012-Mar 2026", clean_span_years=14.0,
      clean_end_cause="base change to 2022-23 (new series released 1 Jun 2026)",
      breaks="base 2004-05 -> 2011-12; base 2011-12 -> 2022-23 (Jun 2026)",
      second_ruler="new-base (2022-23) series, overlap from 2022-23",
      cross_ruler_gap="pending D (overlap exists; first-release/new-base comparisons not extracted in this build)",
      cross_ruler_gap_type="pending D",
      revision_behaviour="DOCUMENTED: quick estimates revised over the following two monthly releases (MoSPI practice); magnitudes pending D",
      n_annual="", n_quarterly="", n_monthly=168, rho_input="-0.097 (real, pilot, log-growth deseasonalised)",
      sigma_inputs="from pilot data", sources="Pilot REPORT.md sec 3; PIB/Lok Sabha base-revision reply (2026)"),
 dict(series_id="S4", series="CPI Combined", ruler_source="NSO / MoSPI",
      frequency="monthly", full_span_published="Jan 2011- (bases 2010, 2012, 2024)",
      clean_span="base 2012: Jan 2011-Dec 2025", clean_span_years=15.0,
      clean_end_cause="base change to 2024 (released 12 Feb 2026); new-base index values exist from Jan 2025 but YoY inflation is comparable only from Jan 2026 - too short to grade",
      breaks="base 2010 -> 2012; base 2012 -> 2024 (Feb 2026: basket 299 -> 358 items, food weight 45.86% -> 36.75%, COICOP 2018 classification)",
      second_ruler="CPI-IW / WPI measure different populations and baskets (not the same quantity - no gap graded); base-2024 series over 2025 overlap",
      cross_ruler_gap="DOCUMENTED: official linking factor 0.5267 (combined) joins base-2012 levels to base-2024; a YoY inflation gap over the overlap year is pending D",
      cross_ruler_gap_type="documented-only",
      revision_behaviour="DOCUMENTED: provisional -> final in the next month's release (e.g. Jan 2026: 2.75% provisional -> 2.74% final); magnitudes pending D",
      n_annual="", n_quarterly="60 published; 58 in joint span with GDP base 2011-12", n_monthly=180,
      rho_input="0.50 (assumed, monthly inflation)", sigma_inputs="Phillips cell: sigma_eps 1.1 pp, sd(gap) 1.4 pp (registration sec 4)",
      sources="MoSPI CPI base-2024 press materials (Feb 2026) via MFIN technical note; PIB/Lok Sabha reply (2026); RBI Handbook Table 34 (span)"),
 dict(series_id="S5", series="WPI (all commodities)", ruler_source="Office of the Economic Adviser, DPIIT",
      frequency="monthly", full_span_published="monthly on successive bases back decades",
      clean_span="base 2011-12: Apr 2012-Apr 2026", clean_span_years=14.1,
      clean_end_cause="base change to 2022-23 (released 15 Jun 2026, from the May 2026 index)",
      breaks="bases ... -> 2004-05 -> 2011-12 -> 2022-23 (Jun 2026)",
      second_ruler="CPI (different concept: wholesale vs consumer prices - noted, not a gap)",
      cross_ruler_gap="none graded (different quantity)", cross_ruler_gap_type="none",
      revision_behaviour="DOCUMENTED: provisional -> final after ~8 weeks (OEA practice); magnitudes pending D",
      n_annual="", n_quarterly="58 in joint span with GDP base 2011-12", n_monthly=169,
      rho_input="0.45 (assumed, monthly inflation)", sigma_inputs="Phillips cell: sigma_eps 1.5 pp, sd(gap) 1.4 pp (registration sec 4)",
      sources="PIB/Lok Sabha base-revision reply (2026); OEA release practice"),
 dict(series_id="S6", series="Bank credit - SCB non-food credit outstanding", ruler_source="RBI (DBIE / Handbook of Statistics)",
      frequency="monthly", full_span_published="monthly banking tables in DBIE from 1997-2001 by table; bank credit definition stable since Nov 1960 (RBI Handbook notes)",
      clean_span="Mar 2003-Oct 2025 (sectoral outstanding, RBI via CEIC listing)", clean_span_years=22.7,
      clean_end_cause="data end (series continuing; levels carry no base year, so no base break ends the span)",
      breaks="no base-year breaks (levels, Rs); coverage events: Jul 2023 HDFC-HDFC Bank merger (level shift in outstanding, noted by RBI/CEIC); sectoral deployment format revision Jan 2021; 2021-22 growth adjusted for past reporting errors (RBI notes)",
      second_ruler="none (single compiler; fortnightly WSS and monthly Section-42 returns are the same ruler at different frequencies)",
      cross_ruler_gap="none", cross_ruler_gap_type="none",
      revision_behaviour="DOCUMENTED: growth rates adjusted for past reporting errors by select SCBs (RBI Handbook notes); magnitudes pending D",
      n_annual="", n_quarterly="", n_monthly=272, rho_input="0.30 (assumed, monthly growth)",
      sigma_inputs="assumption per registration sec 4", sources="RBI Handbook notes on tables; DBIE banking table spans; CEIC/RBI sectoral credit listing (Mar 2003-)"),
 dict(series_id="S7", series="Merchandise trade - exports, values", ruler_source="DGCIS, via RBI Handbook",
      frequency="monthly", full_span_published="monthly values, long (DGCIS EIDB coverage from the late 1990s)",
      clean_span="Apr 2000-Mar 2026 (conservative documented span used for grading)", clean_span_years=26.0,
      clean_end_cause="data end (series continuing; values are levels and carry no base year)",
      breaks="none for values; the DGCIS unit-value / quantity indices (a different product) were rebased 2012-13 -> 2022-23 in Feb 2026",
      second_ruler="none official for values (partner-country mirror statistics are foreign rulers, out of scope)",
      cross_ruler_gap="none", cross_ruler_gap_type="none",
      revision_behaviour="DOCUMENTED: quick estimates revised in later releases; RBI Handbook table note: 'data for 2023-24 are revised; monthly data may not add up to annual data on account of revision'; magnitudes pending D",
      n_annual="", n_quarterly="", n_monthly=312, rho_input="0.15 (assumed, monthly export growth)",
      sigma_inputs="assumption per registration sec 4", sources="RBI Handbook trade tables (Table 193 and notes); DGCIS/PIB trade-indices revision note (Feb 2026)"),
 dict(series_id="S8", series="State finances (deficit & spending categories)", ruler_source="RBI State Finances: A Study of Budgets / e-States database",
      frequency="annual (state panel)", full_span_published="publication since 1950-51; e-States time series from 1990-91; Handbook major indicators from 1980-81",
      clean_span="1990-91 to 2023-24, 28 states (RBI consistent presentation)", clean_span_years=34,
      clean_end_cause="data end (continuing annual publication; no base years in budget documents)",
      breaks="no base years; coverage/classification notes: UTs with legislature included from 2017-18; state bifurcations 2000 (Chhattisgarh, Jharkhand, Uttarakhand), 2014 (Telangana), 2019 (J&K) - panel uses RBI's consistent 28-state presentation; GST (2017) changed tax composition",
      second_ruler="CAG audited accounts",
      cross_ruler_gap="DOCUMENTED-ONLY: RBI Handbook notes state budget-based figures 'could differ' from CAG audited data; the gap is not measured in this build",
      cross_ruler_gap_type="documented-only",
      revision_behaviour="DOCUMENTED structure: each budget publishes BE / RE / actuals for overlapping years (a built-in revision ladder); systematic magnitudes pending D",
      n_annual="952 state-years (28 x 34)", n_quarterly="", n_monthly="",
      rho_input="n/a (regression family)", sigma_inputs="PBC cell: sigma_eps 0.55 pp (capital outlay), 0.80 pp (deficit); sd(election dummy) 0.407; ICC 0.05 (registration sec 4)",
      sources="RBI State Finances explanatory notes; RBI Communication Policy (Jan 2025); RBI Handbook of Statistics on State Government Finances (2010)"),
 dict(series_id="S9", series="Unemployment rate - PLFS", ruler_source="NSO / MoSPI (PLFS)",
      frequency="annual (usual status); quarterly urban CWS; monthly CWS from Apr 2025",
      full_span_published="annual reports 2017-18 to 2023-24 (Jul-Jun) + calendar-2025 report (revamped design); quarterly urban CWS 2019Q1-2024Q4; monthly CWS Apr 2025-",
      clean_span="annual usual status: 2017-18 to 2023-24", clean_span_years=7,
      clean_end_cause="design revamp from Jan 2025 + shift from Jul-Jun to calendar-year reporting (method break)",
      breaks="launch Apr 2017 replacing quinquennial NSS EUS rounds - NSO states PLFS estimates are not comparable with EUS; design revamp Jan 2025 (new rotational panel, monthly dissemination)",
      second_ruler="NSS EUS (predecessor - officially not comparable, so the cross-ruler gap is undefined by the compiler's own statement); CMIE CPHS is a proprietary third ruler (pilot REPORT sec 5)",
      cross_ruler_gap="undefined by construction (compiler declares non-comparability with EUS); CMIE gap pending D / paywalled",
      cross_ruler_gap_type="documented-only",
      revision_behaviour="pending D (no published revision ladder for survey estimates)",
      n_annual=7, n_quarterly="24 (urban CWS 2019Q1-2024Q4; noted, not graded - rule R5)", n_monthly="Apr 2025- (revamped design; too short, not graded)",
      rho_input="n/a (span-rule + regression families)", sigma_inputs="Okun cell: sigma_eps 0.45 pp, sd(growth deviation) 3.0 pp (registration sec 4)",
      sources="PLFS Annual Report 2025 press note (Mar 2026); Lok Sabha reply on PLFS (Apr 2025); pilot REPORT sec 4-5"),
 dict(series_id="S10", series="Groundwater stage of extraction (block-level)", ruler_source="CGWB Dynamic Ground Water Resources (GWRA) assessments",
      frequency="irregular assessment waves", full_span_published="waves 2009, 2013, 2017, 2020, 2022, 2023, 2024, 2025 (~7,000 blocks)",
      clean_span="GEC-2015 waves only: 2017, 2020, 2022, 2023, 2024, 2025 (6 waves)", clean_span_years=9,
      clean_end_cause="method break GEC-97 -> GEC-2015 at the 2017 assessment (pre-2017 waves are not like-for-like)",
      breaks="GEC-97 -> GEC-2015 estimation methodology (2017); assessments annual only since 2022",
      second_ruler="none", cross_ruler_gap="none", cross_ruler_gap_type="none",
      revision_behaviour="pending D",
      n_annual="6 clean waves (irregular)", n_quarterly="", n_monthly="",
      rho_input="n/a", sigma_inputs="n/a - no graded cell; this series powers the future Shah build (ASSESSMENT sec B)",
      sources="CGWB GWRA state/national reports (verified in ASSESSMENT sec B)"),
]
audit_df = pd.DataFrame(AUDIT)
audit_df.to_csv(DATA / "series_audit.csv", index=False)

# ---------------------------------------------------------------- grid
SERIES_NAMES = {"S1": "Monsoon rainfall (IMD + IITM)", "S2": "GDP & national accounts (incl. GSDP)",
                "S3": "IIP", "S4": "CPI Combined", "S5": "WPI", "S6": "Bank credit (SCB non-food)",
                "S7": "Merchandise trade (exports)", "S8": "State finances", "S9": "PLFS unemployment",
                "S10": "CGWB groundwater"}
TEST_NAMES = {"T1": "Kitchin cycle (3-5 yr)", "T2": "Juglar cycle (7-11 yr)",
              "T3": "Monsoon periodicities", "T4": "Phillips curve", "T5": "Okun's law",
              "T6": "Political budget cycle", "T7": "Beta/sigma convergence",
              "T8": "Taylor rule / natural rate"}
NA_REASONS = {
 ("S1","T1"): "Business-cycle bands are not monsoon claims; monsoon periodicities are graded at T3.",
 ("S1","T2"): "Business-cycle bands are not monsoon claims; monsoon periodicities are graded at T3.",
 ("S1","T4"): "No inflation/output-gap pair; Phillips is graded where the inflation ruler lives (S4/S5).",
 ("S1","T5"): "No output-unemployment pair.",
 ("S1","T6"): "Not a fiscal panel; the Khemani design is graded at S8.",
 ("S1","T7"): "No cross-unit income panel.",
 ("S1","T8"): "No price/output/policy-rate system; graded at S4.",
 ("S2","T3"): "Monsoon periodicity bands are monsoon-specific claims (Kane 1990); graded at S1.",
 ("S2","T4"): "Graded where the inflation ruler lives (S4/S5); GDP supplies the partner gap series.",
 ("S2","T5"): "Same pair graded at S9; the binding ruler is unemployment, not output.",
 ("S2","T6"): "The registered Khemani design is a state-fiscal panel; graded at S8.",
 ("S2","T8"): "Graded at S4, where the binding price ruler lives; same joint span.",
 ("S3","T3"): "Monsoon periodicity bands are monsoon-specific claims; graded at S1.",
 ("S3","T4"): "Graded where the inflation ruler lives (S4/S5).",
 ("S3","T5"): "No output-unemployment pair on this row (IIP is not the Okun output ruler in the registered design).",
 ("S3","T6"): "Not a fiscal panel; graded at S8.",
 ("S3","T7"): "No cross-unit income panel.",
 ("S3","T8"): "Graded at S4.",
 ("S4","T3"): "Monsoon periodicity bands are monsoon-specific claims; graded at S1.",
 ("S4","T5"): "No output-unemployment pair; Okun graded at S9.",
 ("S4","T6"): "Not a fiscal panel; graded at S8.",
 ("S4","T7"): "No cross-unit income panel.",
 ("S5","T3"): "Monsoon periodicity bands are monsoon-specific claims; graded at S1.",
 ("S5","T5"): "No output-unemployment pair; Okun graded at S9.",
 ("S5","T6"): "Not a fiscal panel; graded at S8.",
 ("S5","T7"): "No cross-unit income panel.",
 ("S5","T8"): "Taylor/natural-rate graded at S4 (the FIT target ruler is CPI, not WPI).",
 ("S6","T3"): "Monsoon periodicity bands are monsoon-specific claims; graded at S1.",
 ("S6","T4"): "Graded where the inflation ruler lives (S4/S5).",
 ("S6","T5"): "No output-unemployment pair.",
 ("S6","T6"): "Not a fiscal panel; graded at S8.",
 ("S6","T7"): "No cross-unit income panel.",
 ("S6","T8"): "Graded at S4.",
 ("S7","T3"): "Monsoon periodicity bands are monsoon-specific claims; graded at S1.",
 ("S7","T4"): "Graded where the inflation ruler lives (S4/S5).",
 ("S7","T5"): "No output-unemployment pair.",
 ("S7","T6"): "Not a fiscal panel; graded at S8.",
 ("S7","T7"): "No cross-unit income panel.",
 ("S7","T8"): "Graded at S4.",
 ("S8","T1"): "No business-cycle band claim is made for annual fiscal aggregates; the fiscal cycle claim is T6.",
 ("S8","T2"): "No business-cycle band claim is made for annual fiscal aggregates; the fiscal cycle claim is T6.",
 ("S8","T3"): "Monsoon periodicity bands are monsoon-specific claims; graded at S1.",
 ("S8","T4"): "No inflation/output-gap pair; graded at S4/S5.",
 ("S8","T5"): "No output-unemployment pair; graded at S9.",
 ("S8","T7"): "Convergence is a GSDP income test; graded at S2.",
 ("S8","T8"): "Graded at S4.",
 ("S9","T3"): "Monsoon periodicity bands are monsoon-specific claims; graded at S1.",
 ("S9","T4"): "Phillips graded where the inflation ruler lives (S4/S5); an unemployment-gap variant inherits the S9 span problem graded at T5.",
 ("S9","T6"): "Not a fiscal panel; graded at S8.",
 ("S9","T7"): "No cross-unit income panel.",
 ("S9","T8"): "Graded at S4.",
 ("S10","T1"): "Irregular assessment waves are not a fixed-frequency series; no cycle claim applies.",
 ("S10","T2"): "Irregular assessment waves are not a fixed-frequency series; no cycle claim applies.",
 ("S10","T3"): "Not a rainfall series; monsoon bands graded at S1.",
 ("S10","T4"): "No price/output-gap content.",
 ("S10","T5"): "No output/unemployment content.",
 ("S10","T6"): "Not a fiscal series; extraction responds to policy inside the future Shah build (ASSESSMENT sec B), not the Khemani design.",
 ("S10","T7"): "Block extraction is not an income panel; spatial extraction patterns belong to the Shah build.",
 ("S10","T8"): "No monetary-policy system content.",
}

def spec_cell(cfg_key, band, n, span_txt):
    r = SPEC_RESULTS[cfg_key][band]
    return r, n, span_txt

grid = []
def add(series, test, applicable, verdict="", mdes="", mdes_units="", anchor="",
        clean_n="", clean_span="", reason="", detail=""):
    grid.append(dict(series_id=series, series=SERIES_NAMES[series], test_id=test,
                     test=TEST_NAMES[test], applicable=applicable, verdict=verdict,
                     mdes=mdes, mdes_units=mdes_units, anchor=anchor,
                     clean_n=clean_n, clean_span=clean_span, reason=reason,
                     mdes_detail=detail))

# S1 x T3: three rows, joint grade = worse of the two rulers (registration sec 1/6)
BANDS3 = ["ENSO 2-7yr", "Solar 9.5-12.5yr", "Long 17-21yr"]
rank = {"TESTABLE": 0, "UNDERPOWERED": 1, "UNTESTABLE": 2}
for b in BANDS3:
    ri, rt = SPEC_RESULTS["S1-IMD"][b], SPEC_RESULTS["S1-IITM"][b]
    joint = ri["verdict"] if rank[ri["verdict"]] >= rank[rt["verdict"]] else rt["verdict"]
    add("S1", "T3", "yes", joint,
        mdes=f"IMD {ri['mdes_A']} / IITM {rt['mdes_A']}", mdes_units="sinusoid amplitude, sd units",
        anchor=f"{A_MONSOON:.2f} sd (10% variance share)",
        clean_n="125 (IMD) / 146 (IITM)", clean_span="IMD 1901-2025; IITM 1871-2016",
        reason=f"Band {b}: joint grade = worse of the two rulers (IMD {ri['verdict']}, IITM {rt['verdict']}).",
        detail=f"IMD varshare {ri['mdes_varshare']}, IITM varshare {rt['mdes_varshare']}; pilot verdicts on the real series: not supported in this band on either ruler (pilot REPORT sec 2).")
# spectral business-cycle cells
def biz_cell(series, test, cfg, band, n, span_txt, span_years, longest):
    r = SPEC_RESULTS[cfg][band]
    add(series, test, "yes", r["verdict"], mdes=r["mdes_A"],
        mdes_units="sinusoid amplitude, sd units",
        anchor=f"{A_BIZ:.2f} sd (15% variance share)", clean_n=n, clean_span=span_txt,
        reason=f"MDES varshare {r['mdes_varshare']}; {r['span_note']}.",
        detail=f"power at max amp (1.20 sd) = {r['power_at_max_amp']}")
biz_cell("S2", "T1", "S2-GDP-K", "Kitchin 12-20q", 58, "Q1 2011-12-Q2 2025-26 (base 2011-12)", 14.5, 5)
# S2 T2: span rule (14.5 < 22) - no simulation registered for this cell
add("S2", "T2", "yes", "UNTESTABLE", mdes="", mdes_units="sinusoid amplitude, sd units",
    anchor=f"{A_BIZ:.2f} sd (15% variance share)", clean_n=58,
    clean_span="Q1 2011-12-Q2 2025-26 (base 2011-12)",
    reason="Span rule: clean span 14.5 yr < 2x longest Juglar period (22 yr); fewer than two full cycles - no simulation run, per registration sec 3a.")
biz_cell("S3", "T1", "S3-IIP", "Kitchin 36-60mo", 167, "Apr 2012-Mar 2026 growth (base 2011-12)", 13.9, 5)
biz_cell("S3", "T2", "S3-IIP", "Juglar 84-132mo", 167, "Apr 2012-Mar 2026 growth (base 2011-12)", 13.9, 11)
for s, cfg, n, span_txt, yrs in [("S4", "S4-CPI-K", 180, "Jan 2011-Dec 2025 (base 2012)", 15.0),
                                 ("S5", "S5-WPI-K", 169, "Apr 2012-Apr 2026 (base 2011-12)", 14.1)]:
    biz_cell(s, "T1", cfg, "Kitchin 36-60mo", n, span_txt, yrs, 5)
    add(s, "T2", "yes", "UNTESTABLE", mdes="", mdes_units="sinusoid amplitude, sd units",
        anchor=f"{A_BIZ:.2f} sd (15% variance share)", clean_n=n, clean_span=span_txt,
        reason=f"Span rule: clean span {yrs} yr < 2x longest Juglar period (22 yr); no simulation run, per registration sec 3a.")
biz_cell("S6", "T1", "S6-Credit", "Kitchin 36-60mo", 272, "Mar 2003-Oct 2025 growth", 22.7, 5)
biz_cell("S6", "T2", "S6-Credit", "Juglar 84-132mo", 272, "Mar 2003-Oct 2025 growth", 22.7, 11)
biz_cell("S7", "T1", "S7-Trade", "Kitchin 36-60mo", 312, "Apr 2000-Mar 2026 growth", 26.0, 5)
biz_cell("S7", "T2", "S7-Trade", "Juglar 84-132mo", 312, "Apr 2000-Mar 2026 growth", 26.0, 11)
# S9 spectral: span rule only
for t, longest in [("T1", 5), ("T2", 11)]:
    add("S9", t, "yes", "UNTESTABLE", mdes="", mdes_units="sinusoid amplitude, sd units",
        anchor=f"{A_BIZ:.2f} sd (15% variance share)", clean_n=24,
        clean_span="quarterly urban CWS 2019Q1-2024Q4 (longest like-for-like PLFS span)",
        reason=f"Span rule: 6.0 yr < 2x longest band period ({2*longest} yr); the annual usual-status span (7 points) is shorter still. No simulation run, per registration sec 3a.")
# regression cells
p = REG["S4-T4"]
add("S4", "T4", "yes", p["verdict"], mdes=round(p["mdes"], 3), mdes_units="pp inflation per 1 pp output gap",
    anchor="0.25", clean_n=58, clean_span="joint CPI base-2012 + GDP base-2011-12 quarters",
    reason="MDES just above the literature anchor (sacrifice-ratio literature implies slopes ~0.25; published Indian estimates are 'imprecise' on post-1996 data - Patra et al. 2015-16).",
    detail="sigma_eps 1.1 pp, sd(gap) 1.4 pp (registered assumptions).")
p = REG["S5-T4"]
add("S5", "T4", "yes", p["verdict"], mdes=round(p["mdes"], 3), mdes_units="pp inflation per 1 pp output gap",
    anchor="0.25", clean_n=58, clean_span="joint WPI base-2011-12 + GDP base-2011-12 quarters",
    reason="The ruler the classic Indian Phillips estimates (RBI 2002; Kapur & Patra 2003) were run on can now only be used cleanly for 58 quarters; WPI's higher residual variance worsens the MDES vs CPI.",
    detail="sigma_eps 1.5 pp, sd(gap) 1.4 pp (registered assumptions).")
p = REG["S9-T5"]
add("S9", "T5", "yes", p["verdict"], mdes=round(p["mdes"], 3),
    mdes_units="pp dUR per 1 pp growth (formula value, for the record)",
    anchor="0.30 (Okun rule-of-thumb, advanced economies)", clean_n=7,
    clean_span="PLFS annual usual status 2017-18 to 2023-24",
    reason="UNTESTABLE by the registered minimum-n rule (clean n=7 < 20): a slope on 7 annual points - one of them the COVID year - is not a test of Okun's law. The formula MDES is reported for the record only; it is mechanically flattered by the COVID growth outlier inflating sd(x). Quarterly urban CWS pairing not graded (rule R5: urban-only CWS ruler vs national output).",
    detail="sigma_eps 0.45 pp, sd(growth deviation) 3.0 pp (registered assumptions, full-span incl. COVID per rule R6).")
pp_, pd_ = REG["S8-T6-primary"], REG["S8-T6-deficit"]
add("S8", "T6", "yes", pp_["verdict"], mdes=round(pp_["mdes"], 3),
    mdes_units="pp of GSDP (capital outlay, election-year effect)",
    anchor="0.25 pp of GSDP", clean_n="952 state-years (28 states x 34 yrs; n_eff 359 after registered design effect)",
    clean_span="1990-91 to 2023-24 (RBI e-States)",
    reason="TESTABLE on the primary (capital outlay) outcome - the panel design inverts the pilot's H3 problem: hopeless spectrally at annual frequency, ample as a regression. Deficit outcome: MDES "
           f"{pd_['mdes']:.3f} pp vs anchor 0.50 pp ({pd_['verdict']}) - so Khemani's 'no deficit effect' is also a gradeable statement on this span.",
    detail="sigma_eps 0.55 pp (capital outlay) / 0.80 pp (deficit); sd(election dummy) 0.407; ICC 0.05 (registered assumptions).")
b = REG["S2-T7-beta"]; sg = REG["S2-T7-sigma"]
add("S2", "T7", "yes", b["verdict"], mdes=round(b["mdes_lambda_pct"], 2),
    mdes_units="% per year (minimum detectable convergence speed, beta)",
    anchor="1.5 %/yr (Cashin & Sahay 1996)", clean_n="28 states, one 13-year long difference",
    clean_span="per-capita GSDP, base 2011-12: 2011-12 to 2023-24",
    reason=f"Beta: MDES slope {b['mdes_slope']:.4f}/yr vs anchor slope {b['anchor_slope']:.4f}/yr - the cross-section can just detect a Cashin-Sahay-speed convergence over one clean decade. Sigma sub-grade: {sg['verdict']} (MDES trend {sg['mdes_per_yr']:.4f} log-points/yr vs literature drift 0.001-0.003/yr). Caveat: a single long difference containing COVID; the verdict grades the ruler's resolution, not any convergence claim.",
    detail="sigma_eps 1.1 pp/yr, sd(log initial pc income) 0.52 (registered inputs).")
add("S4", "T8", "yes", "UNTESTABLE", mdes="", mdes_units="quarters of clean joint span",
    anchor=">=160 quarters TESTABLE; 100-159 UNDERPOWERED (registration sec 3c)",
    clean_n=58, clean_span="joint CPI base-2012 + GDP base-2011-12 + repo, Q1 2011-12-Q2 2025-26",
    reason="Structural span rule: 58 clean quarters < 100-quarter floor for Laubach-Williams-class r* estimation on consistent rulers. RBI's published r* (1.4-1.9%) exists, but rests on spliced series plus model structure - it is not a data-only test under rule R1.")
# NA cells
for (s, t), reason in sorted(NA_REASONS.items()):
    add(s, t, "no", reason=reason)

grid_df = pd.DataFrame(grid)
order_s = {s: i for i, s in enumerate(["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10"])}
order_t = {t: i for i, t in enumerate(["T1","T2","T3","T4","T5","T6","T7","T8"])}
grid_df["_so"] = grid_df.series_id.map(order_s); grid_df["_to"] = grid_df.test_id.map(order_t)
grid_df = grid_df.sort_values(["_so", "_to"]).drop(columns=["_so", "_to"]).reset_index(drop=True)
grid_df.to_csv(DATA / "atlas_grid.csv", index=False)

summary = {"spectral": SPEC_RESULTS,
           "regression": {k: {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv)
                              for kk, vv in v.items()} for k, v in REG.items()},
           "verdict_counts": grid_df[grid_df.applicable == "yes"].verdict.value_counts().to_dict(),
           "graded_cells": int((grid_df.applicable == "yes").sum()),
           "na_cells": int((grid_df.applicable == "no").sum())}
(DATA / "atlas_summary.json").write_text(json.dumps(summary, indent=2, default=str))
print("verdict counts:", summary["verdict_counts"], "| graded:", summary["graded_cells"], "| NA:", summary["na_cells"])

# ---------------------------------------------------------------- figures
COLORS = {"TESTABLE": "#2e7d32", "UNDERPOWERED": "#e6a817", "UNTESTABLE": "#b03a2e", "NA": "#d9d9d9"}
# heatmap: rows = audit rulers for S1 split, else series; cols include T3 bands separately
rows = [("S1-IMD", "Monsoon - IMD ruler"), ("S1-IITM", "Monsoon - IITM ruler"),
        ("S2", "GDP & national accounts"), ("S3", "IIP"), ("S4", "CPI Combined"), ("S5", "WPI"),
        ("S6", "Bank credit"), ("S7", "Merchandise trade"), ("S8", "State finances"),
        ("S9", "PLFS unemployment"), ("S10", "CGWB groundwater")]
cols = [("T1", "Kitchin"), ("T2", "Juglar"), ("T3E", "Monsoon\nENSO"), ("T3S", "Monsoon\nsolar"),
        ("T3L", "Monsoon\nlong"), ("T4", "Phillips"), ("T5", "Okun"), ("T6", "Political\nbudget cycle"),
        ("T7", "Conver-\ngence"), ("T8", "Taylor /\nr*")]
def cell_verdict(row_id, col_id):
    if col_id.startswith("T3"):
        if row_id == "S1-IMD":
            return SPEC_RESULTS["S1-IMD"][BANDS3[["T3E","T3S","T3L"].index(col_id)]]["verdict"]
        if row_id == "S1-IITM":
            return SPEC_RESULTS["S1-IITM"][BANDS3[["T3E","T3S","T3L"].index(col_id)]]["verdict"]
        return "NA"
    if row_id.startswith("S1"):
        return "NA"
    sel = grid_df[(grid_df.series_id == row_id) & (grid_df.test_id == col_id)]
    if len(sel) == 0:
        return "NA"
    r = sel.iloc[0]
    return r["verdict"] if r["applicable"] == "yes" else "NA"

fig, ax = plt.subplots(figsize=(11, 6.2))
M = np.zeros((len(rows), len(cols)))
for i, (rid, _) in enumerate(rows):
    for j, (cid, _) in enumerate(cols):
        v = cell_verdict(rid, cid)
        M[i, j] = {"TESTABLE": 0, "UNDERPOWERED": 1, "UNTESTABLE": 2, "NA": 3}[v]
from matplotlib.colors import ListedColormap
cmap = ListedColormap([COLORS["TESTABLE"], COLORS["UNDERPOWERED"], COLORS["UNTESTABLE"], COLORS["NA"]])
ax.imshow(M, cmap=cmap, vmin=0, vmax=3, aspect="auto")
for i, (rid, _) in enumerate(rows):
    for j, (cid, _) in enumerate(cols):
        v = cell_verdict(rid, cid)
        ax.text(j, i, {"TESTABLE": "TESTABLE", "UNDERPOWERED": "UNDERPWRD",
                       "UNTESTABLE": "UNTESTABLE", "NA": "n/a"}[v],
                ha="center", va="center", fontsize=6.3,
                color="white" if v in ("TESTABLE", "UNTESTABLE") else "#555555")
ax.set_xticks(range(len(cols))); ax.set_xticklabels([c[1] for c in cols], fontsize=8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[1] for r in rows], fontsize=8.5)
ax.set_title("Testability Atlas - verdict grid (grades the ruler, not the theory)", fontsize=11)
fig.tight_layout(); fig.savefig(FIG / "fig_atlas_heatmap.png", dpi=150); plt.close(fig)

# clean-span timeline
spans = [("Monsoon - IITM", 1871, 2016, 1871, 2016), ("Monsoon - IMD", 1901, 2026, 1901, 2025),
         ("GDP (quarterly)", 1996, 2026, 2011.5, 2025.75), ("IIP", 1994, 2026, 2012.25, 2026.25),
         ("CPI Combined", 2011, 2026, 2011, 2025.99), ("WPI", 1995, 2026, 2012.25, 2026.33),
         ("Bank credit", 1997, 2026, 2003.17, 2025.83), ("Merchandise trade", 2000, 2026, 2000.25, 2026.25),
         ("State finances (e-States)", 1990.75, 2026, 1990.75, 2024.25),
         ("PLFS (annual)", 2017.5, 2025.5, 2017.5, 2024.5), ("CGWB waves", 2009, 2025, 2017, 2025)]
fig, ax = plt.subplots(figsize=(11, 5.4))
for i, (label, f0, f1, c0, c1) in enumerate(spans):
    y = len(spans) - i
    ax.barh(y, f1 - f0, left=f0, height=0.52, color="#cfd8dc", label="published span (spliced where applicable)" if i == 0 else None)
    ax.barh(y, c1 - c0, left=c0, height=0.52, color="#1a5276", label="clean span (single base / method)" if i == 0 else None)
ax.set_yticks([len(spans) - i for i in range(len(spans))])
ax.set_yticklabels([s[0] for s in spans], fontsize=8.5)
ax.set_xlim(1865, 2030); ax.set_xlabel("year")
ax.set_title("Testability Atlas - published span vs clean span per series", fontsize=11)
ax.legend(fontsize=8, loc="lower right")
fig.tight_layout(); fig.savefig(FIG / "fig_atlas_spans.png", dpi=150); plt.close(fig)
print("figures written")
