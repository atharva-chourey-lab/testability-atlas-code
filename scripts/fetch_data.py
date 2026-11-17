#!/usr/bin/env python3
"""Fetch all pilot data from official sources. Re-runnable.

Sources (all Government of India):
1. IMD Pune (imdpune.gov.in) — All-India + homogeneous-region JJAS rainfall table,
   1901-present, HTML. Licence/terms: IMD website; values as published by IMD.
2. IITM Pune (tropmet.res.in) — Homogeneous Indian Monthly Rainfall Data Sets
   1871-2016 (source data: IMD; 306 stations to 2014, IMD subdivisional 2015-16),
   plain text, values in 0.1 mm.
3. MoSPI eSankhyiki API (api.mospi.gov.in) — IIP, base 2011-12, monthly, General
   index. Open API, no auth. (GODL-India applies to data.gov.in dissemination.)

Outputs tidy CSVs into data/. Raw files are kept alongside.
"""
import io
import json
import re
import urllib.request
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}


def download(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    print(f"downloaded {url} -> {dest.name} ({dest.stat().st_size} bytes)")


# ---------------------------------------------------------------- IMD Pune table
def parse_imd_pune(html_path):
    tables = pd.read_html(str(html_path))
    out = []
    region_names = ["All-India", "North West India", "North East India",
                    "Central India", "South Peninsula"]
    used = 0
    for t in tables:
        # Each rainfall table has >=11 cols: YEAR JUN JUL AUG SEP JUN-SEP YEAR + 5 departure cols
        if t.shape[1] < 11 or t.shape[0] < 50:
            continue
        df = t.iloc[:, :6].copy()
        df.columns = ["year", "jun", "jul", "aug", "sep", "jjas"]
        df = df[pd.to_numeric(df["year"], errors="coerce").notna()]
        for c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df.dropna(subset=["jjas"])
        df["region"] = region_names[used] if used < len(region_names) else f"table{used}"
        used += 1
        out.append(df)
    res = pd.concat(out, ignore_index=True)
    return res


# ---------------------------------------------------------------- IITM text files
MONTHCOLS = ["year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
             "sep", "oct", "nov", "dec", "jf", "mam", "jjas", "ond", "ann"]


def parse_iitm(path, kind):
    """Blocks: header line naming the region/subdivision, then year rows of 18 ints (0.1 mm)."""
    rows = []
    current = None
    for line in path.read_text(errors="ignore").splitlines():
        if ("SUBDIVISION" in line or "RAINFALL" in line) and "YEAR" not in line:
            m = re.sub(r"^\s*146\s*", "", line).strip()
            if m:
                current = m
            continue
        parts = line.split()
        if len(parts) == 18 and parts[0].isdigit() and 1800 < int(parts[0]) < 2100:
            try:
                vals = [int(p) for p in parts]
            except ValueError:
                continue
            rec = dict(zip(MONTHCOLS, vals))
            rec[kind] = current
            rows.append(rec)
    df = pd.DataFrame(rows)
    for c in MONTHCOLS:
        if c != "year":
            df[c] = df[c] / 10.0  # 0.1 mm -> mm
    return df


# ---------------------------------------------------------------- MoSPI IIP
def fetch_iip():
    months = {m: i + 1 for i, m in enumerate(
        ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"])}
    raw_all, tidy = [], []
    for year in range(2012, 2027):
        rows_year, page = [], 1
        while True:
            url = ("https://api.mospi.gov.in/api/iip/getIIPData?"
                   f"base_year=2011-12&frequency=Monthly&year={year}"
                   f"&limit=200&page={page}")
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
            rows_year.extend(d.get("data", []))
            if page >= d.get("meta_data", {}).get("totalPages", 1):
                break
            page += 1
        d = {"data": rows_year}
        raw_all.extend(d.get("data", []))
        for row in d.get("data", []):
            if row.get("type") == "General" and row.get("category") == "General":
                tidy.append({"year": int(row["year"]),
                             "month": months[row["month"]],
                             "index": float(row["index"])})
        print(f"IIP {year}: {len(d.get('data', []))} rows")
    (DATA / "iip_raw_2011-12.json").write_text(json.dumps(raw_all))
    df = pd.DataFrame(tidy).sort_values(["year", "month"]).reset_index(drop=True)
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
    return df


def main():
    download("https://imdpune.gov.in/cmpg/Product/Rainfall_Data.html",
             DATA / "imd_pune_rainfall.html")
    download("https://www.tropmet.res.in/data/data-archival/rain/iitm-regionrf.txt",
             DATA / "iitm-regionrf.txt")
    download("https://www.tropmet.res.in/data/data-archival/rain/iitm-subdivrf.txt",
             DATA / "iitm-subdivrf.txt")

    imd = parse_imd_pune(DATA / "imd_pune_rainfall.html")
    imd.to_csv(DATA / "rainfall_imd_regions.csv", index=False)
    print("IMD regions:", {r: (int(g.year.min()), int(g.year.max()), len(g))
                            for r, g in imd.groupby("region")})

    reg = parse_iitm(DATA / "iitm-regionrf.txt", "region")
    reg.to_csv(DATA / "rainfall_iitm_regions.csv", index=False)
    print("IITM regions:", sorted(reg["region"].dropna().unique())[:8], "...")

    sub = parse_iitm(DATA / "iitm-subdivrf.txt", "subdivision")
    sub.to_csv(DATA / "rainfall_iitm_subdivisions.csv", index=False)
    print("IITM subdivisions:", sub["subdivision"].nunique())

    iip = fetch_iip()
    iip.to_csv(DATA / "iip_general_monthly.csv", index=False)
    print("IIP general:", iip["date"].min(), "->", iip["date"].max(), "n =", len(iip))


if __name__ == "__main__":
    main()
