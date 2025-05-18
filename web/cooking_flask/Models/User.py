from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    username: str
    user_email: str
    first_name: str
    last_name: str
    password_hash: str
    date_joined: date