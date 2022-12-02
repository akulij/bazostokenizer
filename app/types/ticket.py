from pydantic import BaseModel

class TicketInfo(BaseModel):
    telegram_account: int | str
    numbers_count: int
    caption: str | None = None

class TicketStatus(BaseModel):
    process_id: int
    msg: str
    error: str | None = None
