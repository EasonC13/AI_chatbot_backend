from fastapi import APIRouter
router = APIRouter()

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

@router.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@router.get("/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title = "FastAPI", version="0.1.0", routes=router.routes)

# 現在是失敗的因為我沒辦法取得所有 App 的 routes
# 可能要透過 main 去取得吧？
# 所以這邊先放棄，因為也沒辦法用 HTTP Basic Auth