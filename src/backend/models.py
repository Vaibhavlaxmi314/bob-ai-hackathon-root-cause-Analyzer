from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class DisruptionEvent(Base):
    __tablename__ = "disruption_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)          # weather | port_strike | geopolitical
    region = Column(String, nullable=False)               # e.g. "Rotterdam", "South China Sea"
    severity = Column(Integer, nullable=False)            # 1-10
    description = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    estimated_end = Column(DateTime, nullable=True)


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_ref = Column(String, unique=True, nullable=False)  # e.g. "SHP-001"
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    cargo_type = Column(String, nullable=False)           # general | refrigerated | hazardous
    cargo_value_usd = Column(Float, nullable=False)
    priority = Column(String, default="normal")           # high | normal | low
    status = Column(String, default="in_transit")         # in_transit | delayed | delivered
    carrier = Column(String, nullable=False)
    eta = Column(DateTime, nullable=True)
    affected = Column(Boolean, default=False)
    impact_severity = Column(Integer, default=0)          # 0-10, set by shipment_impact tool
    disruption_id = Column(Integer, ForeignKey("disruption_events.id"), nullable=True)

    legs = relationship("ShipmentLeg", back_populates="shipment", cascade="all, delete-orphan")


class ShipmentLeg(Base):
    __tablename__ = "shipment_legs"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    leg_order = Column(Integer, nullable=False)           # 1, 2, 3…
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    via_region = Column(String, nullable=False)           # region used for disruption matching
    mode = Column(String, nullable=False)                 # truck | vessel | rail | air
    status = Column(String, default="pending")            # pending | active | completed | blocked

    shipment = relationship("Shipment", back_populates="legs")


class FleetAsset(Base):
    __tablename__ = "fleet_assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_ref = Column(String, unique=True, nullable=False)  # e.g. "TRUCK-007"
    asset_type = Column(String, nullable=False)           # truck | container | reefer | vessel
    location = Column(String, nullable=False)
    region = Column(String, nullable=False)
    capacity_tonnes = Column(Float, nullable=False)
    status = Column(String, default="idle")               # idle | in_use | maintenance
    last_updated = Column(DateTime, default=datetime.utcnow)


class IotSensorLog(Base):
    __tablename__ = "iot_sensor_logs"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    shipment_ref = Column(String, nullable=False)
    cargo_type = Column(String, nullable=False)
    temp_celsius = Column(Float, nullable=False)
    safe_min = Column(Float, nullable=False)              # cargo-type safe range min
    safe_max = Column(Float, nullable=False)              # cargo-type safe range max
    recorded_at = Column(DateTime, nullable=False)
    is_excursion = Column(Boolean, default=False)         # pre-computed for fast query
    severity = Column(String, nullable=True)              # minor | reportable | critical (set by cold_chain tool)
    action = Column(String, nullable=True)                # recommended action (set by cold_chain tool)
