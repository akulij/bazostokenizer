import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://127.0.0.1:8000/api/v1"

token = os.getenv("BOT_TOKEN") or "UNDEFINED"
print(token)

bot = Bot(token=token)
dp = Dispatcher(bot)
