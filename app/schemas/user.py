from pydantic import BaseModel, EmailStr, Field


class UserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
