
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
from pkg.text_process import transform, convert_emotion
from aiohttp_requests import requests
from core.config import CH_GENERATE_API_URL



from pydantic import BaseModel, Field
from typing import Optional

class generate_response_format(BaseModel):
    email: str = "example@gmail.com"
    text:str = "How are you doing?"
    emotion: int = 1
    response_count: Optional[int] = 1
    emoji: Optional[bool] = True
    # replace punct with space
    punct: Optional[bool] = True
    # "": send back "..."(default, no further change), "random": "random new topic"
    default_response: Optional[str] = ""
    zh: Optional[str] = "zh-tw"
    response_language: Optional[str] = ""

from ...api_developer.endpoints.model_utils import deEmojify, remove_punct

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
    #return {"message": "success", "responses" : ["What about your good English?"]}
    email = data.email
    emotion = convert_emotion[data.emotion]
    translate_result = translate(data.text, "zh-tw")

    #暫時避開簡體支援，因為容易跟 tw 搞混
    if data.response_language != "":
        translate_result["detectedSourceLanguage"] = data.response_language
    elif "zh-" in translate_result["detectedSourceLanguage"]:
        translate_result["detectedSourceLanguage"] = data.zh

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
        out_responses = remove_punct(out_responses)
    
    return {"message": "success", "responses" : out_responses}
       