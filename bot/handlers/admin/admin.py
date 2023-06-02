from aiogram import Dispatcher, types

from bot.keyboards.inline import settings_menu
from bot.settings import database


async def open_settings(call: types.CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer('Настройка', reply_markup=settings_menu)


async def shows_all_texts_for_edit(call: types.CallbackQuery) -> None:
    all_db_texts = database.get_text()
    
    if not len(all_db_texts):
        await call.message.answer('Нет текстов')
        return
    
    for text in all_db_texts:
        await call.message.answer(text=text.message)
    

def register_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(open_settings, text='open_settings')
    dp.register_callback_query_handler(shows_all_texts_for_edit, text='settings_database_text')