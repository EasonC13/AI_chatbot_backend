# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

#from .api.api_v1.api import router as api_router
from core.config import ALLOWED_HOSTS, PROJECT_NAME, API_PORT, API_V1_STR
from core.errors import http_422_error_handler, http_error_handler
from db.mongodb_connect import close_mongo_connection, connect_to_mongo
from db.mongodb import AsyncIOMotorClient, get_database
import asyncio


# %%
app = FastAPI(title=PROJECT_NAME)

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

from api.api_v1.api import router as api_v1_router
from api.api_webchat.api import router as api_webchat_router
#app.include_router(api_v1_router, prefix=API_V1_STR)
app.include_router(api_webchat_router, prefix="/api/webchat")


# %%



# %%



# %%
from fastapi.responses import HTMLResponse
@app.get("/")
def home():
    with open(f"{static_file_path}/index.html") as f:
        html = "".join(f.readlines())
    return HTMLResponse(content=html, status_code= 200)

@app.get("/home")
def home():
    with open(f"{static_file_path}/index.html") as f:
        html = "".join(f.readlines())
    return HTMLResponse(content=html, status_code= 200)


# %%
@app.get("/index2")
def fun():
    with open("./static/index2.html") as f:
        html = "".join(f.readlines())
    return HTMLResponse(content=html, status_code= 200)


# %%



# %%



# %%



# %%
static_file_path = "../front-end/dist"
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory=static_file_path), name="static")


# %%
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)


# %%



# %%


# %% [markdown]
# @app.post("/request_phone_code", tags=["user"])
# def request_phone_code():
#     pass
# 
# @app.post("/help_add_bot", tags=["user"])
# def request_phone_code():
#     pass
# %% [markdown]
# @app.get("/")
# def index_page():
#     pass

# %%



# %%
print("讚美主")


