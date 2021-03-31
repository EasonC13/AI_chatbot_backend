
from fastapi import APIRouter
router = APIRouter()
from pkg.aio_telegram_utils import aio_get_profile_img_b64
from pkg.telegram_utils import get_bot_data_by_token, get_full_name_by_data
from db.mongodb import get_database
from core.config import ONLINE_DATABASE_NAME, COLLECTION_Bots

from datetime import datetime

@router.get("/get/avaliable_bot")
async def get_avaliable_bot(user_email:str = "example@gmail.com"):
    db = await get_database()
    col = db[ONLINE_DATABASE_NAME][COLLECTION_Bots]
    find_result = col.find({"$or":[{"is_public": True}, {"Creator": user_email}]},
                       {"_id": False,
                        "display_name": True,
                        "picture_url": True,
                        "create_time": True,
                        "last_update": True,
                        "usage_count": True,
                        "custom_response": True,
                        })
    #先這樣 workaround，未來多頁面時要再改
    result = await find_result.to_list(200)
    return result

from pydantic import BaseModel, Field

class add_bot_format(BaseModel):
    creator: str = "example@gmail.com"
    display_name: str = "Megumin"
    is_public: bool = True
    picture_url: str = "https://i.imgur.com/gyY9jPO.png"

@router.post("/add/newbot")
async def add_new_bot(data: add_bot_format):
    print(data)
    db = await get_database()
    col = db[ONLINE_DATABASE_NAME][COLLECTION_Bots]

    already_have = await col.find_one({
        "creator": data.creator,
        "display_name": data.display_name,
        "picture_url": data.picture_url
        })
    if already_have:
        message = f"Fail, already have create by {already_have['creator']} at {already_have['create_time']}"
    else:
        out_data = {
            "creator": data.creator,
            "display_name": data.display_name,
            "picture_url": data.picture_url,
            "create_time": datetime.now(),
            "last_update": datetime.now(),
            "is_public": data.is_public,
            "usage_count": 0,
            "report_list": [],
            "custom_response": [],
        }
        await col.insert_one(out_data)
        message = "Success, Add Success."
    return {"message": message}

@router.get("/get/chat-history")
async def chat_history(user_email:str = "example@gmail.com"):
    return await get_avaliable_bot(user_email)