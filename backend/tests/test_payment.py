from datetime import date
from decimal import Decimal

from app.models.customer import Customer
from app.models.subscription import Subscription
from app.models.bill import Bill
from app.models.payment import Payment


def create_bill(db):

    customer = Customer(
        name="Payment User",
        phone="9876500001"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    subscription = Subscription(
        customer_id=customer.id,
        plan_name="Lunch Plan",
        monthly_price=3000,
        start_date=date(2026, 9, 1),
        end_date=None,
        status="ACTIVE"
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    bill = Bill(
        customer_id=customer.id,
        subscription_id=subscription.id,
        billing_month=date(2026, 9, 1),
        eligible_days=22,
        paused_days=5,
        billable_days=17,
        monthly_price=Decimal("3000.00"),
        daily_rate=Decimal("136.36"),
        amount=Decimal("2318.18"),
        status="PENDING"
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)

    return bill


def test_partial_payment(db):

    bill = create_bill(db)

    payment = Payment(
        bill_id=bill.id,
        customer_id=bill.customer_id,
        amount=Decimal("1000.00"),
        payment_date=date(2026, 9, 30),
        payment_method="UPI",
        status="COMPLETED"
    )

    db.add(payment)
    db.commit()

    total_paid = sum(
        p.amount
        for p in bill.payments
    )

    assert total_paid == Decimal("1000.00")


def test_full_payment(db):

    bill = create_bill(db)

    payment = Payment(
        bill_id=bill.id,
        customer_id=bill.customer_id,
        amount=Decimal("2318.18"),
        payment_date=date(2026, 9, 30),
        payment_method="CASH",
        status="COMPLETED"
    )

    db.add(payment)

    bill.status = "PAID"

    db.commit()

    assert bill.status == "PAID"
