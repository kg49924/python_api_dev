#Importing modules

from typing import Optional, Any, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from .. import models, schemas, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext


router = APIRouter(
      prefix="/users",
      tags = ['users']
)

@router.post("/",status_code = status.HTTP_201_CREATED, response_model = schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
     
        #hash the password - user.password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(
            **user.dict()
        )

        db.add(new_user) 
        db.commit()
        db.refresh(new_user) 
        return new_user 
             
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_detail = db.query(models.User).filter(models.User.id == id).first()

    if not user_detail:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = {"message":"not found"})
         
    return user_detail       
