# Update app/main.py

from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app.models import (
    Customer,
    Subscription,
    Pause,
    Bill,
    Payment
)
from app.routes.billing import router as billing_router
from app.routes.customers import router as customer_router
from app.routes.payments import router as payment_router
from app.routes.subscriptions import router as subscription_router


app = FastAPI(
    title="Tiffin Subscription & Billing System",
    version="1.0.0"
)


Base.metadata.create_all(
    bind=engine
)

app.include_router(customer_router)
app.include_router(subscription_router)
app.include_router(billing_router)
app.include_router(payment_router)


@app.get("/")
def root():
    return {
        "message": "Tiffin Management API is running"
    }


@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

    return {
        "database": "connected",
        "result": result.scalar()
    }
    