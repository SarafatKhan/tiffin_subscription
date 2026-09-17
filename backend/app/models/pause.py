from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Pause(Base):
	__tablename__ = "pauses"

	id: Mapped[int] = mapped_column(
		primary_key=True,
		index=True
	)

	subscription_id: Mapped[int] = mapped_column(
		ForeignKey("subscriptions.id"),
		nullable=False,
		index=True
	)

	start_date: Mapped[date] = mapped_column(
		Date,
		nullable=False
	)

	end_date: Mapped[date] = mapped_column(
		Date,
		nullable=False
	)

	reason: Mapped[str | None] = mapped_column(
		String(255),
		nullable=True
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		default=datetime.utcnow,
		nullable=False
	)

	subscription = relationship(
		"Subscription",
		back_populates="pauses"
	)
