from sqlmodel import SQLModel, Field, table

class Ticket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    telegram_account: str
    numbers_count: int
    caption: str
