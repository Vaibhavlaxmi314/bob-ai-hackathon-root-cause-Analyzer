from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pydantic import BaseModel
from database import get_db
from tools.shipment_impact import analyze_shipment_impact
from tools.rerouting import get_rerouting_recommendation
from tools.fleet_scanner import scan_idle_fleet
from tools.cold_chain import monitor_cold_chain
from agent import run_query

router = APIRouter(prefix="/api")


# ---------------------------------------------------------------------------
# Tool 1 — Disruption Impact
# ---------------------------------------------------------------------------
@router.get("/disruptions/impact", summary="List all shipments affected by active disruptions")
def disruptions_impact(db: Session = Depends(get_db)):
    results = analyze_shipment_impact(db)
    return {
        "total_affected": len(results),
        "shipments": results,
    }


@router.get("/disruptions", summary="List all disruption events")
def list_disruptions(db: Session = Depends(get_db)):
    from models import DisruptionEvent
    events = db.query(DisruptionEvent).all()
    return [
        {
            "id": e.id,
            "event_type": e.event_type,
            "region": e.region,
            "severity": e.severity,
            "description": e.description,
            "active": e.active,
            "started_at": e.started_at.isoformat() if e.started_at else None,
            "estimated_end": e.estimated_end.isoformat() if e.estimated_end else None,
        }
        for e in events
    ]


# ---------------------------------------------------------------------------
# Tool 3 — Fleet Asset Scanner
# ---------------------------------------------------------------------------
@router.get("/fleet/idle", summary="List idle fleet assets available for redeployment")
def fleet_idle(region: str | None = None, db: Session = Depends(get_db)):
    assets = scan_idle_fleet(db, region=region)
    return {
        "total_idle": len(assets),
        "filter_region": region,
        "assets": assets,
    }


@router.get("/fleet", summary="List all fleet assets")
def list_fleet(db: Session = Depends(get_db)):
    from models import FleetAsset
    assets = db.query(FleetAsset).all()
    return [
        {
            "id": a.id,
            "asset_ref": a.asset_ref,
            "asset_type": a.asset_type,
            "location": a.location,
            "region": a.region,
            "capacity_tonnes": a.capacity_tonnes,
            "status": a.status,
        }
        for a in assets
    ]


# ---------------------------------------------------------------------------
# Tool 4 — Cold Chain Monitor
# ---------------------------------------------------------------------------
@router.get("/coldchain/alerts", summary="Get cold chain excursion alerts for all refrigerated shipments")
def coldchain_alerts(db: Session = Depends(get_db)):
    alerts = monitor_cold_chain(db)
    return {
        "total_alerts": len(alerts),
        "critical": sum(1 for a in alerts if a["severity"] == "CRITICAL"),
        "reportable": sum(1 for a in alerts if a["severity"] == "REPORTABLE BREACH"),
        "minor": sum(1 for a in alerts if a["severity"] == "MINOR DEVIATION"),
        "alerts": alerts,
    }


# ---------------------------------------------------------------------------
# Tool 2 — Re-routing
# ---------------------------------------------------------------------------
@router.post("/shipments/{shipment_id}/reroute", summary="Get rerouting recommendations for an affected shipment")
def reroute_shipment(shipment_id: int, db: Session = Depends(get_db)):
    result = get_rerouting_recommendation(shipment_id, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/shipments", summary="List all shipments")
def list_shipments(db: Session = Depends(get_db)):
    from models import Shipment
    shipments = db.query(Shipment).all()
    return [
        {
            "id": s.id,
            "shipment_ref": s.shipment_ref,
            "origin": s.origin,
            "destination": s.destination,
            "cargo_type": s.cargo_type,
            "cargo_value_usd": s.cargo_value_usd,
            "priority": s.priority,
            "carrier": s.carrier,
            "status": s.status,
            "affected": s.affected,
            "impact_severity": s.impact_severity,
            "eta": s.eta.isoformat() if s.eta else None,
        }
        for s in shipments
    ]


# ---------------------------------------------------------------------------
# Agent — natural language query endpoint
# ---------------------------------------------------------------------------
class QueryRequest(BaseModel):
    query: str


@router.post("/agent/query", summary="Ask the supply chain assistant a natural language question")
def agent_query(body: QueryRequest, db: Session = Depends(get_db)):
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")
    return run_query(body.query, db)
