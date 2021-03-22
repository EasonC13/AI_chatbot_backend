from fastapi import APIRouter

from .endpoints.docs_auth import router as docs_auth_router

router = APIRouter()
router.include_router(docs_auth_router)