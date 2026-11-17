# Assessment — Turning the Limitation into the Product, and the Water Arm

**Date:** 2026-11-17 · **Status:** local assessment, nothing published · **Basis:** pilot `REPORT.md` (registered spectral pilot: monsoon/IIP cycles not supported, political frequency untestable at annual frequency, IMD-vs-IITM monsoon rulers split ≈5%) plus live source/literature checks run for this assessment. Every dataset named below was verified to exist at the cited source; every novelty claim names its closest published neighbour.

**Atharva's two directions assessed:** (1) the pilot's limitation — India's headline series are short, re-based, and ruler-dependent — is itself valuable and should be made into a product; (2) theory-contrast analyses on Indian data, with a water-economics arm (Shah's groundwater thesis) as the named example.

**Grid used for every candidate:** the claim · data actually obtainable · statistical power · novelty scrub · rank.

---

## A. The Testability Atlas — "the limitation as the finding"

**Claim.** For each of India's major official series, compute — not assert — what the series can and cannot support: usable span, base-year breaks, cross-ruler gaps where two official rulers exist, revision behaviour where documented, and a *minimum detectable effect* (for cycle tests: the smallest band amplitude that would clear the pilot's registered AR(1)-surrogate test at that n and variance; for panel/regression uses: the smallest interaction detectable at conventional power). End in a verdict table: named theory × Indian series → **TESTABLE / UNDERPOWERED / UNTESTABLE**, with the reason in one line each.

**Data obtainable.** This is a metadata-plus-series build, and almost all of it is already proven reachable by the pilot or documented in public sources:

| Series | Usable span / frequency | Known breaks & ruler problems (documented) |
|---|---|---|
| GDP / national accounts | Quarterly from 1996 on spliced bases; annual longer | Base revisions 2004-05 → 2011-12 (2015, MCA-21 + SNA-2008) → 2022-23 base released Feb 2026 with back series initially pending; IMF Article IV data-adequacy grade for national accounts: **"C"** (2024 and 2025 reviews) |
| IIP | Monthly; pilot pulled base 2011-12, Apr 2012–Mar 2026, n=168, complete | Bases 2004-05 → 2011-12 → 2022-23 (new series from Jun 2026); splicing is the user's problem, no official continuous long series |
| CPI | Combined CPI only from 2011 (base 2012), new base 2024 from Feb 2026; CPI-IW longer but a different basket/ruler | The inflation-targeting era (2016–) has ~10 years on one ruler |
| WPI | Monthly, long (successive bases back decades) | Measures wholesale, not consumer, prices; used as GDP deflator proxy — one of the IMF's stated "C"-grade reasons |
| Bank credit (SCB) | Fortnightly/monthly, RBI, long | Among the cleanest long series; sectoral deployment shorter |
| Merchandise trade | Monthly, long (DGCIS) | Valuation/partner revisions; less re-basing damage than GDP/IIP |
| Rainfall | Annual JJAS 1871–2016 (IITM) / 1901–2025 (IMD), n=125–146 | Two official rulers split ≈5% in level and disagree on Hurst (pilot §2) — a measured cross-ruler gap, not a rumour |
| State finances | Annual, ~30–45 years, ~28 major states (RBI *State Finances*) | Annual only → spectral political-cycle tests unresolvable (pilot §4); regression designs unaffected |
| PLFS / unemployment | Annual 2017-18–, quarterly urban; monthly from 2025 | Predecessor EUS rounds are quinquennial and not like-for-like; the unemployment *time series* effectively restarts in 2017 |

**Power.** The atlas *is* the power calculation, so its own power question is whether the MDES numbers are computable — they are, with the pilot's exact machinery (surrogate band tests per series; standard panel power formulas per regression use). Illustrative anchors the atlas would formalise: a Juglar-band (7–11 yr) cycle needs ≥4–5 complete cycles → ≥35–55 years of clean data, which **no** post-2011-12-base Indian macro series has; the monsoon (n=125–146) is the only headline series where the pilot's null is genuinely informative rather than a power artefact; state panels invert the problem — n≈28 states × 40 years is ample for *regression* contrasts (Khemani) while remaining hopeless for *spectral* ones.

