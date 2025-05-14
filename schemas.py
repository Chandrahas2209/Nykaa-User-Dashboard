from pydantic import BaseModel, EmailStr
from datetime import datetime
# Request schema for creating a user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
# Request schema for updating a user
class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str
# Response schema for returning user data
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    login_count: int

    class Config:
        from_attributes = True
