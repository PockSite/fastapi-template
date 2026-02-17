from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    id: int
    name: str
    email: EmailStr

