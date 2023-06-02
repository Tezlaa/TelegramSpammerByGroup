from aiogram import Dispatcher, types

import bot.settings as settings
from bot.keyboards.inline import admin_menu


async def start(msg: types.Message):
    if str(msg.from_id) not in settings.ADMINS_ID:
        return
    
    await msg.answer('Админ Панель', reply_markup=admin_menu)


def register_admin_other_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])