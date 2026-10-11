# 🎙️ Speaker Notes: 3–5 Minute Presentation Script

> **Presenter:** Anoop Shukla (Team NeerRakshak)  
> **Target Audience:** Hackathon Judges & MPSeDC / BMC Observers  
> **Duration:** 3 to 5 Minutes  
> **Accompanying Deck:** `presentation/NeerRakshak_Visarjan_Ghat_Watch.pptx`

---

## Slide 1: Title & Introduction (0:00 – 0:30)
> *"Respected judges and peers, good afternoon. I am Anoop Shukla representing team **NeerRakshak**. Today, I am proud to present **Visarjan Ghat Watch** — an empirical, auditable decision-support system built for the Bhopal Municipal Corporation ahead of Durga Visarjan on October 20th."*

---

## Slide 2: The Problem & Ground Reality (0:30 – 1:15)
> *"Every festival season, thousands of idols are immersed across Bhopal's lakes. MPPCB diligently tests the water before, during, and after immersion. But these critical findings remain buried in 90 to 120-page technical PDFs that no ground officer has time to read.*  
> *When we extracted and synthesized all 1,524 readings across the last 3 years, the reality was staggering:*  
> *1. Dissolved oxygen read **zero mg/l four separate times** at Bairagarh Kund — total anoxia where fish cannot survive.*  
> *2. **89.3% of BOD tests violate statutory bathing limits**.*  
> *3. And with Durga Visarjan just **9 days away**, BMC officers have to decide where to deploy aeration pumps and cleaning teams. Until now, that decision was based on memory. Today, it is driven by data."*

---

## Slide 3: The Solution (1:15 – 1:50)
> *"Visarjan Ghat Watch solves this with 4 core pillars:*  
> *First, an objective **MCDA Risk Formula (0 to 100)** ranking all 7 ghats from Critical to Controlled.*  
> *Second, **Live Sensitivity Sliders** allowing officers to adjust DO and BOD priorities on the fly.*  
> *Third, **100% Traceability** — every single number links directly to the scanned MPPCB PDF and exact page number.*  
> *And fourth, a **Forwardable Bilingual Brief** in Hindi and English ready for instant administrative action."*

---

## Slide 4 & 5: Priority Rankings & Architecture (1:50 – 2:30)
> *"Our ranking algorithm places **Bairagarh Kund at #1 Critical Priority** with a risk score of 69.7, followed by **Shahpura Lake at #2**, and **Prempura Ghat as the cleanest at #7**.*  
> *Under the hood, we built this using **Python, Flask, SQLite, Pandas, Chart.js, and Leaflet.js GIS**. It runs 100% locally with zero expensive cloud dependencies and launches via a single click on `run.bat`."*

---

## Slide 6 & 7: Dynamic Pipelines & USPs (2:30 – 3:15)
> *"Most importantly, this is **not a static demo**. It features an end-to-end **bulk ingestion pipeline**. An officer can drag-and-drop a multi-parameter Excel spreadsheet of 2026 tests, or register a newly constructed artificial kund, and the entire system recalculates scores and updates the GIS map in under one second.*  
> *We also built a **Grounded AI Chatbot** that understands colloquial Hinglish and answers queries strictly using verified MPPCB citations."*

---

## Slide 8 & 9: Live Demo & Conclusion (3:15 – 4:00)
> *"In summary, Visarjan Ghat Watch transforms three years of dead PDF data into a living, legally defensible, and actionable shield for Bhopal's lakes.*  
> *The project is 100% open source, fully verified across our 7-step test suite, and offered to MPSeDC and the Government of Madhya Pradesh.*  
> *Thank you, and I look forward to your questions!"*
