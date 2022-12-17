import asyncio
from aiohttp import ClientSession

PROXY = "http://bkabuse5229:5f35bc@192.145.98.63:10223"
PROXY = None

COOKIES = {
    "rekkk": "ano",
    "testcookie": "ano",
    "testcookieaaa": "ano",
    "rekkkb": "ano",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://zvirata.bazos.cz",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://zvirata.bazos.cz/pridat-inzerat.php",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    # "TE": "trailers",
}

URL = "http://zvirata.bazos.cz/pridat-inzerat.php"

async def send_sms(number: str):
    data = {
        "podminky": "1",
        "teloverit": number,
        "Submit": "Odeslat",
    }
    
    async with ClientSession() as session:
        async with session.post(URL,
                                cookies=COOKIES,
                                headers=HEADERS,
                                data=data,
                                proxy=PROXY) as response:
            status = response.status
    
    if status == 200:
        return True
    else:
        return False

async def get_token(number: str, code: str):
    data = {
        "klic": code,
        "klictelefon": number,
        "Submit": "Odeslat",
    }
    
    token = None
    async with ClientSession() as session:
        async with session.post(URL,
                                cookies=COOKIES,
                                headers=HEADERS,
                                data=data,
                                proxy=PROXY) as response:
            status = response.status
            with open("temp.html", "w") as file:
                file.write(await response.text())
            print(response.headers)
            cookie = response.headers["Set-Cookie"]
            print(cookie)
            filtered = session.cookie_jar.filter_cookies(URL)
            for key, value in filtered.items():
                print(f"COOKIE {key} | {value}")
                print(value.value)
                if "bkod=" in str(value):
                    print("THERE")
                    print(value.key)
                    print(value.value)
                    token = value.value
                    print(token)
                    break
    
    # token = cookie.split(";", 1)[0].split("bkod=", 1)[1]
    # token = data

    return token
