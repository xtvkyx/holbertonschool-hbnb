from typing import Optional
from hbnb.repositories.sqlalchemy_repository import SQLAlchemyRepository
from hbnb.models.user import User


class UserRepository(SQLAlchemyRepository):
    """User-specific repository with custom queries."""

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()
