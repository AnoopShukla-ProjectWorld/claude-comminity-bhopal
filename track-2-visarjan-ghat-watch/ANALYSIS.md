# Track 2 — Visarjan Ghat Watch: deep analysis

Prepared 11 Oct 2026 from every file in `track-2-visarjan-ghat-watch/`: the problem statement, the participant guide PDF, the 4 data files, the data dictionary and the 6 source PDFs. All numbers below were computed from the CSVs and cross-checked against the PDF tables. Page numbers are PDF pages in that year's MPPCB report.

---

## 1. TL;DR

- **The user:** a BMC officer planning Durga visarjan on **20 Oct 2026**, nine days from now.
- **What they need:** a ranked list of ghats by risk, a plain-words reason for each rank, every number traceable to report and page, and a short Hindi and English brief they can forward.
- **The data is good.** `bhopal_ghats_2023_2025.csv` matched the PDF tables value for value in every table I checked: 2023 p26 and p60, 2024 p71 and p72, plus the 2025 subagent check.
- **The headline claims hold.** DO is below 5 mg/l in **42 of 116** readings. BOD is above 3 mg/l in **100 of 112**. DO reads 0 four times, all at Bairagarh.
- **The draft risk order is clear.** Bairagarh kund comes out worst by a wide margin. Shahpura, Malikhedi and Rani Kamlapati follow. Prempura is consistently the cleanest.
- **The traps are mostly about data, not code:**
  - Blanks mean "not sampled", not clean.
  - BDL means very low, not zero.
  - Some 2025 metal values look like detection limits printed as numbers.
  - The 2025 Durga "after" metal values are copies of the "pre" values.
  - Two ghats have no Durga 2025 data at all.
  - No sampling dates or units appear anywhere in the reports.
- **The biggest real-world twist is the NGT ban on lake immersion.** Four of the seven ghats sit on the Upper or Lower Lake, and BMC is building new ghats with **zero history**. A good tool says that plainly and turns it into a testing recommendation.

---

## 2. Folder inventory

| Path | What it is | Verdict |
|---|---|---|
| `PROBLEM-STATEMENT.md` | Problem, data guide, rules, judging | Read first. Same content as the guide PDF |
| `Track 2 - ... Participant guide.pdf` | PDF of the above | Duplicate. Checked word by word |
| `data/bhopal_ghats_2023_2025.csv` | 1,524 rows: 7 ghats × 3 years × 2 festivals × 3 phases × 13 parameters (long format) | **Primary input.** Accurate |
| `data/sample_bhopal_2025.csv` | 453 rows, the 2025 subset of the file above | For quick tests only |
| `data/mp_immersion_sites_2023_2025.csv` | 21,600 rows, about 400 site-name variants across MP | Background only. Noisy (see §6) |
| `data/cpcb_water_quality_criteria.csv` | 19 rows, CPCB classes A–E | Use class B (bathing) as the yardstick |
| `data/DATA_DICTIONARY.md` | Columns, codes, ghats | Accurate |
| `resources/Idol_immer._Report_23_CPCB.pdf` | MPPCB 2023, 87 pp. Ganesh p26–28, Durga p58–61 | Source of truth |
| `resources/Ganesh_and_Durga_visarjan_report-2024.pdf` | MPPCB 2024, 118 pp. **Durga first** (p22–26), Ganesh p69–73 | Source of truth |
| `resources/Ganesh_and_Durga_visarjan_report-2025.pdf` | MPPCB 2025, 92 pp. Ganesh p28–30, Durga p63–65. Footnote legend on p62 and p92 | Source of truth |
| `resources/Bhopal-2023-24_upper_lake.pdf` | Monthly Upper Lake monitoring, 6 stations, with coliform | Baseline context |
| `resources/Upper_Lower_Lake_monthly_2025-26_from_xgn.pdf` | Monthly 2025-26. Includes the **only Lower Lake station** (Kalighat) | Baseline context |
| `resources/comparatives-uppe-lak-lower-lake-2003-2023.pdf` | Upper Lake station sheets for 20 years. **Mis-titled: no Lower Lake data** | Long-term trend |

