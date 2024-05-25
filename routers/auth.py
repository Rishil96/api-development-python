from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schema import UserLogin
import models
import utils
import oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm is a class provided by FastAPI that allows us to accept form data to login using
    # username and password. Username could be email, name or username, but it will be under attribute .username

    # Get user with email id
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # Verify if the password is correct
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # Create and return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
