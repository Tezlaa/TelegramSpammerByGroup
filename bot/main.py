import asyncio
from typing import NoReturn

from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import bot.settings as settings
from bot.handlers.register import register_all_handlers
from bot.tools.utils import start_sending_message


async def __on_start_up(dp: Dispatcher) -> NoReturn:
    database = settings.database
    if database.get_sending_option():
        asyncio.create_task(start_sending_message())
    
    register_all_handlers(dp)


def start_bot() -> None:
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)