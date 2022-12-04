from math import ceil
import asyncio

from app.db import (
        get_undone_tickets,
        store_token,
        set_ticket_done,
        )
from app.api.v1.onlinesim import (
        get_number,
        get_sms,
        )

from bazosapi import (
        send_sms,
        get_token
        )

ONT_COUNT = 4 # One Number Token count

async def task(count: int, process_id: int):
    tzid, number = await get_number()
    for index in range(count):
        await send_sms(number)
        code = await get_sms(tzid, index)
        token = get_token(number, code)
        await store_token(process_id, token)

async def main():
    while True:
        tickets = await get_undone_tickets()
        for ticket in tickets:
            numbers_count = ticket.numbers_count
            tasks_count = ceil(numbers_count / ONT_COUNT)
            tasks = [task(ONT_COUNT, ticket.id) for _ in range(tasks_count)]
            asyncio.gather(*tasks)
            await set_ticket_done(ticket.id, True)

asyncio.run(main())