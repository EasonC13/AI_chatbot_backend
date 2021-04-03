
from fastapi import APIRouter

from core.config import API_V1_STR, API_DEVELOPER_V1_STR, API_WEBCHAT_V1_STR

from .api_v1.api import router as api_v1_router
from .api_developer.api import router as api_developer_router
from .api_webchat.api import router as api_webchat_router

router = APIRouter()


router.include_router(api_v1_router, prefix=API_V1_STR, tags=["telegram"])
router.include_router(api_developer_router, prefix=API_DEVELOPER_V1_STR, tags=["developer"])
router.include_router(api_webchat_router, prefix=API_WEBCHAT_V1_STR, tags=["webchat"])