**PDF tip:** `pdftotext -layout` scrambles the "after one week" columns in these reports. Use `pdftotext -table` (or `-raw`) if you parse anything yourself. The provided CSV does not have this problem.

---

## 3. Shape of the Bhopal dataset

- **Rows by year:** 2023 has 525, 2024 has 546, 2025 has 453. Ganesh has 819 and Durga 705.
- **Parameters:** 13. Suspended solids is absent from Durga 2023 and Durga 2025, which leaves 84 rows instead of 120. You can work it out as TS − TDS; that identity holds exactly in the Ganesh tables.
- **No duplicate keys** on year + festival + site + phase + parameter.
- **Encoding:** the conductivity unit is UTF-8 `µS/cm`. Read the file as UTF-8, or Windows tools will show `�S/cm`.

### Coverage gaps (the "honest about missing data" criterion)

| Gap | Rows | Source |
|---|---|---|
| **Durga 2025 is entirely missing for Bairagarh and Malikhedi.** The rows don't exist at all, so a naive groupby won't flag them | 0 rows (should be 2 × 36) | No table in the report and no reason given |
| Ganesh 2025, Bairagarh and Malikhedi: only the "during" phase was sampled. Pre and after are `*` / `**` / blank | 52 cells | Legend p62: "*" means the temporary kund wasn't built yet at pre-sampling; "**" means it had been dismantled by post-sampling |
| Prempura, Durga 2023: BOD missing in all three phases, pH missing for "during" | 4 | `_` in the PDF, p60 |
| Khatlapura, Durga 2023: BOD missing for "during" | 1 | `_`, p59 |
| Khatlapura, Ganesh 2023: all 4 metals missing for "during" | 4 | `_`, p26 |

Each site has 234 possible cells. Usable readings (numbers plus BDL):

- Hathaikheda, Shahpura, Rani Kamlapati: 228
- Prempura: 224
- Khatlapura: 223
- **Bairagarh and Malikhedi: 166 each**

This means the two worst-looking sites are also the least sampled. The tool has to say both things.

### BDL and look-alike detection limits

- **BDL counts:** 174 in total. Chromium has 65, lead 52, copper 36 and zinc 21.
- **Chromium:** BDL at every site and phase in Ganesh 2023 and Durga 2023, so there is no numeric chromium for 2023 at all.
- **Durga 2024:** all four metals are BDL at all 7 ghats in every phase. Ganesh 2024, the same year, has the *highest* metal values in the dataset, even pre-immersion. The two campaigns probably used different labs or detection limits. **Do not read this as Durga being cleaner.**
- **Ganesh 2025:** lead is **0.031** and chromium **0.03** in every cell at every site. Copper is 0.018 in many cells. In Durga 2025, chromium "0.03" turns into "BDL" in the next column (p64). These are almost certainly **detection limits printed as numbers**. Treat them as "≤ value", not as measurements.
- **Durga 2025 metals:** the "after" value is identical to "pre" at all 5 sites (e.g. Shahpura zinc 0.60 / 0.03 / 0.60, p65). This looks like copy-paste. Don't treat "after" as independent.

**Conclusion on metals:** usable only for Ganesh 2024, and partly for 2023 lead, zinc and copper. With no CPCB class-B metal limits either, **don't let metals drive the ranking.** Show them as context.

---

## 4. Findings against the CPCB limits

Class B (organised outdoor bathing) is the right yardstick for an immersion ghat where people stand in the water: DO ≥ 5 mg/l, BOD ≤ 3 mg/l, pH 6.5–8.5. Class D (wildlife and fisheries, DO ≥ 4) is a useful second line.

### Overall (Bhopal, 2023–25)

| Test | Fails | Notes |
|---|---|---|
| DO < 5 (class B) | **42 / 116** (36%) | DO < 4 (fails class D too): 17. DO = 0: 4, all Bairagarh |
| BOD > 3 (class B) | **100 / 112** (89%) | Median BOD 6.4, maximum 22 (Hathaikheda, Ganesh 2024 after) |
| pH outside 6.5–8.5 | 6 / 115 | Highest 9.20 (Hathaikheda, Durga 2024 pre, p23). Lowest 6.49 (Khatlapura, Ganesh 2024 during, p69) |
| Conductivity > 2,250 (class E) | 0 / 116 | Highest 1,882 (Bairagarh, Durga 2023 after) |

