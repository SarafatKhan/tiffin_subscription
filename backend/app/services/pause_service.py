from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pause import Pause
from app.models.subscription import Subscription


def validate_pause_dates(
	subscription: Subscription,
	start_date: date,
	end_date: date
):
	if start_date > end_date:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Pause start date cannot be after end date"
		)

	if start_date < subscription.start_date:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Pause cannot start before subscription start date"
		)

	if (
		subscription.end_date
		and end_date > subscription.end_date
	):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Pause cannot end after subscription end date"
		)


def check_pause_overlap(
	db: Session,
	subscription_id: int,
	start_date: date,
	end_date: date
):
	overlapping_pause = db.scalar(
		select(Pause).where(
			Pause.subscription_id == subscription_id,
			Pause.start_date <= end_date,
			Pause.end_date >= start_date
		)
	)

	if overlapping_pause:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Pause period overlaps with an existing pause"
		)


def pause_subscription(
	db: Session,
	subscription: Subscription,
	start_date: date,
	end_date: date,
	reason: str | None = None
):
	if subscription.status != "ACTIVE":
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Only an active subscription can be paused"
		)

	validate_pause_dates(
		subscription,
		start_date,
		end_date
	)

	check_pause_overlap(
		db,
		subscription.id,
		start_date,
		end_date
	)

	pause = Pause(
		subscription_id=subscription.id,
		start_date=start_date,
		end_date=end_date,
		reason=reason
	)

	db.add(pause)

	subscription.status = "PAUSED"

	db.commit()
	db.refresh(pause)

	return pause


def resume_subscription(
	db: Session,
	subscription: Subscription
):
	if subscription.status != "PAUSED":
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Only a paused subscription can be resumed"
		)

	subscription.status = "ACTIVE"

	db.commit()
	db.refresh(subscription)

	return subscription
