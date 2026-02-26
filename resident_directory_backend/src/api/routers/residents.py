from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.core.db import get_db
from src.api.deps.auth import require_admin
from src.api.schemas.resident import ResidentCreate, ResidentOut, ResidentUpdate
from src.api.services.residents import (
    ListResidentsRequest,
    create_resident_flow,
    delete_resident_flow,
    get_resident_flow,
    list_residents_flow,
    update_resident_flow,
)

router = APIRouter(prefix="/residents", tags=["residents"])


@router.get(
    "",
    response_model=list[ResidentOut],
    summary="List residents",
    description="Public endpoint to list residents, with optional search query and pagination.",
    operation_id="residents_list",
)
def list_residents(
    q: str | None = Query(None, description="Search term matched against name/address/email/phone"),
    limit: int = Query(50, ge=1, le=200, description="Max number of records to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
) -> list[ResidentOut]:
    req = ListResidentsRequest(q=q, limit=limit, offset=offset)
    return list_residents_flow(db, req)


@router.get(
    "/{resident_id}",
    response_model=ResidentOut,
    summary="Get resident",
    description="Public endpoint to fetch a resident by id.",
    operation_id="residents_get",
)
def get_resident(resident_id: int, db: Session = Depends(get_db)) -> ResidentOut:
    resident = get_resident_flow(db, resident_id)
    if not resident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resident not found.")
    return resident


@router.post(
    "",
    response_model=ResidentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create resident (admin)",
    description="Admin-only endpoint to create a resident.",
    operation_id="residents_create",
)
def create_resident(
    payload: ResidentCreate,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
) -> ResidentOut:
    return create_resident_flow(db, payload)


@router.patch(
    "/{resident_id}",
    response_model=ResidentOut,
    summary="Update resident (admin)",
    description="Admin-only endpoint to update (patch) an existing resident.",
    operation_id="residents_update",
)
def update_resident(
    resident_id: int,
    payload: ResidentUpdate,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
) -> ResidentOut:
    resident = get_resident_flow(db, resident_id)
    if not resident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resident not found.")
    return update_resident_flow(db, resident, payload)


@router.delete(
    "/{resident_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete resident (admin)",
    description="Admin-only endpoint to delete a resident.",
    operation_id="residents_delete",
)
def delete_resident(
    resident_id: int,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin),
) -> None:
    resident = get_resident_flow(db, resident_id)
    if not resident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resident not found.")
    delete_resident_flow(db, resident)
    return None