The four DO = 0 readings are all at Bairagarh:

- Ganesh 2023 after (p26)
- Durga 2023 pre and during (p60)
- Ganesh 2025 during (p28)

Malikhedi read 0.6 in Ganesh 2025 during (p29).

### By ghat (all six festival campaigns)

| Ghat | Water body | DO < 5 | Lowest DO | Median DO | BOD > 3 | Highest BOD | Median BOD | pH out | Usable cells |
|---|---|---|---|---|---|---|---|---|---|
| **Bairagarh (Sant Hirdaram) kund** | Upper Lake (temporary kund) | **11/13** | **0.0** | 4.1 | 13/13 | 14.0 | 8.2 | 0 | 166/234 |
| **Malikhedi kund** | Kund (temporary) | 9/13 | 0.6 | 4.5 | 11/13 | 16.8 | 6.6 | 0 | 166/234 |
| **Shahpura lake ghat** | Shahpura Lake | 5/18 | 2.5 | 5.65 | **18/18** | 11.6 | 7.3 | 0 | 228/234 |
| Khatlapura ghat | Lower Lake | 8/18 | 4.0 | 6.05 | 15/17 | 11.2 | 6.2 | 1 | 223/234 |
| **Rani Kamlapati / Kamla Park** | Lower Lake | 6/18 | 2.4 | 6.2 | **18/18** | 9.2 | 5.9 | 0 | 228/234 |
| Prempura ghat | Upper Lake | 3/18 | 3.9 | 6.25 | 9/15 | 6.8 | 3.2 | 2 | 224/234 |
| Hathaikheda dam / kund | Hathaikheda dam | **0/18** | 5.1 | 7.45 | 16/18 | **22.0** | 6.6 | 3 | 228/234 |

### Notable patterns

1. **Bairagarh is a different kind of site.** It is the most mineralised water in the set:
   - Total solids 1,364–1,574 and conductivity 1,686–1,882 in 2023, still about 1,000 in 2025.
   - DO was already 0 *before* immersion in Durga 2023.
   - Read this as a stagnant, confined kund with a poor baseline, not as damage caused only by immersion.
2. **Rani Kamlapati and Shahpura were very low on DO in Durga 2025.** Rani Kamlapati read 2.5 / 2.4 / 2.6 (p64), already low before immersion. Shahpura read 2.5 / 2.8 / 7.4 (p65), with BOD 11.4 during. These are **the most recent Durga readings**, which matters most for a 2026 Durga plan.
3. **Hathaikheda is the paradox.** It never fails DO, sometimes reads 10–11 mg/l (likely algal supersaturation), but has the highest BOD (22), COD (177.84) and turbidity (193.5), all in Ganesh 2024 after (p71). It also has 3 of the 6 pH exceedances, all on the alkaline side, which fits algae.
4. **Prempura is consistently the cleanest:** median BOD 3.2 and the lowest conductivity, about 200–400.
5. **Khatlapura had a one-off spike in Ganesh 2024 "during"** (p69): conductivity 1,473, TS 1,008, chromium 1.98, copper 2.66, pH 6.49. It had fully reverted a week later. This is real as printed, but it is a single sample.
6. **Malikhedi showed the largest damage after immersion** in Ganesh 2023 (p27). From pre to after, BOD went 1.6 → 16.8, COD 10 → 127.4, suspended solids 22 → 286 and DO 7.5 → 3.2.

### Immersion effect (pre → during → after, paired, Bhopal)

| Parameter | Median change, during − pre | Median change, after − pre | Share where after > pre |
|---|---|---|---|
| DO | −0.55 | −0.05 | 45% |
| BOD | +0.4 | +0.8 | 64% |
| COD | +9.5 | +10.1 | 82% |
| Turbidity | +3.6 | +9.9 | 80% |
| Conductivity | +36.5 | +52.9 | 88% |
| Suspended solids | +18 | +46 | 86% |
| Total solids | +49 | +97 | 80% |

