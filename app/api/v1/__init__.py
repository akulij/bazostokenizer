from fastapi import APIRouter

from . import info

router = APIRouter()

router.include_router(info.router)
