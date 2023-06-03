from aiogram.types import InlineKeyboardMarkup

from bot.types import Button
from bot.keyboards.tools import create_button


def edit_or_del(id: int) -> InlineKeyboardMarkup:
    button = create_button([
        Button(text='Изменить', callback_data=f"edit_text__{id}"),
        Button(text='Удалить', callback_data=f"del_from_database__{id}"),
    ])
    return button


admin_menu = create_button([
    Button(text="Старт отправки тексов", callback_data="start_sending_text"),
    Button(text="Остановить⛔", callback_data="stop_sending_text"),
    Button(text="Настройки", callback_data="open_settings"),
])

settings_menu = create_button([
    Button(text="Настройка текстов отправки", callback_data="settings_database_text"),
    Button(text="Настройка задержки", callback_data="settings_timeout"),
    Button(text="Назад", callback_data="start_menu"),
])

settings_text_menu = create_button([
    Button(text="Изменить/Все текста", callback_data="edit_texts"),
    Button(text="Добавить", callback_data="add_text"),
    Button(text="Назад", callback_data="open_settings"),
])

after_edit = create_button([
    Button(text="Изменит/Все текста", callback_data="edit_texts"),
    Button(text="Вернуться", callback_data="settings_database_text"),
])
