from fastapi import FastAPI
from app.api import vendors

app = FastAPI(title="AEDWAP")
app.include_router(vendors.router)

@app.get("/")
def root():
    return {"status": "ok"}