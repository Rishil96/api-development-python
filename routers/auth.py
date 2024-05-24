from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schema import UserLogin
import models
import utils


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credential: UserLogin, db: Session = Depends(get_db)):
    # Get user with email id
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # Verify if the password is correct
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # Create and return token
    return {"token": "example token"}
