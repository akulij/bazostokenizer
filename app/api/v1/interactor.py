from fastapi import APIRouter
from pydantic import BaseModel

from app.types import *
from app.db.tables import Ticket as DBTicket
from app.db import (
        create_ticket,
        get_tickets,
        get_ticket,
        )

router = APIRouter()


@router.post("/proceed", response_model=TicketStatus)
async def proceed(ticket_request: TicketInfo):
    ticket = await create_ticket(ticket_request)
    return ticket

@router.get("/tickets", response_model=list[DBTicket])
async def tickets():
    tickets = await get_tickets()
    return tickets

@router.get("/ticket", response_model=DBTicket | None)
async def status(process_id: int):
    ticket: DBTicket | None = await get_ticket(process_id)
    return ticket
