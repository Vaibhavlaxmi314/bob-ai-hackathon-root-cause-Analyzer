"""
Tool 3 — Fleet Asset Scanner
Identifies idle or under-utilised fleet assets near disrupted regions.
Returns ranked redeployment suggestions.
"""
from sqlalchemy.orm import Session
from models import FleetAsset, DisruptionEvent


# Simple proximity map: regions considered "near" each disrupted region
_NEARBY_REGIONS = {
    "Rotterdam":       ["Rotterdam", "South China Sea"],  # vessels from SCS can divert
    "South China Sea": ["South China Sea", "Arabian Sea"],
    "Suez Canal":      ["Suez Canal", "Arabian Sea", "Rotterdam"],
    "Los Angeles":     ["Los Angeles", "Pacific"],
    "Gulf of Mexico":  ["Gulf of Mexico"],
}


def scan_idle_fleet(db: Session, region: str | None = None) -> list[dict]:
    """
    If region is given, return idle assets in/near that region.
    If region is None, return ALL idle assets across all regions.
    Results are sorted by capacity descending.
    """
    query = db.query(FleetAsset).filter(FleetAsset.status == "idle")

    if region:
        nearby = _NEARBY_REGIONS.get(region, [region])
        query = query.filter(FleetAsset.region.in_(nearby))

    assets = query.order_by(FleetAsset.capacity_tonnes.desc()).all()

    # Enrich with active disruption context
    active_disruptions = (
        db.query(DisruptionEvent).filter(DisruptionEvent.active == True).all()
    )
    disrupted_regions = {d.region for d in active_disruptions}

    return [
        {
            "asset_id": a.id,
            "asset_ref": a.asset_ref,
            "asset_type": a.asset_type,
            "location": a.location,
            "region": a.region,
            "capacity_tonnes": a.capacity_tonnes,
            "status": a.status,
            "near_disruption": a.region in disrupted_regions,
            "suggested_for": _suggest_disruption(a.region, active_disruptions),
        }
        for a in assets
    ]


def _suggest_disruption(asset_region: str, disruptions: list) -> str | None:
    nearby_map = {v: k for k, vs in _NEARBY_REGIONS.items() for v in vs}
    disrupted_region = nearby_map.get(asset_region)
    for d in disruptions:
        if d.region == disrupted_region and d.active:
            return f"{d.event_type.replace('_', ' ').title()} — {d.region}"
    return None
