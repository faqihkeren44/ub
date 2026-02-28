from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, Base
from app import models

app = FastAPI ()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}