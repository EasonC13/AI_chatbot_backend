from telegram import Bot
from telegram.error import InvalidToken, Unauthorized
from core.config import Operator_bot_Token
import requests

def get_bot_data_by_token(Token):
    try:  
        bot = Bot(Token)
        result = bot.get_me()
        return result.to_dict()
    except (InvalidToken, Unauthorized) as e:
        return None

def get_full_name_by_data(bot_data):
    name = ""
    try:
        name += bot_data["first_name"]
    except:
        pass
    return name