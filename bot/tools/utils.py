import asyncio
import logging
from datetime import datetime
import random

import pytz

import bot.settings as settings
from bot.settings import database

from telethon import TelegramClient
from telethon.utils import get_display_name
from telethon.errors import SessionPasswordNeededError

from bot.tools.types import Dialogs


async def start_sending_message():
    all_message_for_send = database.get_texts()
    delay_for_sending = database.get_delay()
    client = await connect_telegram(settings.PHONE_NUMBER,
                                    settings.API_ID,
                                    settings.API_HASH)
    dialogs = settings.DIALOGS_ID
    
    while database.get_sending_option():
        messages = [message_class.message for message_class in all_message_for_send]
        random.shuffle(messages)

        for message in messages:
            await client.send_message(int(random.choice(dialogs)), message)
            await asyncio.sleep(delay_for_sending.delay_in_second)
            
            database.update_last_send(datetime.now(
                tz=pytz.timezone('Europe/Kyiv')
            ))


async def connect_telegram(phone: str, api_id: int, api_hash: str) -> TelegramClient:
    """
    Args:
        phone (str): phone number
        api_id (str): need to register ur own application here - https://my.telegram.org/auth
        api_hash (str): here https://my.telegram.org/auth
        
    Returns:
        client: connect account
    """
    
    client = TelegramClient(phone, api_id, api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        await authorized_user(client, phone)
        
    logging.info('Client initialization complete')
    return client


async def authorized_user(client: TelegramClient, phone: str) -> None:
    """ Authorized user

    Args:
        client (TelegramClient): his client
        phone (str): number for authorized
    """
    
    await client.send_code_request(phone)
    try:
        await client.sign_in(phone, code=input('Enter code: '))
    except SessionPasswordNeededError:
        await client.sign_in(password=input('password: '))
        

async def get_dialogs(how_much_dialogs: int, client: TelegramClient) -> list[Dialogs]:
    """ get account dialogs

    Args:
        how_much_dialogs (int)
        client (TelegramClient)

    Returns:
        list[Dialogs]: list with info about dialog
                       Dialogs(name='HIS NAME', id='HIS ID FOR SENDING')
    """
    dialogs = await client.get_dialogs(how_much_dialogs)
    return [Dialogs(name=get_display_name(dialog.entity),
                    id=dialog.entity.id) for dialog in dialogs]