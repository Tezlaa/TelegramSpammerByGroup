from pydantic import BaseModel


class TextFromDatabase(BaseModel):
    id: int
    message: str
