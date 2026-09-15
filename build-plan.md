# Build Plan — Supply Chain Disruption Assistant & Fleet Utilisation Optimizer

## Stack (locked)
- **Backend:** Python 3.11, FastAPI, IBM Bob SDK, watsonx.ai (Granite), SQLite
- **Frontend:** React 18, Vite
- **MCP Tools:** 4 registered Python functions
- **Data:** Simulated JSON seed files (no live APIs)
- **Granite:** Stubbed during build — `watsonx_client.py` returns mock responses until real `WATSONX_API_KEY` is set
- **Bob agent:** Runs server-side inside FastAPI; called via `POST /api/agent/query`

## Source Layout
```
src/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── database.py              # SQLite init + seed orchestration
│   ├── models.py                # SQLAlchemy table models
│   ├── watsonx_client.py        # Granite inference wrapper
│   ├── tools/
│   │   ├── shipment_impact.py   # MCP Tool 1
│   │   ├── rerouting.py         # MCP Tool 2
│   │   ├── fleet_scanner.py     # MCP Tool 3
│   │   └── cold_chain.py        # MCP Tool 4
│   ├── routers/
│   │   └── api.py               # All REST endpoints
│   ├── seed/
│   │   ├── disruptions.json
│   │   ├── shipments.json
│   │   ├── fleet.json
│   │   └── iot_logs.json
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── pages/
    │   │   ├── Dashboard.jsx
    │   │   ├── Disruptions.jsx
    │   │   ├── Fleet.jsx
    │   │   └── ColdChain.jsx
    │   └── api/client.js
    ├── package.json
    └── vite.config.js
```

---

## Phase 1 — Foundation: Data Models + Seed Data + DB Init
**Delivers:** A runnable backend that seeds SQLite on startup. No logic yet — just structure.

### Files to create
- `src/backend/models.py` — 5 SQLAlchemy models: `DisruptionEvent`, `Shipment`, `ShipmentLeg`, `FleetAsset`, `IotSensorLog`
- `src/backend/database.py` — creates tables, runs seed loader on first run
- `src/backend/seed/disruptions.json` — 5 disruption events (2 port strikes, 2 weather, 1 geopolitical)
- `src/backend/seed/shipments.json` — 20 shipments, each with 2–3 legs, cargo type, ETA, affected region
- `src/backend/seed/fleet.json` — 15 fleet assets with location, type, load status
- `src/backend/seed/iot_logs.json` — temperature readings for 8 refrigerated shipments (3 with excursions)
- `src/backend/requirements.txt` — pinned deps
- `src/backend/.env.example` — final env vars (WATSONX only, no Postgres/Slack)
- `src/backend/main.py` — bare FastAPI app with DB init on startup, single `GET /health` route

**Done when:** `uvicorn main:app --reload` starts, `/health` returns 200, SQLite is seeded.

---

## Phase 2 — MCP Tools 1 & 2: Shipment Impact + Re-routing
**Delivers:** The two highest-value analysis tools. Bob agent can answer "which shipments are affected?" and "what are rerouting options?"

### Files to create / edit
- `src/backend/watsonx_client.py` — thin wrapper: `generate(prompt: str) -> str` using IBM watsonx.ai Python SDK
- `src/backend/tools/shipment_impact.py` — pure function: reads disruptions + shipment legs from DB, returns list of `{shipment_id, affected_leg, severity_score, disruption_id}`
- `src/backend/tools/rerouting.py` — pure function: takes affected shipment record, builds Granite prompt, returns `{shipment_id, ranked_alternatives: [{carrier, route, delay_days, reasoning}]}`
- `src/backend/routers/api.py` — two endpoints:
  - `GET /api/disruptions/impact` — runs shipment impact tool, returns JSON
  - `POST /api/shipments/{id}/reroute` — runs rerouting tool for one shipment
- Wire routers into `main.py`

**Done when:** `/api/disruptions/impact` returns affected shipments list; `/api/shipments/{id}/reroute` returns Granite-generated alternatives.

---

