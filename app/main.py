"""Main entry point for the LaporKita FastAPI application."""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.db.database import engine, Base

app = FastAPI(title="LaporKita", description="Sistem Otomatisasi Triase Keluhan Publik")

os.makedirs("app/static/js", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)