import backend.utils
from backend.utils import format_date, generate_id

def get_user_service(user_id: int):
    """
    Business logic for fetching user information from the database.
    
    Args:
        user_id (int): ID of the user to fetch.
        
    Returns:
        dict: User data mapping.
    """
    return {"id": user_id, "name": f"User {user_id}", "role": "admin"}

def calculate_tax(price: float, rate: float = 0.15):
    """
    Calculate tax for a given price and rate.
    """
    return price * rate
