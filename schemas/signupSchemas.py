from pydantic import BaseModel

class SignUp(BaseModel):
    username:str
    password:str
    