# 💡 Judge Q&A Defense: Visarjan Ghat Watch

## Q1: Why did you use an MCDA formula instead of a Machine Learning or Deep Learning model?
**Answer:**
> "In public environmental administration and statutory compliance (such as NGT hearings), decision models must be **100% explainable, transparent, and legally defensible**. A black-box ML model cannot be easily audited by municipal engineers or defended in court. Our MCDA formula maps directly to statutory CPCB Class B outdoor bathing thresholds (DO, BOD, pH). Furthermore, with our dynamic sensitivity sliders, administrative officers retain full agency to adjust weights based on changing field conditions."

---

## Q2: How do you handle missing data? For instance, why does Bairagarh have no Durga 2025 data?
**Answer:**
> "We practice strict **honesty in data reporting**. In MPPCB's official 2025 Durga report, sampling at Bairagarh was omitted. In our system, missing data is explicitly flagged as `Not Sampled` and given a data completeness score of 88.9%. We never interpolate or assume missing readings are clean water. In fact, a penalty for un-sampled phases is applied to ensure administrative vigilance."

---

## Q3: What is the difference between BDL and zero?
**Answer:**
> "BDL stands for **Below Detection Limit**. It indicates that the laboratory equipment could not measure the substance below a certain sensitivity threshold (e.g. Lead < 0.01 mg/l). It is **not zero** and it is **not missing**. We preserve BDL as an explicit qualitative state (`SAFE_BDL`) to maintain complete laboratory accuracy."

---

## Q4: Can this system handle new data from Durga Visarjan 2026 or future years?
**Answer:**
> "Yes, absolutely! The application is **100% dynamic**. We built a dedicated bulk ingestion pipeline supporting both long tabular CSVs and wide multi-parameter Excel spreadsheets. When BMC enters new readings or registers a new artificial kund, the system automatically commits the data to SQLite, executes CPCB Class B compliance tagging, and recalculates composite risk scores and priority rankings in less than a second."

---

## Q5: How is the AI chatbot grounded? Does it hallucinate?
**Answer:**
> "Our AI chatbot is grounded in an indexed knowledge base of all 1,524 MPPCB readings and CPCB guidelines. It uses phonetic Hinglish alias resolution (understanding queries like *'bairagadh'* or *'hathikheda'*) and accompanies every factual assertion with exact verified citations from MPPCB records. It refuses to make unsupported health or causal claims."

---

## Q6: How easy is it for an officer to run this project?
**Answer:**
> "It requires **zero complex configuration**. The project includes a Windows `run.bat` script. Double-clicking it automatically creates an isolated virtual environment, installs dependencies, validates the database, starts the local server, and launches the dashboard in the default browser."
