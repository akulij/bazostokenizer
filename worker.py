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
    print("TZ")
    print(tzid, number)
    # for index in range(2, count):
    drop_flag = False
    for index in range(count):
        print(f"sending sms to number {number}")
        await send_sms(number)
        print("getting code")
        code = await get_sms(tzid, index)
        print(f"getting token with code {code}")
        token = await get_token(number, code)
        if token == None:
            print("sending sms")
            await send_sms(number)
            print("getting code")
            code = await get_sms(tzid, index)
        print("storing {token=}")
        if token == None:
            drop_flag = True
            break
        await store_token(process_id, token)
        print("cooldown")
        if index + 1 != count: await asyncio.sleep(60*1.5)
    if drop_flag:
        await task(count, process_id)

async def main():
    while True:
        tickets = await get_undone_tickets()
        for ticket in tickets:
            numbers_count = ticket.numbers_count
            tasks_count = numbers_count
            print(f"TICKET for tasks count {tasks_count}")

            tasks = [task(1, ticket.id) for _ in range(tasks_count)]
            pool = []
            for pstask in tasks:
                pool.append(pstask)
                if len(pool) == 5:
                    await asyncio.gather(*pool)
                    pool.clear()
            await asyncio.gather(*pool)

            await set_ticket_done(ticket.id, True)
        await asyncio.sleep(3)

asyncio.run(main())
