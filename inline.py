from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton


"""--------------ADMIN---------------"""
admin_menu = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("💬Отправка отзывов📣", callback_data='start_feadback'),
    InlineKeyboardButton("Остановить⛔", callback_data='stop_feadback'),
    InlineKeyboardButton('📊Отправка курса🔔', callback_data='send_early_rate'),
    InlineKeyboardButton("Остановить⛔", callback_data='stop_early_rate'),
)
