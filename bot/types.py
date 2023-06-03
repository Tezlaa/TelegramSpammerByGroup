from pydantic import BaseModel


class TextFromDatabase(BaseModel):
    id: int
    message: str


class Button(BaseModel):
    text: str
    callback_data: str
