import pytz
import sqlite3
import logging
from datetime import datetime

from bot.tools.types import TextFromDatabase, DelayFromDatabase


class DatabaseConfig:
    """ Create connect and cursor for database,
        this is base class """
    
    def __init__(self, database_name: str) -> None:
        self.connect = sqlite3.connect(database_name)
        
        if self.connect:
            logging.info('Database is connected!')
        else:
            logging.warning(self.connect)
            return
        
        self.cur = self.connect.cursor()
        

class TextToSubmit(DatabaseConfig):
    """ Interface for settings texts in the database,
        CURD class: can do Create, Update, Read, Delete
        """
    
    def create_main_database(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS telegram_spammer(
            id INTEGER PRIMARY KEY,
            message TEXT)""")
        
        self.connect.commit()
    
    def get_text_by_id(self, id: int) -> TextFromDatabase:
        """ Get text by id from database """
        
        data = self.cur.execute(f"SELECT * FROM telegram_spammer WHERE id={id}").fetchone()
        return TextFromDatabase(id=data[0], message=data[1])
    
    def get_texts(self) -> list[TextFromDatabase]:
        """ Get all texts from database """
        
        data = self.cur.execute("""SELECT * FROM telegram_spammer""").fetchall()
        return [TextFromDatabase(id=element[0], message=element[1]) for element in data]

    def add_text(self, text: str) -> None:
        """ Added text to database """
        
        self.cur.execute("INSERT INTO telegram_spammer (message) VALUES (?)", (text, ))
        self.connect.commit()

    def edit_text(self, id: int, text: str) -> TextFromDatabase:
        """ Edit text by id in the database """
        
        self.cur.execute("UPDATE telegram_spammer SET message = ? WHERE id = ?", (text, id))
        self.connect.commit()
        return TextFromDatabase(id=id, message=text)
    
    def del_from_database(self, id: int) -> int:
        """ Deleted text from database by his id.
            Return: his id """
        
        self.cur.execute(f"DELETE FROM telegram_spammer WHERE id={id}")
        self.connect.commit()
        return id


class TimerForSendingMessage(DatabaseConfig):
    def create_delay_database(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS delay(
            delay INT,
            last_send timestamp)""")
        
        if not self.cur.execute("SELECT * FROM delay").fetchone():
            #  set default delay: 12h / last_send: now
            self.cur.execute("INSERT INTO delay VALUES(?, ?)", (60 * 60 * 12,
                                                                datetime.now(tz=pytz.timezone('Europe/Kyiv'))))
            
        self.connect.commit()
    
    def get_delay(self) -> DelayFromDatabase:
        """ get delay and time of last shipment """
        
        data = self.cur.execute("SELECT * FROM delay").fetchone()
        return DelayFromDatabase(delay_in_second=data[0], last_send=data[1])
        
    def update_delay(self, time_in_seconds: int) -> int:
        """ Update delay in the database.
            Return: time_in_seconds"""
        
        self.cur.execute("UPDATE delay SET delay = ?", (time_in_seconds, ))
        self.connect.commit()
        return time_in_seconds
    
    def update_last_send(self, time_now: datetime) -> datetime:
        """ Update time of last shipment
            Return: time_now """

        self.cur.execute("UPDATE delay SET last_send = ?", (time_now, ))
        self.connect.commit()
        return time_now


class SettingsBot(DatabaseConfig):
    def create_settings_database(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS settings(
            sending INTEGER)""")
        
        if not self.cur.execute("SELECT 1 FROM settings").fetchone():
            self.cur.execute("INSERT INTO settings VALUES (?)", (0, ))
            
        self.connect.commit()

    def get_sending_option(self) -> bool:
        """ Get sending option
            Return: True - enable sending
                    False - disable sending"""
                    
        return True if self.cur.execute("SELECT 1 FROM settings").fetchone()[0] else False

    def update_sending_option(self, sending: bool = True) -> bool:
        """ Enable or disable the sending option
            Return: sending"""
            
        self.cur.execute("UPDATE settings SET VALUES(?)", (1 if sending else 0, ))
        self.connect.commit()
        return sending


class Database(SettingsBot, TextToSubmit, TimerForSendingMessage):
    """ Create database and CRUD all table """
    def __init__(self, database_name: str) -> None:
        super().__init__(database_name)
        
        self.create_main_database()
        self.create_settings_database()
        self.create_delay_database()