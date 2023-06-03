import sqlite3
import datetime
import logging

from bot.types import TextFromDatabase
    
    
class Database:
    def __init__(self, database_name: str) -> None:
        self.connect = sqlite3.connect(database_name)
        
        if self.connect:
            logging.info('Database is connected!')
        else:
            logging.warning(self.connect)
            return
        
        self.cur = self.connect.cursor()
        self.create_main_database()
        self.create_delay_database()
    
    def create_main_database(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS telegram_spammer(
            id INTEGER PRIMARY KEY,
            message TEXT)""")
        
        self.connect.commit()
    
    def create_delay_database(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS delay(
            delay INT,
            last_send timestamp)""")
        
        if not self.cur.execute("SELECT * FROM delay").fetchone():
            #  set default delay: 12h / last_send: now
            self.cur.execute("INSERT INTO delay VALUES(?, ?)", (60 * 60 * 12,
                                                                datetime.datetime.now()))
            
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
    
    def update_delay(self, time_in_seconds: int) -> int:
        """ Update delay in the database.
            Return: time_in_seconds"""
        
        self.cur.execute("UPDATE dalay SET time_in_seconds = ?", (time_in_seconds, ))
        return time_in_seconds