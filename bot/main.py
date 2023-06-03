from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.register import register_all_handlers

import bot.settings as settings


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)


def start_bot():    
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)