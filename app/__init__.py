from fastapi import FastAPI

import app.api

app = FastAPI()

app.include_router(api.router, prefix="/api")
