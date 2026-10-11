# 🎤 Presentation Content & Slide-by-Slide Blueprint

## Slide 1: Title & Team
- **Title:** Visarjan Ghat Watch (विसर्जन घाट वॉच)
- **Subtitle:** Turning 3 Years of Buried MPPCB Water Tests into an Auditable Action Plan for Bhopal 2026
- **Team Name:** NeerRakshak
- **Presenter:** Anoop Shukla
- **Event:** Bhopal Impact Lab 2026 · Track 2

---

## Slide 2: The Ground Reality & Problem
- **The Context:** Ganesh and Durga immersions dump thousands of painted idols into Bhopal's water bodies.
- **The Paradox:** MPPCB diligently tests water pre, during, and post-immersion, but results sit in dense 90–120 page annual PDFs that nobody synthesizes.
- **The Numbers:**
  - **4 Anoxic Events (0.0 mg/l DO):** Water at zero oxygen supports no life (Bairagarh Kund).
  - **89.3% BOD Violations:** Organic pollution vastly exceeds statutory limits.
  - **36.2% DO Violations:** Failing CPCB Class B outdoor bathing criteria.
- **The Urgency:** Durga Visarjan is on **20 October 2026 (9 days away)**. BMC must allocate limited resources without guesswork.

---

## Slide 3: The Target User & Decision
- **User:** BMC Immersion Planning Officer & Zonal Municipal Engineers.
- **Core Dilemma:** Where do we send aeration fountains, containment booms, trash skimmers, and suction pumps?
- **Our Answer:** An objective, traceable decision-support platform that transforms laboratory PDFs into an interactive risk priority ranking (#1 to #7).

---

## Slide 4: System Architecture & Workflow
- **End-to-End Flow:** PDF Extraction & CSV ETL &rarr; SQLite Zero-Config DB &rarr; Multi-Criteria Analytics Engine &rarr; Responsive Bilingual Web Dashboard.
- **Zero Heavy Cloud Dependencies:** 100% self-contained Python/Flask architecture runnable via 1-click `run.bat`.

---

## Slide 5: Objective Analytics (MCDA Risk Formula)
- **Mathematical Grounding:**
  $$\text{Composite Risk} = (w_{DO} \times S_{DO}) + (w_{BOD} \times S_{BOD}) + (w_{pH} \times S_{pH})$$
- **Dynamic Sensitivity Sliders:** BMC officers can rebalance weights in real-time, instantly re-ordering ranks without page reloads.
- **Honest Data Handling:** Unsampled phases are never treated as clean; BDL qualifiers are preserved.

---

## Slide 6: Verified Risk Ranking (Bhopal's 7 Sites)
1. **#1 Bairagarh (Sant Hirdaram) kund (Score: 69.7 | 🔴 CRITICAL):** 4 zero DO readings, 100% BOD violations, stagnant mineralized kund.
2. **#2 Shahpura lake ghat (Score: 26.6 | 🟠 HIGH):** 100% BOD violations, DO dropped to 2.5 mg/l.
3. **#3 Malikhedi kund (Score: 23.5 | 🟠 HIGH):** Severe post-immersion surge (BOD 1.6 &rarr; 16.8 mg/l).
4. **#4 Rani Kamlapati / Kamla Park (Score: 20.0 | 🟠 HIGH):** Chronically polluted Lower Lake basin.
5. **#5 Hathaikheda dam / kund (Score: 19.1 | 🟡 MODERATE):** Extreme peak BOD (22.0 mg/l) & COD (177.8 mg/l).
6. **#6 Khatlapura ghat (Score: 17.0 | 🟡 MODERATE):** Baseline Lower Lake pollution.
7. **#7 Prempura ghat (Score: 6.3 | 🟢 LOW):** Consistently the cleanest natural lake ghat.

---

## Slide 7: Interactive GIS & Deep-Dive Analytics
- **Leaflet.js GIS Map:** Real-world GPS coordinates with color-coded risk pins across Bhopal.
- **Ghat Deep-Dive (`/ghat/<site>`):** Longitudinal YoY charts, phase delta impact, and 5-axis table filters.
- **Cinematic MPPCB Hero Banners:** Ground operational images highlighting actual field conditions.

---

## Slide 8: Future-Proof Dynamic Pipelines
- **Bulk Data Ingestion (CSV / Excel):** Ingest hundreds of 2026/2027 tests across multiple parameters in a single click with smart context overrides.
- **Dynamic Kund Onboarding:** BMC can register newly constructed containment kunds with automated deep-dive page creation.
- **Instant Recalculation:** All metrics, rankings, and charts re-calculate automatically on data entry.

---

## Slide 9: 100% Traceability & Grounded AI Assistant
- **Judicial Auditability:** Every single number links to its source MPPCB PDF report and exact page.
- **Bilingual Grounded Chatbot:** Answers natural language questions in Hindi, English, and Hinglish with verified citations.

---

## Slide 10: Summary & Next Steps
- **Immediate Value:** Ready for BMC deployment ahead of 20 October 2026 Durga Visarjan.
- **Extensibility:** Expandable to all 100+ immersion sites across Madhya Pradesh.
- **One-Click Local Deployment:** Double-click `run.bat` for instant zero-config evaluation.
