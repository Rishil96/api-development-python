import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import status, Response
from schema import Post
from database import get_db_connection


app = FastAPI()


# Home Route
@app.get("/")
def home():
    return {"message": "Welcome to Home Page!"}


# Read all posts
@app.get("/posts")
def get_all_posts():
    conn = get_db_connection()                      # Get DB Connection
    cursor = conn.cursor()                          # Get cursor object
    cursor.execute("""SELECT * FROM posts""")       # Build query to get all posts
    all_posts = cursor.fetchall()                   # Fetch all posts using cursor query
    cursor.close()                                  # Close cursor and connection object
    conn.close()
    return {"content": all_posts}


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):                                            # Get DB Connection
    conn = get_db_connection()                                          # Get cursor object
    cursor = conn.cursor()
    cursor.execute("""INSERT into posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))          # Build query to insert a post record in table
    new_post = cursor.fetchone()
    conn.commit()                                                       # Commit changes in database
    cursor.close()                                                      # Close connection and cursor object
    conn.close()
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


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
