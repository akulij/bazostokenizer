from fastapi import APIRouter
from pydantic import BaseModel

from .onlinesim import get_numbers_count

router = APIRouter()

class NumbersCount(BaseModel):
    count: int

@router.get("/numbers_count", response_model=NumbersCount)
async def numbers_count() -> NumbersCount:
    count = await get_numbers_count()
    return NumbersCount(count=count)
