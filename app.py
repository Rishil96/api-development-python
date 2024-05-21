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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"content": all_posts}


# Create a new post
@app.post("/posts")
def create_post(post: Post):
    return {"data": post.dict()}


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
