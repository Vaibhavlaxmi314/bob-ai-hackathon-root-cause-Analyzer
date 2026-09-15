"""
Tool 4 — Cold Chain IoT Monitor
Scans IoT sensor logs for temperature excursions.
Calls watsonx.ai Granite to classify severity and recommend action.
"""
import logging
from sqlalchemy.orm import Session
from models import IotSensorLog
from watsonx_client import generate

logger = logging.getLogger(__name__)


def monitor_cold_chain(db: Session) -> list[dict]:
    """
    Find all sensor readings that are excursions (is_excursion=True).
    Group by shipment, take the worst reading per shipment,
    call Granite to classify severity, persist result, return alerts.
    """
    excursions = (
        db.query(IotSensorLog)
        .filter(IotSensorLog.is_excursion == True)
        .order_by(IotSensorLog.shipment_id, IotSensorLog.recorded_at)
        .all()
    )

    # Group by shipment — keep worst (furthest from range)
    worst: dict[int, IotSensorLog] = {}
    for log in excursions:
        deviation = max(
            abs(log.temp_celsius - log.safe_max),
            abs(log.temp_celsius - log.safe_min),
        )
        if log.shipment_id not in worst:
            worst[log.shipment_id] = (log, deviation)
        else:
            _, prev_dev = worst[log.shipment_id]
            if deviation > prev_dev:
                worst[log.shipment_id] = (log, deviation)

    needs_commit = False
    alerts = []
    for shipment_id, (log, _) in worst.items():
        # Call Granite if not already classified
        if not log.severity:
            prompt = (
                f"You are a cold chain compliance analyst.\n"
                f"A temperature excursion has been detected on a refrigerated shipment.\n\n"
                f"SHIPMENT: {log.shipment_ref}\n"
                f"CARGO TYPE: {log.cargo_type}\n"
                f"SAFE TEMPERATURE RANGE: {log.safe_min}°C to {log.safe_max}°C\n"
                f"RECORDED TEMPERATURE: {log.temp_celsius}°C\n"
                f"RECORDED AT: {log.recorded_at}\n\n"
                f"Classify the severity of this excursion as one of: MINOR DEVIATION, "
                f"REPORTABLE BREACH, or CRITICAL. Provide a recommended action. "
                f"Start your response with 'SEVERITY: <level>.' then 'ACTION: <action>.'"
            )
            try:
                response = generate(prompt)
            except Exception as exc:
                logger.error("Cold chain generate failed for shipment %s: %s", shipment_id, exc)
                response = ""
            severity, action = _parse_cold_chain_response(response)
            log.severity = severity
            log.action = action
            needs_commit = True

        alerts.append({
            "shipment_id": log.shipment_id,
            "shipment_ref": log.shipment_ref,
            "cargo_type": log.cargo_type,
            "safe_range": f"{log.safe_min}°C to {log.safe_max}°C",
            "excursion_temp": log.temp_celsius,
            "deviation": round(log.temp_celsius - log.safe_max, 1) if log.temp_celsius > log.safe_max
                         else round(log.safe_min - log.temp_celsius, 1),
            "recorded_at": log.recorded_at.isoformat(),
            "severity": log.severity,
            "action": log.action,
        })

    # Persist all severity classifications in a single transaction
    if needs_commit:
        try:
            db.commit()
        except Exception as exc:
            logger.error("Cold chain DB commit failed: %s", exc)
            db.rollback()

    # Sort by severity: CRITICAL first, then REPORTABLE BREACH, then MINOR
    severity_order = {"CRITICAL": 0, "REPORTABLE BREACH": 1, "MINOR DEVIATION": 2}
    alerts.sort(key=lambda x: severity_order.get(x["severity"] or "", 3))
    return alerts


def _parse_cold_chain_response(text: str) -> tuple[str, str]:
    severity = "MINOR DEVIATION"
    action = text.strip()

    if "CRITICAL" in text.upper():
        severity = "CRITICAL"
    elif "REPORTABLE" in text.upper():
        severity = "REPORTABLE BREACH"

    action_start = text.upper().find("ACTION:")
    if action_start != -1:
        action = text[action_start + 7:].strip().split("\n")[0].strip()

    return severity, action
