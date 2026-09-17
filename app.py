from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine


app = FastAPI(
    title="Tiffin Management System",
    description="Subscription and pro-rated billing system for tiffin services",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Tiffin Management System API is running"
    }


@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar()
    }