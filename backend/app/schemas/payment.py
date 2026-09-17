from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    bill_id: int = Field(..., gt=0)

    amount: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2
    )

    payment_date: date = Field(
        default_factory=date.today
    )

    payment_method: str = Field(
        ...,
        min_length=2,
        max_length=30
    )

    transaction_reference: str | None = Field(
        default=None,
        max_length=100
    )


class PaymentResponse(BaseModel):
    id: int
    bill_id: int
    customer_id: int
    amount: Decimal
    payment_date: date
    payment_method: str
    transaction_reference: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
