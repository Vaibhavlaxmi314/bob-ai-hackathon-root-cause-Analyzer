"""
Tool 2 — Re-routing Advisor
For a given affected shipment, calls watsonx.ai Granite to produce
ranked rerouting / carrier alternatives with reasoning.
"""
from sqlalchemy.orm import Session
from models import Shipment, DisruptionEvent
from watsonx_client import generate


# Known carrier alternatives per disrupted region (static knowledge base)
_CARRIER_ALTERNATIVES = {
    "Rotterdam": ["CMA CGM via Antwerp", "MSC via Hamburg", "Air freight via Frankfurt"],
    "South China Sea": ["CMA CGM via Malacca Strait", "Air freight via Hong Kong", "Rail via Trans-Siberian"],
    "Suez Canal": ["Cape of Good Hope diversion", "Air freight via Dubai", "Rail via Turkey-Iran corridor"],
    "Los Angeles": ["Rail to Long Beach", "Air freight via LAX", "Reroute to Port of Oakland"],
    "Gulf of Mexico": ["Reroute via Atlantic coast", "Air freight via Miami", "Hold at origin"],
}


def get_rerouting_recommendation(shipment_id: int, db: Session) -> dict:
    """
    Build a structured prompt for the given shipment and call Granite
    to get ranked rerouting alternatives.
    """
    shipment = db.query(Shipment).get(shipment_id)
    if not shipment:
        return {"error": f"Shipment {shipment_id} not found"}

    disruption = None
    if shipment.disruption_id:
        disruption = db.query(DisruptionEvent).get(shipment.disruption_id)

    region = disruption.region if disruption else "unknown region"
    alternatives = _CARRIER_ALTERNATIVES.get(region, ["Air freight", "Alternative carrier", "Hold at origin"])

    prompt = (
        f"You are a logistics rerouting advisor. A shipment is blocked by a supply chain disruption.\n\n"
        f"SHIPMENT DETAILS:\n"
        f"- Reference: {shipment.shipment_ref}\n"
        f"- Origin: {shipment.origin}\n"
        f"- Destination: {shipment.destination}\n"
        f"- Cargo type: {shipment.cargo_type}\n"
        f"- Cargo value: USD {shipment.cargo_value_usd:,.0f}\n"
        f"- Priority: {shipment.priority}\n"
        f"- Carrier: {shipment.carrier}\n"
        f"- ETA: {shipment.eta.strftime('%Y-%m-%d') if shipment.eta else 'unknown'}\n\n"
        f"DISRUPTION:\n"
        f"- Type: {disruption.event_type if disruption else 'unknown'}\n"
        f"- Region: {region}\n"
        f"- Severity: {disruption.severity if disruption else 'unknown'}/10\n"
        f"- Description: {disruption.description if disruption else 'n/a'}\n\n"
        f"AVAILABLE REROUTING OPTIONS:\n"
        + "\n".join(f"- {a}" for a in alternatives)
        + "\n\nProvide 3 ranked rerouting recommendations with estimated delay impact, "
        f"cost differential, and plain-language reasoning for each. "
        f"Label them RECOMMENDATION 1, RECOMMENDATION 2, RECOMMENDATION 3."
    )

    raw_response = generate(prompt)

    return {
        "shipment_id": shipment.id,
        "shipment_ref": shipment.shipment_ref,
        "origin": shipment.origin,
        "destination": shipment.destination,
        "disruption_region": region,
        "disruption_type": disruption.event_type if disruption else None,
        "recommendations_raw": raw_response,
        "recommendations": _parse_recommendations(raw_response),
    }


def _parse_recommendations(text: str) -> list[dict]:
    """Parse RECOMMENDATION N: ... blocks into structured list."""
    recommendations = []
    for i in range(1, 4):
        marker = f"RECOMMENDATION {i}:"
        next_marker = f"RECOMMENDATION {i + 1}:"
        start = text.find(marker)
        if start == -1:
            continue
        end = text.find(next_marker) if text.find(next_marker) != -1 else len(text)
        content = text[start + len(marker):end].strip()
        recommendations.append({"rank": i, "details": content})
    return recommendations
