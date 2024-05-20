import uvicorn
from fastapi import FastAPI
from schema import Post


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to Home Page!"}


@app.post("/posts")
def create_post(post: Post):
    return {"data": post.dict()}


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=8000, reload=True)
