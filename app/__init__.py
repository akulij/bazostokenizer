import asyncio
from fastapi import FastAPI

from app import api
from app.db import migrate

app = FastAPI()

app.include_router(api.router, prefix="/api")

@app.on_event("startup")
async def run_migration():
    await migrate()