**Novelty scrub — the honest part.** Qualitative audits of Indian statistics **exist and are prominent**: Subramanian (Harvard CID WP 354, 2019) estimated post-2011-12 GDP growth overstatement of ≈2.5 pp/yr via 17 cross-check indicators; the IMF's "C" grade for national accounts; the 2018 back-series dispute (NSC sub-committee vs CSO/NITI release); the 2019 NSC resignations over the withheld PLFS 2017-18 and the suppressed CES 2017-18; a delayed decennial census (2011 is still the last completed). **What does not exist** (no equivalent found in this check): a *computed, per-series, per-theory testability table* — MDES/minimum-detectable-cycle numbers attached to named theories, built uniformly, with the cross-ruler gaps measured on the same grid (the pilot's IMD/IITM 5% is the prototype cell). The existing literature argues about whether one series (GDP) is *wrong*; the atlas would state, for ~10 series × ~7 theories, whether each question is *askable at all* on official data, and at what effect size. That is a different product, and it is citable precisely because it ends arguments rather than joining them.

**Verdict: RANK 1 — recommended next build** (see §F). Cheap (weeks, mostly metadata + series already in hand), fully in the lab's registered-null style, and its power tables are a required input to pre-registering B and D honestly.

---

## B. Water Arm 1 — Groundwater as insurance: testing Shah's thesis

**Claim (testable form of Shah, *Taming the Anarchy*, 2009).** India's irrigation economy became atomistic-groundwater: millions of private wells decoupled farm output from canal schedules and rainfall timing. Two-sided prediction, both halves required:
1. **Insurance half:** districts with higher groundwater development show *weaker* sensitivity of crop outcomes (yield/production) to rainfall shocks.
2. **Depletion half:** the same districts pay for it — stage of extraction rises faster, and rises *in response to* dry years (pumping is the smoothing mechanism), so buffering today predicts extraction stress tomorrow, sharply where stage already exceeds 100%.

A build that tests only half 1 is a replication; the joint test is the claim.

**Data obtainable (verified).**
- **CGWB *Dynamic Ground Water Resources* (GWRA):** national + state reports are published PDFs on cgwb.gov.in, block-level stage of extraction. Assessment waves: **2009, 2013 (GEC-97 method), then 2017, 2020, 2022, 2023, 2024, 2025 (GEC-2015)** — CGWB's own state reports confirm the GEC-97→GEC-2015 switch at the 2017 assessment and annual assessments since 2022. So: ~7,000 blocks × 8 waves exist on paper, but (a) pre/post-2017 values are **not like-for-like** (method break must be modelled or the panel restricted to 2017–), and (b) extraction from PDFs is labour, the same shape as the vintages archive.
- **Outcomes:** ICRISAT District-Level Database (data.icrisat.org) — apportioned panel, 311 districts × 1966-67–2011-12, crop area/production/yield for 20 crops, source-wise irrigation (canals/tanks/wells), monthly rainfall; unapportioned versions extend coverage (a 560-district 1990–2015 merge is in circulation). DES district crop statistics 1997–2019 are on data.gov.in (resource 35be999b-0208-4354-b557-f6ca9a5355de, GODL-India) — this is the series that overlaps the CGWB waves.
- **Rainfall:** already in this project (IMD/IITM), plus IMD gridded district rainfall via data.gov.in.
- **Join reality check:** CGWB is block-level, outcomes are district-level → exposure must be aggregated to district (mean stage; share of blocks over-exploited; max). NFHS/PLFS district outcomes are joinable in principle but are survey rounds, not annual panels — secondary outcomes only.

**Power.** District panel: ~300 (ICRISAT, long) to ~600 (DES 1997–2019) districts × 20+ years, with rainfall shocks varying by district-year. Interaction designs (rainfall shock × groundwater development) on panels this size routinely detect sensitivity differences of a few percent of yield — comfortably below the effect sizes the literature reports (Sekhri's poverty effects are 9–10 pp at a depth discontinuity; Fishman et al.'s depletion effects are first-order). The binding constraint is **not** n; it is the CGWB side: effectively 3 pre-2020 GEC-2015 waves (2017, 2020) + annual 2022–25, and block→district aggregation noise. Depletion-half regressions (Δstage on dry-year dummies × baseline development) have ~600 districts × ~5 usable waves — adequate for the sign and rough size, not for fine dynamics.

