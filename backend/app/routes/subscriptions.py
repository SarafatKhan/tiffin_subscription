from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.pause import Pause
from app.models.subscription import Subscription
from app.schemas.pause import PauseCreate, PauseResponse
from app.schemas.subscription import (
	SubscriptionCreate,
	SubscriptionResponse,
	SubscriptionUpdate,
)
from app.services.pause_service import (
	pause_subscription,
	resume_subscription,
)


router = APIRouter(
	prefix="/api/subscriptions",
	tags=["Subscriptions"]
)


@router.post(
	"/",
	response_model=SubscriptionResponse,
	status_code=status.HTTP_201_CREATED
)
def create_subscription(
	subscription_data: SubscriptionCreate,
	db: Session = Depends(get_db)
):
	customer = db.get(
		Customer,
		subscription_data.customer_id
	)

	if not customer:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Customer not found"
		)

	if (
		subscription_data.end_date
		and subscription_data.end_date < subscription_data.start_date
	):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="End date cannot be before start date"
		)

	active_subscription = db.scalar(
		select(Subscription).where(
			Subscription.customer_id == subscription_data.customer_id,
			Subscription.status == "ACTIVE"
		)
	)

	if active_subscription:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Customer already has an active subscription"
		)

	subscription = Subscription(
		customer_id=subscription_data.customer_id,
		plan_name=subscription_data.plan_name,
		monthly_price=subscription_data.monthly_price,
		start_date=subscription_data.start_date,
		end_date=subscription_data.end_date,
		status="ACTIVE"
	)

	db.add(subscription)
	db.commit()
	db.refresh(subscription)

	return subscription


@router.get(
	"/",
	response_model=list[SubscriptionResponse]
)
def get_subscriptions(
	db: Session = Depends(get_db)
):
	subscriptions = db.scalars(
		select(Subscription).order_by(
			Subscription.id
		)
	).all()

	return subscriptions


@router.get(
	"/{subscription_id}",
	response_model=SubscriptionResponse
)
def get_subscription(
	subscription_id: int,
	db: Session = Depends(get_db)
):
	subscription = db.get(
		Subscription,
		subscription_id
	)

	if not subscription:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Subscription not found"
		)

	return subscription


@router.get(
	"/customer/{customer_id}",
	response_model=list[SubscriptionResponse]
)
def get_customer_subscriptions(
	customer_id: int,
	db: Session = Depends(get_db)
):
	customer = db.get(Customer, customer_id)

	if not customer:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Customer not found"
		)

	subscriptions = db.scalars(
		select(Subscription)
		.where(
			Subscription.customer_id == customer_id
		)
		.order_by(Subscription.id)
	).all()

	return subscriptions


@router.put(
	"/{subscription_id}",
	response_model=SubscriptionResponse
)
def update_subscription(
	subscription_id: int,
	subscription_data: SubscriptionUpdate,
	db: Session = Depends(get_db)
):
	subscription = db.get(
		Subscription,
		subscription_id
	)

	if not subscription:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Subscription not found"
		)

	update_data = subscription_data.model_dump(
		exclude_unset=True
	)

	new_start_date = subscription.start_date
	new_end_date = update_data.get(
		"end_date",
		subscription.end_date
	)

	if (
		new_end_date
		and new_end_date < new_start_date
	):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="End date cannot be before start date"
		)

	for field, value in update_data.items():
		setattr(subscription, field, value)

	db.commit()
	db.refresh(subscription)

	return subscription


@router.post(
	"/{subscription_id}/pause",
	response_model=PauseResponse,
	status_code=status.HTTP_201_CREATED
)
def pause(
	subscription_id: int,
	pause_data: PauseCreate,
	db: Session = Depends(get_db)
):
	subscription = db.get(
		Subscription,
		subscription_id
	)

	if not subscription:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Subscription not found"
		)

	return pause_subscription(
		db=db,
		subscription=subscription,
		start_date=pause_data.start_date,
		end_date=pause_data.end_date,
		reason=pause_data.reason
	)


@router.post(
	"/{subscription_id}/resume",
	response_model=SubscriptionResponse
)
def resume(
	subscription_id: int,
	db: Session = Depends(get_db)
):
	subscription = db.get(
		Subscription,
		subscription_id
	)

	if not subscription:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Subscription not found"
		)

	return resume_subscription(
		db=db,
		subscription=subscription
	)


@router.get(
	"/{subscription_id}/pauses",
	response_model=list[PauseResponse]
)
def get_pauses(
	subscription_id: int,
	db: Session = Depends(get_db)
):
	subscription = db.get(
		Subscription,
		subscription_id
	)

	if not subscription:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Subscription not found"
		)

	return db.scalars(
		select(Pause)
		.where(
			Pause.subscription_id == subscription_id
		)
		.order_by(Pause.start_date)
	).all()


@router.post(
	"/{subscription_id}/cancel",
	response_model=SubscriptionResponse
)
def cancel_subscription(
	subscription_id: int,
	db: Session = Depends(get_db)
):
	subscription = db.get(
		Subscription,
		subscription_id
	)

	if not subscription:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Subscription not found"
		)

	if subscription.status == "CANCELLED":
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Subscription is already cancelled"
		)

	subscription.status = "CANCELLED"

	db.commit()
	db.refresh(subscription)

	return subscription
