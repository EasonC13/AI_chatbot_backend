from telegram import Bot
from telegram.error import InvalidToken

def get_bot_data_by_token(Token):
    try:  
        bot = Bot(Token)
        result = bot.get_me()
        return result.to_dict()
    except InvalidToken:
        return None