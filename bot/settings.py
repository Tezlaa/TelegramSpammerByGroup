from environs import Env

env = Env()
env.read_env()

TELEGRAM_TOKEN = env.str('TOKEN')
ADMINS_ID: list[str] = env.list('ADMINS_ID')
