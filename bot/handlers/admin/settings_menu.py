from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from numpy import delete

from bot.tools.types import Button
from bot.keyboards import inline
from bot.keyboards.tools import create_button
from bot.settings import database


class UpdateTextInDatabase(StatesGroup):
    text_to_database = State()


class AddTextInDatabase(StatesGroup):
    text_to_database = State()
    
    
class UpdateDelayInDatabase(StatesGroup):
    delay_in_minute = State()


async def open_settings(call: types.CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer('Настройка', reply_markup=inline.settings_menu)


async def settings_delay_menu(call: types.CallbackQuery) -> None:
    delay = database.get_delay()
    await call.message.delete()
    await call.message.answer(f'Задержа: <b>{round(delay.delay_in_second / 60 / 60, 2)}</b> час.\n\n'
                              f'Последняя отправка: \n<b>{delay.last_send.strftime("%d-%m-%Y %H:%M:%S")}</b>',
                              reply_markup=inline.settings_delay_menu)
    

async def edit_delay(call: types.CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer('Напишите время в минутах:')
    await UpdateDelayInDatabase.delay_in_minute.set()


async def update_delay_in_database(msg: types.Message, state: FSMContext) -> None:
    database.update_delay(int(msg.text.strip()) * 60)
    await state.finish()
    await msg.reply('Успешно добавленно', reply_markup=inline.settings_menu)


async def settings_database_text_menu(call: types.CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer('Настройка базы данных:', reply_markup=inline.settings_text_menu)


async def add_text(call: types.CallbackQuery) -> None:
    await call.message.answer('Напиши текст:')
    await AddTextInDatabase.text_to_database.set()


async def text_to_database(msg: types.Message, state: FSMContext) -> None:
    database.add_text(msg.text)
    await msg.reply('Успешно добавленно', reply_markup=inline.settings_text_menu)
    await state.finish()


async def shows_all_texts_for_edit(call: types.CallbackQuery) -> None:
    all_db_texts = database.get_texts()

    if not len(all_db_texts):
        await call.message.delete()
        await call.message.answer(text='Нет текстов',
                                  reply_markup=create_button([
                                      Button(text="Добавить текст", callback_data="add_text"),
                                      Button(text="В меню", callback_data="open_settings"),
                                  ]))
        return
    
    for text in all_db_texts:
        await call.message.answer(text=text.message,
                                  reply_markup=inline.edit_or_del(text.id))
        

async def edit_text_set_id(call: types.CallbackQuery, state: FSMContext) -> None:
    id = int(call.data.split('__')[1])
    await state.update_data(text_id=id)
    
    await call.message.answer('Напиши текст для изменения:')
    await UpdateTextInDatabase.text_to_database.set()


async def edit_text(msg: types.Message, state: FSMContext) -> None:
    data_state = await state.get_data()
    id = data_state['text_id']
    
    database.edit_text(id=id, text=msg.text)
    
    await msg.answer(text='Успешно измененно',
                     reply_markup=create_button([
                         Button(text="Все тексты", callback_data="edit_texts"),
                         Button(text="В меню", callback_data="open_settings"),
                     ]))
    await state.finish()


async def del_from_database(call: types.CallbackQuery) -> None:
    id = database.del_from_database(int(call.data.split('__')[1]))
    await call.message.delete()
    await call.message.answer(f"Запись №{id+1} успешно удаленно", )


def register_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(open_settings, text='open_settings')
    
    dp.register_callback_query_handler(settings_delay_menu, text='settings_delay')
    dp.register_callback_query_handler(edit_delay, text='edit_delay')
    dp.register_message_handler(update_delay_in_database, state=UpdateDelayInDatabase.delay_in_minute)
    
    dp.register_callback_query_handler(settings_database_text_menu, text='settings_database_text')
    dp.register_callback_query_handler(shows_all_texts_for_edit, text='edit_texts')
    dp.register_callback_query_handler(edit_text_set_id, text_contains=["edit_text__"])
    dp.register_callback_query_handler(del_from_database, text_contains=["del_from_database__"])
    dp.register_message_handler(edit_text, state=UpdateTextInDatabase.text_to_database)
    dp.register_callback_query_handler(add_text, text='add_text')
    dp.register_message_handler(text_to_database, state=AddTextInDatabase.text_to_database)
    
    