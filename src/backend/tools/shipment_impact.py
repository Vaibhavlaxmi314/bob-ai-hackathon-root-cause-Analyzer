"""
Tool 1 — Shipment Impact Analyzer
Cross-references active disruption events against shipment legs.
Returns all affected shipments with impact severity scores.
"""
from sqlalchemy.orm import Session
from models import DisruptionEvent, Shipment, ShipmentLeg


def analyze_shipment_impact(db: Session) -> list[dict]:
    """
    For each active disruption, find shipments whose non-completed legs
    pass through the disrupted region. Compute an impact severity score
    (disruption severity * priority multiplier). Update the shipment record.
    Returns list of affected shipment dicts.
    """
    priority_weight = {"high": 1.0, "normal": 0.7, "low": 0.4}

    active_disruptions = (
        db.query(DisruptionEvent).filter(DisruptionEvent.active == True).all()
    )

    affected = []

    for disruption in active_disruptions:
        # Find legs in the disrupted region that are not completed
        matching_legs = (
            db.query(ShipmentLeg)
            .filter(
                ShipmentLeg.via_region == disruption.region,
                ShipmentLeg.status.in_(["pending", "active"]),
            )
            .all()
        )

        seen_shipments = set()
        for leg in matching_legs:
            if leg.shipment_id in seen_shipments:
                continue
            seen_shipments.add(leg.shipment_id)

            shipment = db.query(Shipment).get(leg.shipment_id)
            if not shipment or shipment.status == "delivered":
                continue

            weight = priority_weight.get(shipment.priority, 0.7)
            score = round(disruption.severity * weight)

            # Update shipment record
            shipment.affected = True
            shipment.impact_severity = score
            shipment.disruption_id = disruption.id

            affected.append({
                "shipment_id": shipment.id,
                "shipment_ref": shipment.shipment_ref,
                "origin": shipment.origin,
                "destination": shipment.destination,
                "cargo_type": shipment.cargo_type,
                "cargo_value_usd": shipment.cargo_value_usd,
                "priority": shipment.priority,
                "carrier": shipment.carrier,
                "eta": shipment.eta.isoformat() if shipment.eta else None,
                "affected_leg": {
                    "from": leg.from_location,
                    "to": leg.to_location,
                    "via_region": leg.via_region,
                    "mode": leg.mode,
                },
                "disruption": {
                    "id": disruption.id,
                    "event_type": disruption.event_type,
                    "region": disruption.region,
                    "severity": disruption.severity,
                    "description": disruption.description,
                },
                "impact_severity": score,
            })

    db.commit()

    # Sort by impact severity descending
    affected.sort(key=lambda x: x["impact_severity"], reverse=True)
    return affected
