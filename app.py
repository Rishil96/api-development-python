import uvicorn
from fastapi import FastAPI
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
@app.post("/posts")
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


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
