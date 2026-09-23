from app.repository.users_repository import UsersRepository


class UserService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def get_all_users(self):
        return self.repo.read_all()

    def get_user_by_id(self, user_id: int):
        return self.repo.read_by_id(user_id)

    def get_user_by_email(self, email: str):
        return self.repo.find_by_email(email)

    def create_user(self, name: str, email: str):
        return self.repo.create({"name": name, "email": email})

    def update_user(self, user_id: int, name: str, email: str):
        return self.repo.update(user_id, {"name": name, "email": email})

    def delete_user(self, user_id: int):
        return self.repo.delete(user_id)
