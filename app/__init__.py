import asyncio
from fastapi import FastAPI

from app import api
from app.db import migrate, close_db_connection

app = FastAPI(title="Tokenizer API")

app.include_router(api.router, prefix="/api")

@app.on_event("startup")
async def run_migration():
    await migrate()

@app.on_event("shutdown")
async def close_db():
    await close_db_connection()
