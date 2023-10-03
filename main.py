from fastapi import FastAPI, Depends, HTTPException, status, Response
from typing import List
from auth import AuthHandler
from schemas import AuthDetails, UserBaseSchema
from models import User
from database import get_db
from sqlalchemy.orm import Session

app = FastAPI()   

auth_handler = AuthHandler()
"""users = []"""

@app.get("/users")
async def read_users(db: Session = Depends(get_db)):
  users = db.query(User).all()
  return users

@app.get("/user/{id}")
async def read_user(id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {id} found')
  
  return user

@app.post("/user")
async def create_user(payload: UserBaseSchema, db: Session = Depends(get_db)): 
  user = User(username=payload.username, password=payload.password, birthday=payload.birthday)
  db.add(user)
  db.commit()
  return user

@app.patch("/user/{id}")
async def update_item(id: int, payload: UserBaseSchema, db: Session = Depends(get_db)):
  query = db.query(User).filter(User.id == id)
  record = query.first()

  if not record:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No record with this id: {id} found')
  
  entry = payload.dict(exclude_unset=True)
  query.update(entry, synchronize_session=False)
  db.commit()

  return entry

@app.delete("/user/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
  query = db.query(User).filter(User.id == id)
  record = query.first()

  if not record:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No record with this id: {id} found')

  query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)



"""
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
"""
