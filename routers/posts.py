from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
import schema
import models
from database import get_db
from typing import List


router = APIRouter(prefix="/posts")


# Read all posts
@router.get("/", response_model=List[schema.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.BlogPost).all()
    return all_posts


# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.Post, db: Session = Depends(get_db)):
    new_post = models.BlogPost(**post.dict())           # Create a new BlogPost as per SQLAlchemy model schema
    db.add(new_post)                                    # Add new BlogPost to database
    db.commit()                                         # Commit the changes
    db.refresh(new_post)                    # Refresh the new post to get details added at DB end (e.g. id, created_at)
    return new_post


# Read a post with ID
@router.get("/{pid}", response_model=schema.PostResponse)
def get_post(pid: int, db: Session = Depends(get_db)):
    # Use filter to mimic WHERE clause in SQL and .first() to get the first match in table
    post = db.query(models.BlogPost).filter(models.BlogPost.id == pid).first()
    # Raise 404 if post is not found
    if not post:
        raise HTTPException(detail=f"Post with ID {pid} not found", status_code=status.HTTP_404_NOT_FOUND)
    return post


# Update an existing post
@router.put("/{pid}", response_model=schema.PostResponse)
def update_post(pid: int, post: schema.Post, db: Session = Depends(get_db)):
    # Build a query to get the post to update
    post_query = db.query(models.BlogPost).filter(models.BlogPost.id == pid)
    # Save the post in a variable by using first
    post_to_update = post_query.first()
    # Raise 404 if post does not exist
    if post_to_update is None:
        raise HTTPException(detail=f"Post with ID {pid} not found", status_code=status.HTTP_404_NOT_FOUND)
    # Update the post using the query variable and pass the below param along with the dictionary of values to update
    post_query.update(post.dict(), synchronize_session=False)
    # Commit the changes and grab the post back from database to return it using the query we built at the start
    db.commit()
    updated_post = post_query.first()
    return updated_post


# Delete a post using ID
@router.delete("/{pid}")
def delete_post(pid: int, db: Session = Depends(get_db)):
    # Get post using query and filter
    post = db.query(models.BlogPost).filter(models.BlogPost.id == pid).first()
    # Raise 404 if post does not exist
    if post is None:
        raise HTTPException(detail=f"Post with ID {pid} not found", status_code=status.HTTP_404_NOT_FOUND)
    # Delete the post using db.delete and commit the changes
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


