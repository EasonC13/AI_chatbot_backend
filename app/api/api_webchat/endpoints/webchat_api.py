
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

from pkg.translate import translate
from aiohttp_requests import requests
from core.config import CH_GENERATE_API_URL
convert = {
    0: "其它",
    1: "喜歡",
    2: "悲傷",
    3: "噁心",
    4: "憤怒",
    5: "開心"
}

replace_map = {
    "&#39;": "'"
}
def transform(text):
    for key in replace_map:
        text = text.replace(key, replace_map[key])
    return text

@router.get("/generate_response")
async def generate_response(email, text:str = "How are you doing?", emotion: int = 1, response_count:int = 1):
    
    emotion = convert[emotion]
    translate_result = translate(text, "zh-tw")

    inputed_text = f"{translate_result['translatedText']}[{emotion}]"
    result = await requests.get(f"{CH_GENERATE_API_URL}/?input_text={inputed_text}&nsamples={response_count}")

    responses = await result.json()

    out_responses = []
    for response in responses:
        text = translate(response["candidate"], translate_result["detectedSourceLanguage"])
        text = text["translatedText"]
        text = transform(text)
        out_responses.append(text)

    return {"message": "success", "responses" : out_responses}
        