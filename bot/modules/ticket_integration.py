import re
import json
from aiogram import types
from aiogram.dispatcher import filters
from aiohttp import ClientSession

from config import dp, API_BASE
from modules.types import Ticket
from modules import db

@dp.message_handler(regexp=r"(\d+)(\W\w+)*")
async def start(message: types.Message):
    print("TI")
    groups = re.match(r"(\d+)(\W\w+)*", message.text)

    count: int = int(groups[1])
    caption: str = groups[2] if groups[2] else ""

    # max_numbers_balance = get_possible_balance_numbers()
    # max_aviable_tokens = get_aviable_tokens()
    # if count > min(max_aviable_numbers, max_numbers_balance):
    #     await message.answer("Слишком большое число токенов! Или недостаточно номеров на сервисе, ил нужно пополнить баланс!")
    #     return

    data = {
            "telegram_account": message.from_user.id,
            "numbers_count": int(count),
            "caption": caption.strip(),
            }
    # data = {
    #         "telegram_account": 0,
    #         "numbers_count": 0,
    #         "caption": "string"
    #         }

    prox = bytes(json.dumps(data), "UTF-8")
    print(prox)
    headers = {
            "Content-Type": "application/json"
            }

    async with ClientSession() as session:
        async with session.post(f"{API_BASE}/proceed", data=prox, headers=headers) as response:
            # print(await response.text())
            ticket_obj: dict = await response.json()
            print(ticket_obj)
            ticket = Ticket.parse_obj(ticket_obj)

    await message.answer(ticket.msg)
