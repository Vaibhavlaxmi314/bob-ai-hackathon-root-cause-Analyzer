# Setup Guide

> **This file is read by the automated evaluation pipeline. Be precise and complete.**

## Prerequisites

Before you begin, ensure you have the following installed and available:

- [ ] Python 3.11 or higher (`python --version`)
- [ ] Node.js 18 or higher (`node --version`) — for the React dashboard
- [ ] An IBM Cloud account with watsonx.ai access
- [ ] Your `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, and `WATSONX_URL` from the IBM watsonx.ai console

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp src/.env.example src/backend/.env
```

| Variable | Description | Required |
|---|---|---|
| `WATSONX_API_KEY` | Your IBM watsonx.ai API key from cloud.ibm.com | Yes |
| `WATSONX_PROJECT_ID` | Your watsonx.ai project ID | Yes |
| `WATSONX_URL` | watsonx.ai endpoint — e.g. `https://us-south.ml.cloud.ibm.com` | Yes |
| `APP_PORT` | Backend port (default: `8000`) | No |
| `APP_ENV` | Environment flag — `development` or `production` | No |

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/root-cause-Analyzer/bob-ai-hackathon-root-cause-Analyzer.git
cd bob-ai-hackathon-root-cause-Analyzer

# 2. Set up the Python virtual environment
cd src/backend
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate

# Activate — macOS / Linux
# source .venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Install React dashboard dependencies (separate terminal)
cd ../frontend
npm install
```

## Running the Application

```bash
# Terminal 1 — Start the FastAPI backend
# (from src/backend/ with .venv activated)
uvicorn main:app --reload --port 8000
```

On first run, the backend automatically seeds the SQLite database with simulated data:
- 15 active disruption events (storms, port strikes, geopolitical crises)
- 120 active shipments with multi-leg routes
- 80 fleet assets (trucks, containers, reefer vessels) with telemetry
- IoT temperature sensor logs for all 38 refrigerated shipments

```bash
# Terminal 2 — Start the React dashboard
# (from src/frontend/)
npm run dev
```

| Service | URL |
|---|---|
| React Dashboard | `http://localhost:5173` |
| FastAPI API | `http://localhost:8000` |
| API Docs (Swagger) | `http://localhost:8000/docs` |

## Running Tests

```bash
# From src/backend/ with .venv activated
pytest tests/ -v
```

## Quick Demo

To see a full disruption scenario end-to-end without interacting with the dashboard:

```bash
# From src/backend/ with .venv activated
# Triggers a simulated port strike affecting 12 shipments and prints recommendations
python demo/run_demo_scenario.py --scenario port_strike_rotterdam
```

This script will:
1. Inject a simulated Rotterdam port strike disruption event
2. Run the Shipment Impact Analyzer across all active shipments
3. Call watsonx.ai to generate rerouting recommendations for the top 3 affected shipments
4. Scan fleet telemetry for idle assets near Rotterdam
5. Print the full structured output to stdout

## Troubleshooting

| Issue | Solution |
|---|---|
| `401 Unauthorized` from watsonx.ai | Check that `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` are correctly set in `src/backend/.env` and that the key has not expired |
| `ModuleNotFoundError` on startup | Ensure the virtual environment is activated (`source .venv/bin/activate`) and run `pip install -r requirements.txt` again |
| React dashboard shows blank / no data | Confirm the FastAPI backend is running on port 8000 and that the SQLite database was seeded (look for `supply_chain.db` in `src/backend/`) |
