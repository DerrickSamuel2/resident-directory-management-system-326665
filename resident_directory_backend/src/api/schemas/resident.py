from __future__ import annotations

from pydantic import BaseModel, Field


class ResidentBase(BaseModel):
    """Shared resident fields (matches DB schema)."""

    first_name: str = Field(..., description="Resident first name", min_length=1, max_length=120)
    last_name: str = Field(..., description="Resident last name", min_length=1, max_length=120)

    unit_number: str | None = Field(None, description="Unit / apartment number")

    address_line1: str | None = Field(None, description="Address line 1")
    address_line2: str | None = Field(None, description="Address line 2")
    city: str | None = Field(None, description="City")
    state: str | None = Field(None, description="State")
    postal_code: str | None = Field(None, description="Postal code")

    phone: str | None = Field(None, description="Phone number")
    email: str | None = Field(None, description="Email address")

    emergency_contact_name: str | None = Field(None, description="Emergency contact name")
    emergency_contact_phone: str | None = Field(None, description="Emergency contact phone")

    notes: str | None = Field(None, description="Additional notes")
    is_active: bool | None = Field(None, description="Whether the resident is active")


class ResidentCreate(ResidentBase):
    """Schema for creating a resident."""


class ResidentUpdate(BaseModel):
    """Schema for partial update of a resident."""

    first_name: str | None = Field(None, description="Resident first name", min_length=1, max_length=120)
    last_name: str | None = Field(None, description="Resident last name", min_length=1, max_length=120)

    unit_number: str | None = Field(None, description="Unit / apartment number")

    address_line1: str | None = Field(None, description="Address line 1")
    address_line2: str | None = Field(None, description="Address line 2")
    city: str | None = Field(None, description="City")
    state: str | None = Field(None, description="State")
    postal_code: str | None = Field(None, description="Postal code")

    phone: str | None = Field(None, description="Phone number")
    email: str | None = Field(None, description="Email address")

    emergency_contact_name: str | None = Field(None, description="Emergency contact name")
    emergency_contact_phone: str | None = Field(None, description="Emergency contact phone")

    notes: str | None = Field(None, description="Additional notes")
    is_active: bool | None = Field(None, description="Whether the resident is active")


class ResidentOut(ResidentBase):
    id: int = Field(..., description="Resident unique identifier")

    class Config:
        from_attributes = True
