from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.bill import Bill
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse


router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"]
)


def get_completed_payment_total(
    db: Session,
    bill_id: int
) -> Decimal:

    total = db.scalar(
        select(
            func.coalesce(
                func.sum(Payment.amount),
                0
            )
        ).where(
            Payment.bill_id == bill_id,
            Payment.status == "COMPLETED"
        )
    )

    return Decimal(str(total or 0))


def update_bill_status(
    db: Session,
    bill: Bill
):

    total_paid = get_completed_payment_total(
        db,
        bill.id
    )

    bill_amount = Decimal(str(bill.amount))

    if total_paid >= bill_amount:
        bill.status = "PAID"

    elif total_paid > Decimal("0.00"):
        bill.status = "PARTIALLY_PAID"

    else:
        bill.status = "PENDING"


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):

    bill = db.get(
        Bill,
        payment_data.bill_id
    )

    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    if bill.status == "PAID":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bill is already fully paid"
        )

    if bill.status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot make payment for a cancelled bill"
        )

    total_paid = get_completed_payment_total(
        db,
        bill.id
    )

    bill_amount = Decimal(str(bill.amount))

    outstanding_amount = (
        bill_amount - total_paid
    )

    if payment_data.amount > outstanding_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Payment exceeds outstanding amount",
                "bill_amount": bill_amount,
                "already_paid": total_paid,
                "outstanding_amount": outstanding_amount
            }
        )

    payment = Payment(
        bill_id=bill.id,
        customer_id=bill.customer_id,
        amount=payment_data.amount,
        payment_date=payment_data.payment_date,
        payment_method=payment_data.payment_method,
        transaction_reference=payment_data.transaction_reference,
        status="COMPLETED"
    )

    db.add(payment)
    db.flush()

    update_bill_status(
        db,
        bill
    )

    db.commit()
    db.refresh(payment)

    return payment


@router.get(
    "/bill/{bill_id}",
    response_model=list[PaymentResponse]
)
def get_bill_payments(
    bill_id: int,
    db: Session = Depends(get_db)
):

    bill = db.get(
        Bill,
        bill_id
    )

    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    payments = db.scalars(
        select(Payment)
        .where(Payment.bill_id == bill_id)
        .order_by(Payment.payment_date.desc())
    ).all()

    return payments


@router.get(
    "/customer/{customer_id}",
    response_model=list[PaymentResponse]
)
def get_customer_payments(
    customer_id: int,
    db: Session = Depends(get_db)
):

    payments = db.scalars(
        select(Payment)
        .where(Payment.customer_id == customer_id)
        .order_by(Payment.payment_date.desc())
    ).all()

    return payments


@router.get(
    "/",
    response_model=list[PaymentResponse]
)
def get_payments(
    db: Session = Depends(get_db)
):

    payments = db.scalars(
        select(Payment)
        .order_by(Payment.created_at.desc())
    ).all()

    return payments


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = db.get(
        Payment,
        payment_id
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment
