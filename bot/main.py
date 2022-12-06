from aiogram import executor

from config import dp

from modules import (
        commands,
        ticket_integration
        )

if __name__ == "__main__":
    executor.start_polling(dp)
