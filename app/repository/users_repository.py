from sqlalchemy.orm import Session
from app.repository.repository import Repository
from app.models.user import User


class UsersRepository(Repository[User, int]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(self.model).filter(self.model.email == email).first()
