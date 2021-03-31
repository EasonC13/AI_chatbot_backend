
from fastapi import APIRouter

from .endpoints.webchat_api import router as webchat_api_router

router = APIRouter()

router.include_router(webchat_api_router)
