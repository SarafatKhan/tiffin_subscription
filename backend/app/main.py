from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import Base, engine
from app.models import (
    Customer,
    Subscription,
    Pause,
    Bill,
    Payment
)

from app.routes.customers import router as customer_router
from app.routes.subscriptions import router as subscription_router
from app.routes.billing import router as billing_router
from app.routes.payments import router as payment_router


app = FastAPI(
    title="Tiffin Subscription & Billing System",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

Base.metadata.create_all(
    bind=engine
)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

app.include_router(customer_router)
app.include_router(subscription_router)
app.include_router(billing_router)
app.include_router(payment_router)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

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