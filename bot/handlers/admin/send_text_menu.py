import asyncio
from aiogram import Dispatcher, types

from bot.settings import database
from bot.keyboards.inline import admin_menu
from bot.tools.utils import start_sending_message


async def call_start_sending_message(call: types.CallbackQuery):
    if not database.get_sending_option():
        database.update_sending_option(True)
        asyncio.create_task(start_sending_message())
        
    await call.message.delete()
    await call.answer('Админ панель', reply_markup=admin_menu)
    

def register_admin_send_text_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(call_start_sending_message, text='start_sending_text')