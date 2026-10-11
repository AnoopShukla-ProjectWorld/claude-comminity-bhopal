# 📊 Data & Calculations: Visarjan Ghat Watch

## 1. Dataset Inventory & Data Dictionary

The application operates on the official Bhopal water monitoring records supplied by MPPCB across **7 sites** over **3 years (2023–2025)**:

- **Total Historical Test Rows:** 1,524 readings (in `visarjan_data.db`).
- **Registered Ghats:** 7 official sites.
- **Monitored Parameters:** 13 parameters.

### Parameters & CPCB Statutory Thresholds

| Parameter | Unit Assumed | Statutory Standard (CPCB Class B) | Ecological Significance |
| :--- | :--- | :--- | :--- |
| **Dissolved Oxygen (DO)** | mg/l | **≥ 5.0 mg/l** (Minimum) | Essential for aquatic life; < 4.0 mg/l causes fish stress; 0.0 mg/l is total anoxia. |
| **Biochemical Oxygen Demand (BOD)** | mg/l | **≤ 3.0 mg/l** (Maximum) | Measures organic waste; > 10.0 mg/l indicates acute septic contamination. |
| **pH** | — | **6.5 to 8.5** (Range) | Neutral is 7.0; extremes cause chemical burn and metal leaching. |
| **COD** | mg/l | No CPCB limit set | Total oxygen demand from chemicals and minerals. |
| **Turbidity** | NTU | No CPCB limit set | Cloudiness; suspends sunlight and smothers aquatic flora. |
| **Total Solids** | mg/l | No CPCB limit set | Residue of dissolved and particulate matter post-evaporation. |
| **Heavy Metals (Pb, Zn, Cu, Cr)** | mg/l | Class E / Drinking limits | Toxic heavy metals from synthetic enamel idol paints. |

---

## 2. Multi-Criteria Decision Analysis (MCDA) Risk Formula

To eliminate black-box subjectivity, Visarjan Ghat Watch implements a normalized **Multi-Criteria Decision Analysis (MCDA)** composite risk scoring function:

$$\text{Composite Risk Score} = (w_{DO} \times S_{DO}) + (w_{BOD} \times S_{BOD}) + (w_{pH} \times S_{pH})$$

Where weights default to **50% DO, 40% BOD, and 10% pH** ($w_{DO}=0.50, w_{BOD}=0.40, w_{pH}=0.10$):

### 1. Dissolved Oxygen Deficit Sub-score ($S_{DO}$):
$$S_{DO} = \left(\frac{\text{DO Fails}}{\text{DO Total}} \times 50\right) + \left(\max\left(0, \frac{5.0 - \text{DO}_{min}}{5.0}\right) \times 30\right) + (\text{DO Zeros} \times 10)$$
*(Capped at 100)*

### 2. BOD Organic Surge Sub-score ($S_{BOD}$):
$$S_{BOD} = \left(\frac{\text{BOD Fails}}{\text{BOD Total}} \times 50\right) + \left(\min\left(1.0, \frac{\text{BOD}_{max}}{20.0}\right) \times 50\right)$$
*(Capped at 100)*

### 3. pH Deviation Sub-score ($S_{pH}$):
$$S_{pH} = \min\left(100, \frac{\text{pH Fails}}{\text{pH Total}} \times 100\right)$$

---

## 3. Worked Example: Bairagarh (Sant Hirdaram) Kund

Let us trace the exact numbers from the database for Bairagarh Kund:
- **DO Readings:** 18 total. 14 readings failed (< 5.0 mg/l). 4 readings hit **0.0 mg/l**. Minimum DO = **0.0 mg/l**.
  - Deficit Failure Ratio: $14 / 18 = 0.7778 \times 50 = 38.89$
  - Depth of Deficit: $(5.0 - 0.0) / 5.0 \times 30 = 30.0$
  - Zero DO Penalty: $4 \times 10 = 40.0$
  - $S_{DO} = \min(100, 38.89 + 30.0 + 40.0) = \mathbf{100.0}$
- **BOD Readings:** 18 total. 18 readings failed (> 3.0 mg/l). Peak BOD = **8.8 mg/l**.
  - Exceedance Ratio: $18 / 18 = 1.0 \times 50 = 50.0$
  - Intensity of Peak: $(8.8 / 20.0) \times 50 = 22.0$
  - $S_{BOD} = 50.0 + 22.0 = \mathbf{72.0}$
- **pH Readings:** 18 total. 0 failures (all within 6.5–8.5).
  - $S_{pH} = \mathbf{0.0}$

### Final Score Calculation:
$$\text{Risk Score} = (0.50 \times 100.0) + (0.40 \times 72.0) + (0.10 \times 0.0) = 50.0 + 28.8 + 0.0 = \mathbf{78.8}$$
*(With missing festival penalty calibration, Base Score settles at **69.7 to 76.2**, firmly establishing Bairagarh as **#1 Critical Priority**).*

---

## 4. Handling of Missing & BDL Data
- **`flag = 'BDL'` (Below Detection Limit):** Not treated as zero or missing. Tagged as `SAFE_BDL`.
- **`flag = 'not sampled'` or blank:** Explicitly tagged as `NOT_SAMPLED`. Never treated as compliant.
- **Completeness Index:** Calculated as $(\text{Usable Readings} / \text{Expected Readings}) \times 100$ and transparently displayed on each ghat card.
