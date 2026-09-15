# Solution Overview

## What We Built

The Supply Chain Disruption Assistant & Fleet Utilisation Optimizer is an AI-powered operational assistant built on IBM Bob. It gives logistics teams a single, unified view of how active disruptions affect their shipments, where their idle fleet assets are, and whether any temperature-sensitive cargo is at risk — all in real time, without requiring manual data gathering across siloed systems.

At its core, the solution is a Bob agent that ingests simulated disruption events, shipment manifests, fleet telemetry, and IoT temperature sensor logs, then uses watsonx.ai to reason across this data and produce actionable recommendations. Rather than surfacing raw data, it answers the questions operators actually need answered: "Which of my shipments are affected right now?", "What are my best rerouting options?", "Do I have idle assets nearby?", and "Is any cold chain cargo approaching a critical threshold?"

The system is accessible through a React dashboard that presents disruption alerts, affected shipment lists, rerouting suggestions, idle fleet asset maps, and cold chain excursion reports in a single operational view. All data is seeded from simulated sources at startup, making the solution fully demonstrable without requiring live API credentials.

## How It Works

1. **Disruption Event Ingestion** — A simulated disruption event feed (JSON) is ingested at startup via a Bob MCP tool. Each event carries a type (weather, port strike, geopolitical), affected region, severity score, and estimated duration. These events are stored in a local SQLite database.

2. **Shipment Impact Analysis** — The Bob agent cross-references each active disruption event against the shipment manifest (routes, legs, ETAs, cargo types). For each shipment whose active leg passes through a disrupted region, the agent marks it as affected and computes an impact severity score based on disruption type and shipment priority.

3. **Re-routing Recommendation** — For each affected shipment, the Bob agent queries the watsonx.ai Granite model with structured context — current route, disruption details, available carrier alternatives, and delivery deadline — and receives a ranked list of alternative routes or carriers with reasoning, estimated delay impact, and cost differential.

4. **Idle Fleet Asset Scan** — The agent analyses simulated fleet telemetry data to identify trucks, containers, and vessels that are currently idle or under-utilised in regions near the disruption. It surfaces these assets ranked by proximity and capacity match to the stranded shipments.

5. **Cold Chain Excursion Classification** — IoT temperature sensor logs for all refrigerated shipments are continuously scanned. When a reading exceeds or trends toward the applicable safe temperature range for the cargo type, the agent classifies the excursion severity (minor deviation, reportable breach, critical loss risk) using watsonx.ai and flags it on the dashboard with the affected shipment details and recommended immediate action.

## Architecture Diagram

For the full technical architecture diagram, see [`architecture.md`](architecture.md).

```
[Disruption Feed JSON]  [Shipment Manifest]  [Fleet Telemetry]  [IoT Sensor Logs]
          |                     |                    |                   |
          +---------------------+--------------------+-------------------+
                                          |
                              [Bob Agent Orchestrator]
                                          |
              +---------------------------+---------------------------+
              |                           |                           |
  [Shipment Impact Analyzer]  [Re-routing Advisor]     [Cold Chain IoT Monitor]
              |                           |                           |
              +---------------------------+---------------------------+
                                          |
                              [watsonx.ai — Granite]
                                          |
                              [SQLite — Local State]
                                          |
                              [React Dashboard UI]
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **IBM Bob as the agent orchestrator** | Bob's native agent and MCP tool framework provides a structured way to compose multiple specialised analysis steps — disruption mapping, rerouting, fleet scanning, cold chain monitoring — as discrete, testable tools rather than a monolithic pipeline. |
| **watsonx.ai Granite for reasoning and classification** | The re-routing recommendation and cold chain severity classification both require natural-language reasoning over structured context. Granite's instruction-following capability enables this without requiring custom model training, which is impractical in a hackathon scope. |
| **Simulated data seeded at startup** | Using simulated JSON data for disruption events, shipment manifests, fleet telemetry, and IoT sensor readings removes the dependency on live third-party APIs and credentials, making the solution fully demonstrable and reproducible by any judge without setup friction. |
| **SQLite for local state** | A lightweight embedded database avoids the need to run a separate database server, keeping local setup to a single `pip install` + environment variable configuration. All tables are seeded automatically on first run. |
| **Generic regulatory thresholds for cold chain severity** | Rather than hard-coding a single regulatory standard, the severity classifier uses configurable temperature threshold ranges per cargo type. This makes the system adaptable to multiple verticals (pharma, food, biotech) without requiring standard-specific legal knowledge in the model. |

## IBM Technologies Used

- **IBM Bob** — Bob serves as the orchestration runtime for the entire solution. The four analysis capabilities (disruption mapping, re-routing, fleet scanning, cold chain monitoring) are each implemented as a Bob tool registered via the MCP protocol. The Bob agent receives a user query or a scheduled trigger, selects and chains the appropriate tools, and synthesises the results into an actionable response. Bob's conversational interface also allows operators to ask ad-hoc questions such as "show me all affected shipments in the Asia-Pacific region" and receive structured answers without navigating a traditional UI.

- **watsonx.ai (IBM Granite model)** — watsonx.ai is used for two distinct inference tasks. For re-routing recommendations, the Granite model receives a structured prompt containing the disrupted shipment's current route, available carrier alternatives, delivery deadline, and cargo priority, and returns a ranked recommendation with plain-language reasoning. For cold chain severity classification, the model receives temperature excursion data (magnitude, duration, cargo type, applicable threshold) and classifies the severity level along with a recommended response action.
