import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

API_V1_STR = "/v1"
API_WEBCHAT_V1_STR = "/webchat"
API_DEVELOPER_V1_STR = "/developer"

#JWT_TOKEN_PREFIX = "Token"
#ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
#SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "Accompany AI Chat")
PROJECT_VERSION = os.getenv("PROJECT_VERSION", "0.1.1")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", "*"))

API_PORT = 8080
API_HOST = "0.0.0.0"
API_WORKER = 5

DEBUG = False

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose


#chage to yours
MONGODB_PORT = 27017
MONGODB_HOST = "localhost"

MONGODB_USERNAME = os.getenv("USER", "user")
MONGODB_PASSWORD = os.getenv("MONGO_PASSWORD", f"mongo_{MONGODB_USERNAME}")

if not MONGODB_URL:
    MONGODB_URL = DatabaseURL(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}")
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)

DATABASE_NAME = "AI_Chatbot_Platform"
COLLECTION_Bots = "bots"

ONLINE_DATABASE_NAME = "AI_Chatbot_Online"

Operator_bot_Token = ""
TELEGRAM_API_ID = 0
TELEGRAM_API_HASH = ''

GOOGLE_APPLICATION_CREDENTIALS = ""
CH_GENERATE_API_URL = ""
