from aiogram import types

from config import dp
from modules.types import User
from modules import db

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user = User(id=message.from_user.id)
    await db.new_user(user)

    await message.answer("Использование: {count} {caption}")