**Interpretation:** solids, turbidity, conductivity and COD rise reliably and are *still higher a week later*. DO dips during immersion and mostly recovers. This is solid, data-backed evidence for "extra aeration during immersion, and cleaning or desilting afterwards". For a careful officer, though, the bigger problem is that **most ghats already fail BOD before immersion starts.** Pre-immersion BOD exceeds 3 in 32 of 37 readings.

### Year and festival view

| Campaign | DO < 5 | BOD > 3 | Median DO | Median BOD |
|---|---|---|---|---|
| Ganesh 2023 | 3/21 | 13/21 | 6.2 | 4.2 |
| Durga 2023 | 10/21 | 16/17 | 5.0 | 7.8 |
| Ganesh 2024 | 12/21 | 21/21 | 4.8 | 6.8 |
| Durga 2024 | 9/21 | 19/21 | 5.7 | 6.0 |
| Ganesh 2025 | 2/17 | 16/17 | 6.4 | 5.0 |
| Durga 2025 | 6/15 | 15/15 | 6.6 | 6.4 |

Durga campaigns tend to show higher BOD than the Ganesh campaign of the same year. There is no clean improving trend across 2023–25. BOD failure is close to universal every year.

---

## 5. Context from the lake reports (baseline)

| Station | DO average | October / November DO | BOD average | Total coliform average |
|---|---|---|---|---|
| Upper Lake, Bairagarh 2023-24 | 7.15 | 7.8 / 7.7 | 1.29 | 168 |
| Upper Lake, Kamla Park 2023-24 | 6.84 | 7.9 / 7.2 | 1.46 | 183 |
| Upper Lake, Bairagarh 2025-26 | 6.86 | 7.0 / 6.8 | 1.94 | 133 |
| **Lower Lake, Kalighat 2025-26** | **5.20** | 5.5 / **4.1** | **5.54** | **≥1,600 every month** |

**What this adds:**

- **The open Upper Lake is roughly class B.** BOD there is about 1.3–1.9, while the ghat and kund samples on the same lake show BOD of 4–14. **The ghats are far worse than the open lake around them.** This is a strong, honest framing: the problem is local to the immersion points, where intervention is possible.
- **The Lower Lake fails class B all year** on BOD and coliform. The Khatlapura and Rani Kamlapati ghats sit on water that is already polluted before any idol arrives. Rani Kamlapati Durga 2023 COD read 90 / 90 / 98 with BOD of about 8.6 throughout (p59).
- **Coliform exists only in the lake reports, never in the immersion data.** The tool must not claim anything about bacteria at the ghats.
- **20-year trend (Upper Lake, 2003–2026):** DO is drifting down, from about 8.6 to about 6.6–6.9. BOD and total coliform have improved. This is useful one-liner context for the brief.
- **Caveats:**
  - The monitoring stations are water-supply intakes, not ghats.
  - Sampling is monthly, so a pulse lasting a few days is easily missed.
  - These come from a different monitoring programme.
  - Use them for context, not for scoring.

---

## 6. The statewide file (`mp_immersion_sites_2023_2025.csv`)

- **Contents:** 21,600 rows and about 400 site-name variants, which are 80–105 actual sites per campaign. **1,272 duplicate keys**, because tables spanning two pages appear twice. 879 rows have `needs_check = yes` (site "UNKNOWN").
- **Regional office names are inconsistent:** "R.O. Jabalpur" vs "R.O.Jabalpur", "R. O. Ujjain" vs "R.O. Ujjain", "Chhindwada" vs "Chhindwara", and so on. Normalise them before grouping.
- **Obvious parse or print errors:**
  - pH 30.6 and 29.4 (Singrauli)
  - DO 32–68 (Gwalior and Datia, 2023)
  - BOD 3,042 (Tikamgarh)
  - Zinc 140 and copper 82 (River Ajnal, Harda)
  - Filter: pH outside 0–14, DO above 15, BOD above 100, metals above 10.
