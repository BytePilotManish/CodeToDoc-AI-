from fastapi import FastAPI, Depends
import backend.models
import backend.services
from backend.services import get_user_service

app = FastAPI()

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to Sample API"}

@app.get("/users/{user_id}")
def read_user(user_id: int, q: str = None):
    """
    Retrieve user details by ID.
    
    Args:
        user_id (int): The unique identifier for the user.
        q (str, optional): An optional query parameter.
    """
    return {"user_id": user_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    """
    Create a new item in the system.
    """
    return item
