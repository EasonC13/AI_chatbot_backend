from telethon import TelegramClient, events, sync
from core.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, Operator_bot_Token
import uuid
import os
import base64
from asyncio import run as aio_run

random_id = str(uuid.uuid4())
client = TelegramClient(f'./tmp/aio_telegram_utils_{random_id}', TELEGRAM_API_ID, TELEGRAM_API_HASH)

#aio_run(client.start(bot_token=Operator_bot_Token))

async def connect_handler():
    if client.is_connected() == False:
        print("Start tg client")
        await client.start(bot_token=Operator_bot_Token)
        

async def aio_get_profile_img_b64(username):
    await connect_handler()
    filename = str(uuid.uuid4())
    filepath = f"./tmp/{filename}.png"
    result = await client.download_profile_photo(username, filepath)
    if result:
        png_encoded = base64.b64encode(open(filepath, "rb").read())
        os.remove(filepath)
        return png_encoded
    else:
        return None


