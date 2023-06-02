from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


"""--------------ADMIN---------------"""
admin_menu = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Старт отправки тексов",
                         callback_data='start_sending_text'),
    InlineKeyboardButton("Остановить⛔",
                         callback_data='stop_sending_text'),
    InlineKeyboardButton('Настройки',
                         callback_data='open_settings'),
)

settings_menu = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton('Настройка текстов отправки',
                         callback_data='settings_database_text'),
    InlineKeyboardButton('Настройка задержки',
                         callback_data='settings_timeout')
)