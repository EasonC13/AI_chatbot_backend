
from fastapi import APIRouter

from .endpoints.tg_bot_api import router as tg_bot_api_router

router = APIRouter()

router.include_router(tg_bot_api_router)
