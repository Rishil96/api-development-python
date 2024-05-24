import uvicorn
from fastapi import FastAPI
from database import engine
import models
from routers import posts, users, auth

# Code that will create the tables in database represented by our models if they don't exist
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


# Home Route
@app.get("/")
def home():
    return {"message": "Welcome to Home Page!"}


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
