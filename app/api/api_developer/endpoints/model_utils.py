
from fastapi import APIRouter
router = APIRouter()
from pkg.aio_telegram_utils import aio_get_profile_img_b64
from pkg.telegram_utils import get_bot_data_by_token, get_full_name_by_data
from db.mongodb import get_database
from core.config import DATABASE_NAME, COLLECTION_Bots
import re


from pkg.translate import translate
from pkg.text_process import transform, convert_emotion
from aiohttp_requests import requests
from core.config import CH_GENERATE_API_URLs



from pydantic import BaseModel, Field
from typing import Optional
import random

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

    
    

def deEmojify(responses):
    out = []
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    for text in responses:
        out.append(regrex_pattern.sub(r'',text))
    return out

def remove_punct(responses):
    out = []
    for text in responses:
        out.append(re.sub(r'[^\w\s]', ' ', text))
    return out

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
    for i in range(10):
        url = random.choice(CH_GENERATE_API_URLs)
        try:
            result = await requests.get(f"{url}/heartbeat", timeout=3)
            #print(f"Work: {result} {url}/generate-text/")
            break
        except Exception as e:
            import traceback
            import sys
            exc_type, exc_value, exc_tb = sys.exc_info()
            result = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            #print(f"Not Working: {''} {url}")
            continue
    result = await requests.get(f"{url}/generate-text/?input_text={inputed_text}&nsamples={data.response_count}")

    responses = await result.json()

    out_responses = []
    for response in responses:
        print(response)
        text = translate(response["candidate"], translate_result["detectedSourceLanguage"])
        text = text["translatedText"]
        text = transform(text)
        out_responses.append(text)
    
    if data.emoji == False:
        out_responses = deEmojify(out_responses)

    if data.punct == False:
        out_responses = remove_punct(out_responses)
    
    return {"message": "success", "responses" : out_responses}
        


@router.get("/middle-ware/generate-text")
async def generateText(input_text: str = "你好[喜歡]", nsamples: int = 1):
    result = await requests.get(f"{CH_GENERATE_API_URL}/?input_text={input_text}&nsamples={nsamples}")
    out =  await result.json()
    return out