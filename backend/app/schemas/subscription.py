from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class SubscriptionCreate(BaseModel):
	customer_id: int = Field(..., gt=0)

	plan_name: str = Field(
		...,
		min_length=2,
		max_length=100
	)

	monthly_price: float = Field(
		...,
		gt=0
	)

	start_date: date

	end_date: date | None = None


class SubscriptionUpdate(BaseModel):
	plan_name: str | None = Field(
		default=None,
		min_length=2,
		max_length=100
	)

	monthly_price: float | None = Field(
		default=None,
		gt=0
	)

	end_date: date | None = None


class SubscriptionResponse(BaseModel):
	id: int
	customer_id: int
	plan_name: str
	monthly_price: float
	start_date: date
	end_date: date | None
	status: str
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(
		from_attributes=True
	)
