from fastapi import FastAPI, Depends, HTTPException, status, Response
from typing import List
from auth import AuthHandler
from schemas import AuthDetails, UserBaseSchema
from models import User
from database import get_db
from sqlalchemy.orm import Session

app = FastAPI()   

auth_handler = AuthHandler()

@app.post("/register")
async def register(payload: UserBaseSchema, db: Session = Depends(get_db)): 
  user = User(username=payload.username, password=auth_handler.get_password_hash(payload.password), birthday=payload.birthday)
  db.add(user)
  db.commit()
  return user

@app.post('/login')
def login(auth_details: AuthDetails, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.username == auth_details.username).first()
  
  if (not user) or (not auth_handler.verify_password(auth_details.password, user.password)):
    raise HTTPException(status_code=401, detail='Invalid username and/or password')

  token = auth_handler.encode_token(user.username)

  return { 'token': token, 'username': user.username, 'id': user.id }

@app.get("/users")
async def read_users(db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
  users = db.query(User).all()
  return users

@app.patch("/user/{id}")
async def update_item(id: int, payload: UserBaseSchema, db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
  query = db.query(User).filter(User.id == id)
  record = query.first()

  if not record:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No record with this id: {id} found')
  
  entry = payload.dict(exclude_unset=True)
  query.update(entry, synchronize_session=False)
  db.commit()

  return entry

@app.delete("/user/{id}")
async def delete_user(id: int, db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
  query = db.query(User).filter(User.id == id)
  record = query.first()

  if not record:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No record with this id: {id} found')

  query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)
