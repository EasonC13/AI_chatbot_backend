
from fastapi import APIRouter
router = APIRouter()
from pkg.aio_telegram_utils import aio_get_profile_img_b64
from pkg.telegram_utils import get_bot_data_by_token, get_full_name_by_data
from db.mongodb import get_database
from core.config import DATABASE_NAME, COLLECTION_Bots
import re

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


from pydantic import BaseModel, Field

class generate_response_format(BaseModel):
    email: str = "example@gmail.com"
    text:str = "How are you doing?"
    emotion: int = 1
    response_count:int = 1
    emoji: bool = True
    punct: bool = True # replace punct with space

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

@router.post("/generate_response")
async def generate_response(data: generate_response_format):
    """{
    0: "其它",
    1: "喜歡",
    2: "悲傷",
    3: "噁心",
    4: "憤怒",
    5: "開心"
}"""
    email = data.email
    emotion = convert[data.emotion]
    translate_result = translate(data.text, "zh-tw")

    #暫時避開簡體支援，因為容易跟 tw 搞混
    if translate_result["detectedSourceLanguage"] == "zh-CN":
        translate_result["detectedSourceLanguage"] = "zh-tw"

    inputed_text = f"{translate_result['translatedText']}[{emotion}]"
    result = await requests.get(f"{CH_GENERATE_API_URL}/?input_text={inputed_text}&nsamples={data.response_count}")

    responses = await result.json()

    out_responses = []
    for response in responses:
        text = translate(response["candidate"], translate_result["detectedSourceLanguage"])
        text = text["translatedText"]
        text = transform(text)
        out_responses.append(text)
    
    if data.emoji == False:
        out_responses = deEmojify(out_responses)

    if data.punct == False:
        out_responses = re.sub(r'[^\w\s]', ' ', out_responses)

    return {"message": "success", "responses" : out_responses}
        
