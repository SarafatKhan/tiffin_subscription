from app.models.customer import Customer


def test_create_customer(db):

    customer = Customer(
        name="Test Customer",
        phone="9876500002",
        email="test@example.com",
        address="Jaipur"
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    assert customer.id is not None
    assert customer.name == "Test Customer"
    assert customer.phone == "9876500002"


def test_customer_phone_unique(db):

    customer1 = Customer(
        name="Customer One",
        phone="9876500003"
    )

    db.add(customer1)
    db.commit()

    customer2 = Customer(
        name="Customer Two",
        phone="9876500003"
    )

    db.add(customer2)

    import pytest
    from sqlalchemy.exc import IntegrityError

    with pytest.raises(IntegrityError):
        db.commit()

    db.rollback()
