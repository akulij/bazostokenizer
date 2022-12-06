import io
import asyncio

from aiohttp import ClientSession
from aiogram.types import InputFile

from config import bot, API_BASE
from modules.types import TicketData

async def get_tickets(done: bool = None):
    params = {}
    if type(done) == bool:
        params["done"] = int(done)

    async with ClientSession() as session:
        async with session.get(f"{API_BASE}/tickets", params=params) as response:
            data: list[dict] = await response.json()

    tickets = [TicketData.parse_obj(t) for t in data]

    return tickets

async def get_tokens(process_id: int) -> str:
    params = {
            "process_id": process_id,
            }

    async with ClientSession() as session:
        async with session.get(f"{API_BASE}/tokens", params=params) as response:
            data: str = await response.text()

    return data

async def drop_ticket(process_id: int):
    params = {
            "process_id": process_id,
            }

    async with ClientSession() as session:
        async with session.get(f"{API_BASE}/dropticket", params=params) as response:
            data = await response.text()
            status = response.status

    return status == 200

async def main():
    while True:
        tickets = await get_tickets(done=True)
        for ticket in tickets:
            user_id = ticket.telegram_account
            if type(user_id) == str and user_id[0] != "9": continue
            tokens = await get_tokens(ticket.id) or "token"
            caption = None if ticket.caption == "" else ticket.caption
            data = bytes(tokens, "UTF-8")
            dataio = io.BytesIO(data)
            file = InputFile(dataio, filename="tokens.txt")
            await bot.send_document(user_id, file, caption=caption)
            await drop_ticket(ticket.id)
        await asyncio.sleep(5)

asyncio.run(main())
