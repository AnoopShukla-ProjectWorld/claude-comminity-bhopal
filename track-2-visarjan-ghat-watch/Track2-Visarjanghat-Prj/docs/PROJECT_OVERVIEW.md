# 🌊 Project Overview: Visarjan Ghat Watch (NeerRakshak)

> **Bhopal Impact Lab 2026 · Track 2: Visarjan Ghat Watch**  
> **Team Name:** NeerRakshak  
> **Team Members:** Anoop Shukla (`anoopshuklanew00@gmail.com`)  
> **Target Audience:** Planning Officer, Bhopal Municipal Corporation (BMC)  
> **Decision Target:** Resource Allocation & Interventions for Durga Visarjan on **20 October 2026**

---

## 1. Problem Statement
Every festive season (Ganesh and Durga festivals), idol immersions deposit thousands of clay and plaster-of-Paris (PoP) idols painted with synthetic chemical dyes into Bhopal's historic water bodies. The Madhya Pradesh Pollution Control Board (MPPCB) monitors water quality three times per festival:
1. **Pre-immersion** (baseline reference)
2. **During immersion** (peak festive shock load)
3. **Post-immersion** (1 week later, recovery/retention assessment)

While MPPCB conducts these scientific tests diligently, the results remain locked inside dense 90–120 page annual technical PDF reports. Historically, these numbers were:
- Never compared against statutory limits (CPCB Class B Outdoor Bathing criteria).
- Never analyzed year-over-year (2023 vs 2024 vs 2025).
- Never synthesized into an operational priority warning for ground administrators.

### The Ground Reality
- **Anoxic Waters (DO = 0.0 mg/l):** Recorded 4 separate times at Bairagarh (Sant Hirdaram) kund. Water with zero oxygen supports no aquatic or fish life.
- **Widespread Organic Failure:** 100 out of 112 Biochemical Oxygen Demand (BOD) readings (89.3%) fail the statutory bathing limit of ≤ 3.0 mg/l across Bhopal ghats.
- **Oxygen Depletion:** 42 out of 116 Dissolved Oxygen (DO) readings (36.2%) fall below the minimum threshold of 5.0 mg/l.
- **Regulatory Turning Point:** In February 2026, the National Green Tribunal (NGT) banned all idol immersions in the Upper Lake (Bada Talab - Ramsar site) and Lower Lake (Chhota Talab). BMC is actively constructing and operating dedicated containment kunds with synthetic liners.

---

## 2. Intended User & Decision Supported
- **Primary User:** BMC Immersion Planning Officer & Ward Environmental Engineers.
- **Operational Decision Supported:**
  Before 20 October Durga Visarjan, the officer must allocate limited engineering assets:
  - Where to deploy mechanical aeration fountains?
  - Where to construct secondary synthetic bunds/booms?
  - Which ghats require mandatory sediment suction skimmers within 48 hours post-immersion?
  - Where must immersion strictly divert to alternative dedicated kunds?

---

## 3. Original Hackathon Requirements vs. Implemented Solutions

| Original Requirement (Problem Statement) | Status | Implemented Solution |
| :--- | :---: | :--- |
| **Ranked list of all 7 Bhopal ghats by risk** | **DONE** | Multi-Criteria Decision Analysis (MCDA) 0–100 Composite Score. |
| **Plain-words justification in English & Hindi** | **DONE** | Contextual explanations dynamically rendered in both languages. |
| **100% Traceability to MPPCB report & page** | **DONE** | Interactive link on every reading opening source PDF at exact page. |
| **Forwardable Brief for WhatsApp/Email** | **DONE** | Bilingual executive memo at `/brief` with 1-click print styling. |
| **Report against CPCB Class B bathing limits** | **DONE** | Strict limit evaluation: DO ≥ 5.0 mg/l, BOD ≤ 3.0 mg/l, pH 6.5–8.5. |
| **Honest handling of missing / un-sampled data** | **DONE** | Explicitly flagged as `Not Sampled`; never treated as clean water. |
| **Distinct treatment of BDL/ND qualifiers** | **DONE** | Flagged as `BDL` (Below Detection Limit); not treated as zero or missing. |
| **No unsupported health claims** | **DONE** | Strictly adheres to official CPCB ecological classification. |

---

## 4. Key Outcomes & High-Value Additions (NeerRakshak Innovation)
In addition to the baseline requirements, NeerRakshak implemented:
1. **Dynamic Risk Sensitivity Sliders:** Real-time client-side re-weighting (DO/BOD/pH) with instant re-ranking.
2. **Interactive GIS Map:** Leaflet.js geospatial visualizer displaying exact coordinates and risk pins.
3. **Multi-Parameter Bulk Ingestion:** Drag-and-drop CSV/Excel importer supporting long and wide matrices.
4. **Dynamic Ghat Onboarding:** Real-time registration of newly constructed kunds with automated deep-dive pages.
5. **Grounded AI Chatbot Assistant:** Bilingual conversational engine answering queries strictly from MPPCB records.
6. **One-Click Deployer (`run.bat`):** Zero-config automated launcher ensuring effortless cross-machine evaluation.
