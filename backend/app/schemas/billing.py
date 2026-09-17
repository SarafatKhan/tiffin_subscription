from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BillGenerateRequest(BaseModel):
	subscription_id: int
	year: int
	month: int
	due_date: date | None = None


class BillResponse(BaseModel):
	id: int
	customer_id: int
	subscription_id: int
	billing_month: date
	eligible_days: int
	paused_days: int
	billable_days: int
	monthly_price: Decimal
	daily_rate: Decimal
	amount: Decimal
	status: str
	generated_at: datetime
	due_date: date | None

	model_config = ConfigDict(
		from_attributes=True
	)
