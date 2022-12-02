from fastapi import APIRouter

from . import (
        info,
        interactor,
        )

router = APIRouter()

router.include_router(info.router)
router.include_router(interactor.router)
