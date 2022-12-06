import asyncio
from typing import Literal
import typing
from aiohttp import ClientSession

from app.config import settings

API_PATH = "https://onlinesim.io/api"
DEMO_API_PATH = "https://onlinesim.io/demo/api"

Action = Literal["getState", "getNumbersStats", "getNum"]

async def fetch_api(action: Action, params: dict, demo: bool = False) -> dict:
    parameters = {
            "apikey": settings.online_sim_token,
            **params
            }
    session = ClientSession()

    api_path = DEMO_API_PATH if demo else API_PATH
    async with session.get(f"{api_path}/{action}.php",
                           params=parameters) as response:
        data = await response.json()
        if type(data) == list:
            data = data[0]

    await session.close()

    print(data)
    return data


async def get_numbers_count() -> int:
    data = await fetch_api("getNumbersStats", {"country": 420}, False)

    return data["services"]["service_bazos"]["count"]

async def get_number() -> tuple[int, str]:
    return 7811957, "+420737873751"
    data = await fetch_api("getNum", {"country": 420, "service": "bazos", "number": "true"})

    return data["tzid"], data["number"]

async def get_sms(tzid: int, index: int) -> str | None:
    wait_time = 15
    sms = None
    for _ in range(5):
        data = await fetch_api("getState", {"tzid": tzid, "msg_list": 1})
        if "msg" in data:
            messages = data["msg"]
            if len(messages) > index:
                sms = messages[index]["msg"]
                break
            else:
                await asyncio.sleep(wait_time)
        else:
            await asyncio.sleep(wait_time)

    return sms
