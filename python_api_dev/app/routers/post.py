

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
     prefix = "/posts",
     tags = ['posts']
)


@router.get("/", response_model = List[schemas.PostBase])
async def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/",status_code = status.HTTP_201_CREATED, response_model=schemas.PostCreate)
async def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db)) -> Any:

        new_post = models.Post(
            **post.dict()
        )

        db.add(new_post) 
        db.commit()
        db.refresh(new_post) 
        return new_post
   

@router.get("/{id}", response_model = schemas.PostBase)
async def get_posts(id: int, response: Response, db: Session= Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = {"message":"not found"})    
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id:int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"not found"})

    post.delete(synchronize_session = False)
    db.commit()
 

@router.put("/{id}")
async def update_posts(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
  
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"message":"not updated"})

    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()
    return post_query.first()
