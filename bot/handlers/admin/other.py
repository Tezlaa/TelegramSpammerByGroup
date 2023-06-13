from aiogram import Dispatcher, types

import bot.settings as settings
from bot.keyboards.inline import admin_menu


async def start(msg_call: types.Message | types.CallbackQuery):
    """ Take Message or Callback """
    
    if isinstance(msg_call, types.CallbackQuery):
        if str(msg_call.from_user.id) not in settings.ADMINS_ID:
            return
        await msg_call.message.delete()
        
        msg_call = msg_call.message
    else:
        if str(msg_call.from_id) not in settings.ADMINS_ID:
            return
    
    await msg_call.answer('Админ панель', reply_markup=admin_menu)


def register_admin_other_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start, text='start_menu')
    dp.register_message_handler(start, commands=['start'])