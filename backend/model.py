from pydantic import BaseModel

class UserInfo(BaseModel):
    username: str
    password: str
    email: str