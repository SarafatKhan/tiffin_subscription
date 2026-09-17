from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.bill import Bill
from app.models.subscription import Subscription
from app.schemas.billing import (
	BillGenerateRequest,
	BillResponse,
)
from app.services.billing_service import (
	calculate_subscription_bill,
)


router = APIRouter(
	prefix="/api/billing",
	tags=["Billing"]
)


@router.post(
	"/generate",
	response_model=BillResponse,
	status_code=status.HTTP_201_CREATED
)
def generate_bill(
	bill_data: BillGenerateRequest,
	db: Session = Depends(get_db)
):
	if bill_data.month < 1 or bill_data.month > 12:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Month must be between 1 and 12"
		)

	if bill_data.year < 2000:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid billing year"
		)

	subscription = db.get(
		Subscription,
		bill_data.subscription_id
	)

	if not subscription:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Subscription not found"
		)

	billing_month = date(
		bill_data.year,
		bill_data.month,
		1
	)

	existing_bill = db.scalar(
		select(Bill).where(
			Bill.subscription_id == subscription.id,
			Bill.billing_month == billing_month
		)
	)

	if existing_bill:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Bill already exists for this subscription and month"
		)

	calculation = calculate_subscription_bill(
		db=db,
		subscription=subscription,
		year=bill_data.year,
		month=bill_data.month
	)

	bill = Bill(
		customer_id=subscription.customer_id,
		subscription_id=subscription.id,
		billing_month=billing_month,
		eligible_days=calculation["eligible_days"],
		paused_days=calculation["paused_days"],
		billable_days=calculation["billable_days"],
		monthly_price=calculation["monthly_price"],
		daily_rate=calculation["daily_rate"],
		amount=calculation["amount"],
		status="PENDING",
		due_date=bill_data.due_date
	)

	db.add(bill)
	db.commit()
	db.refresh(bill)

	return bill


@router.get(
	"/",
	response_model=list[BillResponse]
)
def get_bills(
	db: Session = Depends(get_db)
):
	return db.scalars(
		select(Bill).order_by(
			Bill.billing_month.desc(),
			Bill.id.desc()
		)
	).all()


@router.get(
	"/{bill_id}",
	response_model=BillResponse
)
def get_bill(
	bill_id: int,
	db: Session = Depends(get_db)
):
	bill = db.get(Bill, bill_id)

	if not bill:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Bill not found"
		)

	return bill


@router.get(
	"/customer/{customer_id}",
	response_model=list[BillResponse]
)
def get_customer_bills(
	customer_id: int,
	db: Session = Depends(get_db)
):
	bills = db.scalars(
		select(Bill)
		.where(
			Bill.customer_id == customer_id
		)
		.order_by(
			Bill.billing_month.desc()
		)
	).all()

	return bills
