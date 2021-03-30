
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
        "is_receiver": False,
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

@router.get("/get/myChats")
async def get_my_chats(user_email):
    db = await get_database()
    col = db["AI_Chatbot_Platform"]["bots"]
    receiver_bot = await col.find_one({"Creator": user_email, "is_receiver": True},
                       {"_id": False,
                        "display_name": True,
                        "tg_username":True,
                        "Custom_Response": True,
                        "usage_count": True,
                        "create_time": True,
                        "last_update": True,
                        "profile_pic": True,
                        "response_bots": True
                        })
    if receiver_bot:
        filter = []
        for token in receiver_bot["response_bots"]:
            filter.append({"Token": token})

        find_result = col.find({"$or":filter},
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
        other_bots = await find_result.to_list(200)
        del receiver_bot["response_bots"]
        message = "success"
    else:
        other_bots = []
        message = "fail, not found a receiver bot."
    
    #先這樣 workaround，未來多個機器人時要再改
    return {"message": message, "receivers": [
        {
            "receiver_bot": receiver_bot,
            "other_bots": other_bots
    }]}


@router.get("/get/avaliable_bots")
async def get_avaliable_bots(user_email):
    db = await get_database()
    col = db["AI_Chatbot_Platform"]["bots"]
    find_result = col.find({"$or":[{"is_public": True}, {"Creator": user_email}], "is_receiver": False},
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
async def get_my_bots(user_email):
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
    if target == None:
        message = "Bot Not Found."
    elif target["Creator"] != data.user_email:
        message = "fail, you can't change other's bot."
    elif target["is_public"]:
        message = "fail, is_public = True, only able to use private bot as receiver."
    else:
        bots_token = []
        for username in data.response_bots_username:
            bot = await col.find_one({"tg_username": username})
            bots_token.append(bot["Token"])

        result = await col.update_one({"tg_username": data.target_bot_username, "Creator": data.user_email}, {"$set": {"response_bots": bots_token, "is_receiver": True}})

        if result.modified_count:
            #Webhook target["Token"]
            message = "success"
        else:
            message = "fail, no modified. unknown error when update. (might be same)"
        
    return {"message": message}

class receiver_remove_format(BaseModel):
    user_email: str = "example@gmail.com"
    target_bot_username: str = "@Example_bot"

@router.post("/remove/receiver")
async def receiver_remove(data: receiver_remove_format):
    """Example:
    {
  "user_email": "pricean01@gmail.com",
  "target_bot_username": "@NTNU_Demo_bot"
}"""
    
    db = await get_database()
    col = db["AI_Chatbot_Platform"]["bots"]
    
    target = await col.find_one({"tg_username": data.target_bot_username})
    if target == None:
        message = "Bot Not Found."
    elif target["Creator"] != data.user_email:
        message = "fail, you can't change other's bot."
    elif target["is_public"]:
        message = "fail, is_public = True, only able to use private bot as receiver."
    elif target["is_receiver"]:
        message = "fail, you can't change while it's receiver. Remove receiver first."
    else:
        result = await col.update_one({"tg_username": data.target_bot_username, "Creator": data.user_email},
         {"$set": {"response_bots": [], "is_receiever": False}})
        if result.modified_count:
            #Webhook Remove target["Token"]
            message = "success"
        else:
            message = "fail, no modified. unknown error when update. (might be same)"
    return {"message": message}


class bot_change_public_format(BaseModel):
    user_email: str = "example@gmail.com"
    target_bot_username: str = "@Example_bot"
    is_public: bool = True

@router.post("/bot/change_public")
async def bot_change_public(data: bot_change_public_format):
    db = await get_database()
    col = db["AI_Chatbot_Platform"]["bots"]
    
    target = await col.find_one({"tg_username": data.target_bot_username})
    if target == None:
        message = "Bot Not Found."
    elif target["Creator"] != data.user_email:
        message = "fail, you can't change other's bot."
    else:
        result = await col.update_one({"tg_username": data.target_bot_username, "Creator": data.user_email},
         {"$set": {"is_public": data.is_public}})
        if result.modified_count:
            message = "success"
        else:
            message = "fail, no modified. unknown error when update. (might be same)"
    return {"message": message}