from datetime import datetime

from pydantic import BaseModel


class TextFromDatabase(BaseModel):
    id: int
    message: str


class DelayFromDatabase(BaseModel):
    delay_in_second: int
    last_send: datetime


class Button(BaseModel):
    text: str
    callback_data: str


class Dialogs(BaseModel):
    name: str
    id: int