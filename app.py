import uvicorn
from fastapi import FastAPI, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schema import Post, PostResponse
from database import engine, get_db
import models

# Code that will create the tables in database represented by our models if they don't exist
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Home Route
@app.get("/")
def home():
    return {"message": "Welcome to Home Page!"}


# Read all posts
@app.get("/posts", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.BlogPost).all()
    return all_posts


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.BlogPost(**post.dict())           # Create a new BlogPost as per SQLAlchemy model schema
    db.add(new_post)                                    # Add new BlogPost to database
    db.commit()                                         # Commit the changes
    db.refresh(new_post)                    # Refresh the new post to get details added at DB end (e.g. id, created_at)
    return new_post


# Read a post with ID
@app.get("/posts/{pid}", response_model=PostResponse)
def get_post(pid: int, db: Session = Depends(get_db)):
    # Use filter to mimic WHERE clause in SQL and .first() to get the first match in table
    post = db.query(models.BlogPost).filter(models.BlogPost.id == pid).first()
    # Raise 404 if post is not found
    if not post:
        raise HTTPException(detail=f"Post with ID {pid} not found", status_code=status.HTTP_404_NOT_FOUND)
    return post


# Update an existing post
@app.put("/posts/{pid}", response_model=PostResponse)
def update_post(pid: int, post: Post, db: Session = Depends(get_db)):
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
@app.delete("/posts/{pid}")
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


# Test DB Connection using SQLAlchemy
@app.get("/sqlalchemy")
def test_sql_db(db: Session = Depends(get_db)):
    all_posts = db.query(models.BlogPost).all()
    return {"data": all_posts}


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
