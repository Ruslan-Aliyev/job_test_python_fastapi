from pydantic import BaseModel
from datetime import date

class AuthDetails(BaseModel):
	username: str
	password: str

class UserBaseSchema(BaseModel):
    username: str
    password: str
    birthday: date
