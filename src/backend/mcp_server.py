"""
MCP stdio server — registers all 4 supply chain tools so Bob IDE
can call them directly via the Model Context Protocol.

Usage (register in Bob's mcp.json):
  {
    "mcpServers": {
      "supply-chain-assistant": {
        "command": "python",
        "args": ["<absolute-path>/src/backend/mcp_server.py"],
        "env": {
          "WATSONX_API_KEY": "<your-key>",
          "WATSONX_PROJECT_ID": "<your-project-id>",
          "WATSONX_URL": "https://us-south.ml.cloud.ibm.com"
        }
      }
    }
  }

Run standalone (for testing):
  python mcp_server.py
"""
import sys
import json
import asyncio
from pathlib import Path

# Ensure local modules are importable when run as a script
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from database import init_db, SessionLocal
from tools.shipment_impact import analyze_shipment_impact
from tools.rerouting import get_rerouting_recommendation
from tools.fleet_scanner import scan_idle_fleet
from tools.cold_chain import monitor_cold_chain

# Initialise DB on startup (seeds if first run)
init_db()

app = Server("supply-chain-assistant")


# ---------------------------------------------------------------------------
# Tool 1 — analyze_disruption_impact
# ---------------------------------------------------------------------------
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="analyze_disruption_impact",
            description=(
                "Identifies all active shipments affected by current disruption events "
                "(port strikes, weather, geopolitical). Returns affected shipments with "
                "impact severity scores sorted highest first."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_rerouting_recommendation",
            description=(
                "For a given shipment ID, returns AI-generated ranked rerouting recommendations "
                "with alternative carriers, estimated delay, cost differential, and reasoning."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "shipment_id": {
                        "type": "integer",
                        "description": "The numeric ID of the affected shipment to reroute",
                    }
                },
                "required": ["shipment_id"],
            },
        ),
        types.Tool(
            name="scan_idle_fleet",
            description=(
                "Scans fleet telemetry to find idle trucks, containers, reefer units and vessels "
                "available for redeployment. Optionally filter by disrupted region."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "region": {
                        "type": "string",
                        "description": "Optional region to filter by (e.g. 'Rotterdam', 'Suez Canal'). Omit for all regions.",
                    }
                },
                "required": [],
            },
        ),
        types.Tool(
            name="monitor_cold_chain",
            description=(
                "Scans IoT temperature sensor logs for all refrigerated shipments. "
                "Detects excursions, classifies severity (MINOR DEVIATION, REPORTABLE BREACH, CRITICAL) "
                "using watsonx.ai, and returns actionable alerts sorted by severity."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]


# ---------------------------------------------------------------------------
# Tool dispatcher
# ---------------------------------------------------------------------------
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    db = None
    try:
        db = SessionLocal()
        if name == "analyze_disruption_impact":
            result = analyze_shipment_impact(db)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_rerouting_recommendation":
            shipment_id = arguments.get("shipment_id")
            if not isinstance(shipment_id, int):
                return [types.TextContent(type="text", text='{"error": "shipment_id must be an integer"}')]
            result = get_rerouting_recommendation(shipment_id, db)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "scan_idle_fleet":
            region = arguments.get("region")
            result = scan_idle_fleet(db, region=region)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "monitor_cold_chain":
            result = monitor_cold_chain(db)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [types.TextContent(type="text", text=f'{{"error": "Unknown tool: {name}"}}'  )]

    except Exception as exc:
        return [types.TextContent(type="text", text=json.dumps({"error": str(exc)}))]
    finally:
        if db is not None:
            db.close()


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
