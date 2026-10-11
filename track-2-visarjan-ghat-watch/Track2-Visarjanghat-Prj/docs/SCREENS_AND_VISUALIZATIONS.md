# 🖥️ Screens & Visualizations: Visarjan Ghat Watch

## 1. Verified Screen & Route Inventory

| Screen # | Screen Name | Route / URL | Main Purpose | Data Sources & Interactivity |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Executive Risk Dashboard** | `GET /` | High-level risk intelligence and priority list for BMC officers. | 4 KPI cards, Dynamic Sliders, Leaflet GIS map, Chart.js ranking, 7 ghat cards. |
| **2** | **Ghat Deep-Dive Page (7 Sites)** | `GET /ghat/<site_name>` | Longitudinal trends, phase shock load, and official action directives. | YoY Line chart, Phase Bar chart, 5-axis table filter, direct PDF jump links. |
| **3** | **Bilingual Forwardable Brief** | `GET /brief` | Official printable memorandum formatted for administrative forwarding. | Aggregated executive summary, NGT directives, 1-click print stylesheet. |
| **4** | **1,524 Traceability Table** | `GET /traceability` | Scientific auditability table linking every record to MPPCB page. | Filterable records table, PDF source badges, full metadata inspection. |
| **5** | **Single Sample Entry Modal** | Modal on `/` | Rapid field entry for live water test samples. | Form submission (`POST /api/add-reading`), instant DB write & CPCB tagging. |
| **6** | **Bulk Data Ingestion Modal** | Modal on `/` | Batch ingest CSV/Excel spreadsheets with scope overrides. | File drag-and-drop (`POST /api/bulk-import`), sample CSV template download. |
| **7** | **New Ghat Registration Modal** | Modal on `/` | Real-time onboarding of newly built containment kunds. | Geo-coordinate capture (`POST /api/add-ghat`), automated deep-dive page creation. |
| **8** | **Bilingual AI Assistant Drawer** | Floating on all pages | Context-grounded Q&A assistant verified against MPPCB data. | Natural language search (`POST /api/chat`), Hinglish alias matching. |

---

## 2. Complete Visualizations Catalog

### 1. Leaflet.js Interactive GIS Geospatial Map
- **Location:** Executive Dashboard (`/`)
- **Technology:** Leaflet.js, OpenStreetMap tiles
- **Function:** Displays the exact geographic coordinates (Lat/Lon) of all 7 Bhopal immersion sites.
- **Marker Color Encoding:**
  - 🔴 **Rose (`#E11D48`):** Critical Risk (Score > 50)
  - 🟠 **Orange (`#F97316`):** High Risk (Score 20–50)
  - 🟡 **Amber (`#F59E0B`):** Moderate Risk (Score 10–20)
  - 🟢 **Emerald (`#10B981`):** Low / Controlled Risk (Score < 10)
- **Interaction:** Clicking any circle marker opens a clean popup showing Rank, Score, Water Body, and a direct link to the ghat deep-dive page.

### 2. Chart.js Priority Ranking Bar Chart
- **Location:** Executive Dashboard (`/`)
- **Metrics:** X-axis: Ghat Name, Y-axis: Composite Risk Score (0–100).
- **Interactivity:** Dynamically re-renders in real-time when the MCDA sensitivity sliders are adjusted.

### 3. Chart.js Shock Delta Impact Bar Chart
- **Location:** Executive Dashboard (`/`)
- **Metrics:** Compares median changes across 13 parameters during immersion and 1 week post-immersion relative to pre-immersion baselines.
- **Insight:** Proves that organic and solids spikes persist 7 days after the festival in over 80% of sampling events.

### 4. Chart.js Year-over-Year (YoY) Multi-Line Trend Chart
- **Location:** Ghat Deep-Dive Page (`/ghat/<site_name>`)
- **Metrics:** 2023, 2024, 2025 trends for Dissolved Oxygen and BOD against CPCB limits.

### 5. Historical Tests Filterable Table
- **Location:** Ghat Deep-Dive Page (`/ghat/<site_name>`)
- **Controls:** 5 interactive client-side dropdowns (Year, Festival, Phase, Parameter, CPCB Status) with live matching counter and 1-click reset.