- **R.O. Bhopal ≠ Bhopal city.** It also covers Sehore, Rajgarh and Vidisha (Janki kund, Betwa). The 7-ghat file already excludes them correctly.
- **Bhopal vs the state** (after deduplication):

  | | Median BOD | BOD > 3 | Median DO | DO < 5 |
  |---|---|---|---|---|
  | All of MP | 2.1 | 27.5% | 6.8 | 15.7% |
  | R.O. Bhopal | 4.8 | **73%** | 6.0 | 31% |
  | 7 Bhopal city ghats | 6.4 | 89% | — | — |

  R.O. Bhopal has **the highest BOD failure rate of any regional office in MP.** Only R.O. Mandideep, next door, has worse DO (61% of readings below 5). That is a powerful line for the pitch: "Bhopal's ghats are the worst in the state on organic load."
- **Consistency check:** the Bhopal rows match the statewide file with 0 value mismatches.

---

## 7. What the source reports do NOT give you (say this in the tool)

- **No sampling dates.** "Pre", "during" and "after one week" are the only time labels, and "pre" and "during" are not defined in days.
- **No units, no lab methods, no detection limits.** Units in the CSV are assumed standard units.
- **No idol counts, nirmalya tonnage or BMC actions per ghat.** Compliance text in all three reports is generic statewide boilerplate. Each report ends "No violation were reported".
- **No comparison with CPCB limits anywhere.** This is exactly the gap the tool fills.
- **No coliform and no ammonia** in the immersion data, so class D's ammonia limit can't be checked.
- **Site identity is uncertain:**
  - "Rani Kamlapati" is a "Kamla Park kund" in the Ganesh tables but a "Lower Lake ghat" in the Durga tables.
  - Hathaikheda is a "visarjan kund" in the Ganesh tables but a "dam (ghat)" in the Durga tables.
  - These may be different sampling points.
- **COD is coarse.** Values sit on steps of about 9.6–10: 19.2/19.6, 28.8/29.4, 38.4/39.2. Identical COD rows appear across different sites. Differences under about 10 mean nothing.
- **Implausibly high DO** of 10–14.8 appears at a few sites, likely algal supersaturation or error. Don't reward it as "extra clean".

---

## 8. 2026 reality check

- **NGT has banned immersion in the Upper and Lower Lakes** (FPJ, 26 Feb 2026). BMC is building 4 dedicated ghats.
- **That puts four of the seven historical ghats on banned water:** Bairagarh (Upper), Prempura (Upper), Khatlapura (Lower) and Rani Kamlapati (Lower).
- **Bairagarh and Malikhedi are temporary kunds** that are built and dismantled each festival. They had no Durga 2025 sampling.
- **Implications for the product:**
  - The ranking is still valuable. It tells the officer which water bodies and kind of site historically degrade, where people still gather, and what to watch.
  - **New ghats must show as "No history — test before, during and after immersion",** never as safe. This is a concrete, actionable output the jury will like.
  - The historical pattern (temporary confined kunds go anoxic) is a design warning for the new ghats. They need aeration, water exchange, and nirmalya removal before immersion.

---

## 9. A transparent risk score (recommended approach)

Keep it simple, explainable and auditable. A black-box model on 116 DO readings would be unjustifiable.

**For each ghat:**

1. **Exceedance count:** DO < 5, BOD > 3, pH outside 6.5–8.5, each with the reading, campaign and `source_page`.
2. **Severity:**
   - DO shortfall = mean of max(0, (5 − DO)/5)
   - BOD excess = mean of min(3, max(0, (BOD − 3)/3)) / 3
3. **Recency weight:** Durga 2025 > Ganesh 2025 > 2024 > 2023. Weight Durga campaigns higher, since the next event is Durga.
4. **Confidence:** usable cells ÷ expected cells. Missing campaigns are listed by name. **Missing never lowers the risk.** Low confidence is shown as a badge, and optionally pushes the ghat *up* to "test first".
5. **Score:** 0.5 × DO severity + 0.4 × BOD severity + 0.1 × pH, then rank.

