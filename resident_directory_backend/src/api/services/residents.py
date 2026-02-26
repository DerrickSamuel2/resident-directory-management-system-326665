from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from src.api.models.resident import Resident
from src.api.schemas.resident import ResidentCreate, ResidentUpdate

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ListResidentsRequest:
    """Request object for listing/searching residents."""
    q: str | None
    limit: int
    offset: int


# PUBLIC_INTERFACE
def list_residents_flow(db: Session, req: ListResidentsRequest) -> list[Resident]:
    """
    Canonical flow for listing/searching residents.

    Contract:
      - q: if provided, performs a case-insensitive partial match on name/address/email/phone
      - limit/offset: pagination
      - returns: list of Resident ORM objects
    """
    logger.info("list_residents_flow start q=%s limit=%s offset=%s", req.q, req.limit, req.offset)

    stmt = select(Resident).order_by(Resident.last_name.asc(), Resident.first_name.asc())

    if req.q:
        like = f"%{req.q.strip()}%"
        stmt = stmt.where(
            or_(
                Resident.first_name.ilike(like),
                Resident.last_name.ilike(like),
                Resident.address.ilike(like),
                Resident.email.ilike(like),
                Resident.phone.ilike(like),
            )
        )

    stmt = stmt.limit(req.limit).offset(req.offset)
    residents = list(db.scalars(stmt).all())

    logger.info("list_residents_flow end count=%s", len(residents))
    return residents


# PUBLIC_INTERFACE
def get_resident_flow(db: Session, resident_id: int) -> Resident | None:
    """Get a single resident by id. Returns None if not found."""
    return db.get(Resident, resident_id)


# PUBLIC_INTERFACE
def create_resident_flow(db: Session, payload: ResidentCreate) -> Resident:
    """Create a resident record and return it."""
    resident = Resident(**payload.model_dump())
    db.add(resident)
    db.commit()
    db.refresh(resident)
    return resident


# PUBLIC_INTERFACE
def update_resident_flow(db: Session, resident: Resident, payload: ResidentUpdate) -> Resident:
    """Update a resident in-place using a patch payload."""
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(resident, k, v)
    db.add(resident)
    db.commit()
    db.refresh(resident)
    return resident


# PUBLIC_INTERFACE
def delete_resident_flow(db: Session, resident: Resident) -> None:
    """Delete a resident record."""
    db.delete(resident)
    db.commit()
