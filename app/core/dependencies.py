
from fastapi import Depends
from app.core.database import get_db
from app.repository.users_repository import UsersRepository
from app.service.user_service import UserService

def get_user_service(db = Depends(get_db)):
    repo = UsersRepository(db)
    return UserService(repo)

def get_auth_service(db = Depends(get_db)):
    repo = UsersRepository(db)
    return UserService(repo)
