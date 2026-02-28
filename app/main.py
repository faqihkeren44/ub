from fastapi import FastAPI
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
    except:
        return {"status": "error", "database": "disconnected"}