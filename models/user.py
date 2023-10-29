from pydantic import BaseModel

class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    
