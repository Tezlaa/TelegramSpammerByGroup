from typing import List

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

from bot.types import Button


def create_button(setup: List[Button], row_width: int = 1) -> InlineKeyboardMarkup:
    """ Create button

    Args:
        setup (List[Button]): settings for InlineKeyboardButton,
            Example: [Button(text='text on the button',
                                     callback_data='your_call_back_data'), ...]
        row_width (int, optional): row width. Defaults to 1.

    Returns:
        InlineKeyboardMarkup
    """

    button = InlineKeyboardMarkup(row_width)
    for i in range(len(setup)):
        button.add(InlineKeyboardButton(text=setup[i].text,
                                        callback_data=setup[i].callback_data))
    
    return button
