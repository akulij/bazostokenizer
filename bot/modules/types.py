from pydantic import BaseModel

class User(BaseModel):
    id: int

class Ticket(BaseModel):
    process_id: int
    msg: str
    error: str | None

class TicketData(BaseModel):
    id: int
    telegram_account: int | str
    numbers_count: int
    caption: str
    status: str
