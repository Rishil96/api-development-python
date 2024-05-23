from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
import schema
import utils
from database import get_db


router = APIRouter(prefix="/users")


# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Hash the user password before storing it in database
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())           # Create user by passing dict of pydantic model into SQLAlchemy User
    db.add(new_user)                                # Add new user into the database
    db.commit()                                     # Commit changes into the database
    db.refresh(new_user)                            # Refresh the new user with database details like created_at, id.
    return new_user


# Get user with id
@router.get("/{uid}", response_model=schema.UserResponse)
def get_user(uid: int, db: Session = Depends(get_db)):
    print("Getting user with id:", uid)
    user_get = db.query(models.User).filter(models.User.id == uid).first()
    if user_get is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {uid} does not exist")
    return user_get
