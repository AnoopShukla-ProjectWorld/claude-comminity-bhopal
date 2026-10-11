# 🌊 विसर्जन घाट वॉच · Visarjan Ghat Watch (Bhopal 2026)

> **Bhopal Impact Lab 2026 · Track 2**  
> Claude Impact Lab × Cerebras Café Compute, Bhopal · SSR Global Skills Park  
> **Author & Developer:** Anoop Shukla  
> **Target User:** Bhopal Municipal Corporation (BMC) Planning Officer for Durga Visarjan  
> **Target Date:** Durga Visarjan on **20 October 2026** (9 days away)

---

## 📌 Executive Summary

Every Ganesh and Durga festival, the Madhya Pradesh Pollution Control Board (MPPCB) monitors water quality at Bhopal idol-immersion ghats (pre, during, and after immersion). The results are published in dense 90–120 page annual PDF reports, but historically have never been synthesized against statutory limits or compared year-over-year.

**Visarjan Ghat Watch** extracts and analyzes **1,524 water quality readings** across all **7 Bhopal ghats (2023–2025)**, benchmarks them against **CPCB Class B (outdoor bathing)** criteria, and delivers an auditable, transparent decision-support system:
1. **Ranked Risk List of all 7 Ghats** with plain-words justifications in English and Hindi.
2. **100% Traceability:** Every reading links directly to the MPPCB annual report and exact PDF page number.
3. **Forwardable Bilingual Executive Brief:** An official memo formatted for WhatsApp/email forwarding or single-click PDF printing.
4. **2026 NGT Reality Protocol:** Actionable testing directives for newly constructed BMC dedicated containment kunds following the National Green Tribunal's immersion ban on the Upper and Lower Lakes.

---

## 🚨 Headline Data Findings

* **Dissolved Oxygen (DO < 5.0 mg/l):** **42 of 116 readings (36.2%)** violate the CPCB Class B bathing standard.
* **Biochemical Oxygen Demand (BOD > 3.0 mg/l):** **100 of 112 readings (89.3%)** exceed safe organic waste limits (median 6.4 mg/l; maximum 22.0 mg/l).
* **Anoxic Water (DO = 0.0 mg/l):** Recorded **4 separate times**, all at **Bairagarh (Sant Hirdaram) kund** (Ganesh 2023 post-immersion, Durga 2023 pre and during, Ganesh 2025 during).
* **Post-Immersion Organic Spike:** Immersion triggers immediate surges in Total Solids, Turbidity, and COD that persist **7 days later** in over 80% of sampling events.

---

## 🏆 Bhopal Ghat Risk Ranking (1 to 7)

| Rank | Ghat | Water Body | Risk Score | Level | Plain Language Reason |
|:---:|:---|:---|:---:|:---:|:---|
| **#1** | **Bairagarh (Sant Hirdaram) kund** | Upper Lake Basin | **69.7** | 🔴 CRITICAL | DO hit 0.0 mg/l four times. 100% BOD violations. Stagnant mineralized kund. No Durga 2025 test. |
| **#2** | **Shahpura lake ghat** | Shahpura Lake | **26.6** | 🟠 HIGH | 100% (18/18) BOD violations. In Durga 2025, DO dropped to 2.5 mg/l with during-immersion BOD of 11.4 mg/l. |
| **#3** | **Malikhedi kund** | Dedicated Kund | **23.5** | 🟠 HIGH | Worst post-immersion surge (BOD jumped 1.6 &rarr; 16.8 mg/l in 2023). DO fell to 0.6 mg/l in 2025. No Durga 2025 test. |
| **#4** | **Rani Kamlapati / Kamla Park** | Lower Lake | **20.0** | 🟠 HIGH | 100% BOD violations. DO remained at ~2.5 mg/l across all 3 phases in Durga 2025. Lower Lake chronically polluted. |
| **#5** | **Hathaikheda dam / kund** | Hathaikheda Dam | **19.1** | 🟡 MODERATE | DO maintained (algal bloom), but recorded highest BOD (22.0 mg/l) and COD (177.8 mg/l) after Ganesh 2024. Alkaline pH 8.92. |
| **#6** | **Khatlapura ghat** | Lower Lake | **17.0** | 🟡 MODERATE | DO failed in 8/18 readings. Baseline Lower Lake pollution. Acute conductivity & metal spike in Ganesh 2024. |
| **#7** | **Prempura ghat** | Upper Lake | **6.3** | 🟢 LOW | Consistently the cleanest. Lowest conductivity (200-400 µS/cm) and lowest median BOD (3.2 mg/l). |

---

## ⚡ How to Run in 3 Steps

### Step 1: Open Terminal in Project Folder
```bash
cd "track-2-visarjan-ghat-watch/Track2-Visarjanghat-Prj"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Launch the Application
```bash
python app.py
```
Open **`http://localhost:5000`** in any browser.

---

## 🛠️ Transparent Risk Scoring Methodology

To ensure auditability, our composite scoring avoids opaque black-box models:
$$\text{Risk Score} = 0.50 \times \text{DO Severity} + 0.40 \times \text{BOD Severity} + 0.10 \times \text{pH Severity}$$
* **DO Severity:** Normalized shortfall below $5.0\text{ mg/l}$, with a $+12.5$ penalty for each anoxic reading ($\text{DO} = 0.0$).
* **BOD Severity:** Normalized excess above $3.0\text{ mg/l}$ capped at $3\times$.
* **pH Severity:** Frequency of excursions outside $6.5 - 8.5$.

---

## 🔍 Data Gaps & Honest Disclosures

1. **Missing Durga 2025 Data:** Bairagarh and Malikhedi kunds had no sampling tables in the 2025 MPPCB Durga report. Our tool explicitly highlights this gap rather than assuming the water was clean.
2. **BDL vs Zero vs Missing:**
   * `BDL` (Below Detection Limit) is preserved as safe detection threshold, never converted to 0.
   * `not sampled` / `*` / `**` are flagged explicitly as missing data.
3. **No Unwarranted Health Claims:** This tool evaluates environmental conformity to CPCB Class B standards; it makes no epidemiological claims.
4. **Site Nomenclature:** MPPCB reports alternate between "Kamla Park kund" and "Lower Lake ghat" for Rani Kamlapati (confidence flagged as Medium).

---

## 📜 License
Open source under the [MIT License](LICENSE). Offered to the Government of Madhya Pradesh through MPSeDC.
