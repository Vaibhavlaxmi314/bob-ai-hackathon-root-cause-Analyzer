"""
Demo scenario runner — exercises all 4 tools end-to-end and prints
structured output to stdout. Referenced in docs/setup-guide.md.

Usage:
    python demo/run_demo_scenario.py --scenario port_strike_rotterdam
    python demo/run_demo_scenario.py --scenario suez_closure
    python demo/run_demo_scenario.py --scenario cold_chain_emergency
"""
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from database import init_db, SessionLocal
from tools.shipment_impact import analyze_shipment_impact
from tools.rerouting import get_rerouting_recommendation
from tools.fleet_scanner import scan_idle_fleet
from tools.cold_chain import monitor_cold_chain
from agent import run_query


def separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def run_scenario(scenario: str):
    init_db()
    db = SessionLocal()

    try:
        if scenario == "port_strike_rotterdam":
            separator("SCENARIO: Rotterdam Port Strike")
            print("Disruption: Port workers strike halting all container operations.\n")

            separator("STEP 1 — Shipment Impact Analysis")
            affected = analyze_shipment_impact(db)
            rotterdam = [s for s in affected if s["disruption"]["region"] == "Rotterdam"]
            print(f"Total affected shipments (all disruptions): {len(affected)}")
            print(f"Affected by Rotterdam specifically: {len(rotterdam)}")
            for s in rotterdam[:3]:
                print(f"  - {s['shipment_ref']}: {s['origin']} → {s['destination']} | severity {s['impact_severity']}/10 | carrier: {s['carrier']}")

            separator("STEP 2 — Re-routing Recommendations (top 2 Rotterdam shipments)")
            for s in rotterdam[:2]:
                rec = get_rerouting_recommendation(s["shipment_id"], db)
                print(f"\nShipment {rec['shipment_ref']}:")
                for r in rec["recommendations"]:
                    print(f"  Option {r['rank']}: {r['details'][:120]}...")

            separator("STEP 3 — Idle Fleet Assets Near Rotterdam")
            fleet = scan_idle_fleet(db, region="Rotterdam")
            print(f"Idle assets available: {len(fleet)}")
            for a in fleet:
                print(f"  - {a['asset_ref']} ({a['asset_type']}) — {a['location']} — {a['capacity_tonnes']}t")

            separator("STEP 4 — Cold Chain Excursion Check")
            alerts = monitor_cold_chain(db)
            print(f"Cold chain alerts: {len(alerts)} | Critical: {sum(1 for a in alerts if a['severity']=='CRITICAL')}")
            for a in alerts[:2]:
                print(f"  - {a['shipment_ref']}: {a['excursion_temp']}°C (safe: {a['safe_range']}) — {a['severity']}")

            separator("STEP 5 — Agent Natural Language Summary")
            result = run_query("What is the current disruption situation and what should I do about the Rotterdam port strike?", db)
            print(result["response"])

        elif scenario == "suez_closure":
            separator("SCENARIO: Suez Canal Closure")
            affected = analyze_shipment_impact(db)
            suez = [s for s in affected if s["disruption"]["region"] == "Suez Canal"]
            print(f"Shipments affected by Suez closure: {len(suez)}")
            for s in suez:
                print(f"  - {s['shipment_ref']}: {s['origin']} → {s['destination']} | ${s['cargo_value_usd']:,.0f} | severity {s['impact_severity']}/10")

        elif scenario == "cold_chain_emergency":
            separator("SCENARIO: Cold Chain Emergency")
            alerts = monitor_cold_chain(db)
            critical = [a for a in alerts if a["severity"] == "CRITICAL"]
            print(f"CRITICAL excursions: {len(critical)}")
            for a in critical:
                print(f"\n  Shipment: {a['shipment_ref']}")
                print(f"  Cargo: {a['cargo_type']} | Safe range: {a['safe_range']}")
                print(f"  Recorded: {a['excursion_temp']}°C | Deviation: +{abs(a['deviation'])}°C")
                print(f"  Action: {a['action']}")

        else:
            print(f"Unknown scenario: {scenario}")
            print("Available: port_strike_rotterdam | suez_closure | cold_chain_emergency")
            sys.exit(1)

    finally:
        db.close()

    print("\n" + "="*60)
    print("  Demo complete.")
    print("="*60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a supply chain demo scenario")
    parser.add_argument("--scenario", required=True, help="Scenario name")
    args = parser.parse_args()
    run_scenario(args.scenario)