## Phase 3 — MCP Tools 3 & 4: Fleet Scanner + Cold Chain Monitor
**Delivers:** Idle asset redeployment + cold chain excursion classification. Completes all 4 core capabilities.

### Files to create / edit
- `src/backend/tools/fleet_scanner.py` — pure function: filters fleet assets by `status=idle`, ranks by proximity to disrupted regions, returns `[{asset_id, type, location, capacity, proximity_km}]`
- `src/backend/tools/cold_chain.py` — pure function: scans IoT logs for readings outside cargo thresholds, calls Granite to classify severity per excursion, returns `[{shipment_id, cargo_type, excursion_temp, severity, action}]`
- `src/backend/routers/api.py` — add two more endpoints:
  - `GET /api/fleet/idle` — runs fleet scanner
  - `GET /api/coldchain/alerts` — runs cold chain monitor

**Done when:** All 4 tool endpoints return correct structured JSON with no real API key (mocked Granite response acceptable in test).

---

## Phase 4 — Bob Agent Wiring
**Delivers:** IBM Bob agent that orchestrates all 4 tools via MCP, answering natural-language operator queries.

### Files to create
- `src/backend/agent.py` — registers all 4 tool functions as Bob MCP tools; defines the Bob agent with a system prompt scoped to supply chain operations; exposes `run_query(user_input: str) -> str`
- `src/backend/routers/api.py` — add `POST /api/agent/query` endpoint that calls `agent.run_query`

**Done when:** `POST /api/agent/query` with body `{"query": "Which shipments are affected by the Rotterdam port strike?"}` returns a coherent Bob agent response.

---

## Phase 5 — React Dashboard
**Delivers:** Visual frontend with 4 panels: Disruption Alerts, Affected Shipments + Rerouting, Fleet Map, Cold Chain Alerts.

### Files to create
- `src/frontend/` — Vite + React 18 scaffold (`npm create vite@latest`)
- `src/frontend/src/api/client.js` — axios client pointing to `http://localhost:8000`
- `src/frontend/src/pages/Dashboard.jsx` — summary cards: active disruptions count, affected shipments count, idle assets count, cold chain alerts count
- `src/frontend/src/pages/Disruptions.jsx` — table of affected shipments + inline rerouting panel
- `src/frontend/src/pages/Fleet.jsx` — table of idle fleet assets with type/location/capacity
- `src/frontend/src/pages/ColdChain.jsx` — table of excursion alerts with severity badge + recommended action
- `src/frontend/src/App.jsx` — tab navigation across 4 pages

**Done when:** Dashboard loads at `localhost:5173`, all 4 tabs show real data from the backend.

---

## Phase 6 — Demo Script + Final Wiring
**Delivers:** The `run_demo_scenario.py` script referenced in setup-guide.md + final validation pass.

### Files to create
- `src/backend/demo/run_demo_scenario.py` — CLI script: seeds a fresh Rotterdam port strike, runs all 4 tools, prints structured output to stdout
- Update `src/backend/.env.example` to final state
- Verify GitHub Actions validator passes (no `[` in README, submission.yaml valid, `src/` non-empty)

**Done when:** `python demo/run_demo_scenario.py --scenario port_strike_rotterdam` prints full analysis output; GitHub Actions green.

---

## Build Order Summary

| Phase | What | Key Output |
|---|---|---|
| 1 | DB models + seed data + FastAPI skeleton | `/health` + seeded SQLite |
| 2 | Shipment Impact + Re-routing tools + API | `/api/disruptions/impact` + `/reroute` |
| 3 | Fleet Scanner + Cold Chain tools + API | `/api/fleet/idle` + `/api/coldchain/alerts` |
| 4 | Bob agent MCP wiring | `/api/agent/query` |
| 5 | React dashboard | 4-tab UI at `localhost:5173` |
| 6 | Demo script + final validation | Validator passes |

## Sequence Rule
**Complete and verify each phase before starting the next.** Phases 2 and 3 can be split across sessions — each tool is independently testable via its endpoint.
