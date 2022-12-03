from sqlmodel import SQLModel, Field, table

class Ticket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    telegram_account: str
    numbers_count: int
    caption: str
    status: str
    done: bool = Field(default=False)

class Token(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    process_id: int
    token: str
