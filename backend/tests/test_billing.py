from datetime import date
from decimal import Decimal

from app.models.customer import Customer
from app.models.subscription import Subscription
from app.models.pause import Pause
from app.services.billing_service import calculate_subscription_bill


def test_full_month_without_pause(db):

    customer = Customer(
        name="Rahul",
        phone="9876543210"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    subscription = Subscription(
        customer_id=customer.id,
        plan_name="Monthly Lunch",
        monthly_price=3000,
        start_date=date(2026, 9, 1),
        end_date=None,
        status="ACTIVE"
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    result = calculate_subscription_bill(
        db,
        subscription,
        2026,
        9
    )

    assert result["eligible_days"] == 22
    assert result["paused_days"] == 0
    assert result["billable_days"] == 22
    assert result["amount"] == Decimal("3000.00")


def test_bill_with_pause(db):

    customer = Customer(
        name="Amit",
        phone="9876543211"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    subscription = Subscription(
        customer_id=customer.id,
        plan_name="Monthly Lunch",
        monthly_price=3000,
        start_date=date(2026, 9, 1),
        end_date=None,
        status="PAUSED"
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    pause = Pause(
        subscription_id=subscription.id,
        start_date=date(2026, 9, 8),
        end_date=date(2026, 9, 12),
        reason="Travel"
    )

    db.add(pause)
    db.commit()

    result = calculate_subscription_bill(
        db,
        subscription,
        2026,
        9
    )

    assert result["eligible_days"] == 22
    assert result["paused_days"] == 5
    assert result["billable_days"] == 17
    assert result["amount"] == Decimal("2318.18")


def test_subscription_start_mid_month(db):

    customer = Customer(
        name="Rohit",
        phone="9876543212"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    subscription = Subscription(
        customer_id=customer.id,
        plan_name="Monthly Lunch",
        monthly_price=3000,
        start_date=date(2026, 9, 15),
        end_date=None,
        status="ACTIVE"
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    result = calculate_subscription_bill(
        db,
        subscription,
        2026,
        9
    )

    assert result["eligible_days"] == 12
    assert result["paused_days"] == 0
    assert result["billable_days"] == 12
    assert result["amount"] == Decimal("3000.00")


def test_subscription_ended_mid_month(db):

    customer = Customer(
        name="Vikas",
        phone="9876543213"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    subscription = Subscription(
        customer_id=customer.id,
        plan_name="Monthly Lunch",
        monthly_price=3000,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 15),
        status="CANCELLED"
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    result = calculate_subscription_bill(
        db,
        subscription,
        2026,
        9
    )

    assert result["eligible_days"] == 11
    assert result["paused_days"] == 0
    assert result["billable_days"] == 11
    assert result["amount"] == Decimal("3000.00")
