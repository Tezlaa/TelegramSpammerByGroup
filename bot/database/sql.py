import sqlite3
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
    
    def create_main_database(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS telegram_spammer(
            id INTEGER PRIMARY KEY,
            message TEXT)""")
        
        self.connect.commit()
    
    def get_text(self, id: int | None = None) -> TextFromDatabase | list[TextFromDatabase]:
        """ Get text or texts from database,
            if need to get one text get his id """
        
        if id:  # if have id
            data = self.cur.execute(f"SELECT * FROM telegram_spammer WHERE id={id}").fetchone()
            return TextFromDatabase(id=data[0], message=data[1])
        
        data = self.cur.execute("""SELECT * FROM telegram_spammer""").fetchmany()
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