#Importing modules

from typing import Optional, Any, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from .routers import post, user, authentication

models.Base.metadata.create_all(bind=engine)

app =  FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)


# Server APIs




