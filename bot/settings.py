from environs import Env

from bot.database.sql import Database


env = Env()
env.read_env()

TELEGRAM_TOKEN = env.str('TOKEN')
ADMINS_ID: list[str] = env.list('ADMINS_ID')

database = Database('BotDatabase.db')