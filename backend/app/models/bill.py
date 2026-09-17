from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Bill(Base):
	__tablename__ = "bills"

	id: Mapped[int] = mapped_column(
		primary_key=True,
		index=True
	)

	customer_id: Mapped[int] = mapped_column(
		ForeignKey("customers.id"),
		nullable=False,
		index=True
	)

	subscription_id: Mapped[int] = mapped_column(
		ForeignKey("subscriptions.id"),
		nullable=False,
		index=True
	)

	billing_month: Mapped[date] = mapped_column(
		Date,
		nullable=False,
		index=True
	)

	eligible_days: Mapped[int] = mapped_column(
		Integer,
		nullable=False
	)

	paused_days: Mapped[int] = mapped_column(
		Integer,
		nullable=False
	)

	billable_days: Mapped[int] = mapped_column(
		Integer,
		nullable=False
	)

	monthly_price: Mapped[Decimal] = mapped_column(
		Numeric(10, 2),
		nullable=False
	)

	daily_rate: Mapped[Decimal] = mapped_column(
		Numeric(10, 2),
		nullable=False
	)

	amount: Mapped[Decimal] = mapped_column(
		Numeric(10, 2),
		nullable=False
	)

	status: Mapped[str] = mapped_column(
		String(20),
		nullable=False,
		default="PENDING",
		index=True
	)

	generated_at: Mapped[datetime] = mapped_column(
		DateTime,
		default=datetime.utcnow,
		nullable=False
	)

	due_date: Mapped[date | None] = mapped_column(
		Date,
		nullable=True
	)

	customer = relationship(
		"Customer"
	)

	subscription = relationship(
		"Subscription"
	)

	payments = relationship(
		"Payment",
		back_populates="bill",
		cascade="all, delete-orphan"
	)
