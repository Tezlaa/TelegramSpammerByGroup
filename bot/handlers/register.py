from aiogram import Dispatcher
from bot.handlers.admin import (
    register_admin_other_handlers,
    register_admin_handlers,
    register_admin_send_text_handlers
)


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_admin_other_handlers,
        register_admin_handlers,
        register_admin_send_text_handlers
    )
    for handler in handlers:
        handler(dp)