import uvicorn
from fastapi import FastAPI, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import Post
from database import get_db_connection, engine, get_db
import models

# Code that will create the tables in database represented by our models if they don't exist
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Home Route
@app.get("/")
def home():
    return {"message": "Welcome to Home Page!"}


# Read all posts
@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.BlogPost).all()
    return {"content": all_posts}


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.BlogPost(**post.dict())           # Create a new BlogPost as per SQLAlchemy model schema
    db.add(new_post)                                    # Add new BlogPost to database
    db.commit()                                         # Commit the changes
    db.refresh(new_post)                    # Refresh the new post to get details added at DB end (e.g. id, created_at)
    return {"data": new_post}


# Read a post with ID
@app.get("/posts/{pid}")
def get_post(pid: int):
    conn = get_db_connection()                                              # Get connection and cursor object
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(pid)))     # Build query to select a post
    post = cursor.fetchone()                                                # Fetch the post
    if not post:                                                            # Raise exception if post not found
        raise HTTPException(detail=f"Post with ID {pid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    cursor.close()
    conn.close()
    return {"data": post}


# Update an existing post
@app.put("/posts/{pid}")
def update_post(pid: int, post: Post):
    conn = get_db_connection()                                              # Create DB connection and cursor
    cursor = conn.cursor()
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(pid)))    # Build query using cursor
    updated_post = cursor.fetchone()                                        # Fetch updated post
    if not updated_post:                                                    # Raise exception if post not found
        raise HTTPException(detail=f"Post with ID {pid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()                                                           # Commit changes in database
    cursor.close()                                                          # Close connection and cursor
    conn.close()
    return {"data": updated_post}


# Delete a post using ID
@app.delete("/posts/{pid}")
def delete_post(pid: int):
    conn = get_db_connection()                                                      # Get DB Connection and cursor obj
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(pid))     # Build query to delete a post
    deleted_post = cursor.fetchone()                                                # Fetch deleted post
    if not deleted_post:                                                            # Raise exception if post not exists
        raise HTTPException(detail=f"", status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()                                                                   # Commit changes to database
    cursor.close()                                                                  # Close connection and cursor obj
    conn.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Test DB Connection using SQLAlchemy
@app.get("/sqlalchemy")
def test_sql_db(db: Session = Depends(get_db)):
    all_posts = db.query(models.BlogPost).all()
    return {"data": all_posts}


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
