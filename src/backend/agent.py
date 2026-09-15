"""
Agent Orchestrator — runs server-side, chains the 4 tools,
calls watsonx.ai to produce a natural-language response.
Called via POST /api/agent/query from the dashboard.
"""
import json
import logging
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from tools.shipment_impact import analyze_shipment_impact
from tools.rerouting import get_rerouting_recommendation
from tools.fleet_scanner import scan_idle_fleet
from tools.cold_chain import monitor_cold_chain
from watsonx_client import generate


_SYSTEM_PROMPT = """You are a Supply Chain Disruption Assistant for logistics operations teams.
You have access to four analysis tools:
1. Shipment Impact Analyzer — identifies which active shipments are affected by disruptions
2. Re-routing Advisor — recommends alternative routes and carriers for affected shipments
3. Fleet Asset Scanner — finds idle trucks, containers and vessels available for redeployment
4. Cold Chain Monitor — detects temperature excursions in refrigerated shipments

Answer the operator's question using the tool results provided. Be concise and actionable.
Format your response in plain language — no markdown, no bullet symbols, just clear sentences."""


def run_query(user_input: str, db: Session) -> dict:
    """
    Determine which tools are relevant to the query, run them,
    build a context-rich prompt, and call Granite for a synthesised response.
    """
    q = user_input.lower()

    # --- Run relevant tools based on query keywords ---
    tool_results = {}

    run_all = not any(kw in q for kw in ["fleet", "cold chain", "temperature", "reroute", "route"])

    if run_all or any(kw in q for kw in ["affect", "impact", "disrupt", "shipment", "stranded", "blocked"]):
        tool_results["impact"] = analyze_shipment_impact(db)

    if run_all or any(kw in q for kw in ["reroute", "route", "alternative", "carrier", "bypass"]):
        # Reroute top 3 affected shipments
        impact = tool_results.get("impact") or analyze_shipment_impact(db)
        reroutes = []
        for s in impact[:3]:
            r = get_rerouting_recommendation(s["shipment_id"], db)
            reroutes.append(r)
        tool_results["rerouting"] = reroutes

    if run_all or any(kw in q for kw in ["fleet", "idle", "truck", "vessel", "container", "asset", "redeploy"]):
        tool_results["fleet"] = scan_idle_fleet(db)

    if run_all or any(kw in q for kw in ["cold chain", "temperature", "excursion", "reefer", "freeze", "spoil"]):
        tool_results["cold_chain"] = monitor_cold_chain(db)

    # --- Build synthesis prompt ---
    context_parts = [f"OPERATOR QUERY: {user_input}\n"]

    if "impact" in tool_results:
        affected = tool_results["impact"] or []
        top = affected[0] if affected else None
        context_parts.append(
            f"SHIPMENT IMPACT: {len(affected)} shipments affected by active disruptions. "
            + (f"Top affected: {top['shipment_ref']} ({top['origin']} → {top['destination']}, "
               f"severity {top['impact_severity']}/10, disruption: {top['disruption']['region']})."
               if top else "No shipments currently affected.")
        )

    if "rerouting" in tool_results:
        for r in tool_results["rerouting"]:
            recs = r.get("recommendations") or []
            if recs:
                context_parts.append(
                    f"REROUTING {r.get('shipment_ref', 'unknown')}: Best option — {recs[0]['details'][:120]}..."
                )

    if "fleet" in tool_results:
        fleet = tool_results["fleet"] or []
        top_asset = fleet[0] if fleet else None
        context_parts.append(
            f"IDLE FLEET: {len(fleet)} assets available. "
            + (f"Largest: {top_asset['asset_ref']} ({top_asset['asset_type']}, "
               f"{top_asset['capacity_tonnes']}t, {top_asset['location']})." if top_asset else "No idle assets.")
        )

    if "cold_chain" in tool_results:
        cc = tool_results["cold_chain"] or []
        critical = [a for a in cc if a.get("severity") == "CRITICAL"]
        top_crit = critical[0] if critical else None
        context_parts.append(
            f"COLD CHAIN: {len(cc)} excursion alerts. "
            f"{len(critical)} CRITICAL. "
            + (f"Most severe: {top_crit['shipment_ref']} at {top_crit['excursion_temp']}°C "
               f"(safe range {top_crit['safe_range']})." if top_crit else "")
        )

    synthesis_prompt = (
        _SYSTEM_PROMPT + "\n\n"
        + "\n".join(context_parts)
        + "\n\nProvide a clear, actionable 3-5 sentence response to the operator's query."
    )

    try:
        response_text = generate(synthesis_prompt)
    except Exception as exc:
        logger.error("Agent synthesis generate failed: %s", exc)
        response_text = "Unable to generate a response at this time. Please try again."

    return {
        "query": user_input,
        "response": response_text,
        "tools_used": list(tool_results.keys()),
        "summary": {
            "affected_shipments": len(tool_results.get("impact", [])),
            "idle_fleet_assets": len(tool_results.get("fleet", [])),
            "cold_chain_alerts": len(tool_results.get("cold_chain", [])),
        },
    }
