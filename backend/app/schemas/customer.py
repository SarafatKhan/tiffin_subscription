"""Customer request and response schemas."""
# app/schemas/customer.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CustomerBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15
    )

    email: str | None = Field(
        default=None,
        max_length=100
    )

    address: str | None = Field(
        default=None,
        max_length=255
    )


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    email: str | None = Field(
        default=None,
        max_length=100
    )

    address: str | None = Field(
        default=None,
        max_length=255
    )


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)