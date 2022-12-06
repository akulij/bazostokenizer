from peewee import (
    SqliteDatabase,
    Model,
    ForeignKeyField,
    CharField,
    IntegerField,
    DateTimeField,
    BooleanField,
    FloatField,
    TextField,
)

from modules.types import User

db = SqliteDatabase("application.db")

class DBModel(Model):
    class Meta:
        database = db

class UserTable(DBModel):
    user_id = IntegerField(unique=True)

def migrate():
    db.create_tables([UserTable])

async def new_user(user: User):
    if not await is_user_in_db(user):
        await create_user(user)
        return True

    return False

async def is_user_in_db(user: User) -> bool:
    is_exists = UserTable.select().where(UserTable.user_id == user.id).exists()
    return is_exists

async def create_user(user: User):
    UserTable.create(user_id=user.id)
