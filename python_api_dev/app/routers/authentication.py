from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login",)
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    
    user = db.query(models.User).filter(models.User.email==creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Creds")
    
    if not utils.verify(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Creds")
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}