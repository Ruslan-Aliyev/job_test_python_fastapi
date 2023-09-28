from pydantic import BaseModel

class AuthDetails(BaseModel):
	username: str
	password: str

class Item(BaseModel):
	id: int
	name: str
	price: float