**Novelty scrub — crowded field, one surviving seam.**
- Jayachandran (JPE 2006): rainfall-instrumented productivity → wages, 257 districts 1956–87; wage responsiveness varies with banks/migration costs. Rainfall→outcome sensitivity in India is *hers* (and Kaur 2019's).
- Sekhri (AEJ:Applied 2014): groundwater *access* (8 m depth discontinuity) → poverty −9–10 pp, +conflict; long-run technology adoption. Cross-sectional access effects are *hers*.
- Fishman, Jain & Kishore ("When Water Runs Out", 2017; Fishman et al. 2011/2017 line): geological variation in depletion rates in Gujarat → irrigated area decline, outmigration, failed compensating investment. Depletion→adaptation is *theirs*.
- Rosenzweig & Wolpin (1993, bullocks/credit constraints) and Paxson (1992, Thailand) own the general "assets smooth transitory weather income" frame; Blakeslee et al. (JDE 2023) own the dam-irrigation spatial-development version; Basavappa & Pommer Muñoz (2026 WP) test extraction-smoothing in drought years directly, at farm level, around a micro-irrigation subsidy in western India — the closest living neighbour to half 2's mechanism.
- Shah's own IWMI empirical work documents the atomistic transition descriptively; he does not run the joint district-panel test above.

**What would actually be new, stated exactly:** (i) CGWB *stage of extraction* used as a **time-varying district exposure** (prior work uses depth, geology, or well counts — not the official extraction-stage panel, because until the 2017–2025 waves it barely existed as a panel); (ii) the **insurance and depletion halves estimated in one system on the same districts**, so the trade-off Shah asserts is measured as a trade-off, with the dry-year pumping response as the linking coefficient; (iii) the post-2013 period, which none of the named papers cover. If the build cannot deliver (i)+(ii), it should not be built — it would be a Jayachandran/Sekhri re-run with newer wallpaper.

**Verdict: RANK 2** — the flagship *theory* build. Highest scientific payoff of any candidate here; data real but the CGWB extraction + method-break handling is the cost; pre-registration must fix the aggregation and the GEC break rule in advance (§F).

---

## C. Water Arm 2 — Geography contrast: paddy where the water isn't

**Claim.** Endowment-based trade theory (Allan's virtual water; Heckscher–Ohlin applied to water) predicts water-intensive production locates where water is abundant. India inverts it: paddy concentrated in Punjab/Haryana, whose CGWB stage of extraction is **≈156% (Punjab) and ≈137% (Haryana) against ≈61% nationally** (GWRA 2024/2025 figures, confirmed in parliamentary answers citing CGWB: Punjab 156.36%, 111 of 153 blocks over-exploited; Haryana ≈136–137%).

**Data obtainable.** Everything in B, plus state crop shares (DES/ICRISAT) — the descriptive accounting is a by-product of B's dataset.

**Novelty scrub — this one is done.** Verma, Kampman, van der Zaag & Hoekstra (Physics & Chemistry of the Earth, 2009, "Going against the flow") already quantified inter-state virtual-water flows for India and concluded, in almost these words, that flows *exacerbate* scarcity in water-scarce states and are driven by non-water factors (per-capita cropped area, market access) rather than endowments. Chopra & Behera (2021) extended interstate virtual-water accounting for wheat/rice over 1994–2017; network-analysis versions exist as recently as 2026 conference work. The "India exports virtual water uphill" fact is established, repeatedly.

**What would be new:** only the *causal/policy* layer — estimating how much of the inversion is procurement/MSP-and-free-power driven vs agro-climatic — and that is a different (harder, instrument-hungry) project that properly sits inside B's cropping-margin analysis, not as a standalone build.

**Verdict: RANK 4** — a chapter of B, not a build. Do not headline it; Verma et al. 2009 is the headline and it is 17 years old.

---

## D. Revisions / Vintages (REPORT §5's rank 1) vs the Atlas

One paragraph, as briefed: the Atlas does **not** subsume the vintages build, and the vintages build should no longer go first. The Atlas *precedes* it and contains its scoping chapter — per-series revision behaviour as documented (e.g. GDP's multi-year revision ladder, IIP's monthly revisions) plus the MDES framing that tells you how large a revision pattern must be to be distinguishable from noise. But the vintages *dataset* (first-release vs each revision vs final, extracted from press-release back-files) is a construction project the Atlas neither builds nor replaces; it remains the flagship *dataset* build, now sequenced second, with its pre-registration inheriting the Atlas's per-series power numbers instead of guessing them. Order: **Atlas (scope + verdicts) → Vintages (dataset)**, with B's pre-registration drafted off the same Atlas tables.

---

## E. Broader theory contrasts — brief scrub

- **Phillips curve / sacrifice ratio (India):** done, by the RBI itself and after — RBI (2002) sacrifice ratio ≈2; Kapur & Patra (2003) 0.5–4.7; Dholakia (2014) ≈1.8–2.8; RBI WP 01/2026 re-estimates it time-varying (≈2.3–2.8). **No seam.**
- **Taylor rule / natural rate (India):** done — RBI Bulletin work (Pattanaik, Behera & Sharma 2022; Behera 2026 update: r* 1.4–1.9% for Q4 2023-24) estimates the full NK system (IS + Phillips + Taylor) on Indian data as a matter of routine. **No seam.**
- **Okun's law (India):** the one partial survivor — and it survives as an *Atlas cell*, not a build. India's Okun link is structurally suspect (≈90% informal/self-employed work means output shocks surface as earnings/hours, not open unemployment), the unemployment ruler itself restarted in 2017 (PLFS), and published Okun estimates for India are scattered and specification-sensitive rather than settled. Verdict: **UNDERPOWERED/UNTESTABLE pre-2017, testable only on the short PLFS window** — exactly the kind of line the Atlas exists to print. No standalone build.

---

## F. Ranking, recommendation, and the next pre-registration

**Top 3:**
1. **A — Testability Atlas.** The limitation, computed and published as the product: ~10 series × ~7 named theories, TESTABLE / UNDERPOWERED / UNTESTABLE with MDES numbers, cross-ruler gaps measured on one grid. Novel as a computed product (the existing audits are qualitative and GDP-only); cheap; gates everything else.
2. **B — Groundwater-as-insurance (Shah test).** The flagship theory contrast: joint insurance + depletion test, CGWB stage panel × DES/ICRISAT district outcomes × IMD rainfall. Novel only in the exact form stated in §B — hold that line.
3. **D — Revisions/Vintages archive.** Still the flagship dataset (no Indian ALFRED exists); sequenced after A, scoped by it.

(C is a chapter of B. E yields no build.)

**Recommended next build: A, the Testability Atlas** — with B's pre-registration drafted immediately after, off A's tables.

**What A's pre-registration must fix in advance:**
1. **The series list and the theory list** (the grid's rows and columns) — no adding a theory after seeing its verdict.
2. **The MDES machinery per test family:** for spectra, the pilot's registered rule verbatim (Hann periodogram, 2,000 AR(1) surrogates, band-max, p<0.05) with bands declared per theory *before* computing any series' MDES; for regression/panel uses, the estimator, the effect parameter, and the power formula (α, power, clustering level) per cell.
3. **The verdict thresholds:** the exact MDES cut-offs that separate TESTABLE / UNDERPOWERED / UNTESTABLE (e.g. detectable effect ≤ the smallest effect the theory's literature treats as meaningful → TESTABLE; ≤ 2× that → UNDERPOWERED; above, or n below the minimum cycles/units rule → UNTESTABLE), with the literature anchor effect size cited per theory in the registration itself.
4. **Break and ruler rules:** how base-year breaks truncate usable spans (no silent splicing), and how cross-ruler gaps are measured where two rulers exist (common-years level gap + correlation, as in the pilot's IMD/IITM cell).
5. **Revision-behaviour sourcing:** only documented revision facts (official revision calendars/studies) enter the atlas; anything requiring the vintages dataset is marked "pending D", not estimated.
6. **Language discipline:** a verdict is a statement about data and power, never about whether the theory is true — the atlas grades the *ruler*, not the theory.

*Sources for load-bearing facts above: CGWB GWRA state/national reports and parliamentary answers citing GWRA-2025 (cgwb.gov.in); ICRISAT District-Level Database documentation (data.icrisat.org; apportioned panel 1966–2011, 311 districts, 19 states); DES district crop statistics via data.gov.in resource 35be999b-0208-4354-b557-f6ca9a5355de; Subramanian, CID WP 354 (2019); IMF Article IV 2024/2025 data-adequacy grading as reported 2025–26; Kane (1990), Khemani (2004), Bose & Goyal (2020) per pilot REPORT §0; Jayachandran (JPE 2006); Sekhri (AEJ:Applied 2014); Fishman, Jain & Kishore (2017); Blakeslee et al. (JDE 2023); Verma et al. (2009); Chopra & Behera (2021); RBI WP 01/2026 and RBI Bulletin natural-rate updates (2022/2026).*
