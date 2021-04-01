
from fastapi import APIRouter

from .endpoints.model_utils import router as model_utils_router

router = APIRouter()

router.include_router(model_utils_router)