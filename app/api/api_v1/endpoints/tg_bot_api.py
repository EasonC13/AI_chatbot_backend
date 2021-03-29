
from fastapi import APIRouter
router = APIRouter()
from pkg.aio_telegram_utils import aio_get_profile_img_b64
from pkg.telegram_utils import get_bot_data_by_token, get_full_name_by_data
from db.mongodb import get_database
from core.config import DATABASE_NAME, COLLECTION_Bots

@router.get("/test")
async def test():
    print("HIHI")
    return "Hi Hi"


from pydantic import BaseModel, Field

class add_bot_format(BaseModel):
    creator: str = "example@gmail.com"
    bot_token: str = "1234567890:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    is_public: bool = False

from datetime import datetime

@router.post("/add_bot")
async def addNewBot(data: add_bot_format):
    bot_data = get_bot_data_by_token(data.bot_token)
    if bot_data == None:
        message = "Fail, Bot Not Found"
    else:
        out_data = {
        "Token": data.bot_token,
        "display_name": get_full_name_by_data(bot_data),
        "tg_username": f"@{bot_data['username']}",
        "Creator": data.creator,
        "Custom_Response": [], # S.M.A.R.T
        "is_public": data.is_public,
        "usage_count": 0,
        "is_reciever": False,
        "response_bots": [],
        "last_update": datetime.now(),
        "create_time": datetime.now(),
        "report_list": [],
        "profile_pic": await aio_get_profile_img_b64(f"@{bot_data['username']}")
        }
        db = await get_database()
        col = db[DATABASE_NAME][COLLECTION_Bots]

        #確認是不是已經有了
        already_have = await col.find_one({"Token": data.bot_token})
        if already_have:
            message = f"Fail, already have create by {already_have['Creator']} at {already_have['create_time']}"
        else:
            await col.insert_one(out_data)
            message = "Success, Add Success."
    return {"message": message}

##

from pkg.aio_telegram_utils import aio_get_profile_img_b64
from pkg.telegram_utils import get_bot_data_by_token

class post_token_format(BaseModel):
    bot_token: str = "1234567890:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


@router.post("/get_bot_data_by_token/")
async def api_get_bot_data_by_token(data: post_token_format):
    """Important data use post to transfer"""
    bot_data = get_bot_data_by_token(data.bot_token)
    bot_data["profile_pic"] = await aio_get_profile_img_b64("@"+bot_data["username"])
    return bot_data

@router.get("/get/avaliable_bots")
async def get_avaliable_bots(user_email):
    db = await get_database()
    col = db["AI_Chatbot_Platform"]["bots"]
    find_result = col.find({"$or":[{"is_public": True}, {"Creator": user_email}], "is_reciever": False},
                       {"_id": False,
                        "display_name": True,
                        "tg_username":True,
                        "Custom_Response": True,
                        "usage_count": True,
                        "create_time": True,
                        "last_update": True,
                        "profile_pic": True
                        })
    #先這樣 workaround，未來多頁面時要再改
    result = await find_result.to_list(200)
    return result

@router.get("/get/my_bots")
async def get_avaliable_bots(user_email):
    db = await get_database()
    col = db["AI_Chatbot_Platform"]["bots"]
    find_result = col.find({"Creator": user_email},
                       {"_id": False,
                        "display_name": True,
                        "tg_username":True,
                        "Custom_Response": True,
                        "is_public": True,
                        "usage_count": True,
                        "create_time": True,
                        "last_update": True,
                        "profile_pic": True,
                        "report_list": True,
                        })
    #先這樣 workaround，未來多頁面時要再改
    result = await find_result.to_list(200)
    return result

##


class receiver_set_format(BaseModel):
    user_email: str = "example@gmail.com"
    target_bot_username: str = "@Example_bot"
    response_bots_username: list = []
        
@router.post("/set/receiver")
async def receiver_set(data: receiver_set_format):
    """Example:
    {
  "user_email": "pricean01@gmail.com",
  "target_bot_username": "@NTNU_Demo_bot",
  "response_bots_username": ["@NTNU_2_bot","@NTNU_3_bot","@NTNU_4_bot","@NTNU_test_bot","@NTNU_Demo_bot"]
}"""
    
    db = await get_database()
    col = db["AI_Chatbot_Platform"]["bots"]
    
    target = await col.find_one({"tg_username": data.target_bot_username})
    if target["is_public"]:
        message = "fail, is_public = True, only able to use private bot as reciever."
    if target["Creator"] != data.user_email:
        message = "fail, you can't change other's bot."
    else:
        bots_token = []
        for username in data.response_bots_username:
            bot = await col.find_one({"tg_username": username})
            bots_token.append(bot["Token"])

        if len(bots_token) > 4:
            bots_token = bots_token[0:4]

        result = await col.update_one({"tg_username": data.target_bot_username, "Creator": data.user_email}, {"$set": {"response_bots": bots_token}})

        if result.modified_count:
            message = "success"
        else:
            message = "fail, no modified. unknown error when update. (might be same)"
        
    return {"message": message}