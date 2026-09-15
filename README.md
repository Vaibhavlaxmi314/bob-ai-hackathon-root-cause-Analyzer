# 🚀 Supply Chain Disruption Assistant & Fleet Utilisation Optimizer

---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | root-cause-Analyzer |
| **Track** | AI |
| **Team Lead** | Vaibhavlaxmi — 26mca113@charusat.edu.in |
| **Members** | Kevina, Aayush, Abhishek |

---

## 🎯 Problem Statement

Global supply chains are continuously exposed to disruptions — port strikes, severe weather, geopolitical crises — that cascade silently across hundreds of active shipments simultaneously. Logistics teams have no automated way to identify which shipments are trapped, find alternative routes, locate idle fleet assets nearby, or detect cold chain temperature excursions before they reach delivery. By the time the impact is visible, it is too late to act, and losses can exceed $500,000 per cargo hold.

---

## 💡 Solution

We built an AI-powered operational assistant on IBM Bob that gives logistics teams a unified, real-time view of supply chain disruptions. The Bob agent ingests simulated disruption events, shipment manifests, fleet telemetry, and IoT temperature sensor logs, then uses watsonx.ai (Granite) to identify affected shipments, recommend alternative routes and carriers, surface idle fleet assets for redeployment, and classify cold chain excursion severity — all from a single React dashboard.

---

## ✨ Key Features

- **Feature 1: Disruption-to-Shipment Impact Mapping** — Automatically cross-references live disruption events (weather, port strikes, geopolitical crises) against all active shipment legs to instantly identify which shipments are trapped or at risk, with an impact severity score.
- **Feature 2: AI-Powered Re-routing Recommendations** — For each affected shipment, the IBM Bob agent queries watsonx.ai Granite with the current route, carrier alternatives, and delivery deadline to produce a ranked rerouting recommendation with plain-language reasoning.
- **Feature 3: Idle Fleet Asset Redeployment** — Scans simulated fleet telemetry to identify idle trucks, containers, and reefer vessels near disrupted regions and ranks them for redeployment to stranded shipments.
- **Feature 4: Cold Chain Excursion Detection and Severity Classification** — Monitors IoT temperature sensor logs for refrigerated shipments, detects threshold breaches or approaching excursions, and uses watsonx.ai to classify severity and recommend immediate action before delivery.
- **Feature 5: Unified React Operations Dashboard** — Presents all four analysis outputs — disruption alerts, affected shipments, rerouting options, fleet map, cold chain reports — in a single operational view accessible without manual data aggregation.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python, JavaScript (React) |
| **Frameworks** | FastAPI, IBM Bob SDK, React 18 |
| **IBM Technologies** | IBM Bob, watsonx.ai (Granite model) |
| **Databases** | SQLite (local, seeded on startup) |
| **Other** | GitHub Actions, simulated JSON/CSV data sources |

---

## 📁 Repository Structure

```
├── src/                  # All source code
│   ├── backend/          # FastAPI backend + Bob agent + MCP tools
│   ├── frontend/         # React dashboard
│   └── data/             # Simulated seed data (disruptions, shipments, fleet, IoT)
├── docs/                 # Written documentation
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/                 # Demo artifacts
│   ├── screenshots/      # App screenshots
│   └── demo-video-link.txt  # Link to demo video
├── presentation/         # Slide deck
└── submission.yaml       # Structured submission metadata
```

---

## ⚡ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/root-cause-Analyzer/bob-ai-hackathon-root-cause-Analyzer.git
cd bob-ai-hackathon-root-cause-Analyzer

# 2. Set up Python environment
cd src/backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and fill in WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL

# 4. Start the backend (seeds SQLite database on first run)
uvicorn main:app --reload --port 8000

# 5. In a separate terminal, start the React dashboard
cd src/frontend
npm install
npm run dev
```

The dashboard will be available at: `http://localhost:5173`
The API will be available at: `http://localhost:8000`

For full setup details see [`docs/setup-guide.md`](docs/setup-guide.md).

---

## 🖥️ Demo

| Artifact | Link |
|---|---|
| 📹 Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| 🌐 Live Demo | [See demo/live-demo-url.txt](demo/live-demo-url.txt) |
| 🖼️ Screenshots | [See demo/screenshots/](demo/screenshots/) |
| 📊 Presentation | [See presentation/](presentation/) |

---

## ⚠️ Known Limitations

- **Simulated data only** — All disruption events, shipment manifests, fleet telemetry, and IoT sensor logs are simulated JSON/CSV files seeded at startup. No live third-party APIs or carrier systems are integrated.
- **No production authentication** — The FastAPI backend and React dashboard have no auth layer in this prototype. All endpoints are open on localhost.
- **Single-node deployment** — The solution runs locally as a single process. Horizontal scaling and production deployment infrastructure are not included in this submission.

---

## 🏅 What We're Most Proud Of

The cold chain excursion detection and severity classification pipeline is the feature we are most proud of. Connecting IoT time-series temperature data to a watsonx.ai Granite classification call — with enough structured context about cargo type, excursion magnitude, and duration — produces genuinely useful severity assessments and action recommendations. This is the feature that most directly addresses the $500K+ cargo loss scenario described in the problem statement, and it demonstrates meaningful, grounded use of IBM Bob and watsonx.ai together rather than a surface-level integration.

---
