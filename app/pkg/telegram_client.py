# This is a fail test.


# from telethon import TelegramClient, events, sync
# from core.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, Operator_bot_Token
# import uuid
# import logging

# class TG_Client:
#     client = None


# tg_client = TG_Client()


# async def get_tg_client():
#     return tg_client.client



# async def connect_to_tg_client():
    
#     logging.info("Connecting to Telegram Client...")
#     tg_client.client = TelegramClient(f'./tmp/{str(uuid.uuid4())}', TELEGRAM_API_ID, TELEGRAM_API_HASH)
#     print("Connecting to Telegram Client...")
#     logging.info("Connecting to Telegram Client.")


# async def close_tg_client_connection():
#     logging.info("Closing Connection from Telegram Client...")
#     print("Connecting to Telegram Client...")
#     tg_client.client.close()
#     logging.info("Closing Connection from Telegram Client Success.")