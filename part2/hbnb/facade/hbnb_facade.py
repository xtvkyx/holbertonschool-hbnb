"""Facade to simplify communication between API and business/persistence."""
from __future__ import annotations

from typing import Dict, List

from hbnb.persistence.repository import InMemoryRepository
from hbnb.business.models.user import User


class HBnBFacade:
    def __init__(self) -> None:
        self.repo = InMemoryRepository()
        # Enforce unique email for users
        self.repo.register_unique_field("User", "email")

    # -------- Users --------
    def create_user(self, data: Dict) -> User:
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
            is_admin=data.get("is_admin", False),
        )
        return self.repo.add(user)

    def get_user(self, user_id: str) -> User | None:
        return self.repo.get(User, user_id)

    def list_users(self) -> List[User]:
        return self.repo.list(User)

    def update_user(self, user_id: str, data: Dict) -> User:
        user = self.get_user(user_id)
        if user is None:
            raise KeyError("User not found")

        # Only allow updating these fields
        if "first_name" in data:
            user.first_name = User._validate_name(data["first_name"], "first_name")
        if "last_name" in data:
            user.last_name = User._validate_name(data["last_name"], "last_name")
        if "email" in data:
            user.email = User._validate_email(data["email"])

        # DO NOT allow password updates in this task
        # If you want to explicitly reject it:
        if "password" in data or "password_hash" in data:
            raise ValueError("Password update is not allowed here")

        return self.repo.update(user)
