# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

#from .api.api_v1.api import router as api_router
from core.config import ALLOWED_HOSTS, PROJECT_NAME, API_PORT, API_V1_STR
from core.errors import http_422_error_handler, http_error_handler
from db.mongodb_connect import close_mongo_connection, connect_to_mongo
from db.mongodb import AsyncIOMotorClient, get_database
import asyncio


# %%
from pkg.aio_telegram_utils import get_profile_img_b64
from pkg.telegram_utils import get_bot_data_by_token


# %%



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
app.include_router(api_v1_router, prefix=API_V1_STR)


# %%



# %%
from fastapi.responses import HTMLResponse
@app.get("/")
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


# %% [markdown]
# from telegram import Bot
# from telegram.error import InvalidToken
# def get_bot_data_by_token(Token):
#     try:  
#         bot = Bot(Token)
#         result = bot.get_me()
#         return result.to_dict()
#     except InvalidToken:
#         return None

# %%
from datetime import datetime
async def addNewBot(creator, bot_token):
    bot_data = get_bot_data_by_token(bot_token)
    if bot_data == None:
        message = "Fail, Bot Not Found"
    else:
        data = {
        "Token": bot_token,
        "tg_username": f"@{bot_data['username']}",
        "Creator": creator,
        "Custom_Response": [], # S.M.A.R.T
        "is_public": False,
        "usage_count": 0,
        "is_reciever": True,
        "response_bots": [],
        "last_update": datetime.now(),
        "create_time": datetime.now(),
        "report_list": [],
        }
        db = await get_database()
        col = db["AI_Chatbot_Platform"]["bots"]

        #確認是不是已經有了
        already_have = await col.find_one({"Token": bot_token})
        if already_have:
            message = f"Fail, already have create by {already_have['Creator']} at {already_have['create_time']}"
        else:
            await col.insert_one(data)
            message = "Success, Add Success."
        return {"message": message}


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



