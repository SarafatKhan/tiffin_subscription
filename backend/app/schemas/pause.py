from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PauseCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str | None = Field(
        default=None,
        max_length=255
    )


class PauseResponse(BaseModel):
    id: int
    subscription_id: int
    start_date: date
    end_date: date
    reason: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
