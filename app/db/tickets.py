from sqlalchemy.util import asyncio
from sqlmodel import select
from app.types.ticket import TicketStatus, TicketInfo

from .tables import (
        Ticket,
        Token
        )
from . import session

async def create_ticket(ticket_creation: TicketInfo):
    ticket = Ticket.parse_obj({**ticket_creation.dict(), "status": "creating"})
    session.add(ticket)
    await session.commit()

    return TicketStatus(process_id=ticket.id, msg="Creating")

async def get_tickets():
    q = select(Ticket)
    e = await session.exec(q)
    
    tickets: list[Ticket] = e.all()

    return tickets

async def get_ticket(process_id: int):
    q = select(Ticket).where(Ticket.id == process_id)
    ticket = (await session.exec(q)).first()

    return ticket

async def get_undone_tickets():
    q = select(Ticket).where(Ticket.done == 0)
    e = await session.exec(q)

    tickets: list[Ticket] = e.all()

    return tickets

async def store_token(process_id: int, token: str):
    token_db = Token(process_id=process_id, token=token)
    session.add(token_db)
    await session.commit()

async def set_ticket_done(ticket_id: int, done: bool):
    q = select(Ticket).where(Ticket.id == ticket_id)
    e = await session.exec(q)

    ticket: Ticket = e.first()

    ticket.done = int(done)

    session.add(ticket)
    await session.commit()

async def get_tokens(process_id: int) -> list[str]:
    q = select(Token).where(Token.process_id == process_id)
    e = await session.exec(q)
    
    tokens: list[Token] = e.all()

    return [token.token for token in tokens]
