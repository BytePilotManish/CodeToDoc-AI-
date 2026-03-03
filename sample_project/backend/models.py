from pydantic import BaseModel
from typing import List, Optional
import backend.database

class User(BaseModel):
    """
    Data model representing a system user.
    """
    id: int
    username: str
    email: str

class Item(BaseModel):
    """
    Data model representing a catalog item.
    """
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []
