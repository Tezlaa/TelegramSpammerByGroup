from aiogram import Dispatcher, types

import bot.settings as settings


async def start(msg: types.Message):
    if str(msg.from_id) not in settings.ADMINS_ID:
        return
    
    await msg.answer('Hello')


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])