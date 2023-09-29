from fastapi import FastAPI, Depends, HTTPException
from typing import List
from auth import AuthHandler
from schemas import AuthDetails, Item

app = FastAPI()   

"""
@app.get("/") 
async def main_route():     
  return {"message": "Hey, It is me Goku"}
"""

auth_handler = AuthHandler()
users = []
items = []

@app.get("/items", response_model=List[Item])
async def read_items():
  return items

@app.get("/item/{item_id}", response_model=Item)
async def read_item(item_id: int):
  return items[item_id]

@app.post("/item", response_model=Item)
async def create_item(item: Item):
  items.append(item)
  return item

@app.patch("/item/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
  items[item_id] = item
  return item

@app.delete("/item/{item_id}")
async def delete_item(item_id: int):
  del items[item_id]
  return {"message": "Item deleted"}



@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
  if any(x['username'] == auth_details.username for x in users):
    raise HTTPException(status_code=400, detail='Username is taken')
  hashed_password = auth_handler.get_password_hash(auth_details.password)
  users.append({
    'username': auth_details.username,
    'password': hashed_password    
  })
  return


@app.post('/login')
def login(auth_details: AuthDetails):
  user = None
  for x in users:
    if x['username'] == auth_details.username:
      user = x
      break
  
  if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
    raise HTTPException(status_code=401, detail='Invalid username and/or password')
  token = auth_handler.encode_token(user['username'])
  return { 'token': token }


@app.get('/unprotected')
def unprotected():
  return { 'hello': 'world' }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
  return { 'name': username }
