from pydantic import BaseModel, EmailStr

class RecipientModel(BaseModel):
    email: EmailStr
    user_type: str  # e.g., "premium", "free", "churned"
    attributes: dict = {}