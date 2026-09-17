from datetime import date

import pytest
from fastapi import HTTPException

from app.models.customer import Customer
from app.models.subscription import Subscription
from app.services.pause_service import (
    validate_pause_dates,
    check_pause_overlap
)


def create_subscription(db):

    customer = Customer(
        name="Test User",
        phone="9876500000"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    subscription = Subscription(
        customer_id=customer.id,
        plan_name="Lunch Plan",
        monthly_price=3000,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 30),
        status="ACTIVE"
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


def test_invalid_pause_dates(db):

    subscription = create_subscription(db)

    with pytest.raises(HTTPException):

        validate_pause_dates(
            subscription,
            date(2026, 9, 15),
            date(2026, 9, 10)
        )


def test_pause_before_subscription(db):

    subscription = create_subscription(db)

    with pytest.raises(HTTPException):

        validate_pause_dates(
            subscription,
            date(2026, 8, 25),
            date(2026, 9, 5)
        )


def test_pause_after_subscription(db):

    subscription = create_subscription(db)

    with pytest.raises(HTTPException):

        validate_pause_dates(
            subscription,
            date(2026, 9, 25),
            date(2026, 10, 5)
        )


def test_overlapping_pause(db):

    subscription = create_subscription(db)

    from app.models.pause import Pause

    pause = Pause(
        subscription_id=subscription.id,
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 15),
        reason="Travel"
    )

    db.add(pause)
    db.commit()

    with pytest.raises(HTTPException):

        check_pause_overlap(
            db,
            subscription.id,
            date(2026, 9, 12),
            date(2026, 9, 18)
        )
