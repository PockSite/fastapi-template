from fastapi.params import Depends
from app.repository.repository import Repository
from app.core.security import verify_access_token

class UserService:
    def __init__(self, repo: Repository):
        self.repo = repo
    
    def register_user(self, user_id: int, email: str, name: str, token: str):
        payload = verify_access_token(token)
        if (payload is None) or (payload.get("sub") != "server"):
            raise ValueError("Invalid token")
        user_data = {'email': email, 'name': name, 'id': user_id}
        return self.repo.create(user_data)
    
    def get_all_users(self):
        return self.repo.read_all()
    
    def get_current_user(self, token: str):
        payload = verify_access_token(token)
        if payload is None:
            raise ValueError("Invalid token")
        user = self.repo.read_by_id(payload.get("sub"))
        return user