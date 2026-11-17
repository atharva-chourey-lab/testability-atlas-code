# Data provenance

All pulls by `scripts/fetch_data.py` on 2026-11-17. All sources are Government of India.

| File | Source | Span / n | Licence / terms |
|---|---|---|---|
| `imd_pune_rainfall.html` (raw), `rainfall_imd_regions.csv` (tidy) | IMD Pune, Climate Prediction & Monitoring Group page "India (June–Sept) Rainfall" — imdpune.gov.in/cmpg/Product/Rainfall_Data.html | All-India + 4 homogeneous regions, JJAS monthly + total (mm), 1901–2026 | As published by IMD on its website; IMD is the provider to credit |
| `iitm-regionrf.txt`, `iitm-subdivrf.txt` (raw), `rainfall_iitm_regions.csv`, `rainfall_iitm_subdivisions.csv` (tidy) | IITM Pune (Ministry of Earth Sciences), "Homogeneous Indian Monthly Rainfall Data Sets" — tropmet.res.in/data/data-archival/rain/ ; underlying observations: IMD (306 stations to 2014; IMD subdivisional 2015–16) | All-India + 5 macro-regions + 30 subdivisions, monthly (0.1 mm in raw, converted to mm), 1871–2016 | IITM makes the data sets available online for scientific use; underlying data © IMD |
| `iip_raw_2011-12.json` (raw), `iip_general_monthly.csv` (tidy) | MoSPI eSankhyiki API — api.mospi.gov.in/api/iip/getIIPData (base 2011-12, monthly, type=General) | IIP General index, Apr 2012–Mar 2026, n=168, no missing months | MoSPI open API, no auth; GoI data disseminated under GODL-India via data.gov.in |

## Failed / not-used routes (recorded honestly)

- **data.gov.in** resource "Sub Divisional Monthly Rainfall 1901–2017": the portal did not return the file from this host on 2026-11-17 (page fetch failed / connection timed out). The IITM homogeneous series (IMD-sourced, longer span) was used instead for subdivisions.
- **MoSPI CPI endpoint**: without undocumented filter codes it serves only a latest-year slice (2025; totalRecords ≈ 326k across all states/groups/years). A clean All-India combined monthly pull was not obtained in pilot effort; IIP was chosen under the pre-registered rule instead.
- **mospi-esankhyiki Python package**: installed, but its metadata route failed through this host's proxy (RemoteDisconnected). The same API was used directly — identical data.
- **RBI DBIE / Handbook**: not used; interactive portal, and the registered choice rule was satisfied by MoSPI IIP.
- **IMD gridded daily rainfall (1901–2024)**: requires registration on the IMD portal; not attempted in the pilot.
