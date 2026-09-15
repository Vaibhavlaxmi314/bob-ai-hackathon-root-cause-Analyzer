import json
import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from models import Base, DisruptionEvent, Shipment, ShipmentLeg, FleetAsset, IotSensorLog

DB_PATH = Path(__file__).parent / "supply_chain.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Enable WAL mode for SQLite — safer concurrent reads
@event.listens_for(engine, "connect")
def set_wal(dbapi_conn, _):
    dbapi_conn.execute("PRAGMA journal_mode=WAL")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SEED_DIR = Path(__file__).parent / "seed"


def _parse_dt(s):
    return datetime.fromisoformat(s) if s else None


def _load_seed(filename: str) -> list:
    """Read a seed JSON file; return empty list and log a warning if missing."""
    path = SEED_DIR / filename
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        logger.warning("Seed file not found, skipping: %s", path)
        return []
    except json.JSONDecodeError as exc:
        logger.error("Malformed seed file %s: %s", path, exc)
        return []


def init_db():
    """Create tables and seed data if the DB is brand new."""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        # Only seed if tables are empty
        if session.query(DisruptionEvent).count() > 0:
            return

        # --- Disruptions ---
        for d in _load_seed("disruptions.json"):
            session.add(DisruptionEvent(
                id=d["id"],
                event_type=d["event_type"],
                region=d["region"],
                severity=d["severity"],
                description=d["description"],
                active=d["active"],
                started_at=_parse_dt(d["started_at"]),
                estimated_end=_parse_dt(d.get("estimated_end")),
            ))

        # --- Shipments + Legs ---
        for s in _load_seed("shipments.json"):
            shipment = Shipment(
                id=s["id"],
                shipment_ref=s["shipment_ref"],
                origin=s["origin"],
                destination=s["destination"],
                cargo_type=s["cargo_type"],
                cargo_value_usd=s["cargo_value_usd"],
                priority=s["priority"],
                carrier=s["carrier"],
                eta=_parse_dt(s.get("eta")),
                status=s["status"],
            )
            session.add(shipment)
            for leg in s.get("legs", []):
                session.add(ShipmentLeg(
                    shipment_id=s["id"],
                    leg_order=leg["leg_order"],
                    from_location=leg["from_location"],
                    to_location=leg["to_location"],
                    via_region=leg["via_region"],
                    mode=leg["mode"],
                    status=leg["status"],
                ))

        # --- Fleet Assets ---
        for f in _load_seed("fleet.json"):
            session.add(FleetAsset(
                id=f["id"],
                asset_ref=f["asset_ref"],
                asset_type=f["asset_type"],
                location=f["location"],
                region=f["region"],
                capacity_tonnes=f["capacity_tonnes"],
                status=f["status"],
            ))

        # --- IoT Sensor Logs ---
        for entry in _load_seed("iot_logs.json"):
            for reading in entry["readings"]:
                temp = reading["temp_celsius"]
                is_excursion = temp < entry["safe_min"] or temp > entry["safe_max"]
                session.add(IotSensorLog(
                    shipment_id=entry["shipment_id"],
                    shipment_ref=entry["shipment_ref"],
                    cargo_type=entry["cargo_type"],
                    temp_celsius=temp,
                    safe_min=entry["safe_min"],
                    safe_max=entry["safe_max"],
                    recorded_at=_parse_dt(reading["recorded_at"]),
                    is_excursion=is_excursion,
                ))

        session.commit()
        logger.info("Seeded database at %s", DB_PATH)


def get_db():
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
