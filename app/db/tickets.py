from sqlalchemy.util import asyncio
from sqlmodel import select
from app.types.ticket import TicketStatus, TicketInfo

from .tables import Ticket
from . import session

async def create_ticket(ticket_creation: TicketInfo):
    ticket = Ticket.parse_obj({**ticket_creation.dict(), "status": "creating", "done": False})
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
