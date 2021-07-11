# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

#from .api.api_v1.api import router as api_router
from core.config import ALLOWED_HOSTS, PROJECT_NAME, PROJECT_VERSION, API_PORT
from core.errors import http_422_error_handler, http_error_handler
from db.mongodb_connect import close_mongo_connection, connect_to_mongo
from db.mongodb import AsyncIOMotorClient, get_database
import asyncio


# %%
app = FastAPI(title=PROJECT_NAME, version = PROJECT_VERSION)

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)


# %%



# %%

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

@app.get("/api/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.get("/api/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title = app.title, version=app.version, routes=app.routes)


# %%
from api.api import router as api_router
app.include_router(api_router, prefix="/api")


# %%



# %%



# %%



# %%
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)


# %%



# %%
print("讚美神")


# %%



# %%



