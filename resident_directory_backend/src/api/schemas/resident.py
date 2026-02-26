from __future__ import annotations

from pydantic import BaseModel, Field


class ResidentBase(BaseModel):
    first_name: str = Field(..., description="Resident first name", min_length=1, max_length=120)
    last_name: str = Field(..., description="Resident last name", min_length=1, max_length=120)

    address: str | None = Field(None, description="Street address")
    apartment: str | None = Field(None, description="Apartment/unit number")

    phone: str | None = Field(None, description="Phone number")
    email: str | None = Field(None, description="Email address")

    birth_date: str | None = Field(None, description="Birth date (free-form string for flexibility)")
    notes: str | None = Field(None, description="Additional notes")
    photo_url: str | None = Field(None, description="Public URL of resident photo")


class ResidentCreate(ResidentBase):
    """Schema for creating a resident."""


class ResidentUpdate(BaseModel):
    """Schema for partial update of a resident."""

    first_name: str | None = Field(None, description="Resident first name", min_length=1, max_length=120)
    last_name: str | None = Field(None, description="Resident last name", min_length=1, max_length=120)

    address: str | None = Field(None, description="Street address")
    apartment: str | None = Field(None, description="Apartment/unit number")

    phone: str | None = Field(None, description="Phone number")
    email: str | None = Field(None, description="Email address")

    birth_date: str | None = Field(None, description="Birth date (free-form string for flexibility)")
    notes: str | None = Field(None, description="Additional notes")
    photo_url: str | None = Field(None, description="Public URL of resident photo")


class ResidentOut(ResidentBase):
    id: int = Field(..., description="Resident unique identifier")

    class Config:
        from_attributes = True
