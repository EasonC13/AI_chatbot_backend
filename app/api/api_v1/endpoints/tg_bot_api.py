
from fastapi import APIRouter
router = APIRouter()
from pkg.aio_telegram_utils import get_profile_img_b64
from pkg.telegram_utils import get_bot_data_by_token
from db.mongodb import get_database


@router.get("/test")
async def test():
    print("HIHI")
    return "Hi Hi"


from pydantic import BaseModel, Field

class add_bot_format(BaseModel):
    creator: str = "example@gmail.com"
    bot_token: str = "1234567890:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

from datetime import datetime

@router.post("/add_bot")
async def addNewBot(data: add_bot_format):
    bot_data = get_bot_data_by_token(data.bot_token)
    if bot_data == None:
        message = "Fail, Bot Not Found"
    else:
        out_data = {
        "Token": data.bot_token,
        "tg_username": f"@{bot_data['username']}",
        "Creator": data.creator,
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
        already_have = await col.find_one({"Token": data.bot_token})
        if already_have:
            message = f"Fail, already have create by {already_have['Creator']} at {already_have['create_time']}"
        else:
            await col.insert_one(out_data)
            message = "Success, Add Success."
    return {"message": message}