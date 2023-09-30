from pydantic import BaseModel
from datetime import date, datetime

class AuthDetails(BaseModel):
	username: str
	password: str

class TestBaseSchema(BaseModel):
	id: int
	thing: str

class UserBaseSchema(BaseModel):
    id: int
    username: str
    password: str
    birthday: date
    create_time: datetime
    last_login: datetime
