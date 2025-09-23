from pydantic import BaseModel


class Loign (BaseModel):
    username:str
    password:str
    