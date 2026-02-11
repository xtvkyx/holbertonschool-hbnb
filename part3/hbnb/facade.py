from hbnb.models.user import User
from hbnb.repositories.user_repository import UserRepository


class HBnBFacade:
    """Facade using UserRepository for user operations."""

    def __init__(self, user_repo=None):
        self.user_repo = user_repo or UserRepository()

    def create_user(self, email: str, password: str, **kwargs) -> User:
        if self.user_repo.get_by_email(email):
            raise ValueError("email already exists")

        user = User(
            email=email,
            is_admin=bool(kwargs.get("is_admin", False))
        )
        user.set_password(password)

        if "first_name" in kwargs:
            user.first_name = kwargs["first_name"]
        if "last_name" in kwargs:
            user.last_name = kwargs["last_name"]

        return self.user_repo.add(user)

    def get_user(self, user_id: str):
        return self.user_repo.get(User, user_id)

    def list_users(self):
        return self.user_repo.get_all(User)

