from aiohttp import ClientSession

ENDPOINTS = [
        "https://functions.yandexcloud.net/d4eu2pjdbl5csnih2i7b",
        "https://functions.yandexcloud.net/d4eg74rncihgcg18c9v9",
        "https://functions.yandexcloud.net/d4esmg9vgj17nk0h8qtc",
        "https://functions.yandexcloud.net/d4e4rh73qji6lvloaaa3",
        "https://functions.yandexcloud.net/d4eob2fop2gbcgliku6m",
        ]

def generator(l):
    idx = 0
    while True:
        yield l[idx%len(l)]
        idx += 1

endpoint = generator(ENDPOINTS)

async def send_sms(number: str):
    data = {
            "method": "send_sms",
            "arguments": [number],
            }
    async with ClientSession() as session:
        async with session.post(next(endpoint),
                                data=data) as response:
            status = response.status
    
    if status == 200:
        return True
    else:
        return False

async def get_token(number: str, code: str):
    data = {
            "method": "get_token",
            "arguments": [number, code],
            }
    async with ClientSession() as session:
        async with session.post(next(endpoint),
                                data=data) as response:
            status = response.status

            if status == 200:
                data = await response.json()
                return data["content"]
            else:
                return None
