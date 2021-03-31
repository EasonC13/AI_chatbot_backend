
from fastapi import APIRouter

from .endpoints.webchat_api import router as webchat_api_router
from .endpoints.webchat_management import router as webchat_manage_api_router

router = APIRouter()

router.include_router(webchat_api_router)
router.include_router(webchat_manage_api_router)
