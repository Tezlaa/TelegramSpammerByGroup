from environs import Env

from bot.database.sql import Database


env = Env()
env.read_env()

TELEGRAM_TOKEN = env.str('TOKEN')
ADMINS_ID: list[str] = env.list('ADMINS_ID')

API_ID = env.int('API_ID')
API_HASH = env.str('API_HASH')
PHONE_NUMBER = env.str('PHONE_NUMBER')

DIALOGS_ID = env.list('DIALOGS_ID')

database = Database('BotDatabase.db')