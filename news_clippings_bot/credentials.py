import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN_ENV = os.getenv('BOT_TOKEN')
APP_NAME_ENV = os.getenv('APP_NAME')

BOT_TOKEN = BOT_TOKEN_ENV
APP_NAME = APP_NAME_ENV
