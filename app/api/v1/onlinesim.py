from typing import Literal
import typing
from aiohttp import ClientSession

from app.config import settings

API_PATH = "https://onlinesim.io/api"
DEMO_API_PATH = "https://onlinesim.io/demo/api"

Action = Literal["getState", "getNumbersStats"]

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

    return data


async def get_numbers_count() -> int:
    data = await fetch_api("getNumbersStats", {"country": 420}, False)

    return data["services"]["service_bazos"]["count"]
