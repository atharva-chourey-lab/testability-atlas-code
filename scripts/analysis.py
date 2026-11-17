#!/usr/bin/env python3
"""Pilot analysis, exactly as registered in PREREGISTRATION.md.

- Spectra: Hann-tapered periodogram of the demeaned, linear-detrended series.
- Null: 2,000 AR(1) surrogates (rho, sd from the preprocessed series; seed 42),
  each demeaned+detrended identically. Band statistic = maximum power in band.
  Verdict 'supported' iff empirical p < 0.05.
- R/S Hurst: classic rescaled range, windows 8..n/2, secondary check only.
Run after scripts/fetch_data.py. Regenerates figures/ and data/results_*.csv/json.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal

ROOT = Path(__file__).resolve().parent.parent
DATA, FIG = ROOT / "data", ROOT / "figures"
FIG.mkdir(exist_ok=True)
NSIM, SEED = 2000, 42

H1_BANDS = {"ENSO 2-7yr": (2.0, 7.0), "Solar 9.5-12.5yr": (9.5, 12.5),
            "Long 17-21yr": (17.0, 21.0)}
H2_BANDS = {"Kitchin 3-5yr": (36.0, 60.0), "Juglar 7-11yr": (84.0, 132.0)}


def detrend_demean(x):
    x = np.asarray(x, float)
    t = np.arange(len(x))
    b, a = np.polyfit(t, x, 1)
    return x - (a + b * t)


def ar1_surrogates(x, nsim=NSIM, seed=SEED):
    rho = np.corrcoef(x[:-1], x[1:])[0, 1]
    sd = x.std(ddof=1)
    rng = np.random.default_rng(seed)
    n = len(x)
    innov = rng.normal(0, sd * np.sqrt(max(1 - rho ** 2, 1e-6)), (nsim, n + 200))
    surr = np.zeros((nsim, n + 200))
    for t in range(1, n + 200):
        surr[:, t] = rho * surr[:, t - 1] + innov[:, t]
    return surr[:, 200:], rho


def spectrum(x):
    # Zero-padded FFT grid (8x) interpolates the spectrum so pre-declared bands
    # always contain grid points even at small n; it adds no information and is
    # applied identically to the real series and every surrogate.
    f, p = signal.periodogram(x, fs=1.0, window="hann", scaling="spectrum",
                              nfft=8 * len(x))
    return f, p


def band_tests(x_raw, bands, label, hypothesis):
    """x_raw: series before preprocessing. Returns (rows, plotdata)."""
    x = detrend_demean(x_raw)
    f, p = spectrum(x)
    surr, rho = ar1_surrogates(x)
    surr_p = np.array([spectrum(detrend_demean(s))[1] for s in surr])
    env95 = np.percentile(surr_p, 95, axis=0)
    rows = []
    for band, (plo, phi) in bands.items():
        m = (f >= 1.0 / phi) & (f <= 1.0 / plo) & (f > 0)
        real_max = p[m].max()
        peak_period = 1.0 / f[m][np.argmax(p[m])]
        null_max = surr_p[:, m].max(axis=1)
        pval = float((null_max >= real_max).mean())
        rows.append({
            "hypothesis": hypothesis, "series": label, "n": len(x),
            "band": band, "peak_period": round(float(peak_period), 2),
            "peak_power": float(real_max),
            "null95_bandmax": float(np.percentile(null_max, 95)),
            "p_value": pval,
            "verdict": "supported" if pval < 0.05 else "not supported",
            "ar1_rho": round(float(rho), 3),
        })
    return rows, (f, p, env95)


def hurst_rs(x_raw):
    x = detrend_demean(x_raw)
    n = len(x)
    sizes = np.unique(np.round(np.logspace(np.log10(8), np.log10(n // 2), 18)).astype(int))
    rs_mean = []
    for s in sizes:
        vals = []
        for start in range(0, n - s + 1, s):
            chunk = x[start:start + s]
            z = np.cumsum(chunk - chunk.mean())
            r = z.max() - z.min()
            sd = chunk.std(ddof=1)
            if sd > 0:
                vals.append(r / sd)
        rs_mean.append(np.mean(vals))
    slope, _ = np.polyfit(np.log(sizes), np.log(rs_mean), 1)
    return float(slope)


def plot_spectrum(plotdata, bands, title, path, period_max):
    f, p, env95 = plotdata
    period = np.where(f > 0, 1.0 / np.where(f == 0, np.inf, f), np.inf)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for (plo, phi), col in zip(bands.values(), ["#cfe8cf", "#fdeec9", "#f9d5d5"]):
        ax.axvspan(plo, phi, color=col, alpha=0.7)
    ax.plot(period[1:], p[1:], color="#1a5276", lw=1.4, label="periodogram")
    ax.plot(period[1:], env95[1:], color="#b03a2e", lw=1.2, ls="--",
            label="AR(1) null, 95th pct per frequency")
    ax.set_xlim(1.5, period_max)
    ax.set_xlabel("period (years)" if period_max < 60 else "period (months)")
    ax.set_ylabel("power (Hann periodogram, spectrum scaling)")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    results, extra = [], {}

    # ---------------- H1 primary: IMD Pune All-India + regions, 1901-2025
    imd = pd.read_csv(DATA / "rainfall_imd_regions.csv")
    imd_p = imd[imd.year <= 2025]
    pd_ai = None
    for region, g in imd_p.groupby("region"):
        g = g.sort_values("year")
        rows, pd_ = band_tests(g["jjas"].values, H1_BANDS,
                               f"IMD JJAS {region} 1901-2025", "H1")
        for r in rows:
            r["span"] = "1901-2025"
        results += rows
        if region == "All-India":
            pd_ai = pd_
            plot_spectrum(pd_, H1_BANDS,
                          "H1 — All-India SW monsoon (IMD, 1901–2025): spectrum vs AR(1) red-noise null",
                          FIG / "fig_h1_allindia_imd.png", 40)
    # regions figure (4 panels)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, (region, g) in zip(axes.flat,
                               [(r, g) for r, g in imd_p.groupby("region") if r != "All-India"]):
        g = g.sort_values("year")
        _, (f, p, env95) = band_tests(g["jjas"].values, H1_BANDS, region, "H1")
        period = 1.0 / f[1:]
        ax.plot(period, p[1:], color="#1a5276", lw=1.2)
        ax.plot(period, env95[1:], color="#b03a2e", lw=1.0, ls="--")
        ax.set_xlim(1.5, 40)
        ax.set_title(region, fontsize=10)
        ax.set_xlabel("period (years)")
    fig.suptitle("H1 — IMD homogeneous regions, JJAS 1901–2025 (dashed = AR(1) null 95th pct)")
    fig.tight_layout()
    fig.savefig(FIG / "fig_h1_regions_imd.png", dpi=150)
    plt.close(fig)

    # sensitivity: All-India including the 2026 row present in the source
    g26 = imd[imd.region == "All-India"].sort_values("year")
    rows26, _ = band_tests(g26["jjas"].values, H1_BANDS, "IMD JJAS All-India 1901-2026", "H1-sens")
    extra["allindia_incl_2026"] = {r["band"]: (r["verdict"], r["p_value"]) for r in rows26}

    # ---------------- H1 sensitivity: IITM All-India 1871-2016 + subdivisions
    iitm_reg = pd.read_csv(DATA / "rainfall_iitm_regions.csv")
    ai = iitm_reg[iitm_reg.region.str.startswith("ALL-INDIA")].sort_values("year")
    rows, _ = band_tests(ai["jjas"].values, H1_BANDS, "IITM JJAS All-India 1871-2016", "H1-sens")
    for r in rows:
        r["span"] = "1871-2016"
    results += rows

    sub = pd.read_csv(DATA / "rainfall_iitm_subdivisions.csv")
    sub["name"] = (sub["subdivision"].str.replace(r"^\s*\d+\.", "", regex=True)
                   .str.replace("SUBDIVISION", "").str.split(" Area").str[0]
                   .str.strip().str.replace(r"\s+", " ", regex=True))
    wanted = ["COASTAL KARNATAKA", "WEST RAJASTHAN", "EAST MADHYA P", "ASSAM & MEGHALAYA"]
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, name in zip(axes.flat, wanted):
        g = sub[sub.name == name].sort_values("year")
        rows, (f, p, env95) = band_tests(g["jjas"].values, H1_BANDS,
                                         f"IITM JJAS {name.title()} 1871-2016", "H1-sens")
        for r in rows:
            r["span"] = "1871-2016"
        results += rows
        period = 1.0 / f[1:]
        ax.plot(period, p[1:], color="#1a5276", lw=1.2)
        ax.plot(period, env95[1:], color="#b03a2e", lw=1.0, ls="--")
        ax.set_xlim(1.5, 40)
        ax.set_title(name.title(), fontsize=10)
        ax.set_xlabel("period (years)")
    fig.suptitle("H1 sensitivity — IITM subdivisions, JJAS 1871–2016 (dashed = AR(1) null 95th pct)")
    fig.tight_layout()
    fig.savefig(FIG / "fig_h1_subdivisions_iitm.png", dpi=150)
    plt.close(fig)

    # Welch sensitivity for the primary H1 series (registered as sensitivity only)
    ai_imd = imd_p[imd_p.region == "All-India"].sort_values("year")

    def welch_band_verdicts(x_raw):
        x = detrend_demean(x_raw)
        fw, pw = signal.welch(x, fs=1.0, window="hann", nperseg=40,
                              noverlap=20, nfft=8 * 40)
        surr, _ = ar1_surrogates(x, nsim=500)
        sp = []
        for s in surr:
            _, p_ = signal.welch(detrend_demean(s), fs=1.0, window="hann",
                                 nperseg=40, noverlap=20, nfft=8 * 40)
            sp.append(p_)
        sp = np.array(sp)
        out = {}
        for band, (plo, phi) in H1_BANDS.items():
            m = (fw >= 1.0 / phi) & (fw <= 1.0 / plo) & (fw > 0)
            pv = float((sp[:, m].max(axis=1) >= pw[m].max()).mean())
            out[band] = ("supported" if pv < 0.05 else "not supported", pv)
        return out

    extra["welch_sensitivity_allindia_imd"] = welch_band_verdicts(ai_imd["jjas"].values)

    # R/S Hurst benchmarked against same-rho AR(1) surrogates (bias check)
    def hurst_surrogate_check(x_raw, label):
        x = detrend_demean(x_raw)
        surr, rho = ar1_surrogates(x, nsim=200, seed=7)
        hs = [hurst_rs(s) for s in surr]
        real = hurst_rs(x_raw)
        return {"H": real, "surr_mean": float(np.mean(hs)),
                "surr_p95": float(np.percentile(hs, 95)),
                "p_H_above_surr": float((np.array(hs) >= real).mean())}

    extra["hurst_surrogate_check"] = {
        "IMD All-India JJAS 1901-2025": hurst_surrogate_check(ai_imd["jjas"].values, "imd"),
        "IITM All-India JJAS 1871-2016": hurst_surrogate_check(ai["jjas"].values, "iitm"),
    }

    # ---------------- R/S Hurst (secondary, registered)
    ai_imd = imd_p[imd_p.region == "All-India"].sort_values("year")
    extra["hurst"] = {
        "IMD All-India JJAS 1901-2025": hurst_rs(ai_imd["jjas"].values),
        "IITM All-India JJAS 1871-2016": hurst_rs(ai["jjas"].values),
    }
    extra["monsoon_means_mm"] = {
        "IMD 1901-2025": float(ai_imd["jjas"].mean()),
        "IITM 1901-2016 (overlap)": float(ai[(ai.year >= 1901)]["jjas"].mean()),
        "IMD 1901-2016 (overlap)": float(ai_imd[ai_imd.year <= 2016]["jjas"].mean()),
    }
    # two-rulers check on identical years: mean abs difference of JJAS totals
    merged = ai_imd[ai_imd.year <= 2016][["year", "jjas"]].merge(
        ai[["year", "jjas"]], on="year", suffixes=("_imd", "_iitm"))
    extra["imd_vs_iitm_overlap"] = {
        "mean_abs_diff_mm": float((merged.jjas_imd - merged.jjas_iitm).abs().mean()),
        "corr": float(np.corrcoef(merged.jjas_imd, merged.jjas_iitm)[0, 1]),
    }

    # time-series figure (two official All-India series)
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(ai_imd.year, ai_imd.jjas, color="#1a5276", lw=1.2, label="IMD Pune operational, 1901–2025")
    ax.plot(ai.year, ai.jjas, color="#b03a2e", lw=1.0, ls="--", label="IITM homogeneous, 1871–2016")
    ax.set_ylabel("JJAS rainfall (mm)")
    ax.set_title("All-India SW monsoon — two official series")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_monsoon_series.png", dpi=150)
    plt.close(fig)

    # ---------------- H2: IIP (chosen per registered rule; see REPORT.md)
    iip = pd.read_csv(DATA / "iip_general_monthly.csv", parse_dates=["date"])
    iip = iip.sort_values("date")
    dates = pd.date_range(iip.date.min(), iip.date.max(), freq="MS")
    extra["iip"] = {"n_months": int(len(iip)), "span": f"{iip.date.min():%Y-%m} to {iip.date.max():%Y-%m}",
                    "missing_months": int(len(dates) - len(iip))}
    growth = 100 * np.log(iip["index"].values[1:] / iip["index"].values[:-1])
    months = iip["month"].values[1:]
    deseas = growth.copy()
    for m in range(1, 13):
        deseas[months == m] -= growth[months == m].mean()
    rows, pd_iip = band_tests(deseas, H2_BANDS, "IIP General log-growth, deseasonalised", "H2")
    for r in rows:
        r["span"] = extra["iip"]["span"]
        r["peak_period"] = round(r["peak_period"], 1)  # months
    results += rows
    plot_spectrum(pd_iip, H2_BANDS,
                  "H2 — IIP monthly growth (MoSPI, Apr 2012–Mar 2026): spectrum vs AR(1) null",
                  FIG / "fig_h2_iip.png", 200)

    out = pd.DataFrame(results)
    out.to_csv(DATA / "results_band_tests.csv", index=False)
    (DATA / "results_extra.json").write_text(json.dumps(extra, indent=2))
    print(out.to_string(index=False))
    print(json.dumps(extra, indent=2))


if __name__ == "__main__":
    main()