**Prototype result:**

| Rank | Ghat | Score, all campaigns | Score, Durga only | Why, in plain words |
|---|---|---|---|---|
| 1 | Bairagarh (Sant Hirdaram) kund | 44.7 | 51.9 | Oxygen hit zero 4 times. BOD above the limit in every reading. Saltiest water. No Durga 2025 test |
| 2 | Shahpura lake ghat | 26.6 | 36.0 | BOD above the limit in all 18 readings. Oxygen fell to 2.5 in Durga 2025 |
| 3 | Malikhedi kund | 23.5 | 20.1 | Oxygen 0.6 in 2025. Worst damage after immersion (BOD 1.6 → 16.8, 2023). No Durga 2025 test |
| 4 | Rani Kamlapati / Kamla Park | 20.0 | 26.4 | BOD above the limit in all 18 readings. Oxygen about 2.5 in all three Durga 2025 tests. Lower Lake polluted all year |
| 5 | Hathaikheda dam / kund | 19.1 | 14.1 | Oxygen fine, but the highest BOD, COD and turbidity after Ganesh 2024. pH up to 9.2 |
| 6 | Khatlapura ghat | 17.0 | 18.1 | Oxygen below 5 in 8 of 18 readings. One-off metal and salt spike during Ganesh 2024 |
| 7 | Prempura ghat | 6.3 | 2.9 | Cleanest overall. BOD still above the limit in 9 of 15 readings |

Weights are a team choice. **Show them in the UI and let the officer see the ranking under different weights.** That is honest and builds trust with the jury.

---

## 10. What to build (recommendation)

**One screen, one workflow:** "Durga 2026 plan for the BMC officer".

1. **Ranked ghat table.** For each ghat: risk badge, reason in one plain sentence, data-confidence badge, and "missing" chips (e.g. "No Durga 2025 test").
2. **Click through to evidence.** Show every reading behind the rank against its CPCB limit: red/green, BDL shown as "< DL", missing shown hatched with "not sampled". Each reading gets a `Report 2025 · p64` link that opens the PDF at that page (`file.pdf#page=64` works in browsers).
3. **Action column**, rule-based: low DO → aeration; solids and turbidity rising after immersion → cleaning or desilting within 48 h; no data → testing before, during and after.
4. **One-page brief in English and Hindi.** Generate it with Claude from the computed facts only, with a strict prompt: no health claims, cite the numbers, list the gaps. Offer it as a printable or WhatsApp-able PDF.
5. **"New ghats" row:** no history, mandatory test plan.
6. **Optional:** a map of the 7 ghats; Upper Lake baseline vs ghat comparison chart; a statewide context line.

**Suggested stack:** a single Streamlit or plain HTML app reading the CSV; works offline, which the department needs; a `.env` for the API key.

**Team split:**

- Data and scoring
- UI
- Hindi brief and wording checks (non-technical)
- PDF number verification and NGT/CPCB research (non-technical)
- Map, pitch and 2-minute recording (non-technical)

---

## 11. Pitfalls checklist

- [ ] Blank or `not sampled` is never 0 or clean. Absent rows (Durga 2025 for Bairagarh and Malikhedi) are detected explicitly.
- [ ] BDL and ND are "below the limit", not 0 and not missing. 2025 values of 0.03, 0.031 and 0.018 are flagged as probable detection limits.
- [ ] Durga 2025 "after" metals are not used as independent data.
- [ ] Durga 2024 "all metals BDL" is not presented as an improvement.
- [ ] Units are labelled "assumed".
- [ ] No health or illness claims. No claims about coliform at ghats.
- [ ] The Rani Kamlapati / Kamla Park identity caveat is shown.
- [ ] The NGT ban is acknowledged, and new ghats are marked as having no data.
- [ ] The statewide file is deduplicated and outlier-filtered if used.
- [ ] CSVs are read as UTF-8, because of `µS/cm`.
- [ ] Repo: README with team, user, 5-step run guide, what works and what doesn't, LICENSE (MIT), no keys.
