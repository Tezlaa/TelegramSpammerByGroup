from aiogram import Dispatcher, types

from bot.settings import database
from bot.keyboards.inline import admin_menu


async def start_sending_text(call: types.CallbackQuery):
    
    await call.answer('Админ панель', reply_markup=admin_menu)


def register_admin_send_text_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_sending_text, text='start_sending_text')