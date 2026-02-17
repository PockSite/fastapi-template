from app.repository.repository import Repository
from app.models.user import User

class UsersRepository(Repository[User]):
    def __init__(self, db):
        super().__init__(db, User)
